# LFSM (4EU UU mode) FEATURE_LIST

> Step 3 交付物（依据 `docs/pycircuit_implementation_method.md` Step 3
> action 4 与「从转换后的 Markdown …」§2）。把规格分解为可测试功能
> （F-001…），并给出：转写稿索引、SRC-01 全标题核对表、功能→测试
> 摘要。建立日期：2026-10-13。
> 需求编号（SRC-xx/R-xx）见 `REQUIREMENT_SOURCES.md`；决策编号
> （A-xxx）见 `ASSUMPTIONS.md`；端口契约见 `PORT_LIST.md`。
> 范围：4EU UU mode（Shared MEM baseline）+ UU C-only 路径。
>
> Spec trace 文档简称：`02_LFSM`=SRC-01；`00_TOP`=SRC-02；
> `01_FSM走法`=SRC-03；`02_配置契约`=SRC-04；`04_Buf_RAM`=SRC-05；
> `05_MEM`=SRC-06；`11_流程图`=SRC-07；`07_RU`=SRC-08。

## 0. 图例

- **优先级**：P0 = sign-off 必须（功能正确性）；P1 = 观察/兼容字段；
  P2 = 可选增强。
- **Spec trace**：指向权威 `.md` 的章节标题（本模块全部为原生
  Markdown，无转换件，waiver 见 `REQUIREMENT_SOURCES.md` §0）。
  `02_LFSM` 存在两个 `### 9.1`（编辑性重号），按行序记为
  9.1(a)=「数据粒度」/ 9.1(b)=「有效 M 与 slice 计数」（§4 注）。
- **触发条件**：该功能被激活的输入/状态条件。
- **可观察效果**：端口或 TB 可探测状态上的预期表现（端口名见
  `PORT_LIST.md`）。
- **依赖**：必须先实现/验证的 F-xxx。
- F-id 分组：CFG=F-001…F-003、WLK=F-010…F-012、RDG=F-020…F-025、
  Q=F-030…F-032、ASM=F-040/F-041（公共）+ F-050（A）+ F-055/F-056（B）+
  F-060/F-061（AMX）+ F-065…F-067（BMX）、CHD=F-070…F-073、
  ALC=TCK=F-080…F-083、ARB=F-090…F-094、C=F-100、横切=F-110…F-113、
  观察=F-120。

## 1. 功能清单

### 1.1 配置与控制（CFG）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-001 | 配置配对握手：WalkConfig/LFSMInstructionConfig 各入配置 FIFO，两 head `inst_id` 相等时同拍接收并启动；不等即协议错误断言 | P0 | 02_LFSM sec 3.1；02_配置契约 sec 2.1/2.2；00_TOP sec 3.7 | 两通道 head 均 valid | `o_*_cfg_ready` 同拍拉高；instruction 寄存，walker 可启动 | — |
| F-002 | 配置寄存与结构断言：原始规模计数（`n_hw_count`/`k_groups`/`m_slice_count`）、地址范围/MX 参数保持；硬件安全不变量断言（`k_groups≤32`、`m_slice_count≤2`、span∈{1,2,4}、`n_step==1`）；合法性由上游 TOP 保证；loop 几何不下发（`n_blocks[]`/`n_outer_count`/`k_step_per_outer`/`k_outer_count`，见 F-010 与 A-005.1 v3） | P0 | 02_配置契约 sec 16；00_TOP sec 3.3；02_LFSM sec 9.1(b) | F-001 配对接收 | 配置寄存器组可读后保持稳定；非法组合触发断言 | F-001 |
| F-003 | reset 最高优先级：清空 walker/counter、`rd_id`/`rdgen_id` 序号、四路 Queue、Assembler context、held candidate、binding、load_ptr、C FIFO、配置 FIFO、RR cursor（=A）；reset 期间忽略输入握手 | P0 | 02_LFSM sec 3.1/5/16；02_配置契约 sec 11 | reset 有效 | 全部状态回初值；`rr_cursor=A`；配置 FIFO 空 | — |

### 1.2 Walker（WLK）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-010 | MKN walker FSM：循环嵌套 `k_outer→n_outer→m_slice→k_local→n_inner`，counter/transition 优先级、`walk_seq`、token 字段（`m_idx/n_idx/n_span=1/k_idx/first_mkn/last_mkn`）；active 期间每拍 commit 一个 token；transition 边界**加法级**维护 loop base/length（`n_len=(rem==9‖rem==10)?4:min(8,rem)`、`n_base+=n_len`；`k_count=min(k_step,k_groups−k_base)`、`k_base+=k_count`；`k_step=m_mode?4:8`；loop 结束 `base≥total`），无除法器/n_blocks 查表（2026-10-13 用户决策，A-005.1 v3） | P0 | 01_FSM走法 sec 4–12；00_TOP sec 3.5.2/3.5.3；02_LFSM sec 2.3(1)/6 | 已配对 instruction 存在且无更高优先级保持 | 逐拍 WalkToken 序列与 golden `MknWalkFSM` 一致（MKN 序列对拍） | F-001, F-002 |
| F-011 | walker 无 RDQ 容量 stall：内部 stall 通路 tie-off 但保持语义完整（stall 时 counter/`walk_seq` 保持）；`o_walk_stall` 恒 0 | P0 | 02_LFSM sec 3.2/6；01_FSM走法 sec 3.1/12 | — | `o_walk_stall==0` 恒成立；无 `STALL RDQ_FULL` | F-010 |
| F-012 | instruction 边界与背靠背：last token commit 拍 walker 置 done（`active_instruction` 清空）；配置 FIFO head 已配对时**次拍** evaluate/commit 启动下一条，可与前一条的 Queue/Packer/Arbiter drain 重叠（golden `start_instruction` 分支语义，REF-02；两条 instruction 可处于不同流水阶段） | P0 | 02_LFSM sec 15；00_TOP sec 3.7；REF-02 | last token commit 且配置 FIFO head 已配对 | MKN 序列按 instruction 重启（精确启动拍以 golden 对拍冻结）；`rdgen_id`/`rd_id` 从 1/0 重计 | F-010, F-001 |

