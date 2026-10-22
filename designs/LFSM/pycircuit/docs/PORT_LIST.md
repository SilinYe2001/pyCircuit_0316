# LFSM (4EU UU mode) PORT_LIST

> Step 3 交付物（依据 `docs/pycircuit_implementation_method.md` Step 3，
> 「从转换后的 Markdown …」§1 order-4）。冻结 `lfsm_top` 对外契约：
> 全部输入/输出的名称、方向、位宽、向量 shape、时钟域、协议相位与
> prefix-key。建立日期：2026-10-13。
> 需求编号（SRC-xx/R-xx）见 `REQUIREMENT_SOURCES.md`；决策编号
> （A-xxx）见 `ASSUMPTIONS.md`。范围：4EU UU mode（Shared MEM
> baseline）+ UU C-only 路径；RU overlay / TMEM / 8EU 出界。

## 1. 模块角色（顶层功能一段话）

`lfsm_top` 是 4EU UU mode 的 LFSM 读数据流水：接受按 `inst_id` 配对
的 `WalkConfig` / `LFSMInstructionConfig` 后运行独立 MKN walker，为
A/AMX/B/BMX 四路生成首访去重的逻辑 RD 并原子批量入队（无容量反压），
经 DataBlock merge/padding、128B 带宽打包、destination 分配与
`(inst_id,rd_mem_id)` 优先键 + RR 仲裁，每拍最多向 Shared MEM 原子发出
一笔带 buffer metadata 的 `RdMemRequest`，同拍向 Buf/RAM 发出对应的
`LoadPtrUpdate`；每个唯一 C key `(inst,m,n)` 经独立 C FIFO 以
`RegisterRequest(C)` 输出到 register port（C-only 流量，无竞争仲裁）。

## 2. 时钟、复位与 CDC

- **单时钟域**：`create_domain("lfsm", ...)`；全部子模块经
  `domain.call()` 共享该域（push/pop 周期隔离，PRC-01 §7.3）。
- **复位**：规格输入 `reset`（SRC-01 sec 3.1）映射为 domain reset
  （Tb `tb.reset("rst", cycles_asserted=2, cycles_deasserted=1)`，
  PRC-01 §9），**不作为数据端口**；所有状态经
  `domain.signal(reset_value=...)` 赋初值；reset 优先级最高（A-010，
  R-33）。
- **CDC**：无跨时钟域路径，不需要 `m.cdc_sync` / `m.async_fifo`。

## 3. 静态（build-time）参数

均为模块实例静态配置（A-005.5、SRC-02 sec 3.8），不设运行时配置端口。

| 参数 | 默认 | 说明 / 依据 |
| :--- | ---: | :--- |
| `LOAD_BUS_BYTES` | 128 | 共享 MEM 读带宽；MX 要求 128B 的 2 幂缩放倍数（SRC-01 sec 9.3/11.4，R-32） |
| `BUFA_SLOTS` | 8 | A tag 深度（SRC-04 sec 3.4） |
| `L0B_SLOTS` | 32 | B tag 深度（SRC-04 sec 3.4） |
| `AMX_SLOTS` | 32 | `= BUFA_SLOTS × 4`（SRC-04 sec 3.5/16） |
| `BMX_SLOTS` | 256 | full-width headroom 深度（SRC-04 sec 3.5） |
| `MAX_MX_TAG_SPAN` | 4 | HIF4（SRC-04 sec 3.5/16） |
| `A_BLOCK_ORDER` | `EU_M_HALF_K_HALF` | 3 值枚举静态参数（SRC-01 sec 9.1，R-12） |
| `RDQ_A_DEPTH` | 16 | 参数化深度 + never-full 断言（A-002 结论 1，A-011） |
| `RDQ_B_DEPTH` | 128 | 同上 |
| `RDQ_AMX_DEPTH` | 8 | 同上 |
| `RDQ_BMX_DEPTH` | 4 | 同上 |
| `BMX_WINDOW_POOL` | 2 | 窗口 context 池（1 active + 1 完成待 drain），每窗口 ≤32 owner slot（A-002） |
| `C_FIFO_DEPTH` | 8 | C FIFO 参数化深度 + never-full（A-002） |
| `CFG_FIFO_DEPTH` | 2 | WalkConfig/LFSMInstructionConfig 配置 FIFO（A-005.2） |
| `MAX_SRC_RANGES` | 32 | 单次 fire source range 上限（BMX MXFP8 窗口 32 cell；§7） |
| `MAX_WRITES` | 32 | 单次 fire `buffer_writes[]` 上限（A-003） |
| `MAX_ADVANCE` | 32 | `LoadPtrUpdate.advance` / query advance 上限（A-003） |
| `TAG_RANGES_LEN` | 1 | `tag_ranges[]` 定长 1（A-003，已决策） |
| `INST_ID_W` | 4 | `inst_id` 位宽参数 |
| `ADDR_W` | 32 | 地址位宽参数 |
| `RDGEN_ID_W` | 14 | token 上限 = m_slice(2)×n_hw(128)×k_groups(32) = 8192 |
| `CAND_SEQ_W` | 13 | per-lane per-instruction request 序号（B lane ≤ 4096 笔） |
| `TAG_IDX_W` | 8 | 最深 lane BMX=256；浅 lane 高位 tie-0 |
| `TAG_ADV_W` | 6 | advance ≤ 32 |
| `BYTE_CNT_W` | 8 | byte count ≤ 128 |
| `BYTE_OFF_W` | 11 | 最大 slot = BufA 2048B（512B/EU × 4EU） |

