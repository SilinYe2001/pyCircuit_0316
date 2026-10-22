# LFSM (4EU UU mode) ALGORITHM_SEQUENTIAL

> Step 4 交付物（依据 `docs/pycircuit_implementation_method.md` Step 4：
> 「Sequential (imperative) behavior, function-oriented decomposition」）。
> 把 LFSM 行为描述为**命令式程序**：每拍一个 `lfsm_cycle()` 主例程调用
> 一组职责单一的子程序；只有概念数据结构与显式状态变量，**不**承诺
> 硬件模块边界、**不**出现 `domain.next()`/周期标记（那是 Step 5/6 的事）。
> 建立日期：2026-10-13。
> 需求编号（SRC-xx/R-xx）见 `REQUIREMENT_SOURCES.md`；决策编号
> （A-xxx）见 `ASSUMPTIONS.md`；功能编号（F-xxx）见
> `FEATURE_LIST.md`；端口/位宽以 `PORT_LIST.md` §3/§4 为准。
> 范围：4EU UU mode（Shared MEM baseline）+ UU C-only 路径。
>
> 本文伪码是 golden（REF-01…REF-05）的**精确功能转写**，凡与 golden
> 表示法不同之处（set 去重→计数器条件、突发块池→emit-on-demand）
> 都在 §14「表示差异与等价性论证」登记；微架构新决策记为 D-xx
> （§15，Step 7 时按流程提升进 `ASSUMPTIONS.md` / `TRACEABILITY.md`）。

## 0. 记法约定

- `## 状态` 注释引出**显式状态变量**（跨拍保持；Step 5 映射为
  `domain.signal()`）。其余变量都是当拍求值的临时量。
- `lane ∈ {A=0, AMX=1, B=2, BMX=3}`（PORT_LIST §4 约定，与 RR 扫描序
  一致）；`LANES = (A, AMX, B, BMX)`。
- `required_lanes(mx_en) = mx_en ? (A,AMX,B,BMX) : (A,B)`（F-024）。
- 配置派生量：`k_step = m_mode ? 4 : 8`；
  `span = mx_mode_en ? mx_bytes_per_k0 : 0`（∈{1,2,4}）；
  `base_k = 4/span`（∈{4,2,1}，BMX 窗口 K 行数）；
  `keys_per_tile = 4/span`（AMX 每 32B tile 的 key chunk 数）；
  `n_hw2 = n_hw_count + (n_hw_count & 1)`（BMX 行 stride，SRC-04 sec 7）；
  `rg_len = ceil(k_groups*span/4)*32`（AMX row-group 字节数，
  SRC-04 sec 7；ceil/4 = `(x+3)>>2`，加法级）。
- `FULL_COUNT = {A:1, AMX:4, B:1, BMX:4}`（`= LOAD_BUS_BYTES(128) /
  block_bytes`，block_bytes = {A:128, B:128, AMX:32, BMX:32}，
  SRC-01 sec 10，R-17）。
- `DEPTH = {A:8, AMX:32, B:32, BMX:256}`（静态参数，全为 2 幂；
  ring 运算 `(base+i) % DEPTH` 退化为 `& (DEPTH-1)`）。
- 数据结构写字段即全部字段；`≪enqueue≫`/`≪pop≫` 表示对概念队列的
  原子操作（Step 5 前不指定实现）。

## 1. 概念数据结构

### 1.1 配置

```text
WalkCfgFields      { inst_id, m_mode, m_slice_count, n_hw_count, n_step(恒1), k_groups }
LfsmCfgFields      { inst_id, eu_mode(恒0/4EU), data_type, mx_mode_en, mx_bytes_per_k0,
                     n_hw_count, a_base, a_mx_base, b_base, b_mx_base, l0c_base,
                     a_limit, a_mx_limit, b_limit, b_mx_limit   # limit 仅供 TB/sva 越界断言（F-023），不进功能路径
                     }
InstrConfig        = WalkCfgFields + LfsmCfgFields + 派生量(k_step, span, base_k,
                     keys_per_tile, n_hw2, rg_len, a_bytes_per_key=2048, b_bytes_per_key=128)
```

### 1.2 流水对象

```text
WalkToken   { inst_id, m_idx, n_idx, k_idx, walk_seq, first, last,
              n_blk_base, n_blk_len,              # 当前 N block（供 BMX entry 注解）
              fv_a, fv_b, fv_c }                  # 首访条件（A-001，见 §3.2）

RdEntry(lane) {                                    # RD Queue entry（≈REF-05 RdRequest + D-002 注解）
  公共:  is_end=0, inst_id, rdgen_id, rd_id, src_addr
  A:     m_idx, k_idx
  B:     n_idx, k_idx, n_tail_single               # D-002 注解：奇数 N 尾单 owner
  AMX:   m_idx, k_idx, span, k_groups, is_k_tail   # D-002 注解
  BMX:   n_idx, k_idx, span, k_groups, n_hw2, n_blk_base, n_blk_len   # D-002 注解
}
EndEntry    { is_end=1, inst_id }                  # LaneLoadEnd（F-024）
QueueEntry  = RdEntry | EndEntry

CEntry      { inst_id, rdgen_id, m_idx, n_idx, src_addr }   # C FIFO entry（F-025）

BlockView(lane) {                                  # 一个 DataBlock 的按需展开视图（D-001）
  src_ranges[] : (addr, len) ≤ 8 项                # 含 mem-pad fragment；len>0
  valid_bytes, pad_bytes                           # valid 含 mem-pad（MEM-read 口径）
}

CandView(lane) {                                   # cand_holder/arbiter 候选视图（D-001）
  formable                                         # 可见块数 ≥ FULL_COUNT（§5.5 精确函数）
  inst_id, rd_mem_id                               # 优先键（rd_mem_id=首 block rdgen_id）
  n_blocks                                         # = FULL_COUNT（UU 恒成立，§5.5）
  blocks[FULL_COUNT] : BlockView                   # 按需展开，不落池
  new_owner_cnt, planned_advance                   # = Σ新 owner span
  group_final                                      # 本候选完成后 group 全部 owner 打包完
  is_last                                          # fire 时有效：instruction 末笔（§8.4）
  load_bytes, valid_bytes, pad_bytes               # Σ blocks；UU 下 load≡128、partial≡0（D-003）
  wr_hint                                          # 供 writes 展开的位置游标（cursor/half/rg/window）
}

GroupBind   { open, base, cnt }                    # 每 lane 当前 allocation group（D-004：UU ≤1 open）
LoadPtrUpdate { lane, old_ptr, new_ptr, advance }  # SRC-01 sec 13
```

