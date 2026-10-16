# LFSM (4EU UU mode) ALGORITHM_CYCLE_AWARE_PSEUDOCODE

> Step 6 交付物（依据 `docs/pycircuit_implementation_method.md` Step 6：
> 「Full cycle-aware algorithm in detailed pseudocode」）。**逐行可译 V6**
> 的完整伪码：每个子模块给出签名、`inputs` 字典键（位宽/shape）、
> 返回 `outs` 键（类型）、内部 `domain.next()` 数、reset/idle/反压
> 路径与全部状态赋值点。建立日期：2026-10-13。
> 上游：`ALGORITHM_SEQUENTIAL.md`（SEQ，功能语义权威）、
> `ALGORITHM_PIPELINED.md`（PIPE，cycle/寄存器/存储决策）、
> `PORT_LIST.md`（端口与位宽）、`FEATURE_LIST.md`（F-xxx 追踪）。
> V6 规范引用：PRC-01 = `docs/v6_PyCircuit_Specification.md`。
> 本文不引入新语义决策；D-001…D-005 见 SEQ §15。

## 0. 记法与公共约定

- 每个带状态子模块结构固定（PIPE §1）：`# Cycle 0` 段声明状态 + 纯
  组合求值 + 组装 `outs`（全部 cycle-0 CAS）；`domain.next()`（内部
  **1 次**）；`# Cycle 1` 段对每个状态恰好一次 `<<=` / `.assign(when=)`
  （读 0 写 1 → 1 DFF，PRC-01 §4）。无 `domain.cycle()`、无 gap≥2。
- `submodule_input(inputs, key, m, domain, prefix=prefix, width=W)` 声明
  每个输入键；向量输入在该助手之外以
  `cas(domain, m.input(f"{prefix}_<key>", width=W, shape=[N]), cycle=0)`
  创建（PRC-01 §2/§5）。独立模式（`inputs is None`）才发射
  `m.output()`：标量 `wire_of(sig)`，向量 `Wire` 直传。
- 辅助函数（types.py 内实现，组合小逻辑）：
  `vec_rd(v, idx)`（动态读 = mux 树）、`vec_wr(v, idx, val, en)`（逐
  element 条件写，返回次态向量）、`ring_add(base, x, DEPTH)`（2 幂
  → `& (DEPTH-1)`）、`min2/argmin_key`（比较树）。
- 常量（types.py）：lane 编码 `A=0/AMX=1/B=2/BMX=3`；位宽
  `INST_ID_W=4, ADDR_W=32, RDGEN_ID_W=14, RD_ID_W=12, CAND_SEQ_W=13,
  TAG_IDX_W=8, TAG_ADV_W=6, BYTE_CNT_W=8, BYTE_OFF_W=11, SEQ_W=13,
  M_IDX_W=1, N_IDX_W=8, K_IDX_W=6`；dtype/m_mode/eu_mode 编码见
  PORT_LIST §4 约定；`FULL_COUNT={1,4,1,4}[lane]`；
  `BLOCK_BYTES={128,32,128,32}[lane]`；`DEPTH={8,32,32,256}[lane]`
  （静态参数 BUFA/AMX/L0B/BMX_SLOTS）。
- `sva(...)` = TB/sva 断言（F-112 落点，不进硬件功能路径）。
- **多赋值约定**：同一信号出现多个 `.assign()` 时，按书写顺序构成
  优先级链（**后者优先**）；实现时合并为单个次态函数（嵌套 `mux`），
  保证每个信号每拍恰好一个有效赋值点。无 `.assign()` 命中的状态保持
  （F-113）。
- 端口 key 全表见 PORT_LIST §4；本文只列子模块 `inputs`/`outs` 键。
  各 `inputs` 表末列为**来源**（该键由哪个模块/外部端口驱动），
  `outs` 表末列为**去向**（该键被哪个模块/外部端口消费）；「经 top」
  表示经 `lfsm_top` 纯连线转接（无寄存器），「§11A」为顶层组合 mux。

## 1. `config_regs`（prefix `lfsm_cfg`，内部 next=1）

### 1.1 inputs 键

| key | 位宽/shape | 语义 | 来源 |
| :--- | :--- | :--- | :--- |
| `i_walk_cfg_valid` / `i_walk_cfg_inst_id` / `i_walk_cfg_m_mode` / `i_walk_cfg_m_slice_count` / `i_walk_cfg_n_hw_count` / `i_walk_cfg_n_step` / `i_walk_cfg_k_groups` | 1 / 4 / 1 / 2 / 8 / 2 / 6 | WalkConfig 通道（PORT_LIST §4.1） | TOP（外部端口） |
| `i_lfsm_cfg_valid` / `i_lfsm_cfg_inst_id` / `i_lfsm_cfg_eu_mode` / `i_lfsm_cfg_data_type` / `i_lfsm_cfg_mx_mode_en` / `i_lfsm_cfg_mx_bytes_per_k0` / `i_lfsm_cfg_n_hw_count` | 1 / 4 / 1 / 3 / 1 / 3 / 8 | LFSMInstructionConfig 通道（§4.2） | TOP（外部端口） |
| `i_lfsm_cfg_{a,a_mx,b,b_mx}_base_addr` / `..._limit_addr` / `i_lfsm_cfg_l0c_base_addr` | 32 ×9 | 地址范围（limit 仅供 sva） | TOP（外部端口） |
| `i_start_accept` | 1 | 启动准入 | walker（`~wlk_active`，经 top） |

### 1.2 outs 键（均 cycle-0 标量 CAS）

| key | 位宽 | 语义 | 去向 |
| :--- | :--- | :--- | :--- |
| `o_walk_cfg_ready` / `o_lfsm_cfg_ready` | 1 | 配置 FIFO 非满 | TOP（外部端口） |
| `pair_ok` | 1 | 两 FIFO head `inst_id` 相等 | （观测/TB） |
| `start` | 1 | 配对启动 strobe | walker、rdgen |
| `cfg_inst_id` | 4 | 当前 instruction | walker、rdgen |
| `cfg_m_mode` / `cfg_m_slice` / `cfg_k_step` | 1/2/4 | 走法几何 | walker |
| `cfg_n_hw` / `cfg_k_groups` | 8/6 | 规模计数 | walker、rdgen |
| `cfg_mx_en` / `cfg_span` / `cfg_rg_len` / `cfg_n_hw2` / `cfg_base_k` / `cfg_keys_per_tile` | 1/3/11/8/3/3 | MX/派生几何 | rdgen |
| `cfg_{a,a_mx,b,b_mx,l0c}_base` | 32 ×5 | 地址基址 | rdgen |
| `cfg_empty` | 1 | 配置 FIFO 全空 | lfsm_top（`o_lfsm_idle`） |

### 1.3 伪码

```python
def config_regs(m, domain, *, inputs=None, prefix="lfsm_cfg", CFG_FIFO_DEPTH=2):
    # ── Cycle 0 ──────────────────────────────────────────────
    # 状态：两条配置 FIFO（字段展平的 signal 数组 + ptr）
    wq_v   = domain.signal(width=1, shape=[CFG_FIFO_DEPTH], reset_value=0, name=f"{prefix}_wq_v")
    # … wq_inst(4)/wq_m_mode(1)/wq_mslice(2)/wq_nhw(8)/wq_nstep(2)/wq_kgroups(6) ×depth
    lq_v   = domain.signal(width=1, shape=[CFG_FIFO_DEPTH], reset_value=0, name=f"{prefix}_lq_v")
    # … lq_*（§1.1 各字段）×depth
    w_head, w_tail = domain.signal(width=1, ...), domain.signal(width=1, ...)
    l_head, l_tail = domain.signal(width=1, ...), domain.signal(width=1, ...)
    # 配置寄存组（start 时装载）
    cfg_*  = domain.signal(...)              # §1.2 全部 cfg_* 字段
    # 输入
    wv = submodule_input(inputs, "i_walk_cfg_valid", m, domain, prefix=prefix, width=1)
    # … 其余输入按 §1.1
    start_accept = submodule_input(inputs, "i_start_accept", ..., width=1)

    w_full  = wq_v[0] & wq_v[1]          # 见注①
    w_ready = ~w_full                    # ready = 非满（cycle-0 组合，PORT_LIST §5.1）
    l_full  = lq_v[0] & lq_v[1]
    l_ready = ~l_full
    accept_w = wv & w_ready
    accept_l = lv & l_ready
    pair_ok  = wq_v[w_head] & lq_v[l_head] & (wq_inst[w_head] == lq_inst[l_head])
    sva(~(wq_v[w_head] & lq_v[l_head] & (wq_inst[w_head] != lq_inst[l_head])),
        "config inst_id mismatch")       # A-005.2 协议错误
    start    = pair_ok & start_accept    # walker 空闲才启动（F-012）
    cfg_empty = ~(wq_v[0] | wq_v[1] | lq_v[0] | lq_v[1])   # 见注①
    outs = dict(o_walk_cfg_ready=w_ready, o_lfsm_cfg_ready=l_ready,
                pair_ok=pair_ok, start=start, cfg_inst_id=cfg_inst, ..., cfg_empty=cfg_empty)

    domain.next()
    # ── Cycle 1（写周期 1 → 1 DFF；reset_value 全 0，A-010）─────────────
    # accept 入队（拍末生效）；start pop（v 位清除）——两者永不写同一槽
    for i in range(CFG_FIFO_DEPTH):
        wq_v[i].assign(1, when=accept_w & (w_tail == i))
        wq_v[i].assign(0, when=start & (w_head == i))
        # … wq_*[i].assign(payload, when=accept_w & (w_tail==i))
    w_tail.assign(w_tail + 1, when=accept_w)
    # … lq 同理
    # start：pop 两 FIFO head + 装载配置寄存组（派生量一次算好）
    w_head.assign(w_head + 1, when=start)
    l_head.assign(l_head + 1, when=start)
    cfg_inst.assign(wq_inst[w_head], when=start)      # 两 FIFO head inst_id 相等
    cfg_kstep.assign(mux(wq_m_mode[w_head], u(4,4), u(4,8)), when=start)
    cfg_span.assign(mux(lq_mx_en[w_head], lq_mx_bpk0[w_head], u(3,0)), when=start)
    cfg_base_k.assign(base_k_of(lq_mx_bpk0[w_head]), when=start)      # 4/span ∈{4,2,1}
    cfg_kpt.assign(keys_per_tile_of(lq_mx_bpk0[w_head]), when=start)  # 4/span
    cfg_nhw2.assign(lq_nhw[w_head] + (lq_nhw[w_head] & 1), when=start)
    cfg_rglen.assign(rg_len_of(wq_kgroups[w_head], lq_mx_bpk0[w_head]), when=start)
    #   rg_len_of(k,s) = ((k*s + 3) >> 2) << 5（加法级，SEQ §13）
    # … 其余 cfg_*（base 地址群）assign
    # 结构断言（F-002，sva）：k_groups≤32、m_slice≤2、mx_en→span∈{1,2,4}、
    #   n_step==1、eu_mode==0；loop 自检（A-005.3）：终值 n_base==n_hw、k_base==k_groups
    return outs
```

注①：深度 2 FIFO 的 full/empty 用 `v[]` 位向量 + 单 bit 指针直接展开
（DEPTH 小，无需 cnt 寄存器）；`cfg_empty` 供 `o_lfsm_idle`（F-120）。

## 2. `walker`（prefix `lfsm_wlk`，内部 next=1）

### 2.1 inputs / outs

