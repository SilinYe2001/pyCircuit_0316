# Agent 命令参考：pyCircuit 常用 bash 与产物

本文件是《[新手 Agent 操作指南](../agent_guide/prompts.md)》的配套参考，收录 Agent 在驱动 pyCircuit 工作流时实际执行的 bash 命令、环境变量和产物路径。用户日常不需要手敲这些命令，把它们交给 Agent 即可。

## 1. 环境准备

```bash
# 从仓库根目录构建 pycc 工具链（Release）
bash flows/scripts/pyc build

# 构建完成后，工具在：
PYCC=.pycircuit_out/toolchain/install/bin/pycc
$PYCC --help
```

前端通过 `PYTHONPATH` 直接使用：

```bash
export PYTHONPATH=$PWD/compiler/frontend
export PYC_TOOLCHAIN_ROOT=$PWD/.pycircuit_out/toolchain/install
```

## 2. 分步流程：Python → MLIR → Verilog/C++

以 `designs/examples/counter` 为例：

```bash
# 2a. Python → MLIR (.pyc)
python3 -m pycircuit.cli emit designs/examples/counter/counter.py \
    -o .pycircuit_out/demo/counter.pyc

# 2b. MLIR → Verilog（扁平化）
$PYC_TOOLCHAIN_ROOT/bin/pycc .pycircuit_out/demo/counter.pyc \
    --emit=verilog --flatten --logic-depth=64 \
    -o .pycircuit_out/demo/counter_flat.v

# 2c. MLIR → C++ 仿真模型
$PYC_TOOLCHAIN_ROOT/bin/pycc .pycircuit_out/demo/counter.pyc \
    --emit=cpp --out-dir .pycircuit_out/demo/cpp
```

编译成功后 stderr 会打印资源统计，如 `stats: regs=... max_depth=... WNS=...`。

## 3. 一键构建 + 双后端仿真（主流程）

```bash
python3 -m pycircuit.cli build designs/examples/counter/tb_counter.py \
    --out-dir .pycircuit_out/demo/counter_build \
    --target both --jobs 8 --logic-depth 64 \
    --run-verilator
```

关键产物：

```text
.pycircuit_out/demo/counter_build/
├── device/verilog/          # 综合用 RTL
├── device/cpp/              # C++ 仿真模型源码
├── tb/tb_counter.cpp        # 生成的 C++ 测试主程序
├── tb/tb_counter.sv         # 生成的 SystemVerilog 测试台
├── cpp_build/build/pyc_tb   # C++ 仿真器可执行文件
└── verilator_build/Vtb_counter  # Verilator 仿真器可执行文件
```

手动重跑两个仿真器：

```bash
# C++ 仿真（失败返回 1，成功返回 0，无 OK 字样）
.pycircuit_out/demo/counter_build/cpp_build/build/pyc_tb

# Verilator 仿真（失败 $fatal，成功打印 OK 并 $finish）
cd .pycircuit_out/demo/counter_build
./verilator_build/Vtb_counter
```

## 4. 日常功能迭代（只跑 C++）

```bash
python3 -m pycircuit.cli build designs/examples/counter/tb_counter.py \
    --out-dir .pycircuit_out/demo/counter_build \
    --target cpp --jobs 8

.pycircuit_out/demo/counter_build/cpp_build/build/pyc_tb
```

## 5. 生成 VCD 波形

`Vtb_counter` 默认不写波形；VCD 只从 C++ 仿真器产生：

```bash
cd .pycircuit_out/demo/counter_build
mkdir -p waves
PYC_TRACE_DIR=$PWD/waves ./cpp_build/build/pyc_tb
```

生成文件：`waves/tb_counter/tb_counter.vcd`，包含 `clk/rst/enable/count`。

文本核验（无 GUI 时 Agent 用）：

```bash
head -n 40 waves/tb_counter/tb_counter.vcd
grep -n "count" waves/tb_counter/tb_counter.vcd
```

交互查看：

```bash
gtkwave waves/tb_counter/tb_counter.vcd
```

## 6. Verilog 签收（功能锁定后）

```bash
python3 -m pycircuit.cli build designs/examples/counter/tb_counter.py \
    --out-dir .pycircuit_out/demo/counter_build \
    --target verilator --jobs 8 --run-verilator
```

等价于手动：

```bash
verilator --binary -Wall -Wno-fatal --timing --trace \
    --top-module tb_counter \
    --Mdir .pycircuit_out/demo/counter_build/verilator_build \
    .pycircuit_out/demo/counter_build/tb/tb_counter.sv \
    .pycircuit_out/demo/counter_build/device/verilog/pyc_primitives.v \
    .pycircuit_out/demo/counter_build/device/verilog/counter.v

cd .pycircuit_out/demo/counter_build
./verilator_build/Vtb_counter
```

## 7. 回归与全量检查

两个词是验证规模的分层约定，不是框架内建概念：

- **smoke（冒烟）**：秒级最小自检。每个例子的 `*_config.py` 里 `TB_PRESETS["smoke"]` 给很小的 `finish`/`timeout`（counter 为 `{"timeout": 64, "finish": 4}`），所有 `tb_*.py` 默认就用它。
- **nightly（夜间回归）**：`flows/scripts/run_sims_nightly.sh` 自动发现 `designs/examples` 全部例子，每个按 `--target both` 双后端构建运行，带每例超时（默认 1 小时）和超时重试。`TB_PRESETS["nightly"]` 的更长激励档是预留扩展点，默认不被选中。

```bash
# 仓库 smoke 回归（G1/G2 gate）
bash flows/scripts/pyc smoke

# 全例子 × 双后端夜间回归
bash flows/scripts/run_sims_nightly.sh
```

## 8. 常见失败定位

| 现象 | 优先检查 |
|---|---|
| `pyc build` 失败 | `llvm-config-19` 是否可用；`LLVM_DIR`/`MLIR_DIR` 推断 |
| C++ 仿真 expect 失败 |  stderr 中 `ERROR: <port> mismatch: got=... exp=...`，对照 `tb_counter.py` 该周期期望 |
| Verilator 仿真失败 | `$fatal` 输出的周期和端口，先确认 C++ 仿真是否通过 |
| 没有生成 VCD | 是否对 `Vtb_counter` 误设了 `PYC_TRACE_DIR`；应改用 `pyc_tb` |
| 找不到 `pycc` | 是否执行了 `bash flows/scripts/pyc build` |

## 9. 目录约定

- 所有构建/仿真产物放在 `.pycircuit_out/`（git 已忽略）。
- 设计源码：`designs/examples/<name>/`
- 测试台：`designs/examples/<name>/tb_<name>.py`
- 不要手动编辑 `tb/*.cpp`、`tb/*.sv`、`device/` 下的生成文件。