## 2. 显式状态变量（全局清单）

```text
## 配置（config_regs 组）
cfg_fifo_walk[CFG_FIFO_DEPTH=2], cfg_fifo_lfsm[2]   # 两条配置 FIFO + head/tail
cfg        : InstrConfig                            # 当前 active instruction 配置寄存

## walker（walker 组）
wlk_active, walk_seq(≤8191), m_idx, cnt_n_inner, k_local,
n_base, n_len, k_base, k_count                      # loop 几何现场维护（A-005 v3）

## rdgen（rdgen 组）
rd_id[4]                                            # 每 lane lane-local owner 序号（instruction 开始清零）

## 四路 RD Queue（rd_queue 组 ×4）
q_entries[lane][RDQ_DEPTH[lane]], q_head, q_tail, q_cnt
                                                    # DEPTH = {A:16, AMX:8, B:128, BMX:4}（A-002/A-011）

## assembler context（assembler 组 ×4，几何各异，D-001 emit-on-demand）
A:   emit{valid, inst, rdgen_id, src, cur}                                       # cur∈0..15
B:   coll{valid, inst, rdgen_id, src, n, k} ; emit{valid, inst, rdgen_id,
        src0, src1, single, half}                                                # half∈{0,1}
AMX: run{cnt≤4, inst, span, kgs, keys[4].{src,rdgen_id}, sum≤4, closed, m} ;
     emit{valid, inst, rdgen_id, cnt, span, rg_len, srcs[4], rg}                 # rg∈{0,4}
BMX: win[2].{valid, complete, inst, rdgen0, n_base, n_len, rows, span, n_hw2,
        kw_base, cnt, expected, srcs[32]} ; coll, drain                          # 池=2（A-002）+ 收集/drain 指针
每 lane 公共: end_v, end_inst                                                   # 最近消费的 LaneLoadEnd（valid + inst_id；SEQ §8.6）

## cand_holder（cand_holder 组 ×4，同构；对应规格 BandwidthPacker 的持有职能）
held[4] { valid, inst_id, rd_mem_id, seq, planned_base, planned_advance }        # 每 lane 恰好 1 个（F-073）
cand_seq[4], lane_inst[4]                                                        # seq 计数与 per-inst 清零（D-005）

## tag_checker（tag_checker 组，对应规格 DestinationAllocator）
load_ptr[4], grp[4]:GroupBind

## arbiter（arbiter 组）
rr_cursor                                                                          # reset=A

## req_sched（req_sched 组，A-014 发送队列）
rq[2] : {payload 全字段 + LoadPtrUpdate 组}, rq_cnt(0..2), rq_pr, rq_pw   # 2-slot 发送 FIFO

## C 路径（c_path 组）
c_fifo[C_FIFO_DEPTH=8] : CEntry, c_head, c_tail, c_cnt
```

## 3. 主例程

```python
def lfsm_cycle(inputs, S):                  # S = §2 全部显式状态
    # ── evaluate 阶段：只读 cycle-start 状态，形成全部当拍决策（R-34/F-113）
    start   = cfg_eval(inputs, S)            # 配对判定（不 pop）
    tok     = walk_token(S)                  # 组合 token（S.wlk_active 时有效）
    rdg     = rdg_eval(tok, S)               # 首访判定 + entry 构造（不入队）
    qv      = {l: q_head_view(l, S) for l in LANES}      # cycle-start head
    av      = {l: asm_view(l, qv[l], S) for l in LANES}  # emit-on-demand 展开
    cv      = {l: chd_eval(l, av[l], S) for l in LANES} # 仲裁仅见 held 快照（边3 严格流水；fresh 拍末入 held）
    dest    = tck_eval(cv, inputs, S)        # query + destination_ok
    grant   = arb_eval(cv, dest, rqp, inputs, S)  # eligibility(issue_room) + 优先键 + RR
    rqp     = rqp_eval(inputs, S)                  # 发送队列 front/pop/issue_room（A-014）
    c_issue = c_eval(inputs, S)              # C FIFO head + register_ready

    # ── commit 阶段：原子提交全部状态更新（无 partial batch，R-07/F-113）
    if grant.fire:        fire_commit(grant.lane, cv, S)     # §10：内部 commit 原子；端口组经发送队列在 issue 拍发出（A-014）
    tck_commit(grant, cv, S)                                 # load_ptr/group/LoadPtrUpdate
    chd_commit(grant, cv, av, S)                            # consume/replacement/seq
    asm_commit(grant, qv, S)                                 # collect/emit/cursor/end tag
    q_commit(rdg, asm_pop_strobes, S)                        # pop ≤1/lane + 入队(RD/END)
    rdg_commit(tok, start, S)                                # rd_id 递增/instruction 清零
    walk_commit(tok, start, S)                               # counter/几何/start/done
    cfg_commit(inputs, start, S)                             # FIFO 握手/pop/配置装载
    rqp_commit(grant, rqp, S)                                # §11B：grant 拍 push（fire 载荷）/ issue 拍 pop
    c_commit(c_issue, rdg, S)
```

优先级总线（F-111/R-27 映射）：reset > 保持已有 valid/payload（held、
Queue head、context 未 fire 不变）> 处理本 lane 最老 head/owner
（pop/collect/cursor 推进）> 产生新工作（enqueue/新 candidate）。
各子程序内部的优先级在 §4–§11 逐项给出。

## 4. 子程序：配置配对与启动（CFG，F-001/F-002/F-012）

```python
def cfg_eval(inp, S):
    accept_w = inp.walk_cfg_valid and cfg_ready(S.cfg_fifo_walk)   # ready = 非满
    accept_l = inp.lfsm_cfg_valid and cfg_ready(S.cfg_fifo_lfsm)
    pair_ok  = (nonempty(S.cfg_fifo_walk) and nonempty(S.cfg_fifo_lfsm)
                and head(S.cfg_fifo_walk).inst_id == head(S.cfg_fifo_lfsm).inst_id)
                # inst_id 不等 = 协议错误断言（A-005.2，sva）
    start    = pair_ok and not S.wlk_active      # golden：walker 空闲才启动（F-012）
    return (accept_w, accept_l, pair_ok, start)

def cfg_commit(inp, ev, S):
    if ev.accept_w: push(S.cfg_fifo_walk, inp.walk_cfg)      # 拍末生效
    if ev.accept_l: push(S.cfg_fifo_lfsm, inp.lfsm_cfg)
    if ev.start:
        S.cfg = derive_config(pop(S.cfg_fifo_walk), pop(S.cfg_fifo_lfsm))
        # derive：k_step/span/base_k/keys_per_tile/n_hw2/rg_len 一次算好（§0，加法级）
        # limit 字段入寄存但仅供 sva；结构断言：k_groups≤32、m_slice≤2、
        # span∈{1,2,4}（MX 时）、n_step==1、eu_mode==0（F-002）
```