| in key | 位宽 | 语义 | 来源 |
| :--- | :--- | :--- | :--- |
| `start` | 1 | 启动 strobe | config_regs |
| `cfg_inst_id/cfg_m_mode/cfg_m_slice/cfg_n_hw/cfg_k_groups/cfg_k_step` | 4/1/2/8/6/4 | 配置字段 | config_regs |
| `stall` | 1 | 内部 tie-0（A-009；保持语义完整实现，F-011） | lfsm_top（常量 0） |

| out key | 位宽 | 语义 | 去向 |
| :--- | :--- | :--- | :--- |
| `wlk_active` | 1 | walker 忙 | config_regs（`i_start_accept`）、lfsm_top（idle） |
| `tok_valid` / `tok_inst_id` / `tok_m` / `tok_n` / `tok_k` | 1/4/1/8/6 | token | rdgen |
| `tok_seq` | 13 | walk_seq（rdgen_id=seq+1） | rdgen |
| `tok_first` / `tok_last` / `tok_done` | 1 | first/last/done=advance&&last | rdgen |
| `tok_nblk_base` / `tok_nblk_len` | 8/4 | BMX entry 注解 | rdgen |
| `tok_fv_a` / `tok_fv_b` / `tok_fv_c` | 1 | 首访条件（A-001） | rdgen |
| `tok_tr` | 3 | transition 枚举 | rdgen（观测/对拍） |

### 2.2 伪码

```python
def walker(m, domain, *, inputs=None, prefix="lfsm_wlk"):
    # ── Cycle 0 ──────────────────────────────────────────────
    active  = domain.signal(width=1,  reset_value=0, name=f"{prefix}_active")
    seq     = domain.signal(width=13, reset_value=0, name=f"{prefix}_seq")
    m_idx   = domain.signal(width=1,  reset_value=0, name=f"{prefix}_m")
    n_inner = domain.signal(width=4,  reset_value=0, name=f"{prefix}_ninner")
    k_local = domain.signal(width=4,  reset_value=0, name=f"{prefix}_klocal")
    n_base  = domain.signal(width=8,  reset_value=0, name=f"{prefix}_nbase")
    n_len   = domain.signal(width=4,  reset_value=0, name=f"{prefix}_nlen")
    k_base  = domain.signal(width=6,  reset_value=0, name=f"{prefix}_kbase")
    k_count = domain.signal(width=4,  reset_value=0, name=f"{prefix}_kcount")
    start   = submodule_input(inputs, "start", ..., width=1)
    cfg_*   = submodule_input(...)     # §2.1
    stall   = submodule_input(inputs, "stall", ..., width=1)   # 顶层 tie 0

    rem_n     = cfg_n_hw - n_base
    n_len_nxt = mux((rem_n == 9) | (rem_n == 10), u(4,4),
                    mux(rem_n > 8, u(4,8), rem_n[0:4]))        # n_len_rule（SEQ §5.2）
    k_count_nxt = mux(cfg_k_groups - k_base > cfg_k_step, cfg_k_step,
                      (cfg_k_groups - k_base)[0:4])            # k_count_rule
    last_block = (n_base + n_len == cfg_n_hw)
    last_outer = (k_base + k_count == cfg_k_groups)
    tr = mux(n_inner + 1 < n_len,        TR_N_INNER,
         mux(k_local + 1 < k_count,      TR_K_LOCAL,
         mux(m_idx + 1 < cfg_m_slice,    TR_M_SLICE,
         mux(~last_block,                TR_N_OUTER,
         mux(~last_outer,                TR_K_OUTER, TR_DONE)))))   # 优先级表（SEQ §5.3）
    advance   = active & ~stall
    tok_done  = advance & (tr == TR_DONE)
    outs = dict(
        wlk_active=active,
        tok_valid=active, tok_inst_id=cfg_inst,
        tok_m=m_idx, tok_n=(n_base + n_inner)[0:8], tok_k=(k_base + k_local)[0:6],
        tok_seq=seq, tok_first=(seq == 0), tok_last=(tr == TR_DONE), tok_done=tok_done,
        tok_nblk_base=n_base, tok_nblk_len=n_len,
        tok_fv_a=(n_base == 0) & (n_inner == 0),
        tok_fv_b=(m_idx == 0),
        tok_fv_c=(k_base == 0) & (k_local == 0),
        tok_tr=tr)

    domain.next()
    # ── Cycle 1 ──────────────────────────────────────────────
    # start 装载（优先于 advance；start 与 active 互斥，start 时 active==0）
    active.assign(1, when=start);  active.assign(0, when=tok_done)
    seq.assign(u(13,0), when=start); seq.assign(seq + 1, when=~start & advance)
    m_idx.assign(u(1,0), when=start)
    m_idx.assign(m_idx + 1, when=~start & advance & (tr == TR_M_SLICE))
    m_idx.assign(u(1,0), when=~start & advance & ((tr == TR_N_OUTER) | (tr == TR_K_OUTER)))
    n_inner.assign(u(4,0), when=start | (advance & (tr != TR_N_INNER)))
    n_inner.assign(n_inner + 1, when=~start & advance & (tr == TR_N_INNER))
    k_local.assign(u(4,0), when=start | (advance & ((tr == TR_M_SLICE) | (tr == TR_N_OUTER) | (tr == TR_K_OUTER))))
    k_local.assign(k_local + 1, when=~start & advance & (tr == TR_K_LOCAL))
    n_base.assign(u(8,0), when=start | (advance & (tr == TR_K_OUTER)))
    n_base.assign(n_base + n_len, when=~start & advance & (tr == TR_N_OUTER))
    n_len.assign(n_len_nxt, when=start | (advance & ((tr == TR_N_OUTER) | (tr == TR_K_OUTER))))
    k_base.assign(u(6,0), when=start)
    k_base.assign(k_base + k_count, when=~start & advance & (tr == TR_K_OUTER))
    k_count.assign(k_count_nxt, when=start | (advance & (tr == TR_K_OUTER)))
    # stall 语义（F-011/A-009）：stall=1 时上述 advance 全不成立 → 全保持；
    # 顶层 stall tie-0。reset：全部 reset_value=0（F-003）。
    return outs
```

## 3. `rdgen`（prefix `lfsm_rdg`，内部 next=1）

### 3.1 inputs / outs

| in key | 位宽 | 语义 | 来源 |
| :--- | :--- | :--- | :--- |
| `tok_*` | §2.1 | walker token 全组 | walker |
| `start` | 1 | rd_id per-instruction 清零 | config_regs |
| `cfg_inst_id/cfg_mx_en/cfg_span/cfg_rg_len/cfg_n_hw2/cfg_n_hw/cfg_k_groups/cfg_{a,a_mx,b,b_mx,l0c}_base` | — | 配置字段 | config_regs |

| out key | 位宽 | 语义 | 去向 |
| :--- | :--- | :--- | :--- |
| `enq_{a,amx,b,bmx}_valid` | 1 | 各 lane 入队使能（≤1/拍/lane） | rd_queue（对应 lane 实例） |
| `enq_*_payload…` | 见 §3.2 | entry 字段（含 D-002 注解） | rd_queue（对应 lane 实例） |
| `end_{a,amx,b,bmx}` | 1 | LaneLoadEnd strobe（done 拍，required lanes） | rd_queue（对应 lane 实例） |
| `c_enq_valid` / `c_enq_{inst,rdgen,m,n,src}` | 1 / 4/14/1/8/32 | C FIFO entry | c_path |

### 3.2 entry payload 位宽（D-002）

```text
A:   {inst 4, rdgen 14, rd_id 12, src 32}                        # m/k 仅观测用，不进队列
B:   {inst 4, rdgen 14, rd_id 12, src 32, n 8, k 6, single 1}
AMX: {inst 4, rdgen 14, rd_id 12, src 32, m 1, k 6, span 3, kgs 6, is_k_tail 1}
BMX: {inst 4, rdgen 14, rd_id 12, src 32, span 3, kgs 6, nhw2 8, nblk_base 8, nblk_len 4, k 6}
```

字段×lane 对照（四路不对齐的依据：公共核 62b 一致，差异全部是
D-002 注解——各 lane assembler 的 merge/展开规则所需的 per-inst 几何
判定字段不同；b2b 下 assembler 不读当前配置寄存器，SEQ §14.2）：

| 字段 | A | B | AMX | BMX | 谁消费 / 用途 |
| :--- | :-: | :-: | :-: | :-: | :--- |
| `inst 4` | ✓ | ✓ | ✓ | ✓ | 优先键 / b2b 区分 / `is_last` 比对 |
| `rdgen 14` | ✓ | ✓ | ✓ | ✓ | `rd_mem_id`（split 沿用、merge 取最早，R-18） |
| `rd_id 12` | ✓ | ✓ | ✓ | ✓ | lane-local owner 序号（分配序/观测） |
| `src 32` | ✓ | ✓ | ✓ | ✓ | rdgen 生成拍预算好的最终地址（下游不做地址计算） |
| `n 8` | — | ✓ | — | — | B pair 兼容判定 `head.n==coll.n+1` |
| `k 6` | — | ✓ | ✓ | ✓ | K32B 列坐标：B 同 k（pair 同列才能拼 N8×K16B）；AMX `k==last_k+1`（tile 覆盖连续 K4B；全局序号天然跨 K-outer）；BMX `kw_base=k&~(base_k-1)`（窗口 K 对齐，2 幂屏蔽） |
| `single 1` | — | ✓ | — | — | B 奇数 N 尾单飞标志（rdgen 预算，**替代 n_hw_count**；pair 不跨 N block 论证见 SEQ §14.1）；尾单发 2 块 = owner range + pad slot（`src+128`）mem-pad range（F-056 v2） |
| `m 1` | — | — | ✓ | — | AMX 同 m run 判定 |
| `span 3` | — | — | ✓ | ✓ | AMX `Σspan≤4` / chunk=8×span；BMX `base_k=4/span` / frag=4×span；advance=Σspan |
| `kgs 6` | — | — | ✓ | ✓ | AMX emit 重算 `rg_len`（tile-major 行组 stride）；BMX `rows=min(base_k, kgs−kw_base)`（K 尾截断） |
| `is_k_tail 1` | — | — | ✓ | — | AMX run 强制闭合条件 2（K 尾 → mem-pad，F-061） |
| `nblk_base/len 8/4` | — | — | — | ✓ | BMX 窗口键 / `expected=n_len×rows`（walker 现场几何经 token 注解） |
| `nhw2 8` | — | — | — | ✓ | BMX mem-pad 地址行 stride（N2 pair 量化布局，F-067） |
| **合计** | **62** | **77** | **79** | **97** | （另 +1b `is_end`，四路公共） |

选用理由（不对齐无代价）：A 展开全静态（满 key 恒 16×128B，
`block(cur)=src+cur*128`），k 只参与 rdgen 地址预算，故零注解；B 是
动态二元配对（判定=merge 规则本体），只需 `n/k/single`；AMX 是 K-run
连续 merge + tile-major stride 重算，需 `m/k/span/kgs/is_k_tail`；
BMX 是固定窗口累积（slot 位置由坐标序隐式确定，无需 pair 判定），需
窗口几何 `nblk_*/k/span/kgs/nhw2`，且**不带 n_idx**（到达序=坐标序=
FIFO 位置 j）。四路队列深度本就不同（16/8/128/4），各自独立例化，
统一宽度只会浪费寄存器（§4.1 payload 字段集按 lane 参数化展开）。

### 3.3 伪码