派生常量：`FULL_COUNT[A/B]=1`、`FULL_COUNT[AMX/BMX]=4`
（`= LOAD_BUS_BYTES / block_bytes`，SRC-01 sec 10，R-17）。

## 4. 端口表

约定：

- 独立模式下标量输入经 `submodule_input()` 创建，发射名 =
  `lfsm_<key>`；向量端口在该助手之外以
  `cas(domain, m.input("lfsm_<key>", width=W, shape=[4]), cycle=0)`
  创建；标量输出 `m.output("lfsm_<key>", wire_of(sig))`，向量输出
  `Wire` 直接传入（PRC-01 §2/§7）。
- 向量 `shape=[4]` 的 lane 序固定为 `[A, AMX, B, BMX]`；lane 编码
  A=0 / AMX=1 / B=2 / BMX=3（与 RR 扫描序一致，SRC-04 sec 11）。
- 所有 valid 高有效；所有输入在 evaluate（cycle-0）采样，只读
  cycle-start 状态（SRC-01 sec 5，R-34）。
- data_type 编码：B32=0 / B16=1 / B8=2 / B4=3 / MXFP8=4 / MXFP4=5 /
  HIF4=6；m_mode 编码：0=16 / 1=32；eu_mode 编码：0=4（UU 固定，
  断言）/ 1=8（保留，拒收）。

### 4.1 WalkConfig 通道（TOP → LFSM，valid/ready）

| key | 方向 | 位宽 / shape | 协议相位 | Spec trace |
| :--- | :--- | :--- | :--- | :--- |
| `i_walk_cfg_valid` | in | 1 | valid/ready；accept = valid&&ready 于拍末 commit；未 accept payload 保持 | SRC-04 sec 2.1；SRC-02 sec 3.7 |
| `o_walk_cfg_ready` | out | 1 | 配置 FIFO 非满即 1（cycle-0 组合） | 同上 |
| `i_walk_cfg_inst_id` | in | 4 | 随 valid 采样 | SRC-04 sec 2.1 |
| `i_walk_cfg_m_mode` | in | 1 | 同 payload | 同上 |
| `i_walk_cfg_m_slice_count` | in | 2 | 1..2 | 同上 |
| `i_walk_cfg_n_hw_count` | in | 8 | 1..128 | 同上 |
| `i_walk_cfg_n_step` | in | 2 | LFSM 断言 ==1（SRC-04 sec 16；2026-10-13 人工确认**保留**该端口，不移除） | 同上 |
| `i_walk_cfg_k_groups` | in | 6 | 1..32 | 同上 |

注（2026-10-13 用户决策，§8 适配 8）：loop 几何**不随配置下发**——
`n_blocks[]` / `n_outer_count` / `k_step_per_outer` / `k_outer_count`
四个派生字段从本通道移除（避免 TOP 侧 ceil 除法与迭代生成，也省掉
`n_blocks[]` 寄存数组）。walker 已逐拍维护 m/k/n index，故在
transition 边界以**加法级**运算（inc/cmp/sub/mux，无除法器）现场维护
每个 loop 的 base 与 length：

- N block：`remaining = n_hw_count − n_base`；
  `n_len = (remaining==9 || remaining==10) ? 4 : min(8, remaining)`
  （与 SRC-02 sec 3.5.2 的 9→[4,5]/10→[4,6] 规则逐项等价）；
  N_OUTER transition 时 `n_base += n_len`；
