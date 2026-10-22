# LFSM (4EU UU mode) REQUIREMENT_SOURCES

> Step 2 交付物（依据 `docs/pycircuit_implementation_method.md` Step 2）。
> 范围：4EU UU mode（Shared MEM baseline）+ UU C-only 路径；不含 RU
> overlay、TMEM、Buf/RAM 内部、MEM 内部、EFSM/运算单元、8EU dual-core。
> 建立日期：2026-10-13；v2 修订 2026-10-13（补 REF-08、R-29 显式
> `rdgen_id` 规则、`o_tag_state` 排除注记、§4.1 spec 歧义注记）。

## 0. 规格格式声明（Design specification conversion waiver）

本模块全部权威输入均为**原生 Markdown**，不存在 `.docx` / `.pdf` /
`.xlsx` 权威件，无需转换；`REQUIREMENT_SOURCES` 直接引用原始 `.md`
路径（即 digest 路径）。若未来引入二进制规格，必须先按
`docs/pycircuit_implementation_method.md`「Design specification
conversion」转出 `.md` 再进入本表。

## 1. 权威需求源（normative sources）

| SRC | 路径 | 角色 | 本设计使用范围 |
| :--- | :--- | :--- | :--- |
| SRC-01 | `designs/LFSM/design_spec/docs/four_eu/02_LFSM.md` | **主规格**：LFSM 读数据流水全部行为 | 全文 sec 1–17（8EU override 段除外） |
| SRC-02 | `designs/LFSM/design_spec/docs/shared/00_TOP模块连接框架.md` | 系统连接、配置 fanout、合法性检查、地址推导 | sec 1–3（配置推导/合法性）、sec 4–7（连接组、时序反拍、系统不变量中 LFSM 相关行） |
| SRC-03 | `designs/LFSM/design_spec/docs/shared/01_FSM走法逻辑.md` | 共享 MKN walk 唯一行为规格 | 全文 sec 1–14（LFSM 实例：`n_step=1`、无 RDQ 容量 stall；EFSM 实例/8EU override 仅作对照） |
| SRC-04 | `designs/LFSM/design_spec/docs/shared/02_LFSM配置与数据契约.md` | 配置字段、静态默认值、地址公式、ID 契约、队列数据结构、日志字段、参数断言 | sec 1.1–1.3 仅作模式边界确认；sec 2–8、9、10、11、12、14、16、17 全文 |
| SRC-05 | `designs/LFSM/design_spec/docs/four_eu/04_Buf_RAM.md` | Buf/RAM 侧接口（外部模块） | **仅** sec 7.6（pointer 反压与回卷保护、`fresh_idle_guard`、occupied 容量检查）与 sec 8（`o_load_range_idle` 查询、`i_load_ptr_update` 契约） |
| SRC-06 | `designs/LFSM/design_spec/docs/four_eu/05_MEM.md` | MEM 侧接口（外部模块） | **仅** sec 5（`RdMemRequest` 接口与 buffer metadata）与 sec 10（`source_ok`/backpressure） |
| SRC-07 | `designs/LFSM/design_spec/docs/four_eu/11_RD_Queue到仲裁出口流程图.md` | Queue→Arbiter 全链路图解与阅读顺序 | 全文（不新增行为规则，权威仍归 SRC-01/05/06） |
| SRC-08 | `designs/LFSM/design_spec/docs/four_eu/07_RegisterUnit_RU.md` | RU 规格 | **仅** sec 5/5.1（非 RU 模式 C key 去重、地址、`rdgen_id` 取用）与 sec 6 中 C FIFO 无上限条款；其余 RU 分流/仲裁全部出界 |
| SRC-09 | `designs/LFSM/design_spec/code/TYPICAL_CASES.md` | 验收用例矩阵（19 单指令 + 4 b2b） | 4EU 用例 TC02/TC08/TC13/TC15/TC17 + 4EU b2b TC-B2B-01/02（dev）；8EU/RU 用例仅作对照 |
| SRC-10 | `designs/LFSM/design_spec/code/VERIFICATION_POINTS.md` | 派生计数与 checker 点 | 派生公式（`S/H/P/T_N/G/EXEC`）与 LFSM 相关 checker ID，供 TEST_PLAN 引用 |
| SRC-11 | `designs/LFSM/design_spec/docs/shared/mkn_range.md` | M/N/K 输入范围 | 输入合法性边界（K 恒为 bytes、按 32B 对齐） |

