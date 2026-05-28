# 个人知识库 — Schema

这是一个基于 LLM Wiki 模式的个人知识管理系统。所有知识以 Markdown 文件形式存储，Agent（Claude Code / Codex CLI / Cursor / Cline / aider 等）负责自动化维护，人类负责审核确认。

本文件遵循 [agents.md](https://agents.md) 跨 agent 规范，主流 agent 启动时会自动读取。

## 目录结构

```
raw/           原始素材（不可变，只增不改）
  notes/       个人笔记、想法、灵感、研究过程快照
  snippets/    代码片段、技术方案、架构记录
wiki/          编译后的知识层（agent 维护）
  index.md     主索引
  concepts/    概念页（长期维护的知识节点）
  projects/    项目页
  reports/     研究报告（一次性、自洽叙事、综合多 concept 的深度产物）
  journal/     变更日志
templates/     页面模板（concept.md / project.md / report.md）
scripts/       工具脚本
```

## 页面格式

所有 wiki 页面必须包含 YAML frontmatter：

```yaml
---
title: 页面标题
tags: [tag1, tag2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: [raw/notes/xxx.md, raw/snippets/yyy.md]
---
```

项目页额外包含 `status: active|paused|archived` 和 `repo:` 字段。

## 链接格式

使用 `[[wikilink]]` 格式进行交叉引用：
- 概念页：`[[concepts/页面名]]`
- 项目页：`[[projects/页面名]]`
- 链接文本不含 `.md` 后缀

## 操作规则

### Ingest（摄取）

当用户要求摄取新内容时：

1. 读取 `raw/` 中指定的素材（如果是 URL，先按下方"外部素材抓取"小节落 raw）
2. 提炼关键概念、决策、经验
3. 检查 wiki 中是否已有相关页面：
   - 已有 → 更新页面，补充新信息，标注新 source
   - 没有 → 按 `templates/` 中的模板创建新页面
4. 更新所有受影响页面的交叉引用 `[[wikilink]]`
5. 更新 `wiki/index.md` 索引
6. 在 `wiki/journal/` 中记录本次变更（文件名格式：`YYYY-MM-DD.md`）

每次 ingest 通常影响 3-10 个页面。不要只创建一个孤立页面。

#### 外部素材抓取（绕过反爬）

公开网页一般直接用 agent 自带的抓取工具（Claude Code 的 `WebFetch`、Codex 的 `web_fetch` 等价能力）就够了。但有两类高价值源默认会被拦——遇到时按以下方法绕过，抓到原文后再落 `raw/notes/`。

**X.com / Twitter**（未登录直访返回 402，Nitter SSL 失败，vxtwitter 只重定向）

唯一稳定的免登录通道是 fxtwitter 的 JSON API：

```bash
curl -s https://api.fxtwitter.com/{user}/status/{id} | python3 -m json.tool
```

- 短推：正文在 `tweet.text`
- X Article（长文形态）：`tweet.text` 为空；正文在 `tweet.article.content.blocks[]`，按数组顺序拼接每个 block 的 `text`；标题在 `tweet.article.title`
- 元数据可取：`tweet.{likes, retweets, views, bookmarks, created_at}`、`tweet.author.{name, screen_name, description}`——落 raw 时附"传播规模"标注，方便后续判断该论点的扩散范围

**微信公众号（mp.weixin.qq.com）**（WebFetch 直访会撞"环境验证"反爬墙，返回验证页而非正文）

绕过方式：用 iPhone Safari User-Agent 走 curl 拿完整 HTML，再提正文：

```bash
curl -s -A "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" \
  "https://mp.weixin.qq.com/s/{id}" -o /tmp/wx.html
# 正文在 <div id="js_content"> 内，可用 BeautifulSoup 或简单 regex 提取
```

公众号链接常带 `__biz` 等参数，**保留完整原 URL（含参数）作为 sources 元数据**，便于以后回溯。

#### `wiki/index.md` 设计原则：扫标题模式

index 是知识库最重要的导航入口，**设计假设是读者扫读条目标题，不是细读描述**。所有条目格式规则都从这个假设推导：

- **每条 ≤ 1 行（约 120 字符）硬约束**——超出说明信息密度不对，要么压缩要么拆页
- **描述写"为什么这条值得点开"，不是"这条页面的内容摘要"**
  - 反例：`减重原理：基础代谢 1500-1800 kcal / 蛋白质 1.6g/kg / 缺口 500 kcal/天 / 周减 0.5kg`（一串数字扫读时进不了脑子）
  - 正例：`减重原理：为什么"少吃多动"是对的废话——缺口要靠哪些具体行为撑住`（一句话告诉读者这页解决什么困惑）
- **禁止字段堆砌**：数字、参数、清单这种细节属于概念页内容，不属于 index
- **禁止**：`**粗体**`、`（多层括号细节）`、`/ 斜杠堆要点`、"更新 N 页 / 事实核查 N 项"等统计、把 journal 节标题原样搬过来
- **同一概念可以在多处出现**——index 是导航不是单一规范层级，比如 `番茄工作法` 既是"时间管理方法"组成员，又是"注意力训练"组成员，两边都列是对的

#### 「最近更新」段落格式

- 同样遵守 ≤ 1 行硬约束
- 格式：`- YYYY-MM-DD: 摄取 {素材简述}：{核心内容/观点/事实}`
- **直接描述内容**，不要用"→ 新建 [[xxx]]"开头占主位——读者关心今天摄取了什么观点/事实/决策，不关心生成了哪些文件
- 需要点出页面归属时用自然语言，如"+ 微型工厂概念页"或正文中嵌入 wikilink
- 这段是"什么发生了 + 去哪看详细"的索引，不是 journal 摘要

### Report（深度研究报告）

`wiki/reports/` 承载 concept 页装不下的"自洽叙事 + 多 concept 综合 + 时间点产物"内容。与其他类型的边界：

| | concept 页 | report 页 | raw notes |
|---|---|---|---|
| 定位 | 知识节点 | 一次研究的完整产物 | 原始素材 / 研究过程快照 |
| 时效 | 长期维护，跨摄取累积 | 一次性，特定时间点 | 不可变 |
| 视角 | 中立事实 + 多源 | 作者立场 + 综合论证 | 采证 |
| 阅读 | 索引跳转 | 顺序读完 | 不直接面向读者 |

**何时新建 report**：

- 用户对某个具体论点追问"值得深入研究"
- 一次研究跨越多个已有 concept、单一 concept 装不下
- 需要把原文核对 + 算账 + 论点边界 + 修正决定一站式记录
- 综合判断带作者立场（"知识库初版过简化、本报告做修正"），不适合写入"中立 concept 页"

**何时不要新建 report**：

- 单一概念能讲清楚 → 写 concept 页
- 只是素材沉淀 → 放 raw/notes
- 只是日常 ingest 的摘要 → 写 journal

**操作规则**：

1. 文件名：`YYYY-MM-DD-{topic-slug}.md`，按时间倒序自然排序
2. 必须 frontmatter：`type: report`、`status: draft|published`、`version`、`sources`、`related_concepts`
3. 模板见 `templates/report.md`
4. 一份 report 可以对应多个 raw（采证），可以引用多个 concept（结论散落处的回连）
5. report 修订要 bump `version` 字段；不可静默重写——保留前一版判断作为历史
6. 在 `wiki/index.md` 的 `## 研究报告` 章节挂入口（按时间倒序）
7. 在相关 concept 页的"相关概念"或末尾加 "完整研究链路：→ [[reports/...]]" 回连
8. 在 `wiki/journal/` 中记录新建/修订（与 ingest 同等待遇）

### Query（查询）

当用户提问时：

1. 先在 wiki 页面中查找相关内容
2. 基于已有页面回答，标注引用来源：`（见 [[concepts/xxx]]）`
3. 如果 wiki 中无相关内容，如实告知并建议补充
4. 高质量的回答可以建议转化为新 wiki 页面

### Lint（审查）

当用户要求 lint 或定期维护时：

1. 运行 `python scripts/lint.py` 获取健康报告
2. 根据报告修复问题：
   - 断链 → 创建缺失页面或修正链接
   - 孤立页 → 添加到相关页面的"相关概念"中
   - 缺失字段 → 补全 frontmatter
   - 过时内容 → 标记提醒用户审核

## 协作规则

- **Agent 的角色**：生成草稿、维护交叉引用、记录变更。所有写操作都是建议。
- **人类的角色**：审核变更（通过 git diff）、决定是否采纳、提供原始素材。
- **不要**自动删除任何已有内容，只做增量更新。
- **不要**修改 `raw/` 目录中的文件，它们是不可变的原始记录。
- **不要**在 wiki 页面中编造没有 source 支撑的内容。
- **不要**自动 `git commit` / `git push`——由人类审核 diff 后手动提交。
