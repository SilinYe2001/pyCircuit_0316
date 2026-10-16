# V6 周期感知（Cycle-Aware）设计在 LFSM 代码中的体现

> 汇报材料 · LFSM（4EU UU mode）PyCircuit V6 设计
> 事项：逐条指出 V6 周期感知（Cycle-Aware）设计模型在 LFSM 实现代码中的
> 具体体现位置——统一周期范式、寄存器推导、三条边的同拍/跨拍语义、
> 条件保持、测试侧对称模型
> 权威来源：[docs/v6_PyCircuit_Specification.md](../../../../docs/v6_PyCircuit_Specification.md)（§2/§4/§6）、
> [designs/LFSM/pycircuit/docs/ALGORITHM_CYCLE_AWARE_PSEUDOCODE.md](../docs/ALGORITHM_CYCLE_AWARE_PSEUDOCODE.md)（Step 6 定稿）
> 实例代码：`designs/LFSM/pycircuit/lfsm/`、`designs/LFSM/pycircuit/tests/`
> 整理日期：2026-10-16

---

## 1. 一句话概述

LFSM 全部 13 个带状态叶模块遵循同一条周期范式——**cycle 0 纯组合求值 →
恰好一次 `domain.next()` → cycle 1 统一 `<<=` 提交**；三条数据通路边的
"允许/禁止同拍 bypass"契约、GAP-06/07 的两道寄存割断、跨模块同拍查询环，
全部用 cycle 语义在代码中显式表达——**时序结构就是代码结构**。

---

## 2. 背景：cycle-aware 的四个核心概念

| 概念 | 含义 | 规范出处 |
| :--- | :--- | :--- |
| CAS 周期标签 | 每个信号携带"逻辑周期"，组合不同周期信号时输出取 max(cycle) | [Spec](../../../../docs/v6_PyCircuit_Specification.md) §1/§6 |
| `domain.next()` | 推进逻辑周期，标记时序分界点 | [Spec](../../../../docs/v6_PyCircuit_Specification.md) §6 |
| 寄存器推导 | `domain.signal()` 声明（cycle 0 读）+ `<<=` 在 cycle 1 写 → 读 0 写 1 ⟹ 一级 DFF；写周期 < 读周期 = 编译错误 | [Spec](../../../../docs/v6_PyCircuit_Specification.md) §4 |
| 同拍 = 纯组合 | 同一周期内的信号链是零延迟组合穿透（同拍 bypass）；跨周期必须经过寄存提交 | [Spec](../../../../docs/v6_PyCircuit_Specification.md) §6 自动周期平衡 |

---

## 3. LFSM 的统一周期范式