### 1.3 RdGenerator（RDG）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-020 | data-key 首访去重（计数器条件）：A/AMX 新 key ⟺ `cnt_n_outer==0 && cnt_n_inner==0`；B/BMX 新 key ⟺ `m_idx==0`；AMX/BMX 另受 `mx_mode_en` gate；判定仅 `walk_advance` commit 时生效 | P0 | 02_LFSM sec 7.2；A-001 | walker active token | 每 `(inst,lane)` 同一 data key 只入队一次；入队流与 golden set 去重逐拍一致 | F-010 |
| F-021 | owner/`rd_id` 与 `rdgen_id`：`rd_id` lane-local 从 0、仅该 lane 成功入队时递增；`rdgen_id=walk_seq+1` per-instruction 从 1、reuse token 占号、stall 保持；同 token 全部 RdRequest 共享 `rdgen_id` | P0 | 02_LFSM sec 7.1/7.3；02_配置契约 sec 8 | 新 key 判定为真 | 入队 entry 的 owner/`rdgen_id` 字段与 golden 一致 | F-020 |
| F-022 | 原子批量入队：同 token 全部 RdRequest 一次 commit；同 lane 原子；跨 lane 同拍；无 partial batch；无容量 gate | P0 | 02_LFSM sec 7.3 | 任一 lane 新 key | 四路 Queue 拍末追加集合与 golden commit 一致 | F-020, F-021 |
| F-023 | 四路地址生成：A/B 线性（`m×k_groups+k` / `k×n_hw+n`）；AMX tile-major（`rg_len=ceil(k_groups×span/4)×32`）；BMX 行线性 pair+块量化（`n_hw2`/`k_groups2`）；越界检查为 **TB/sva 断言**（fail-fast，对齐 golden `ModelError`；2026-10-13 人工决策：不进硬件功能路径，与「合法性由 TOP 保证」并存——断言仅验证期生效） | P0 | 02_配置契约 sec 7；00_TOP sec 3.5.6 | 新 key 判定为真 | 入队 entry 的 `src_addr` 与 golden `_make_rd` 一致 | F-020, F-002 |
| F-024 | LaneLoadEnd 生成：最后 WalkToken commit 后把结束标记排在**该 required lane** 最后一笔逻辑 RD 之后（走 Queue，无同拍 bypass）；只发给 `required_lanes()`——A/B 恒发，AMX/BMX 仅 `mx_mode_en=1` 时发，非 required lane 不发（与 golden `required_lanes()`/`end_instruction` 对齐，REF-02） | P0 | 02_LFSM sec 15；02_配置契约 sec 10.9；11_流程图 sec 3(2)(3)；REF-02 | last token commit | 每 required lane 每 instruction 恰好一个结束标记入队；非 required lane（如非 MX 的 AMX/BMX）无标记、其 Queue 恒空 | F-010 |
| F-025 | C key 首访去重与地址预计算：`C key=(inst,m,n)`，新 key ⟺ `cnt_k_outer==0 && k_local==0`；地址 `l0c_base+(m×n_hw+n)×16`；`rdgen_id` 取首访 token `walk_seq+1`；不建 owner/binding/tag | P0 | 02_LFSM sec 7.1；07_RU sec 5/5.1；00_TOP sec 3.6.2；A-001 | walker active token | 每 instruction 每 `(m,n)` 恰好一个 C entry 入 C FIFO；地址/rdgen_id 与 golden 一致 | F-010, F-002 |

### 1.4 四路 RD Queue（Q）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-030 | 四路独立 FIFO：head 为最老 entry；每拍每路最多向 Assembler 传一个 head；仅 head dequeue；反压时 head/payload 保持；entry 不得同时处于 Queue 与 Assembler | P0 | 02_LFSM sec 8；02_配置契约 sec 9；11_流程图 sec 2 | 队列非空 | head 序列严格 FIFO；消费计数不变量 `enqueue−dequeue==size` | F-022 |
| F-031 | Queue→Assembler 无同拍 bypass：拍末 commit 入队、次拍起可见 | P0 | 02_LFSM sec 5；11_流程图 sec 2 | rdgen 入队拍 | 新 entry 当拍不出现在 Assembler 输入 | F-030 |
| F-032 | 无容量反压的有界实现：参数化深度（A16/B128/AMX8/BMX4+窗口池2/C8）+ never-full 仿真断言；断言失败=TB 失败而非流控；TYPICAL 包络外 worst-legal 形状为显式 waiver | P0 | 02_LFSM sec 6/8；A-002；A-011 | 任意运行 | 占用峰值不越界；无 `STALL RDQ_FULL`；waiver 记入 TRACEABILITY gap | F-030 |

