# V6 可读性 head-to-head：手写 RTL `mkn_walker.v` vs V6 `walker.py`（FSM 跳转）

> 汇报材料 · LFSM（4EU UU mode）PyCircuit V6 设计
> 事项：同一 MKN walk FSM 的**跳转功能**在两份实现中的可读性对比——手写
> Verilog RTL（[`mkn_walker.v`](./mkn_walker.v)，本目录存档件）vs PyCircuit V6
> （[`lfsm/walker.py`](../lfsm/walker.py)）
> 姊妹篇：[《V6代码可读性_代码理解_调试成本_LFSM实例.md》](./V6代码可读性_代码理解_调试成本_LFSM实例.md)
> （本文沿用其"代码把握 / 代码理解 / 调试成本"三维度框架）
> 规格来源：[docs/shared/01_FSM走法逻辑.md](../../design_spec/docs/shared/01_FSM走法逻辑.md)
> 整理日期：2026-10-16
> **行号基准**：文中所有行号以与本文件同一次提交的两个源文件版本为准。

---

## 1. 一句话概述

同一条 6 级转移优先级链、同一份 N 块划分规则、同一份 stall/done 语义：
手写 RTL 需要"注释 + 外部原语契约 + 规格文档"三件套才能还原语义，V6 把
规格语义直接写成代码形态——**规格里的循环嵌套变量就是信号名，转移优先级
就是 mux 嵌套顺序，次态优先级就是行序，寄存器级数就是 `domain.next()` 次数**。

---

## 2. 对比对象界定（先说公平性）

### 2.1 语义等价性核对（逐项对过）

| 语义点 | `mkn_walker.v` | `walker.py` | 等价 |
| :--- | :--- | :--- | :--- |
| 转移优先级 | `always @*` if-else（L263-271） | `mux` 嵌套链（L81-86） | ✅ 同序 |
| N 块划分 | 闭式 `len=(R<9)?R:(R<=10)?4:8` + `n_bound` 寄存器 | `_n_len_rule(rem)` 纯函数（L40-43） | ✅ 同规则 |
| K 边界 | `k_idx+1` 对 8/4 对齐或 == `k_groups`（L247-258） | `k_count=min(k_step, k_groups-k_base)`（L74-75） | ✅ |
| M 边界 | `m_idx+1 >= m_slice_count`（L260-261） | `m_idx+1 < m_slice` 继续（L83） | ✅ |
| N_OUTER 条件 | `n_bound == cfg_n_hw_count`（L244） | `n_base + n_len == cfg_nhw`（L77） | ✅ |
| K_OUTER 条件 | `k_next == cfg_k_groups`（L258） | `k_base + k_count == cfg_kgroups`（L78） | ✅ |
| stall 保持 | `i_stall_en` 逐实例分发 + `advance` 门控 | `advance = active & ~stall`，次态默认保持 | ✅ |
| done 时序 | `o_walk_done = active & advance & TR_DONE`（L477） | `tok_done = advance & (tr==TR_DONE)`（L88） | ✅ |

### 2.2 不等价的职责（对比时折算掉）

| 项 | `mkn_walker.v`（565 行） | `walker.py`（160 行） |
| :--- | :--- | :--- |
| 状态分解 | 绝对索引 `n_idx/k_idx/m_idx` + `addr_gen` 内部 savepoint（检查点/返回） | `n_base+n_inner` / `k_base+k_local` 分解（循环嵌套直写） |
| 额外职责 | `bufc_idx`（L420-451）、`kn_linear` 消乘法器（L368-394）、`n_index_double` 配对、cfg 回读，≈130 行 | 无（配对走 mem-pad 方案，地址辅助在其他模块） |
| n_span | `cfg_n_step` 1\|2，`cur_n_span=min(n_step, n_rem)`（L233-240） | 无此概念 |
| k_step 来源 | 由 `m_mode` 推导（m16→8, m32→4，L247-256） | 直接输入 `cfg_k_step`（L69） |
| 规格词汇 | `k_local`/`n_inner` **不作为信号存在**，由 savepoint 间接表达 | 规格嵌套 `k_outer→n_outer→m_slice→k_local→n_inner` 同构出现 |

### 2.3 行数结算

- `mkn_walker.v` 总 565 行 = 头注 61 + 附加功能 ≈130 + sim guard 36 + **核心 FSM ≈370**，
  且 FSM 逻辑散布在 L190-525。
- `walker.py` 总 160 行 = docstring 12 + 状态/输入声明 + **转移+次态核心 L73-152 约 80 行全覆盖**。
- 扣除附加功能后核心 FSM 仍 ≈370 vs ≈150（≈2.4 倍）。

---