对 `lfsm/` 全目录 grep `domain.next()` 的证据：**每个带状态叶模块恰好 1 次**
（十步流程 Step 6 的硬性决策，[`types.py`](../lfsm/types.py#L1) docstring 固化的 authoring 纪律）：

| 模块 | `domain.next()` 行 | 模块 | `domain.next()` 行 |
| :--- | :--- | :--- | :--- |
| [walker](../lfsm/walker.py#L143) | 143 | [assembler_b](../lfsm/assembler_b.py#L190) | 190 |
| [rdgen](../lfsm/rdgen.py#L134) | 134 | [assembler_amx](../lfsm/assembler_amx.py#L256) | 256 |
| [rd_queue](../lfsm/rd_queue.py#L103) | 103 | [assembler_bmx](../lfsm/assembler_bmx.py#L238) | 238 |
| [cand_holder](../lfsm/cand_holder.py#L103) | 103 | [tag_checker](../lfsm/tag_checker.py#L110) | 110 |
| [arbiter](../lfsm/arbiter.py#L68) | 68 | [req_sched](../lfsm/req_sched.py#L117) | 117 |
| [c_path](../lfsm/c_path.py#L86) | 86 | [config_regs](../lfsm/config_regs.py#L219) | 219 |
| [assembler_a](../lfsm/assembler_a.py#L129) | 129 | | |

每个模块内部都是同一个四段式骨架（以 walker 为样板）：

> [lfsm/walker.py](../lfsm/walker.py)

```python
# ── Cycle 0: state ──            # 54-60: domain.signal 声明，Q 端 cycle 0 可读
# ── Cycle 0: inputs ──           # 63-70: sin() 双模输入
# ── Cycle 0: combinational ──    # 73-86: 纯组合（转移优先级、token 输出）
# ── Cycle 0: next-state ──       # 114-141: 次态表达式
    domain.next()                 # 143: 唯一时序分界
# ── Cycle 1: commits ──          # 146-152: 统一 <<= 提交
```

**读法收益：`domain.next()` 的次数 = 寄存器级数；`<<=` 出现在哪个 cycle =
寄存器插在哪。** 全设计的时序可以不动仿真器直接从源码数出来。

---

## 4. 体现点 1：寄存器推导（读 0 写 1 ⟹ 一级 DFF）

`domain.signal()` 在 cycle 0 声明、Q 端立即可读；次态表达式在 cycle 0 算好；
`domain.next()` 之后 `<<=` 把写动作落在 cycle 1——读写周期差 1，编译器推导
出一级反馈寄存器：

> [lfsm/walker.py:54-56](../lfsm/walker.py#L54)（cycle 0 声明）、[143-148](../lfsm/walker.py#L143)（cycle 1 提交）

```python
active = domain.signal(width=1, reset_value=0, name=f"{prefix}_active")
seq = domain.signal(width=SEQ_W, reset_value=0, name=f"{prefix}_seq")
...
domain.next()
active <<= active_nxt
seq <<= seq_nxt
```

**代码中没有一行"寄存器"字样——寄存器是周期差推导出来的。** 这就是
cycle-aware 的核心思想：设计者表达"什么时候读、什么时候写"，存储元件
由编译器推断。

---

## 5. 体现点 2：三条边的 bypass 契约 = 周期语义

LFSM 数据通路三条边的规格契约，在代码里全部翻译成"同拍组合 or 跨拍寄存"
的周期表达：

| 边 | 契约 | 代码体现 |
| :--- | :--- | :--- |
| 边1 queue→assembler | **禁止**同拍 bypass：rdgen 拍末 commit 入队，次拍可见；head 是寄存读出 | [`rd_queue.py:70-79`](../lfsm/rd_queue.py#L70) head 视图从 `domain.signal` 存储体经 `vec_rd` 组合读出；入队写经 cycle 1 `<<=`（[`rd_queue.py:107-111`](../lfsm/rd_queue.py#L107)） |
| 边2 assembler→cand_holder | 允许同拍 bypass（本拍形成的视图本拍可被捕获判定消费） | assembler 的 `view_*` 输出是 cycle-0 组合；cand_holder 捕获判定同拍使用（[`cand_holder.py:77-81`](../lfsm/cand_holder.py#L77)） |
| 边3 cand_holder→arbiter | **GAP-06 改严格流水**：仲裁只认 held 快照 Q 端，fresh 不旁路 | [`cand_holder.py:60-68`](../lfsm/cand_holder.py#L60)（见体现点 3） |

边1 的"次拍可见"不需要任何显式延迟语句——它就是"cycle 1 才 `<<=`"的
自然结果；边2 的"同拍穿透"也不需要任何特殊语法——cycle 0 内不跨
`domain.next()` 的信号链天然是纯组合。

---

## 6. 体现点 3：cand_holder —— GAP-06 割断①的周期表达

`cand_holder` 是边3 严格流水的落地模块。docstring 直接写明周期语义：

> [lfsm/cand_holder.py:1-7](../lfsm/cand_holder.py#L1)（docstring）

```python
"""LFSM cand_holder — held candidate lifetime + seq/planned latch (CYCLE §9).

Edge-3 strict pipeline (D-006): arbitration sees only the held snapshot —
a fresh candidate is captured at cycle end and participates from the next
cycle (chain head +1); fire-replacement is captured same-cycle and may fire
again next cycle (1 fire/cycle steady state). ..."""
```

present 视图**只输出 held 寄存器的 Q 端**（fresh 零旁路）：

> [lfsm/cand_holder.py:59-67](../lfsm/cand_holder.py#L59)

```python
# ── Cycle 0: present = held snapshot (no fresh bypass) ─────────
outs = dict(
    cand_valid=h_v,
    cand_inst=h_ins,
    cand_rd_mem_id=h_rid,
    ...
)
```

捕获逻辑（fresh/replacement/clr）在 cycle 0 算好、cycle 1 提交
（[`cand_holder.py:77-112`](../lfsm/cand_holder.py#L77)）。"fresh candidate 形成拍仅供捕获、次拍起参与
仲裁"这一 GAP-06 不变量，在代码里 = **outs 字典里没有任何一个键来自
当拍组合视图**——审查方式就是读 outs 的每个值是否全部 `h_*` 寄存器。

---

## 7. 体现点 4：req_sched —— GAP-07 割断②（grant 拍 / issue 拍分离）

2-slot 发送队列把"grant 拍"与"issue 拍"显式拆成相邻两拍。docstring 写明
两拍职责，组合逻辑里 `pop`（issue 条件）与 `room`/`push`（grant 反压闭环）
都是 cycle-0 当拍电平：

> [lfsm/req_sched.py:66-70](../lfsm/req_sched.py#L66)

```python
# ── Cycle 0: combinational ─────────────────────────────────────
front_valid = cnt > u(2, 0)
pop = front_valid & mem_ready            # issue 拍：front && mem_ready 当拍出队
room = (cnt < u(2, 2)) | ((cnt > u(2, 0)) & mem_ready)
push = push_valid & room                 # grant 拍：cnt=2 冻结 push（反压闭环）
```

深度 2 的选取也是周期论证：ready=1 时 pop 与 push 同拍发生、`cnt` 经
`mux` 显式保持（[`req_sched.py:106-108`](../lfsm/req_sched.py#L106)），稳态 1 issue/拍——这正是
[pipeline 报告](pipeline划分修改工作记录与下一步方向评估.md) §2.4 连发流水视图（T 形成 / T+1 grant / T+2 issue）的
代码落点。

---

## 8. 体现点 5：tag_checker —— 跨模块同拍组合查询环（A-004 相位契约）

R1 决策环是全设计最特殊的周期结构：`o_load_range_query` **出模块**、外部
Buf/RAM **同拍**组合算 idle、`dest_ok` 同拍回来参与仲裁——一个跨越模块
边界的 cycle-0 组合环：

> [lfsm/tag_checker.py:53-61](../lfsm/tag_checker.py#L53)

```python
# ── Cycle 0: per-lane query / dest ─────────────────────────────
for l in range(4):
    pa_nz = cand_pa[l] > u(TAG_ADV_W, 0)
    v = cand_valid[l] & pa_nz
    q_v.append(v)
    q_base.append(mux(v, cand_pb[l], load_ptr[l]))
    q_adv.append(mux(v, cand_pa[l], u(TAG_ADV_W, 0)))
    dest_ok.append(mux(v, idle_in[l], u(1, 1)))   # valid=0 ⟹ 答案必须为 1（A-004）
```

顶层用 `fw_*` named_wire 把这个同拍环闭合（[`lfsm_top.py:110-123`](../lfsm/lfsm_top.py#L110) 声明 +
`m.assign` 回连）——**组合环的位置在代码里是显式枚举的**，不是藏在网表里。
这也是 [pipeline 报告](pipeline划分修改工作记录与下一步方向评估.md)把 R1 列为"头号风险、不可内部切分"的原因：环的任何
一段打拍都等于改规格相位契约（gate-first 流程）。

---

## 9. 体现点 6：`.assign(when=)` —— 条件保持即"反压无状态机"

寄存器使能是周期语义的另一表达：值只在 `when` 条件成立的拍末更新，其余
拍保持。LFSM 用它实现全部反压/握手保持，**没有任何独立反压 FSM**：

> [lfsm/config_regs.py:233-238](../lfsm/config_regs.py#L233)、[lfsm/assembler_a.py:137-138](../lfsm/assembler_a.py#L137)

```python
# config_regs：配置寄存器 start 拍末加载，其余拍保持
cfg_inst.assign(wh_inst, when=start)
cfg_m_mode.assign(wh_mmode, when=start)
cfg_mslice.assign(wh_mslice, when=start)

# assembler_a：END 标记 end_pop 拍末置位
end_v.assign(u(1, 1), when=end_pop)
end_ins.assign(head_inst, when=end_pop)
```

审查反压正确性 = 逐寄存器检查 `when` 表达式清单（[pipeline 报告](pipeline划分修改工作记录与下一步方向评估.md) §4.3 的
结论："任一情形当拍无 fire_consume → 全部状态经 `assign(when=)` 条件
保持"）。

---

## 10. 体现点 7：驯化自动周期平衡 —— `_v5_bal` 零插入纪律

V6 的自动周期平衡会在组合不同周期信号时自动插 DFF。LFSM 刻意让它成为
**no-op**：[`types.py`](../lfsm/types.py#L1) docstring 规定所有表达式在 cycle 0（`domain.next()`
之前）算完，之后只允许 `<<=`/`.assign()`——于是没有任何平衡寄存器被插入，
并由结构测试守护：

> [lfsm/types.py:1-8](../lfsm/types.py#L1)（docstring）、[tests/unit/test_walker.py:130-133](../tests/unit/test_walker.py#L130)

```python
"""... every expression is computed at cycle 0 *before* ``domain.next()``;
after ``domain.next()`` only ``<<=`` / ``.assign()`` statements referencing
precomputed expressions are allowed, so no ``_v5_bal`` balancing register
is ever inserted."""

def test_walker_mlir_clean():
    """Structural: compiles, no balancing registers inserted."""
    mlir = compile_cycle_aware(build, name="tb_walker_top", eager=True).emit_mlir()
    assert "func.func" in mlir
    assert "_v5_bal" not in mlir
```

**意义：pipeline 划分（三拍分段）是设计决策，不允许编译器"帮忙"改。**
自动平衡仍在，但被 authoring 纪律驯化为零效应，并有测试固化。

---

## 11. 体现点 8：显式周期标注与 cycle provenance

- 输入包装显式标周期：`cas(domain, m.input(...), cycle=0)`（[`types.py:97`](../lfsm/types.py#L97)
  `vin()`、[`types.py:81`](../lfsm/types.py#L81) `kcas()`）；
- 顶层 forward wire 进子模块前显式重新标注：`cas(domain, ~fw_active,
  cycle=0)`（[`lfsm_top.py:127`](../lfsm/lfsm_top.py#L127)）——因为 named_wire 本身无周期信息；
- 子模块输出 dict 存 CAS 本体（[`types.py:100-103`](../lfsm/types.py#L100) `emit_outs` 只在独立
  模式才 `wire_of`）——**cycle provenance 随 dict 穿过 `domain.call()`
  边界**，父模块据此做周期对齐；
- `domain.call()` 自动 push/pop 隔离父周期计数器，但不改变返回信号的
  cycle 值（[Spec](../../../../docs/v6_PyCircuit_Specification.md) §6）——LFSM 的 [`lfsm_top.py`](../lfsm/lfsm_top.py) 整条调用链依赖这一性质
  保持各叶模块的 cycle-0/cycle-1 语义不被组合位置影响。

---

## 12. 体现点 9：测试侧的对称周期模型（CycleAwareTb + phase）

测试台用与设计**对称**的周期模型编写：`tb.next()` 推进、`drive/expect`
落在当前周期，无需手工数绝对拍号：

> [tests/unit/test_walker.py:86-107](../tests/unit/test_walker.py#L86)

```python
@testbench
def tb(t: Tb) -> None:
    tb = CycleAwareTb(t)
    tb.clock("clk")
    tb.reset("rst", cycles_asserted=2, cycles_deasserted=1)
    ...
    tb.drive("lfsm_wlk_start", 1)
    tb.next()                        # → 次拍：第一个 token 出现
    tb.drive("lfsm_wlk_start", 0)
    for tok in toks:
        _expect_token(tb, tok, n_hw, tb.cycle)
        tb.next()
```

观测相位精确到"沿前/沿后"：walker 单测全部用 `phase="pre"`（TICK-OBS，
时钟沿计算后、提交前观测）逐拍比对 token 流——**这与"cycle 0 组合 /
cycle 1 提交"的设计相位一一对应**，对拍口径和代码周期结构互为镜像：

> [tests/unit/test_walker.py:68-73](../tests/unit/test_walker.py#L68)

```python
tb.expect("lfsm_wlk_tok_valid", 1, phase="pre", msg=f"valid c{cyc}")
tb.expect("lfsm_wlk_tok_advance", 1, phase="pre", msg=f"adv c{cyc}")
```

集成 TB（[`test_bypass_chain.py`](../tests/integration/test_bypass_chain.py) / [`test_replay_typical.py`](../tests/integration/test_replay_typical.py) /
[`test_backpressure.py`](../tests/integration/test_backpressure.py)）同款模型；GAP-06/07 的 +2 拍链首相移也在 TB 的
期望值里显式表达（[TEST_PLAN](../docs/TEST_PLAN.md) §0.4 "逐笔等价 + 链首相移 +2 拍"）。

---

## 13. 周期语义总表（一屏速查）

| 结构 | 周期表达 | 代码位置 |
| :--- | :--- | :--- |
| 寄存器 | 读 cycle 0 / 写 cycle 1 → 一级 DFF | 全部叶模块四段式（[walker](../lfsm/walker.py) 为样板） |
| 边1 无 bypass | 入队 cycle 1 `<<=`，次拍可见 | [`rd_queue.py:103-111`](../lfsm/rd_queue.py#L103) |
| 边2 同拍 bypass | 同一 cycle-0 内的组合链 | assembler `view_*` → [`cand_holder.py:77-81`](../lfsm/cand_holder.py#L77) |
| 边3 严格流水（GAP-06） | outs 只含 held Q 端，零 fresh 旁路 | [`cand_holder.py:60-68`](../lfsm/cand_holder.py#L60) |
| grant/issue 分离（GAP-07） | push（grant 拍）/ pop（issue 拍）同拍电平 | [`req_sched.py:66-70`](../lfsm/req_sched.py#L66) |
| R1 同拍查询环（A-004） | query 出模块、idle 同拍回答、dest_ok 当拍 | [`tag_checker.py:53-61`](../lfsm/tag_checker.py#L53) + [`lfsm_top.py:110-123`](../lfsm/lfsm_top.py#L110) |
| 反压保持 | `assign(when=)` 条件使能 | [`config_regs.py:233-244`](../lfsm/config_regs.py#L233)、各 assembler `end_v` |
| 自动平衡 | 纪律性零插入 + 结构断言 | [`types.py`](../lfsm/types.py#L1) docstring、[`test_walker.py:130-133`](../tests/unit/test_walker.py#L130) |
| 链首相移 +2 | TB 期望值显式相移 | [TEST_PLAN](../docs/TEST_PLAN.md) §0.4、集成 TB |

---

## 14. 相关文档索引

| 材料 | 位置 |
| :--- | :--- |
| 周期感知语言定义 | [docs/v6_PyCircuit_Specification.md](../../../../docs/v6_PyCircuit_Specification.md) §2/§4/§6 |
| 逐拍伪码（Step 6 定稿） | [designs/LFSM/pycircuit/docs/ALGORITHM_CYCLE_AWARE_PSEUDOCODE.md](../docs/ALGORITHM_CYCLE_AWARE_PSEUDOCODE.md) |
| 流水线映射（Step 5） | [designs/LFSM/pycircuit/docs/ALGORITHM_PIPELINED.md](../docs/ALGORITHM_PIPELINED.md) |
| 三拍分段决策与估算 | 同目录[《pipeline划分修改工作记录与下一步方向评估.md》](pipeline划分修改工作记录与下一步方向评估.md) |
| 可读性三维度收益 | 同目录[《V6代码可读性_代码理解_调试成本_LFSM实例.md》](V6代码可读性_代码理解_调试成本_LFSM实例.md) |
| Pipeline 对齐单例图解（cand_holder） | 同目录[《CycleAware_Pipeline对齐图解_cand_holder实例.md》](CycleAware_Pipeline对齐图解_cand_holder实例.md) |
| 实例代码 | `designs/LFSM/pycircuit/lfsm/`、`designs/LFSM/pycircuit/tests/` |
