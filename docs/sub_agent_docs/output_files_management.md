# 输出文件管理规范（可复用）

本文约定 **pyCircuit / pycc / 仿真与验证** 产生物的目录结构，便于按日期与项目归档、避免与源码树混杂。仓库根下 **`output_files_2026-03-24/`** 为按本规范归档的批次（另有符号链接 **`output_files_0324`** 指向同一目录，便于按「0324」检索）。教程与示例脚本默认通过环境变量 **`PYC_OUTPUT_ROOT`**（未设置时即为该日期目录）写入对应子路径。

---

## 目录层级

### Level 1：`output_files_<日期>`

- **命名**：`output_files_YYYY-MM-DD`（UTC 或本地日期二选一，团队内统一即可）。
- **位置**：建议放在**仓库根目录**下，与 `docs/`、`compiler/` 并列；若需集中大文件，可改为仓库外路径并在本文「变体」节说明。
- **作用**：同一天、同一仓库下的多次实验可共用同一 Level 1 文件夹，或按「一次完整跑批」再分子目录（见可选扩展）。

### Level 2：命名约定

- **Sub-agent 工作流（同一 IP）**：使用 **唯一** Level 2 目录 **`<module>__subagent`**（如 `arith_shifter__subagent`）。其下同时放 **`docs/`**、**`pycircuit/`**、**`rtl/`**、**`compile/`**、**`verification/`**、**`logs/`**、shell 脚本等。**禁止**再为同一模块另建无后缀的 **`module/`**，以免出现两套 workflow。
- **未走 Sub-agent 的跑批**：仍可用与 **`__pycircuit_name__`** 一致的 **`module`**（无 `__subagent`），与上互不混用。
- **禁止使用**含糊名如 `run1`、`test`。

### Level 3：产出类型（`docs/` 与 `generated_code/` 同级）

| 文件夹名 | 存放内容 | 典型文件 |
|----------|----------|----------|
| `docs/` | **仅**置于 **`module__subagent`** 下（**与 `generated_code/` 同级**）。**子代理正式交接**：**`architecture.md`**、**`test_plan.md`**（Markdown，不生成 `plan.json` / `test_plan.json`）。**`docs/design/*.md`** 可选实现笔记。**`docs/monitor/<run_slug>/`**：**monitor** Sub-Agent 的 **执行摘要**（warning/error 分条）与 **规格一致性报告**（architecture / design / test_plan 对照），与规划文档**同级**存放。 | `docs/plans/…`、`docs/test_plans/…`、`docs/monitor/…` |
| `generated_code/` | 可选：**MLIR、IR 快照** 等；**不要**放 Sub-agent 规划/测试计划 Markdown | `*.mlir` 导出等 |
| `compile/` | **编译链路**输出 | `*.pyc`、`pycc` 生成的 `*.v` / `*.stats.json`、`cpp` 相关 manifest 等 |
| `verification/` | **仿真/形式化/综合验证**：Testbench RTL（`tb_*.v` / `tb_*.sv`）、Verilator 构建目录（`obj_verilator/` 等）、波形（`*.vcd`/`*.fst`）、golden 向量、报告附件等 | `tb_overflow_wide_vs_zext.v`、`obj_verilator/`、`seq_mult_uu.vcd` |
| `logs/` | **验证与脚本**的纯文本记录 | `$display` 重定向、`*.log`、回归摘要、`PASS/FAIL` 说明 |

原则：**文本 log 一律进 `logs/`**；**大块二进制或构建树进 `verification/`**；**编译器确定性的生成文件进 `compile/`**。  
**Testbench**：与仿真脚本配套的 `tb_*.v` / `tb_*.sv` 放在 **同一 Level 2 项目** 下的 `verification/`（与 `obj_verilator/`、`*.vcd` 同级或同树），脚本与文档路径统一为 `<项目>/verification/tb_…`，避免与 `compile/` 中的 DUT 生成网表混放。

**仓库内与 `output_files_<date>/` 的关系**：版本控制下的 RTL testbench 通常放在 **源码子项目** 的 `verification/`（例如 `tutorial_5_1_arithmetic_verify/verification/`）；按日期归档的 `output_files_<date>/<module>/verification/` 仍以 **仿真产物**（`obj_*`、波形）为主，必要时可将 TB **复制**进该目录做自包含交付，但应与源码目录 **择一为主** 以免双份漂移。

---

## 示例（目录树）

