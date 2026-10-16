# LFSM (4EU UU mode) TEST_PLAN

> Step 8 交付物（依据 `docs/pycircuit_implementation_method.md` Step 8：
> 无端口无功能未测；reset/smoke/directed/stress/corner 分类；全部映射
> `CycleAwareTb`）。建立日期：2026-10-13。
> 覆盖关系反向索引（F-xxx → T-xxx、端口 → T-xxx）以
> `TRACEABILITY.md` §1/§2 为权威；本文件为 T-xxx 定义的唯一权威
> （TRACEABILITY 维护规则 3）。依赖：golden 向量（GAP-04）、伪码锚点
> （GAP-03）。范围：4EU UU mode + UU C-only 路径。

## 0. 编号、分类与通用约定

### 0.1 号段与分类

| 号段 | 类别 | 条数 | 调度 |
| :--- | :--- | ---: | :--- |
| T-001…T-006 | reset | 6 | inline |
| T-010…T-013 | smoke | 4 | inline |
| T-020…T-065 | directed·单元 | 46 | inline |
| T-066…T-069 | directed·小集成（三边相位/drain/联合） | 4 | inline |
| T-070…T-077 | directed·集成回放（golden 向量） | 8 | inline |
| T-080…T-086 | stress（反压/并发/包络） | 7 | inline |
| T-090…T-097 | corner（几何/边界/矩阵；T-097 含 b2b 异几何混叠） | 8 | inline |
| T-100…T-103 | system（Step 10 预览，反应式 stub 闭环） | 4 | T-102 sidecar，余 inline |

### 0.2 TB 契约（全部 `CycleAwareTb`，PRC-01 §9 / PRC-04）

- 复位：`tb.reset("rst", cycles_asserted=2, cycles_deasserted=1)`
  （PORT_LIST §2；reset 为 domain reset，非数据端口）。
- 相位约定（A-008 evaluate/commit 映射）：
  - **组合输出**（`o_mem_req_*` / `o_load_ptr_update_*` /
    `o_load_range_query_*` / `o_reg_req_*` / grant/valid 等 cycle-0
    组合量）：本拍 `tb.drive()` 输入后 `tb.expect(..., phase="pre")`
    （TICK-OBS，提交前采样）；
  - **寄存状态/拍末 commit 效果**（Queue head 更新、held candidate
    写入、idle 电平、下一拍可见性）：`tb.expect(..., phase="post")`
    （XFER-OBS，默认）。
- 边相检查：边1「无同拍 bypass」用「enq 拍 `phase="pre"` 不可见、次拍
  `phase="pre"` 可见」两段断言；边2「允许同拍」用 `phase="pre"` 断
  当拍候选形成与 held 捕获；**边3 严格流水（DEV-2026-10-14，GAP-06）**：
  仲裁只认 held 快照——fresh 形成拍 `phase="pre"` 断**无** grant、
  次拍断 grant（链首 +1 拍）；replacement 链每拍 1 grant。
  **发送段（DEV-2026-10-14，GAP-07/A-014）**：内部 grant commit
  （fire_consume/load_ptr/RR）在 grant 拍 `phase="post"` 断言；
  `o_mem_req_*`/`o_load_ptr_update_*` 在 **issue 拍（grant 次拍）**
  `phase="pre"` 断同拍双脉冲——禁止沿用旧「grant 拍端口直达」口径。
- 每测试文件可独立运行（`python3 tests/unit/test_xxx.py`），每日回归
  走 `pycircuit build <tb>.py --target cpp`；长随机用 sidecar
  （T-102）。编译入口：`compile_cycle_aware(..., eager=True)`；
  层次化发射检查（hierarchical=True）属 Step 10。

### 0.3 目录与文件布局

```text
tests/unit/        test_reset.py        T-001…T-003, T-006, T-013
                   test_config_regs.py  T-020…T-023
                   test_walker.py       T-011, T-024…T-028
                   test_rdgen.py        T-029…T-035
                   test_rd_queue.py     T-036…T-038
                   test_assembler_a.py  T-039, T-040
                   test_assembler_b.py  T-041…T-043
                   test_assembler_amx.py T-044, T-045
                   test_assembler_bmx.py T-046…T-049
                   test_cand_holder.py   T-050…T-053
                   test_tag_checker.py   T-054…T-057
                   test_arbiter.py      T-004, T-058…T-063, T-069
                   test_c_path.py       T-005, T-012, T-064, T-065
                   test_req_sched.py    T-060/T-061 端口段（issue 拍脉冲/保持/顺序；A-014）
tests/integration/ test_bypass_chain.py T-066…T-068
                   test_replay_typical.py T-010, T-070…T-077（参数化向量）
                   test_backpressure.py  T-080…T-085
                   test_corner.py       T-090…T-097（部分向量驱动）
                   test_system_stub.py  T-100…T-103
vectors/           golden dump（tools/dump_lfsm_golden.py，GAP-04）
```

### 0.4 Golden 向量契约（`vectors/`，golden todo 产出）

`tools/dump_lfsm_golden.py` 驱动 `design_spec/code/run_model.py`
（4EU non-RU，REF-06）按用例 dump 两级 JSON：

