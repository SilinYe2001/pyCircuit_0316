# pyCircuit: From Source Code to Simulation — Counter Walkthrough

This document walks through the complete pyCircuit flow using an 8-bit counter as the
example. By following these steps you will go from Python source code to a compiled
simulation binary, run it, and inspect the results.

---

## Overview

```
  Python Source (.py)
        │
        │  Step 1 — pycircuit emit
        ▼
  MLIR IR (.pyc)
        │
        │  Step 2 — pycc --emit=cpp / --emit=verilog
        ▼
  C++ Model (.hpp/.cpp)  or  Verilog (.v)
        │
        │  Step 3 — pycircuit build (CMake + Ninja)
        ▼
  Simulation Binary (pyc_tb)
        │
        │  Step 4 — run
        ▼
  Pass/Fail + VCD Waveform
```

---

## Prerequisites

- Python 3.9+
- LLVM/MLIR development libraries (`sudo apt-get install llvm-dev mlir-tools libmlir-dev`)
- CMake, Ninja
- (Optional) GTKWave for viewing VCD waveforms

---

## Step 0: Environment Setup

```bash
cd /path/to/pyCircuit

# Create and activate a virtual environment (one-time)
python3 -m venv .venv
source .venv/bin/activate

# Install the pycircuit Python package in editable mode
pip install -e .

# Build the MLIR-based compiler (pycc). Skip if build/bin/pycc already exists.
bash flows/scripts/pyc build
```

Verify the compiler is available:

```bash
ls build/bin/pycc
```

---

## Step 1: Understand the Source Code

A pyCircuit design consists of three files:

### 1a. Design file — `designs/examples/counter/counter.py`

```python
from __future__ import annotations

from pycircuit import Circuit, compile, module, u


@module
def build(m: Circuit, width: int = 8) -> None:
    clk = m.clock("clk")
    rst = m.reset("rst")
    en = m.input("enable", width=1)

    count = m.out("count_q", clk=clk, rst=rst, width=width, init=u(width, 0))
    count.set(count.out() + 1, when=en)
    m.output("count", count)


build.__pycircuit_name__ = "counter"
```

Key points:
- `@module` marks this as a hardware module entry point.
- `m.clock` / `m.reset` / `m.input` declare I/O ports.
- `m.out(...)` with `clk`, `rst`, and `init` creates a register (D flip-flop).
- `count.set(count.out() + 1, when=en)` — increment when enabled.
- `m.output("count", count)` exposes the register value as an output port.

### 1b. Configuration — `designs/examples/counter/counter_config.py`

```python
DEFAULT_PARAMS = {
    'width': 8
}

TB_PRESETS = {
    "smoke": {"timeout": 64, "finish": 4},
    "nightly": {"timeout": 256, "finish": 16},
}

SIM_TIER = "normal"
```

This provides default JIT parameters and testbench presets (how many cycles to run).

### 1c. Testbench — `designs/examples/counter/tb_counter.py`

```python
from __future__ import annotations

import sys
from pathlib import Path

from pycircuit import Tb, compile, testbench

_THIS_DIR = Path(__file__).resolve().parent
if str(_THIS_DIR) not in sys.path:
    sys.path.insert(0, str(_THIS_DIR))

from counter import build
from counter_config import DEFAULT_PARAMS, TB_PRESETS


@testbench
def tb(t: Tb) -> None:
    p = TB_PRESETS["smoke"]
    t.clock("clk")
    t.reset("rst", cycles_asserted=2, cycles_deasserted=1)
    t.timeout(int(p["timeout"]))
    t.drive("enable", 1, at=0)
    for cyc in range(5):
        t.expect("count", cyc + 1, at=cyc)
    t.finish(at=int(p["finish"]))
```

Key points:
- `@testbench` marks this as a testbench entry point.
- `t.clock("clk")` — declares which port is the clock.
- `t.reset("rst", ...)` — asserts reset for 2 cycles, then deasserts for 1 cycle before stimulus begins.
- `t.drive("enable", 1, at=0)` — drives the `enable` signal high at cycle 0.
- `t.expect("count", cyc + 1, at=cyc)` — after each cycle, checks the counter value (expects 1, 2, 3, 4, 5 at cycles 0–4).
- `t.finish(at=4)` — ends the simulation after cycle 4.
- `t.timeout(64)` — fail-safe: abort if the simulation runs more than 64 cycles.

---

## Step 2: Manual Step-by-Step Flow (Educational)

These steps show what happens under the hood. For day-to-day use, skip to
Step 3 which does all of this in one command.

