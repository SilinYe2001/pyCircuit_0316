# LFSM (4EU UU mode) TRACEABILITY

> Step 7 交付物（依据 `docs/pycircuit_implementation_method.md` Step 7：
> 端口覆盖矩阵 + 功能覆盖矩阵 + 显式 gap 列表；「从转换后的 Markdown
> …」§1 order-8）。建立日期：2026-10-13。
> 端口契约见 `PORT_LIST.md`；功能编号（F-xxx）见 `FEATURE_LIST.md`；
> 测试编号（T-xxx）在本文件 §0 划定号段、完整定义见 `TEST_PLAN.md`；
> 决策编号（A-xxx）见 `ASSUMPTIONS.md`；需求编号（SRC-xx/R-xx）见
> `REQUIREMENT_SOURCES.md`。范围：4EU UU mode（Shared MEM baseline）
> + UU C-only 路径。

## 0. 编号与锚点约定

- **T-xxx 号段**（TEST_PLAN 完整定义；括号内为该号段条数）：
  T-001…T-006 reset（6）；T-010…T-013 smoke（4）；
  T-020…T-065 directed 单元（46）；T-066…T-069 directed 小集成（4）；
  T-070…T-077 directed 集成·回放式（8）；
  T-080…T-086 stress（7）；T-090…T-097 corner（8）；
  T-100…T-103 system（Step 10 预览，4）。
- **伪码锚点**：`CPS::<fn>` = `ALGORITHM_CYCLE_AWARE_PSEUDOCODE.md`
  （Step 6）中子模块函数节；`SEQ::<name>` / `PIPE::<fn>` 为 Step 4/5
  文档同名子程序节。子模块函数名冻结于 `PORT_LIST.md` §9
  （`config_regs` / `walker` / `rdgen` / `rd_queue` /
  `assembler_{a,b,amx,bmx}` / `cand_holder` / `tag_checker` / `arbiter` /
  `c_path` / `req_sched` / `lfsm_top`；2026-10-14 改名：`packer`→`cand_holder`、
  `allocator`→`tag_checker`，语义/接口不变）。Step 6 已落盘，锚点
  于 2026-10-14 核对完毕并同步本文件（**GAP-03 已关闭**）。
  `RdMemRequest` payload 的 4:1 组装位于 `CPS::lfsm_top` **§11A**，
  端口直出位于 `CPS::req_sched` **§11B**（A-014 发送队列，issue 拍）
  （arbiter 仅输出 `fire/grant_lane/fire_consume` 纯控制）；
  顶层端口发射（`m.output`/`submodule_input` 声明）亦位于
  `CPS::lfsm_top`，矩阵「伪码落点」列按此归属。
- **R-xx 覆盖**：R-01…R-36 经 `FEATURE_LIST.md` §6 全部映射到
  F-xxx；本文件功能矩阵覆盖全部 44 个 F-xxx，故 R-xx 覆盖随之闭合，
  不再单列第三张矩阵。
- **标题核对 parity**：`FEATURE_LIST.md` §4 对 SRC-01 的 36 行标题
  全部落到 F-xxx 或 —；§2 功能矩阵覆盖全部 F-xxx，即标题核对表无
  未决行。

## 1. 端口覆盖矩阵（PORT_LIST §4 全键 → 伪码 → F-xxx → T-xxx）

### 1.1 WalkConfig 通道（PORT_LIST §4.1）

| 端口 key | 伪码落点 | F-xxx | T-xxx |
| :--- | :--- | :--- | :--- |
| `i_walk_cfg_valid` | `CPS::config_regs`（配置 FIFO enq/accept） | F-001, F-003 | T-020, T-022, T-003 |
| `o_walk_cfg_ready` | `CPS::config_regs`（FIFO 非满组合） | F-001 | T-020, T-022 |
| `i_walk_cfg_inst_id` | `CPS::config_regs`（head 配对比较） | F-001 | T-020, T-021 |
| `i_walk_cfg_m_mode` | `CPS::config_regs`（寄存）→ `CPS::walker`（`k_step` 1-bit mux） | F-002, F-010 | T-023, T-024, T-025 |
| `i_walk_cfg_m_slice_count` | `CPS::config_regs`（寄存 + 断言 ≤2）→ `CPS::walker` | F-002 | T-023, T-025 |
| `i_walk_cfg_n_hw_count` | `CPS::config_regs`（寄存）→ `CPS::walker`（N block 加法级生成） | F-002, F-010 | T-023, T-025 |
| `i_walk_cfg_n_step` | `CPS::config_regs`（断言 ==1，保留端口） | F-002 | T-023 |
| `i_walk_cfg_k_groups` | `CPS::config_regs`（寄存 + 断言 ≤32）→ `CPS::walker`（K outer 生成） | F-002, F-010 | T-023, T-025 |

