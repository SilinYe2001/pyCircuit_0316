# LFSM (4EU UU mode) PyCircuit V6 设计

以 `designs/LFSM/design_spec/docs/four_eu/02_LFSM.md` 为设计输入、
`designs/LFSM/design_spec/code/`（4EU non-RU）为 golden 参考，按
`docs/pycircuit_implementation_method.md` 十步流程完成 LFSM 4EU UU
mode（Shared MEM baseline + C-only 路径）的 PyCircuit V6 实现。
范围/边界见 `docs/REQUIREMENT_SOURCES.md` §0/§5。

## Step 1 笔记（authoring mode 与风格参考）

- **Authoring mode**：全部单元采用 V6 cycle-aware
  （`CycleAwareCircuit` / `CycleAwareDomain` / `CycleAwareSignal`），
  编译入口 `compile_cycle_aware(..., eager=True)`；层次化发射检查用
  `compile_cycle_aware(..., eager=True, hierarchical=True)`。
  不使用 V4 风格 `@module` / `Circuit` JIT 路径。
- **信号纪律**：遵守 V6 spec §2（标量 CAS、向量 `Wire[Vector]` +
  `cas()`、无 `domain.state()`、不读 `.wire`、`wire_of()` 仅用于标量
  输出、输出 dict 存 CAS）。四 lane 的同类信号用 `shape=[4]` 向量，
  不手工拆标量。
- **风格参考**：
  - 层次化多模块（`domain.call()` 六步法、prefix 级联）：
    DavinciOO `davinci/`（外部仓库，canonical 参考）；
  - 向量 lane：`designs/BypassUnit/`、`designs/IssueQueue/`；
  - FIFO/存储原语：`designs/examples/fifo_loopback/`（注意其为 V4
    风格入口；本设计 FIFO 以 `domain.signal()` 数组实现，见
    `docs/ASSUMPTIONS.md` A-007——仓库内暂无 `m.fifo` 的 V6 用户，
    属潜在原语缺口，若改用须 gate-first）。
- **Python 模型映射**：`evaluate()/commit()` → cycle-0 组合求值 +
  `<<=`/`.assign(when=)` 拍末提交；同拍 bypass = cycle-0 纯组合链
  （A-008）。
- **仓库纪律**：本设计不改 IR/编译器；发现 V6 原语缺口先停下走
  gate-first（`AGENTS.md`、`docs/updatePLAN.md`）。

## 环境

```bash
python3 -m pip install -e .                 # 仓库根；安装 pycircuit 前端
export PYTHONPATH=<repo>/compiler/frontend:$PYTHONPATH
export PYC_TOOLCHAIN_ROOT=<repo>/.pycircuit_out/toolchain/install
```

Golden 模型驱动（在 `designs/LFSM/design_spec/` 下）：

```bash
python3 code/run_model.py --eu-mode 4 --M 128 --N 128 --K 128 \
  --m-mode 32 --data-type B4 --mem-load-latency 3 --no-echo   # TC17
python3 code/run_typical_cases.py --no-echo                   # 全矩阵
```

## Sign-off 命令（Step 10 收口标准）

```bash
# 全量单测/集成回归（CycleAwareTb，golden 向量回放 + 反应式 stub）
python3 -m pytest designs/LFSM/pycircuit/tests -x -q
# C++ 构建（每日回归）
pycircuit build designs/LFSM/pycircuit/tests/integration/<tb>.py --target cpp
# Verilator sign-off（同 expect 结果）
pycircuit build designs/LFSM/pycircuit/tests/integration/<tb>.py \
  --target verilator --run-verilator
```

## 文档索引（`docs/`）

| 文档 | 步骤 | 状态 |
| :--- | :--- | :--- |
| `REQUIREMENT_SOURCES.md` | Step 2 | ✅ 已建立 v2（含 §4.1 spec 歧义注记） |
| `ASSUMPTIONS.md` | Step 2–3 | ✅ 已建立 v2（含首访去重、在途积压口径与深度决策、waiver） |
| `PORT_LIST.md` | Step 3 | ✅ 已建立（含 `load_range_query` 相位契约、payload 展平、存储分类） |
| `FEATURE_LIST.md` | Step 3 | ✅ 已建立（F-001…F-120、02_LFSM.md 全标题核对表、R-xx 交叉索引） |
| `ALGORITHM_SEQUENTIAL.md` | Step 4 | ✅ 已建立（子程序式伪码 + 表示差异等价性论证 + D-001…D-005 决策记录） |
| `ALGORITHM_PIPELINED.md` | Step 5 | ✅ 已建立（cycle 映射/三边 bypass/寄存器推断/存储定稿：块池=0 emit-on-demand） |
| `ALGORITHM_CYCLE_AWARE_PSEUDOCODE.md` | Step 6 | ✅ 已建立（逐模块 inputs/outs 键、内部 next 数、逐行 V6 伪码） |
| `TRACEABILITY.md` | Step 7 | ✅ 已建立（端口/功能双矩阵 + GAP-01…07；2026-10-14 锚点核对完成并同步改名/payload 归属/边3 严格流水与发送段偏差） |
| `TEST_PLAN.md` | Step 8 | ✅ 已建立（T-001…T-103 全分类；回放向量依赖 golden todo；fire/issue 对拍口径=逐笔等价+链首相移 +2，GAP-06/07） |
| `IMPLEMENTATION_LOG.md` | Step 9 | ⬜ |
| `SYSTEM_TEST.md` | Step 10 | ⬜ |
