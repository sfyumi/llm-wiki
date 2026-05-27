---
title: Agency 框架：定义边界的能力
tags: [设计哲学, 工具, 人机协作, AI, 框架]
created: 2026-04-12
updated: 2026-04-14
sources: [raw/notes/ivan-zhao-agency-muscle.md, raw/notes/mark-cuban-ai-knowledge-democratization.md, raw/notes/creao-ai-first-engineering-2026.md]
---

## 定义

Agency（主动性/判断力）像肌肉一样，用进废退。AI 是放大器——放大你已有的方向，主动学习的人被加速，被动依赖的人被淘汰。关键变量不是工具，是使用者的意图。

## 三个视角

- **Ivan Zhao**（设计者）：Agency is a muscle. Tools can strengthen it — or let it atrophy.
- **职场**：听话是天花板。执行力是下限，判断力是上限。纯执行的人和 AI 竞争同一个生态位。

## Agency vs Deterministic Agent：时序框架

不是二选一，是时序循环：

```
人的 Agency（定义问题/设标准/选方向）
        ↓
Deterministic Agent（在边界内执行/生产/监测）
        ↓
人的 Agency（评估结果/反思/调整边界）
```

**Agency 是操作系统，Agent 是应用程序。** Agency 定义 agent 运行的空间，agent 在空间内执行，agency 再评估调整。

| 概念 | Agency（定义边界） | Agent（边界内执行） |
|------|---------|-------------|
| `harness-engineering` | 写 CLAUDE.md 规则 | Agent 在规则内执行 |
| [[concepts/first-principles-deletion]] | "有必要吗？" | 压缩执行时间 |
| [[concepts/idea-meritocracy]] | 压力测试 → 选方向 | 在选定方向上执行 |
| `orchestration-free-agents` | 设计任务池和规则 | 16 个 Agent 自组织 |

### 实操判断标准

- **不可逆/新领域/反馈慢** → 人的 agency
- **可逆/已定义/反馈快** → deterministic agent

## 经验钙化与柯达陷阱

经验 → 心智模型 → 环境稳定时加速判断（复利）→ 环境变化时变成偏见（路径依赖）。**经验越成功越难放弃**（沉没成本+身份绑定）。不同经验衰减速度不同：

- **领域专精**（"我懂胶片"）→ 半衰期短，柯达陷阱
- **元能力**（"我知道怎么学"）→ 半衰期长，跨环境可迁移
- **判断力**（"我知道什么重要"）→ 最持久但盲区最隐蔽

**成功悖论**：经验最危险的时候恰恰是运行最好的时候。三道防线：压力测试（[[concepts/idea-meritocracy]]）、第一性原理（[[concepts/first-principles-deletion]]）、时序框架的"评估调整"环节。

**AI 积累的是模式，不是经验**——经验需要具身性、时间连续性、利害关系，AI 只有模式。对多数商业应用模式够了，但不可逆高风险决策中差距仍然关键。

### CREAO 实证

CREAO CTO（Peter Pang）在 AI-first 转型中观察到（见 `ai-first-engineering`）：

- **初级工程师比高级工程师适应更快**——没有十年习惯要卸载，工具放大了影响力
- **高级工程师两个月的工作被 AI 一小时完成**——接受这一点需要放弃稀缺技能的身份认同
- **"适应性比积累的技能更重要"**——在环境剧变时，这不是价值判断，是观察事实

这精确对应经验钙化的三层：领域专精（"我懂写代码"）半衰期短→柯达陷阱；元能力（"我知道怎么评估"）半衰期长→架构师角色；判断力（"我知道什么重要"）→最持久但盲区最隐蔽。

## 相关概念

- [[concepts/creative-thinking-shannon]] — Shannon 的"动机"= Agency 的情感基础，建设性不满 = 重新定义边界的冲动