- K outer：`k_count = min(k_step, k_groups − k_base)`；
  K_OUTER transition 时 `k_base += k_count`；`k_step = m_mode ? 4 : 8`
  （1-bit mux，无需下发）；
- loop 结束条件为 `base ≥ total`（`n_hw_count` / `k_groups`），无需显式
  outer count（消除 `ceil(k_groups/k_step)` 除法）。

golden `WalkConfig.n_block_step`（REF-05）4EU 恒 1，同样不携带（§8
适配 6）。

### 4.2 LFSMInstructionConfig 通道（TOP → LFSM，valid/ready）

| key | 方向 | 位宽 / shape | 协议相位 | Spec trace |
| :--- | :--- | :--- | :--- | :--- |
| `i_lfsm_cfg_valid` | in | 1 | 同 §4.1 | SRC-04 sec 2.2；SRC-02 sec 3.7 |
| `o_lfsm_cfg_ready` | out | 1 | 同 §4.1 | 同上 |
| `i_lfsm_cfg_inst_id` | in | 4 | 与 WalkConfig head 按 `inst_id` 配对（不等即协议错误断言，A-005.2） | SRC-04 sec 2.2 |
| `i_lfsm_cfg_eu_mode` | in | 1 | UU 断言 ==0（4EU） | 同上 |
| `i_lfsm_cfg_data_type` | in | 3 | 编码见 §4 约定 | 同上 |
| `i_lfsm_cfg_mx_mode_en` | in | 1 | | 同上 |
| `i_lfsm_cfg_mx_bytes_per_k0` | in | 3 | 0/1/2/4 | 同上 |
| `i_lfsm_cfg_n_hw_count` | in | 8 | C 地址预计算用（SRC-02 sec 3.6.2） | 同上 |
| `i_lfsm_cfg_a_base_addr` / `i_lfsm_cfg_a_limit_addr` | in | 32 / 32 | | 同上 |
| `i_lfsm_cfg_a_mx_base_addr` / `i_lfsm_cfg_a_mx_limit_addr` | in | 32 / 32 | | 同上 |
| `i_lfsm_cfg_b_base_addr` / `i_lfsm_cfg_b_limit_addr` | in | 32 / 32 | | 同上 |
| `i_lfsm_cfg_b_mx_base_addr` / `i_lfsm_cfg_b_mx_limit_addr` | in | 32 / 32 | | 同上 |
| `i_lfsm_cfg_l0c_base_addr` | in | 32 | C 地址 = `l0c_base+(m×n_hw+n)×16` | SRC-02 sec 3.6.2 |

配对启动规则：两通道各进 `CFG_FIFO_DEPTH` 配置 FIFO，两 FIFO head
`inst_id` 相等时同拍接收并启动该 instruction（A-005.2，R-01）。

### 4.3 Buf/RAM 接口

| key | 方向 | 位宽 / shape | 协议相位 | Spec trace |
| :--- | :--- | :--- | :--- | :--- |
| `o_load_range_query_valid` | out | 1 × `shape=[4]` | **cycle-0 组合输出**：由 cycle-start held candidate 锁存的 `planned_*` 派生；外部 Buf/RAM 同拍组合回答（§5.2 契约，A-004） | SRC-01 sec 3.1/11.2；SRC-05 sec 8.1；A-004 |
| `o_load_range_query_base` | out | 8 × `shape=[4]` | 同上；`planned_base`（split 续写时 = `load_ptr`，valid=0） | 同上 |
| `o_load_range_query_advance` | out | 6 × `shape=[4]` | 同上；`planned_advance` ≤ 32；0 表示无需检查 | 同上 |
| `i_load_range_idle` | in | 1 × `shape=[4]` | cycle-0 组合采样；`valid=0` 时外部**必须**回答 1（A-004 相位契约） | SRC-01 sec 3.1；SRC-05 sec 8.1 |
| `o_load_ptr_update_valid` | out | 1 | **issue 拍单拍脉冲**（发送队列出口，A-014/GAP-07）：与 `o_mem_req_valid` 同拍原子；无 ready（Buf/RAM 必收，SRC-05 sec 8.2）；`advance>0` | SRC-01 sec 13；SRC-04 sec 10.7 |
| `o_load_ptr_update_lane` | out | 2 | 同 payload | 同上 |
| `o_load_ptr_update_old_ptr` | out | 8 | | 同上 |
| `o_load_ptr_update_new_ptr` | out | 8 | `= (old+advance) % DEPTH[lane]` | 同上 |
| `o_load_ptr_update_advance` | out | 6 | 1..32 | 同上 |

