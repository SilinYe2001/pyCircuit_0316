# LFSM (4EU UU mode) ALGORITHM_PIPELINED

> Step 5 交付物（依据 `docs/pycircuit_implementation_method.md` Step 5：
> 「Align sequential description with cycle-aware hardware」）。把
> `ALGORITHM_SEQUENTIAL.md`（下称 SEQ）的子程序映射到时钟周期：
> **cycle 映射**、**三边 bypass 链**、**寄存器推断规则**、**存储原语
> 选型**、`domain.call()` 子模块边界与 `inputs` 键映射、prefix 级联。
> 建立日期：2026-10-13。
> 上游：SEQ（子程序/状态清单）、`PORT_LIST.md`（端口/位宽/prefix）、
> `ASSUMPTIONS.md`（A-001…A-011）、`FEATURE_LIST.md`（F-xxx）。
> 下游：`ALGORITHM_CYCLE_AWARE_PSEUDOCODE.md`（Step 6，逐行可译 V6 伪码）。
> V6 规范引用：PRC-01 = `docs/v6_PyCircuit_Specification.md`。

## 1. Cycle 映射总原则（A-008）

规格的 evaluate/commit 两拍语义（SRC-01 sec 5，R-34）映射为 V6 的
**cycle-0 组合求值 + cycle-1 寄存提交**：

| 规格相位 | V6 实现 | 涉及内容 |
| :--- | :--- | :--- |
| evaluate：只读 cycle-start 状态 | 子模块在**自身 cycle 0** 读取 `domain.signal()`（读周期 0）并纯组合求值 | token、queue head view、asm 展开视图、candidate/eligibility/grant、`o_load_range_query`、`o_reg_req_*`、`o_mem_req_*`/`o_load_ptr_update_*`（= **req_sched 队列 front 寄存直出**，A-014 后不再由当拍组合链直驱）、`issue_room` |
| commit：原子提交 | `domain.next()` 后在**自身 cycle 1** 用 `<<=` / `.assign(when=)` 写回（写周期 1） | 全部状态：counter、指针、context、held、FIFO 存储 |

**每个带状态子模块的内部结构固定为**：

```python
def leaf(m, domain, *, inputs=None, prefix=..., **cfg):
    # ── cycle 0：声明状态（读周期 0）+ 全部组合求值 + 组装 outs（CAS, cycle=0）
    ...
    domain.next()          # 内部仅 1 次
    # ── cycle 1：全部寄存器提交（写周期 1 → 读 0 写 1 → 各推导 1 级 DFF，PRC-01 §4）
    ...
    return outs            # 全部输出为 cycle-0 CAS
```

- **内部 `domain.next()` 数**：每个带状态叶模块 = **1**；`lfsm_top` 自身
  无状态 = **0**（纯连线 + 输出收集）。
- 读 0 写 1 → 每信号恰好 1 级 DFF；本设计**无** gap≥2 流水反馈、**无**
  gap-0 组合赋值（全状态统一拍末提交）；`domain.cycle()` 不使用
  （无独立命名流水级需求）。
- 自动周期平衡（PRC-01 §6）在本设计**不应触发**：所有跨模块消费的信号
  都是 cycle-0 CAS；Step 9 以 MLIR 检查无意外 `pyc.reg` 链作为
  sign-off 检查项之一。

## 2. 子模块边界与 `domain.call()` 链

层次（prefix 级联，PRC-01 §7.4；PORT_LIST §9）：

```text
lfsm_top (prefix "lfsm", 内部 next=0)
├── domain.call(config_regs,  prefix="lfsm_cfg")      # next=1
├── domain.call(walker,       prefix="lfsm_wlk")      # next=1
├── domain.call(rdgen,        prefix="lfsm_rdg")      # next=1
├── for lane in [a, amx, b, bmx]:                      # Python 循环静态展开 4 实例
│   ├── domain.call(rd_queue,     prefix=f"lfsm_q_{lane}")    # next=1
│   ├── domain.call(assembler_{lane}, prefix=f"lfsm_asm_{lane}")  # next=1（几何各异）
│   └── domain.call(cand_holder,  prefix=f"lfsm_chd_{lane}")  # next=1（同构 ×4）
├── domain.call(tag_checker,  prefix="lfsm_tck")      # next=1（对应规格 DestinationAllocator）
├── domain.call(arbiter,      prefix="lfsm_arb")      # next=1（纯控制；payload mux 在顶层 §11A → §11B 队列）
├── domain.call(req_sched,   prefix="lfsm_rqp")      # next=1（A-014 发送队列 2-slot；issue 拍端口直出）
└── domain.call(c_path,       prefix="lfsm_c")        # next=1
```

