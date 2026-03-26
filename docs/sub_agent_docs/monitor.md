# monitor（工作流监控 Sub-Agent）

## 定位

在 **`module__subagent`** 同一棵产出树下，做两类**只读汇总与交叉校验**（默认**不改**架构/设计笔记/测试计划/DUT/TB，除非用户另行要求你改文件）：

1. **执行摘要（Function A）**：把后台/脚本/编译/仿真里出现的 **warning、error** 分条整理（来源、摘录、可能原因、建议处理与升级对象），落盘为 Markdown。  
2. **规格一致性（Function B）**：对照 **`architecture.md`**、**`docs/design/*.md`**（实现侧可选笔记）、**`test_plan.md`**，找出**偏差**并生成报告，**提示你人工审阅**。

规范行为以 **[`.cursor/agents/monitor.md`](../../.cursor/agents/monitor.md)** 为准。

## 产出路径（与其他 Sub-Agent 同级）

根路径与 Planner/实现/验证相同：

**`$PYC_OUTPUT_ROOT/<module>__subagent/docs/monitor/`**

建议子目录示例：**`docs/monitor/<run_slug>/`**

| 报告类型 | 典型文件名 |
|----------|------------|
| Function A | `execution_digest.md` 或 `execution_digest_<日期>_<时间>.md` |
| Function B | `spec_consistency_report.md` |

## Function A — 何时调用、带什么输入

- **适用**：某次 **`build_verilog.sh` / `run_verilator.sh` / pyCircuit C++ TB / pycc** 等跑完后，日志里有告警或报错。  
- **输入**：用户粘贴日志片段，或给出 **`logs/`**、**`compile/`**、**`verification/obj_*`** 下具体 **`.log` 路径**（仓库相对路径）。  
- **输出**：按条目的 **ID、严重级别、来源工具、摘录、可能原因、建议解决方案**；文首可加汇总表。若无问题，也写简短说明「本次输入内未发现 warning/error」。

## Function B — 何时调用

- **适用**：已有 **`docs/plans/.../architecture.md`**；可选已有 **`docs/design/*.md`**；已有或刚更新 **`docs/test_plans/.../test_plan.md`**。  
- **做什么**：比对 **端口/参数/位宽/时钟复位假设/范围与行为描述** 等；**设计笔记缺失**时会在报告中注明「未对比设计笔记」。  
- **输出**：每条偏差 **C-xxx**、两侧引用、风险、建议以谁为准（通常端口以 **`architecture.md`** 为准）。  
- **必须**：在对话里**明确请你审阅**该报告路径，而不是假定你已同意。

## 与其他 Sub-Agent 的关系

| Agent | 关系 |
|-------|------|
| Planner / 实现 / 验证 | Monitor **不替代**其职责；Monitor 消费其产出与日志 |
| **asic-verification-mastermind MODE 2** | 可先修 TB；Monitor Function A 适合对**当前日志快照**做归档式整理 |

## 延伸阅读

- [subagent_collaboration_workflow.md](subagent_collaboration_workflow.md) — 总流程（已含 Monitor）  
- [pycircuit-output-files SKILL](../../.cursor/skills/pycircuit-output-files/SKILL.md) — `PYC_OUTPUT_ROOT` 与目录层级  