有意排除：SRC-05 §8.1 `o_tag_state[lane][index]`（optional debug/full
view）不实现（REQUIREMENT_SOURCES §5）。

### 4.4 MEM 接口

| key | 方向 | 位宽 / shape | 协议相位 | Spec trace |
| :--- | :--- | :--- | :--- | :--- |
| `i_shared_mem_ready` | in | 1 | **issue 拍状态采样**（发送队列出口 pop 门，A-014/GAP-07）：**不进** arbiter eligibility（由 `issue_room` 承接）；即 MEM 侧 `o_mem_req_ready`（§8 适配 5） | SRC-01 sec 3.1；SRC-06 sec 5/10 |
| `i_mem_source_ok` | in | 1 × `shape=[4]` | cycle-0 状态采样；baseline 恒 1 | SRC-01 sec 3.1；SRC-06 sec 10 |
| `o_mem_req_valid` | out | 1 | **issue 拍单拍脉冲**（发送队列出口，A-014/GAP-07）：front 有效且 `i_shared_mem_ready=1` ⇒ 同拍原子发出 request + `LoadPtrUpdate`；内部 grant commit（消费 candidate/binding/load_ptr/RR）在 grant 拍完成 | SRC-01 sec 12/13；SRC-06 sec 5 |
| `o_mem_req_key_inst_id` | out | 4 | request_key 三元组之一；MEM 随 response 原样返回（系统定位/error 关联；Buf/RAM 按 exact range 匹配，不依赖该字段） | SRC-06 sec 5/12 |
| `o_mem_req_key_lane` | out | 2 | request_key 之二；同时派生 `load_type`（LOAD_A/AMX/B/BMX，§8 适配 5） | 同上 |
| `o_mem_req_key_seq` | out | 13 | request_key 之三；per-lane、instruction 开始清零 | 同上 |
| `o_mem_req_rd_mem_id` | out | 14 | candidate 首 DataBlock 的 one-based `rdgen_id`（R-18） | SRC-01 sec 10/12 |
| `o_mem_req_src_addr` | out | 32 × `shape=[32]` | 定长展平 + count；未用项 0（§7） | SRC-06 sec 5；REF-02 `source_ranges` |
| `o_mem_req_src_len` | out | 8 × `shape=[32]` | 每 range 连续字节数 ≤ 128 | 同上 |
| `o_mem_req_src_count` | out | 6 | 0..32 | 同上 |
| `o_mem_req_load_byte_count` | out | 8 | transport 实际字节 ≤ 128 | SRC-06 sec 5/11 |
| `o_mem_req_valid_byte_count` | out | 8 | 含 B/BMX/AMX mem-pad（MEM-read 口径） | SRC-04 sec 10.4 |
| `o_mem_req_padding_byte_count` | out | 8 | 纯 transport fill | SRC-06 sec 5/11 |
| `o_mem_req_wr_index` | out | 8 × `shape=[32]` | `buffer_writes[]` 定长展平（§7、§8 适配 1/2） | SRC-01 sec 14；SRC-06 sec 5.2 |
| `o_mem_req_wr_offset` | out | 11 × `shape=[32]` | slot 内字节偏移 | 同上 |
| `o_mem_req_wr_len` | out | 8 × `shape=[32]` | 连续写字节数 | 同上 |
| `o_mem_req_wr_count` | out | 6 | 0..32 | 同上 |
| `o_mem_req_tag_range_base` | out | 8 | `tag_ranges[]` 定长 1（A-003）；与本次 `LoadPtrUpdate.old_ptr` 一致（split 续写复用首笔 range） | SRC-01 sec 14；A-003 |
| `o_mem_req_tag_range_count` | out | 6 | 1..32 | 同上 |
| `o_mem_req_tag_range_confirm` | out | 1 | `confirm_on_response`；仅整 range 末贡献 request 置 1 | SRC-01 sec 14 规则 3 |
| `o_mem_req_is_partial_beat` | out | 1 | instruction-last partial；BMX 恒 0 | SRC-06 sec 5/11 |
| `o_mem_req_is_instruction_last` | out | 1 | 本 lane 当前 instruction 末笔 | SRC-04 sec 10.4 |

MEM response（`MemDataResponse`）由 MEM 直接送 Buf/RAM，**不经过**
LFSM（SRC-01 sec 14/14.1；SRC-06 sec 6），本模块无 response 端口。