- `domain.call()` 自动 push/pop 周期隔离（PRC-01 §6/§7.3）：每个子模块
  内部的 `domain.next()` 不影响父模块 cycle 计数；父模块全程停留在
  cycle 0 调用全部子模块。
- **入口周期约定**：全部子模块的输入都在其自身 **cycle 0** 采样；
  输出 dict 全部在自身 cycle 0 组装（cycle 0 CAS）——这是三边相位契约
  （边3 为 held 寄存割断）与跨模块组合链不插入意外 DFF 的充要条件。
- **cycle provenance**（PRC-01 §7.3 第 4 步）：父模块 cycle-0 CAS →
  子模块 `inputs` → 子模块内部仍以 cycle 0 引用；子模块返回的
  cycle-0 CAS 供父模块内后续子模块（同拍）继续消费。
- 四 lane 同构部分（rd_queue/cand_holder）用同一函数实例化：rd_queue
  按 lane 传 `depth` + payload 字段集；cand_holder 仅 `prefix`（无几何
  参数）；assembler 几何各异分四个函数（`assembler_a/b/amx/bmx`），
  按 lane 传 `full_count/block_bytes`，共享同一份「统一骨架」注释
  约定（SEQ §8.0）。

### 2.1 子模块签名模板

```python
def rd_queue(m, domain, *, inputs=None, depth=16, prefix="lfsm_q_a") -> dict: ...
rd_queue.__pycircuit_name__ = "rd_queue"
```

配置参数（keyword-only，build-time 静态，PORT_LIST §3）：
`depth`（队列）、`full_count/block_bytes`（assembler）、
`lane`（编码）、顶层 `LOAD_BUS_BYTES/BUFA_SLOTS/.../A_BLOCK_ORDER/
RDQ_*_DEPTH/C_FIFO_DEPTH/CFG_FIFO_DEPTH/BMX_WINDOW_POOL` 经
`lfsm_top` 参数透传。`INST_ID_W/ADDR_W/RDGEN_ID_W/CAND_SEQ_W/
TAG_IDX_W/TAG_ADV_W/BYTE_CNT_W/BYTE_OFF_W` 为全局位宽常量（types.py）。

## 3. 三边相位契约的周期实现（R-11/F-031/F-073）

| 边 | 规格 | V6 实现 |
| :--- | :--- | :--- |
| 边1 Queue→Assembler **无同拍 bypass** | rdgen 拍末 commit 入队，次拍起可见；每拍每 lane ≤1 cycle-start head；反压保持 | queue 存储 = `domain.signal` 数组，head view 在 cycle 0 **直读寄存器**；rdgen 入队走 cycle-1 `<<=`。新 entry 物理上不可能在当拍出现在 head——用存储相位实现，无需额外 gate |
| 边2 Assembler→Packer **允许同拍 bypass**（规格边名；本设计实现为 assembler→cand_holder） | 拍初 head 本拍形成的 DataBlock 可本拍进 cand_holder | asm 的 `emit/incoming` 展开视图是 **cycle-0 纯组合函数**（输入：queue head 寄存器 + context 寄存器）；cand_holder 的 form 判定同为 cycle-0 组合 |
| 边3 Packer→Arbiter **不允许同拍**（**2026-10-14 用户决策**：严格流水；相对 SRC-01 sec 5「允许」取**规格偏差**；本设计实现为 cand_holder→arbiter） | 规格 baseline 为「本拍新 candidate 可本拍 fire」；本设计禁用该旁路 | **仲裁输入束只认 held 快照寄存（Q 端）**：`present_* = held_*`，fresh candidate 形成拍仅供拍末 held 捕获（cycle-1 `assign`），**次拍起**参与 tag_checker 的 dest_ok 与 arbiter 仲裁/fire（链首 +1 拍）。arbiter 全部数据/键类输入同源于该 held 快照（同步同拍进入）；`source_ok/i_register_ready` 与 `i_load_range_idle` 保持当拍电平采样（eligibility 每拍重算，R-34/SRC-07 sec 3(9)）；`i_shared_mem_ready` 在 **§11B 队列出口（issue 拍）** 当拍电平采样、不进 eligibility（A-014/GAP-07；eligibility 用 `issue_room` 承接），不寄存 |

