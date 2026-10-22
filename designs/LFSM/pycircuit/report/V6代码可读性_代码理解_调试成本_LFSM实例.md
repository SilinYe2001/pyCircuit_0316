# V6 代码可读性的工程收益 —— 代码把握 · 代码理解 · 调试成本（LFSM 实例）

> 汇报材料 · LFSM（4EU UU mode）PyCircuit V6 设计
> 事项：以 LFSM 开发中的真实代码与真实事件为例，说明 PyCircuit V6 的代码
> 可读性给设计者带来的三类收益——**对代码的把握**、**代码理解**、
> **调试成本下降**
> 权威来源：[docs/v6_PyCircuit_Specification.md](../../../../docs/v6_PyCircuit_Specification.md)、[docs/v6_PyCircuit_Tutorial.md](../../../../docs/v6_PyCircuit_Tutorial.md)；
> 实例代码 `designs/LFSM/pycircuit/lfsm/`、`designs/LFSM/pycircuit/tests/`
> 整理日期：2026-10-16

---

## 1. 一句话概述

V6 把"硬件长什么样"从需要脑内反编译网表，变成**直接读 Python 源码布局**；
LFSM 的十步流程又把这个可读性优势用文档纪律（ASSUMPTIONS / TRACEABILITY /
GAP 登记）固化成可审计的工程资产——**理解成本低的地方，调试成本自然跟着低**。

---

## 2. 背景：V6 可读性的四个机制来源