### 2a. Emit MLIR IR

```bash
source .venv/bin/activate
pycircuit emit designs/examples/counter/counter.py -o counter.pyc
```

This compiles the Python design into MLIR IR. The output `counter.pyc` contains:

```
module attributes {pyc.top = @counter, pyc.frontend.contract = "pycircuit"} {
func.func @counter(%clk: !pyc.clock, %rst: !pyc.reset, %enable: i1) -> i8 ... {
  %v1 = pyc.alias %enable {pyc.name = "en__counter__L10"} : i1
  %v2 = pyc.wire {pyc.name = "count_q__next"} : i8
  %v3 = pyc.constant 1 : i1
  %v4 = pyc.constant 0 : i8
  %v5 = pyc.reg %clk, %rst, %v3, %v2, %v4 : i8
  %v6 = pyc.alias %v5 {pyc.name = "count_q"} : i8
  %v7 = pyc.alias %v6 {pyc.name = "count__counter__L12"} : i8
  %v8 = pyc.constant 1 : i8
  %v9 = pyc.add %v7, %v8 : i8
  %v10 = pyc.mux %v1, %v9, %v7 : i8
  pyc.assign %v2, %v10 : i8
  func.return %v7 : i8
}
}
```

### 2b. Compile MLIR to C++

```bash
./build/bin/pycc counter.pyc --emit=cpp --out-dir counter_build/
```

Generates `counter_build/counter.hpp` and `counter_build/counter.cpp` containing
a `pyc::gen::counter` C++ struct with `eval()` (combinational), `tick()` (sequential),
and clock/reset bindings.

### 2c. Compile MLIR to Verilog

```bash
./build/bin/pycc counter.pyc --emit=verilog -o counter.v
```

Generates synthesizable Verilog with a `counter` module, combinational assigns,
and a `pyc_reg` instance for the flip-flop.

---

## Step 3: One-Command Build + Simulate (Recommended)

The `pycircuit build` command handles the entire pipeline: emit per-module MLIR,
run `pycc` on each module, generate a testbench C++ harness, produce a CMake
project, and compile everything into a single executable.

```bash
source .venv/bin/activate

pycircuit build designs/examples/counter/tb_counter.py \
    --out-dir counter_sim_out \
    --target cpp \
    --profile release
```

What this does:
1. JIT-compiles `counter.py` into a `Design` object.
2. Emits per-module `.pyc` files into `counter_sim_out/device/modules/`.
3. Generates testbench C++ source (`counter_sim_out/tb/tb_counter.cpp`).
4. Runs `pycc` to convert each `.pyc` into C++ headers/sources.
5. Generates a `CMakeLists.txt` and builds with Ninja, producing the `pyc_tb` binary.

Expected output:

```
/path/to/counter_sim_out/cpp_build/src/CMakeLists.txt
-- The CXX compiler identification is GNU 13.3.0
...
[1/3] Building CXX object .../counter.cpp.o
[2/3] Building CXX object .../tb_counter.cpp.o
[3/3] Linking CXX executable pyc_tb
/path/to/counter_sim_out/project_manifest.json
```

### Build options

| Flag | Description |
|------|-------------|
| `--target cpp` | Build C++ simulation only |
| `--target verilator` | Build Verilator simulation only |
| `--target both` | Build both (default) |
| `--profile release` | Optimized build (`-O2 -DNDEBUG`) |
| `--profile dev` | Debug build (`-O0 -g`) |
| `--jobs N` | Parallel compilation jobs |
| `--run-verilator` | Also execute the Verilator binary after build |

### Verilator build + run

To run the same counter testbench through Verilator in one command:

```bash
source .venv/bin/activate

pycircuit build designs/examples/counter/tb_counter.py \
    --out-dir counter_sim_verilator_run \
    --target verilator \
    --profile release \
    --run-verilator
```

Expected result:

```text
...
OK
- /path/to/counter_sim_verilator_run/tb/tb_counter.sv:...: Verilog $finish
/path/to/counter_sim_verilator_run/project_manifest.json
```

This produces a Verilator-built binary under `counter_sim_verilator_run/verilator_build/`
and runs it immediately after the build completes.

---

## Step 4: Run the Simulation

```bash
./counter_sim_out/cpp_build/build/pyc_tb
```

### Pass result

```
OK
```

The simulation prints `OK` to stderr and exits with code 0. This means all
`t.expect(...)` assertions in the testbench passed.

### Run the generated Verilator binary manually