```text
output_files_2026-03-24/
├── arith_shifter__subagent/        # Sub-agent IP：单一 Level 2（文档 + 源码 + build + 仿真）
│   ├── docs/
│   │   ├── plans/arith_shifter_1.0.0/architecture.md
│   │   ├── design/arith_shifter.md            # 可选实现笔记
│   │   ├── test_plans/arith_shifter/test_plan.md
│   │   └── monitor/<run_slug>/                # monitor：execution_digest / spec_consistency_report
│   ├── pycircuit/                  # Mode A
│   ├── rtl/                        # Mode B（可选）
│   ├── build_verilog.sh, run_verilator*.sh
│   ├── generated_code/             # 可选：MLIR
│   ├── compile/
│   ├── verification/               # tb_*.v, obj_*, vcd
│   └── logs/
├── seq_mult_uu/
│   ├── generated_code/     # 可选：emit_mlir 等
│   ├── compile/
│   │   ├── seq_mult_uu.pyc
│   │   └── verilog/
│   │       ├── seq_mult_uu.v
│   │       └── seq_mult_uu.v.stats.json
│   ├── verification/
│   │   ├── tb_seq_mult_uu.v
│   │   ├── obj_verilator/
│   │   └── seq_mult_uu.vcd
│   └── logs/
│       └── verilator_run.log
└── mul_s8_u4_verify16/
    ├── compile/
    │   ├── mul_s8_u4_verify16.pyc
    │   └── pycircuit_verilog/
    │       └── mul_s8_u4_verify16.v
    ├── verification/
    │   ├── tb_mul_s8_u4_verify16.v   # 与仿真同目录或子目录
    │   └── obj_verilator/
    └── logs/
        └── mul_s8_u4_signedness_verification.log
```

---

## 脚本与路径约定

1. **环境变量（推荐）**  
   - `PYC_OUTPUT_ROOT`：Level 1 根路径，例如 `export PYC_OUTPUT_ROOT=$REPO/output_files_2026-03-24`（与 `output_files_0324` 符号链接指向同一目录时可二选一）。  
   - 子脚本拼接：Sub-agent 流程用 **`$PYC_OUTPUT_ROOT/<module>__subagent/{compile,verification,logs}/`**；未走 Sub-agent 时用 **`$PYC_OUTPUT_ROOT/<module>/…`**（**勿**对同一 IP 混用两者）。

2. **相对仓库根**  
   - 文档与 README 中写「相对于 `REPO`」的路径，避免写死机器绝对路径。

3. **`.gitignore`**  
   - 若 `output_files_*` 体积大，可在根 `.gitignore` 增加 `output_files_*/**` 或按团队策略只提交 `logs/` 中的摘要。

---

## 与现有仓库目录的关系

| 现有习惯 | 说明 |
|----------|------|
| 旧路径 `generated_artifacts/`、`tutorial_*/generated/`、`*/generated/` | 已迁入 `output_files_2026-03-24/` 下对应 Level 2；新跑批仍用 `PYC_OUTPUT_ROOT` 指向所选日期目录。 |
| Sub-agent 同一 IP | **仅** **`output_files_.../<module>__subagent/`**：`docs/`、`pycircuit/`、`compile/`、`verification/`、`logs/` 同树；**不要**另建并列 **`module/`**。产出布局与 Sub-Agent 协作说明见 **`docs/sub_agent_docs/`**（本文件、[subagent_collaboration_workflow.md](subagent_collaboration_workflow.md) 等）；其他教程仍可在 **repo-root `docs/`**。 |

---

## 可选扩展

- **同日内多轮实验**：在 Level 2 下再加 `run_<序号或简短标签>/`，再套 Level 3 四类文件夹。  
- **CI**：Level 1 可用 `output_files_ci_${{ github.run_id }}` 避免并行 job 冲突。

---

## 以后任务如何复用

1. 开任务时先定 **日期**：Sub-agent 流程下 **只建** **`output_files_…/<module>__subagent/`**，内放 `docs/`、`pycircuit/`、`rtl/`、`verification/`、脚本及 `compile/`、`logs/`。  
2. 修改或编写 shell/Python：`ROOT` 指向该 **`module__subagent`** 目录，相对路径引用 `pycircuit/`、`compile/` 等。  
3. 在 PR/实验说明里写：**Level 2** `output_files_YYYY-MM-DD/<module>__subagent/`。

本文路径：`docs/sub_agent_docs/output_files_management.md`。

**Cursor Agent**：自动遵循产出布局时，参见项目 Skill **[`.cursor/skills/pycircuit-output-files/SKILL.md`](../../.cursor/skills/pycircuit-output-files/SKILL.md)**；仓库规则 **[`.cursor/rules/pycircuit-output-files-layout.mdc`](../../.cursor/rules/pycircuit-output-files-layout.mdc)** 为 `alwaysApply`，涉及脚本/路径时会要求对齐本规范。