1. **顶层逐拍向量**（集成回放用）：每拍 `inputs`
   （`i_load_range_idle[4]` / `i_shared_mem_ready` /
   `i_mem_source_ok[4]` / `i_register_ready` / 配置通道注入拍）与
   `expect`（`o_mem_req_*` 完整 payload / `o_load_ptr_update_*` /
   `o_reg_req_*` / `o_load_range_query_*` / `o_walk_stall` /
   `o_lfsm_idle`）；
2. **单元流**（单元 TB 用）：walker token 流（含
   `m/n/k_idx, walk_seq, first/last_mkn`）、四路 enq 流（owner /
   `rdgen_id` / 地址 / LaneLoadEnd **+ D-002 per-entry 几何注解**：B
   `n_tail_single`、AMX `span/k_groups/is_k_tail`、BMX
   `span/k_groups/n_hw2/n_blk_base/n_blk_len`——assembler 单元 TB
   不读配置寄存、只按 entry 注解驱动，dump 按 `inst_id` 分组）、
   per-lane emit block 流、candidate 流、C entry 流。

回放规则：顶层向量逐拍 `drive(inputs)` → `expect(组合输出,
phase="pre")`；入队/commit 类事件经「次拍可见性 + TB 镜像占用模型」
间接核对（边 1 语义决定当拍不可直接观察）。**fire 时序口径（边3 严格
流水 + A-014 发送段，GAP-06/07）**：每条 candidate 链首相对 golden
恒定 **+2 拍**（边3 +1、发送段 +1）——`expect` 对 `o_mem_req_*` 与
`o_load_ptr_update_*` 逐笔比对元数据与顺序，拍号按「链首偏移」整形
后核对（不做原始拍号的逐拍精确等价；两端口流同拍成对出现）。单元流
按各 TB 的小循环逐拍比对。独立 golden 公式（VERIFICATION_POINTS §3：
`S/H/T_N/G/EXEC`、unique keys、release advance 总和、地址公式）作
为最终计数 oracle；checker 口径引用 VERIFICATION_POINTS §4 的 ID。
**插桩口径**：dump 附带 `pending_mem_owners[lane]` 逐拍占用流
（A-002 探针 B；`LFSM-Q-02` 口径——Queue 出队不减、该 owner 首次
MEM issue 才减），供 I5/T-085/T-086 的 TB 镜像深度监视与新 T-097
的逐 instruction 溯源。

### 0.5 公共断言套件（T-076，默认挂载）

全部回放/系统 TB 与适用的单元 TB 默认启用下列不变量断言（任一违例
即 TB 失败；覆盖 F-112 内部条目与 F-030/F-041 等，落点为 TB/sva，
不进硬件——2026-10-13 决策）：

| 断言 | 口径来源 |
| :--- | :--- |
| 每拍 `o_mem_req_valid` 脉冲 ≤1 | SRC-01 sec 12；`LFSM-ARB-01` |
| `valid+padding==load_byte_count ≤128`；padding 不产生 write/confirm | `LFSM-PAD-01`；SRC-04 sec 16 |
| `buffer_writes ≤32`、`advance ≤32`、`tag_ranges==1` | A-003 |
| `LoadPtrUpdate` 与 `tag_range_base/count` 一致；`advance>0` | `LFSM-RANGE-01` |
| 去重唯一：同 `(inst,lane)` data key 不重复入队（镜像 key 集） | `LFSM-RD-02` |
| 顺序守恒：per-lane fire 的 owner 序 = RD 生成序（绑定序=walk 序） | `LFSM-BIND-01` |
| `enqueue−dequeue==size`（TB 镜像占用，永不 <0、永不越深度） | R-35；`LFSM-Q-01` |
| MX 原子 span：MX range 覆盖完整 span 组 | `LFSM-ALLOC-02` |
| `o_walk_stall==0` 恒成立 | F-011 |
| 未握手保持：valid 未 fire 时 payload 逐拍不变 | SRC-01 sec 5 保持清单；`MEM-REQ-01` |
| `is_partial_beat ≡ 0`（UU 128B 下 partial 结构性不可达；实现保留，登记式断言） | D-003；CYCLE §11A/SEQ §14.4 |
| issue 拍成对与顺序：`o_load_ptr_update_valid=1 ⇒ o_mem_req_valid=1` 同拍；request 流顺序 == grant 流顺序（发送队列 FIFO；push→pop 最早 +1 拍、无同拍 bypass） | A-014/GAP-07；CYCLE §11B 时序性质 1/4 |
| per lane open allocation group ≤1；BMX 连发同拍 open+close、无 group 泄漏 | D-004；CYCLE §10 sva |
| held 快照一致性：held valid ⇒ 本拍 asm 视图 == held 内容（§11A mux 元数据与获选 candidate 一致直至 fire） | GAP-06 sva；F-113 |

## 1. reset 类（T-001…T-006）