### 4.5 RegisterUnit C-only 接口

| key | 方向 | 位宽 / shape | 协议相位 | Spec trace |
| :--- | :--- | :--- | :--- | :--- |
| `i_register_ready` | in | 1 | cycle-0 状态采样；C issue 唯一准入 | SRC-01 sec 3.1；SRC-08 sec 6 |
| `o_reg_req_valid` | out | 1 | C FIFO head valid；**未 fire 保持**（valid&&ready 才 pop）；rdgen 拍末新 entry 无同拍 bypass | SRC-08 sec 5/6 |
| `o_reg_req_inst_id` | out | 4 | | SRC-04 sec 10.10 |
| `o_reg_req_rdgen_id` | out | 14 | 首次生成该 C key 的 token `walk_seq+1`（R-29） | SRC-08 sec 5.1 |
| `o_reg_req_m_idx` | out | 1 | C data key `(inst,m,n)` 之 m | 同上 |
| `o_reg_req_n_idx` | out | 8 | 之 n | 同上 |
| `o_reg_req_src_addr` | out | 32 | `l0c_base+(m×n_hw+n)×16`，rdgen 预计算 | SRC-08 sec 5.1；SRC-02 sec 3.6.2 |

常量化字段（不占用端口）：`kind=C`；C 数据量恒 16B（地址公式
`×16`）；`beat_index/total_beats=1/1`；无 owner/writes/
confirmed_ranges（C 不占 Buffer，SRC-08 sec 5.1、SRC-04 sec 10.10）。

### 4.6 观察输出

| key | 方向 | 位宽 | 协议相位 | Spec trace |
| :--- | :--- | :--- | :--- | :--- |
| `o_walk_stall` | out | 1 | **恒 0**（tie-off；RD Queue 无容量反压） | SRC-01 sec 3.2；A-009 |
| `o_lfsm_idle` | out | 1 | 电平；walker 无 active instruction、四路 Queue/Assembler context/held candidate/C FIFO 全空（TB 与系统集成 drain 观察字段，非规格功能端口，§8 适配 7） | —（观察字段，类同 `walk_stall` 性质） |

## 5. 协议相位契约（逐总线）

### 5.1 配置通道（WalkConfig / LFSMInstructionConfig）

- 标准 valid/ready：发送方 valid 未握手必须保持 payload；接收方
  （本模块）ready = 对应配置 FIFO 非满（cycle-0 组合）。
- accept 于拍末 commit 生效；两 FIFO head `inst_id` 相等时同拍配对
  接收（A-005.2）。
- reset 期间忽略全部输入握手，配置 FIFO 清空（A-010）。

### 5.2 `o_load_range_query` / `i_load_range_idle`（A-004 边界澄清）

规格只命名输入 `load_range_idle[lane]`（SRC-01 sec 3.1），但该 bit
需要 candidate range 才能计算（SRC-05 sec 7.6/8.1：全 idle + 非
`fresh_idle_guard` + `occupied+advance ≤ DEPTH`）。Buf/RAM 为外部
模块，故本模块增加 `o_load_range_query` 输出，相位契约如下：

1. 每 lane：有 held candidate 且 `planned_advance>0` ⇒
   `{valid=1, base=planned_base, advance=planned_advance}`；否则
   `{valid=0, base=load_ptr, advance=0}`（split 续写
   `planned_advance=0`，`destination_ok` 恒真，不查 destination，
   SRC-01 sec 11.3）。
2. query 由 **cycle-start 状态**（held candidate 寄存器）经纯组合
   派生；外部 Buf/RAM **同拍组合**回答 `i_load_range_idle`；
   eligibility 每拍重算（全部读取 cycle-start 状态，SRC-07 sec 3(5)
   (9)）。
3. **`valid=0` 时外部必须回答 `i_load_range_idle=1`**（无 range 需要
   检查；人工决策 2026-10-13，A-004）。
4. 外部实现须含 `fresh_idle_guard` 两拍规则：release commit 拍 C →
   C+1 tag 已 idle 但 `load_range_idle=0` → 最早 C+2 允许
   `idle→loading`（SRC-01 sec 11.2；SRC-05 sec 7.6/12）；集成 TB 的
   反应式 Buf/RAM stub 按 REF-04 `range_idle` 实现。

### 5.3 `RdMemRequest` / `LoadPtrUpdate`

**A-014（2026-10-14 用户决策，GAP-07 规格 deviation；推翻 A-006
"不采纳 `lfsm_req_pipe`"）**——grant 与 MEM 下发解耦，发送队列 2-slot：