**三拍分段**（边3 held 寄存割断 + §11B 发送队列寄存割断；屏障 =
held 寄存器与 req_sched 2-slot 队列，均为既有/新增状态、无组合越段）：

```text
形成段（本拍 cycle-0 组合 + cycle-1 捕获）：
    q head(寄存) → asm 视图(组合) → fresh 判定(组合) → held 快照捕获(拍末)
仲裁段（次拍 cycle-0 组合）：
    held Q → tck dest_ok(组合) → arb grant(组合) → §11A mux(组合)
    fire_consume 拍末回授 asm/chd/tck（cycle-1 提交）；grant = 内部 fire commit
    + §11A 载荷（含 LoadPtrUpdate 组）push 入 §11B 队列（cycle-1 捕获）
发送段（再次拍 cycle-0 组合）：
    req_sched front(寄存) → o_mem_req_*/o_load_ptr_update_*（同拍原子发出；
    o_mem_req_valid = front && i_shared_mem_ready）
```

时序性质：
- **链首 +2 拍**：fresh candidate 形成拍 → grant 次拍 → issue 再次拍
  （边3 +1 与发送段 +1；相对 golden 形成-拍-fire 的合计相移）；
- **连发节奏不变**：grant 连续 1/拍（边3 replacement 链）且 issue 连续
  1/拍（§11B 2-slot 深度保证 ready=1 稳态不降速）；
- **held/req sched 快照一致性不变量**：held valid 时 asm 视图 == held
  内容（context 至 fire 前不推进，F-113）；§11B front 在 pop 前字段不变
  → 端口 payload 与获选 candidate 恒一致（sva）；
- **端口原子性原样保留**：issue 拍 `o_mem_req_valid=1` ⇒ request 与
  `LoadPtrUpdate` 同拍发出（SRC-01 sec 13/14.1 时序图口径不变；
  spec sec 13「grant 拍端口即发」为 **GAP-07 偏差**，A-014）；
- **golden 等价口径**：逐笔 fire/issue 元数据等价 + 链首相移
  （+2 拍/链首；TEST_PLAN §0.4/T-066/T-070 已随更新）。

**反压表现**（无独立反压状态机）：`destination_ok=0` / `source_ok=0`
使 eligibility=0；`shared_mem_ready=0` 由 §11B 队列承接（front 保持、
不 pop；cnt 到 2 → `issue_room=0` → grant 冻结）；`register_ready=0`
关断 C issue——任一情形当拍无 `fire_consume` → held/context/queue
head/C FIFO head/req_sched front 经 `assign(when=)` 条件保持（SEQ
§8–§11 的保持分支）；输入侧状态电平不锁存（PORT_LIST §5.5）。

## 4. 寄存器推断规则（逐模块清单）

统一规则：`domain.signal(width=W, reset_value=..., name=f"{prefix}_*")`
在 cycle 0 声明并读取；cycle 1 写回 → 1 DFF。向量状态用
`shape=[N]`（PRC-01 §3.5）。`reset_value` 全部 0（含指针/计数；
`rr_cursor` reset=A=0 天然满足；A-010）。条件保持全部写成
`sig.assign(sig_next, when=cond)` 或「不写回=保持」的分支结构——
Step 6 对每个信号给出唯一赋值点。