### 1.2 LFSMInstructionConfig 通道（PORT_LIST §4.2）

| 端口 key | 伪码落点 | F-xxx | T-xxx |
| :--- | :--- | :--- | :--- |
| `i_lfsm_cfg_valid` | `CPS::config_regs`（配置 FIFO enq/accept） | F-001, F-003 | T-020, T-022, T-003 |
| `o_lfsm_cfg_ready` | `CPS::config_regs`（FIFO 非满组合） | F-001 | T-020, T-022 |
| `i_lfsm_cfg_inst_id` | `CPS::config_regs`（head 配对比较） | F-001 | T-020, T-021 |
| `i_lfsm_cfg_eu_mode` | `CPS::config_regs`（断言 ==0，8EU 拒收） | F-002 | T-023 |
| `i_lfsm_cfg_data_type` | `CPS::config_regs`（寄存）→ `CPS::rdgen` / `CPS::assembler_*`（几何选择） | F-002 | T-023, T-096 |
| `i_lfsm_cfg_mx_mode_en` | `CPS::config_regs` → `CPS::rdgen`（AMX/BMX gate、required_lanes） | F-002, F-020, F-024 | T-023, T-035, T-096 |
| `i_lfsm_cfg_mx_bytes_per_k0` | `CPS::config_regs` → `CPS::rdgen`（span/地址推导） | F-002, F-023 | T-023, T-096 |
| `i_lfsm_cfg_n_hw_count` | `CPS::config_regs` → `CPS::rdgen`（C 地址 `m×n_hw+n`） | F-025 | T-031 |
| `i_lfsm_cfg_a_base_addr` / `i_lfsm_cfg_a_limit_addr` | `CPS::config_regs` → `CPS::rdgen`（A 线性地址 + 越界断言） | F-023 | T-034 |
| `i_lfsm_cfg_a_mx_base_addr` / `i_lfsm_cfg_a_mx_limit_addr` | `CPS::config_regs` → `CPS::rdgen`（AMX tile-major 地址） | F-023 | T-034 |
| `i_lfsm_cfg_b_base_addr` / `i_lfsm_cfg_b_limit_addr` | `CPS::config_regs` → `CPS::rdgen`（B 线性地址） | F-023 | T-034 |
| `i_lfsm_cfg_b_mx_base_addr` / `i_lfsm_cfg_b_mx_limit_addr` | `CPS::config_regs` → `CPS::rdgen`（BMX 行线性 pair 地址） | F-023 | T-034 |
| `i_lfsm_cfg_l0c_base_addr` | `CPS::config_regs` → `CPS::rdgen`（C 地址预计算） | F-025 | T-031 |

### 1.3 Buf/RAM 接口（PORT_LIST §4.3）