- **grant 拍（内部 fire commit）**：原子完成消费 candidate、提交
  binding、推进 load_ptr、group 开关、更新 RR cursor（六效果中的全部
  内部状态），§11A mux 载荷（request + `LoadPtrUpdate` 组合）入 §11B
  发送队列；
- **issue 拍（grant 次拍）**：front 有效且 `i_shared_mem_ready=1` ⇒
  `o_mem_req_valid=1` 同拍脉冲，`RdMemRequest` 与 `LoadPtrUpdate`
  **同拍原子发出**——"valid ⇒ 同拍发出"在端口落位原样成立，
  无独立 ready 等待态；`i_shared_mem_ready` 在 **issue 拍采样**
  （R-25 语义 = MEM 出口准入）；
- eligibility = `candidate_valid && issue_room && i_mem_source_ok[lane]
  && destination_ok`：`i_shared_mem_ready` 不再进 eligibility，由
  2-slot 队列以 `issue_room`（非满/本拍可腾）承接背压——`mem_ready=0`
  期间 front/payload 保持，队列满时 grant 冻结、其余 lane 一并不获准
  （单 MEM 口的固有串行，SRC-01 sec 12「每 cycle 最多 grant 一笔」
  保持）；深度 2 保证 `ready=1` 稳态连发 1 issue/拍；
- 未获 grant 的 held candidate 与未 pop 的队列 front valid/payload 经
  `assign(when=)` 保持（SRC-01 sec 5 保持清单 + F-113）。
- `LoadPtrUpdate` 无 ready，Buf/RAM 必收且原子执行
  `idle→loading`（SRC-05 sec 8.2）；split 续写 `advance=0`，不产生
  update（SRC-04 sec 14）。

### 5.4 `RegisterRequest(C)`

- C FIFO head 的 valid/payload 保持至
  `fire = o_reg_req_valid && i_register_ready`；fire 拍末 pop。
- rdgen 拍末 commit 的新 C entry 次拍起可 issue（与普通 Queue 一样
  无同拍 bypass，SRC-08 sec 6）。
- 无竞争仲裁（UU C-only，SRC-08 sec 5）；每拍最多 1 笔。

### 5.5 状态输入（`i_load_range_idle` / `i_shared_mem_ready` /
`i_mem_source_ok` / `i_register_ready`）

均为 cycle-0 采样的电平输入，参与当拍判定；不锁存、不产生
内部反压状态（反压表现为 held candidate / FIFO head /
**发送队列 front** 保持；反压承接点：`mem_ready=0` → §11B 队列
front 保持 + `issue_room` 回授仲裁侧，A-014）。`i_shared_mem_ready`
的采样落位 = **issue 拍**（发送队列出口）。

## 6. 逻辑总线分组

| 总线 | 成员 | 方向 | 说明 |
| :--- | :--- | :--- | :--- |
| `walk_cfg` | §4.1 全部 | TOP → LFSM | valid/ready 配置通道 1 |
| `lfsm_cfg` | §4.2 全部 | TOP → LFSM | valid/ready 配置通道 2 |
| `buf_query` | `o_load_range_query_*` + `i_load_range_idle` | LFSM ⇄ Buf/RAM | 每 lane 同拍组合查询（§5.2） |
| `buf_update` | `o_load_ptr_update_*` | LFSM → Buf/RAM | 单拍脉冲，原子 `idle→loading` |
| `mem_req` | `o_mem_req_*` + `i_shared_mem_ready` + `i_mem_source_ok` | LFSM ⇄ MEM | 预合格 valid 的 request 通道（§5.3） |
| `reg_c` | `o_reg_req_*` + `i_register_ready` | LFSM ⇄ RegisterUnit | C-only，valid 保持型（§5.4） |
| `obs` | `o_walk_stall` / `o_lfsm_idle` | LFSM → TOP/TB | 观察字段 |

## 7. Payload 定长展平（A-003 同系决策）

单次 `rd_mem_fire` 元数据上限与展平方式：