### 1.5 Assembler 公共规则（ASM）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-040 | merge/padding 优先级与 context 保持：兼容 RD 填满 block > Queue 空/局部 loop 边界保持 > 几何尾 padding > LaneLoadEnd 兜底 drain；context 跨 bubble 保持；不跨 instruction 合并 | P0 | 02_LFSM sec 9.2/16；11_流程图 sec 2/3(1) | context 未满且有新 head/事件 | 未满 context 不因 bubble/transition 提前 emit；优先级顺序与 golden 一致 | F-030 |
| F-041 | padding 语义：`valid+padding==block_bytes`；A/B/AMX 均无 transport padding（B 尾与 AMX K 尾补齐为 mem pad，实存随读计 valid）；BMX 窗口未覆盖 slot 为 transport padding；任何 padding/mem-pad 不生成 owner/MKN/buffer write、不分配 index、不推进 load_ptr | P0 | 02_LFSM sec 9.3；02_配置契约 sec 6 | 几何尾/drain emit | 输出 block 字节账目守恒；padding 无副作用 | F-040 |

### 1.6 A Assembler（ASM-A）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-050 | A 几何切分：满 key（M64×K32B/owner）按 `a_block_order`（EU_M_HALF_K_HALF / EU_K_HALF_M_HALF / M_HALF_K_HALF_EU，静态参数）展开为 16 个 M8×K16B=128B DataBlock；无 padding；block 数/带宽/binding 不受 order 影响。**本轮范围（2026-10-13 人工决策）：只实现/验证默认序 `EU_M_HALF_K_HALF`**；两个非默认序为未验证功能，Step 7 记 TRACEABILITY gap（带日期），静态参数保留三值枚举以便后续启用不改端口 | P0 | 02_LFSM sec 9.1(a)/9.1(b)；02_配置契约 sec 3.6/5.1/6 | A head 进入 Assembler | 每 owner 依次 emit 16 block，地址/字节与 golden `_emit_a`（默认序）一致 | F-040, F-023 |

### 1.7 B Assembler（ASM-B）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-055 | B N4 pair merge：固定 K 把连续偶/奇 N4 owner 合成 N8/K32，切 2 个 128B block；非 N 尾单 N4 保持等待；pair 不跨 N block（REQUIREMENT_SOURCES §4.1 歧义注记） | P0 | 02_LFSM sec 9.1/9.2；02_配置契约 sec 5.1/6 | 相邻两个 N4 owner 可用 | 每 pair emit 2 block；fragment 序与 golden `_emit_b_group` 一致 | F-040, F-023 |
| F-056 | B 奇数 N 尾 mem-pad：instruction N coverage 为奇数时最后单 N4 生成 2×128B block（各 64B owner valid + 64B pair-completion mem pad；pad slot 实存于该 K 行 `n_hw2−1` 位、随真实数据读取并计入 valid）；B 无 transport padding | P0 | 02_LFSM sec 9.3；05_MEM sec 11 | 奇数 N 尾 owner 到达且为几何尾 | tail 块字节账目 128 valid+0 pad；src ranges 含 pad slot 地址；buffer write 仅 128B | F-055, F-041 |

### 1.8 AMX Assembler（ASM-AMX）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-060 | AMX K-run merge：固定 M 按连续 K key 累积至 `tag_span` 和 =4（K4B），按 M8×K4B=32B tile 展开；允许跨 K-outer merge，不因 K-outer transition 截断 | P0 | 02_LFSM sec 9.2；02_配置契约 sec 6/7 | AMX head 进入且 M 相同 K 连续 | run 完整后每 row-group emit 32B tile；merge 跨 K-outer 与 golden `_emit_amx_group` 一致 | F-040, F-023 |
| F-061 | AMX K 尾 tile mem-pad：K 尾不足 K4B 时尾 tile 缺失 key chunk 为 MEM 实存 pad（随 tile 读取、计入 valid、无 owner/tag/buffer write）；AMX transport padding 随之消失 | P0 | 02_LFSM sec 9.3；02_配置契约 sec 6 | run 到达 instruction K 尾 | 尾 tile 的 mem-pad fragment 出现在 source ranges；`padding_bytes` 仅纯 transport fill | F-060, F-041 |