背靠背（F-012/R-26）：instruction *i* 的 last token commit 拍 walker 转
空闲；次拍 evaluate 见 `pair_ok` 即 start；再下一拍首 token 输出——与
golden `start_instruction` 分支逐拍一致（两 instruction 可同时处于
不同流水阶段：walker 已在走 *i+1*，lane 仍在 drain *i*）。lane 侧
instruction 切换由 entry 携带的 `inst_id` 与 D-002 注解驱动，不读
`S.cfg`（关键：assemblers 使用 entry 注解而非当前配置寄存器，见 §14.2）。

## 5. 子程序：walker（WLK，F-010/F-011/F-012）

### 5.1 token 生成（组合）

```python
def walk_token(S):
    if not S.wlk_active: return INVALID
    n_idx = S.n_base + S.cnt_n_inner
    k_idx = S.k_base + S.k_local
    tr    = next_transition(S)               # §5.3 优先级表
    return WalkToken(
        inst_id=S.cfg.inst_id, m_idx=S.m_idx, n_idx=n_idx, k_idx=k_idx,
        walk_seq=S.walk_seq, first=(S.walk_seq==0), last=(tr==DONE),
        n_blk_base=S.n_base, n_blk_len=S.n_len,
        fv_a=(S.n_base==0 and S.cnt_n_inner==0),     # A/AMX 新 key（A-001）
        fv_b=(S.m_idx==0),                            # B/BMX 新 key（A-001）
        fv_c=(S.k_base==0 and S.k_local==0))          # C 新 key（A-001）
```

### 5.2 loop 几何规则（加法级，A-005 v3）

```python
n_len_rule(rem)  = 4 if rem in (9, 10) else min(8, rem)   # 与 build_n_blocks 逐项等价
k_count_rule(kb) = min(k_step, S.cfg.k_groups - kb)       # k_step = m_mode?4:8
last_block       = (S.n_base + S.n_len == S.cfg.n_hw_count)
last_outer       = (S.k_base + S.k_count == S.cfg.k_groups)
```

### 5.3 transition 与 advance

```python
def next_transition(S):                        # REF-01 _next_transition 逐写
    if S.cnt_n_inner + 1 < S.n_len:    return N_INNER    # n_span=1
    if S.k_local + 1 < S.k_count:      return K_LOCAL
    if S.m_idx + 1 < S.cfg.m_slice_count: return M_SLICE
    if not last_block(S):              return N_OUTER
    if not last_outer(S):              return K_OUTER
    return DONE

def walk_commit(tok, start, S):
    if start:
        (S.wlk_active, S.walk_seq, S.m_idx, S.cnt_n_inner, S.k_local,
         S.n_base, S.k_base) = (1, 0, 0, 0, 0, 0, 0)
        S.n_len   = n_len_rule(S.cfg.n_hw_count)
        S.k_count = k_count_rule(0)
        return
    if not tok.valid: return
    advance = True                              # stall 内部 tie-0（A-009）；
                                                # stall 分支保持全部 counter/walk_seq（F-011 语义完整）
    S.walk_seq += 1
    case tok.tr:
      N_INNER: S.cnt_n_inner += 1
      K_LOCAL: S.cnt_n_inner, S.k_local = 0, S.k_local+1
      M_SLICE: S.m_idx, S.k_local, S.cnt_n_inner = S.m_idx+1, 0, 0
      N_OUTER: nb = S.n_base + S.n_len
               S.n_base, S.n_len = nb, n_len_rule(S.cfg.n_hw_count - nb)
               S.m_idx, S.k_local, S.cnt_n_inner = 0, 0, 0
      K_OUTER: kb = S.k_base + S.k_count
               S.k_base, S.k_count = kb, k_count_rule(kb)
               S.n_base, S.n_len = 0, n_len_rule(S.cfg.n_hw_count)
               S.m_idx, S.k_local, S.cnt_n_inner = 0, 0, 0
      DONE:    S.wlk_active = 0                  # done = advance && last（F-012）
```

不变量（对拍锚点）：token 流 = REF-01 `MknWalkFSM` 逐拍；
`rdgen_id = walk_seq + 1`，per-instruction 从 1 起（R-08）。

## 6. 子程序：rdgen（RDG，F-020…F-025）

```python
def rdg_eval(tok, S):                     # 只构造 entry，不入队（commit 才入队）
    if not tok.valid: return EMPTY
    rid = tok.walk_seq + 1                # rdgen_id（R-08；reuse token 占号）
    needs = {}
    if tok.fv_a:                          # A/AMX data key = (inst,m,k)
        needs[A] = RdEntryA(inst, rid, rd_id=S.rd_id[A],
                            src = a_base + (m*k_groups + k)*2048)
        if mx_en: needs[AMX] = RdEntryAMX(inst, rid, rd_id=S.rd_id[AMX],
                            src = a_mx_base + m*8*rg_len + k*8*span,
                            span=span, k_groups=k_groups,
                            is_k_tail=(k == k_groups-1))
    if tok.fv_b:                          # B/BMX data key = (inst,k,n)
        needs[B] = RdEntryB(inst, rid, rd_id=S.rd_id[B],
                            src = b_base + (k*n_hw2 + n)*128,          # n_hw2 pair 量化 stride（F-056 v2）
                            n_tail_single=(n == n_hw-1 and n%2==0))
        if mx_en: needs[BMX] = RdEntryBMX(inst, rid, rd_id=S.rd_id[BMX],
                            src = b_mx_base + (k*n_hw2 + n)*(4*span),
                            span=span, k_groups=k_groups, n_hw2=n_hw2,
                            n_blk_base=tok.n_blk_base, n_blk_len=tok.n_blk_len)
    if tok.fv_c:                          # C data key = (inst,m,n)（R-29）
        c = CEntry(inst, rid, m, n, src = l0c_base + (m*n_hw + n)*16)
    ends = required_lanes(mx_en) if tok.last else ()
    return (needs, c, ends)               # 同 token 全 lane 一次构造（R-07）

def rdg_commit(tok, start, S):
    if start: S.rd_id[*] = 0              # instruction 开始清零（F-021）
    if tok.valid:
        for lane in needs:  S.rd_id[lane] += 1      # 仅成功入队 lane 递增
        # q_commit 把 needs/ends/CEntry 原子追加（同 lane 原子、跨 lane 同拍）
```