| T-ID | TB 文件 | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- | :--- |
| T-001 | `test_reset.py` | 上电 reset 2 拍，无配置 | 全部 valid 输出=0；`o_lfsm_idle=1`；`o_walk_stall=0`；`o_*_cfg_ready=1`；query valid=0 | F-003, F-120；obs/全部 valid 端口 |
| T-002 | `test_reset.py` | 单 instruction 运行**中途**拉 reset 2 拍，释放后重发配置 | 中途状态清空（无残留 fire/reg_req）；重启后行为与全新运行逐拍一致（对齐向量前缀） | F-003, F-110 |
| T-003 | `test_reset.py` | reset 期间 drive 两配置通道 valid=1 + `i_shared_mem_ready=1` 等 | reset 期间不 accept、无任何输出脉冲；释放后需重发方可配对启动 | F-003, F-001；cfg 通道 |
| T-004 | `test_arbiter.py` | reset 后构造多 lane 同 `(inst_id,rd_mem_id)` eligible | 首 grant = A（cursor 复位值）；其后按 `[A,AMX,B,BMX]` RR | F-003, F-091 |
| T-005 | `test_c_path.py` | C FIFO 非空时拉 reset | `o_reg_req_valid` 复位拍起=0；重配后 C 流从空重启 | F-003, F-100 |
| T-006 | `test_reset.py` | 构造 held candidate 或发送队列在途 entry（`mem_ready=0` 堵住）后拉 reset | reset 优先于「保持已有 valid/payload」：candidate/queue/发送队列/query 全清 | F-003, F-111, F-113 |

## 2. smoke 类（T-010…T-013）

| T-ID | TB 文件 | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- | :--- |
| T-010 | `test_replay_typical.py` | 最小单 instruction 向量（M64/N32/K32/m16/B8，G=1/H=8）全输入恒 ready/idle | 配置→首 fire→末 fire→drain 全序列与向量等价（链首 +2 整形，§0.4）；fire 笔数 = golden 计数 | F-001, F-010, F-022, F-092（冒烟横切） |
| T-011 | `test_walker.py` | 任意 walker 运行全程 | `o_walk_stall==0` 每拍断言；内部 stall 通路 tie-off 不改变 token 流 | F-011；`o_walk_stall` |
| T-012 | `test_c_path.py` | 小形状 B8 instruction，`i_register_ready` 恒 1 | `o_reg_req_valid` 出现且逐拍 ≤1 笔；C FIFO 不积压（镜像 size ≤1 常拍） | F-100；`reg_c` 总线 |
| T-013 | `test_reset.py` | idle→单 instruction→drain | `o_lfsm_idle` 电平序列：启动后 0、drain 完成后回 1；中间无毛刺脉冲；idle 组成含配置 FIFO 与发送队列空（A-014 `rqp_empty`，CYCLE §13） | F-120；`o_lfsm_idle` |

## 3. directed·单元（T-020…T-065）

### 3.1 config_regs（`tests/unit/test_config_regs.py`）

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-020 | 两通道按序 valid、`inst_id` 相等 | 同拍 accept（ready&&valid）；instruction 寄存、walker 启动输出置位；FIFO 非满期 ready=1 | F-001；walk_cfg/lfsm_cfg 全 valid/ready/inst_id |
| T-021 | 两 FIFO head `inst_id` 不等（错序注入） | 协议错误断言触发（TB 捕获 assertion = pass）；不启动 | F-001（负例） |
| T-022 | 注满配置 FIFO（深度 2）再发第 3 笔 | 满时 ready=0 且不 accept；发送方保持 payload（TB 侧契约）；drain 后恢复 | F-001 |
| T-023 | 逐条非法结构注入：`k_groups=33`、`m_slice_count=3`、span=3、`n_step≠1`、`eu_mode=1`；另验证配置寄存后多拍稳定 | 每条触发对应断言；合法配置寄存值在运行全程不变（经下游地址/几何使用点核对） | F-002；`n_step`/`eu_mode`/`data_type`/`mx_*` 端口 |

### 3.2 walker（`tests/unit/test_walker.py`）

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-024 | m16、单 n_outer、无 K 尾（如 N64/K128）配置 | token 流逐拍 = 独立 `walk_golden` 序列（`WALK-SEQ-02` 口径） | F-010 |
| T-025 | 矩阵：m16/m32 × {N tail 9→[4,5]、10→[4,6]、17→[8,4,5]、整 8} × {K 整 / K 尾 outer}（加法级生成：`n_len`/`k_count` 现场维护） | 序列逐拍对拍（`WALK-TAIL-01`/`WALK-SEQ-03`）；loop 终值自检 `n_base==n_hw_count`、`k_base==k_groups` | F-010, F-002 |
| T-026 | 同 T-024/T-025 流 | token 字段逐字段对拍：`m_idx/n_idx/k_idx/n_span==1/first_mkn/last_mkn/walk_seq` | F-010 |
| T-027 | 全程运行 | `o_walk_stall==0`；无 `STALL RDQ_FULL` 路径存在（静态检查 + 运行断言） | F-011 |
| T-028 | 两条配置背靠背注入 | last token commit 拍 done；**次拍**启动下一条（精确拍以 golden 向量冻结）；两 instruction 可跨流水阶段重叠 | F-012 |

