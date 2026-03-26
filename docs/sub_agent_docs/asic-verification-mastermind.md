# asic-verification-mastermind（验证 Sub-Agent）

## 定位

面向 **pyCircuit 工具链**的验证：**Verilator** 语法/告警、**C++ 周期精确仿真**（见 **[docs/counter_walkthrough.md](../counter_walkthrough.md)**）、以及 **TB / 配置 / 追踪与构建参数** 的排错。  
**不**修改 DUT（Pycircuit 设计源或作为规格的金 RTL）；DUT 或编译器问题应 **上报/升级**，由实现或工具链侧处理。

## 两种模式（每次调用只选其一）

| 模式 | 典型输入 | 输出 |
|------|----------|------|
| **MODE 1 — 测试规划** | 无 C++/仿真日志；已有已批准的 **`architecture.md`** | **`test_plan.md`** + **落盘的 testbench 源码**（须与计划严格一致） |
| **MODE 2 — 日志分析与调试** | 编译/链接/仿真日志、Verilator 告警 + 当前 TB/config 上下文 | **Markdown** 的可执行修改步骤（面向 Coder/实现者） |

正式 **Markdown 交接**仍是 **`test_plan.md`**（替代历史上的 `test_plan.json`）。**MODE 1 不允许「只写计划不写 TB」**：必须在同一次交付中，在 **`…/<module>__subagent/verification/`**（或项目约定的同 Level 2 树下）写入 **`tb_*.py`**（C++ 周期 TB）、**`tb_*.v` / `tb_*.sv`**、wrapper 等，并**逐项落实** `test_plan.md` 中的接口绑定、激励顺序、角例、检查器、VCD/Wrapper 约定等。工具链用的 trace **config** 若计划要求，可含磁盘上的 `.json`，那是**工具配置**，不是子代理之间的 JSON 规格交接。

## MODE 1 — 测试计划 + 配套 testbench

- **前置条件**：与启动 **pycircuit-implementation-engineer** 相同——须已 **评审并批准** **`architecture.md`**。批准后 MODE 1 与实现可 **并行**。  
- **输入**：**`architecture.md`**（叙事 + **Implementation specification**）。  
- **`test_plan.md` 内容**：范围、待测接口、激励策略、检查器与参考、角例、**Trace/VCD 计划**、通过/失败准则、回归分层等。  
- **Testbench 与计划对齐（硬性要求）**  
  - 端口/DUT 例化/位宽与计划及架构一致；计划里写的 wrapper 名、时钟复位、posedge 激励须在 RTL/TB 中实现，**不能**只写在文档里。  
  - C++ 流程遵循 **counter_walkthrough / tutorial**：典型 **drive → step → expect**，每周期驱动全部输入并检查输出。  
  - 计划列出的角例与向量须在 TB 中覆盖（若确需分期，须在 `test_plan.md` 中写明范围；**默认应完整对齐**）。  
  - 若 **`architecture.md`** 与 **`test_plan.md`** 冲突，以 **`architecture.md`** 为准，并同步修正计划与 TB。  
- **落盘**  
  - **`$PYC_OUTPUT_ROOT/<module>__subagent/docs/test_plans/<slug>/test_plan.md`**  
  - **`$PYC_OUTPUT_ROOT/<module>__subagent/verification/`** 下 TB / wrapper 等（布局见 **[pycircuit-output-files skill](../../.cursor/skills/pycircuit-output-files/SKILL.md)**）  
- **Written artifacts**：列出 **`test_plan.md` 与所有 TB/配置文件路径**；不要写 **`test_plan.json`**。

### 纯组合 DUT 与 Wrapper

若 DUT **纯组合**（模块上无 `clk`/`rst`、内部无寄存器），MODE 1 必须在 **`test_plan.md`** 中约定 **Wrapper / TB shell for VCD**，并在 **TB 或 RTL wrapper** 中实现：时钟/复位、按周期打激励、层次与追踪信号与计划一致。

## MODE 2 — 调试

- **可改范围**：**`tb_*.py`**、**`*_config.py`**、trace **配置**、**构建/CLI 参数**。  
- **输出结构建议**：`## Summary` / `## Evidence` / `## Instructions for Coder`。  
- **Written artifacts**：默认 **`Written artifacts: none`**；若写了摘要类 Markdown 可放在 **`logs/`** 等路径并列出。

### Verilator 与 `output_files` 日志

若 shell 将日志写入 **`verification/obj_verilator_*/logs/*.log`**，应使用 **`{ … } 2>&1 | tee "$LOG"`** 与 **`set -o pipefail`**，避免仿真段被截断、看不到 **PASS**。MODE 2：段 1 看 **%Error/%Warning**，段 2 看 **$display / PASS/FAIL**。

## 其他约束摘要

- **默认 C++ TB 流程**对齐 **counter_walkthrough** 与 **[docs/tutorial/](../tutorial/index.md)**；除非用户规格要求，**不**默认推 UVM/SV 大框架。  
- MODE 2 保持简洁 Markdown；MODE 1 以**磁盘上的计划 + TB 一致**为准。

## 规范源文件

- Agent 定义： **[`.cursor/agents/asic-verification-mastermind.md`](../../.cursor/agents/asic-verification-mastermind.md)**