## 2. Golden 参考代码（行为等价对照，非规格）

| REF | 路径 | 对拍内容 |
| :--- | :--- | :--- |
| REF-01 | `designs/LFSM/design_spec/code/mkn_walker.py` | `MknWalkFSM`：counter/transition/`walk_seq`/stall hold |
| REF-02 | `designs/LFSM/design_spec/code/four_eu/load_path.py` | `LoadEngine`：配对启动、`_needed_rds` set 去重、原子批量入队、地址生成、C key 去重与 `ru_c_queue`、eligibility/grant、`_allocate_candidate`、`rd_mem_fire` 原子提交 |
| REF-03 | `designs/LFSM/design_spec/code/four_eu/lane_pipeline.py` | `LanePipeline`/`LaneAssembler`：`entries` 队列、`preview_bypass`（三边时序）、四 lane merge/padding、window、packer、held candidate |
| REF-04 | `designs/LFSM/design_spec/code/four_eu/buffer_ram.py` | `range_idle`（idle + `fresh_idle_guard` + capacity）——外部 Buf/RAM 行为，集成 TB stub 依据 |
| REF-05 | `designs/LFSM/design_spec/code/model_types.py` | 配置/请求/候选数据结构、lane span、深度参数 |
| REF-06 | `designs/LFSM/design_spec/code/run_model.py` / `run_typical_cases.py` | CLI → `RawInstruction`/`ModelConfig` 归一化；TYPICAL_CASES 驱动方式（golden dump 工具复用） |
| REF-07 | `designs/LFSM/design_spec/code/four_eu/simulator.py` | cycle evaluate/commit 编排、`rdq`/`rdmem` 日志口径（事件 dump 字段依据） |
| REF-08 | `designs/LFSM/design_spec/code/four_eu/memory.py` | MEM 准入/latency/响应生成行为（Step 10 反应式 MEM stub 依据） |

> 注：`four_eu/checker.py` 为 Python 侧 checker，不作为 V6 对拍参考
> （golden 断言在 TB 内实现），有意排除。

## 3. 流程/语言规范源（V6 authoring，Step 1 复读）

| SRC | 路径 | 用途 |
| :--- | :--- | :--- |
| PRC-01 | `docs/v6_PyCircuit_Specification.md` | 信号纪律（§2）、类型（§3）、寄存器推导（§4/§6）、模块六步法（§7）、存储原语（§8）、Tb（§9）、编译入口（§10） |
| PRC-02 | `docs/v6_PyCircuit_Tutorial.md` | 示例：计数器/流水线/层次化/向量/存储/构建 |
| PRC-03 | `docs/v6_PyCircuit_Software_Architecture.md` | 工具链分层、`pyc` 方言、`pycc`、C++/Verilog 发射 |
| PRC-04 | `docs/TESTBENCH.md`、`docs/SIDECAR_SCHEDULE.md` | `Tb`/`CycleAwareTb` 契约、inline/sidecar 调度 |
| PRC-05 | `docs/pycircuit_implementation_method.md` | 十步流程（本设计的流程权威） |
| PRC-06 | `AGENTS.md`、`docs/updatePLAN.md`、`docs/rfcs/pyc4.0-decisions.md` | 仓库纪律：gate-first、禁 backend-only 语义修复；本设计不改 IR/编译器 |

## 4. 需求主题 → 源映射（source table）