```python
def rdgen(m, domain, *, inputs=None, prefix="lfsm_rdg"):
    # ── Cycle 0 ──────────────────────────────────────────────
    rd_id = domain.signal(width=RD_ID_W, shape=[4], reset_value=0, name=f"{prefix}_rd_id")
    tok_* = submodule_input(...)      # §3.1
    rid   = tok_seq + 1               # rdgen_id（R-08；one-based，reuse 占号）
    # 地址生成（SEQ §6；小位宽乘法/shift-add，无除法器）
    a_lin   = tok_m * cfg_k_groups + tok_k                     # 1b×6b+6b
    a_src   = cfg_a_base + (a_lin << 11)                       # ×2048
    amx_src = cfg_amx_base + mux(tok_m, cfg_rg_len << 3, u(32,0)) + (tok_k * cfg_span << 3)
    b_lin   = tok_k * cfg_n_hw2 + tok_n                        # 5b×8b（n_hw2 pair 量化 stride，F-056 v2）
    b_src   = cfg_b_base + (b_lin << 7)                        # ×128
    bmx_src = cfg_bmx_base + ((tok_k * cfg_n_hw2 + tok_n) * cfg_span << 2)   # ×4*span
    c_src   = cfg_l0c_base + (((tok_m * cfg_n_hw) + tok_n) << 4)             # ×16
    new_a   = tok_valid & tok_fv_a
    new_amx = tok_valid & tok_fv_a & cfg_mx_en
    new_b   = tok_valid & tok_fv_b
    new_bmx = tok_valid & tok_fv_b & cfg_mx_en
    new_c   = tok_valid & tok_fv_c
    outs = dict(
        enq_a_valid=new_a,   enq_a_inst=cfg_inst, enq_a_rdgen=rid, enq_a_rd_id=rd_id[A], enq_a_src=a_src,
        enq_amx_valid=new_amx, enq_amx_...(含 span=cfg_span, kgs=cfg_k_groups,
                          is_k_tail=(tok_k == cfg_k_groups - 1)),
        enq_b_valid=new_b,  enq_b_...(含 single=((tok_n == cfg_n_hw - 1) & ~tok_n[0])),
        enq_bmx_valid=new_bmx, enq_bmx_...(含 span/kgs/nhw2/nblk_*),
        end_a=tok_done, end_amx=tok_done & cfg_mx_en,
        end_b=tok_done, end_bmx=tok_done & cfg_mx_en,      # required_lanes（F-024）
        c_enq_valid=new_c, c_enq_inst=cfg_inst, c_enq_rdgen=rid,
        c_enq_m=tok_m, c_enq_n=tok_n, c_enq_src=c_src)

    domain.next()
    # ── Cycle 1 ──────────────────────────────────────────────
    for l in range(4):
        rd_id[l].assign(u(RD_ID_W,0), when=start)               # instruction 开始清零（F-021）
        rd_id[l].assign(rd_id[l] + 1, when=enq_fire[l])         # 仅成功入队递增（F-021）
    # enq_fire[l] = 对应 enq_*_valid（入队无容量 gate，valid 即成功，R-07）
    # sva（F-023）：a/amx/b/bmx_src ∈ 对应 [base,limit]（limit 来自配置寄存，仅 sva）
    return outs
```

## 4. `rd_queue`（prefix `lfsm_q_{lane}`，×4 实例，内部 next=1）

### 4.1 参数与 inputs / outs

参数：`depth`（A16/AMX8/B128/BMX4）、`payload 字段集`（§3.2，按 lane）。
写入 **双口**（SEQ §7：RD + LaneLoadEnd 可同拍，≤2/拍）。

| in key | 位宽 | 语义 | 来源 |
| :--- | :--- | :--- | :--- |
| `enq_rd_valid` + payload… | §3.2 | rdgen entry | rdgen |
| `enq_end_valid` / `enq_end_inst` | 1/4 | LaneLoadEnd（is_end=1，仅占位） | rdgen |
| `pop` | 1 | assembler 消费（≤1/拍） | assembler（本 lane） |

| out key | 位宽 | 语义 | 去向 |
| :--- | :--- | :--- | :--- |
| `head_valid` / `head_is_end` | 1 | head 存在/类型 | assembler（本 lane） |
| `head_…` | §3.2 | head payload 各字段（RD 时有效） | assembler（本 lane） |
| `head1_valid` / `head1_is_end` / `head1_…` | 同上 | head+1 视图（第二组合读口；asm 次态视图用，见 §5.3 注②） | assembler（本 lane；B/AMX 使用） |
| `cnt` | log2(depth)+1 | 占用（never-full sva、idle） | lfsm_top（`o_lfsm_idle`） |

### 4.2 伪码

```python
def rd_queue(m, domain, *, inputs=None, depth=16, prefix="lfsm_q_a"):
    # ── Cycle 0 ──────────────────────────────────────────────
    PTR_W = log2(depth); CNT_W = PTR_W + 1
    is_end = domain.signal(width=1, shape=[depth], reset_value=0, name=f"{prefix}_is_end")
    # 每 payload 字段一个向量状态，如：
    f_inst = domain.signal(width=INST_ID_W, shape=[depth], reset_value=0, name=f"{prefix}_f_inst")
    # …（§3.2 全字段）
    head = domain.signal(width=PTR_W, reset_value=0, name=f"{prefix}_head")
    tail = domain.signal(width=PTR_W, reset_value=0, name=f"{prefix}_tail")
    cnt  = domain.signal(width=CNT_W, reset_value=0, name=f"{prefix}_cnt")
    enq_rd_valid = submodule_input(...); pop = submodule_input(...)  # …

    head_valid = cnt > 0
    head1_valid = cnt > 1
    outs = dict(head_valid=head_valid,
                head_is_end=vec_rd(is_end, head),
                head_inst=vec_rd(f_inst, head), …,   # 各字段 vec_rd
                head1_valid=head1_valid,
                head1_is_end=vec_rd(is_end, head + 1),
                head1_inst=vec_rd(f_inst, head + 1), …,   # head+1 各字段 vec_rd
                cnt=cnt)

    domain.next()
    # ── Cycle 1 ──────────────────────────────────────────────
    # 写口 0 = RD，写口 1 = END（END 恒在 RD 之后入队，SEQ §7）
    for i in range(depth):
        hit0 = enq_rd_valid & (tail == i)
        hit1 = enq_end_valid & ((tail + enq_rd_valid) == i)
        is_end[i].assign(0, when=hit0);  f_inst[i].assign(enq_rd_inst, when=hit0)  # …各字段
        is_end[i].assign(1, when=hit1);  f_inst[i].assign(enq_end_inst, when=hit1)
    head.assign(head + 1, when=pop)                       # PTR_W 自然回卷（2 幂）
    tail.assign(tail + enq_rd_valid + enq_end_valid, when=enq_rd_valid | enq_end_valid)
    cnt <<= cnt + enq_rd_valid + enq_end_valid - pop
    sva(cnt + enq_rd_valid + enq_end_valid - pop <= depth, "rdq never-full")   # F-032/A-011
    return outs
```

**无同拍 bypass（F-031）由存储相位保证**：head 直读寄存器，入队走
cycle-1 写 → 新 entry 次拍才可见。反压保持（F-113）：无 pop 时 head/
payload 不变（寄存器无写）。

## 5. `assembler_a`（prefix `lfsm_asm_a`，内部 next=1）

参数：`full_count=1, block_bytes=128`（§13 透传）。

### 5.1 inputs / outs

| in key | 位宽 | 语义 | 来源 |
| :--- | :--- | :--- | :--- |
| `head_valid/head_is_end/head_inst(4)/head_rdgen(14)/head_src(32)` | — | 队列 head | rd_queue（本 lane） |
| `fire_consume` | 1 | 本 lane candidate 本拍 fire | arbiter（经 top `fire_l`） |
| `dest_base` | 8 | writes 展开基址 | tag_checker |

| out key | 位宽/shape | 语义 | 去向 |
| :--- | :--- | :--- | :--- |
| `pop` | 1 | 队列消费（load 或 END） | rd_queue（本 lane） |
| `view_formable` | 1 | visible≥1（SEQ §9） | cand_holder |
| `view_inst` / `view_rd_mem_id` | 4/14 | candidate 键 | cand_holder |
| `view_advance` | 6 | 本 candidate 新增分配 | cand_holder |
| `view_group_final` | 1 | group 末笔标志 | tag_checker、§11A mux |
| `view_is_last` | 1 | instruction 末笔 | §11A mux（lfsm_top） |
| `view_load/valid/pad` | 8×3 | 字节账目（128/128/0） | §11A mux（lfsm_top） |
| `view_src_addr` / `view_src_len` | 32×[32] / 8×[32] + `view_src_cnt` 6 | src ranges（A 恒 cnt=1；向量 CAS） | §11A mux（lfsm_top） |
| `view_wr_index` / `view_wr_offset` / `view_wr_len` / `view_wr_cnt` | 8/11/8 ×[32] + 6 | writes（A 恒 1 项） | §11A mux（lfsm_top） |
| `view_next_formable` / `view_next_*`（标量组） | — | 次态视图（cand_holder replacement 用，PIPE §4） | cand_holder |
| `ctx_empty` | 1 | emit 无效（idle） | lfsm_top（`o_lfsm_idle`） |

### 5.2 伪码

```python
def assembler_a(m, domain, *, inputs=None, prefix="lfsm_asm_a",
                full_count=1, block_bytes=128):
    # ── Cycle 0 ──────────────────────────────────────────────
    e_v    = domain.signal(width=1,  reset_value=0, name=f"{prefix}_e_v")
    e_inst = domain.signal(width=4,  reset_value=0, name=f"{prefix}_e_inst")
    e_rdg  = domain.signal(width=14, reset_value=0, name=f"{prefix}_e_rdgen")
    e_src  = domain.signal(width=32, reset_value=0, name=f"{prefix}_e_src")
    cur    = domain.signal(width=4,  reset_value=0, name=f"{prefix}_cur")   # 0..15
    end_v   = domain.signal(width=1, reset_value=0, name=f"{prefix}_end_v")
    end_ins = domain.signal(width=4, reset_value=0, name=f"{prefix}_end_inst")
    # inputs（§5.1）…

    head_rd  = head_valid & ~head_is_end
    load     = ~e_v & head_rd                     # emit 空 → head 直入视图（chain）
    end_pop  = head_valid & head_is_end           # A：END 随时可 pop（SEQ §8.6）
    pop      = load | end_pop
    formable = e_v | load
    v_cur    = mux(e_v, cur, u(4,0))
    v_src    = mux(e_v, e_src, head_src)
    v_inst   = mux(e_v, e_inst, head_inst)
    v_rdg    = mux(e_v, e_rdg, head_rdgen)
    # block 视图：默认序 EU_M_HALF_K_HALF → src = v_src + cur*128（F-050；非默认序 gap）
    block_addr = v_src + (v_cur << 7)
    advance    = mux(v_cur == 0, u(6,1), u(6,0))
    gfinal     = v_cur == 15
    is_last    = end_v & (v_inst == end_ins) & gfinal      # tag 式 end（SEQ §8.6）
    # writes（dest_base 来自 tag_checker；split 时 dest_base=grp_base）
    wr0_idx    = dest_base
    wr0_off    = v_cur << 7                         # BYTE_OFF_W=11
    # 次态视图（供 cand_holder replacement）：复用同一组合函数，输入为次态（§5.3 注②）
    nv_v, nv_cur, nv_src, nv_inst, nv_rdg = next_ctx(...)
    view_next_formable = nv_v | head_rd   # A 特例：~nv_v ⟹ 本拍无 pop（注③），head 即次态 head
    outs = dict(pop=pop, view_formable=formable, view_inst=v_inst, view_rd_mem_id=v_rdg,
                view_advance=advance, view_group_final=gfinal, view_is_last=is_last,
                view_load=u(8,128), view_valid=u(8,128), view_pad=u(8,0),
                view_src_cnt=u(6,1),
                view_src_addr=vec1(block_addr), view_src_len=vec1(u(8,128)),
                view_wr_cnt=u(6,1), view_wr_index=vec1(wr0_idx),
                view_wr_offset=vec1(wr0_off), view_wr_len=vec1(u(8,128)),
                view_next_formable=view_next_formable, view_next_inst=..., …,
                ctx_empty=~e_v)

    domain.next()
    # ── Cycle 1 ──────────────────────────────────────────────
    fire_load  = fire_consume & ~e_v                # 从 head 直接 fire（chain）
    fire_emit  = fire_consume & e_v
    e_v.assign(1, when=fire_load | (load & ~fire_consume) | (fire_emit & (cur < 15)))
    e_v.assign(0, when=fire_emit & (cur == 15))
    e_inst.assign(head_inst, when=fire_load | (load & ~fire_consume))
    e_rdg.assign(head_rdgen,  when=fire_load | (load & ~fire_consume))
    e_src.assign(head_src,    when=fire_load | (load & ~fire_consume))
    cur.assign(u(4,1), when=fire_load)
    cur.assign(cur + 1,  when=fire_emit & (cur < 15))
    cur.assign(u(4,0), when=load & ~fire_consume)
    # end tag（SEQ §8.6）：END pop 时装载，不清零（下一条 END 覆盖）
    end_v.assign(1, when=end_pop)
    end_ins.assign(head_inst, when=end_pop)
    return outs
```