### 1.9 BMX Assembler（ASM-BMX）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-065 | BMX 固定几何窗口：按 N8×K(4/span) owner slot 窗口暂存 context（窗口池 2）；窗口完整（或 LaneLoadEnd 强制）后按坐标序展开 4 个 32B block；恒满 128B；保存 `fragment/owner→destination` 内部 map；MEM issue 序不要求等于 walk 序，最终 binding 按 walk 序 | P0 | 02_LFSM sec 9.2/9.3；02_配置契约 sec 6 | BMX head 归属窗口 slot | 每窗口一笔 candidate；窗口完成顺序与 golden `_emit_ready_bmx_windows` 一致 | F-040, F-023 |
| F-066 | BMX transport padding slot：窗口内 walk 未生成的 owner slot 恒为 transport padding，可出现在任意窗口位置；无 owner/tag/buffer write、不推进 pointer | P0 | 02_LFSM sec 9.3 | 窗口存在未覆盖 slot | `padding_bytes` 含这些 slot；无任何副作用 | F-065, F-041 |
| F-067 | BMX mem-pad 块量化：奇数 N 尾每条 K row 按 N2 pair 补 1 pad slot（行 stride `n_hw2×4×span`）；K 尾不足 `4/span` 行按 2D block 补 pad row（`k_groups2`）；pad 实存 MEM、随真实数据读取、计入 valid（MEM-read 口径）、无 owner/tag/buffer write | P0 | 02_LFSM sec 9.3；02_配置契约 sec 6/7 | N 尾奇数 owner / K 尾窗口 | mem-pad fragment 出现在 source ranges；footprint 地址与 golden 一致 | F-065, F-023 |

### 1.10 BandwidthPacker / cand_holder（CHD）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-070 | full-width packing：`full_count=BW/block_bytes`（128B 下 A/B=1、AMX/BMX=4）；DataBlock 不得从中间拆开；非 instruction-last 不足带宽等待；可跨 N block 打包完整 block | P0 | 02_LFSM sec 10；11_流程图 sec 2 PACKFULL | 可见同 instruction block 数 ≥ full_count | candidate 组成与 golden `_can_form`/`form_candidate` 一致 | F-050…F-067 |
| F-071 | instruction-last partial：Assembler 完成 drain 后剩余 block 立即形成末笔 partial request；未使用总线宽度不创建全 padding block；BMX 例外（固定窗口恒满，无 partial） | P0 | 02_LFSM sec 10；11_流程图 sec 2 PACKEND | LaneLoadEnd drain 完成且有剩余 block | 末笔 `is_partial_beat`/`is_instruction_last` 标记正确 | F-070, F-024 |
| F-072 | `rd_mem_id` 规则：split block 沿用来源 `rdgen_id`；merge 取最早来源；candidate 的 `rd_mem_id` 取首 DataBlock 的 `rdgen_id` | P0 | 02_LFSM sec 10；02_配置契约 sec 8 规则 4–7 | candidate 形成 | 输出 `o_mem_req_rd_mem_id` 与 golden 一致 | F-070 |
| F-073 | held candidate 与仲裁旁路：Assembler→Packer 允许同拍 bypass（cycle-0 纯组合链）；Packer→Arbiter **不允许同拍**——**边3 严格流水**（2026-10-14 用户决策，相对 SRC-01 sec 5「允许」取**偏差** DEV-2026-10-14）：仲裁只认 held 快照寄存，fresh 形成拍仅供拍末捕获、**次拍起**参与仲裁（链首 +1 拍），replacement 链保持每拍 1 fire；每 lane 恰好 1 个 held candidate；未 grant 时 valid/payload 保持；candidate 形成时锁存 `planned_base/planned_advance` | P0 | 02_LFSM sec 5（边3 偏差，DEV-2026-10-14）；11_流程图 sec 3(8)；A-008 | held 存在 / block emit / candidate 未 fire | cycle-start head 形成的 candidate **次拍**起可获选 fire；未 grant 下拍 payload 不变；连发节奏 1 fire/拍 | F-070, F-031 |

### 1.11 DestinationAllocator / tag_checker（TCK）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-080 | load_ptr ring 顺序分配：新逻辑数据从 `load_ptr` 连续分配；禁跳 busy、不搜索其他 idle range、后 owner 不越 head owner；回卷以 candidate range tag state 为准（不比 pointer） | P0 | 02_LFSM sec 11.2；04_Buf_RAM sec 7.6 | 新 candidate 含未绑定 owner | `o_load_range_query_base` 序列与 golden `load_ptr` 轨迹一致 | F-073 |
| F-081 | binding 建立与 span：`span` 表（A/B=1、AMX/BMX=mx_tag_span）；绑定顺序只由 owner MKN walk/RD 序决定；每 owner 恰好一次 binding；多 context 经内部 map 关联乱序完成 fragment | P0 | 02_LFSM sec 11.1；02_配置契约 sec 14 | candidate 首次含新 owner | binding 元数据与 golden `Binding`/`AllocationGroup` 一致 | F-080 |
| F-082 | split 复用：第一笔 fire 建立 binding，后续 request 复用同一 binding/range、只改 byte offset；load_ptr 只推进一次；`planned_advance=0` 不查 destination | P0 | 02_LFSM sec 11.3；02_配置契约 sec 14 | split candidate 续写 | 续写无 `LoadPtrUpdate`；`o_load_range_query_valid=0` | F-081 |
| F-083 | destination_ok 查询：candidate 形成时锁存 `planned_base/planned_advance`，经 `o_load_range_query` 输出、每拍对 `i_load_range_idle` 重算 eligibility；`destination_ok=0` 时 candidate/binding/load_ptr/payload 全保持且不阻塞他 lane | P0 | 02_LFSM sec 11.2；04_Buf_RAM sec 7.6/8.1；A-004 | held candidate 存在 | query 输出与 golden candidate planned range 一致；busy 期间无 fire | F-073, F-080 |