| 模块 | 状态（→ `domain.signal`） | cycle-0 组合输出 | cycle-1 提交条件 |
| :--- | :--- | :--- | :--- |
| `config_regs` | 2×配置 FIFO 存储/head/tail/cnt；`cfg` 配置寄存组（含派生量 rg_len/n_hw2/k_step 等） | `o_*_cfg_ready`、pair_ok、start、cfg 字段 | accept 入队；start 时 pop+装载 cfg |
| `walker` | active、walk_seq、m_idx、cnt_n_inner、k_local、n_base、n_len、k_base、k_count | token 全字段（含 fv_a/b/c、tr、last） | start 装载 / advance transition 更新 |
| `rdgen` | rd_id[4]（`shape=[4]`） | 4 lane enq payload + c_enq payload + end strobes（payload 为组合） | start 清零 / token 拍按 needs 递增 |
| `rd_queue` ×4 | entries 数组（`shape=[depth]` 拍平 entry 各字段）、head/tail/cnt；写入 ≤2/拍（RD+END 双写口，SEQ §7） | head 全字段 + head1 全字段（第二组合读口，asm 次态视图用）、cnt（never-full 供 sva） | pop（asm）、push（rdgen） |
| `assembler_a` | emit{valid,inst,rdgen_id,src,cur}、end_v/end_inst | 视图（1 block + 标量）、pop strobe、context 空 | fire 推进 cur / 退役；emit 空&head RD 时装载 |
| `assembler_b` | coll、emit{pair,half}、end_v/end_inst | 视图、pop strobe | §8.3 装载/完成/推进规则 |
| `assembler_amx` | run(4 key 槽)、emit(4 key 副本+rg)、end_v/end_inst | 视图（4 tile 展开）| run append/闭合、closed→emit 移交、rg 推进 |
| `assembler_bmx` | win[2]（srcs[32] + 键寄存组）、pool 指针(coll/drain)、end_v/end_inst | 视图（4 block 展开）、pop strobe | append/complete/open/fire 释放 |
| `cand_holder` ×4 | held{valid,inst,rd_mem_id,seq,planned_base,planned_advance}、cand_seq、lane_inst | candidate 标量（valid/键/planned）；**present=held Q（仲裁快照，边3 严格流水：fresh 不旁路，拍末捕获）** | SEQ §9 统一规则：`held' = formable(view(ctx')) ? scalars : INVALID`；seq 计数/inst 清零（D-005） |
| `tag_checker` | load_ptr[4]、grp[4]{open,base,cnt}（`shape=[4]` 小向量） | `o_load_range_query_*`（由 held 派生）、dest_ok、dest_base、load_ptr、load_ptr_post、`o_load_ptr_update_*` | fire 且 advance>0：load_ptr/grp 装载 + `LoadPtrUpdate` 输出；group_final fire：grp.open 清零 |
| `arbiter` | rr_cursor | fire、grant_lane、fire_consume[4]（**纯控制**；eligibility 含 `issue_room`；payload 组装 = 顶层 §11A mux → §11B 队列，A-014） | fire 时 rr_cursor←grant+1 |
| `req_sched` | 2-slot 发送队列（payload+update 全字段副本 ≈2.3Kb×2）、cnt、pr/pw | `o_mem_req_*`/`o_load_ptr_update_*`（front 直出，issue 拍）、issue_room、rqp_empty | push=fire（grant 拍末）；pop=front&&mem_ready（issue 拍） |
| `c_path` | C FIFO 数组/ptr/cnt | `o_reg_req_*`（head 直出）、valid | fire pop / rdgen push |
| `lfsm_top` | —（无状态） | `o_walk_stall`(tie 0)、`o_lfsm_idle`（children 空态 **AND**，§16 F-120/CYCLE §13）+ 请求 payload 组合 mux（Step 6 §11A） | — |

**寄存器量级估算**（信息量，供 Step 9 核对）：cfg ≈ 150b；walker ≈
45b；rdgen 48b；四路 Queue ≈ 16×55+8×62+128×56+4×75 ≈ 8.3Kb；
assembler context ≈ A 55b + B 140b + AMX 400b + BMX 2×(32×32+40) ≈
2.8Kb；held ≈ 4×46b；tck ≈ 4×24b；req_sched ≈ 2×2.3Kb（A-014）；
C FIFO ≈ 8×60b。全部为小并行
寄存器组，无大容量单端口结构（数据通路只存 metadata，PORT_LIST §10）。

## 5. 存储原语选型（A-007 + A-002 结论 2 定稿）