| 端口 key | 伪码落点 | F-xxx | T-xxx |
| :--- | :--- | :--- | :--- |
| `o_load_range_query_valid[4]` | `CPS::tag_checker`（由 `CPS::cand_holder` held 快照的 `planned_*` 派生；split 续写 valid=0） | F-083, F-082 | T-056, T-057 |
| `o_load_range_query_base[4]` | `CPS::tag_checker`（`planned_base`，load_ptr ring 轨迹） | F-083, F-080 | T-054, T-057 |
| `o_load_range_query_advance[4]` | `CPS::tag_checker`（`planned_advance` ≤32） | F-083 | T-057 |
| `i_load_range_idle[4]` | `CPS::tag_checker`（`destination_ok` 每拍重算）→ `CPS::arbiter`（eligibility 组成） | F-083, F-090 | T-057, T-069, T-080 |
| `o_load_ptr_update_valid` | `CPS::tag_checker`（grant 拍 commit）→ `CPS::req_sched` §11B（issue 拍脉冲，与 `o_mem_req_valid` 同拍原子） | F-092, F-093 | T-060, T-061 |
| `o_load_ptr_update_lane` | `CPS::tag_checker` → §11B | F-093 | T-061 |
| `o_load_ptr_update_old_ptr` | `CPS::tag_checker`（ring 推进前值）→ §11B | F-093 | T-061 |
| `o_load_ptr_update_new_ptr` | `CPS::tag_checker`（`(old+advance) % DEPTH[lane]`）→ §11B | F-093 | T-061 |
| `o_load_ptr_update_advance` | `CPS::tag_checker`（1..32；split 续写不产生 update） | F-093, F-082 | T-061, T-056 |

### 1.4 MEM 接口（PORT_LIST §4.4）

| 端口 key | 伪码落点 | F-xxx | T-xxx |
| :--- | :--- | :--- | :--- |
| `i_shared_mem_ready` | `CPS::req_sched` §11B（issue 拍 pop 准入；A-014/GAP-07——不再进 arbiter eligibility） | F-090 | T-058, T-081 |
| `i_mem_source_ok[4]` | `CPS::arbiter`（eligibility 组成，per-lane） | F-090 | T-058, T-082 |
| `o_mem_req_valid` | `CPS::req_sched` §11B（front && `i_shared_mem_ready`，issue 拍单拍脉冲；同一拍与 `LoadPtrUpdate` 原子发出，A-014/GAP-07） | F-090, F-092 | T-058, T-060 |
| `o_mem_req_key_inst_id` | `CPS::cand_holder`（held `inst`）→ §11A（mux）→ `CPS::req_sched` §11B（issue 拍；request_key 展平 §8 适配 3） | F-092, F-094 | T-063 |
| `o_mem_req_key_lane` | `CPS::lfsm_top` §11A（=grant_lane）→ `CPS::req_sched` §11B；兼派生 `load_type`（§8 适配 5） | F-092, F-094 | T-063 |
| `o_mem_req_key_seq` | `CPS::cand_holder`（held `cand_seq`，per-lane per-instruction）→ §11A → §11B | F-094, F-021 | T-063 |
| `o_mem_req_rd_mem_id` | `CPS::cand_holder`（held `rd_mem_id`=首 block `rdgen_id`）→ §11A → §11B | F-072 | T-052 |
| `o_mem_req_src_addr[32]` | `CPS::assembler_*`（fragment source ranges 元数据视图）→ §11A（定长展平 mux）→ `CPS::req_sched` §11B（issue 拍） | F-094 | T-062 |
| `o_mem_req_src_len[32]` | 同上（每 range ≤128B） | F-094 | T-062 |
| `o_mem_req_src_count` | 同上（0..32） | F-094 | T-062 |
| `o_mem_req_load_byte_count` | `CPS::assembler_*`（Σ blocks transport 字节账目）→ §11A → §11B（≤128） | F-070, F-094 | T-062 |
| `o_mem_req_valid_byte_count` | `CPS::assembler_*`（含 AMX/BMX mem-pad，MEM-read 口径）→ §11A → §11B | F-041, F-061, F-067, F-094 | T-062 |
| `o_mem_req_padding_byte_count` | `CPS::assembler_*`（纯 transport fill 账目）→ §11A → §11B | F-041, F-094 | T-062 |
| `o_mem_req_wr_index[32]` | `CPS::assembler_*`（wr 视图；index 基址=`CPS::tag_checker` dest_base）→ §11A → §11B | F-081, F-094 | T-062 |
| `o_mem_req_wr_offset[32]` | `CPS::assembler_*`（slot 内字节偏移，wr 视图）→ §11A → §11B | F-094 | T-062 |
| `o_mem_req_wr_len[32]` | `CPS::assembler_*`（连续写字节，wr 视图）→ §11A → §11B | F-094 | T-062 |
| `o_mem_req_wr_count` | `CPS::assembler_*` → §11A → §11B（≤32，A-003） | F-094 | T-062 |
| `o_mem_req_tag_range_base` | `CPS::tag_checker`（dest_base）→ §11A → §11B（定长 1；split 复用首笔 range） | F-093, F-094 | T-061, T-062 |
| `o_mem_req_tag_range_count` | `CPS::tag_checker`（tag_cnt，1..32）→ §11A → §11B | F-093, F-094 | T-061, T-062 |
| `o_mem_req_tag_range_confirm` | `CPS::assembler_*`（group_final 组合）→ §11A → §11B（仅整 range 末贡献 request 置 1） | F-094 | T-062 |
| `o_mem_req_is_partial_beat` | `CPS::assembler_*`（view flag；D-003 UU 恒 0；BMX 恒满）→ §11A → §11B | F-071 | T-051 |
| `o_mem_req_is_instruction_last` | `CPS::assembler_*`（end tag 比对 view，本 lane 末笔）→ §11A → §11B | F-071 | T-051 |

