# A-001 首访去重替代 CAM —— 设计决策说明

> 汇报材料 · LFSM（4EU UU mode）PyCircuit V6 设计
> 决策编号：A-001（`docs/ASSUMPTIONS.md`）；功能编号：F-020 / F-025（`docs/FEATURE_LIST.md`）
> 整理日期：2026-10-15；状态：已决策，进入实现对拍阶段（计划 I2 增量）

---

## 1. 一句话摘要

规格要求 RdGenerator 对 data key 做"首访去重"（同一数据块每条指令只加载一次）。
Golden 参考模型用 **set 集合查重**实现；直接硬件化等价于造一块 **CAM**。
本决策利用 **walk 遍历顺序固定**这一性质，把"该 key 是否见过"退化为对 walker
**现有循环计数器的判零条件**，零 CAM、零历史 key 存储，等价性由与 golden 的
逐拍对拍保证。

---

## 2. 背景：为什么需要去重

MKN walker 在遍历 (m, n, k) 空间时，同一个数据块会被**反复访问**——这正是
数据复用的来源。例如 A 矩阵的一个块 `(m, k)` 会在每一个 n 位置都被走到一次，
但它只需要从 MEM 加载一次。

因此规格（`02_LFSM.md` sec 7.2）要求：每个唯一的 **data key** 只生成一条逻辑
RD 请求。三类 key 的构成：

| 集合 | data key | 含义 |
| :--- | :--- | :--- |
| A/AMX | `(inst_id, m_idx, k_idx)` | A 操作数块，按 (m,k) 寻址，与 n 无关 |
| B/BMX | `(inst_id, k_idx, n_idx)` | B 操作数块，按 (k,n) 寻址，与 m 无关 |
| C | `(inst_id, m_idx, n_idx)` | C 结果写回/加载块，按 (m,n) 寻址，与 k 无关 |

---

## 3. Golden 参考实现：set 查重

Python 参考模型（`design_spec/code/four_eu/load_path.py`）为每 `(inst, lane)`
维护一个 `generated_keys` 集合，逐 token 查重：

```python
# golden：data key 计算（load_path.py::_data_key）
if lane in (Lane.A, Lane.AMX):
    return (instruction.inst_id, token.m_idx, token.k_idx)
return (instruction.inst_id, token.k_idx, n_idx)

# golden：去重判定（load_path.py::_needed_rds）
if key not in self.generated_keys.setdefault((instruction.inst_id, lane), set()):
    needed.append(RdNeed(lane=lane, n_idx=n_idx))
```

语义要点：**evaluate 只查不登记，commit（成功入队）才 `add` 进集合**。

---

## 4. 直接硬件化的问题：这是一块 CAM

若硬件照搬"存下所有历史 key、新 key 全量比对"的语义，就需要一块
**CAM（Content-Addressable Memory，内容寻址存储器）**：

- 普通 RAM：给地址 → 读数据；CAM：给 key → 同拍并行比对所有条目，回答
  "在不在 / 在哪"。
- **面积大**：每个存储位都要配比较逻辑，成本远高于同容量 SRAM/寄存器堆。
- **时序差**：全阵列并行 match 的线长与延迟随条目数增长。
- **规模难定**：key 数量随 instruction 的 (m, n, k) 规模变化，容量上限不好取。

对于一个每拍都要做的判定，CAM 是明显的过度设计。

---

## 5. 改进方案：首访判定退化为计数器判零

### 5.1 关键洞察

walk 的循环嵌套顺序是**固定的**（`01_FSM走法逻辑.md`；由外到内）：

```
k_outer → n_outer → m_slice → k_local → n_inner
```

遍历顺序固定 ⟹ 每个唯一 key 的**首次出现点可以静态预测**：它恰好落在
"构成该 key 之外的那些内层循环计数器全为 0"的那个 token 上。
于是"这个 key 见过没有"不再需要查历史，只需看当前计数器：

| 集合 | data key | 与 key 无关的循环维度 | 新 key ⟺ 首访条件 |
| :--- | :--- | :--- | :--- |
| A/AMX | `(inst, m, k)` | n_outer、n_inner | `cnt_n_outer==0 && cnt_n_inner==0` |
| B/BMX | `(inst, k, n)` | m_slice | `m_idx==0` |
| C | `(inst, m, n)` | k_outer、k_local | `cnt_k_outer==0 && k_local==0` |

### 5.2 逐条推导

- **A/AMX**（key 不含 n）：固定 `(m,k)` 在每个 n_outer block 内被访问一遍
  （n_inner 扫满整个 block）。按字典序，全 instruction 的首次访问 = 第一个
  n_outer block 的第一个 n_inner 位置 ⟺ `cnt_n_outer==0 && cnt_n_inner==0`。
- **B/BMX**（key 不含 m）：`k_idx = cnt_k_outer*k_step + k_local` 与
  `(cnt_k_outer, k_local)` 一一对应（尾 outer 的 `k_count<k_step` 区间仍不相交）。
  固定 `(k,n)` 只随 m_idx 重访（m32 时有 m_idx=1），首访 ⟺ `m_idx==0`。
  **m16 特例**：m_idx 恒 0，每个 token 都是新 key——与规格"4EU 每 token 最多
  一条 B"一致。
