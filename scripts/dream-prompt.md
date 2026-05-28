# Dream Task — 知识库周期性整合

> **工具名约定**：本文档中提到的 `Read` / `Grep` / `Glob` / `Edit` / `WebSearch` / `WebFetch` / `CronCreate` / `ToolSearch` 是 Claude Code 的内置工具命名。其他 agent（Codex CLI / Cursor / Cline / aider 等）使用等价能力即可——名字不同但语义同源（读文件 / 模糊搜文件 / 文件名匹配 / 行替换 / 网页搜索 / 网页抓取 / 定时任务 / 工具发现）。把这份 prompt 喂给任何 reasoning-capable agent 都应该能跑完。

你正在本知识库仓库根目录执行一次 "dream" 任务。目的是为知识库生成一份**分诊队列**，让用户审阅、决定是否采纳，**不要直接改正式 wiki 页面**。

类比：模仿"REM 睡眠"的整合过程——把最近摄取的 raw 素材与已有 wiki 知识层做一次离线匹配，找出该成页未成页的概念、该连未连的交叉引用、彼此矛盾或过时的论断。

---

## 硬约束

1. **只允许写一个文件**：`wiki/journal/dream-{today}.md`（today 用 ISO 格式 YYYY-MM-DD）
2. **不准修改**：`wiki/concepts/*`、`wiki/projects/*`、`wiki/index.md`、`raw/**`、任何已有 journal 文件
3. **不准 git commit**——用户会人工 review 后 commit
4. 如果 `dream-{today}.md` 已存在，追加 `## 第 N 次` 段落，不覆盖
5. 完成主任务后必须重新调度下一次 dream（见末尾「Reschedule」）

## 输入采集（高效采样，不要穷举读取）

```bash
# 1. 最近 7 天新增/修改的 raw 素材
find raw -name '*.md' -mtime -7

# 2. 最近 14 天的 raw（用于「概念候选」交叉验证）
find raw -name '*.md' -mtime -14

# 3. lint 结构报告
python scripts/lint.py
```

然后：
- Read `wiki/index.md` 全文（这是导航图）
- Glob `wiki/concepts/*.md` 和 `wiki/projects/*.md`，只看文件名（不读 body）
- Read 最近 3 篇 `wiki/journal/*.md`（按文件名日期排序，跳过 dream-* 文件）

**不要**逐个 Read 几十个 wiki 概念页——太贵。需要时按文件名推测，或针对具体怀疑点 Grep。

## 三类分析

### Bucket 1: 概念候选（raw 高频出现，wiki 未成页）

判定规则：一个主题在 raw（最近 14 天）≥3 个不同文件中出现，但 `wiki/concepts/` 下没有对应页。

每条输出：
- 建议页名：`wiki/concepts/xxx.md`
- 出现的 raw 文件路径（≥3 个）
- 一句"为什么值得成页"（不要泛泛说"重要"，说出独特角度）

**反例**：一个主题虽出现多次但只是别人转述同一来源——不算候选。先 Grep 验证是独立来源。

### Bucket 2: 未捕捉的交叉引用

判定规则：两个已有 wiki 页面共享一个明显概念，但互相没有 `[[wikilink]]`。

每条输出：
- 页面 A ↔ 页面 B
- 共享的概念（一句话）
- 建议方向（双向 / 单向）

**起点**：lint 输出里的"孤立页"列表——它们最缺连接。

**反例**：两个页面只是"都跟 AI 有关"——这种关联太弱不算。要有具体共享概念。

### Bucket 3: 矛盾 / 过时

判定规则：wiki 页面里的论断互相打架，或被更新的 raw 素材推翻。

每条输出：
- 涉及页面（路径）
- 冲突点：两边各引用一两句原文
- 倾向：哪个 source 更新 / 更权威（不要替用户拍板，只给信号）

如某 bucket 当周无内容，写「（本周无）」——**不准编**。

## 输出格式

写入 `wiki/journal/dream-{today}.md`：

```markdown
---
title: Dream {today}
type: dream
created: {today}
scan_window: {today-7} ~ {today}
---

# Dream {today}

> 自动生成的分诊队列。每条都是建议，请人工 triage 后再决定是否落地。

## 1. 概念候选

...

## 2. 未捕捉的交叉引用

...

## 3. 矛盾 / 过时

...

## 4. Lint 结构问题摘要

（粘贴 `scripts/lint.py` 输出的关键部分，不要全量贴）
```

## Reschedule（必须执行）

dream 任务的最后一步——重新调度下周日同时间的下一次 dream，否则链条断掉。

1. 用 `python -c "import datetime; d=datetime.date.today(); n=d+datetime.timedelta(days=(6-d.weekday())%7 or 7); print(n.day, n.month)"` 算出下周日的日和月
2. 如果 CronCreate 工具未直接可用，先 `ToolSearch` query `select:CronCreate` 加载 schema
3. 调用 CronCreate：
   - `cron`: `"{minute} 9 {dom} {month} *"` —— minute 用 7、13、47 等非整点值，避开 :00
   - `recurring`: `false`（一次性，由本任务自延续）
   - `durable`: `true`（跨 session 保留）
   - `prompt`: `"读取 scripts/dream-prompt.md 并按其指令执行 dream 任务。"`

完成后简短输出：
```
Dream complete. Wrote wiki/journal/dream-{today}.md.
Next dream scheduled: {next_sunday} 09:{minute}.
```

## 时间预算

整个任务目标 ≤ 5 分钟、≤ 30 个工具调用。如果时间不够，宁可 bucket 写得简短，也要确保完成 reschedule——链条断了比内容稀薄更糟。