注②（view_next 构造约定，§5–§8 共用）：`view_next_*` = **同一组合视图
函数**作用于「次态 context + 次态 queue head」；`next_ctx()` 为
cycle-1 次态的组合函数副本（同一规则写两遍：赋值语句 + 次态函数；
实现时用内部辅助函数避免漂移）。次态 queue head = 本拍 pop 时的
**head+1 视图**（rd_queue `head1_*` 第二组合读口），否则为 head。
注③（A 特例）：A 的 `~nv_v` 仅在 `fire & cur==15`（退役）时出现，
该拍 `load` 不成立（`e_v=1`）→ 无 pop → 当前 head 即次态 head，无需
head1 读口。B/AMX 的次态视图需 head1（emit 退役与 coll_load 可同拍）；
BMX 的次态视图仅依赖窗口池状态，无需 queue head。
`sva`：fire 且 advance>0 时 dest_base==load_ptr（在 tag_checker 侧）；
`is_partial≡0`（D-003）。

## 6. `assembler_b`（prefix `lfsm_asm_b`，内部 next=1）

参数：`full_count=1, block_bytes=128`（§13 透传）。

### 6.1 inputs / outs（差异项）

in 增：`head_n(8)/head_k(6)/head_single(1)`（来源同 §5.1：rd_queue 本
lane）；out 结构同 §5.1（B 几何；去向亦同 §5.1：`pop`→rd_queue、
`view_*` 标量→cand_holder/tag_checker、元数据视图→§11A mux、
`ctx_empty`→lfsm_top）。
状态：coll 槽 + emit 槽（SEQ §8.3）。

### 6.2 伪码

```python
    # ── Cycle 0 ──────────────────────────────────────────────
    # 状态：c_v/c_inst/c_rdg/c_src/c_n/c_k；e_v/e_inst/e_rdg/e_src0/e_src1/e_single/e_half；
    #       end_v/end_ins（end tag，同 §5.2）
    head_rd  = head_valid & ~head_is_end
    compat   = c_v & head_rd & (head_inst == c_inst) & (head_k == c_k) & (head_n == c_n + 1)
    sva(~(c_v & head_rd & ~compat), "B merge: incompatible RD before N tail")  # 合法走法不可达
    complete_pair   = compat & ~e_v
    complete_single = ~c_v & head_rd & head_single & ~e_v
    coll_load       = ~c_v & head_rd & ~head_single           # 与 emit 忙闲无关
    end_pop = head_valid & head_is_end
    sva(~(end_pop & c_v), "B LaneLoadEnd with open pair")     # SEQ §8.6
    pop = complete_pair | complete_single | coll_load | end_pop
    formable = e_v | complete_pair | complete_single
    v_half   = mux(e_v, e_half, u(1,0))
    v_src0   = mux(e_v, e_src0, mux(complete_pair, c_src, head_src))
    v_src1   = mux(e_v, e_src1, head_src)
    v_single = mux(e_v, e_single, complete_single)
    v_inst   = mux(e_v, e_inst, mux(complete_pair, c_inst, head_inst))
    v_rdg    = mux(e_v, e_rdg, mux(complete_pair, c_rdg, head_rdgen))   # merge 取最早（R-18）
    # block 视图：pair 两 range 各 64B；single = owner range + pair-completion
    # mem-pad range（pad slot = v_src0+128，实存随读、计 valid 不写 buffer，F-056 v2）
    addr0 = v_src0 + (v_half << 6); addr1 = v_src1 + (v_half << 6)
    pad_addr = v_src0 + 128 + (v_half << 6)
    src_cnt = u(6,2)                                   # pair/single 恒 2 range（single 次 range 为 mem-pad）
    valid_b = u(8,128); pad_b = u(8,0)                 # mem-pad 计 valid，B 无 transport padding
    advance = mux(v_half == 0, mux(v_single, u(6,1), u(6,2)), u(6,0))
    gfinal  = v_half == 1
    is_last = end_v & (v_inst == end_ins) & gfinal
    # writes：pair 两项 (dest_base+i, half*64, 64)；single 一项 (dest_base, half*64, 64)
    wr0 = (dest_base, v_half << 6, 64)
    wr1 = (ring_add(dest_base, 1, DEPTH_B), v_half << 6, 64)
    # 次态视图：next_ctx() 组合副本 + head1 视图（§5.3 注②；emit 退役与
    # coll_load 可同拍，故 complete_pair'/complete_single' 需 head1 判定）
    outs = dict(pop=pop, view_formable=formable, …, ctx_empty=~e_v & ~c_v)

    domain.next()
    # ── Cycle 1 ──────────────────────────────────────────────
    from_inc = fire_consume & ~e_v                     # incoming 直接 fire（chain）
    e_v.assign(1, when=(from_inc | complete_pair | complete_single) & ~(fire_consume & (v_half == 1)))
    e_v.assign(0, when=fire_consume & e_v & (e_half == 1))
    e_half.assign(u(1,1), when=fire_consume & (v_half == 0))
    e_half.assign(u(1,0), when=(complete_pair | complete_single) & ~fire_consume)
    # 装载字段（incoming fire 与未 fire 装载共用 when）
    load_e = from_inc | ((complete_pair | complete_single) & ~fire_consume)
    e_inst.assign(v_inst, when=load_e); e_rdg.assign(v_rdg, when=load_e)
    e_src0.assign(v_src0, when=load_e); e_src1.assign(v_src1, when=load_e)
    e_single.assign(v_single, when=load_e)
    c_v.assign(1, when=coll_load)
    c_v.assign(0, when=complete_pair)            # coll 仅经 complete_pair 清空；emit 退役不动 coll
    c_inst.assign(head_inst, when=coll_load); c_rdg.assign(head_rdgen, when=coll_load)
    c_src.assign(head_src, when=coll_load)
    c_n.assign(head_n, when=coll_load);   c_k.assign(head_k, when=coll_load)
    end_v.assign(1, when=end_pop)
    end_ins.assign(head_inst, when=end_pop)
    return outs
```

优先级（F-111）：`fire_consume`（退役/推进）> `complete_*`（最老
pair 移交）> `coll_load`（新工作）；未 fire 时 emit/coll 字段无赋值
路径 → 保持（F-113）。

## 7. `assembler_amx`（prefix `lfsm_asm_amx`，内部 next=1）

参数：`full_count=4, block_bytes=32`（§13 透传）。

### 7.1 状态与要点

run 槽（≤4 key，SEQ §8.4）+ emit 槽（闭合 run 副本 + rg∈{0,4}）。
in 增：`head_m(1)/head_k(6)/head_span(3)/head_kgs(6)/head_is_k_tail(1)`
（来源同 §5.1：rd_queue 本 lane）；out 结构/去向同 §5.1。

### 7.2 伪码

```python
    # ── Cycle 0 ──────────────────────────────────────────────
    # run 状态：r_cnt(3) r_inst r_m r_span(3) r_kgs(6) r_sum(3) r_closed r_last_k(6)
    #           r_src[4](向量 32b) r_rdg[4](向量 14b)
    # emit 状态：e_v e_inst e_rdg e_cnt(3) e_span(3) e_rglen(11) e_srcs[4] e_rg(3)
    # end tag：end_v/end_ins（同 §5.2）
    head_rd = head_valid & ~head_is_end
    app_ok  = head_rd & ~r_closed & (
                (r_cnt == 0) |
                ((head_inst == r_inst) & (head_m == r_m) &
                 (head_k == r_last_k + 1) & (r_sum + head_span <= 4)))
    sva(~(head_rd & (r_cnt != 0) & ~r_closed & ~app_ok & (r_sum < 4)),
        "AMX merge: incompatible RD before K tail")           # 合法走法不可达（SEQ §8.4）
    close_now = app_ok & ((r_sum + head_span == 4) | head_is_k_tail)
    transfer  = r_closed & ~e_v                               # 已闭合、emit 空
    close_chain = close_now & ~e_v                            # 本拍闭合 chain 进视图
    end_pop = head_valid & head_is_end
    sva(~(end_pop & (r_cnt != 0) & ~r_closed), "AMX LaneLoadEnd with open run")
    pop = app_ok | end_pop
    formable = e_v | transfer | close_chain
    # 视图 keys 集合：emit 态=e_srcs；transfer=r_src；close_chain=r_src∪{head}
    v_cnt  = mux(e_v, e_cnt, mux(transfer, r_cnt, r_cnt + 1))
    v_span = mux(e_v, e_span, mux(close_chain & (r_cnt == 0), head_span, r_span))
    v_kgs  = mux(e_v, e_kgs,  mux(transfer | (r_cnt != 0), r_kgs, head_kgs))
    v_rg   = mux(e_v, e_rg, u(3,0))
    v_rglen = mux(e_v, e_rglen, rg_len_of(v_kgs, v_span))     # ((k*s+3)>>2)<<5
    v_inst = mux(e_v, e_inst, mux(transfer | (r_cnt != 0), r_inst, head_inst))
    v_rdg  = mux(e_v, e_rdg, mux(transfer | (r_cnt != 0), r_rdg[0], head_rdgen))
    v_srcs = mux(e_v, e_srcs, run_srcs_with_head)             # 向量拼接
    kpt    = keys_per_tile_of(v_span)                         # 4/span
    # 4 tile 展开（r = v_rg..v_rg+3；每 tile kpt 个 chunk，chunk 字节 = 8*span）
    for r in range(4):                                        # Python 静态展开
        rr = v_rg + r
        for j in range(4):                                    # kpt≤4
            real = j < v_cnt
            frag_addr[r][j] = mux(real, v_srcs[j] + rr * v_rglen,
                                        v_srcs[0] + j * (v_span << 3) + rr * v_rglen)
            frag_len[r][j]  = v_span << 3                     # 8*span
            frag_en[r][j]   = j < kpt
    # 字节账目：每 tile valid=32（mem-pad 计入），pad=0（F-061；AMX 无 transport padding）
    advance = mux(v_rg == 0, v_cnt * v_span, u(6,0))
    gfinal  = v_rg == 4
    is_last = end_v & (v_inst == end_ins) & gfinal
    # src ranges：Σ tile Σ chunk（frag_en）→ ≤16 项展平（A-003 ≤32 sva）
    # writes：tile r 的实 chunk j → tag t = j（owner j 占 span… 见 SEQ §10.1）：
    #   wr_index=(dest_base + j*1… 注：tag 序号 = chunk 位 t（0..3），t < v_cnt*v_span 才写
    #   wr_offset = rr*8, wr_len=8；每 candidate ≤16 项
    # 次态视图：next_ctx() 组合副本 + head1 视图（§5.3 注②）
    outs = dict(pop=pop, view_formable=formable, …, ctx_empty=~e_v & (r_cnt == 0))

    domain.next()
    # ── Cycle 1 ──────────────────────────────────────────────
    # run append（与 emit 推进独立；SEQ §8.4 独立槽）
    r_src[r_cnt].assign(head_src, when=app_ok)                # vec_wr 展开
    r_rdg[r_cnt].assign(head_rdgen, when=app_ok)
    r_cnt.assign(r_cnt + 1, when=app_ok)
    r_sum.assign(r_sum + head_span, when=app_ok)
    r_last_k.assign(head_k, when=app_ok)
    r_closed.assign(1, when=close_now)
    r_inst.assign(head_inst, when=app_ok & (r_cnt == 0))      # 开 run 装载
    r_m.assign(head_m, when=app_ok & (r_cnt == 0))
    r_span.assign(head_span, when=app_ok & (r_cnt == 0))
    r_kgs.assign(head_kgs, when=app_ok & (r_cnt == 0))
    # run → emit 移交（transfer/close_chain；fire 时 rg 直接到 4）
    load_e = (transfer | close_chain)                         # 含 fire 与未 fire
    e_v.assign(1, when=load_e & ~(fire_consume & (v_rg == 4)))
    e_v.assign(0, when=fire_consume & e_v & (e_rg == 4))
    e_rg.assign(u(3,4), when=fire_consume & load_e)
    e_rg.assign(u(3,0), when=load_e & ~fire_consume)
    e_rg.assign(e_rg + 4, when=fire_consume & e_v & (e_rg == 0))
    e_inst.assign(v_inst, when=load_e); e_rdg.assign(v_rdg, when=load_e)
    e_cnt.assign(v_cnt, when=load_e);  e_span.assign(v_span, when=load_e)
    e_rglen.assign(v_rglen, when=load_e)
    e_srcs.assign(v_srcs, when=load_e)                        # 向量整体
    r_cnt.assign(u(3,0), when=load_e)                         # run 清空（多赋值后者优先，§0）
    r_closed.assign(0, when=load_e)
    r_sum.assign(u(3,0), when=load_e)
    end_v.assign(1, when=end_pop)
    end_ins.assign(head_inst, when=end_pop)
    return outs
```