### 3.3 rdgen（`tests/unit/test_rdgen.py`，token 流由 walk 单元流驱动）

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-029 | m16/m32 × 单/多 n_outer × K outer 重访 token 矩阵，另含 **B4（m32）** 流 | A/AMX 入队 ⟺ `cnt_n_outer==0 && cnt_n_inner==0`；入队流与 golden set 去重（`rd_golden`）逐拍一致；B4 每 token ≤1 个 B entry 且 N4 owner 序保持（SRC-01 sec 17 条 2/22，单元级） | F-020 |
| T-030 | m32 token 流（M0/M1 slice） | B/BMX 入队 ⟺ `m_idx==0`；M1 不重入队（`LFSM-RD-02`）；m16 每 token 入队 | F-020 |
| T-031 | 含 C 的 token 流 | C entry ⟺ `cnt_k_outer==0 && k_local==0`；地址 `l0c_base+(m×n_hw+n)×16`；`rdgen_id`=首访 `walk_seq+1`；与 golden `ru_c_queue` 入队侧一致（`RU-C-KEY-01`） | F-025；`i_lfsm_cfg_n_hw_count`/`l0c_base_addr` |
| T-032 | 多 lane 同 token 流 | `rd_id` lane-local 从 0 逐入队递增；`rdgen_id=walk_seq+1` 从 1；reuse token 占号；同 token 跨 lane 共享 `rdgen_id`（`LFSM-RD-01/03`） | F-021 |
| T-033 | 同 token 多 RD 拍 | 全部 RdRequest 同拍 commit、无 partial batch（enq 集合完整性断言） | F-022 |
| T-034 | 四路配置（plain + MX）+ 越界配置注入 | `src_addr` 与 golden `_make_rd` 一致：A/B 线性、AMX tile-major（`rg_len`）、BMX 行线性 pair+块量化（`n_hw2`/`k_groups2`）；越界触发 TB 断言（fail-fast 负例） | F-023；四组 base/limit 端口 |
| T-035 | 非 MX 与 MX 配置各一 | LaneLoadEnd 排在各 **required** lane 末 RD 后；非 MX 时 AMX/BMX 无标记且其 Queue 恒空；每 required lane 恰 1 个标记（`LFSM-END-01`） | F-024；`i_lfsm_cfg_mx_mode_en` |

### 3.4 rd_queue（`tests/unit/test_rd_queue.py`）

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-036 | enq/pop 定向序列 + pop 反压 | head=最老；每拍 ≤1 head；仅 head dequeue；`asm_pop=0` 时 head/payload 保持；`enq−deq==size` | F-030, F-113 |
| T-037 | 单 entry enq | 拍末入队、当拍 head 不变、次拍可见（边 1 无同拍 bypass；`LFSM-TIME-01`） | F-031 |
| T-038 | 参数化小深度实例（如 depth=4）：灌至 depth−1；再越界灌 1 笔 | 计数/保持正确；越界触发 never-full 断言（负例捕获）；断言=失败而非流控 | F-032 |

### 3.5 assembler ×4（head 流由 golden per-lane enq 流直接驱动）

| T-ID | TB 文件 | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- | :--- |
| T-039 | `test_assembler_a.py` | 满 A key（M64×K32B/owner）head | 默认序 `EU_M_HALF_K_HALF` 展开 16×128B block；地址/字节与 golden `_emit_a` 一致；无 padding | F-050（非默认两序 → GAP-01） |
| T-040 | `test_assembler_a.py` | head 流中插入 bubble / loop transition / LaneLoadEnd | context 跨 bubble/transition 保持、不提前 emit；不跨 instruction 合并；A 全程无 padding | F-040, F-041, F-050 |
| T-041 | `test_assembler_b.py` | 连续偶/奇 N4 owner 流（含跨 N block 边界） | pair 合成 N8 → 2×128B；非尾单 N4 保持等待；pair 不跨 N block（REQUIREMENT_SOURCES §4.1） | F-055, F-040 |
| T-042 | `test_assembler_b.py` | 奇数 N coverage 尾单 N4 | 2×128B（各 64B valid+64B pad）；账目 128 valid+128 pad；buffer write 仅 128B（`LFSM-PAD-02`） | F-056, F-041 |
| T-043 | `test_assembler_b.py` | LaneLoadEnd 到达时仍有未满 context | 兜底 drain emit；优先级：填满 > Queue 空保持 > 几何尾 > LaneLoadEnd | F-040, F-110 |
| T-044 | `test_assembler_amx.py` | 连续 K key 流（含 K-outer transition 与 Queue bubble） | K-run 累积至 span 和=4 紧密 merge；跨 K-outer 不截断；M8×K4B=32B tile 序对拍 `_emit_amx_group`（`LFSM-ASM-03`） | F-060, F-040 |
| T-045 | `test_assembler_amx.py` | K 尾不足 K4B 的 run | 尾 tile 缺失 chunk = mem-pad fragment：出现在 source ranges、计入 valid、无 owner/tag/write；transport padding=0 | F-061, F-041 |
| T-046 | `test_assembler_bmx.py` | 多窗口 owner 流（MXFP8/4/HIF4） | N8×K(4/span) slot 窗口；窗口完整后按坐标序 4×32B block；完成序对拍 `_emit_ready_bmx_windows`；窗口池=2（1 active+1 待 drain） | F-065 |
| T-047 | `test_assembler_bmx.py` | 窗口内存在 walk 未覆盖 slot（含任意位置） | 该 slot 恒为 transport padding；无 owner/tag/write、不推进 pointer | F-066, F-041 |
| T-048 | `test_assembler_bmx.py` | 奇数 N 尾 + K 尾窗口 | N2 pair 补 1 pad slot（行 stride `n_hw2×4×span`）；K 尾按 2D block 补 pad row（`k_groups2`）；mem-pad 地址/footprint 对拍 golden | F-067, F-023 |
| T-049 | `test_assembler_bmx.py` | LaneLoadEnd 到达时窗口未满 | 强制窗口完成并 drain；不跨 instruction 合并 | F-065, F-040, F-110, F-024 |