### 1.5 RegisterUnit C-only 接口（PORT_LIST §4.5）

| 端口 key | 伪码落点 | F-xxx | T-xxx |
| :--- | :--- | :--- | :--- |
| `i_register_ready` | `CPS::c_path`（issue 唯一准入） | F-100 | T-064, T-083 |
| `o_reg_req_valid` | `CPS::c_path`（C FIFO head valid，未 fire 保持） | F-100 | T-064 |
| `o_reg_req_inst_id` | `CPS::rdgen`（C key inst）→ `CPS::c_path` | F-025, F-100 | T-031, T-064 |
| `o_reg_req_rdgen_id` | `CPS::rdgen`（首访 token `walk_seq+1`）→ `CPS::c_path` | F-025, F-100 | T-031, T-064 |
| `o_reg_req_m_idx` | `CPS::rdgen`（C key `(inst,m,n)` 之 m）→ `CPS::c_path` | F-025, F-100 | T-031 |
| `o_reg_req_n_idx` | `CPS::rdgen`（之 n）→ `CPS::c_path` | F-025, F-100 | T-031 |
| `o_reg_req_src_addr` | `CPS::rdgen`（`l0c_base+(m×n_hw+n)×16` 预计算）→ `CPS::c_path` | F-025, F-100 | T-031 |

### 1.6 观察输出与复位（PORT_LIST §4.6 + §2）

| 端口 key | 伪码落点 | F-xxx | T-xxx |
| :--- | :--- | :--- | :--- |
| `o_walk_stall` | `CPS::walker`（stall 通路 tie-off）→ `CPS::lfsm_top`（恒 0） | F-011 | T-011, T-027 |
| `o_lfsm_idle` | `CPS::lfsm_top`（聚合四路 Queue/Assembler context/held candidate/req_sched 队列/C FIFO/walker 空；A-014 含 `rqp_empty`） | F-120 | T-001, T-013, T-103 |
| domain `reset`（非数据端口，PORT_LIST §2） | 全体子模块 `domain.signal(reset_value=…)` + reset 分支 | F-003 | T-001…T-006 |

端口覆盖结论：PORT_LIST §4 全部 65 个端口 key + domain reset 均
落到伪码子模块、F-xxx 与 ≥1 个 T-xxx，无未覆盖端口。

## 2. 功能覆盖矩阵（44 个 F-xxx → 伪码 → T-xxx）

### 2.1 配置与控制（CFG）

| F-ID | 伪码落点 | T-xxx（directed / 回归） | 备注 |
| :--- | :--- | :--- | :--- |
| F-001 | `CPS::config_regs`（配对握手） | T-020, T-021, T-022, T-003, T-093 | T-021 为协议错误断言负例 |
| F-002 | `CPS::config_regs`（寄存+结构断言）；`CPS::walker`（loop 现场生成终值自检） | T-023, T-025 | T-023 逐条非法结构负例 |
| F-003 | 全体子模块 reset 分支 | T-001…T-006 | 含中途 reset/reset 期间握手忽略 |

### 2.2 Walker（WLK）

