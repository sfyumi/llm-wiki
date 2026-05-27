---
title: LLM Wiki 模式
tags: [知识管理, LLM, 架构模式]
created: 2026-04-12
updated: 2026-04-17
sources: [raw/notes/karpathy-llm-wiki.md, raw/notes/huxuan-vibe-coding-games-2026.md]
---

## 定义

由 Andrej Karpathy 提出的知识管理范式。核心思想：用 LLM 维护一个**持久化的、编译式的 Wiki** 作为中间知识层，替代传统 RAG 的"每次查询都从零开始"模式。

## 关键要点

- 三层架构：Raw Sources（不可变原始素材）→ Wiki（LLM 维护的 Markdown）→ Schema（规则配置）
- 三个操作：Ingest（摄取）、Query（查询）、Lint（审查）
- 核心洞察："The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the **bookkeeping**." LLM 擅长的正是这种机械性维护工作
- 知识具有复利效应：每次摄取都在已有知识上叠加，而非重新发现
- 甜蜜区在 50-200 条目，超过 200 条目后需要更复杂的工程（分层记忆、冲突检测）

## 同源模式：PDF2GAME（结构化提取另一应用）

腾讯研究院 2026-04 vibe coding 游戏长文（→ `vibe-coding-creator-motives`）介绍了 PDF2GAME 开源工具链：

```
上传图书 → 大模型提取全文 → 结构化为人物/地点/事件等实体 → 衍生互动游戏
```

原型基于江户川乱步《诡计集成》。案例《大明王朝》中玩家可选择扮演嘉靖年间多位历史人物，每个属性值由 AI 结合文本得出，与角色选项相关（高智力角色破局更合理，低武力角色更需要保护）。

**这与 LLM Wiki 模式同源**——都是把非结构化文本（书 / 笔记 / 文章）"编译"为结构化中间层，再在中间层之上做应用：

| 模式 | 输入 | 中间层 | 输出 |
|---|---|---|---|
| LLM Wiki | 笔记 / 文章 | concepts / projects / links | 知识查询 / 摄取 |
| PDF2GAME | 图书 | 人物 / 地点 / 事件实体 | 互动游戏 |

两者验证了"raw → 结构化中间层 → 应用"是 LLM 时代处理非结构化文本的通用范式，应用方向各异（知识管理 vs 互动叙事 vs 推理 vs 决策），但中间层模式同构。

## 相关概念