### 3.6 cand_holder（`tests/unit/test_cand_holder.py`；对应规格 BandwidthPacker 持有职能）

> 驱动面：asm view 标量 stub（Step 6 冻结键）——`visible ≥ full_count`
> 判定与块账目在 assembler（D-001 emit-on-demand）；本 TB 注入
> `view_* / view_next_*` 标量验证 held 持有/seq/planned 锁存与
> fire_consume 递补。**边3 严格流水（GAP-06）**：held 捕获拍不 fire，
> 次拍起参与仲裁（链首 +1 拍）；replacement 链每拍 1 fire。

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-050 | 各 lane view 标量流（A/B 单 block、AMX/BMX 4 block，formable 拍注入） | formable（`visible≥full_count`，A/B=1、AMX/BMX=4）当拍形成候选并捕获入 held；不拆 block；非 instruction-last 不足带宽保持等待；可跨 N block | F-070 |
| T-051 | LaneLoadEnd 消费（end tag 置位）后的末笔 view 样本（A/B/AMX/BMX 全 lane，含 drain 与 BMX 窗口收尾） | **D-003（2026-10-14）**：UU 128B 下 instruction-last partial 结构性不可达（A/B `full_count=1`、AMX 块数恒 4 的倍、BMX 恒满窗口）——登记式断言全样本 `is_partial_beat==0`（实现保留路径 + sva，不构造可达激励）；末笔 `is_instruction_last=1` 逐一核对；无全 padding block；BMX 无 partial | F-071；`o_mem_req_is_partial_beat`（≡0）`/is_instruction_last` |
| T-052 | split 序列 + merge 组 | `rd_mem_id`：split 沿用来源 `rdgen_id`、merge 取最早、held=首 block 的 `rdgen_id`（`MEM-ARB-01`） | F-072；`o_mem_req_rd_mem_id` |
| T-053 | candidate 形成后 grant  withhold N 拍 | held candidate 每 lane 恰 1 个；未 grant 期 valid/payload 逐拍不变；`planned_base/planned_advance` 形成时锁存；候选形成拍当拍完成 held 捕获（边 2 同拍形成），**形成拍不 fire、次拍起可获选 fire（边3 严格流水，GAP-06）** | F-073, F-113 |

### 3.7 tag_checker（`tests/unit/test_tag_checker.py`）

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-054 | candidate 流 + `i_load_range_idle` 模式（含回卷、busy 段） | 从 `load_ptr` 连续分配；禁跳 busy、不搜其他 idle、后 owner 不越 head；回卷不比 pointer；`o_load_range_query_base` 序列 = golden `load_ptr` 轨迹（`LFSM-ALLOC-01`） | F-080；query 端口 |
| T-055 | 新 owner candidate 流（含 MX span） | binding 元数据与 golden `Binding`/`AllocationGroup` 一致；span 表 A/B=1、AMX/BMX=mx_tag_span；每 owner 恰一次 binding | F-081 |
| T-056 | split candidate 续写 | `planned_advance=0`：`o_load_range_query_valid=0`、不产生 `LoadPtrUpdate`、只改 byte offset；load_ptr 只推进一次 | F-082 |
| T-057 | held candidate + 逐拍翻转 `i_load_range_idle` | query=`{valid, planned_base, planned_advance}` 组合输出；eligibility 每拍重算；busy 时 candidate/binding/load_ptr/payload 全保持；`valid=0` 时 TB 强制回答 idle=1（A-004 相位契约自检） | F-083 |