## 8. `assembler_bmx`（prefix `lfsm_asm_bmx`，内部 next=1）

参数：`full_count=4, block_bytes=32`（§13 透传）。

### 8.1 状态与要点

窗口池 2 槽（A-002）：`w_v/w_complete/w_inst/w_rdg0/w_nbase(8)/w_nlen(4)/
w_rows(3)/w_span(3)/w_nhw2(8)/w_kwbase(6)/w_cnt(6)/w_expected(6)/
w_srcs[32]` ×2 + `coll(1b)` + `drain(1b)` + end_v/end_ins。收集串行、
完成按序；**收集指针 `coll`** 指向当前收集槽（完成拍翻转）、
**drain 指针 `drain`** 指向下一个待 fire 的完成槽（fire 拍翻转）——
两指针各自交替即保证「完成序 = fire 序」（SEQ §8.5；sva 校验窗口
完成顺序）。
in 增：`head_span(3)/head_kgs(6)/head_nhw2(8)/head_nblk_base(8)/
head_nblk_len(4)/head_k(6)`（来源同 §5.1：rd_queue 本 lane）；
out 结构/去向同 §5.1。

### 8.2 伪码

```python
    # ── Cycle 0 ──────────────────────────────────────────────
    W = lambda i: slot(i)                                     # 槽视图别名
    head_rd  = head_valid & ~head_is_end
    base_k_hd = base_k_of(head_span)                          # 4/span
    kw_hd     = head_k & ~(base_k_hd - 1)                     # shift-mask
    cur  = W(coll)
    open_ok  = head_rd & ~cur.w_v
    match    = head_rd & cur.w_v & ~cur.w_complete &
               (head_nblk_base == cur.w_nbase) & (kw_hd == cur.w_kwbase)
    sva(~(head_rd & cur.w_v & ~cur.w_complete & ~match), "BMX window key mismatch")
    append   = open_ok | match
    rows_hd     = min2(base_k_hd, head_kgs - kw_hd)           # K 尾截断（SEQ §8.5）
    expected_hd = head_nblk_len * rows_hd                     # ≤8×4=32
    complete_now = append & (mux(open_ok, u(6,0), cur.w_cnt) + 1 ==
                             mux(open_ok, expected_hd, cur.w_expected))
                             # open_ok 拍 w_cnt 视为 0（槽内为上一窗残留，open 时覆盖）
    emit_sel = (W(drain).w_v & W(drain).w_complete) ? drain : (drain ^ 1)
    emit_ok  = W(emit_sel).w_v & W(emit_sel).w_complete
    ev = W(emit_sel)
    end_pop = head_valid & head_is_end
    sva(~(end_pop & cur.w_v & ~cur.w_complete), "BMX LaneLoadEnd with incomplete window")
    pop = append | end_pop
    formable = emit_ok
    # 4-block 展开（SEQ §8.5；Python 静态展开 b∈0..3, r∈0..3, s∈0..1）
    for b in range(4):
        bucket_live = (2 * b) < ev.w_nlen
        for r in range(4):                                    # r<base_k(ev.w_span)
            for s in range(2):
                j      = r * ev.w_nlen + 2 * b + s
                real   = bucket_live & ((2*b + s) < ev.w_nlen) & (r < ev.w_rows) & (r < base_k_of(ev.w_span))
                pad    = bucket_live & ~real & (r < base_k_of(ev.w_span))
                f_addr[b][r][s] = mux(real, ev.w_srcs[j],
                                          ev.w_srcs[2*b] + ((r * ev.w_nhw2 + s) * ev.w_span << 2))
                f_en[b][r][s]   = real | pad                  # mem-pad 进 src ranges
    # 字节账目：Σ real/pad；空 bucket → padding-only block（valid=0,pad=32）
    advance  = ev.w_cnt * ev.w_span                           # ≤32（A-003 sva）
    gfinal   = u(1,1)                                         # BMX 单 candidate 一窗（D-004）
    is_last  = end_v & (ev.w_inst == end_ins) &
               ~(W(emit_sel ^ 1).w_v & (W(emit_sel ^ 1).w_inst == ev.w_inst))
               # 池中无同 inst 的其它窗口（SEQ §8.6 tag 式判定）
    # writes：real owner j（j<w_cnt）逐 span：(dest_base + j*span + s, 0, 4)，共 advance 项
    outs = dict(pop=pop, view_formable=formable,
                view_inst=ev.w_inst, view_rd_mem_id=ev.w_rdg0,
                view_advance=advance, …, ctx_empty=~(W(0).w_v | W(1).w_v))

    domain.next()
    # ── Cycle 1 ──────────────────────────────────────────────
    # fire：释放 emit 槽（整窗一笔消费），drain 翻转
    W(emit_sel).w_v.assign(0, when=fire_consume & emit_ok)
    drain.assign(drain ^ 1, when=fire_consume & emit_ok)
    # append / open
    for i in range(2):
        hit = append & (coll == i)
        W(i).w_srcs[W(i).w_cnt].assign(head_src, when=hit)    # vec_wr；写位置=当前 w_cnt（SEQ §14.1）
        W(i).w_cnt.assign(mux(open_ok, u(6,1), W(i).w_cnt + 1), when=hit)
        W(i).w_v.assign(1, when=hit)
        W(i).w_complete.assign(0, when=hit & open_ok)         # 清上一窗残留
        W(i).w_complete.assign(1, when=hit & complete_now)    # 后者优先（§0）
        # open 装载键寄存（open_ok 拍）
        W(i).w_inst.assign(head_inst, when=hit & open_ok)
        W(i).w_rdg0.assign(head_rdgen, when=hit & open_ok)
        W(i).w_nbase.assign(head_nblk_base, when=hit & open_ok)
        W(i).w_nlen.assign(head_nblk_len, when=hit & open_ok)
        W(i).w_rows.assign(rows_hd, when=hit & open_ok)
        W(i).w_span.assign(head_span, when=hit & open_ok)
        W(i).w_nhw2.assign(head_nhw2, when=hit & open_ok)
        W(i).w_kwbase.assign(kw_hd, when=hit & open_ok)
        W(i).w_expected.assign(expected_hd, when=hit & open_ok)
    coll.assign(coll ^ 1, when=complete_now)                  # 完成后切收集槽
    end_v.assign(1, when=end_pop)
    end_ins.assign(head_inst, when=end_pop)
    # 池满（两槽 w_v 且收集槽 complete 后需第三槽）→ 停止 pop（append 不成立自然保持）；
    # sva never-need-3rd（A-011 包络）：complete_now 时 W(coll^1).w_v 必为 0 或本拍释放
    return outs
```

## 9. `cand_holder`（prefix `lfsm_chd_{lane}`，×4 同构，内部 next=1；对应规格 BandwidthPacker 的 candidate 持有职能）

> 命名说明（2026-10-14 用户决策）：`packer` 改名 `cand_holder`，直观
> 体现其职责——held candidate 的持有/形成/递补 + `cand_seq` +
> `planned_*` 锁存。规格 BandwidthPacker（SRC-01 sec 10）的职能在本
> 设计中由两部分承担：满宽/可见块判定与块展开在 assembler（emit-on-
> demand 视图），candidate 的寿命管理在本模块。

**参数**：除 `prefix` 外**无几何参数**——`formable` 判定
（`visible ≥ full_count`）与字节账目在各 assembler 内完成
（`full_count/block_bytes` 配给 assembler，见 §13），cand_holder 只做
held/seq/planned 管理，这是四路能完全同构的原因。位宽全部为
types.py 全局常量（四路一致，非 per-lane 配置）。

**边3 严格流水（2026-10-14 用户决策，规格偏差登记 A-013 预登记）**：
仲裁/分配输入只认 **held 快照寄存**——fresh candidate 形成拍不旁路进
arbiter/tag_checker，仅驱动拍末 held 捕获，**次拍起**参与仲裁
（链首 +1 拍）；fire 后递补（replacement）同拍捕获、次拍可再 fire，
连发节奏保持每拍 1 fire。held 快照一致性不变量：held valid 时本拍
asm 视图 == held 内容（context 至 fire 前不推进，F-113）——payload
mux 元数据与获选 candidate 恒一致（sva）。

### 9.1 inputs / outs

| in key | 位宽 | 语义 | 来源 |
| :--- | :--- | :--- | :--- |
| `view_formable/view_inst(4)/view_rd_mem_id(14)/view_advance(6)` | — | asm 当前视图 | assembler（本 lane） |
| `view_next_formable/view_next_*` | 同上 | asm 次态视图 | assembler（本 lane） |
| `load_ptr` | 8 | 本 lane load_ptr（fresh/保持锁存源） | tag_checker |
| `load_ptr_post` | 8 | 本 lane fire 后的 load_ptr 次态值（replacement 锁存源） | tag_checker |
| `fire_consume` | 1 | 本 lane fire | arbiter（经 top `fire_l`） |