| F-ID | 伪码落点 | T-xxx | 备注 |
| :--- | :--- | :--- | :--- |
| F-010 | `CPS::walker`（MKN FSM + 加法级 base/length） | T-024, T-025, T-026, T-090, T-091, T-092 | 逐拍对拍 golden `MknWalkFSM` 序列；含 9/10/17 N tail 与 K 尾 outer |
| F-011 | `CPS::walker`（stall tie-off）→ `CPS::lfsm_top` | T-011, T-027 | `o_walk_stall==0` 恒成立断言 |
| F-012 | `CPS::config_regs` + `CPS::walker`（done/重启链路） | T-028, T-075, T-093 | 启动拍以 golden 对拍冻结；b2b 向量 |

### 2.3 RdGenerator（RDG）

| F-ID | 伪码落点 | T-xxx | 备注 |
| :--- | :--- | :--- | :--- |
| F-020 | `CPS::rdgen`（计数器条件去重，A-001） | T-029, T-030, T-071 | m16/m32 × 单/多 n_outer × K outer 重访矩阵；T-071 = m32 return-base 不重载回归 |
| F-021 | `CPS::rdgen`（`rd_id`/`rdgen_id` 序号） | T-032, T-063 | reuse token 占号、stall 保持 |
| F-022 | `CPS::rdgen`（原子批量入队 commit） | T-029, T-033 | 无 partial batch 断言；B4 每 token ≤1 B owner（sec 17 条 2/22）T-029 单元级断言 |
| F-023 | `CPS::rdgen`（四路地址生成 + 越界 TB 断言） | T-034, T-048 | 越界断言负例进 T-034 |
| F-024 | `CPS::rdgen`（LaneLoadEnd 生成，required_lanes） | T-035, T-049, T-090 | 非 required lane Queue 恒空断言 |
| F-025 | `CPS::rdgen`（C key 去重 + 地址预计算） | T-031 | 对拍 golden `ru_c_queue` 入队侧 |

### 2.4 四路 RD Queue（Q）

| F-ID | 伪码落点 | T-xxx | 备注 |
| :--- | :--- | :--- | :--- |
| F-030 | `CPS::rd_queue` ×4 | T-036, T-076 | `enqueue−dequeue==size` 不变量入 T-076 套件 |
| F-031 | `CPS::rd_queue`（拍末 commit 次拍可见） | T-037, T-065, T-067 | 对齐 `LFSM-TIME-01` 口径 |
| F-032 | `CPS::rd_queue` / `CPS::c_path` / `CPS::assembler_bmx`（参数化深度 + never-full 断言） | T-038, T-074, T-085, T-086 | T-074 = B 在途峰值包络锚点；包络外 worst-legal 为 GAP-02 waiver；req_sched 2-slot 属**流控结构**（cnt≤2 由 issue_room 反压，T-081/T-085 监视），非 never-full 对象 |

### 2.5 Assembler（ASM 公共 + 四 lane）

| F-ID | 伪码落点 | T-xxx | 备注 |
| :--- | :--- | :--- | :--- |
| F-040 | `CPS::assembler_{a,b,amx,bmx}`（merge/padding 优先级 + context 保持） | T-040, T-041, T-043, T-044, T-049 | 对齐 `LFSM-ASM-02` 口径 |
| F-041 | `CPS::assembler_*`（padding 语义 + 字节守恒） | T-042, T-045, T-047, T-076 | `valid+padding==block` 入 T-076 套件 |
| F-050 | `CPS::assembler_a`（默认序 `EU_M_HALF_K_HALF`） | T-039, T-040, T-077 | 非默认两序未验证 → **GAP-01** waiver |
| F-055 | `CPS::assembler_b`（N4 pair merge） | T-041, T-092, T-074 | pair 不跨 N block（REQUIREMENT_SOURCES §4.1）；T-074 = B4 N8 block 边界回归 |
| F-056 | `CPS::assembler_b`（奇数 N 尾 padding） | T-042, T-072 | 128 valid + 128 pad 账目对拍 |
| F-060 | `CPS::assembler_amx`（K-run 跨 K-outer merge） | T-044, T-096, T-073 | Queue bubble 不截断；T-073 = MXFP8 K4 dense merge 回归 |
| F-061 | `CPS::assembler_amx`（K 尾 tile mem-pad） | T-045, T-096 | mem-pad 计 valid、无 owner/tag/write |
| F-065 | `CPS::assembler_bmx`（固定几何窗口 + 窗口池 2） | T-046, T-049, T-073 | 完成序对拍 golden `_emit_ready_bmx_windows` |
| F-066 | `CPS::assembler_bmx`（transport padding slot） | T-047 | 任意窗口位置、无副作用 |
| F-067 | `CPS::assembler_bmx`（mem-pad 块量化） | T-048, T-096 | N2 pair / K 尾 pad row 地址对拍 |