### 3.8 arbiter（`tests/unit/test_arbiter.py`，T-004 见 reset 类；纯控制——`o_mem_req_*` 端口断言归 `test_req_sched.py`，A-014）

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-058 | 四路 candidate + 逐项 gate：`issue_room=0`（req_sched 满且不 pop）/ `source_ok[lane]=0` / `destination_ok=0` / valid=0（A-014：`shared_mem_ready` 不进 eligibility） | eligibility 四项与；每项缺失即无 grant；issue 拍 `o_mem_req_valid` ≤1 脉冲 | F-090；`issue_room`/`i_mem_source_ok`（req_sched 单元侧断言 `o_mem_req_valid`） |
| T-059 | 多 lane 异 `(inst_id,rd_mem_id)` + 同键矩阵 | 最小键优先；同键从 `rr_cursor` 按 `[A,AMX,B,BMX]` 扫描；仅 fire 更新 cursor 指向 granted 下一 lane；grant 序列对拍 golden `evaluate` | F-091 |
| T-060 | 单 lane candidate + 恒 ready（req_sched 集成） | **两拍落位（A-014/GAP-07）**：grant 拍 `phase="post"` 断内部 commit（consume/binding/load_ptr/RR）——与 golden fire 拍逐项一致；issue 拍（次拍）`phase="pre"` 断 `o_mem_req_*` 与 `o_load_ptr_update_*` 同拍脉冲、payload 逐字段等价（`LFSM-FIRE-01` 拆分口径） | F-092；`o_mem_req_valid`/`o_load_ptr_update_valid` |
| T-061 | 多笔 fire（含 split 复用），`mem_ready=0` 间歇 | 每次 pointer 推进恰 1 个 `LoadPtrUpdate`（issue 拍、与 request 同拍）；`old/new/advance` 正确、`new=(old+advance)%DEPTH`；`tag_range_base==old_ptr`；`advance>0`；ready=0 时 front 保持、恢复后续传、顺序不变 | F-093；buf_update 全端口 + req_sched 保持 |
| T-062 | A/B/AMX/BMX 各 lane fire 样本 + MX + padding 情形 | `buffer_writes[]`（index/offset/len）与 golden `MemRequest` 逐笔一致；`tag_ranges` 恒 1；`confirm_on_response` 仅整 range 末贡献 request=1；padding 不写不确认；MX range 覆盖完整 span；`src_addr/len/count`、三字 byte count 对拍（`MEM-BW-01`/`LFSM-PAD-03`） | F-094, F-082；mem_req 全 payload 端口 |
| T-063 | 跨 instruction fire 流 | `key_seq` per-lane 从 0 递增、instruction 开始清零；`key_inst_id/key_lane` 与 candidate 一致；`rd_id`/`rdgen_id` 从 1/0 重计 | F-094, F-021；`o_mem_req_key_*` |
| T-069 | lane X `destination_ok=0` 持续 + 其余 lane eligible | X 保持不 grant；其余 lane grant 不被阻塞、优先级序不变 | F-083, F-090, F-111 |

### 3.9 c_path（`tests/unit/test_c_path.py`，T-005/T-012 见 reset/smoke）

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-064 | C entry 流 + `i_register_ready` 正常/间歇 0 | `o_reg_req_*` 流与 golden `ru_c_queue` issue 逐拍一致；head valid/payload 保持至 fire；fire=valid&&ready 拍末 pop；每拍 ≤1 笔、无仲裁 | F-100；reg_c 全端口 |
| T-065 | rdgen 拍末新 C entry | 次拍起可 issue、当拍不出现（同边 1 相位）；never-full 断言（小深度负例同 T-038 方法） | F-100, F-031, F-032 |

## 4. directed·小集成（T-066…T-068，`tests/integration/test_bypass_chain.py`）

> queue+assembler+cand_holder+tag_checker+arbiter 单 lane 链（lfsm_top 缩配），
> 定向验证三条边的相位（PIPE §3 三边相位契约；`LFSM-TIME-01`）。
> 边3 为严格流水（DEV-2026-10-14，GAP-06）。

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-066 | 拍初 head 已就绪 + 全链路空闲 + 恒 ready | 边2 同拍：cycle-start head 当拍形成候选并 held 捕获（`phase="pre"` 断捕获前无 grant）；**边3 严格流水**：grant 落次拍（断 `fire_consume`/load_ptr 内部 commit，链首 +1）；**发送段（A-014）**：`o_mem_req_valid`/`o_load_ptr_update_valid` 同拍双脉冲落**再次拍**（issue 拍，链首合计 +2）；replacement 链稳态 1 grant/issue 每拍；fire/issue 元数据与 golden `preview_bypass` 逐笔一致、拍号按 +2 整形（`LFSM-TIME-01` 更新口径） | F-073, F-031, F-092 |
| T-067 | 拍末新入队 entry | 当拍（enq 拍）不出现于 assembler 输入/任何下游；次拍起可消费 | F-031 |
| T-068 | LaneLoadEnd 结尾的 block 流 | drain 后末笔 candidate `is_instruction_last=1`；fire 后该 lane held candidate/队列全空；无残留 context | F-071, F-110 |

## 5. directed·集成回放（T-070…T-077，`tests/integration/test_replay_typical.py`）

> 顶层 lfsm_top + golden 向量逐拍回放（§0.4）。全部挂载 T-076 公共
> 断言套件。向量依赖 GAP-04。用例选择 = REQUIREMENT_SOURCES SRC-09
> 的 4EU 子集 + b2b。

| T-ID | 向量 | 对拍要点 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-070 | TC02（4EU m16 B8，M64/N64/K128，latency 3） | 基线全链路：fire/issue 流逐笔等价 + 链首相移整形（§0.4 GAP-06/07 口径，+2 拍）；A/B 地址、fire 序、C 流 | F-010…F-100 横切（基线） |
| T-071 | TC08（4EU m32，M128/N32/K256，latency 0） | m32 return-base：M1 不重载 B（`LFSM-RD-02`/`EFSM-BASE-01` 口径）；latency 0 输入模式 | F-020, F-012 |
| T-072 | TC13（4EU N tail 9→[4,5]，M64/N36/K64，latency 0） | N tail 切分 + B 奇数 N 尾 padding 账目 | F-010, F-055, F-056 |
| T-073 | TC15（4EU m32 MXFP8，M128/N40/K160，latency 5） | AMX K4 dense merge + BMX 窗口 + MX span 原子分配 | F-060, F-065, F-081 |
| T-074 | TC17（4EU m32 B4，M128/N128/K128，latency 3） | B4 N8 block 边界、B 在途峰值（A-002 包络锚点）、`4EU-CAL-IDEAL` 计数 | F-055, F-032, F-112 |
| T-075 | TC-B2B-01 / TC-B2B-02（4EU b2b 2/4 instruction） | 背靠背：边界不混合、`rd_id`/`rdgen_id` 重计、配置 FIFO 配对流水、两 instruction 跨阶段重叠 | F-012, F-110 |
| T-076 | （公共套件，挂载于全部回放/系统 TB） | §0.5 不变量套件全程断言（原十项 + 边3/发送段/D-003/D-004 增补行） | F-112, F-030, F-041 |
| T-077 | dev 附加形状：N tail 17→[8,4,5]（B16/B4）、窄 N block、K 尾组合 | I7 增量边界对拍 | F-050, F-055, F-092 |