| # | 需求主题 | 源（文档:章节 / 代码） |
| :--- | :--- | :--- |
| R-01 | 配置配对握手（`WalkConfig`+`LFSMInstructionConfig` 按 `inst_id` 配对后启动） | SRC-01:sec 3.1；SRC-04:sec 2.1/2.2；SRC-02:sec 3.6–3.7；REF-02 `commit` START 分支 |
| R-02 | 输入规模/模式合法性（M/N/K 范围、`m_mode`、dtype/MX 联动、无 partial M） | SRC-02:sec 3.3；SRC-11；SRC-04:sec 16（参数断言） |
| R-03 | MKN walker（循环嵌套 `k_outer→n_outer→m_slice→k_local→n_inner`、counter、transition、`walk_seq`、stall 保持、done） | SRC-03:sec 4–12；REF-01 |
| R-04 | `WalkConfig` 验收条件（`k_step_per_outer`/`k_outer_count`/`n_blocks` 连续无空洞等；注：v3 起这些字段不下发、由 walker 内部加法级生成，验收转为生成正确性对拍，见 ASSUMPTIONS A-005.1 v3 / PORT_LIST §8 适配 8） | SRC-03:sec 5；SRC-02:sec 3.5 |
| R-05 | LFSM baseline 无 walk stall（`walk_stall` 恒 0 观察字段；RDQ 无容量反压） | SRC-01:sec 3.2/6；SRC-03:sec 3.1/12；SRC-04:sec 3.3 |
| R-06 | data-key 去重（A/AMX `(inst,m,k)`、B/BMX `(inst,k,n)`、C `(inst,m,n)`；成功入队才登记） | SRC-01:sec 7.1/7.2；SRC-04:sec 8；REF-02 `_needed_rds`/`_ru_c_needed` |
| R-07 | 原子批量入队（同 token 全部 RdRequest 一次 commit；同 lane 原子；跨 lane 同拍） | SRC-01:sec 7.3；REF-02 `commit` |
| R-08 | owner/rd_id（lane-local 从 0）与 `rdgen_id=walk_seq+1`（per-instruction 从 1；reuse token 占号；stall 保持） | SRC-01:sec 7.3；SRC-04:sec 8；REF-02 `_make_rd` |
| R-09 | 四路 RD Queue（FIFO head、每拍每路 ≤1 head、仅 head dequeue、反压保持、无同拍 bypass、无容量上限） | SRC-01:sec 5/6/8；SRC-07:sec 2；SRC-04:sec 9；REF-03 |
| R-10 | `LaneLoadEnd`（最后 token commit 后排在 lane 最后 RD 之后；兜底 drain；不跨 instruction） | SRC-01:sec 15；SRC-07:sec 3；SRC-04:sec 10.9；REF-03 `end_instruction` |
| R-11 | Queue→Assembler 无同拍 bypass / Assembler→Packer、Packer→Arbiter 允许同拍 bypass | SRC-01:sec 5；SRC-07；SRC-04:sec 9；REF-03 `preview_bypass` |
| R-12 | A assembler（M8×K16B=128B block、每 active EU 4 block、`a_block_order` 三种序、无 padding） | SRC-01:sec 9.1/9.2；SRC-04:sec 3.6/6；REF-03 `_emit_a` |
| R-13 | B assembler（固定 K 偶/奇 N4 合成 N8；奇数 N 尾 2×128B(64B valid+64B pad)；非尾单 N4 等待） | SRC-01:sec 9.2/9.3；SRC-04:sec 6；SRC-06:sec 11；REF-03 `_emit_b_group` |
| R-14 | AMX assembler（M8×K4B=32B tile、K-run 至 `tag_span=4`、跨 K-outer merge、K 尾 tile mem-pad） | SRC-01:sec 9.2/9.3；SRC-04:sec 6/7；REF-03 `_emit_amx_group` |
| R-15 | BMX assembler（固定几何窗口 N8×K(4/span)、窗口恒满总线、walk 未覆盖 slot=transport padding、N2/K4B 块量化 mem-pad、多 context） | SRC-01:sec 9.2/9.3；SRC-04:sec 6/7；REF-03 `_bmx_*` |
| R-16 | merge/padding 优先级（兼容填满 > Queue 空保持 > 几何尾 > LaneLoadEnd drain；非尾禁止 padding） | SRC-01:sec 9.2/9.3/16；SRC-07:sec 2–3 |
| R-17 | BandwidthPacker（128B 满宽；`full_count=BW/block_bytes`；instruction-last partial；不拆 block；可跨 N block；BMX 恒满窗口无 partial） | SRC-01:sec 10；SRC-07:sec 2（PACKFULL/PACKEND）；REF-03 `_can_form`/`form_candidate` |
| R-18 | candidate 的 `rd_mem_id`（首 DataBlock 的 one-based `rdgen_id`；split 沿用、merge 取最早） | SRC-01:sec 10；SRC-04:sec 8 规则 4–7；REF-03 |
| R-19 | DestinationAllocator（per-lane `load_ptr` ring、连续分配禁跳 busy、binding、`span`、split 复用只推进一次、merge 按 owner 序拼接） | SRC-01:sec 11.1–11.3；SRC-04:sec 14；REF-02 `_allocate_candidate` |
| R-20 | `destination_ok`/`load_range_idle`（全 idle + 非 `fresh_idle_guard` + capacity；`rdy→idle→loading` 中间一个完整 idle-visible 拍；回卷不比 pointer） | SRC-01:sec 11.2；SRC-05:sec 7.6/8.1；SRC-07:sec 3(5)(9)；REF-04 |
| R-21 | ReadArbiter（eligible = valid & `shared_mem_ready` & `source_ok` & `destination_ok`；优先键 `(inst_id,rd_mem_id)` 升序；同键 `[A,AMX,B,BMX]` RR；reset cursor=A；每拍 ≤1 grant；fire 才更新 cursor） | SRC-01:sec 12；SRC-04:sec 11/16；REF-02 `evaluate` |
| R-22 | `rd_mem_fire` 原子提交（消费 candidate、提交 binding、推进 load_ptr、`LoadPtrUpdate`、`RdMemRequest` 带 metadata、更新 RR cursor） | SRC-01:sec 13；SRC-05:sec 8.2；REF-02 `commit` |
| R-23 | `LoadPtrUpdate` ↔ 唯一 exact active loading range（不按 owner 拆 subrange；整 range 完成后才 `loading→rdy`） | SRC-01:sec 13/14；SRC-04:sec 12/14；SRC-05:sec 9.3 |
| R-24 | `RdMemRequest` buffer metadata（`buffer_writes[]`/`tag_ranges[]`、split 复用 range、末贡献 request 才 `confirm_on_response`、padding 不写不确认、MX range 覆盖完整 span） | SRC-01:sec 14；SRC-06:sec 5.2；SRC-04:sec 10.8 |
| R-25 | MEM 准入（`shared_mem_ready`、`source_ok[lane]`；payload 未握手保持） | SRC-01:sec 3.1；SRC-06:sec 5/10 |
| R-26 | instruction 边界与背靠背（不混 block/request；背靠背可处于不同流水阶段） | SRC-01:sec 15；SRC-04:sec 15；SRC-09 TC-B2B-01/02 |
| R-27 | 逻辑优先级（reset > 保持 valid > 最老 head/owner > 新工作）与各模块优先级 | SRC-01:sec 16 |
| R-28 | 核心不变量 1–22（UU 相关条；23–25 为 RU 条，出界） | SRC-01:sec 17 |
| R-29 | UU C-only 路径（C key 去重、`l0c_base+(m*n_hw+n)*16`、C FIFO、`RegisterRequest(C)`、C request 的 `rdgen_id` = 首次生成该 key 的 token `walk_seq+1`、无竞争、`register_ready` 准入、不建 owner/binding/tag） | SRC-01:sec 4/7.1；SRC-08:sec 5/5.1/6；SRC-02:sec 3.6.2；REF-02 `_make_ru_c_request` |
| R-30 | 地址生成（A/B 线性、AMX tile-major、BMX 行线性 pair+块量化；`mx_bytes_per_k0`/`mx_tag_span`） | SRC-04:sec 7；SRC-02:sec 3.5.6；REF-02 `_make_rd` |
| R-31 | 数据粒度与字节公式（A/B/MX 逻辑 RD 与 DataBlock 字节、span 表） | SRC-01:sec 9.1/11.1；SRC-04:sec 3.4–3.6/5/14 |
| R-32 | 静态配置默认值（`load_bus=128B`、bufa=8/l0b=32/amx=32/bmx=256、`rd_queue_depth` 兼容 no-op、latency=3、issue=1） | SRC-04:sec 3；SRC-02:sec 3.8 |
| R-33 | reset（最高优先，清空 walker/ID/Queue/Assembler/Packer/candidate/binding/context/load_ptr） | SRC-01:sec 3.1/5/16 |
| R-34 | evaluate/commit 两拍语义（evaluate 只读 cycle-start、不 pop/不递增/不推进；commit 原子） | SRC-01:sec 5；SRC-07:sec 3(9)；REF-07 `run` |
| R-35 | 日志/计数不变量（`enqueue-dequeue==queue_size`、`pending_mem_owners` 口径、`rdq` 列） | SRC-01:sec 8；SRC-04:sec 9/15；REF-03 `assembler_step` |
| R-36 | 参数断言（span/BW 对齐、`valid+padding==load`、fresh_idle_guard 不等式等） | SRC-04:sec 16 |