### 1.12 ReadArbiter 与原子提交（ARB）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-090 | eligibility 与 grant：`eligible = candidate_valid && issue_room && source_ok[lane] && destination_ok`（A-014：`shared_mem_ready` 不进 eligibility，由 2-slot 发送队列以 `issue_room` 承接，`mem_ready` 落位 issue 拍出口）；每 cycle 最多 grant 一笔 | P0 | 02_LFSM sec 12（mem_ready 准入演进 = DEV-2026-10-14/GAP-07）；05_MEM sec 5/10 | 任一 lane candidate | 每拍 grant ≤1；issue 拍 `o_mem_req_valid` 至多 1 脉冲 | F-083 |
| F-091 | 优先键 + RR：先选最小 `(inst_id,rd_mem_id)`；同键从 `rr_cursor` 按 `[A,AMX,B,BMX]` 扫描；reset cursor=A；仅 `rd_mem_fire` 更新 cursor 指向 granted lane 下一 lane | P0 | 02_LFSM sec 12；02_配置契约 sec 11/16 | 多 lane eligible | grant 序列与 golden `evaluate` 一致 | F-090 |
| F-092 | `rd_mem_fire` 原子提交（A-014 两拍落位，DEV-2026-10-14/GAP-07）：**grant 拍**原子完成消费 candidate、提交 binding/range、推进 load_ptr、group 开关、更新 RR cursor + 载荷（`RdMemRequest` + `LoadPtrUpdate` 组合）入 §11B 发送队列；**issue 拍（grant 次拍）**两端口组同拍原子发出（推翻 A-006，采纳 `lfsm_req_pipe` 思路并连带 LoadPtrUpdate 保 sec 13/14.1 端口同拍性） | P0 | 02_LFSM sec 13（端口时序 = 偏差，GAP-07）；A-006 v2/A-014 | grant 成立 | 内部效果与 golden commit 一致（grant 拍）；端口两脉冲同拍且内容逐笔等价（issue 拍） | F-091 |
| F-093 | `LoadPtrUpdate` ↔ 唯一 exact active range：一个 update 只登记一个与 affected range 完全一致的 active loading range，不按 owner 拆 subrange；`advance>0`；整 range 完成后才 `loading→rdy`（外部）；端到端时序 = grant 拍 commit / issue 拍随 request 原子发出（A-014） | P0 | 02_LFSM sec 13/14；02_配置契约 sec 12/14 | F-092 且 advance>0 | 每次 pointer 推进恰好一个 update；`old/new/advance` 正确；与 `o_mem_req_valid` 同拍 | F-092 |
| F-094 | `RdMemRequest` buffer metadata：`buffer_writes[]`（lane/index/offset/len）、`tag_ranges[]` 定长 1；split 复用首笔 range；仅整 range 末贡献 request 置 `confirm_on_response=1`；padding 不写不确认；MX range 覆盖完整 span | P0 | 02_LFSM sec 14；05_MEM sec 5.2；A-003 | F-092 | 输出 metadata 与 golden `MemRequest` 逐笔一致（writes ≤32、advance ≤32、ranges==1 断言） | F-092, F-081 |

### 1.13 C-only register 路径（C）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-100 | C FIFO 与 `RegisterRequest(C)`：rdgen 拍末新 entry 入 C FIFO（深度 8 + never-full），次拍起可 issue；head valid/payload 保持至 `register_ready`；每拍最多 1 笔、无竞争仲裁；C 不占 Buffer、不建 owner/binding/tag | P0 | 07_RU sec 5/6；02_LFSM sec 4；A-002 | C FIFO 非空 | `o_reg_req_*` 流与 golden `ru_c_queue` issue 逐拍一致 | F-025 |

### 1.14 横切规则（XCUT）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-110 | instruction 边界不混合：不跨 instruction 合并 DataBlock/request；`LaneLoadEnd` 兜底 drain 全部剩余 context；背靠背 instruction 可处于不同流水阶段 | P0 | 02_LFSM sec 15；11_流程图 sec 3(2)(3) | LaneLoadEnd 到达 / 新 instruction 启动 | 无任何跨 instruction 的 block/request；b2b 向量（TC-B2B-01/02）对拍一致 | F-024, F-040, F-071 |
| F-111 | 逻辑优先级：reset > 保持已有 valid/payload > 处理本 lane 最老 head/owner > 产生新工作；Assembler/Packer/Allocator/Arbiter 各模块优先级表 | P0 | 02_LFSM sec 16 | 竞争条件 | 冲突场景下选择顺序与规格表一致 | F-003, F-040, F-091 |
| F-112 | 核心不变量断言（**落点决策 2026-10-13：全部 TB/sva，不进硬件功能路径**）：sec 17 UU 相关条（1–22）中 LFSM 内部条目（去重唯一、顺序守恒、字节守恒、每拍 ≤1 fire、MX 原子 span 等）→ 单元/集成 TB 断言；依赖外部模块状态的条目（如 #14 confirmation 不拆分、#20 回卷不覆盖 `loading/rdy`，需 Buf/RAM tag/MEM 可见性）→ 集成 TB stub 侧断言 | P0 | 02_LFSM sec 17；04_Buf_RAM sec 7.6；05_MEM sec 14 | 全运行 | 任一不变量违例即 TB 失败 | 全部 |
| F-113 | evaluate/commit 两拍语义：evaluate 只读 cycle-start 状态（不 pop/不递增 ID/不推进 pointer/不改 context）；commit 原子；valid 未握手保持清单（valid/payload、Queue head、candidate、暂定 range、byte/fragment 进度） | P0 | 02_LFSM sec 5；11_流程图 sec 3(9)；A-008 | 每拍 | 未握手场景下全部保持量逐拍不变 | F-003 |