## 6. stress 类（T-080…T-086，`tests/integration/test_backpressure.py`）

> 反应式驱动（无需向量处用手写激励；与 golden 对齐处用向量前后缀
> 对齐）。覆盖 A-011 第 2 类（有限长反压内 never-full 必须成立）。

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-080 | 运行中段 `i_load_range_idle[X]=0` 持续 N 拍（扫描 N=1/4/16/64） | X 的 candidate/query/binding/load_ptr 全保持、无 fire；他 lane 正常；恢复后 fire 序列与 golden 相位对齐（仅延迟、不改变） | F-083, F-090, F-113 |
| T-081 | `i_shared_mem_ready=0` 持续 N 拍（A-014：出口反压；队列未满期间 grant 照常、cnt 到 2 后冻结） | req_sched front 保持、无 pop；队列到 2 → `issue_room=0` → grant 冻结；held/context 全保持；恢复后 FIFO 序续传（顺序 == grant 序）且稳态 **1 issue/拍** 保持不减半——2-slot 深度设计点（单级寄存会退化为每 2 拍 1 笔）；TB 镜像 req_sched `cnt ≤ 2`；与 issue 拍 `phase="pre"` 口径一并断言 push→pop ≥+1 拍 | F-090, F-093, F-113；`i_shared_mem_ready`/`issue_room` |
| T-082 | `i_mem_source_ok[X]=0` 间歇序列 | 仅 X 停；他 lane grant 序不变（优先级不受阻塞 lane 影响） | F-090, F-111；`i_mem_source_ok` |
| T-083 | `i_register_ready=0` 持续/间歇 | C FIFO head 保持、不 pop；恢复后顺序 issue 无丢重 | F-100；`i_register_ready` |
| T-084 | 四 lane 同时 eligible 高负载段（A 突发 16 block + m16 B 每 token owner + MX 窗口，可由 TC15/TC17 向量段裁剪） | 每拍 ≤1 fire；优先键序保持；RR 有界等待（连续 eligible lane 在 K 拍内必获 grant，TB 监视器断言，无饿死） | F-090, F-091, F-111 |
| T-085 | T-080…T-083 各反压序列下镜像占用监视 | 有限长反压内 RDQ/C FIFO/BMX 窗口池占用 ≤ 参数深度、req_sched `cnt ≤2`（never-full 成立；A-011 第 2 类） | F-032 |
| T-086 | TYPICAL 4EU 子集 + b2b 全向量回放 + 镜像占用插桩 | 仲裁积压（无反压亦存在）峰值 ≤ 深度（A 16/B 128/AMX 8/BMX 4+窗口池 2/C 8；A-002 结论 1、A-011 第 1 类）；包络外 worst-legal 不测（GAP-02 waiver） | F-032 |

## 7. corner 类（T-090…T-097，`tests/integration/test_corner.py`）

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-090 | 最小形状 G=1、H=8、单 K group（first==last token） | first/last_mkn 同 token 成立；LaneLoadEnd 紧随唯一 RD 块；完整 drain | F-010, F-024 |
| T-091 | 包络内最大形状回归（m32 M128 × n_hw=128 × k_groups=32 子集组合，B16/B8） | 全向量对拍；结构断言（`k_groups≤32`/`m_slice≤2`）边界取等不触发 | F-002, F-010 |
| T-092 | K 尾 outer（`k_count<k_step`）× N tail {9,10,17} 矩阵 | walker 尾 outer 序列 + B pair / AMX run 在 K 尾处的 merge/pad 对拍 | F-010, F-055, F-060 |
| T-093 | 当前 instruction drain 期间下一条配对到达（配置 FIFO 非空边界 + FIFO 满边界） | 次拍启动不错拍；配置 accept 与 drain 无互相干扰；无跨 instruction block/request | F-001, F-012 |
| T-094 | A owner 16 block split 续写序列 + 中途 `destination busy` 插入 | 续写无 `LoadPtrUpdate`、query valid=0；busy 期保持；恢复后 byte offset 连续正确 | F-082, F-083 |
| T-095 | stub 侧构造 release→重分配相邻拍序列（反应式 Buf/RAM） | `fresh_idle_guard`：release 拍 C → C+1 `idle` 可见但 `load_range_idle=0` → 最早 C+2 `idle→loading`（`BUF-VIS-02`；stub 侧断言，F-112 外部条目） | F-083, F-093 |
| T-096 | MX 小形状扫描：{MXFP8 span1, MXFP4 span2, HIF4 span4} × {N 奇/偶} × {K 整/K 尾} | AMX run/tile、BMX 窗口、mem-pad、span 原子分配逐组合对拍（`EFSM-GATE-02`/`LFSM-ALLOC-02` 口径） | F-060, F-061, F-065…F-067, F-081；`data_type`/`mx_bytes_per_k0` |
| T-097 | **b2b 异几何序列**（D-002 注解专项）：I0=B8 整 N block → I1=MXFP8+N 尾 9 → I2=B4+N 尾 17，背靠背注入；激励=golden 单 instruction 流按 `inst_id` 拼接（对拍用单元流 + 顶层回放 +2 整形） | 几何注解不混叠：I0 尾部 entries 在 I1 配置已寄存后仍严格按 I0 几何 drain（assembler 不读当前 cfg，D-002）；I1/I2 的 span/`n_tail_single`/窗口几何各自正确；无跨 instruction block/request；BMX 窗口池在 I1→I2 边界不泄漏；`rd_id`/`rdgen_id`/`cand_seq` 重计正确；cfg FIFO 边界（T-093 口径）叠加 | F-110, F-040, F-065, F-067, F-021；D-002 |

