---
title: obs-wiki — 本知识库
tags: [元项目, 知识管理, LLM]
status: active
created: 2026-05-25
updated: 2026-05-27
repo: ""
sources: [raw/notes/karpathy-llm-wiki.md]
---

## 概述

obs-wiki 是这个仓库本身。它既是工具（你正在用的知识管理系统），也是 [[concepts/llm-wiki-pattern]] 的最小可运行示范。

设计意图：
- **raw → wiki → journal 三层**：原始素材不可变 → LLM 编译的知识层可累积修订 → 变更日志追溯审计
- **Claude 维护，人类审核**：Claude 生成草稿和交叉引用，人类通过 `git diff` 决定是否采纳
- **概念页是节点，wikilink 是边**：知识价值在连接而非孤立条目；新建页面必须接入现有图

## 关键决策

- **不上数据库**：纯 Markdown + 文件系统。Git 是版本控制 + 协作通道 + 备份
- **不自动 commit**：所有 Claude 生成的变更必须人类审核 `git diff` 后再 commit。这是知识库可信度的最后防线
- **甜蜜区 50-200 条目**：超过 200 条需要更复杂的工程（分层记忆 / 冲突检测），目前规模内不优化
- **lint 是质量底线**：`python scripts/lint.py` 抓断链 / 孤立页 / 缺失 frontmatter，是 ingest 之后的强制 gate

## 经验教训

- **孤立页面是失败信号**：一次 ingest 如果只新建一个页面没动其他，说明没扫够现有 wiki，应回到"找连接点"步骤重做
- **index 是导航不是规范层级**：同一概念可以在多处出现（如某个概念既属"方法论"又属"AI 工程"），两边都列是对的
- **journal 不是摘要**：journal 应该写"今天看到了什么观点/事实/决策"，不要用 `→ 新建 [[xxx]]` 开头占位——读者关心内容不关心生成了哪些文件
- **每条关键提取必须带 `→ [[xxx]]` 连接**：连接是这套方法论的核心价值，不是装饰

## 相关概念

- [[concepts/llm-wiki-pattern]] — 本项目的方法论来源