### 1.15 观察（OBS）

| F-ID | 功能 | P | Spec trace | 触发条件 | 可观察效果 | 依赖 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| F-120 | `o_lfsm_idle` 观察电平：walker 无 active instruction、四路 Queue/Assembler context/held candidate/发送队列/C FIFO 全空（TB/集成 drain 观察字段，PORT_LIST §8 适配 7；A-014 后含 req_sched cnt==0） | P1 | —（观察字段；类比 02_LFSM sec 3.2 `walk_stall` 性质） | 状态全空 | drain 完成后拉高 | F-030, F-073, F-092, F-100 |

## 2. 子模块分解与 `domain.call()` 链（Step 3 action 5）

子模块函数、prefix 与实例数见 `PORT_LIST.md` §9。预定调用链
（均经 `domain.call(fn, inputs={...}, prefix=...)`，PRC-01 §7.3）：

```text
lfsm_top
├── lfsm_cfg  config_regs      outs: cfg_active, walk 字段, lfsm 字段, cfg_inst_id
├── lfsm_wlk  walker           in: start/cfg → outs: token_valid, m/n/k_idx, walk_seq, first/last_mkn
├── lfsm_rdg  rdgen            in: token+cfg → outs: 四路 enq payload, c_enq payload
├── lfsm_q_{a,amx,b,bmx}   rd_queue ×4      in: enq/asm_pop → outs: head_valid/head_payload/end_flag
├── lfsm_asm_{a,b,amx,bmx} assembler ×4     in: head/head1 + fire_consume + dest_base → outs: view 标量 + 元数据视图（src/wr/bytes/flags）+ view_next、pop、ctx_empty（Step 6 冻结键；D-001 emit-on-demand）
├── lfsm_chd_{a,amx,b,bmx} cand_holder ×4  in: asm view 标量 → outs: held candidate, planned_base/advance（对应规格 BandwidthPacker 持有职能）
├── lfsm_tck  tag_checker      in: candidate+load_range_idle → outs: destination_ok, binding/planned, load_ptr 更新载荷
├── lfsm_arb  arbiter          in: 四路仲裁键+dest_ok+issue_room → outs: grant, fire（纯控制；RdMemRequest/LoadPtrUpdate 载荷组装走 Step 6 §11A mux）
├── lfsm_rqp  req_sched        in: §11A 载荷+i_shared_mem_ready → outs: o_mem_req_*/o_load_ptr_update_*（issue 拍）、issue_room（A-014）
└── lfsm_c    c_path           in: c_enq/register_ready → outs: o_reg_req_*
```

逐键 `inputs`/`outs` 字典（键名、位宽、shape）在 Step 6
`ALGORITHM_CYCLE_AWARE_PSEUDOCODE.md` 冻结；位宽以
`PORT_LIST.md` §3/§4 为准。

## 3. 转写稿索引（粗粒度）

本模块权威输入全部原生 Markdown（无 `.docx/.pdf/.xlsx` 转换件，
waiver 见 `REQUIREMENT_SOURCES.md` §0），索引直接映射原文件章节。

### 3.1 主规格 SRC-01（`design_spec/docs/four_eu/02_LFSM.md`）

| 章节 | F-id |
| :--- | :--- |
| sec 1 文档定位 / sec 2.1–2.2 所有权 | —（边界声明；范围冻结见 REQUIREMENT_SOURCES §5） |
| sec 2.3 核心目标 | F-022, F-030, F-032, F-040, F-080, F-082, F-092, F-093, F-094 |
| sec 3 模块接口 | F-001, F-003, F-011, F-120（端口细节 → PORT_LIST） |
| sec 4 / 4.1 顶层流水 | F-010…F-100（全链路分解） |
| sec 5 Cycle Model | F-003, F-031, F-073, F-113 |
| sec 6 Walker 与无上限 RD Queue | F-010, F-011, F-032 |
| sec 7 RdGenerator | F-020…F-025 |
| sec 8 四路 RD Queue | F-030, F-031, F-032 |
| sec 9 DataBlockAssembler | F-040, F-041, F-050, F-055, F-056, F-060, F-061, F-065, F-066, F-067 |
| sec 10 BandwidthPacker | F-070, F-071, F-072 |
| sec 11 DestinationAllocator | F-080, F-081, F-082, F-083 |
| sec 12 ReadArbiter | F-090, F-091 |
| sec 13 `rd_mem_fire` 原子提交 | F-092, F-093 |
| sec 14 MEM Request Buffer Metadata | F-093, F-094 |
| sec 15 Instruction 边界 | F-024, F-110 |
| sec 16 逻辑优先级 | F-111 |
| sec 17 核心不变量 | F-112 |