| out key | 位宽 | 语义 | 去向 |
| :--- | :--- | :--- | :--- |
| `cand_valid` | 1 | held.valid（**present = held Q**；fresh 不旁路，拍末入 held，链首 +1 拍） | tag_checker、arbiter、lfsm_top（idle） |
| `cand_inst` / `cand_rd_mem_id` | 4/14 | 优先键 | arbiter（ballot）、§11A mux |
| `cand_seq` | 13 | per-lane、instruction 首 candidate 清零（D-005） | §11A mux |
| `cand_planned_base` / `cand_planned_advance` | 8/6 | 锁存 planned | tag_checker |

### 9.2 伪码（统一 held 规则，SEQ §9/§14.3）

```python
def cand_holder(m, domain, *, inputs=None, prefix="lfsm_chd_a"):
    # ── Cycle 0 ──────────────────────────────────────────────
    h_v   = domain.signal(width=1,  reset_value=0, name=f"{prefix}_h_v")
    h_ins = domain.signal(width=4,  reset_value=0, name=f"{prefix}_h_inst")
    h_rid = domain.signal(width=14, reset_value=0, name=f"{prefix}_h_rid")
    h_seq = domain.signal(width=13, reset_value=0, name=f"{prefix}_h_seq")
    h_pb  = domain.signal(width=8,  reset_value=0, name=f"{prefix}_h_pb")
    h_pa  = domain.signal(width=6,  reset_value=0, name=f"{prefix}_h_pa")
    cseq  = domain.signal(width=13, reset_value=0, name=f"{prefix}_cand_seq")
    linst = domain.signal(width=4,  reset_value=0, name=f"{prefix}_lane_inst")
    # inputs（§9.1）…

    fresh    = ~h_v & view_formable              # 本拍形成（仅驱动拍末 held 捕获，不进入仲裁）
    new_inst = view_inst != linst                  # fresh candidate 属新 instruction
    seq_fresh = mux(new_inst, u(13,0), cseq)
    # 边3 严格流水：present = held Q（仲裁快照）。fresh 不旁路进arbiter/tck，
    # 拍末捕获入 held，次拍起参与仲裁——见 §9 头注（链首 +1 拍）。
    present_v   = h_v
    present_ins = h_ins
    present_rid = h_rid
    present_seq = h_seq
    present_pb  = h_pb
    present_pa  = h_pa
    outs = dict(cand_valid=present_v, cand_inst=present_ins, cand_rd_mem_id=present_rid,
                cand_seq=present_seq, cand_planned_base=present_pb,
                cand_planned_advance=present_pa)

    domain.next()
    # ── Cycle 1（held' = formable(view(ctx')) ? scalars(view(ctx')) : INVALID）──
    repl     = fire_consume & view_next_formable          # replacement 形成
    repl_new_inst = view_next_inst != mux(fresh, view_inst, linst)
    seq_ctr_fresh = mux(new_inst, u(13,1), cseq + 1)      # fresh 形成后的计数器
    h_v.assign(1, when=view_next_formable & (fire_consume | ~h_v))   # 见注④
    h_v.assign(0, when=fire_consume & ~view_next_formable)
    h_ins.assign(view_next_inst, when=view_next_formable)
    h_rid.assign(view_next_rd_mem_id, when=view_next_formable)
    # planned_base：replacement 锁存 **fire 后** load_ptr_post（golden commit
    # 先 advance 再 form_candidate，SEQ §9）；fresh 锁存当前 load_ptr；
    # 保持分支不重写（held 期间 load_ptr 不变，值自洽）
    h_pb.assign(mux(view_next_advance > 0, load_ptr_post, u(8,0)), when=repl)
    h_pb.assign(mux(view_advance > 0, load_ptr, u(8,0)), when=~fire_consume & ~h_v & view_next_formable)
    h_pa.assign(view_next_advance, when=repl)
    h_pa.assign(view_advance,      when=~fire_consume & ~h_v & view_next_formable)
    h_seq.assign(mux(repl_new_inst, u(13,0),
                     mux(fresh, seq_ctr_fresh, cseq)),    when=repl)
    h_seq.assign(seq_fresh, when=~fire_consume & fresh & view_next_formable)
    cseq.assign(mux(repl_new_inst, u(13,1),
                    mux(fresh, seq_ctr_fresh, cseq) + 1), when=repl)   # 无 fresh 时仅 +1
    cseq.assign(seq_ctr_fresh, when=fresh & ~repl)
    linst.assign(view_next_inst, when=repl)
    linst.assign(view_inst, when=fresh & ~repl)
    return outs
```

注④：`h_v` 两规则：fire 且无 replacement → 清 0；`view_next_formable`
且（fire 或原本无 held）→ 置 1；`~fire & h_v & view_next_formable`
（保持）无赋值路径 → 保持（字段同值亦不重写，F-113）。
`planned_base` 锁存规则（A-004/F-073）：replacement 用 `load_ptr_post`
（fire 后次态指针——被 fire 的 candidate 可能本拍推进了 load_ptr，
如 BMX 窗口连发）；fresh/保持用 `load_ptr`；advance==0 时锁 0
（query valid=0 不查 destination）。

## 10. `tag_checker`（prefix `lfsm_tck`，内部 next=1；对应规格 DestinationAllocator，SRC-01 sec 11）

> 命名说明：本模块即规格的 DestinationAllocator；改名 `tag_checker`
> 以直观体现其对外职能——经 `o_load_range_query` 查询 Buf/RAM tag
> 状态、以 `i_load_range_idle` 判定 `destination_ok`（另承担
> load_ptr ring / allocation group / `LoadPtrUpdate` 提交）。

### 10.1 inputs / outs

| in key | 位宽/shape | 语义 | 来源 |
| :--- | :--- | :--- | :--- |
| `cand_valid/cand_planned_base(8)/cand_planned_advance(6)` ×4 | 标量 ×4 lane | cand_holder present | cand_holder（4 路） |
| `view_group_final` ×4 | 1 ×4 | group 末笔标志 | assembler（4 路） |
| `i_load_range_idle` | 1 × `shape=[4]` | Buf/RAM 组合回答（PORT_LIST §5.2） | Buf/RAM（外部端口） |
| `fire` / `grant_lane` | 1/2 | grant 与获选 lane | arbiter |

| out key | 位宽/shape | 语义 | 去向 |
| :--- | :--- | :--- | :--- |
| `o_load_range_query_valid` / `_base` / `_advance` | 1/8/6 × `shape=[4]` | A-004 相位契约 | Buf/RAM（外部端口） |
| `dest_ok` ×4 | 1 ×4 | destination 可分配 | arbiter |
| `dest_base(8)` ×4 | 8 ×4 | writes/tag_range 基址 | assembler（4 路，writes 基址）、§11A mux（tag_range_base） |
| `tag_cnt(6)` ×4 | 6 ×4 | tag_range 长度 | §11A mux |
| `load_ptr` ×4 | 8 ×4 | 当前 load_ptr（观测/锁存源） | cand_holder |
| `load_ptr_post` ×4 | 8 ×4 | fire 后 load_ptr 次态（replacement 锁存用，§9） | cand_holder |
| `o_load_ptr_update_valid` / `_lane(2)` / `_old_ptr(8)` / `_new_ptr(8)` / `_advance(6)` | — | LoadPtrUpdate 载荷 | §11A（与 request 同组入 req_sched）→ Buf/RAM（外部端口） |

### 10.2 伪码

```python
    # ── Cycle 0 ──────────────────────────────────────────────
    load_ptr = domain.signal(width=8, shape=[4], reset_value=0, name=f"{prefix}_load_ptr")
    grp_open = domain.signal(width=1, shape=[4], reset_value=0, name=f"{prefix}_grp_open")
    grp_base = domain.signal(width=8, shape=[4], reset_value=0, name=f"{prefix}_grp_base")
    grp_cnt  = domain.signal(width=6, shape=[4], reset_value=0, name=f"{prefix}_grp_cnt")
    # per lane l：
    q_v[l]  = cand_valid[l] & (cand_planned_advance[l] > 0)
    q_base[l] = mux(q_v[l], cand_planned_base[l], load_ptr[l])
    q_adv[l]  = mux(q_v[l], cand_planned_advance[l], u(6,0))
    dest_ok[l]   = mux(q_v[l], i_load_range_idle[l], u(1,1))   # valid=0 外部必答 1（A-004）
    dest_base[l] = mux(cand_planned_advance[l] > 0, cand_planned_base[l], grp_base[l])
    tag_cnt[l]   = mux(cand_planned_advance[l] > 0, cand_planned_advance[l], grp_cnt[l])
    g = grant_lane
    upd_v = fire & (cand_planned_advance[g] > 0)
    sva(~upd_v | (cand_planned_base[g] == load_ptr[g]), "planned_base != load_ptr")
    # fire 后 load_ptr 次态（供 cand_holder replacement 的 planned_base 锁存，§9）
    load_ptr_post[l] = mux(fire & (g == l) & (cand_planned_advance[l] > 0),
                           ring_add(load_ptr[l], cand_planned_advance[l], DEPTH[l]),
                           load_ptr[l])
    outs = dict(o_load_range_query_valid=vec4(q_v), o_load_range_query_base=vec4(q_base),
                o_load_range_query_advance=vec4(q_adv), dest_ok=…, dest_base=…, tag_cnt=…,
                load_ptr=load_ptr, load_ptr_post=…,
                o_load_ptr_update_valid=upd_v, o_load_ptr_update_lane=g,
                o_load_ptr_update_old_ptr=cand_planned_base[g],
                o_load_ptr_update_new_ptr=ring_add(cand_planned_base[g],
                                                   cand_planned_advance[g], DEPTH[g]),
                o_load_ptr_update_advance=cand_planned_advance[g])

    domain.next()
    # ── Cycle 1 ──────────────────────────────────────────────
    for l in range(4):
        me = fire & (g == l)
        load_ptr[l].assign(ring_add(load_ptr[l], cand_planned_advance[l], DEPTH[l]),
                           when=me & (cand_planned_advance[l] > 0))
        grp_base[l].assign(cand_planned_base[l], when=me & (cand_planned_advance[l] > 0))
        grp_cnt[l].assign(cand_planned_advance[l], when=me & (cand_planned_advance[l] > 0))
        grp_open[l].assign(1, when=me & (cand_planned_advance[l] > 0))
        grp_open[l].assign(0, when=me & view_group_final[l])     # 同拍 open+close→0（BMX，D-004）
        sva(~(me & (cand_planned_advance[l] > 0) & grp_open[l]),
            "group leak: open while open")                        # D-004 单 open 不变量
            # （新 group 开启时旧 group 必已关闭：A cur15/B half1/AMX rg4 先行 fire，
            #  BMX 上笔 fire 同拍 open+close 后 grp_open==0）
    return outs
```

## 11. `arbiter`（prefix `lfsm_arb`，内部 next=1，**纯控制：不接触 payload**）

只做"**选谁**"，不做"**发什么**"：输入仅为仲裁所需的控制/键信号，
输出为选择控制信号；candidate 元数据的 4:1 mux 剥离至顶层（§11A），
控制流（ballot/grant）与 payload（元数据）完全解耦。
（2026-10-14 用户决策：原 §11 的 `o_mem_req_*` 组装逻辑移至 §11A。）

### 11.1 inputs / outs

| in key | 位宽/shape | 语义 | 来源 |
| :--- | :--- | :--- | :--- |
| `cand_valid/cand_inst(4)/cand_rd_mem_id(14)` ×4 | 标量 ×4 lane | 仲裁 ballot（`seq/planned_*` 不进 arbiter） | cand_holder（4 路） |
| `dest_ok` ×4 | 1 ×4 | destination 可分配 | tag_checker |
| `issue_room` | 1 | 发送队列准入（非满 / 本拍 pop 可腾；A-014） | req_sched |
| `i_mem_source_ok` | 1 × `shape=[4]` | lane source（baseline 恒 1） | MEM（外部端口） |