地址公式 = SRC-04 sec 7 / REF-02 `_make_rd` 逐项；乘法均为小位宽
（`m*k_groups` 1b×6b、`k*n_hw` 5b×8b、`k*8*span`/`m*8*rg_len` shift-add、
`k*n_hw2` 5b×8b、C 地址 `m*n_hw` 1b×8b），单拍组合可完成，无除法器。
越界（limit）检查 = TB/sva 断言（F-023 决策）。

## 7. 子程序：四路 RD Queue（Q，F-030/F-031/F-032）

```python
def q_head_view(lane, S):                 # cycle-start head（寄存状态直读）
    return S.q_entries[lane][S.q_head] if S.q_cnt[lane] > 0 else EMPTY

def q_commit(rdg, pops, S):
    for l in LANES:
        if pops[l]:                       # ≤1/拍/lane（asm collect/END 消费）
            S.q_head[l] += 1 mod DEPTH; S.q_cnt[l] -= 1
        for e in enqueue_set(rdg, l):     # ≤2/拍/lane：1 RD + 1 LaneLoadEnd
            S.q_entries[l][S.q_tail[l]] = e
            S.q_tail[l] += 1 mod DEPTH; S.q_cnt[l] += 1
        assert S.q_cnt[l] <= RDQ_DEPTH[l] # never-full（F-032/A-002/A-011，sva 落点）
```

规则直译（R-09）：head 为最老 entry；每拍每路 ≤1 个 head 交给
Assembler；仅 head dequeue；反压时 head/payload 保持（无 pop 即不变）；
entry 不得同时处于 Queue 与 Assembler（pop 与 collect 同一 commit）。
**无同拍 bypass**（F-031）：rdgen 入队在拍末 commit，次拍起才出现于
head view。计数不变量 `enqueue−dequeue==size`（R-35）由 TB 断言。

## 8. 子程序：assembler（ASM，F-040/F-041 + 四路几何）

### 8.0 统一骨架（D-001 emit-on-demand）

每 lane 的 context 分**收集侧**（merge 几何槽位）与**展开侧**（emit
槽位 + block 游标）；DataBlock 不设物理池，是 context 的**组合展开
视图**，在 candidate 形成拍按需生成（A-002 结论 2 定稿，见
`ALGORITHM_PIPELINED.md` §5）。每拍骨架：

```python
def asm_view(lane, qh, S):                 # evaluate：产出候选视图 + pop/转移决策
    inc = incoming(lane, qh, S)            # 本拍可完成的 collect/窗口收尾（含 chain：head 直接进视图）
    if emit_active(lane, S):   return view_from_emit(lane, S)
    if inc:                    return view_from_incoming(lane, inc)
    return NOT_FORMABLE

def asm_commit(lane, grant, qh, S):        # commit：保持 > 最老 > 新工作
    # 1) fire：cursor 推进 / emit 退役（cursor 到尾）
    # 2) 未 fire：emit/collect 全保持（F-113 保持清单）
    # 3) collect 转移：head 兼容 → pop+append；完成 → 移交 emit（emit 空闲时）
    # 4) END：head.is_end → pop，装载 end_v/end_inst（各 lane 合法性 sva 见 §8.6）
    # 5) context 不跨 instruction（F-110）：新 inst entry 只在 emit 全空后进
```

`emit_active` 时 head 不得 pop（A/B 例外：B 的 collect 槽与 emit 独立，
可并行收集下一 pair 的首 owner，§8.3；AMX run 槽与 emit 独立，可并行
收集下一 run，§8.4；BMX 收集窗口与完成窗口为池内两槽，§8.5）。

### 8.1 公共规则（F-040/F-041）

- merge 只允许：同 lane、同 instruction、M/N/K 几何连续、地址合法；
  **不跨 instruction**（F-110）。
- 等待规则：未达几何尾/未收 LaneLoadEnd 时，Queue 空/局部 loop 边界/
  下游反压都**不是** padding 条件——保持 context（F-040）。
- padding：只允许几何尾或 LaneLoadEnd drain；A/B/AMX 均无 transport
  padding（B 尾与 AMX K 尾补齐为 mem pad——实存 MEM、随读计 valid）；
  BMX 窗口未覆盖 slot 恒为 transport padding（任意窗口位置）；任何
  padding/mem-pad 不产生 owner/tag/buffer write、不推进 load_ptr
  （F-041）；`valid+padding==block_bytes` 逐 block 成立。

### 8.2 A（F-050）

```text
收集侧：无（单 owner 直接进 emit）。
emit 装载：emit 空 且 head 为 RD →（本拍即可进视图，chain）
展开 view(cur)：满 key 2048B 恒成立（partial M 非法，F-002）→ 16 个
  128B block；默认序 EU_M_HALF_K_HALF 下 block(cur) 的
  (eu,mh,kh) = (cur/4, (cur%4)/2, cur%2)，src = owner.src + cur*128，
  单 range、valid=128、pad=0、无 mem-pad。
  （非默认 a_block_order 本轮不实现：F-050 决策，TRACEABILITY gap。）
cursor：fire 一次 +1；cur==15 fire 后 emit 退役。
new_owner：cur==0 的 candidate（advance=1）；group_final：cur==15。
```

### 8.3 B（F-055/F-056）