| 机制 | 内容 | LFSM 落点 |
| :--- | :--- | :--- |
| 统一骨架 | cycle 0 声明/组合 → `domain.next()` → cycle 1 `<<=` 提交 | 每个带状态叶模块恰好 1 次内部 `domain.next()` |
| 硬件语义显式化 | 硬件选择必须写 `mux`/`select`（信号禁止作 Python bool） | [`walker.py`](../lfsm/walker.py) 转移优先级 mux 链 |
| 名字即路径 | prefix 级联命名（`lfsm_wlk_*` / `lfsm_q_a_*` …） | [`lfsm_top.py`](../lfsm/lfsm_top.py)、[`emit_outs()`](../lfsm/types.py#L100) |
| 共享词汇表 | 微架构术语沉淀为 helper（`vec_rd` / `rr_scan` / `ring_add` …） | [`lfsm/types.py`](../lfsm/types.py) |

---

## 3. 维度一：可读性 → 对代码的把握

### 例 1：`walker.py` —— 一个 FSM 的全部秘密写在 160 行里

整个 MKN walk FSM 遵循统一"四段式"布局，读者第一次打开即可建立心智模型：

```text
Cycle 0: 状态声明 (domain.signal) → 输入 (sin) → 纯组合逻辑 → 次态表达式
         domain.next()
Cycle 1: 统一 <<= 提交
```

转移优先级核心逻辑是一条 mux 嵌套链，**逐行对应规格 [`01_FSM走法逻辑.md`](../../design_spec/docs/shared/01_FSM走法逻辑.md)
的优先级**（N_INNER > K_LOCAL > M_SLICE > N_OUTER > K_OUTER > DONE）：

> [lfsm/walker.py:81-86](../lfsm/walker.py#L81)

```python
tr = mux(n_inner + u(4, 1) < n_len, u(TR_W, TR_N_INNER),
     mux(k_local + u(4, 1) < k_count, u(TR_W, TR_K_LOCAL),
     mux(m_idx.zext(2) + u(2, 1) < cfg_mslice, u(TR_W, TR_M_SLICE),
     mux(~last_block, u(TR_W, TR_N_OUTER),
     mux(~last_outer, u(TR_W, TR_K_OUTER), u(TR_W, TR_DONE))))))
```

文件 [docstring](../lfsm/walker.py#L1) 开头 10 行即记录了本模块唯一的设计偏差（`n_len`/`k_count`
用组合计算替代寄存加载，修复 N_OUTER/K_OUTER 边界 off-by-one-block），并
写明它与 golden 的哪条性质（`current_n_len` property 语义）对应。
**把握一个模块不需要读全部代码——读 docstring + 四段式骨架即可。**

### 例 2：`rd_queue.py` —— 微架构意图两行写完

双写端口（RD + LaneLoadEnd 同拍入队）的优先级语义压缩成两行比较 + 两行
mux，注释就是规格原文：

> [lfsm/rd_queue.py:86-90](../lfsm/rd_queue.py#L86)

```python
hit0 = enq_rd_valid & (tail == u(PTR_W, i))
hit1 = enq_end_valid & ((tail + enq_rd_valid.zext(PTR_W))[0:PTR_W] == u(PTR_W, i))
v = mux(hit0, u(1, 0), is_end[i])
v = mux(hit1, u(1, 1), v)                      # END later (priority)
```

计数器语义一行读完：`cnt_nxt = cnt + enq_rd + enq_end - pop`
（[`rd_queue.py:100-101`](../lfsm/rd_queue.py#L100)）。不需要在脑内反编译 always 块。

### 例 3：`lfsm_top.py` —— 代码就是架构图

顶层调用链与计划 mermaid 框图一一对应：

```text
config_regs → walker → rdgen → 4×(rd_queue→assembler→cand_holder)
            → tag_checker → arbiter → req_sched → c_path
```

prefix 级联命名（`lfsm_cfg` / `lfsm_wlk` / `lfsm_q_a` …）让**仿真波形 /
MLIR 里的信号名 = 模块路径**，看波形时不用查映射表。跨模块前递线显式
声明为 `fw_*` named_wire（[`lfsm_top.py:110-123`](../lfsm/lfsm_top.py#L110)）——全设计有几处组合环、
在哪里，扫一眼 fw 列表就有数。

### 例 4：`types.py` —— 团队共享的微架构词汇表

[`vec_rd`](../lfsm/types.py#L123)（动态索引读 = one-hot tree mux）、[`ring_add`](../lfsm/types.py#L138)（2 幂环形指针）、
[`argmin4_key`](../lfsm/types.py#L172)（四路 argmin）、[`rr_scan`](../lfsm/types.py#L187)（RR 仲裁）——这些 helper 让
assembler / arbiter 的代码读起来是**架构术语而不是位操作**。每个
docstring 写明硬件形态和原因（"balanced tree mode, log-depth — linear mux
chains blow the pycc logic-depth limit"），把时序考量沉淀在词汇定义里。

---

## 4. 维度二：代码理解带来的帮助

### 例 5：时序结构可以从代码布局直接"数"出来

[`types.py`](../lfsm/types.py#L1) docstring 纪律（cycle 0 算完全部表达式，`domain.next()` 后只许
`<<=`）带来关键性质：**`domain.next()` 的次数 = 寄存器级数**。十步流程把
它固化为 Step 6 决策——"每带状态叶模块恰好 1 次内部 `domain.next()`"。
还有结构测试守着：

> [tests/unit/test_walker.py:130-133](../tests/unit/test_walker.py#L130)

```python
def test_walker_mlir_clean():
    """Structural: compiles, no balancing registers inserted."""
    mlir = compile_cycle_aware(build, name="tb_walker_top", eager=True).emit_mlir()
    assert "func.func" in mlir
    assert "_v5_bal" not in mlir
```

这正是 [pipeline 报告](pipeline划分修改工作记录与下一步方向评估.md) §5.1 门级深度估算表（R1 决策环 ≈15–20 级、R2 数据环
BMX 最深 ≈15–25 级）能够**在实现之前**做出来的原因：V6 代码结构与组合链
结构一一对应，**看代码就能谈时序**。GAP-06/07 的三拍分段讨论（held 快照
割断①、req_sched 割断②）本质是代码结构讨论——"在哪插寄存器"翻译成
"在哪个模块的 `<<=` 里加一级"；关键不变量"仲裁段全部输入只认 held 的
Q 端"可以直接在 [`cand_holder.py`](../lfsm/cand_holder.py) / [`arbiter.py`](../lfsm/arbiter.py) 的输入连线上人工检查。

### 例 6：A-001 首访去重 —— CAM 消失在 3 行代码里，且根因可追溯

golden 模型用 set 查重（[`load_path.py`](../../design_spec/code/four_eu/load_path.py) 的 `generated_keys`），直接硬件化
等于一块 CAM。决策利用 walk 顺序固定，把"见过没有"退化为计数器判零，
落地就是 walker 输出里的三个信号：

> [lfsm/walker.py:108-110](../lfsm/walker.py#L108)

```python
tok_fv_a=(n_base == u(8, 0)) & (n_inner == u(4, 0)),
tok_fv_b=m_idx == u(1, 0),
tok_fv_c=(k_base == u(6, 0)) & (k_local == u(4, 0)),
```

理解收益在于**完整证据链**：决策报告（为什么等价：循环嵌套
`k_outer→n_outer→m_slice→k_local→n_inner`）→ [`ASSUMPTIONS.md`](../docs/ASSUMPTIONS.md) A-001 登记
→ 代码 3 行 → golden 逐拍对拍兜底。任何人质疑"去重逻辑对不对"，沿着
这条链 10 分钟就能闭环。详见同目录
[《A-001_首访去重替代CAM_设计决策说明.md》](A-001_首访去重替代CAM_设计决策说明.md)。

### 例 7：一次规格演进的全影响面可见

[`design_spec/code/debug_records/20261014_112400_b_pair_quantized_layout.md`](../../design_spec/code/debug_records/20261014_112400_b_pair_quantized_layout.md)
记录了 B 奇数 N 尾改 mem-pad 的 freeze 全过程：

- **文档同步表**：规格 6 处 + V6 文档 4 处落点（精确到 F-056、
  PORT_LIST §4.4、SEQ §8.3、CYCLE §6.2）；
- **代码改动表**：6 个文件 + 2 个"无需改"并注明原因；
- **回归证据**：单测全绿、TYPICAL PASS=19 FAIL=0；
- **遗留项**：8EU fork 留待评审。

因为 V6 代码/文档/测试之间有 F-xxx ↔ T-xxx 追踪矩阵（44 功能 × 103 测试），
一次语义变更的**影响面是查表得出的，不是靠记忆搜索的**——"不静默省略"
（GAP-01…07 全部登记）是这套理解体系的纪律兜底。

---

## 5. 维度三：调试成本的帮助

### 例 8：对拍失败信息直接告诉你"哪一拍、哪个字段"

CycleAwareTb 的 expect 带周期消息，walker 单测每个 token 逐字段比对：

> [tests/unit/test_walker.py:68-73](../tests/unit/test_walker.py#L68)

```python
tb.expect("lfsm_wlk_tok_valid", 1, phase="pre", msg=f"valid c{cyc}")
tb.expect("lfsm_wlk_tok_advance", 1, phase="pre", msg=f"adv c{cyc}")
tb.expect("lfsm_wlk_tok_m", t["m_idx"], phase="pre", msg=f"m c{cyc}")
tb.expect("lfsm_wlk_tok_n", t["n_idx"], phase="pre", msg=f"n c{cyc}")
```

失败输出形如 `m c137: expected 1 got 0`——第一现场就有周期号和信号路径名
（prefix 命名红利）。集成侧 [`tests/lfsm_tb_common.py`](../tests/lfsm_tb_common.py) 的
`unit_walker / unit_enq / unit_emit / unit_cands` 把 golden 向量**按指令、
按 lane、按流水段切片**，系统级 failure 直接降到"第 i 条指令在 B lane 的
assembler 段"粒度，不用在全系统波形里捞针。

### 例 9：结构性自检在 elaboration 期抓错，仿真成本为零

例 5 的 `_v5_bal` 断言、`assert "func.func" in mlir` 这类检查跑在
`compile_cycle_aware(...).emit_mlir()` 上——**不启动仿真器就能抓纪律违例**
（如意外插入的平衡寄存器 = pipeline 划分被破坏）。eager 路径还允许在设计
代码里插 `print` 观察展开过程、`emit_mlir()` 直接看生成物。

### 例 10：instance eval cache bug（2026-10-15）—— 层次化结构降低隔离成本

完整 root-cause 记录在 [`tests/lfsm_tb_common.py:63-73`](../tests/lfsm_tb_common.py#L63) 注释。症状：反压
窗口下 A-seq65 丢失 + B-seq48 重复。定位路径体现 V6 结构的调试红利：

1. **同一激励，flat 编译通过、hierarchical 失败** → 问题锁定在层次化
   求值而非设计逻辑；
2. 层次化模块边界让复现压缩到最小——[`tests/integration/test_rqp_hier.py`](../tests/integration/test_rqp_hier.py)
   （"minimal hierarchical repro of the req_sched cnt glitch"）只含
   req_sched 一个真实模块；
3. 根因 = req_sched 的 room→arbiter→push 环路上 instance eval cache 错误
   跳过一次必需重估，workaround = `-DPYC_DISABLE_INSTANCE_EVAL_CACHE`
   （工具链问题已记录，待 gate-first 修复）。

若是扁平大网表，"哪个状态元件提交错了"的隔离成本会高得多。

### 例 11：反压行为审查 = 检查 `when` 条件清单

[pipeline 报告](pipeline划分修改工作记录与下一步方向评估.md) §4.3 明确"**无独立反压状态机**"：`dest_ok=0` /
`mem_ready=0` 等一切保持行为都经 `assign(when=)` 的条件使能实现。审查反压
正确性不需要追踪 FSM 状态迁移——逐寄存器检查 `when` 表达式即可；
[`tests/integration/test_backpressure.py`](../tests/integration/test_backpressure.py) 的 hold 不变量测试直接对应这些
条件。

### 例 12：walker off-by-one 的修复方式本身降低了回归成本

例 1 提到的 docstring 偏差：原 Step-6 伪码在 N_OUTER/K_OUTER 边界"加载
寄存器"的写法会 off-by-one-block（9→[4,5]、10→[4,6]、17→[8,4,5] 等尾块
形状）。修复不是加补丁，而是**改成与 golden property 语义逐字对应的组合
计算**——修完后这些尾块形状全部进入 [`test_walker.py:30-42`](../tests/unit/test_walker.py#L30) 的 CASES 矩阵
固化。**调试产出（对失败形状的洞察）直接转化为回归资产**，同类 bug 不会
再活过一次提交。

---

## 6. 小结：三个维度的因果链

| 维度 | V6 机制 | LFSM 实证 |
| :--- | :--- | :--- |
| 代码把握 | 四段式骨架、mux 即优先级、prefix=路径、共享词汇表 | walker / rd_queue / lfsm_top / types |
| 代码理解 | `domain.next()` 计数 = 寄存器级数、代码结构 ≈ 组合链结构、F↔T 追踪 | 深度估算表、A-001 三行证据链、GAP 登记、freeze 影响面查表 |
| 调试成本 | 对拍消息带周期/路径、结构断言零仿真、eager 可 print、层次化可隔离 | `msg=c{cyc}`、`_v5_bal` 断言、eval cache 最小复现、反压 when 清单 |

---

## 7. 相关文档索引

| 材料 | 位置 |
| :--- | :--- |
| V6 语言规范 / 教程 | [docs/v6_PyCircuit_Specification.md](../../../../docs/v6_PyCircuit_Specification.md)、[docs/v6_PyCircuit_Tutorial.md](../../../../docs/v6_PyCircuit_Tutorial.md) |
| 周期感知设计体现 | 同目录[《V6周期感知_CycleAware设计_LFSM代码体现.md》](V6周期感知_CycleAware设计_LFSM代码体现.md) |
| 实例代码 | `designs/LFSM/pycircuit/lfsm/`（[walker](../lfsm/walker.py) / [rd_queue](../lfsm/rd_queue.py) / [lfsm_top](../lfsm/lfsm_top.py) / [types](../lfsm/types.py) 等） |
| 测试实例 | `designs/LFSM/pycircuit/tests/`（[unit](../tests/unit/test_walker.py) / [integration](../tests/integration/test_backpressure.py) / [lfsm_tb_common](../tests/lfsm_tb_common.py)） |
| 十步流程与证据链 | 同目录[《十步工作流流程图_LFSM设计实例.md》](十步工作流流程图_LFSM设计实例.md) |
| A-001 决策全过程 | 同目录[《A-001_首访去重替代CAM_设计决策说明.md》](A-001_首访去重替代CAM_设计决策说明.md) |
| pipeline 三拍分段与深度估算 | 同目录[《pipeline划分修改工作记录与下一步方向评估.md》](pipeline划分修改工作记录与下一步方向评估.md) |
| 规格演进 freeze 记录 | [designs/LFSM/design_spec/code/debug_records/20261014_112400_b_pair_quantized_layout.md](../../design_spec/code/debug_records/20261014_112400_b_pair_quantized_layout.md) |
| 追踪与偏差登记 | [designs/LFSM/pycircuit/docs/TRACEABILITY.md](../docs/TRACEABILITY.md)（GAP-01…07）、[ASSUMPTIONS.md](../docs/ASSUMPTIONS.md)（A-001…A-014） |