### 3.2 其他权威源（经 R-xx 汇入）

| 源 | 使用章节 | 汇入 F-id |
| :--- | :--- | :--- |
| SRC-02 00_TOP | sec 3.3/3.5/3.6/3.7/3.8 | F-001, F-002, F-010, F-012, F-023, F-025 |
| SRC-03 01_FSM走法 | sec 3–12 | F-010, F-011 |
| SRC-04 02_配置契约 | sec 2/3/5/6/7/8/9/10/11/12/14/16 | F-001…F-094（字段/公式/ID/断言层） |
| SRC-05 04_Buf_RAM | sec 7.6/8 | F-080, F-083, F-093 |
| SRC-06 05_MEM | sec 5/10/11 | F-056, F-090, F-094 |
| SRC-07 11_流程图 | 全文 | F-031, F-040, F-070, F-071, F-073, F-083, F-113 |
| SRC-08 07_RU | sec 5/5.1/6 | F-025, F-100 |
| SRC-09 TYPICAL_CASES | 4EU 用例集 | 驱动验证（§5 测试摘要） |
| SRC-11 mkn_range | 输入范围 | F-002 |

## 4. 标题核对表（SRC-01 全标题枚举）

维护规则（方法 §2.4）：若 `02_LFSM.md` 新增/重命名标题，更新本表或在
`TRACEABILITY.md` 增加 F-xxx / 缺口条目。注：规格存在两个
`### 9.1`（编辑性重号），核对表按行序记为 9.1(a)/9.1(b)。

| # | 标题（原文） | F-id / — |
| :--- | :--- | :--- |
| 1 | `# LFSM 模块规格` | —（文档题头；8EU override 引用块出界，REQUIREMENT_SOURCES §5） |
| 2 | `## 1. 文档定位` | —（文档地图） |
| 3 | `## 2. 职责与所有权` | —（由子节覆盖） |
| 4 | `### 2.1 LFSM 拥有` | F-010, F-020, F-030, F-040, F-080, F-092（所有权→对应模块功能） |
| 5 | `### 2.2 LFSM 不拥有` | —（出界声明，REQUIREMENT_SOURCES §5） |
| 6 | `### 2.3 核心目标` | F-022, F-030, F-032, F-040, F-080, F-082, F-092, F-093, F-094（目标 1–6/8/9；目标 7 为 RU 条，出界） |
| 7 | `## 3. 模块接口` | —（由子节覆盖；端口 → PORT_LIST） |
| 8 | `### 3.1 输入` | F-001, F-003, F-083, F-090, F-100（输入消费功能；端口 → PORT_LIST §4） |
| 9 | `### 3.2 输出` | F-011, F-092, F-093, F-094, F-100, F-120 |
| 10 | `## 4. 顶层流水` | F-010…F-100（阶段一览逐行映射；C-only 段落 → F-025/F-100） |
| 11 | `### 4.1 RD Queue 出口到仲裁出口` | F-030, F-073, F-083, F-090（引用 SRC-07） |
| 12 | `## 5. Cycle Model` | F-003, F-031, F-073, F-113 |
| 13 | `## 6. Walker 与无上限 RD Queue` | F-010, F-011, F-032 |
| 14 | `## 7. RdGenerator` | —（由子节覆盖） |
| 15 | `### 7.1 Owner 与数据身份` | F-021, F-025 |
| 16 | `### 7.2 新数据判断` | F-020 |
| 17 | `### 7.3 原子入队` | F-021, F-022 |
| 18 | `## 8. 四路 RD Queue` | F-030, F-031, F-032 |
| 19 | `## 9. DataBlockAssembler` | —（由子节覆盖） |
| 20 | `### 9.1 数据粒度`（9.1(a)） | F-050, F-055, F-060, F-065 |
| 21 | `### 9.1 有效 M 与 slice 计数（partial M 已非法）`（9.1(b)） | F-002, F-050 |
| 22 | `### 9.2 Merge 规则` | F-040, F-055, F-060, F-065 |
| 23 | `### 9.3 Padding` | F-041, F-056, F-061, F-066, F-067 |
| 24 | `## 10. BandwidthPacker` | F-070, F-071, F-072 |
| 25 | `## 11. DestinationAllocator` | —（由子节覆盖） |
| 26 | `### 11.1 内部 Binding` | F-081 |
| 27 | `### 11.2 Busy Range 与顺序` | F-080, F-083 |
| 28 | `### 11.3 Split、Merge 与 Ring` | F-081, F-082 |
| 29 | `### 11.4 默认带宽关系` | F-070, F-080, F-081（4EU 128B 基线行；历史 unified-8EU 对照出界） |
| 30 | `## 12. ReadArbiter` | F-090, F-091 |
| 31 | `## 13. rd_mem_fire 原子提交` | F-092, F-093 |
| 32 | `## 14. MEM Request Buffer Metadata` | F-093, F-094 |
| 33 | `### 14.1 Request 生命周期` | F-092, F-093, F-094（时序图；response 不经 LFSM → PORT_LIST §4.4） |
| 34 | `## 15. Instruction 边界` | F-024, F-110 |
| 35 | `## 16. 逻辑优先级` | F-111 |
| 36 | `## 17. 核心不变量` | F-112（条 1–22；条 23–25 为 RU 条，出界） |