If you built with `--target verilator` without `--run-verilator`, or you want to
re-run the generated simulator directly:

```bash
./counter_sim_verilator_run/verilator_build/Vtb_counter
```

### Fail result

If an assertion fails, the output looks like:

```
ERROR: count mismatch: got=0x3 exp=0x5
```

The program exits with code 1.

### Timeout

If the simulation exceeds `t.timeout(...)` cycles without reaching `t.finish(...)`:

```
TIMEOUT
```

The program exits with code 1.

---

## Step 5: Inspect Simulation Results

### 5a. VCD Waveform

The C++ simulation automatically writes a VCD trace file:

```
tb_counter/tb_counter.vcd
```

(Relative to the working directory where you ran `pyc_tb`. Set `PYC_TRACE_DIR`
to redirect.)

View it with GTKWave:

```bash
gtkwave tb_counter/tb_counter.vcd
```

The VCD contains all DUT ports: `clk`, `rst`, `enable`, `count[7:0]`.
You will see:

| Time (ns) | clk | rst | enable | count |
|-----------|-----|-----|--------|-------|
| 0         | 1   | 1   | 0      | 0x00  |
| 1–4       | tog | 1   | 0      | 0x00  |
| 5         | tog | 0   | 0      | 0x00  |
| 6+        | tog | 0   | 1      | 0x01, 0x02, ... |

### 5b. Verilator VCD waveform

The Verilator flow writes its trace to a separate file so it does not collide
with the C++ backend output:

```text
counter_sim_verilator_run/verilator_tb_counter.vcd
```

Open it with GTKWave:

```bash
gtkwave counter_sim_verilator_run/verilator_tb_counter.vcd
```

### 5c. Redirect VCD output

```bash
PYC_TRACE_DIR=/tmp/my_traces ./counter_sim_out/cpp_build/build/pyc_tb
# VCD written to /tmp/my_traces/tb_counter/tb_counter.vcd
```

### 5d. Compiler statistics

```bash
cat counter_sim_out/device/cpp/counter/compile_stats.json
```

Shows register count, memory count, maximum combinational logic depth, and
timing slack.

### 5e. Project manifest

```bash
cat counter_sim_out/project_manifest.json
```

Contains paths to all build artifacts: the executable, module sources,
testbench sources, and the C++ project manifest.

---

## Step 6: Simulation Runtime Statistics (Optional)

Enable runtime simulation statistics by setting environment variables:

```bash
PYC_SIM_STATS=1 PYC_SIM_STATS_PATH=sim_stats.txt \
    ./counter_sim_out/cpp_build/build/pyc_tb

cat sim_stats.txt
```

Output:

```
instance_eval_calls=...
instance_cache_skips=...
primitive_eval_calls=...
primitive_cache_skips=...
fallback_iterations=...
```

---

## Quick Reference

```bash
# Full flow — setup once
source .venv/bin/activate
pip install -e .
bash flows/scripts/pyc build          # only if build/bin/pycc doesn't exist

# Build + simulate — repeat as needed
pycircuit build designs/examples/counter/tb_counter.py \
    --out-dir counter_sim_out --target cpp --profile release

./counter_sim_out/cpp_build/build/pyc_tb

# Verilator build + run
pycircuit build designs/examples/counter/tb_counter.py \
    --out-dir counter_sim_verilator_run \
    --target verilator --profile release --run-verilator

# View waveform
gtkwave tb_counter/tb_counter.vcd
gtkwave counter_sim_verilator_run/verilator_tb_counter.vcd

# Run all examples (CI-style)
bash flows/scripts/run_sims.sh
```

---

## Output Directory Structure

```
counter_sim_out/
├── project_manifest.json           # Master manifest with all artifact paths
├── cpp_project_manifest.json       # C++ build manifest (sources, includes)
├── .build_cache.json               # Incremental build cache
├── device/
│   ├── modules/
│   │   └── counter.pyc             # Per-module MLIR
│   └── cpp/
│       └── counter/
│           ├── counter.hpp         # Generated C++ header
│           ├── counter.cpp         # Generated C++ implementation
│           ├── compile_stats.json  # Compiler statistics
│           └── manifest.json       # Module manifest
├── tb/
│   ├── tb_counter.pyc              # Testbench MLIR
│   └── tb_counter.cpp              # Generated testbench C++ source
└── cpp_build/
    ├── src/
    │   └── CMakeLists.txt          # Auto-generated CMake project
    └── build/
        └── pyc_tb                  # Simulation executable
```
