# Sub-Agent 说明文档

本目录收录 pyCircuit 仓库中 Cursor **Sub-Agent** 的人类可读说明，便于选型、门禁与路径约定对齐。

| 文档 | Agent | 一句话 |
|------|--------|--------|
| [asic-arch-master-planner.md](asic-arch-master-planner.md) | 架构规划 | 自然语言规格 → 单一 **`architecture.md`**（含规范表格，无 RTL） |
| [pycircuit-implementation-engineer.md](pycircuit-implementation-engineer.md) | 实现工程 | 已批准的 **`architecture.md`** → Mode A（Pycircuit）或 Mode B（手写 Verilog） |
| [asic-verification-mastermind.md](asic-verification-mastermind.md) | 验证 | MODE 1：**`test_plan.md`** + **`verification/`** 下 TB；MODE 2 根据日志改 TB/config（不改 DUT） |
| [monitor.md](monitor.md) | 工作流监控 | **A** 整理 warning/error → **`docs/monitor/`**；**B** 对照 architecture / design / test_plan 输出一致性报告并请你审阅 |
| [output_files_management.md](output_files_management.md) | （规范） | **`PYC_OUTPUT_ROOT`**、Level 1–3 目录、`module__subagent` 与 `compile/` / `verification/` / `logs/` 约定 |

**规范定义（机器/Agent 行为）**仍以仓库内 **[`.cursor/agents/`](../../.cursor/agents/)** 下同名文件为准；若与本文有出入，以 **`.cursor/agents/*.md`** 为准。

**协作顺序与流程图：** [subagent_collaboration_workflow.md](subagent_collaboration_workflow.md)

**产出目录与 `PYC_OUTPUT_ROOT`：** [`.cursor/skills/pycircuit-output-files/SKILL.md`](../../.cursor/skills/pycircuit-output-files/SKILL.md)、[output_files_management.md](output_files_management.md)

**评审门禁：** [.cursor/rules/asic-planner-review-gate.mdc](../../.cursor/rules/asic-planner-review-gate.mdc)
