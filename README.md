# obs — 个人知识库模板

基于 [Andrej Karpathy 提出的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)的个人知识管理仓库模板。Coding agent（Claude Code / Codex CLI / Cursor / Cline / aider 等）负责机械维护——抓取、整理、加交叉引用、做 bookkeeping；人类只做判断——审核、决定采纳、提供素材。

> "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the **bookkeeping**." LLM 擅长的正是这件事。

## 这套方法解决什么问题

普通笔记软件的问题是 **bookkeeping 成本太高**：你看完一篇文章，想把要点提取出来 + 链接到三个月前看过的相关概念 + 更新主索引 + 写一条变更记录——这些都是机械工作，但加起来比读原文还累。于是大多数人最终就停在"剪藏"层，知识无法沉淀。

LLM Wiki 把这件事翻转：**人提供素材和判断，LLM 做所有 bookkeeping**。你把一篇文章粘进会话，agent 自动：

1. 落到 `raw/notes/` 作为不可变原始素材
2. 提炼关键论点，扫描已有 `wiki/concepts/` 找连接点
3. 新建或更新概念页，加上 `[[wikilink]]` 交叉引用
4. 更新 `wiki/index.md` 主索引
5. 在 `wiki/journal/` 写一条今日变更日志

你审核 `git diff`，满意就 commit。不满意改动后再 commit。

## 目录结构

```
raw/             原始素材（不可变，只增不改）
  notes/         笔记、文章、对话、研究素材
  snippets/      代码、配置、技术决策片段
wiki/            编译后的知识层（agent 维护）
  index.md       主索引
  concepts/      概念页（长期维护的知识节点）
  projects/      项目页
  reports/       研究报告（一次性、多 concept 综合的深度产物）
  journal/       变更日志（每次 ingest 一条）
templates/       页面模板（concept / project / report）
scripts/         lint.py 检健康、build.py 生成静态站
AGENTS.md        ⭐ 给 agent 看的完整 schema 与操作规则（agents.md 跨 agent 规范）
CLAUDE.md        指向 AGENTS.md 的转发文件（兼容只识别 CLAUDE.md 的旧版本 Claude Code）
```

## 快速开始

```bash
# 1. fork 或 clone 本仓库
git clone <your-fork> my-wiki && cd my-wiki

# 2. 清空示范内容（保留 templates / scripts / AGENTS.md / CLAUDE.md）
rm wiki/concepts/*.md wiki/projects/*.md wiki/journal/*.md
echo "# 知识库索引" > wiki/index.md

# 3. 编辑 AGENTS.md 适配你的偏好（标签体系、tone、术语对齐等）

# 4. 在仓库根启动你的 coding agent，然后说：
#    「摄取这篇文章：<URL>」「摄取这段对话：<粘贴正文>」

# 5. lint 检查健康度
python scripts/lint.py
```

## 跨 agent 支持

仓库根的 `AGENTS.md` 是规范本体，遵循 [agents.md](https://agents.md) 跨 agent 约定。常见 agent 的识别情况：

| Agent | 默认识别的规范文件 | 本仓库适配方式 |
|---|---|---|
| Claude Code | `CLAUDE.md` + `AGENTS.md` | `CLAUDE.md` 是 1 行 stub 转发到 `AGENTS.md`，两边都生效 |
| Codex CLI | `AGENTS.md` | 原生支持 |
| Cursor | `.cursorrules` / `.cursor/rules/` | 可加一个 1 行 stub：`See AGENTS.md` |
| Cline | `.clinerules` | 同上 |
| aider | `CONVENTIONS.md`（需在 `.aider.conf.yml` 指定） | 可加 stub 或直接 `read: AGENTS.md` |

规范本体只放一份（`AGENTS.md`）避免漂移，其他 agent 的入口文件用一行 stub 转发即可。

`scripts/dream-prompt.md` 里出现的 `Read` / `Grep` / `Edit` / `WebFetch` / `CronCreate` 等是 Claude Code 的工具命名，其他 agent 用等价能力（读文件 / grep / 行替换 / 网页抓取 / 定时任务）即可——dream-prompt 开头有说明。

## 示范内容

为了让你看到这套方法跑起来是什么样子，仓库带了 9 个示例概念页 + 1 个示例项目页 + 1 个示例 journal。覆盖思维方法、AI 时代认知不对称、个人成长三个主题。可以从 [`wiki/index.md`](wiki/index.md) 进。

清空示范内容后，仓库结构本身就是空模板。

## 设计原则

仓库的 schema 设计假设和取舍写在 [`AGENTS.md`](AGENTS.md) 里，包括：

- **每次 ingest 必影响 3-10 个页面**——孤立创建一个新页面是失败信号
- **index 是导航不是规范层级**——同一概念可以在多处分类下出现
- **journal 写"今天看到了什么观点"，不写"创建了哪些文件"**——读者要内容不要清单
- **concept 中立 / report 带立场 / raw 不可变**——三类页面边界明确
- **不自动 commit**——人类审核 `git diff` 是质量底线

## 工具脚本

- `scripts/lint.py` — 检查断链 / 孤立页 / 缺失 frontmatter，是 ingest 之后的强制 gate
- `scripts/build.py` — 把 wiki 渲染成静态 HTML 站（可选，纯阅读用）
- `scripts/dream-prompt.md` — 周期性"dream"任务的 prompt：扫最近 raw + 已有 wiki，生成"该成页未成页 / 该连未连 / 矛盾过时"三类分诊队列。配合 cron 触发，让知识库会自我反思

## Credits

- 方法论来源：[Andrej Karpathy 论 LLM Wiki](https://x.com/karpathy)
- 本仓库是该思路的一种具体落地，不代表唯一解。schema 细节、工作流约束、journal 措辞密度都可以按你自己的偏好调整