```text
collect 槽：1 个 owner（偶数 N4）；emit 槽：完整 pair 或奇尾 single + half 游标。
pair 成员（由 D-002 注解 n_tail_single 判定，不查表）：
  single ⟺ entry.n_tail_single（= n==n_hw-1 且 n 偶；pair 天然不跨 N block，
  因非末 block 长恒偶、边界 base 恒偶——§14.1 论证）。
装载/完成：
  coll 空 & head 为 RD & !head.single → coll ≪pop≫（emit 忙也可收集）
  coll 空 & head.single → 待 emit 空闲：emit=(single, half=0)，≪pop≫
  coll 有 & head 兼容（同 inst、同 k、n==coll.n+1）→ 待 emit 空闲：
    emit=(pair(coll,head), half=0)，coll 清空，≪pop≫
  coll 有 & head 不兼容 → 合法走法不可达（sva；规格为模型错误）
展开 view(half)：pair：两个 range（src_i + half*64, 64），valid=128；
  single：两个 range——owner（src + half*64, 64）+ pair-completion
  mem-pad（src + 128 + half*64, 64；pad slot 实存于该 K 行 `n_hw2−1` 位、
  随真实数据读取并计入 valid（MEM-read 口径）、不产生 owner/tag/buffer
  write），valid=128，pad=0（F-056 v2，B 无 transport padding）。
cursor：fire 一次 half+1；half==1 fire 后 emit 退役。
new_owner：half==0 candidate（advance = single?1:2）；group_final：half==1。
```

### 8.4 AMX（F-060/F-061）

```text
run 槽：≤4 key（同 m、K 连续、Σspan≤4）；emit 槽：已闭合 run 副本 + rg 游标。
收集（与 emit 并行）：
  run 空 & head 为 RD → 开 run（记入 inst/m/span/kgs；sum=span）
  run 开 & head 兼容（同 inst、同 m、k==末 key+1、sum+span≤4）→ append
  闭合条件（append 后判定）：sum==4 或 head.is_k_tail（D-002 注解）
  ── 跨 K-outer 不截断（F-060）：k_idx 为全局序号，连续性天然跨 outer；
     4EU 走法下 run 恒在 k_outer 内闭合（4|k_step），跨 outer 为规格许可的
     未激发行为，§14.1 注记。
移交：closed 且 emit 空闲 → emit=run 副本(rg=0)，run 清空（本拍可 chain 进视图）
展开 view(rg..rg+3)：每 tile = 一个 M8×K4B 32B block：
  chunk j（j<keys_per_tile）：j<cnt → real(key_j.src + r*rg_len, 8*span)
  j≥cnt → mem-pad(key_0.src + j*8*span + r*rg_len, 8*span)   # K 尾实存 pad（F-061）
  tile.valid = 32（mem-pad 计入 valid），tile.pad = 0          # AMX 无 transport padding
  r ∈ {rg, rg+1, rg+2, rg+3}（valid_rgs≡8：满 M slice 恒 8 个 row-group）
cursor：fire 一次 rg+4；rg==4 fire 后 emit 退役。
new_owner：rg==0 candidate（advance=cnt×span）；group_final：rg==4。
```

### 8.5 BMX（F-065/F-066/F-067）

```text
窗口池：2 槽（1 收集 + 1 完成待 drain，A-002）；窗口 = N(块长)×K(base_k 行)
owner slot 网格，4EU 128B 下 blocks_per_window=4、每 block = N2×base_k。
开窗口（head 为 RD 且收集槽空/已开窗口不匹配为新窗口）：
  n_base/n_len ← entry.n_blk_*；kw_base = k_idx & ~(base_k-1)
  rows = min(base_k, entry.k_groups - kw_base)；expected = n_len × rows
收集：append src FIFO（到达序 = 坐标序 = FIFO 位置 j，§14.1 论证）；
  cnt+1；cnt==expected → complete（本拍可 chain 进视图）。
  同窗口匹配（sva）：head 的 (n_blk_base, k_idx&~(base_k-1)) == 窗口键。
展开 view（4 block 同时）block b∈0..3：
  2b ≥ n_len → padding-only block（0 fragment，valid=0, pad=32）
  否则 cell (r,s)，r∈0..base_k-1、s∈{0,1}：
    real ⟺ (2b+s < n_len) 且 (r < rows)；j = r*n_len + 2b + s
    real → frag(srcs[j], 4*span)
    否则 → mem-pad(srcs[2b] + (r*n_hw2 + s)*4*span, 4*span)   # N 对/K 块量化实存 pad（F-067）
fire：整窗口 4 block 一笔 candidate 一次消费（恒满 128B，无 partial）；
  槽位释放；候选的 rd_mem_id = 窗口 rdgen0（窗口首 owner）。
new_owner：全部 cnt 个 owner（advance=cnt×span）；group_final 恒 1（D-004）。
drain：LaneLoadEnd 时收集窗口 cnt==expected（sva；golden force 语义）；
  池满（两槽均占且收集槽又需新窗口）→ 停止 pop，反压由 RD Queue 承接（A-002 结论 3）。
```

### 8.6 LaneLoadEnd 消费条件（F-024/F-110）

| lane | END pop 条件 | pop 时合法性 sva |
| :--- | :--- | :--- |
| A | head.is_end（随时，emit 可仍忙） | — |
| B | head.is_end | coll 必为空（奇尾 single 收集即完成，不会滞留） |
| AMX | head.is_end | run 为空或已 closed（K 尾恒闭合，不会开着） |
| BMX | head.is_end | 收集窗口 cnt==expected（golden force 不报错） |

pop 时装载 `end_v=1, end_inst=head.inst_id`（**tag 式寄存，不清零**——
下一条 END 自然覆盖；b2b 下 instruction *i+1* 的 context 可与 *i* 的
drain 并存，bit 式 `end_seen` 会被错误清零，故用 inst_id 比对）。
`is_last`（fire 时组合计算）：
A：`end_v && v_inst==end_inst && cur==15`；
B：`end_v && v_inst==end_inst && half==1`；
AMX：`end_v && v_inst==end_inst && rg==4`；
BMX：`end_v && 窗口.inst==end_inst && 池内无同 inst 的其它窗口`。
（END 按 FIFO 序位于同 inst 全部 entry 之后：`end_inst==X` ⟹ 队列与
上游 context 中不会再有 inst X 的 entry；B/AMX/BMX 的收集侧 sva（上表）
保证 END pop 时同 inst 无悬挂 work；收集侧允许存在的是**新** inst 的
work，其 inst≠end_inst，不干扰 `is_last`——§14.1 论证。）

## 9. 子程序：cand_holder（CHD，F-070…F-073）

> 命名（2026-10-14 用户决策）：`packer` 改名 `cand_holder`（candidate
> 持有/形成/递补 + seq/planned 锁存），对应规格 BandwidthPacker 的
> candidate 持有职能；满宽/可见块判定与块展开在 assembler（§8）。
> **边3 严格流水（同日用户决策，规格偏差）**：仲裁只认 held 快照——
> fresh 形成拍不参与仲裁/fire，拍末捕获入 held，次拍起参与（链首 +1 拍）；
> fire 后递补同拍捕获、次拍可再 fire（连发 1 fire/拍）。

