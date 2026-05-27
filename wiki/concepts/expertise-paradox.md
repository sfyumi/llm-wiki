---
title: 专家悖论：AI 在你不懂的领域看起来神
tags: [AI, 认知, 评估, 判断力, 市场叙事]
created: 2026-04-28
updated: 2026-04-28
sources: [raw/notes/karri-saarinen-some-notes-on-ai-2026-04-26.md]
---

## 定义

AI 在评估者**最不懂**的领域看起来最神奇，在评估者**最懂**的领域看起来最破绽百出。同一份输出在两类观察者眼中评分极度撕裂——这不是模型时好时坏，是观察者判断力的不对称。

Linear CEO Karri Saarinen 在 2026-04-26 X 长文《Some Notes on AI》明确把这个现象命名为 **expertise paradox**，并指出它是 **2026 年 AI 市场叙事极度撕裂的最大单一根因**——不是模型在某些领域真的强、某些领域真的弱，而是观察者在自己懂的领域看到 slop、在不懂的领域看到 magic。

> "AI often feels most impressive in domains where you know the least, which I think it's largest contributor to the dissonance in the market."
> — Karri Saarinen, 2026-04-26

## 双框架：Gell-Mann + Dunning-Kruger 在 AI 时代的合流

Saarinen 把 expertise paradox 的认知机制拆成两个已有概念的合流：

### Gell-Mann Amnesia（Crichton 2002）

Michael Crichton 2002 演讲《Why Speculate?》提出，用物理学家 Murray Gell-Mann 的名字打趣命名（Crichton 自承"借名增重")：

> 你打开报纸，看到自己专业领域的文章——记者完全不懂事实和议题，错得离谱（"湿街道导致下雨"）。然后翻页到国际新闻，**居然又开始相信报纸**。这种健忘只能用 amnesia 解释。

Gell-Mann Amnesia 原本只描述媒体场景。Saarinen 把它移植到 AI 评估场景——AI 输出对你领域内的人是"湿街道导致下雨"，对你领域外的人是权威信息源。

### Dunning-Kruger（Kruger & Dunning 1999）

Cornell 心理学经典，能力低者**高估自己**：因为不知道自己不知道什么，所以无法识别自己的输出有多差。

合流到 AI 评估：

| 你的领域 | 你看 AI 输出的眼睛 | 你给 AI 的评分 |
|---|---|---|
| 你深度懂 | Gell-Mann 模式：看到 slop / 缺上下文 / 编造细节 / 选最显眼路径 / 需要重 steering | 严格、低 |
| 你不懂 | Dunning-Kruger 模式：缺判断什么是缺失的能力 → 看起来 magic | 宽松、高 |

**两个偏差方向相反但效果叠加**——不懂的人给 AI 高分、懂的人给低分，结果就是同一份输出收到极度撕裂的评价。

## 悖论的三层含义

### 第一层：市场叙事撕裂的根因

> "AI capabilities are described and understood as limitless to the casual observer."

Saarinen 指出 2026 时点 AI 市场叙事撕裂的根本——casual observer（不懂目标领域的人）持有"无限能力"印象，因为他们用 Dunning-Kruger 模式评估；deep practitioner 看到具体边界，因为他们用 Gell-Mann 模式评估。两者持有的"AI 能力图景"相差几倍。

这条与 `individual-vs-institutional-ai` "生产力幻觉"（METR 实验：用 AI 实际慢 19%，自认快 20%，感知差 39 个百分点）同源——**自我评估 AI 是 Dunning-Kruger 模式**（你用 AI 是新手，不知道自己不知道什么）。

### 第二层：专家在 AI 时代更难，但更有价值

Saarinen 的核心反直觉判断：

> "**The paradox is that expertise makes AI harder to use, but also more valuable if you know how to wield in a proper way.**"

- **专家用 AI 更难**：因为看到所有 slop，挫败感更强（输出"差不多但不对"比"完全错"更让人崩溃）
- **专家用 AI 更值钱**：因为知道怎么 steer / constrain / evaluate model——novice 没有这层判断，只能接受 AI 第一次输出

这把 [[concepts/experience-over-knowledge]] "AI 让知识贬值、经验升值" 加了一层精确的机制：经验在 AI 时代更值钱，**不是因为 AI 不能做你做的事，是因为 AI 能做但需要被有判断力的人 steer**——专家的角色从"亲自做"变成"设方向 + 设标准 + 评估"。

> "So AI does not remove the value of expertise. It makes expertise more about direction, judgment, and knowing what good looks like."

这与 `aesthetics-beyond-visual` "审美 = 区分能力" 同源——专家的核心价值在区分（什么是好、什么是缺、什么是错），而不是产出。AI 让产出贬值，让区分升值。

### 第三层：销售决策的盲区

含义对采购方、投资人、分析师：**评估 AI 产品时如果你自己不是该领域专家，你的"看起来很神"评分应该被强制打折**。