**决策（已定稿）**：全部队列/FIFO/寄存器组使用 `domain.signal()` 数组
+ head/tail pointer；**不使用** `m.fifo` / `m.rv_queue` / `m.sync_mem`
原语（A-007：仓库内暂无 `m.fifo` 的 V6 用户，其 ready/valid 相位与本
设计「寄存 head 直读 + 拍末入队 + 无同拍 bypass」契约未验证；若改用
须 gate-first）。无 CDC（单时钟域）。

**DataBlock 池定稿**（A-002 结论 2 授权的 Step 4-6 落点）：物理块池 =
**0**。DataBlock 为 context 的组合展开视图（D-001），逐 lane context
槽位定稿：

| lane | collect 槽 | emit 槽 | block 游标 | 视图宽度 |
| :--- | :--- | :--- | :--- | :--- |
| A | —（单 owner 直入 emit） | 1 owner | cur 0..15 | 1 block |
| B | 1 owner | 1 pair（或 single） | half 0..1 | 1 block |
| AMX | 4 key | 4 key 副本 | rg ∈{0,4} | 4 tile |
| BMX | 窗口槽 1（≤32 src） | 窗口槽 2（≤32 src，完成态） | —（整窗一笔） | 4 block |

可见块数函数（与 golden `same_inst_count` 逐拍等价，SEQ §9/§14.3）：
`A: emit?16−cur:(head?16:0)`；`B: emit?2−half:(完成?2:0)`；
`AMX: emit?8−rg:(闭合/移交?8:0)`；`BMX: 完成槽?4:0`。
form ⟺ `visible ≥ FULL_COUNT`（UU 下 A/B 退化为 `visible≥1`）。
在途积压全部由 **RD Queue + held candidate + BMX 窗口池 + req_sched
发送队列（2-slot，A-014）** 承接
（A-002 结论 3 + A-014 出口段），never-full sva 受力点：RDQ(A16/B128/AMX8/BMX4)、
C FIFO(8)、BMX 池(2)、配置 FIFO(2×2)、req_sched(2，never-overflow)。

## 6. 子模块 `inputs`/`outs` 键映射（Step 6 逐键冻结的母表）

键名约定：snake_case；父 dict 键与子 `submodule_input()` 键完全一致；
lane 向量用 `shape=[4]`（外部端口）或在父模块内按 lane 下标取用。
位宽以 PORT_LIST §3/§4 为准，此处只标语义。

```text
config_regs  in : walk_cfg_* / lfsm_cfg_*（顶层端口组）
             out: cfg_ready{w,l}, start, cfg_*（m_mode/m_slice/n_hw/k_groups/
                  span/base_k/kpt/rg_len/n_hw2/各 base 地址/mx_en/inst_id）
walker       in : start, cfg 几何字段
             out: tok_valid, tok_*（含 fv_a/b/c、n_blk_*、tr、last）
rdgen        in : tok_*、cfg 地址/几何字段
             out: enq[4]{valid,payload…}, end[4], c_enq{valid,payload}
rd_queue     in : enq_rd{valid,payload}, enq_end{valid,inst_id}, pop
             out: head_valid, head_is_end, head_payload…,
                  head1_valid, head1_is_end, head1_payload…, cnt
assembler_*  in : head_*（队列）、fire_consume（来自 arbiter）、
                  dest_base（writes 展开用，来自 tag_checker）
             out: view{formable,inst,rd_mem_id,visible,blocks 元数据视图,
                  new_owner_cnt,planned_advance,group_final,is_last,
                  load/valid/pad bytes, wr 视图}, pop, ctx_empty
cand_holder  in : asm view 标量（含 view_next）、load_ptr、load_ptr_post、fire_consume
             out: present{cand_valid,inst,rd_mem_id,seq,planned_base,planned_advance}
tag_checker  in : held[4] 标量、view_group_final[4]、i_load_range_idle[4]、
                  fire + grant_lane
             out: query[4]、dest_ok[4]、dest_base[4]、load_ptr[4]、load_ptr_post[4]、
                  load_ptr_update{valid,lane,old,new,advance}
arbiter      in : chd[4] 仲裁键（valid/inst/rd_mem_id）、dest_ok[4]、issue_room、
                  i_mem_source_ok[4]     # 纯控制，不接触 payload，不采样 mem_ready（A-014）
             out: fire、grant_lane、fire_consume[4]
req_sched    in : §11A req_mux 全组（payload+update）、i_shared_mem_ready（issue 拍采样）
             out: o_mem_req_* 全组、o_load_ptr_update_* 全组、issue_room、rqp_empty
（顶层 §11A mux  # grant 拍 cycle-0 组合：asm 元数据视图[4] + chd present 标量
              + tck dest_base/tag_cnt/update 组 + arb fire/grant_lane → req_mux
              → req_sched push 输入；无状态）
c_path       in : c_enq、i_register_ready
             out: reg_req_*（head）、c_empty
lfsm_top     收集：PORT_LIST §4 全部端口；o_lfsm_idle = 各 child 空态 AND
```