```python
FULL_COUNT = {A:1, AMX:4, B:1, BMX:4}

def chd_eval(lane, av, S):
    # 可见块数函数（A-002 结论 2 精确化；与 golden same_inst_count 等价，§14.3）
    visible = {A:   emit ? 16-cur : (head_rd ? 16 : 0),
               B:   emit ? 2-half : (completing ? 2 : 0),
               AMX: emit ? 8-rg   : (closing/transfer ? 8 : 0),
               BMX: emit_complete ? 4 : 0}[lane]
    formable = visible >= FULL_COUNT[lane]
    # instruction-last partial（通用规则）：end_v && view.inst==end_inst && 0<visible<FULL_COUNT → 也 formable；
    # UU 128B 下不可达（D-003：A/B FULL_COUNT=1、AMX 8≡0 mod 4、BMX 例外），sva 登记。
    cand = S.held[lane]                   # 边3 严格流水：仲裁只认 held 快照（valid 才可仲裁）；
                                          # fresh 形成额仅供 commit 拍末捕获入 held，不进入本拍 cv
    return cand

def chd_commit(lane, grant, av, S):
    # 统一规则（§14.3 推导）：held' = formable(view(ctx')) ? scalars(view(ctx')) : INVALID
    # ctx' = asm_commit 后的次态 context；fire 时 ctx' 已含消费效果
    # seq：fresh 形成用 cand_seq（若 view.inst != lane_inst 则为 0 并将 lane_inst 切换、
    # cand_seq 置 1）；fire 后 replacement 形成再 +1（D-005 全 case 表，Step 6 冻结）
```

规则直译（R-17/R-18）：DataBlock 不拆半；非 instruction-last 不足带宽
等待；`rd_mem_id` = 首 block 的 `rdgen_id`（split 沿用、merge 取最早——
各 lane view 构造已保证）；每 lane 恰好 1 个 held candidate；未 grant
时 valid/payload 保持（由「源 context 冻结 + held 寄存」双重实现，
§14.3）；candidate 形成时锁存 `planned_base/planned_advance`（F-073）。

## 10. 子程序：tag_checker + arbiter + fire（TCK/ARB，F-080…F-094）

> 命名（2026-10-14 用户决策）：`allocator` 改名 `tag_checker`（直观体现
> tag 状态查询职能），对应规格 DestinationAllocator。
> 硬件映射注记：本节 `fire_commit` 的 RdMemRequest 组装在 Step 6 落为
> **顶层 payload mux → §11B req_sched 发送队列**（CYCLE_AWARE §11A/§11B，
> A-014），arbiter 模块仅保留选择控制（eligibility/优先键/RR/cursor），
> 控制流与 payload 解耦；端口组在 issue 拍（grant 次拍）原子发出。

```python
def tck_eval(cv, inp, S):
    for l in LANES:
        # A-004 相位契约：query 由 cycle-start held 锁存派生；valid=0 时外部必须答 1
        query[l] = (cv[l].valid and cv[l].planned_advance > 0) \
                   ? (1, cv[l].planned_base, cv[l].planned_advance) \
                   : (0, S.load_ptr[l], 0)
        dest_ok[l] = query[l].valid ? inp.load_range_idle[l] : True   # split 续写恒真（F-082）
    return dest_ok

def arb_eval(cv, dest_ok, inp, S):
    elig[l] = cv[l].valid and inp.issue_room and inp.source_ok[l] and dest_ok[l]
    # A-014：eligible 准入用发送队列 issue_room（mem_ready 移至 §11B 队列出口，issue 拍采样）
    # 优先键：最小 (inst_id, rd_mem_id)；同键从 rr_cursor 按 [A,AMX,B,BMX] 扫描（F-091）
    grant = first_in_rr_order(argmin_key(elig), S.rr_cursor) if any(elig) else NONE
    return grant                              # 每拍 ≤1 grant（F-090）；端口 valid⇒同拍发出在 issue 拍（A-014，§5.3 新落位）

def fire_commit(lane, cv, S):                 # SRC-01 sec 13：内部六效果同一 commit（A-014：端口组经 §11B 发送队列在 issue 拍发出）
    base = cv[lane].planned_advance>0 ? cv[lane].planned_base : S.grp[lane].base
    req = RdMemRequest(
        key=(cv.inst_id, lane, cv.seq), rd_mem_id=cv.rd_mem_id,
        src_ranges = Σ blocks.src_ranges（≤32，A-003）,
        load_bytes=cv.load_bytes, valid_bytes=cv.valid_bytes, pad_bytes=cv.pad_bytes,
        writes   = expand_writes(lane, cv, base)（≤32，§10.1）,
        tag_range= (base, cv.planned_advance if new else S.grp[lane].cnt),   # 定长 1（A-003）
        confirm  = cv.group_final,                # 仅整 range 末贡献 request（F-094）
        is_partial = (cv.load_bytes < 128),       # UU 恒 0（D-003，sva）
        is_last    = cv.is_last)
    emit_via_rqp(req)                      # A-014：request+update 组合入 §11B 发送队列，issue 拍原子发出
    S.rr_cursor = lane + 1 mod 4      # cursor 仅 fire 更新（F-091；fire=内部 grant commit）

def tck_commit(grant, cv, S):
    if grant.fire and cv.planned_advance > 0:
        old = S.load_ptr[lane]                    # sva：== planned_base（held 期间不变）
        upd = LoadPtrUpdate(lane, old, (old+adv) % DEPTH[lane], adv)  # A-014：与 request 同组入 §11B 队列，issue 拍原子发出（F-093）
        S.load_ptr[lane] = old + adv (mod DEPTH)  # 连续分配、禁跳 busy（F-080；内部 commit 在 grant 拍）
        S.grp[lane] = GroupBind(open=1, base=old, cnt=adv)
    if grant.fire and cv.group_final:
        S.grp[lane].open = 0                      # UU 每 lane ≤1 open group（D-004，sva）
```

### 10.1 writes 展开（PORT_LIST §8 适配 1/2；byte_mask→{index,offset,len}）

```text
A：   1 项  (base,            cur*128, 128)
B：   pair? 2 项 (base+i, half*64, 64) ；single 1 项 (base, half*64, 64)
AMX： 4 tile × 每 tile 实 chunk：(base+t, (rg+r)*8, 8)，t<cnt×span（实 key 覆盖的 tag）；
      mem-pad chunk 不写；≤16 项
BMX： 逐 real owner j、逐 span：(base + j*span + s, 0, 4)；= advance 项（≤32）
tag_range：base/count 同上；confirm=group_final；padding 不写不确认（F-094）；
MX range 覆盖完整 span（由 advance=Σspan 构造保证）。
```