### 2.6 BandwidthPacker（PCK）

| F-ID | 伪码落点 | T-xxx | 备注 |
| :--- | :--- | :--- | :--- |
| F-070 | `CPS::assembler_*`（visible ≥ full_count 判定）+ `CPS::cand_holder`（held 形成捕获） | T-050 | `full_count` A/B=1、AMX/BMX=4 |
| F-071 | `CPS::assembler_*`（末笔 partial 视图）+ `CPS::cand_holder`（held） | T-051, T-068 | BMX 恒满；**D-003：UU 128B 下 partial 结构性不可达**——T-051 为登记式断言（`is_partial≡0` sva + 末笔 `is_instruction_last`） |
| F-072 | `CPS::cand_holder`（held `rd_mem_id`）+ `CPS::assembler_*`（组帧规则视图） | T-052 | split 沿用 / merge 取最早 |
| F-073 | `CPS::cand_holder`（held candidate；边2 当拍形成、**边3 严格流水**——GAP-06：形成拍不 fire、链首 +1、replacement 链 1 fire/拍） | T-053, T-066 | 每 lane 恰 1 held；未 grant 保持；链首 +1 拍 |

### 2.7 DestinationAllocator（ALC）

| F-ID | 伪码落点 | T-xxx | 备注 |
| :--- | :--- | :--- | :--- |
| F-080 | `CPS::tag_checker`（load_ptr ring 顺序分配） | T-054 | 回卷以 candidate range tag state 为准 |
| F-081 | `CPS::tag_checker`（binding/span 建立） | T-055, T-073 | 每 owner 恰一次 binding；T-073 = MX span 原子分配回归 |
| F-082 | `CPS::tag_checker`（split 复用） | T-056, T-062, T-094 | `planned_advance=0` 不查 destination |
| F-083 | `CPS::tag_checker`（`destination_ok` 查询相位） | T-057, T-069, T-080, T-094, T-095 | A-004 相位契约（valid=0 ⇒ idle=1） |

### 2.8 ReadArbiter 与原子提交（ARB）

| F-ID | 伪码落点 | T-xxx | 备注 |
| :--- | :--- | :--- | :--- |
| F-090 | `CPS::arbiter`（eligibility 组成：`cand_valid && issue_room && source_ok && dest_ok`，A-014/GAP-07） | T-058, T-080, T-081, T-082, T-084 | 每拍 ≤1 grant 断言；`issue_room` 来自 `CPS::req_sched` |
| F-091 | `CPS::arbiter`（优先键 + RR） | T-004, T-059, T-084 | reset cursor=A；fire 才更新 |
| F-092 | **grant 拍**：`CPS::arbiter`（grant/RR）+ `CPS::tag_checker`（load_ptr/range commit）+ `CPS::cand_holder`（consume/递补）+ `CPS::assembler_*`（游标推进）；**issue 拍**：`CPS::req_sched` §11B（request+`LoadPtrUpdate` 同拍原子发出，A-014/GAP-07） | T-060 | A-006 v2：采纳发送段（推翻 v1 不采纳） |
| F-093 | `CPS::tag_checker`（`LoadPtrUpdate` ↔ 唯一 exact range，grant 拍 commit）→ `CPS::req_sched` §11B（issue 拍随 request 原子发出） | T-061, T-095 | 对齐 `LFSM-RANGE-01`/`BUF-VIS-02` |
| F-094 | `CPS::assembler_*`（src/wr 视图）+ `CPS::tag_checker`（tag 组）+ `CPS::lfsm_top` §11A（组装）→ `CPS::req_sched` §11B（发出） | T-062, T-063 | writes ≤32 / advance ≤32 / ranges==1 断言（A-003） |

