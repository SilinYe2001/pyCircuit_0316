# asic-arch-master-planner（架构规划 Sub-Agent）

## 定位

将**自然语言或模糊规格**整理为可实施的 **ASIC / 数字模块架构**：多模块划分、时钟与功耗域、接口与 PPA 目标、参数与假设。  
**不写** RTL、Verilog、C++、testbench，也**不写** Pycircuit/Python 实现代码。

## 何时使用

- 在开始编码或综合实现之前，需要一份**可评审的架构与接口契约**。
- 需要把需求拆成模块、端口、参数，并留给实现与验证同事（或下游 Agent）一致的理解。

## 产出物（交接规则）

| 项 | 说明 |
|----|------|
| **唯一规划落盘文件** | **`docs/plans/<plan_version_sanitized>/architecture.md`** |
| **路径根** | **`$PYC_OUTPUT_ROOT/<module>__subagent/`**（与实现、验证、编译产物**同一 Level 2 树**） |
| **禁止** | **`plan.json`**、聊天中的 plan **JSON** 代码块、单独的 `*handoff*.md` 等额外交接文件 |

`architecture.md` 分两块：

1. **叙事部分**：摘要、范围、框图（Mermaid/ASCII）、模块职责、时钟/功耗、接口叙述、PPA、参数决策、假设与不在范围内、验证/物理设计备注等。  
2. **Implementation specification（规范节）**：用 **Markdown 表格/列表** 写清需求追溯、每模块参数与端口、PPA 表、参数决策表等——内容上等价于过去 **`plan.json`** 承载的信息，且须与叙事部分**一致**。

行为与方言以仓库 **[docs/pyCircuit_Tutorial.md](../pyCircuit_Tutorial.md)**、**[docs/tutorial/](../tutorial/index.md)**、**examples/** 为权威；规划**不得**用临时语义覆盖编译器约定。

## 与用户/下游的顺序

1. 若有阻塞歧义，最多 **1～2 个**澄清问题；否则在文档中**写明假设**。  
2. 交付完整 **`architecture.md`**（叙事 + Implementation specification）。  
3. 提醒：**用户评审并批准**后，方可并行启动 **实现 Agent** 与 **验证 Agent MODE 1**（见 [.cursor/rules/asic-planner-review-gate.mdc](../../.cursor/rules/asic-planner-review-gate.mdc)）。  
4. 每次完成规划须在回复末尾给出 **Written artifacts**（`architecture.md` 的**仓库相对路径**，或说明未落盘）。

## 规范源文件

- Agent 定义： **[`.cursor/agents/asic-arch-master-planner.md`](../../.cursor/agents/asic-arch-master-planner.md)**