### 4.1 spec 文字歧义注记（实现防误读）

- SRC-01 sec 9.2「DataBlock 与 MEM request 可跨相邻 N block 组合」：
  B 的 N4 pair **从不跨 N block**（按 `n_hw` 奇偶配对且 block 边界
  对齐，REF-03 `b_pair_members`）；「跨 N block」实际作用于 BMX 固定
  窗口（跨 block 组成窗口）与 packer 对完整 DataBlock 的聚合。
  FEATURE_LIST 引用该句时须区分，避免实现成 B pair 跨 block。
- SRC-01 sec 14 规则 5「一笔 request 可携带多个互不重叠 exact
  range」：UU 下结构性不出现（每笔 candidate 恰一 allocation
  group，实测 4628 笔全 =1，见 ASSUMPTIONS A-003）；多 range 为
  通用/RU/乱序窗口保留。

## 5. 范围外源（仅边界对照，不提取需求）

| 路径 | 出界内容 |
| :--- | :--- |
| `designs/LFSM/design_spec/docs/four_eu/03_EFSM.md` | EFSM 全部（除 shared walk 一致性约束） |
| `designs/LFSM/design_spec/docs/four_eu/04_Buf_RAM.md` 其余章节 | Buf/RAM 内部 data/tag 实现 |
| SRC-05 §8.1 `o_tag_state[lane][index]`（optional debug/full view） | 有意排除：非功能必需的 debug 全量 tag 视图（TB 内部自持） |
| `designs/LFSM/design_spec/docs/four_eu/05_MEM.md` 其余章节 | MEM 内部 service/latency 实现（TB 反应式 stub 经 REF-08 取 latency 行为） |
| `designs/LFSM/design_spec/docs/four_eu/06_运算单元.md` | 运算单元 |
| `designs/LFSM/design_spec/docs/four_eu/07_RegisterUnit_RU.md`（sec 5 以外） | RU overlay：A/AMX 分流、C>AMX>A 仲裁 |
| `designs/LFSM/design_spec/docs/four_eu/08/09/10_*.md` | 容量/映射图解（背景） |
| `designs/LFSM/design_spec/docs/eight_eu/*.md` | 8EU dual-core 全部 |
| `designs/LFSM/design_spec/code/eight_eu/` | 8EU 参考模型 |
| `designs/LFSM/design_spec/docs/four_eu/13_TMEM模式.md`（如存在）/ TMEM code | TMEM |