### 2.9 C-only register 路径（C）

| F-ID | 伪码落点 | T-xxx | 备注 |
| :--- | :--- | :--- | :--- |
| F-100 | `CPS::c_path`（C FIFO + `RegisterRequest(C)`） | T-005, T-012, T-064, T-065, T-083 | 无竞争仲裁；`register_ready` 反压保持；T-005 = reset 清 C FIFO |

### 2.10 横切规则（XCUT）与观察（OBS）

| F-ID | 伪码落点 | T-xxx | 备注 |
| :--- | :--- | :--- | :--- |
| F-110 | `CPS::assembler_*` / `CPS::cand_holder`（drain）+ `CPS::rdgen`（边界标记） | T-002, T-043, T-049, T-068, T-075, T-097, T-101 | 不跨 instruction 合并断言；T-097 = b2b 异几何混叠（D-002 注解专项） |
| F-111 | 全体子模块（reset > 保持 > 最老 > 新工作优先级表） | T-006, T-084, T-101 | 冲突场景选择顺序对拍 |
| F-112 | TB 断言套件（**全部落 TB/sva，不进硬件**，2026-10-13 决策）：内部条目→单元/集成 TB；外部条目（#14/#20）→集成 TB stub 侧 | T-076, T-100, T-102 | sec 17 UU 条 1–22；23–25 RU 条出界 |
| F-113 | 全体子模块（evaluate/commit 两拍映射，A-008） | T-036, T-053, T-080, T-081 | 未握手保持清单逐拍断言 |
| F-120 | `CPS::lfsm_top`（idle 聚合） | T-001, T-013, T-103 | P1 观察字段；idle 组成含 cfg FIFO 与发送队列空（A-014 `rqp_empty`，CYCLE §13） |

功能覆盖结论：44 个 F-xxx 全部落到伪码子模块且各有 ≥1 个
regression-sensitive T-xxx；无「TBD 无日期」条目，两个已决策偏差
记入 §3 gap 表。

## 3. Gap 列表（显式登记；空项不得静默省略）