- 投资人看 AI 法律产品 → 你不是律师 → 你看到的是 magic 不是 slop
- CIO 评估 AI 客服 → 你不是客服一线 → 你看到的是 wow 不是常见漏洞
- 用户买 AI 编程工具 → 你不是有 10 年经验的工程师 → 你看到的是"AI 写出能跑的代码" 不是"AI 写出有维护性问题的代码"

**反过来**，如果某个领域专家说一个 AI 工具好，比 casual observer 说好的 weight 应该高几倍——但 2026 公开市场的报道、社交媒体热度、Twitter 演示视频几乎全部来自 casual observer，这是市场叙事系统性偏向乐观侧的结构性原因。

## 三个领域的具体表现

### 编程

Saarinen 给的具体形态：

> "[In areas you understand deeply,] The output is close but not quite right. It misses context, invents details, chooses the obvious path, or needs heavy steering before it becomes useful."

这与 `vibe-coding-creator-motives` 一线访谈印证——**专业开发者 80% 时间在 debug**（"那个功能没实现 / 你把上一个改坏了"），**普通 vibe coder 6% 完成率**。两者不在同一个评估世界——专业开发者看到 80% 都是修，vibe coder 看到 100% 都是 magic（直到撞到挑战墙）。

### 设计

Saarinen 自己作为前 Airbnb / Coinbase / Linear 设计师的 expert 视角：

> "Image generation seems to break down the more iterations you have. It is hard to make the AI change one specific thing in one specific way. It often changes many things at once."

novice 看 AI 出图 = magic（"它居然能画"）；专业设计师看 AI 出图 = "无法控制单点修改 / 滤镜污染 / 必须重启对话才能修一个细节"。

### 写作

> "This also happens in writing, where asking for one change often causes the model to reshape the entire piece."

novice 看 AI 写作 = "它居然能写完整文章"；专业作者 = "它把我的语调改了 + 它编了一个我没说的事实 + 它把要点顺序换了"。

## 与 `research-preview-pattern` Anthropic Kat Wu "100% 才是真自动化" 的关系

Kat Wu 在 2026-04 给 `ai-first-engineering` 95% 论加了反向硬约束：

> "如果一个自动化不能 100% 工作，那它就不是真正的自动化。"

expertise paradox 给这条硬约束的**心理学解释**——novice 容易满足于 95%（看起来已经很神），expert 才会坚持到 100%（因为只有他们看得到剩下 5% 是什么、为什么必须做掉）。**95% → 100% 的最后一公里就是 expert vs novice 评估差的具体长度**。

CREAO 选 3a（审核也 AI 化）vs 多数企业停 3b（审核保留人工）也是 expertise paradox 的组织化表现——CREAO 团队是 architect（看到剩 5% 必须做），多数企业是 operator（看到 95% 已经很好不想动）。

## 与已有概念的连接

### 同源：Gell-Mann + Dunning-Kruger 的 AI 应用


### 反向力量：判断力 / 审美 / 经验

- [[concepts/experience-over-knowledge]] 经验在 AI 时代升值——本页给"为什么升值"加机制层（专家是 AI 唯一可靠评估者）
- [[concepts/agency-framework]] 经验钙化的反向力量——expert 看到 slop 是判断力的运用，不是钙化

### 应用边界


## 适用边界

- **不是所有 AI 评估都触发 expertise paradox**——任务结果有明确客观判据时（如 unit test 通过 / 数学题答案）任何人都能判断对错
- **Saarinen 给的是观察者层认知机制，不是 AI 能力机制**——本页不主张 AI 真的没用，只主张评估 AI 时观察者要做认知校准

## 可操作的去偏方法

Saarinen 没给具体方法，本页根据机制推论：

1. **强制让目标领域专家做最后审核**——不要让 PM / 销售 / 投资人当评估终审
2. **看专家私下发言而不是公开演示**——公开演示是 Dunning-Kruger 模式的典型场地（演示者也是新手 + 观众也是新手）
3. **延长评估窗口**——magic 印象通常在第一次试用产生，第 5 次、第 50 次试用专家偏差才显现
4. **多 expert 交叉**——不同领域 expert 看到不同的 slop，单一专家也有盲区
5. **承认你自己是 novice**——casual observer 评估 AI 工具时主动给自己评分降权

## 待观察

- 模型变强是否会让 expertise paradox 减弱？理论上 expert 看到的 slop 减少时，novice 与 expert 评分会逐渐收敛——但 Saarinen 在文章里明确说"capabilities 提升后这个 paradox 没消失"
- 是否存在反向 expertise paradox：某些场景下 AI 能力**超过专家**——专家用旧框架评估新能力时反而误判？这是 [[concepts/experience-over-knowledge]] "经验是包袱"的另一种表达
- 这个命名（expertise paradox）会不会成为业界统一术语？2026-04-26 是 Saarinen 首次明确命名移植，传播规模待观察

## 相关概念

- [[concepts/experience-over-knowledge]] — AI 让经验升值的机制层补强：专家是 AI 唯一可靠评估者
- [[concepts/agency-framework]] — 判断力是经验钙化的反向力量