| 数组 | 上限 | 展平 | 上限依据 |
| :--- | ---: | :--- | :--- |
| source ranges | 32 | `src_addr[32]` + `src_len[32]` + `src_count` | BMX MXFP8 窗口 = 4 block × 2 slot × 4 K-row = 32 cell（每 cell 一 fragment，含 mem-pad cell，REF-03 `_emit_bmx_window`）；AMX MXFP8 = 4 block × 4 key = 16；B ≤ 2；A = 1 |
| `buffer_writes[]` | 32 | `wr_index/offset/len[32]` + `wr_count` | A-003（实测 max 24；上限 32 = BMX MXFP8 窗口真实 owner 数 × span1） |
| `tag_ranges[]` | **1** | 标量 `{base,count,confirm}` | A-003（已决策；实测 4628 笔全 =1；多 range 为通用/RU/乱序窗口保留） |
| `LoadPtrUpdate.advance` | 32 | 标量 6b | A-003（窗口真实 owner 数 × span） |

每 fragment 的 source range 连续（A/B 块内几何使相邻 owner 的
fragment 在 MEM 线性/tile-major/行线性布局中分别退化为单 range 或
少量连续 range；BMX 按 cell 枚举），与 golden
`source_ranges = (addr, len)` 列表（REF-02）一一对应。

## 8. 接口适配决策（本文件记录，非新假设）

1. **`byte_mask` → `byte_offset + byte_len`**：规格
   `BufferWriteRef.byte_mask`（SRC-04 sec 10.8、SRC-06 sec 5）保留为
   接口契约但 Python 模型不验证 byte lane（SRC-04 sec 6、SRC-06
   sec 6「不属于当前验证范围」）；本设计全部合法几何中单笔写均
   连续，以等价的 `{index, byte_offset, byte_len}` 表达。若未来引入
   非连续写，须先扩展本契约再走 gate-first。
2. **per-write `lane` 字段上提**：candidate 恒单 lane，
   `buffer_writes[]`/`tag_ranges[]` 的 lane 与 request lane 一致，
   端口只保留 request 级 `o_mem_req_key_lane`。
3. **`request_key` 展平**：golden `(inst_id, lane, candidate_seq)`
   → `{key_inst_id, key_lane, key_seq}`；`candidate_seq` per-lane、
   instruction 开始清零。功能匹配按 exact range（SRC-05 sec 9.2
   规则 4），key 仅供 MEM echo/error 关联。
4. **`source_fragments[]` = `(addr,len)` 连续 range**（§7），语义同
   golden `source_ranges`。
5. **`load_type` 由 lane 派生**（LOAD_A/AMX/B/BMX，SRC-06 sec 5.1）；
   **`o_mem_req_ready` ≡ `i_shared_mem_ready`**（同一 MEM 准入口，
   SRC-01 sec 3.1 与 SRC-06 sec 5/10 的命名差）。
6. **golden 专有字段不携带**：`n_block_step`（4EU 恒 1）、
   `replica_count`（恒 1，SRC-04 sec 10.2 遗留字段）、
   `rd_queue_depth` 兼容字段（no-op，SRC-01 sec 6）均不进端口。
7. **`o_lfsm_idle` 观察端口**：规格未命名，属 TB/系统集成 drain
   观察字段（性质同类 `walk_stall` 兼容观察字段，SRC-01 sec 3.2）；
   不影响任何功能契约。
8. **WalkConfig 只携带原始规模计数，loop 几何由 walker 现场维护**
   （2026-10-13 用户决策）：`n_blocks[]` / `n_outer_count` /
   `k_step_per_outer` / `k_outer_count` 不下发（相对 SRC-04 sec 2.1
   契约的偏差，信息内容由 walker 加法级生成等价保持：N block 生成
   规则 `remaining==9/10→4、否则 min(8,remaining)`（SRC-02
   sec 3.5.2）、K outer `k_count=min(k_step, k_groups−k_base)`
   （SRC-02 sec 3.5.3）、`k_step=m_mode?4:8`、loop 结束以
   `base≥total` 判定）。每拍计算复杂度保持加法级（无除法器、无
   n_blocks 查表数组）；与 golden 含这些字段的 `WalkConfig`
   （REF-05）的等价性由 MKN 序列逐拍对拍闭环（FEATURE_LIST
   F-010）。ASSUMPTIONS A-005.1 相应改写（v3）。

## 9. 子模块 prefix / key 规范

层次化 `domain.call()` 链与 prefix 级联（PRC-01 §7；计划「模块
分解」）：