## 6. DOC_SYNC_QUEUE 评估（规格冻结状态）

`designs/LFSM/design_spec/code/DOC_SYNC_QUEUE.md` 现有 4 条 pending
候选，逐条评估对 UU baseline 的影响：

| 候选 | 性质 | 对本轮 UU baseline 的影响 |
| :--- | :--- | :--- |
| `a3_amx_job_budget_div4` | RU/TMEM register-port AMX job 预算 | **无**（文中明确 "UU (Shared MEM lane) has no budget concept and is untouched"） |
| `tmem_mx_candidate` / `tmem_mode_candidate` | TMEM 模式 | **无**（TMEM 出界） |
| `lfsm_req_payload_pipe` (`lfsm_req_pipe`) | RTL 微架构（request payload 晚一拍） | **已采纳**（2026-10-14 用户决策，A-014/GAP-07，推翻 A-006 v1）：采纳并补全——`LoadPtrUpdate` 与 request 同组入 2-slot 发送队列 `req_sched`，issue 拍（grant 次拍）同拍原子发出；内部 grant commit 照旧原子。落点见 ASSUMPTIONS A-006 v2/A-014、CYCLE §11B、TRACEABILITY GAP-07 |

结论：UU baseline 语义以当前 `docs/` 冻结文本为准，无 pending 项需要等待。

## 7. Step 1 复读记录（V6 文档）

已复读：PRC-01 全文（重点 §2/§3/§4/§6/§7/§8/§9/§10）、PRC-05 全文、
PRC-06（`AGENTS.md`、`docs/updatePLAN.md`、pyc4.0-decisions 前 200 行
决策 0001–0009 及 ground rules）、SRC-01/02/03/04 全文、SRC-05/06 指定
章节、SRC-07 全文。Step-1 笔记（authoring mode、风格参考、环境命令）
见 `designs/LFSM/pycircuit/README.md`。