## 8. system 类（T-100…T-103，`tests/integration/test_system_stub.py`，Step 10 预览）

> 反应式 stub 闭环：TB 内建 Buf/RAM tag 状态机（`range_idle` 含
> `fresh_idle_guard` 两拍规则 + capacity，REF-04）、固定 latency MEM
> stub（REF-08；response 不经 LFSM，仅服务计数）、register port stub
> （可编程 ready）。本组为 Step 10 SYSTEM_TEST 的预科；sign-off 口径
> 由 SYSTEM_TEST 冻结。

| T-ID | 激励 | 期望 / 断言 | 覆盖 |
| :--- | :--- | :--- | :--- |
| T-100 | TYPICAL 4EU 全子集 + b2b 在 stub 闭环中跑 | 全程端口行为与回放向量一致（stub 在恒 ready/idle 配置下退化为回放等价）；stub 侧：MEM req==rsp、release/confirm 生命周期合法、tag 终态全 idle（`TOP-DONE-01` 口径）；F-112 外部条目（#14/#20）在 stub 侧断言 | F-112, F-110 |
| T-101 | 组合场景：四 lane 并发 + destination busy 段 + 指令边界（b2b）交叠 | 优先级不变量保持；无跨 instruction 混合；busy 解除后无丢重；`o_lfsm_idle` 最终归 1 | F-110, F-111, F-083 |
| T-102 | 伪随机长运行（随机形状 × 随机反压序列，sidecar 调度，种子固定可复现） | 无死锁（进度监视）；公共断言套件全程；最终计数 = 独立 golden 公式（unique keys = `G×(S+H)`/MX ×2、release advance 总和、C 数 = `S×H`） | F-112, F-020 |
| T-103 | 任一闭环用例收尾 | 完成谓词：walker 无 active、四路 Queue/Assembler context/held candidate/C FIFO/**发送队列/配置 FIFO** 全空、`o_lfsm_idle=1`；request 计数 = golden 计数 | F-120, F-112 |

## 9. 覆盖闭环与运行方式

- **F-xxx 覆盖**：44 个 F-xxx 的 T-xxx 反向索引见
  `TRACEABILITY.md` §2（每行 ≥1 个 regression-sensitive T-xxx；
  GAP-01/02 两个已决策 waiver 除外）。任一 F-xxx 被移除时其映射
  T-xxx 必失败（回归敏感），满足方法 Step 8 action 2。
- **端口覆盖**：PORT_LIST §4 全部 65 个端口 key + domain reset 的
  T-xxx 映射见 `TRACEABILITY.md` §1；本文件每个 T-xxx 行内「覆盖」
  列列出新增端口 key（首次覆盖处）。
- **运行命令**：

```bash
# 全量回归（pytest 收集 tests/unit + tests/integration）
python3 -m pytest designs/LFSM/pycircuit/tests -x -q
# 单 TB 独立运行（示例）
python3 designs/LFSM/pycircuit/tests/unit/test_walker.py
# C++ 构建（每日回归，expect 为功能判据）
pycircuit build designs/LFSM/pycircuit/tests/integration/test_replay_typical.py \
  --target cpp
# 长随机 sidecar（T-102）
pycircuit build designs/LFSM/pycircuit/tests/integration/test_system_stub.py \
  --target cpp --tb-schedule-mode sidecar
# Verilator sign-off（Step 10）
pycircuit build <tb>.py --target verilator --run-verilator
```

- **增量挂钩**（plan Step 9 增量 → 新增/激活的 T-xxx；回放向量类
  测试另依赖 `golden` todo 的向量落盘，GAP-04）：
  I0→T-001, T-003, T-013；I1→T-011, T-020…T-028；
  I2→T-029…T-038；I3→T-039…T-043, T-050…T-063, T-066…T-071；
  I4→T-044…T-049, T-073, T-096；I5→T-080…T-085, T-094；
  I6→T-005, T-012, T-031, T-064, T-065；I7→T-002, T-072,
  T-074, T-075, T-077, T-090…T-093, T-097；Step 10→T-076, T-086, T-095,
  T-100…T-103。每增量跑全量回归 + `pycircuit build --target cpp`
  （plan Step 9）。