核对结果：36 行标题全部落到 F-xxx 或 —，无未解决项。

## 5. 功能 → 测试摘要（T-xxx 占位）

T-xxx 编号与激励/期望在 Step 8 `TEST_PLAN.md` 建立（计划日期：Step
9 增量实现启动前）；下表仅为映射意图，不构成测试定义。占位状态将
在 `TRACEABILITY.md`（Step 7）登记为带日期待办。

| F-id 组 | 计划测试层 | 测试来源 |
| :--- | :--- | :--- |
| F-001…F-003 | 单元 TB（config_regs）+ reset 类 | 定向握手/配对/非法配对断言；reset 中途拉抬 |
| F-010…F-012 | 单元 TB（walker） | MKN 序列对拍（golden dump），m16/m32 × 单/多 n_outer × K outer 重访 |
| F-020…F-025 | 单元 TB（rdgen+queue） | 入队流/owner/rdgen_id/地址/C entry 对拍 |
| F-030…F-032 | 单元 TB（rd_queue）+ 全量回归 | FIFO 协议定向 + never-full 断言（TYPICAL 包络） |
| F-040…F-067 | 单元 TB（四个 assembler）| plain B8/B16/B4、奇数 N 尾、窄 N block、MXFP8/MXFP4/HIF4 窗口与 mem-pad；A 仅默认 block order（非默认序 gap，见 F-050） |
| F-070…F-073 | 单元 TB（cand_holder） | full/partial、bypass、held 保持 |
| F-080…F-083 | 单元 TB（tag_checker+query） | destination busy hold、wrap、split 复用 |
| F-090…F-094 | 单元 TB（arbiter + req_sched）+ 集成回放 | grant 序列、内部 commit（grant 拍）+ 端口双脉冲（issue 拍）两拍落位断言、metadata 逐笔对拍（A-014/GAP-07） |
| F-100 | 单元 TB（c_path） | C 流对拍、`register_ready` 反压保持 |
| F-110…F-113 | 集成 TB（回放式 + 反应式 stub） | TYPICAL_CASES 4EU 子集 + b2b；destination busy / mem_ready=0 / source_ok=0 定向 |
| F-120 | 集成 TB | drain 完成观察 |

## 6. R-xx → F-xxx 交叉索引

| R-xx | 主题 | F-xxx |
| :--- | :--- | :--- |
| R-01 | 配置配对握手 | F-001 |
| R-02 | 输入规模/模式合法性 | F-002 |
| R-03 | MKN walker | F-010 |
| R-04 | WalkConfig 验收条件 | F-002, F-010（loop 几何改内部生成，验收转为生成正确性对拍） |
| R-05 | 无 walk stall | F-011, F-032 |
| R-06 | data-key 去重 | F-020, F-025 |
| R-07 | 原子批量入队 | F-022 |
| R-08 | owner/`rd_id`/`rdgen_id` | F-021 |
| R-09 | 四路 RD Queue | F-030 |
| R-10 | LaneLoadEnd | F-024, F-110 |
| R-11 | 三边 bypass 相位 | F-031, F-073 |
| R-12 | A assembler | F-050 |
| R-13 | B assembler | F-055, F-056 |
| R-14 | AMX assembler | F-060, F-061 |
| R-15 | BMX assembler | F-065, F-066, F-067 |
| R-16 | merge/padding 优先级 | F-040, F-041 |
| R-17 | BandwidthPacker | F-070, F-071 |
| R-18 | `rd_mem_id` | F-072 |
| R-19 | DestinationAllocator | F-080, F-081, F-082 |
| R-20 | `destination_ok`/`load_range_idle` | F-083 |
| R-21 | ReadArbiter | F-090, F-091 |
| R-22 | `rd_mem_fire` 原子提交 | F-092 |
| R-23 | `LoadPtrUpdate`↔exact range | F-093 |
| R-24 | request buffer metadata | F-094 |
| R-25 | MEM 准入 | F-090 |
| R-26 | instruction 边界与背靠背 | F-012, F-110 |
| R-27 | 逻辑优先级 | F-111 |
| R-28 | 核心不变量 | F-112 |
| R-29 | UU C-only 路径 | F-025, F-100 |
| R-30 | 地址生成 | F-023 |
| R-31 | 数据粒度与字节公式 | F-050, F-055, F-060, F-065 |
| R-32 | 静态配置默认值 | F-002（PORT_LIST §3） |
| R-33 | reset | F-003 |
| R-34 | evaluate/commit 两拍 | F-113 |
| R-35 | 日志/计数不变量 | F-030, F-112 |
| R-36 | 参数断言 | F-002 |