| out key | 位宽 | 语义 | 去向 |
| :--- | :--- | :--- | :--- |
| `fire` | 1 | 本拍存在获选 eligible candidate（内部 grant commit + §11B 入队使能；`o_mem_req_valid` 源移至 §11B 出口，A-014） | tag_checker、§11A（`push_valid`） |
| `grant_lane` | 2 | 获选 lane（顶层 payload mux 选择键 + req_sched 入队 lane） | tag_checker、§11A（mux 键） |
| `fire_consume` ×4 | 1 ×4 | per-lane consume strobe（`fire && grant==lane`） | assembler / cand_holder（经 top `fire_l`） |

### 11.2 伪码

```python
    # ── Cycle 0 ──────────────────────────────────────────────
    rr = domain.signal(width=2, reset_value=0, name=f"{prefix}_rr")   # reset=A（F-091）
    # per lane：elig[l] = cand_valid[l] & issue_room & i_mem_source_ok[l] & dest_ok[l]
    # issue_room 来自 req_sched（§11B，发送队列非满/本拍可腾）；
    # i_shared_mem_ready 移至队列出口 pop 门（A-014；规格 eligibility 四项中的
    # mem_ready 语义 = MEM 出口准入，落位 issue 拍）
    # 优先键：argmin (cand_inst, cand_rd_mem_id)（18b 比较树，×4）
    best   = argmin_key(elig, keys)
    tied   = [elig[l] & (keys[l] == best) for l in range(4)]
    grant  = rr_scan(tied, rr)          # 从 rr 起 [A,AMX,B,BMX] 首个 tied（F-091）
    fire   = |elig                      # grant 拍 = 内部 commit + 入队（端口 fire 在 §11B 出口）
    outs = dict(fire=fire, grant_lane=grant,
                fire_consume=[fire & (grant == l) for l in range(4)])

    domain.next()
    # ── Cycle 1 ──────────────────────────────────────────────
    rr.assign(grant + 1, when=fire)    # cursor 仅 fire 更新（F-091）；2b 自然回卷
    return outs
```

## 11A. 请求 payload 组装 mux（`lfsm_top` 内组合；输出入 §11B 队列）

原 arbiter 中的 4:1 元数据 mux 剥离到顶层：`arbiter` 只产出
`fire/grant_lane/fire_consume`（§11），顶层据此把四路 asm 元数据视图、
cand_holder present 标量与 tag_checker 的 tag 组选择成单笔
**待发载荷**（PORT_LIST §4.4 端口组逐字段不变）。**A-014（2026-10-14
用户决策，推翻 A-006）**：mux 输出不再直出端口，而是写入 §11B
`req_sched` 发送队列；`rd_mem_fire` 的端口时序落位 **issue 拍
（grant 次拍）**——选择与 MEM 下发解耦。

连接：输入 = assembler×4（`view_*` 元数据视图）+ cand_holder×4
（`cand_inst/rd_mem_id/seq`）+ tag_checker（`dest_base/tag_cnt` 与
`o_load_ptr_update_*`）+ arbiter（`fire/grant_lane`）；输出 =
`req_mux` 全组 → req_sched（§11B）。

```python
    # ── Cycle 0（lfsm_top，组合；无寄存器）──────────────────
    g, fire = arb_o["grant_lane"], arb_o["fire"]
    req_mux = dict(                      # 待发载荷组合（push 侧，§11B 直收）
        push_valid=fire,
        key_inst_id=chd_o[g]["cand_inst"], key_lane=u(2, g),
        key_seq=chd_o[g]["cand_seq"], rd_mem_id=chd_o[g]["cand_rd_mem_id"],
        src_addr=mux4(asm_view_src_addr, g),   # shape=[32] 向量 mux
        src_len=mux4(asm_view_src_len, g),
        src_count=mux4(asm_view_src_cnt, g),
        load_byte_count=mux4(asm_view_load, g),
        valid_byte_count=mux4(asm_view_valid, g),
        padding_byte_count=mux4(asm_view_pad, g),
        wr_index=mux4(asm_view_wr_index, g),
        wr_offset=mux4(asm_view_wr_offset, g),
        wr_len=mux4(asm_view_wr_len, g),
        wr_count=mux4(asm_view_wr_cnt, g),
        tag_range_base=tck_o["dest_base"][g],
        tag_range_count=tck_o["tag_cnt"][g],
        tag_range_confirm=mux4(asm_view_group_final, g),
        is_partial_beat=mux4(asm_view_is_partial, g),   # UU≡0（D-003 sva）
        is_instruction_last=mux4(asm_view_is_last, g),
        upd_valid=tck_o["o_load_ptr_update_valid"],     # LoadPtrUpdate 同组入队（A-014）
        upd_lane=u(2, g), upd_old_ptr=tck_o["o_load_ptr_update_old_ptr"],
        upd_new_ptr=tck_o["o_load_ptr_update_new_ptr"],
        upd_advance=tck_o["o_load_ptr_update_advance"])
    sva(mux4(asm_view_src_cnt, g) <= 32); sva(mux4(asm_view_wr_cnt, g) <= 32)
    sva(mux4(asm_view_advance, g) <= 32)   # A-003 上限
```

说明：mux 无寄存器（cycle-0 组合）；数据环（最深 = BMX 展开 → 本 mux）
终点改为 §11B 队列写端而非端口 pad（A-014 的时序收益之一）。

## 11B. `req_sched` 发送队列（prefix `lfsm_rqp`，内部 next=1；**A-014 采纳**）

**决策（2026-10-14 用户决策，推翻 A-006"不采纳 `lfsm_req_pipe`"——
A-006 v2 历史改写；规格偏差 DEV＝TRACEABILITY GAP-07）**：选择（grant）
与 MEM 下发解耦——`o_mem_req_*` 与 `o_load_ptr_update_*` **同组**经
**2-slot 发送队列**在 issue 拍（grant 次拍）原子发出；端口"update +
request 同拍"原子关系原样保留（SRC-01 sec 13/14.1 时序图口径）。
**深度=2 的理由**：`i_shared_mem_ready=0` 背压时保持 **1 issue/拍** 的
稳态连发（单级寄存会使 back-to-back 退化为每 2 拍 1 笔）；2-slot =
1 级管道 + 1 深背压余量，反压经 `issue_room` 回传仲裁侧。

语义映射：
- **grant 拍（fire 拍）**：内部 commit 仍原子——消费 candidate、binding
  提交、load_ptr 推进、group 开关、RR 更新（§9/§10/§11）+ §11A 载荷
  **入队**（grant 与 fire_consume 语义不变）；
- **issue 拍（次拍）**：front 有效且 `i_shared_mem_ready=1` ⇒
  `o_mem_req_valid=1` 单拍脉冲，`RdMemRequest` 与 `LoadPtrUpdate` 同拍
  原子发出——`valid⇒同拍发出` 在端口层原样成立（PORT_LIST §5.3 新落位）。

### 11B.1 inputs / outs

| in key | 位宽/shape | 语义 | 来源 |
| :--- | :--- | :--- | :--- |
| §11A `req_mux` 全组 | 见 §11A | push 载荷（payload+update；`push_valid`=fire） | §11A 组合 mux（lfsm_top；汇聚 assembler 视图、cand_holder 标量、tag_checker tag 组、arbiter 选择） |
| `i_shared_mem_ready` | 1 | MEM 出口准入（**issue 拍采样**，R-25） | MEM（外部端口） |

| out key | 语义 | 去向 |
| :--- | :--- | :--- |
| `issue_room` | 队列非满或本拍可腾（arbitration 准入项，§11） | arbiter |
| `o_mem_req_valid` + payload 全组 | PORT_LIST §4.4（front 直出） | MEM（外部端口） |
| `o_load_ptr_update_valid/_lane/_old_ptr/_new_ptr/_advance` | PORT_LIST §4.3（与 request 同拍原子） | Buf/RAM（外部端口） |
| `rqp_empty` | cnt==0（`o_lfsm_idle` 组成项，F-120） | lfsm_top |

### 11B.2 伪码

```python
def req_sched(m, domain, *, inputs=None, prefix="lfsm_rqp"):
    # ── Cycle 0 ──────────────────────────────────────────────
    # 2-slot FIFO：每 slot = §11A 全字段副本（payload+update，≈2.3Kb/slot）
    s_v = domain.signal(width=1, shape=[2], reset_value=0, ...)
    # … s_key_inst[2](4) / s_src_addr[2×32](32) / … / s_upd_v[2](1) 全字段
    cnt = domain.signal(width=2, reset_value=0, name=f"{prefix}_cnt")   # 0..2
    pr  = domain.signal(width=1, reset_value=0, name=f"{prefix}_pr")    # read ptr
    pw  = domain.signal(width=1, reset_value=0, name=f"{prefix}_pw")    # write ptr
    push_valid, key_inst_id, … = submodule_input(...)   # §11A req_mux 全组
    mem_ready = submodule_input(inputs, "i_shared_mem_ready", ..., width=1)

    front_valid = s_v[pr]
    pop  = front_valid & mem_ready            # = o_mem_req_valid（issue 拍脉冲）
    room = (cnt < 2) | ((cnt > 0) & mem_ready)   # 满 2 时若本拍 pop 仍可腾
    outs = dict(issue_room=room, rqp_empty=(cnt == 0),
                o_mem_req_valid=pop,
                o_mem_req_key_inst_id=vec_rd(s_key_inst, pr), …,  # front 全字段直出
                o_load_ptr_update_valid=pop & vec_rd(s_upd_v, pr),
                o_load_ptr_update_lane=vec_rd(s_upd_lane, pr),
                o_load_ptr_update_old_ptr=vec_rd(s_upd_old, pr),
                o_load_ptr_update_new_ptr=vec_rd(s_upd_new, pr),
                o_load_ptr_update_advance=vec_rd(s_upd_adv, pr))
    sva(~push_valid | room)                   # never-overflow（eligibility 保证）

    domain.next()
    # ── Cycle 1 ──────────────────────────────────────────────
    push = push_valid & room                  # 每字段写入 slot[pw]
    for i in range(2):
        hit = push & (pw == i)
        s_v[i].assign(1, when=hit)            # … s_key_inst[i]/s_src_addr[i]… 全字段
    pr.assign(pr + 1, when=pop)
    pw.assign(pw + 1, when=push)
    cnt <<= cnt + push - pop                  # push/pop 可同拍（cnt 自洽）
    # 时序性质（TB 断言锚点）：
    #  1) push→pop 最早 +1 拍（无同拍 bypass）；
    #  2) 稳态 ready=1：grant 连续 1/拍、pop 连续 1/拍 —— 端口 1 req/拍保持；
    #  3) ready=0：front 保持（payload 不变，F-113）；cnt==2 → issue_room=0 →
    #     grant 冻结（mem_ready 反压由本队列承接，不回灌 eligibility）；
    #  4) 端口顺序 == grant 顺序（FIFO）；MEM in-order response 前提不破坏（SRC-04 sec 17）。
    return outs
```

说明：请求流相对 golden 的相移 = 边3 +1 与本段 +1，**合计链首 +2 拍**
（连发节奏不变）；`o_mem_req_valid` 由 front 组合产生，"valid ⇒ 同拍
发出"承诺在 issue 拍落位成立。

## 12. `c_path`（prefix `lfsm_c`，内部 next=1）