## 3. 转移优先级：块本身都清晰，差距在"定义距离"

单看转移块，两边都一目了然——`.v` 的 if-else 甚至对 RTL 工程师更亲切：

> [mkn_walker.v:263-271](./mkn_walker.v#L263)

```verilog
reg [2:0] transition;
always @* begin
    if (!last_n_inner)       transition = TR_N_INNER;
    else if (!last_k_local)  transition = TR_K_LOCAL;
    else if (!last_m_slice)  transition = TR_M_SLICE;
    else if (!last_n_outer)  transition = TR_N_OUTER;
    else if (!last_k_outer)  transition = TR_K_OUTER;
    else                     transition = TR_DONE;
end
```

> [walker.py:81-86](../lfsm/walker.py#L81)

```python
tr = mux(n_inner + u(4, 1) < n_len, u(TR_W, TR_N_INNER),
     mux(k_local + u(4, 1) < k_count, u(TR_W, TR_K_LOCAL),
     mux(m_idx.zext(2) + u(2, 1) < cfg_mslice, u(TR_W, TR_M_SLICE),
     mux(~last_block, u(TR_W, TR_N_OUTER),
     mux(~last_outer, u(TR_W, TR_K_OUTER), u(TR_W, TR_DONE))))))
```

差距不在块本身，而在**理解一个条件需要回溯多远**：

- **V6**：`n_inner + 1 < n_len` 中的 `n_len` 定义在 8 行之前（`walker.py:73`），
  规则函数 `_n_len_rule` 在文件顶部（`walker.py:40-43`）带规格引用
  （SRC-02 §3.5.2）。**定义距离 ≤10 行**；且 `mux` 链即硬件形态——优先级
  编码深度就是嵌套层数，"看代码就能谈时序"。
- **RTL**：`last_n_inner` 定义在 20 行前（`mkn_walker.v:243`，`= n_rem_fits`）
  → `n_rem_fits`/`n_rem` 在 L233-236 → 依赖 `n_bound` 寄存器（L285-306）
  → 依赖闭式 len 计算（L190-228）。完整闭环一个条件要回溯 **~100 行、
  4 层定义链**；且 `always @*` if-else 是仿真语义，优先级逻辑靠综合器
  推断，门级形态不可直读。

---

## 4. N 块划分：寄存器 + 独热 mux 云 vs 一个带 docstring 的纯函数

同一规则 `len = (R<9) ? R : (R<=10) ? 4 : 8`：

- **RTL**：`n_bound` 边界寄存器 + `r_init`/`r_next` 两套独热化计算 + 累加
  mux（`mkn_walker.v:190-228` 与 `285-306`，≈60 行），另有 `n_rem_fits`
  支持 n_span 截断（L233-240）。
- **V6**：

> [walker.py:40-43](../lfsm/walker.py#L40)

```python
def _n_len_rule(rem):
    """``rem∈{9,10} ? 4 : min(8, rem)`` — SRC-02 sec 3.5.2 balanced split."""
    return mux((rem == u(8, 9)) | (rem == u(8, 10)), u(4, 4),
               mux(rem > u(8, 8), u(4, 8), rem[0:4]))
```

配合 `walker.py:73-78` 两行，`last_block`/`last_outer` 就是基址+长度的
等值判断。这正是 walker.py docstring 登记的那处设计偏差（`n_len` 组合
计算 = golden `current_n_len` property 语义，修复 9→[4,5]、17→[8,4,5]
尾块 off-by-one）——**偏差说明、规格出处、golden 对应物写在文件开头 12
行内**；`.v` 的头注虽然完整（L1-61），但信息载体是注释而非代码。

---

## 5. 计数器次态：两跳阅读 vs 一跳直读

问题"K_LOCAL 时 `n_idx` 归几？"：

- **RTL（两跳）**：先查控制汇聚 `adv_k_local`（L276-281）→ 查 `u_n_idx`
  的 `i_return_en = n_ret_en = adv_k_local | adv_m_slice`（L318-334）→
  再回忆/查阅 `addr_gen` 的 return 语义是"恢复 savepoint"，而 savepoint 由
  `i_record_nxt_en=adv_n_outer` 在上次 N_OUTER 更新。**第二跳的原语
  `rtl/prim/addr_gen.v` 不在本仓库**——savepoint 寄存器在 walker 源码中
  不可见，是隐藏状态。5 个实例共 ~135 行端口映射，行为靠实例上方注释
  声明意图（如 L311-315）。

> [mkn_walker.v:310-339](./mkn_walker.v#L310)（节选）

```verilog
// N index: plus n_span within and across blocks (...); return to the
// block-base savepoint on K_LOCAL / M_SLICE; re-init on K_OUTER / accept.
wire               n_ret_en      = adv_k_local | adv_m_slice;
addr_gen #(.ADDR_WIDTH (N_IDX_W), ...) u_n_idx (
    .i_stall_en       (stall),
    .i_init_en        (n_init_en),
    .i_plus_en        (n_plus_en),
    .i_record_nxt_en  (adv_n_outer),
    .i_return_en      (n_ret_en),
    // ...
    .o_addr_out       (n_idx),
);
```

- **V6（一跳）**：每信号一张"次态真值表"，行序即优先级，首行默认值即
  hold：

> [walker.py:124-127](../lfsm/walker.py#L124)

```python
ni_nxt = n_inner
ni_nxt = mux(advance & (tr == u(TR_W, TR_N_INNER)), (n_inner + u(4, 1))[0:4], ni_nxt)
ni_nxt = mux(advance & (tr != u(TR_W, TR_N_INNER)), u(4, 0), ni_nxt)
ni_nxt = mux(start == u(1, 1), u(4, 0), ni_nxt)
```

stall 语义同理：`.v` 把 `i_stall_en` 逐实例分发（5 处端口）；V6 一个
`advance = active & ~stall`（`walker.py:88`）门控全部次态链，保持是 mux
默认值，**不需要任何代码表达"不动"**。

---

## 6. 寄存器级数与时序

- **V6**：1 次 `domain.next()`（`walker.py:143`）= 1 级寄存器。四段式骨架
  （状态声明 → 组合/次态 → `domain.next()` → `<<=` 提交）让时序结构从
  代码布局直接数出来（主报告例 5 的门级深度估算即靠此性质）。
- **RTL**：需数 9 个状态实例（5 `addr_gen` + `reg_n_bound` + `reg_cfg` +
  `reg_active` + `reg_walk_seq`），且"addr_gen/reg_en 是仅有时序原语"这条
  信息写在注释里（L150-153）——又是注释承担。两边实际都是 1 级寄存器，
  但 V6 是**可数出来的**，RTL 是**注释声明的**。

---

## 7. 三维度结算（沿用主报告框架）

| 维度 | `mkn_walker.v` | `walker.py` | 差距来源 |
| :--- | :--- | :--- | :--- |
| 代码把握 | 565 行，规格映射在 61 行头注 + 实例注释；需先建立 addr_gen 心智模型 | 160 行，docstring + 四段式骨架；mux 链=优先级、行序=更新优先级 | 语义载体：注释 vs 代码 |
| 代码理解 | 转移条件定义链 ~100 行/4 层；寄存器级数数实例+信注释；savepoint 是外部原语隐藏状态 | 定义距离 ≤10 行；`domain.next()` 计数=级数；无隐藏状态 | 两跳阅读 vs 一跳；结构≈组合链 |
| 调试成本 | sim guard 质量高（溢出/kn_linear 交叉验证/n_bound sanity，L527-562），但触发在仿真时、粒度是 `$time+%m` | 逐字段 expect 带周期号（主报告例 8）、`_v5_bal` 结构断言零仿真（例 9）、prefix=波形路径 | 定位粒度：时间戳 vs 周期+字段 |

---

## 8. 公平性说明与结论

`mkn_walker.v` 不是烂 RTL——它原语化（全模块只剩 1 个 always 块）、独热
mux、头注精确到规格章节号，已是手写 Verilog 的纪律上限。差距主要来自
**表达媒介**：同一个 FSM，Verilog 版需要"注释 + 外部原语契约 + 规格文档"
三件套才能还原语义，且状态正确性依赖 addr_gen 内部不可见的 savepoint；
V6 版把规格语义直接写成代码形态。这是主报告 §2"硬件语义显式化"在
FSM 跳转这个最小功能切片上的实证：**理解成本低的地方，调试成本自然
跟着低**——`.v` 里"K_LOCAL 时 n_idx 归几"需要两跳推理，`.py` 里是一行
直读。

---

## 9. 相关文档索引

| 材料 | 位置 |
| :--- | :--- |
| 对比源文件（RTL 存档件） | [mkn_walker.v](./mkn_walker.v) |
| 对比源文件（V6 设计） | [lfsm/walker.py](../lfsm/walker.py) |
| 三维度框架主报告 | [V6代码可读性_代码理解_调试成本_LFSM实例.md](./V6代码可读性_代码理解_调试成本_LFSM实例.md) |
| FSM 走法规格 | [docs/shared/01_FSM走法逻辑.md](../../design_spec/docs/shared/01_FSM走法逻辑.md) |
| 周期感知设计体现 | [V6周期感知_CycleAware设计_LFSM代码体现.md](./V6周期感知_CycleAware设计_LFSM代码体现.md) |