## 7. prefix 级联与命名

```text
lfsm                # 顶层端口：lfsm_i_walk_cfg_valid …（PORT_LIST §4 key）
├─ lfsm_cfg_*       # config_regs 内部寄存器/（独立模式端口）
├─ lfsm_wlk_*
├─ lfsm_rdg_*
├─ lfsm_q_{a,amx,b,bmx}_*
├─ lfsm_asm_{a,amx,b,bmx}_*
├─ lfsm_chd_{a,amx,b,bmx}_*
├─ lfsm_tck_*
├─ lfsm_arb_*
├─ lfsm_rqp_*
└─ lfsm_c_*
```

`__pycircuit_name__` 与函数名一致；层次化发射
（`compile_cycle_aware(eager=True, hierarchical=True)`）每个
`domain.call()` 边界为一个 `func.func` + `pyc.instance`（PRC-01 §7.6）。

## 8. 风险与检查项（带入 Step 6/9）

1. **组合链深度（总体）**：边3 严格流水（held 寄存割断）把旧单拍链
   拆为三段（§3「三拍分段」），时序压力较同拍 bypass 版本下降
   （该决策动机之一，2026-10-14 用户决策）。两段各自的 deepest
   路径、契约约束与再切分选项逐项盘于 **§8.1**；若时序评估仍
   不达标，按 §8.1 选项回 Step 5 重议（走 gate-first，不做
   backend-only 修补）。
   - 更正（2026-10-14）：早期版本曾把「BMX 32 槽展开」记在形成段，
     不准确——emit-on-demand 下**元数据视图（src/wr 数组）每拍从
     ctx 寄存器组合重算、直接喂 §11A 顶 mux**，属**仲裁段**路径；
     形成段只消费 view 的轻标量（formable/键/advance）。见 §8.1。
2. **B lane 128 深队列 head/head1 读取**：两路 128:1 寄存器 mux（head
   + head1 第二组合读口，供 asm 次态视图）；为已知代价（A-002 深度
   决策的物理对应），MLIR/C++ 仿真层面接受。
3. **自动周期平衡审计**：Step 9 检查发射 MLIR 中无意外 `pyc.reg`
   延迟链（§1 末条）。
4. **D-xx 决策**（D-001…D-006，SEQ §15）随本文一并进入 Step 7
   TRACEABILITY / ASSUMPTIONS v4 复查。

### 8.1 逻辑深度风险点与再切分选项（2026-10-14，随边3 决策盘点）

**段内路径分解**（门级量级粗估，ASIC 口径；深度 = 起点寄存器到终点
端口/写端的组合级数）：