- **C**（key 不含 k）：固定 `(m,n)` 随 `k_local`、`cnt_k_outer` 重访，首访 ⟺
  `cnt_k_outer==0 && k_local==0`。

### 5.3 与 golden evaluate/commit 分割的对应

"成功入队才登记 key"映射为：首访条件仅在 `walk_advance` **commit** 时生效；
walker stall 时条件会被重复求值，但不产生新入队——与 golden 中 evaluate 查、
commit 才 `add` 的分割精确一致（UU baseline 中该 stall 分支 dormant，保留是
为与 EFSM 共享 walker 语义完整）。

---

## 6. 实现落点（v3 现状）

**Walker 在生成 token 时顺带算出三个首访标志**，RdGenerator 直接消费，连
比较器都不用单独摆：

```python
# ALGORITHM_SEQUENTIAL.md §5.1（walker token 生成）
fv_a = (S.n_base==0 and S.cnt_n_inner==0)   # A/AMX 新 key（A-001）
fv_b = (S.m_idx==0)                          # B/BMX 新 key（A-001）
fv_c = (S.k_base==0 and S.k_local==0)        # C 新 key（A-001）
```

```python
# ALGORITHM_SEQUENTIAL.md §6（rdgen 消费）
if tok.fv_a:  needs[A]  = RdEntryA(...)      # + AMX（mx_en 时）
if tok.fv_b:  needs[B]  = RdEntryB(...)      # + BMX（mx_en 时）
if tok.fv_c:  c = CEntry(...)                # 入 C FIFO
```

**v3 修订（A-005 v3，2026-10-13 用户决策）**：WalkConfig 不再下发 loop 几何
（`n_blocks[]`/`n_outer_count` 等移除），walker 加法级现场维护 `n_base/n_len/
k_base`。因此外圈判据由 `cnt_n_outer==0`/`cnt_k_outer==0` 改写为等价的
`n_base==0`/`k_base==0`，思想不变，还顺带消除了 TOP 侧除法与 n_blocks 寄存
数组。

---

## 7. 等价性验证策略

计数器条件 ⟺ set 去重，**不做形式化证明，靠 golden 逐拍对拍冻结**：

- `tools/dump_lfsm_golden.py` dump golden set-based 的每拍 `needed_rds` /
  owner 流为 JSON 向量（`vectors/`）；
- V6 计数器版逐拍比对，任何一次漏判/误判立即失配；
- 覆盖矩阵：**m16/m32 × 单/多 n_outer block × K outer 重访**（含 m32
  return-base 不重载回归）；
- 追踪挂钩：F-020（A/B 去重）→ T-029 / T-030 / T-071；F-025（C 去重）→ T-031。

---

## 8. 收益小结

| 维度 | set/CAM 方案 | 计数器条件方案 |
| :--- | :--- | :--- |
| 历史 key 存储 | 需要（容量随 instruction 规模） | **零** |
| 内容寻址逻辑 | CAM 全阵列并行比较 | **零**（几个计数器判零） |
| 判定延迟 | 随条目数增长 | O(1) 纯组合 |
| 附加收益 | — | walker 顺带产出 `fv_*`；v3 还省掉 loop 几何下发 |

---

## 9. 风险与边界

- **强依赖 walk 顺序固定**：若未来 walker 走法改变（新的循环嵌套/跳步），
  首访条件必须重新论证，不能直接沿用。
- **作用域为 UU baseline**：C 的条件对应 key `(inst,m,n)`；TMEM mode 的 C key
  含 k_outer 维度、RU overlay 另有分流仲裁，均不在本决策范围内（本轮范围外）。
- **等价性锚定对拍覆盖**：正确性证据 = TYPICAL_CASES 覆盖矩阵下的逐拍对拍；
  矩阵外的极端形状依赖 never-full/对拍回归兜底。

---

## 10. 相关文档索引

| 文档 | 位置 |
| :--- | :--- |
| 决策原文 | `designs/LFSM/pycircuit/docs/ASSUMPTIONS.md` A-001 |
| 功能 checklist | `designs/LFSM/pycircuit/docs/FEATURE_LIST.md` F-020 / F-025 |
| 算法伪码 | `designs/LFSM/pycircuit/docs/ALGORITHM_SEQUENTIAL.md` §5.1 / §6 / §14.1 |
| 追踪矩阵 | `designs/LFSM/pycircuit/docs/TRACEABILITY.md`（F-020 → T-029/030/071） |
| 规格输入 | `designs/LFSM/design_spec/docs/four_eu/02_LFSM.md` sec 7.2；`docs/shared/01_FSM走法逻辑.md` |
| Golden 实现 | `designs/LFSM/design_spec/code/four_eu/load_path.py`（`_data_key` / `_needed_rds`）；`designs/LFSM/design_spec/code/mkn_walker.py` |
| 总体计划 | `.cursor/plans/lfsm_uu_v6_设计实现_d9a4c45e.plan.md`（关键微架构决策第 1 条） |