| GAP | 类型 | 日期 | 关联 | 陈述与处置 |
| :--- | :--- | :--- | :--- | :--- |
| GAP-01 | 已决策 waiver | 2026-10-13 | F-050；A 块序 | 本轮只实现/验证默认 `a_block_order=EU_M_HALF_K_HALF`；`EU_K_HALF_M_HALF` / `M_HALF_K_HALF_EU` 两序为**未验证功能**（静态参数保留三值枚举，启用时不改端口）。处置：后续启用时补 assembler_a 定向 T-xxx 并重跑全量回归；sign-off 前本行须保持可见。 |
| GAP-02 | 已决策 waiver | 2026-10-13 | F-032；A-002/A-011 | 有界实现（RDQ A16/B128/AMX8/BMX4+窗口池2/C8）与规格「无上限队列」语义仅在 **TYPICAL 包络 + 有限长反压**内等价；worst-legal 形状（在途实测 A 60 / B 513 / AMX 61）显式排除在 never-full 保证之外。处置：深度为参数，覆盖全合法形状只需调参（A 64 / B 1024 / AMX 64）不改结构；SYSTEM_TEST 记录包络与 waiver 状态。 |
| GAP-03 | 已关闭 | 2026-10-13 开、2026-10-14 关 | 全矩阵「伪码落点」列 | Step 4-6 三份算法文档已落盘；锚点核对完成，本文件同步了改名（cand_holder/tag_checker）、payload 归属（`CPS::lfsm_top` §11A → `CPS::req_sched` §11B，GAP-07）与边3 时序（见 GAP-06）。 |
| GAP-04 | 已关闭 | 2026-10-13 开、2026-10-14 关 | T-010, T-070…T-077, T-086, T-091, T-096, T-097 | golden 向量（`tools/dump_lfsm_golden.py` + `vectors/`）是回放式集成测试与向量驱动单元测试的输入。2026-10-14 向量已落盘并冻结 `lfsm_golden_vector` schema v1：7 个全量回放用例（TC02/08/13/15/17 + TC-B2B-01/02，顶层逐拍向量 + 单元流）+ 8 个 A-002 占用插桩应力形状（X-MAXK/X-HIF4/X-MXFP4/X-MAXN/X-WORST-A/X-WORST-AMX/X-WORST-B-m16/X-WORST-B-m32），15/15 PASS（模型 checker 全绿、A-003 三上限逐 fire 断言、walker 流与独立 `MknWalkFSM` 逐拍等价）；探针 B 实测与 A-002 v2 记录全部一致（TC02 B=46、TC08 A=10、TC15 AMX=6/BMX=34、TC17 B=64、X-WORST A=60/AMX=61/B-m16=513），峰值汇总 `vectors/occupancy_summary.json`。处置：上述 T-xxx 现可按 §0.4 口径进入首次跑绿（Step 9 增量挂钩）；向量再生成须保持 schema v1 兼容或升版并同步本行。 |
| GAP-05 | 信息注记（非缺口） | 2026-10-13 | F-112；R-28 | sec 17 条 14（confirmation 不拆分）/条 20（回卷不覆盖 `loading/rdy`）依赖 Buf/RAM tag 与 MEM 可见性，LFSM 单元级不可断言；已映射到集成 TB 反应式 stub 侧断言（T-095/T-100），非覆盖缺口，登记以免误读为遗漏。 |
| GAP-06 | 规格偏差（DEV-2026-10-14；ASSUMPTIONS 预登记 A-013） | 2026-10-14 | F-073；R-11；T-053/T-066/T-070…T-077 回放口径 | **边3 严格流水**：SRC-01 sec 5「Packer→Arbiter 允许同拍 bypass」不再采纳——仲裁输入束只认 held 快照寄存；fresh candidate 形成拍不 fire，replacement 链维持每拍 1 grant；held 快照一致性（held valid ⇒ asm 视图 == held 内容）为 sva。处置：golden 对拍口径＝逐笔 fire 元数据等价 + 链首相移（与 GAP-07 相移叠加为 +2 拍/链首）；TEST_PLAN §0.2/§0.4、T-053/T-066 已随更新；sign-off 前保持可见；回退须回 PIPE §3/CYCLE §9/TEST_PLAN 同步撤销。 |
| GAP-07 | 规格偏差（DEV-2026-10-14；**A-014，推翻 A-006 v1**） | 2026-10-14 | F-090/F-092/F-093/F-120；R-22/R-25；T-058/T-060/T-061/T-062/T-070…T-077 | **发送段 req_sched**：grant 与 MEM 下发解耦——§11A mux 载荷（`RdMemRequest`+`LoadPtrUpdate` 同组）经 2-slot 发送队列在 issue 拍（grant 次拍）原子发出；相对 SRC-01 sec 13「`rd_mem_fire` 拍端口即发」为**端口时序偏差**（内部 grant commit 照旧原子；端口「update+request 同拍」原子关系原样保留，sec 14.1 时序图口径不变）；`i_shared_mem_ready` 落位 issue 拍，eligibility 改 `issue_room`，深度 2 保 ready 稳态 1 issue/拍。处置：ASSUMPTIONS A-006 v2/A-014、PORT_LIST §4.3/§4.4/§5.3/§5.5/§9/§10、PIPE §3/§8.1、CYCLE §11A/§11B/§13/§14、SEQ §10/§12/§14.3/§15（D-007）、TEST_PLAN 已随更新；sign-off 前保持可见；回退同上全文撤销。 |

## 4. 维护规则

1. SRC-01 标题新增/重命名 → 先更新 `FEATURE_LIST.md` §4 核对表，
   再回本文件 §2 增行或登记新 GAP（方法 §2.4）。
2. 任一 F-xxx 的 T-xxx 集合在 TEST_PLAN 变更后，回本文件 §2 同步；
   sign-off（Step 10）要求 §2 无空 T-xxx 单元格、§3 仅剩已决策
   waiver 行（GAP-01/GAP-02）且状态显式。
3. T-xxx 定义以 `TEST_PLAN.md` 为唯一权威；本文件只引用 ID。
4. 发现 V6 原语缺口（如 `m.fifo` 语义）不走本文件，按
   `AGENTS.md`/`docs/updatePLAN.md` gate-first 停下处理（A-007）。