### 10.2 子程序：req_sched 发送队列（A-014，§11B 的 SEQ 对应物）

```python
def rqp_eval(inp, S):
    front_v = S.rq_cnt > 0
    pop     = front_v and inp.shared_mem_ready      # issue 拍：valid⇒同拍发出
    room    = (S.rq_cnt < 2) or (S.rq_cnt > 0 and inp.shared_mem_ready)
    # room 供 arb_eval 的 eligibility（issue_room 替代 mem_ready 准入，A-014）
    return (front_v, pop, room)

def rqp_commit(grant, ev, S):
    if ev.pop:                                  # issue 拍消费 front（payload 未 pop 保持）
        S.rq_pr = (S.rq_pr + 1) % 2; S.rq_cnt -= 1
    if grant.fire:                              # grant 拍：§11A 载荷（req+update）写入 slot[pw]
        S.rq[S.rq_pw] = fire_payload(grant.lane)   # emit_via_rqp 的 SEQ 视图
        S.rq_pw = (S.rq_pw + 1) % 2; S.rq_cnt += 1
    assert S.rq_cnt <= 2                        # never-overflow（eligibility 保证）
```

性质：`push→pop` 最早 +1 拍；稳态 ready=1 时 grant/pop 各 1/拍（端口
1 issue/拍保持）；ready=0 时 front 保持、cnt 到 2 则 grant 冻结；
端口顺序 == grant 顺序（FIFO，不破坏 MEM in-order 前提）。

## 11. 子程序：C-only 路径（C，F-100/F-025）

```python
def c_eval(inp, S):
    head = S.c_fifo[S.c_head] if S.c_cnt > 0 else INVALID
    fire = head.valid and inp.register_ready      # 唯一准入；无竞争仲裁；≤1/拍
    return (head, fire)

def c_commit(ev, rdg, S):
    if ev.fire: S.c_head += 1; S.c_cnt -= 1       # 未 fire 保持 head/payload
    if rdg.c:   S.c_fifo[S.c_tail] = rdg.c; S.c_tail += 1; S.c_cnt += 1
    assert S.c_cnt <= 8                           # never-full（A-002，sva）
    # rdgen 拍末新 entry 次拍起可 issue（与普通 Queue 一样无同拍 bypass）
```

C entry 常量化字段（不占状态）：kind=C、16B、`beat 1/1`、无
owner/writes/confirmed_ranges（SRC-08 sec 5.1）。

## 12. reset 与 idle（F-003/F-120/A-010）

reset 最高优先级，清空：§2 全部状态（配置 FIFO、cfg、walker、rd_id、
四路 Queue、全部 assembler context、held、cand_seq、grp、load_ptr、
C FIFO；`rr_cursor=A`）；reset 期间忽略全部输入握手。

`o_walk_stall` 恒 0（A-009）。`o_lfsm_idle` = walker 不 active 且两条
配置 FIFO 空 且四路 Queue 空 且四路 assembler context 全空 且四路 held
无效 且**发送队列空（§11B cnt==0）** 且 C FIFO 空（电平；含配置
FIFO 空以对齐 golden `drained()`，发送队列空覆盖端口在途回放）。

## 13. 几何辅助函数汇总

| 函数 | 定义 | 落点 |
| :--- | :--- | :--- |
| `n_len_rule(rem)` | `rem∈{9,10} ? 4 : min(8,rem)` | walker N_OUTER/K_OUTER/start |
| `k_count_rule(kb)` | `min(k_step, k_groups−kb)` | walker K_OUTER/start |
| `span_decode` | span∈{1,2,4}→base_k/keys_per_tile | 配置装载 |
| `rg_len` | `ceil(k_groups*span/4)*32` | 配置装载（rdgen 用）；AMX emit（entry 注解重算） |
| `n_hw2` | `n_hw_count + (n_hw_count&1)` | 配置装载；BMX entry 注解 |
| `ring(i)` | `(base+i) & (DEPTH-1)` | tag_checker/writes |

## 14. 表示差异与等价性论证（对拍锚点）

### 14.1 计数器条件替代查表/CAM（A-001 扩展）

- 去重：`generated_data_keys` set → `fv_a/fv_b/fv_c` 计数器条件（A-001
  原始论证）；outer 计数由 `n_base==0`/`k_base==0` 替代（A-005 v3）。
- B pair 不跨 N block：非末 block 长恒为 8 或 4（偶），末 block 才可为
  奇；block base 恒偶 ⟹ (偶,奇) pair 不越界；奇尾 single ⟺
  `n==n_hw-1 && n偶` ⟹ `n_tail_single` 单 bit 注解等价
  `b_pair_members` 查表（REF-03 policy）。
- BMX 到达序 = 坐标序：窗口坐标按 (k 行, n 内层) 字典序，walk 在窗口内
  恰好按 k_local→n_inner 生成且每坐标一次 ⟹ FIFO 位置 j = 坐标序号，
  替代 golden 的 `slot_of/expected_coordinates` 列表比较。
- `is_last` 无需查队列尾：END 按 FIFO 序位于同 inst 全部 entry 之后，
  `end_inst==X` ⟹ 队列与上游 context 中无 inst X 的 entry（§8.6 tag 式
  判定，b2b 安全）。

### 14.2 b2b 几何混叠与 entry 注解（D-002）

lane 可在 walker 已进入 instruction *i+1* 时仍在 drain *i*，故
assembler **不读** `S.cfg`，所需 per-inst 几何全部由 rdgen 在生成拍
（配置必为当前 instruction）写进 entry 注解：B=`n_tail_single`；
AMX=`span/k_groups/is_k_tail`；BMX=`span/k_groups/n_hw2`（+
`n_blk_base/n_blk_len` 随 token 注解）。A/C 无需注解。与 golden 按
`inst_id` 查配置表（REF-03 `instructions[...]`）语义等价。

### 14.3 emit-on-demand 与突发块池（D-001，A-002 结论 2 定稿）

golden 的 `assembler.blocks` 为无界突发池（建模产物）；本文以
collect/emit 槽 + block 游标 + 组合展开视图替代，物理块池 = 0。
等价性论证（结构性）：
1. **可见块数等价**：§9 `visible[lane]` 与 golden `_can_form` 的
   `same_inst_count` 在每拍边界同值（A/B 游标差、AMX 8−rg、BMX 窗口
   完成即 4），formable 判定逐拍一致；