### 12.1 inputs / outs

| in key | 位宽 | 语义 | 来源 |
| :--- | :--- | :--- | :--- |
| `c_enq_valid` / `c_enq_inst(4)` / `c_enq_rdgen(14)` / `c_enq_m(1)` / `c_enq_n(8)` / `c_enq_src(32)` | — | C FIFO entry（拍末入队） | rdgen |
| `i_register_ready` | 1 | C issue 唯一准入 | RegisterUnit（外部端口） |

| out key | 位宽 | 语义 | 去向 |
| :--- | :--- | :--- | :--- |
| `o_reg_req_valid` / `_inst_id(4)` / `_rdgen_id(14)` / `_m_idx(1)` / `_n_idx(8)` / `_src_addr(32)` | — | `RegisterRequest(C)`（head 直出，未 fire 保持） | RegisterUnit（外部端口） |
| `c_empty` | 1 | C FIFO 空 | lfsm_top（`o_lfsm_idle`） |

### 12.2 伪码

```python
    # ── Cycle 0 ──────────────────────────────────────────────
    # 状态：c_inst[8]/c_rdg[8]/c_m[8]/c_n[8]/c_src[8]（向量）+ head/tail/cnt（3/3/4b）
    head_v = cnt > 0
    fire   = head_v & i_register_ready                 # 唯一准入；无竞争仲裁（F-100）
    outs = dict(o_reg_req_valid=head_v,
                o_reg_req_inst_id=vec_rd(c_inst, head), o_reg_req_rdgen_id=vec_rd(c_rdg, head),
                o_reg_req_m_idx=vec_rd(c_m, head), o_reg_req_n_idx=vec_rd(c_n, head),
                o_reg_req_src_addr=vec_rd(c_src, head), c_empty=~head_v)
    domain.next()
    # ── Cycle 1 ──────────────────────────────────────────────
    head.assign(head + 1, when=fire)                   # 未 fire 保持 head/payload（F-100）
    for i in range(8):                                 # rdgen 拍末入队，次拍起可 issue（无同拍 bypass）
        c_inst[i].assign(c_enq_inst, when=c_enq_valid & (tail == i))   # …各字段
    tail.assign(tail + 1, when=c_enq_valid)
    cnt <<= cnt + c_enq_valid - fire
    sva(cnt + c_enq_valid - fire <= 8, "c fifo never-full")            # A-002
    return outs
```

## 13. `lfsm_top`（prefix `lfsm`，内部 next=0）

```python
def lfsm_top(m, domain, *, inputs=None, LOAD_BUS_BYTES=128, BUFA_SLOTS=8, L0B_SLOTS=32,
             AMX_SLOTS=32, BMX_SLOTS=256, MAX_MX_TAG_SPAN=4,
             A_BLOCK_ORDER="EU_M_HALF_K_HALF",
             RDQ_A_DEPTH=16, RDQ_B_DEPTH=128, RDQ_AMX_DEPTH=8, RDQ_BMX_DEPTH=4,
             BMX_WINDOW_POOL=2, C_FIFO_DEPTH=8, CFG_FIFO_DEPTH=2,
             prefix="lfsm"):
    # ── Cycle 0（无自有状态；全组合连线 + 子模块调用）────────────────────
    # 1) 端口输入：标量 submodule_input；向量 cas(domain, m.input(shape=[4]), cycle=0)
    cfg_o = domain.call(config_regs, inputs={**walk_cfg_pins, **lfsm_cfg_pins,
                        "i_start_accept": ~wlk_o["wlk_active"]}, prefix="lfsm_cfg",
                        CFG_FIFO_DEPTH=CFG_FIFO_DEPTH)
    wlk_o = domain.call(walker, inputs={"start": cfg_o["start"], "stall": zero1,
                        **cfg_fields}, prefix="lfsm_wlk")
    rdg_o = domain.call(rdgen, inputs={"start": cfg_o["start"], **wlk_o_tok,
                        **cfg_fields}, prefix="lfsm_rdg")
    for lane, L in ((0,"a"), (1,"amx"), (2,"b"), (3,"bmx")):
        q_o[lane]   = domain.call(rd_queue, inputs={**rdg_enq[lane], "pop": asm_o[lane]["pop"]},
                                  prefix=f"lfsm_q_{L}", depth=RDQ_DEPTH[lane])
        asm_o[lane] = domain.call(ASM_FN[lane], inputs={**q_o[lane],
                                  "fire_consume": fire_l[lane], "dest_base": tck_o["dest_base"][lane]},
                                  prefix=f"lfsm_asm_{L}", full_count=FULL_COUNT[lane],
                                  block_bytes=BLOCK_BYTES[lane])
        chd_o[lane] = domain.call(cand_holder, inputs={**asm_view_scalars(asm_o[lane]),
                                  "load_ptr": tck_o["load_ptr"][lane],
                                  "load_ptr_post": tck_o["load_ptr_post"][lane],
                                  "fire_consume": fire_l[lane]},
                                  prefix=f"lfsm_chd_{L}")
    tck_o = domain.call(tag_checker, inputs={**present_scalars(chd_o),
                        **group_final(asm_o), "i_load_range_idle": idle_in,
                        "fire": arb_o["fire"], "grant_lane": arb_o["grant_lane"]},
                        prefix="lfsm_tck")
    # §11A 组合 mux（cycle-0）产出 req_mux 包 → §11B req_sched 发送队列（A-014）
    rqp_o = domain.call(req_sched, inputs={**req_mux_of(tck_o, chd_o, asm_o,
                        arb_o["fire"], arb_o["grant_lane"]),   # §11A 全组
                        "i_shared_mem_ready": mem_ready},
                        prefix="lfsm_rqp")
    arb_o = domain.call(arbiter, inputs={**present_keys(chd_o), **tck_o["dest_ok"],
                        "issue_room": rqp_o["issue_room"], "i_mem_source_ok": src_ok},
                        prefix="lfsm_arb")
    c_o   = domain.call(c_path, inputs={**rdg_o_c, "i_register_ready": reg_ready},
                        prefix="lfsm_c", depth=C_FIFO_DEPTH)
    fire_l = arb_o["fire_consume"]                        # per-lane consume strobe（注⑤）
    # 端口：o_mem_req_* / o_load_ptr_update_* 全组由 rqp_o 直出（issue 拍，§11B）；
    # 其余观察端口照旧
    # 观察输出（F-120/A-009）
    o_walk_stall = u(1,0)
    o_lfsm_idle  = ~wlk_o["wlk_active"] & cfg_o["cfg_empty"] & \
                   all_(q_o[l]["cnt"] == 0 for l in range(4)) & \
                   all_(asm_o[l]["ctx_empty"] for l in range(4)) & \
                   all_(~chd_o[l]["cand_valid"] for l in range(4)) & \
                   rqp_o["rqp_empty"] & c_o["c_empty"]
    if inputs is None:      # 独立模式：发射 PORT_LIST §4 全部端口
        m.output(f"{prefix}_o_walk_cfg_ready", wire_of(cfg_o["o_walk_cfg_ready"]))
        # … 其余标量 wire_of；向量（o_load_range_query_* 等）Wire 直传
    return {**cfg_o, **wlk_o, **rdg_o, **tck_o, **arb_o, **c_o, "o_lfsm_idle": o_lfsm_idle}
```

注⑤：`fire_l`/`~wlk_o[...]` 等前引信号在 Python  elaboration 层按
依赖序局部重排（eager=True 下为纯元编程）；`asm_o`/`chd_o` 引用在其
`domain.call` 之后定义——文本顺序按依赖拓扑排序书写，上表为逻辑序。

## 14. reset / idle / 反压 汇总

- **reset（F-003/A-010）**：全部 `domain.signal(reset_value=0)`；
  `rr_cursor=0`（=A）；reset 由 domain 统一驱动（Tb
  `tb.reset("rst", cycles_asserted=2, cycles_deasserted=1)`，PRC-01 §9），
  不作数据端口；reset 期间输入握手被 ready 自然拒绝（FIFO 空）。
- **idle（F-120）**：`o_lfsm_idle` 见 §13；`o_walk_stall` tie-0（A-009）。
- **反压（F-113/I5 定向）**：`destination_ok=0`（query valid=1 且
  `i_load_range_idle=0`）、`i_mem_source_ok=0`、`i_register_ready=0`、
  **`i_shared_mem_ready=0`（新语义，A-014）**——前两类使 `elig=0` /
  C `fire=0`；`mem_ready=0` 则由 **§11B 发送队列承接**（front 保持、
  不 pop；cnt 到 2 → `issue_room=0` → grant 冻结）；任一情形当拍无
  `fire_consume`，asm/cand_holder/queue/c_path 全部状态经「无赋值路径 =
  保持」与 `.assign(when=)` 分支保持；输入电平不锁存（PORT_LIST
  §5.5）。优先级不变量（F-111）在各模块 `when=` 链中按「fire/退役 >
  移交 > 新工作」书写。

## 15. 实例化参数与静态断言

- 顶层静态参数（PORT_LIST §3）经 `lfsm_top` kwargs 透传；
  `FULL_COUNT/BLOCK_BYTES/DEPTH` 由参数推导为常量。
- build-time 断言（elaboration 期 `assert`，对应 SRC-04 sec 16）：
  `LOAD_BUS_BYTES % 128 == 0`；`AMX_SLOTS == BUFA_SLOTS*4`；
  `BMX_SLOTS % MAX_MX_TAG_SPAN == 0`；各 DEPTH 为 2 幂；
  `RDQ_*_DEPTH/C_FIFO_DEPTH/CFG_FIFO_DEPTH/BMX_WINDOW_POOL > 0`；
  `REQ_SCHED_DEPTH == 2`（A-014，固定不可配——单 slot 会在
  `mem_ready=0` 时把稳态 issue 降为每 2 拍 1 笔）；
  `A_BLOCK_ORDER == "EU_M_HALF_K_HALF"`（本轮范围，F-050 gap）。
- 内部 `domain.next()` 数复核：叶模块全 = 1，`lfsm_top` = 0
  （PIPE §1）；层次化发射每个 `domain.call()` 一个 `func.func`
  （PRC-01 §7.6）。

## 16. F-xxx → 伪码落点速查（供 Step 7 TRACEABILITY 展开）

| F-xxx | 落点 |
| :--- | :--- |
| F-001/F-002 | §1 config_regs（pair_ok/start/sva） |
| F-003 | §14 + 各模块 `reset_value=0` |
| F-010/F-011/F-012 | §2 walker（transition/advance/stall tie-0/start-done） |
| F-020…F-023 | §3 rdgen（fv 条件/地址/sva） |
| F-024/F-110 | §3 end strobes + §5–§8 end_pop/is_last |
| F-021/F-025 | §3 rd_id/CEntry |
| F-030…F-032 | §4 rd_queue（双写口/head view/never-full sva） |
| F-040/F-041 | §5–§8 各 asm 保持/padding 规则 |
| F-050/F-055/F-056 | §5/§6 |
| F-060/F-061 | §7 |
| F-065…F-067 | §8 |
| F-070…F-073 | §9 cand_holder（formable/统一 held 规则/planned 锁存） |
| F-080…F-083 | §10 tag_checker（query/dest_ok/grp/load_ptr） |
| F-090…F-094 | §11 arbiter（elig/优先键/RR/选择控制）+ §11A 顶层 mux（payload 组装）+ §11B req_sched（发送队列/issue 拍/同拍原子发出，A-014）+ sva |
| F-100 | §12 c_path |
| F-111…F-113 | §14 + 各模块 when 链优先级 |
| F-120 | §13 o_lfsm_idle |
```