| 环 | 路径（寄存器起 → 终） | 主要逻辑 | 量级 | 评价 |
| :--- | :--- | :--- | :--- | :--- |
| 形成段 | `q head/head1` 寄存 → chd 捕获写端 | head/head1 读出（B 128:1 ×2 口）→ asm view 标量（match/close/complete 计数比较等）→ fresh/repl 捕获使能 | ≈10–15 级 | 非 fire 环：只需拍末前稳定，**非全局关键路径** |
| 仲裁段·决策环 | `held Q/ctx` 寄存 → grant（§11B 入队使能） | tck planned mux（1–2）→ **`o_load_range_query` 出模块 → 外部 Buf/RAM 组合算 idle** → `i_load_range_idle` → dest_ok（2–3）→ 4 路 18b argmin 比较树（6–8）→ RR 扫描（3–4）→ grant | 内部 ≈15–20 级 **+ 外部未知** | **R1（头号风险）：A-004 跨模块组合查询环**（A-014 后 eligibility 用 `issue_room`，mem_ready 移至队列出口——对 R1 无缓解，环仍同拍） |
| 仲裁段·数据环 | `ctx/held` 寄存 → §11B 队列写端 | asm 元数据视图重组算：**BMX 32-slot mem-pad 地址 + ≤32 writes 的 dest_base 加法**（AMX ≈16 fragment 同类，B/A 浅）→ §11A 4:1 宽 mux → 队列 slot 写端 | ≈15–25 级 | **R2：BMX 最深**；终点为队列写端而非端口（A-014 收益：输出 pad 路径移出数据环） |
| 发送段 | `req_sched` 队列寄存 → 端口 | front 直出（≈0–2 级） | 极浅 | **A-014 新增**；端口 = 纯寄存出口，彻底解除端口 deadline 压力 |
| 面积项 | — | §11A 4:1×（32b×32 src + 27b×32 wr）宽度；B 128 深双读口 | 深度小 | R4/R5：A-006 拒绝 payload 晚一拍后，宽 mux 属保留成本（面积/布线，非深度） |

**R1 处置（不打拍、改约束）**：`query→idle→grant→fire` 是规格强制的
同拍环（A-004 相位契约 + eligibility 每拍重算 R-34；fire 单拍原子
A-006），**不可在 LFSM 内部切分**。处置：
- PORT_LIST §5.2 相位契约之上追加**集成时序预算**（对 Buf/RAM 实现方）：
  per-lane `range_idle` 建议预归约/预译码（把 ≤32 tag 的 AND-reduce
  用浅逻辑实现）、`fresh_idle_guard` 以寄存查看表实现；
- Step 10 sign-off 时序表把「query→idle→grant→fire」列为**关键路径行**；
- 集成 TB 反应式 stub（REF-04 口径）实现深度与该预算对齐。

**进一步拆分选项（均未采纳；待 Step 9 时序评估触发后再定）**：

| 选项 | 内容 | 收益 | 代价/约束 | 状态 |
| :--- | :--- | :--- | :--- | :--- |
| **P1 fire 前付运快照** | fresh/repl 捕获拍把该 candidate 的**全部付运字段**（src ranges、writes、三账目、flags）与当拍 `dest_base` 一起算好写入 per-lance **fire-side 快照寄存**（≈2.2Kb×4） | 数据环整体移出 grant 关键路径；形成段复用同一拍已算视图，无新增组合深度 | ≈8.8Kb 寄存器 + chd→asm 捕获使能新连线；**修订 D-001**；wr 展开改用捕获拍 dest_base | **降级为可选**：A-014 发送段已把端口 deadline 解除、数据环终点改为队列写端——P1 仅在 Step 9 时序评估显示"数据环→队列写端"仍超标时再启用 |
| P1-lite | 只快照最重数组字段（BMX/AMX src/wr），标量保持组合 | R2 进一步缓解 | ≈4–5Kb | 同上（备选） |
| P2 payload/控制 pipe | grant 拍只发控制，payload 打拍次拍 | 决策/数据/端口三环全部解耦 | … | **已采纳（A-014，2026-10-14 用户决策，推翻 A-006）**——落地为 §11B `req_sched` 2-slot 发送队列（含 LoadPtrUpdate 同组、issue 拍同拍原子发出、`issue_room` 反压回仲裁侧）；GAP-07 规格 deviation 登记 |

若采纳 P1/P1-lite 的落点：CYCLE §5–§8（asm 增 fire_copy 寄存组 +
capture 使能输入）、§9（chd 输出 capture 使能）、§13（§11A mux 源改
fire_copy）、SEQ §14.3 补「付运快照与组合视图在 held 期间逐拍同值
（context 冻结）」等价性条款；登记 **D-007** 并同步 TRACEABILITY
（新 GAP 或并入 GAP-06 备注）。R1 不受 P1 影响（决策环仍在）——
sign-off 时序表必须两环分开评估。
```