2. **candidate 组成等价**：blocks 内容/顺序由同一几何规则展开，
   `rd_mem_id`/new owner/advance/is_last 构造规则相同；
3. **fire 序列等价（边3 严格流水 + A-014 发送段版）**：candidate 形成
   后一律经 held 快照参与仲裁（次拍 grant）、再经 §11B 发送队列在
   issue 拍发出——**每条 candidate 链首相对 golden 相移 +2 拍**（边3
   +1、发送段 +1），链内 replacement 保持每拍 1 grant/issue。等价口径：
   **逐笔 fire/issue 元数据等价 + 链首恒定相移**（grant 拍内部 commit
   == golden fire 拍的状态效果；端口流按 issue 次序逐笔等值），而非逐拍
   精确等价（回放式 TB 对拍口径随此调整，Step 8 TEST_PLAN 落实；
   `ALGORITHM_PIPELINED.md` §3 三拍分段）；
4. **保持语义等价**：未 fire 时 context/held 全保持（F-113）；
5. **积压位置等价**：context 钉死几何界后，在途 owner 由 RD Queue
   承接（A-002 结论 3），never-full 受力点不变。
最终闭环：`rd_mem_fire` 粒度 golden 对拍（计划「验证策略」）。

### 14.4 UU 下恒真/不可达项登记（D-003/D-004）

- D-003：`is_partial_beat ≡ 0`（128B：A/B FULL_COUNT=1、AMX 块数恒
  8≡0 mod 4、BMX 固定窗口恒满）；instruction-last partial 路径实现但
  不可达 → sva 登记，generic `FULL_COUNT` 规则保留（LOAD_BUS_BYTES 参数）。
- D-004：每 lane 任意时刻 ≤1 个 open allocation group（A 单 owner、
  B pair、AMX run、BMX 窗口，均串行开关）⟹ `tag_ranges[]` 定长 1
  （A-003 已决策）、grp 单槽实现；confirm = `group_final` 组合条件
  （替代 golden `fully_packed/confirmation_sent` 集合），group 完成即
  context 退役，不会重复 confirm（TB 断言每 group 恰好 confirm 一次）。

## 15. 派生决策记录（D-xx；Step 7 提升路径）

| ID | 决策 | 依据 | 提升落点 |
| :--- | :--- | :--- | :--- |
| D-001 | emit-on-demand：DataBlock 为 context 组合展开视图，物理块池=0；collect/emit 槽尺寸定稿（A:1 owner、B:1+2、AMX:4+4、BMX:2×32 src） | A-002 结论 2 授权 Step 4-6 定稿；§14.3 | ASSUMPTIONS v4 + PIPELINED §5 |
| D-002 | per-inst 几何经 entry 注解下发（B/AMX/BMX），assembler 不读当前配置寄存 | b2b 混叠分析 §14.2；golden 按 inst_id 查表 | ASSUMPTIONS v4 |
| D-003 | UU 128B 下 `is_partial_beat≡0`、instruction-last partial 不可达（实现保留 + sva） | §9/§14.4 | ASSUMPTIONS v4 + TEST_PLAN |
| D-004 | 每 lane ≤1 open group；confirm=`group_final` 组合 | §14.4；A-003 同系 | ASSUMPTIONS v4 |
| D-005 | `cand_seq` per-lane、instruction 首 candidate 清零（PORT_LIST §8 适配 3）；golden dump 按 instruction 重排号对拍 | PORT_LIST §4.4/§8 | TEST_PLAN/golden 工具 |
| D-006 | **边3 严格流水**（规格偏差）：cand_holder→arbiter 禁同拍——仲裁输入=held 快照 + 当拍 ready 电平；fresh 形成拍不 fire（链首 +1 拍）；replacement 链维持 1 fire/拍；golden 对拍口径改为逐笔 fire 等价 + 链首相移 | 2026-10-14 用户决策（时序收口动机）；§9/§14.3；PIPE §3 | ASSUMPTIONS 预登记（A-013）+ FEATURE_LIST F-073 + TEST_PLAN |
| D-007 | **发送段 req_sched（A-014，规格偏差，推翻 A-006）**：grant 与 MEM 下发解耦——§11A mux 载荷（含 LoadPtrUpdate 组）经 **2-slot 发送队列**在 issue 拍（grant 次拍）原子发出；`i_shared_mem_ready` 移至队列出口；仲裁准入改 `issue_room`；深度 2 保 ready 稳态 1 issue/拍；内部 commit（消费/binding/load_ptr/RR）仍在 grant 拍原子 | 2026-10-14 用户决策（拆分选择与 MEM 下发 chain）；§10/§14.3；PIPE §3 三拍分段/§8.1、CYCLE §11B/§13 | ASSUMPTIONS 预登记（A-014）+ TRACEABILITY GAP-07 + TEST_PLAN 端口断言调整 |

## 16. golden 函数映射表

| 本文子程序 | golden 参照 | 对拍粒度 |
| :--- | :--- | :--- |
| §4 cfg_* | REF-02 `commit` START 分支 / `config_queue` | 配对/启动拍 |
| §5 walk_* | REF-01 `MknWalkFSM`（含 transition 优先级） | 逐拍 token 序列 |
| §6 rdg_* | REF-02 `_needed_rds/_make_rd/_make_ru_c_request/end_instruction` | 入队流/C 流 |
| §7 q_* | REF-03 `entries/enqueue/end_instruction` + REF-02 计数不变量 | head 序列/占用 |
| §8 asm_* | REF-03 `LaneAssembler.step/_emit_a/_emit_b_group/_emit_amx_group/_emit_bmx_window/_emit_ready_bmx_windows` | block 流 |
| §9 chd_* | REF-03 `_can_form/form_candidate/consume_candidate` | candidate 流 |
| §10 tck/arb/fire + §10.2 rqp | REF-02 `evaluate/_allocate_candidate/_build_mem_request/commit` + REF-04 `range_idle`（外部） | `rd_mem_fire` 逐笔（端口按 issue 序） |
| §11 c_* | REF-02 `_ru_c_needed/_make_ru_c_request` + RU C FIFO issue | `o_reg_req_*` 流 |
| §12 reset/idle | REF-02 `drained()`、REF-07 reset | drain 完成拍 |
```