| 子模块函数 | prefix | 职责 | 实例数 |
| :--- | :--- | :--- | :--- |
| `lfsm_top` | `lfsm` | 顶层组合、配置通道、观察输出 | 1 |
| `config_regs` | `lfsm_cfg` | 配置 FIFO、配对握手、配置寄存 | 1 |
| `walker` | `lfsm_wlk` | MKN FSM、counter、walk_seq、loop base/length 加法级维护（§8 适配 8） | 1 |
| `rdgen` | `lfsm_rdg` | 首访去重、owner/`rdgen_id`、地址、原子批量入队、LaneLoadEnd、C key | 1 |
| `rd_queue` | `lfsm_q_{a,amx,b,bmx}` | per-lane FIFO（寄存状态） | 4 |
| `assembler_{a,b,amx,bmx}` | `lfsm_asm_{a,b,amx,bmx}` | per-lane merge context + DataBlock 展开 | 4（几何各异） |
| `cand_holder` | `lfsm_chd_{a,amx,b,bmx}` | candidate 持有/形成/递补 + seq/planned 锁存（对应规格 BandwidthPacker；2026-10-14 改名） | 4（同构） |
| `tag_checker` | `lfsm_tck` | per-lane load_ptr ring、binding、query/eligibility（对应规格 DestinationAllocator；2026-10-14 改名） | 1 |
| `arbiter` | `lfsm_arb` | 优先键 + RR + fire 选择控制（纯控制；eligibility 含 `issue_room`；payload 由顶层 mux 组装入发送队列，Step 6 §11A/§11B，A-014） | 1 |
| `req_sched` | `lfsm_rqp` | 2-slot 发送队列：request + `LoadPtrUpdate` 同组，issue 拍原子发出；`issue_room` 反压回仲裁侧（A-014/GAP-07） | 1 |
| `c_path` | `lfsm_c` | C FIFO + `RegisterRequest(C)` | 1 |

各子模块 `inputs` 字典键 / 返回 `outs` 键在 Step 6
`ALGORITHM_CYCLE_AWARE_PSEUDOCODE.md` 逐键冻结（位宽以本文件 §3/§4
为准）；顶层端口 key 以本文件 §4 为准。

## 10. 存储分类（Step 3 action 6）

按 A-007：**全部**队列/FIFO/寄存器组使用 `domain.signal()` 数组 +
head/tail pointer（小并行寄存器组），不使用 `m.fifo` / `m.rv_queue`
/ `m.sync_mem` 原语；无大容量单端口结构（数据通路不存数据，只存
metadata）。若后续评估改用 `m.fifo`，须先按
`AGENTS.md`/`docs/updatePLAN.md` gate-first 验证其 V6 语义，不做
backend-only 绕过。

| 结构 | 实现 | 尺寸 |
| :--- | :--- | :--- |
| WalkConfig / LFSMInstructionConfig 配置 FIFO | `domain.signal` 数组 + ptr | 2 × `CFG_FIFO_DEPTH` |
| 配置寄存（`m_mode`/`m_slice_count`/`n_hw_count`/`k_groups`/地址范围等） | `domain.signal` 标量/小组 | §4.1/§4.2 |
| walker loop base/length 寄存（`n_base`/`n_len`、`k_base`/`k_count`） | `domain.signal` 标量组 | 加法级维护（§8 适配 8） |
| 四路 RD Queue | `domain.signal` 数组 + head/tail | `RDQ_{A,B,AMX,BMX}_DEPTH` |
| Assembler merge/expansion context（B pair / AMX K-run / A expansion / BMX 窗口池） | `domain.signal` 组 | 几何常量；BMX 2 窗口 × 32 slot |
| held candidate（每 lane 1 个） | `domain.signal` 组 | 4 |
| req_sched 发送队列（payload+update 全字段副本） | `domain.signal` 组 | 2 slot（A-014） |
| binding / allocation group | `domain.signal` 组 | 每 lane 当前 group |
| load_ptr / rr_cursor / `rd_id` / `rdgen_id` 序号 | `domain.signal` | 标量/小向量 |
| C FIFO | `domain.signal` 数组 + ptr | `C_FIFO_DEPTH` |

## 11. 端口 → 需求/假设钩子

| 端口/总线 | R-xx | A-xxx |
| :--- | :--- | :--- |
| `walk_cfg` / `lfsm_cfg` | R-01, R-02, R-04 | A-005, A-010 |
| `buf_query` | R-20 | A-004 |
| `buf_update` | R-19, R-22, R-23 | A-003 |
| `mem_req` | R-21, R-22, R-24, R-25 | A-003, A-006(v2)/A-014（GAP-07） |
| `reg_c` | R-29 | A-002 |
| `obs` | R-05 | A-009 |
| （内部）队列/池深度 | R-09, R-32, R-35 | A-002, A-011 |
| （内部）evaluate/commit 相位 | R-11, R-34 | A-008 |
