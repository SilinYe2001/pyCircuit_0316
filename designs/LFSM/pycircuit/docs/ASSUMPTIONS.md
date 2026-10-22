# LFSM (4EU UU mode) ASSUMPTIONS

> Step 2–3 交付物（依据 `docs/pycircuit_implementation_method.md` §1
> order-3）。记录所有**推断性决策**：规格未显式规定、或从 golden 模型
> 结构反推的微架构选择。每条含：陈述 / 依据 / 验证方式。
> 建立日期：2026-10-13；**v2 修订 2026-10-13**（复查后人工决策落档：
> A-002/A-011 深度口径 = TYPICAL 包络 + 显式 waiver；A-003
> `tag_ranges[]` 定长 1；A-004 query 相位契约 = `valid=0` + 外部默认
> `idle=1`）；**v3 修订 2026-10-13**（用户决策：WalkConfig loop 几何
> 不下发——`n_blocks[]`/`n_outer_count`/`k_step_per_outer`/
> `k_outer_count` 移除，walker 加法级现场维护 base/length，消除
> TOP 侧除法与 n_blocks 寄存数组；A-005.1 改写）。
> 需求源编号见 `REQUIREMENT_SOURCES.md`。

---

## A-001 首访去重替代 CAM（data-key dedup → 计数器条件）

**陈述**：规格的 `generated_data_keys[lane]` set（SRC-01 sec 7.2）在
硬件中以 walker 计数器条件实现，不做内容寻址。新 key 判定退化为纯
组合条件：

| 集合 | data key | 新 key ⟺ 首访条件 |
| :--- | :--- | :--- |
| A/AMX | `(inst_id, m_idx, k_idx)` | `cnt_n_outer == 0 && cnt_n_inner == 0` |
| B/BMX | `(inst_id, k_idx, n_idx)` | `m_idx == 0`（m16 下恒真） |
| C | `(inst_id, m_idx, n_idx)` | `cnt_k_outer == 0 && k_local == 0` |

**依据**：walk 循环嵌套（SRC-03 sec 6/8/9，REF-01
`_next_transition` 优先级）为
`k_outer → n_outer → m_slice → k_local → n_inner`。

- A/AMX：固定 `(m,k)` 在每个 n_outer block 内被访问一遍（n_inner 扫
  全 block）；全 instruction 首访 = 第一个 n_outer block 的第一个
  n_inner 位置 ⟺ `cnt_n_outer==0 && cnt_n_inner==0`。
- B/BMX：`k_idx = cnt_k_outer*k_step + k_local` 与 `(cnt_k_outer,
  k_local)` 一一对应（尾 outer `k_count<k_step` 区间仍不相交）；固定
  `(k,n)` 在同一 `(k_outer,n_outer,k_local,n_inner)` 下随 m_idx 重访
  （仅 m32 有 m_idx=1），首访 ⟺ `m_idx==0`。m16 时 m_idx 恒 0，每
  token 都是新 key，与 SRC-01 sec 7.2「4EU 每 token 最多一条 B」一致。
- C：固定 `(m,n)` 随 `k_local`、`cnt_k_outer` 重访，首访 ⟺
  `cnt_k_outer==0 && k_local==0`。

「成功入队才登记 key」（SRC-01 sec 7.2）映射为：判定结果仅在
`walk_advance` commit 时生效；walker stall 时条件重复求值但不产生新
入队——与 REF-02 `_needed_rds`（evaluate 计算、commit 才 `add`）
的 evaluate/commit 分割一致（该 stall 分支在 UU baseline dormant：
无 RDQ 容量 stall；保留表述是为与 EFSM 共享 walker 语义完整）。

**验证**：golden 对拍 —— `tools/dump_lfsm_golden.py`（golden todo）
dump REF-02 set-based 每拍 `needed_rds`/owner 流，与 V6 计数器版逐拍
比对（T-xxx 映射入 TEST_PLAN，覆盖 m16/m32 × 单/多 n_outer block ×
K outer 重访）。

---

## A-002 无上限结构的有界实现 + 在途积压口径（人工决策 2026-10-13）

**陈述**：规格禁止容量反压（SRC-01 sec 2.3/6：RD Queue 无上限、
walker 无 RDQ stall；C FIFO 同，SRC-08 sec 6），因此所有队列/池取
**参数化深度 + never-full 断言**（仿真期断言，非硬件反压）。断言语义
= 环境前向进展契约：MEM/RegisterUnit/Buf-RAM 的反压持续时间有限，
占用不越界；越界即 TB 失败而非流控。

**积压的两类来源（v2 澄清）**：

1. **仲裁积压**——合法形状下单口 1 fire/拍与生成率的固有失配
   （A 每 key 突发 16 block、m16 下 B 每 token 1 owner），**无需
   任何反压即出现**（TC02 的 B 在途 46 即纯仲裁积压）；
2. **反压积压**——destination busy / `mem_ready=0` / `source_ok=0` /
   `register_ready=0` 期间。

两类积压最终都由 **RD Queue + held candidate** 承接（context 钉死
几何界、块池 ≈ candidate 级，见结论 2），因此**队列深度必须覆盖
在途 owner 峰值**——这是深度选型的正确插桩对象。

**插桩方法**（正式插桩并入 `tools/dump_lfsm_golden.py`，golden todo，
可复跑）：

- **探针 A（结构占用，burst 表示）**：REF-07 `FsmSimulator` 逐拍记录
  各结构占用峰值（post-commit 采样）；
- **探针 B（表示无关物理量，v2 新增）**：`pending_mem_owners[lane]`
  （「已生成、未首次 fire」的在途 owner 数）逐拍峰值——该量不随
  池/队列表示变化，是深度选型依据；同时逐笔 fire 记录
  `len(buffer_writes)/len(tag_ranges)/advance` 最大值；
- 驱动用例：TYPICAL 4EU 子集 TC02/08/13/15/17 + TC-B2B-02 + 合法
  应力形状 X-MAXK(M128/N32/K1024/m32/B8)、X-HIF4(M128/N68/K288/
  m32/HIF4+mx)、X-MXFP4(M128/N48/K192/m32/MXFP4+mx)、X-MAXN
  (M128/N512/K128/m32/B8)、X-WORST-A(M128/N4/K1024)、X-WORST-AMX
  (HIF4 M128/N4/K1024)、X-WORST-B-m16(M64/N512/K1024)、
  X-WORST-B-m32(M128/N64/K1024)。

**实测（v2，以探针 B 为准）**：

| 量 | TYPICAL 峰值 | worst-legal 实测 | 备注 |
| :--- | ---: | ---: | :--- |
| 在途 owner A | 10（TC08） | **60**（M128/N4/K1024） | ≈ m_slice×k_groups(64) − 已 fire |
| 在途 owner B | **64**（TC17）、46（TC02） | **513**（M64/N512/K1024/m16） | m16 下生成率 1 owner/拍 |
| 在途 owner AMX | 6（TC15） | 61（HIF4 M128/N4/K1024） | |
| 在途 owner BMX | 34（TC15） | ~34 | 生成率 0.125/拍 < drain，结构性 ≈2 窗口 |
| 在途 owner C | 1 | 1 | 生成 ≤1/拍、issue 1/拍无竞争 |
| burst `entries[lane]` | ≤2 | ≤2 | burst 块池吸收积压时的**假象读数**，非深度依据 |
| merge pending B / AMX | 1 / 3 | 1 / 3 | 几何界（pair ≤2 owner / run ≤4 key） |
| BMX 打开窗口数 | 1 | 1 | 4EU 窗口按坐标序串行完成（REF-03） |
| burst blocks 池 | A 166（TC08） | A **622**（X-MAXK） | 建模产物，不搬进硬件（结论 2） |
| held candidate | 1/lane | 1/lane | 结构不变量（SRC-01 sec 5/12） |

**结论 1（队列深度选型；人工决策 = TYPICAL 包络）**：

| 结构 | 深度选型 | 说明 |
| :--- | :--- | :--- |
| RD Queue A | **16**（参数）+ never-full | TYPICAL 在途 10 → 2 幂 |
| RD Queue B | **128**（参数）+ never-full | TYPICAL 在途恰 64（TC17）→ 加倍 2 幂留余量 |
| RD Queue AMX | **8**（参数）+ never-full | TYPICAL 在途 6 |
| RD Queue BMX | **4**（参数）+ never-full | 在途 34 主要由窗口池承接（≈32 slot + 余量） |
| BMX 窗口 context 池 | **2 窗口**（1 active + 1 完成待 drain）+ never-full | 每窗口 ≤32 owner slot（MXFP8 N8×K4） |
| C FIFO | **8**（参数 `C_FIFO_DEPTH`）+ never-full | 实测 1；覆盖 `register_ready` 短反拍 |
| B merge context | 2（几何常量） | N4 pair |
| AMX merge context | 4 key（几何常量） | `4/span` 上界 |

深度均为**参数**：覆盖全合法形状只需调参（A 64 / B 1024 / AMX 64），
不改结构（waiver 见 A-011）。v1 曾按 burst `entries≤2` 误选 RDQ=8
（表示相关假象读数），v2 已按在途口径纠正。

**结论 2（DataBlock 池 —— 对计划决策 #2 的重要扩展）**：Python 模型
的 `assembler.blocks` 突发式无界 deque（实测应力峰值 622，合法形状
下随 `16×m_slice×k_groups` 增长）是**建模产物，不搬进硬件**。硬件
采用 **emit-on-demand**：DataBlock 是 merge/expansion context 的
**组合展开视图**，在 candidate 形成拍按需生成，不设置深池：

- A：1 个 owner 展开 context + block cursor（0..15），按需展开；
- B：≤2 owner pair context；
- AMX：≤4 key 的 K-run context；
- BMX：窗口 context（≤32 slot）完成拍组合展开 4 个 block；
- 每 lane 物理缓冲 ≈ 1 个 candidate 的 `full_count` 个 block
  （A/B `full_count=1`，AMX/BMX `full_count=4`，128B 总线）+ 同拍
  bypass 通路；
- **在途积压由 RD Queue 承接（v2 明确）**：context 钉死几何界后，
  未展开的 owner 停在队列里——队列深度与结论 1 口径必须配套
  （该配套关系是 v1 遗漏项）。

候选/`rd_mem_fire` 请求流与突发式 golden **逐拍等价**（DataBlock 内
容、顺序、candidate 组成、`rd_mem_id` 均不变；golden packer 本就按 FIFO 序
取 block；`_can_form` 的「可见同 instruction 块数」在两种表示下同值
——由已完成 context 的状态函数计算）。该等价性当前为**结构性论
证**：Step 4-6 伪码必须把「可见块数」函数精确化，等价性由 golden
对拍在 `rd_mem_fire` 粒度闭环。最终池尺寸在 Step 4-6
`ALGORITHM_PIPELINED.md` 定稿。

**结论 3（积压位置，v3 增补 2026-10-14）**：两类积压（仲裁/反压）
由 **RD Queue + held candidate（上游侧）+ req_sched 发送队列
（2-slot，出口侧，A-014）** 承接：context 恒几何界、块池恒
candidate 级；never-full 的受力点 = RD Queue（结论 1 深度）、
C FIFO 与 BMX 窗口池（反压包络，见 A-011）、req_sched（2，
never-overflow——`mem_ready=0` 由出口队列承接，经 `issue_room`
冻结 grant 传播到上游）。I5 反拍增量定向压测
「队列在途数 ≤ 结论 1 深度」不越界。

---

## A-003 candidate / fire 元数据上限（端口定长展平；tag_ranges 已决策）

**陈述**：单次 `rd_mem_fire` 元数据按定长数组展平：

- `buffer_writes[]` 上限 **32**（4EU 128B 总线下最大单次 fire 的
  owner 数 = BMX MXFP8 窗口 32 slot；每 owner span=1 时 write 数 =
  tag 数 ≤ 32；实测 max 24，TC15 BMX 窗口）；
- `LoadPtrUpdate.advance` ≤ **32**（MXFP8 32×1 / MXFP4 16×2 /
  HIF4 8×4 = 32；SRC-01 sec 9.3：request advance = 窗口真实 owner
  数 × span；实测 max 24）；
- `tag_ranges[]` 定长 **1**（人工决策 2026-10-13）：UU 下每笔
  candidate 的全部 owner 恰属**同一** allocation group——A split
  续写首次 fire 建立的同一 range；B pair 两 owner 在第一笔
  candidate 同时首次 fire、一次 `LoadPtrUpdate` 一起分配、第二笔
  续写；AMX K-run group 一次分配、group 内 candidate 都属它；BMX
  4EU 窗口按坐标序完成、每笔 candidate 恰一窗口、owner 全新。实测
  10 用例共 **4628 笔 request `len(tag_ranges)` 全部 =1**。SRC-01
  sec 14 规则 5 的多 range 情形（一笔 request 同时贡献不同历史
  LoadPtrUpdate）在 UU 不出现，为通用/RU/乱序窗口保留。

**依据**：SRC-01 sec 9.3/11.4/14；SRC-04 sec 14；探针 B 实测。
A/B candidate `full_count=1` 时 new owner ≤2（B pair）、A 恒 1。
**验证**：golden dump 逐 fire 校验三上限（writes ≤ 32 /
advance ≤ 32 / ranges == 1）；越界即断言失败。

---

## A-004 `load_range_idle` 边界澄清：增加 `o_load_range_query` 输出

**陈述**：规格只命名输入 `load_range_idle[lane]`（SRC-01 sec 3.1），
但该 bit 的计算需要 candidate range（SRC-05 sec 7.6/8.1：
all-idle + 非 fresh_idle_guard + `occupied+advance<=DEPTH`）。
Buf/RAM 为外部模块，故 LFSM 增加输出
`o_load_range_query[lane] = {valid, base, advance}`：

- 有 held candidate 且 `planned_advance>0`：`{1, planned_base,
  planned_advance}`；
- 无 held candidate，或 held candidate 为 split 续写
  （`planned_advance=0`，`destination_ok` 恒真）：`{0, load_ptr, 0}`；
- **跨模块相位契约（人工决策 2026-10-13）**：query `valid=0` 时
  外部 Buf/RAM **必须**回答 `load_range_idle=1`（无 range 需要检
  查）；该默认连同相位（eligibility 每拍对 query 重算、全部读取
  cycle-start 状态）写入 PORT_LIST 端口契约。

外部 Buf/RAM 据此组合算出 `load_range_idle[lane]` 回读；eligibility
每拍重算（SRC-07 sec 3(5)）。split 后续 request（`planned_advance=0`）
不查 destination（SRC-01 sec 11.3：只改 byte offset）。

**验证**：PORT_LIST（Step 3）冻结相位；集成 TB 的反应式 Buf/RAM
stub（含 `fresh_idle_guard` 两拍规则）按 REF-04 `range_idle` 实现。

**v4 修订（2026-10-16，两拍查询契约）**：相位契约由"同拍组合回答"
改为"**第一拍查询、第二拍返回**"——`o_load_range_query` 第 N 拍发
出，`i_load_range_idle` 作为第 N−1 拍查询的**寄存储备回答**在第 N
拍被采样（sync-RAM 读语义；外部 `fresh_idle_guard` 两拍规则不受影
响，`valid=0` 必答 1 规则保留）。tag_checker 内新增 per-lane 查询
上下文寄存器 `rq_cv/rq_pb/rq_pa`（上拍候选三元组）+ match guard：
held candidate 稳定时次拍起 match=1、回答与候选对齐；capture 边
（fresh/replacement）首拍三元组必变 → guard 强制 `dest_ok=0`，屏蔽
在途陈旧默认 1——**最早 fire = 候选第 2 个 held 拍**（per-lane 稳态
1 fire/2 拍，arbiter 跨 lane 聚合仍 1 fire/拍）；`planned_advance=0`
候选不查询、`dest_ok` 恒 1 不变。`query valid=0 ⟹ dest_ok=1` 的默认
语义保留（仅作用于无查询需求的候选）。R1 跨模块同拍组合环随之断开
（pipeline 报告"同拍环不可内部切分"的前提由本契约修订解除）。
**验证**：`tests/unit/test_tag_checker.py`（T-054…T-057 重定时）+
`tests/integration/test_cand_tck_arb_pipe.py`（guard/节奏/层数结构
断言）；PORT_LIST/PSEUDOCODE §10 等全量文档同步见后续项。

---

## A-005 配置存储与配对握手

**陈述**：

1. ~~`n_blocks[]` 上限 16 项打包寄存~~（**v3 改写，2026-10-13 用户
   决策**）：WalkConfig 不再携带 `n_blocks[]` / `n_outer_count` /
   `k_step_per_outer` / `k_outer_count` 派生字段（消除 TOP 侧 ceil
   除法/迭代生成与 16 项寄存数组；相对 SRC-04 sec 2.1 的契约偏差记
   入 PORT_LIST §8 适配 8）。walker 已逐拍维护 m/k/n index，在
   transition 边界以加法级运算（inc/cmp/sub/mux，无除法器）现场维护
   每个 loop 的 base/length：
   - N block：`remaining = n_hw_count − n_base`；
     `n_len = (remaining==9 || remaining==10) ? 4 : min(8, remaining)`
     ——与 SRC-02 sec 3.5.2 的 9→[4,5]/10→[4,6] 规则逐项等价
     （rem=9→[4,5]、rem=10→[4,6]、rem=17→[8,4,5] 等已逐值核对）；
     N_OUTER transition 时 `n_base += n_len`；
   - K outer：`k_count = min(k_step, k_groups − k_base)`；K_OUTER
     transition 时 `k_base += k_count`；`k_step = m_mode ? 4 : 8`
     （1-bit mux，无需下发）；
   - loop 结束条件为 `base ≥ total`（`n_hw_count` / `k_groups`），
     无需显式 outer count（消除 `ceil(k_groups/k_step)` 除法）。
   与 golden 含这些字段的 `WalkConfig`（REF-05）的等价性由 MKN 序
   列逐拍对拍闭环（FEATURE_LIST F-010 / TEST_PLAN T-xxx）；
2. WalkConfig / LFSMInstructionConfig 两条 valid/ready 通道各设参数
   化深度配置 FIFO（默认 2，支持 b2b 验收的 2–4 instruction 流）；
   配对 = 两 FIFO head `inst_id` 相等时同拍接收，不等即协议错误
   （断言；合法 TOP 保证同 `inst_id` 四份配置同序到达，SRC-02
   sec 3.7）；
3. 配置合法性（SRC-02 sec 3.3、SRC-03 sec 5）由上游 TOP 保证；LFSM
   内部仅断言硬件安全所需结构不变量（如 `k_groups≤32`、
   `m_slice_count≤2`、span ∈ {1,2,4}），以及 loop 现场生成的结构性
   自检（N block 序列终值 `n_base==n_hw_count`、K outer 终值
   `k_base==k_groups`，v3）；
4. walker 不解析原始 M/N/K size，直接消费 WalkConfig 派生字段
   （SRC-03 sec 3.1）；C 地址所需 `n_hw_count`/`l0c_base_addr` 由
   LFSMInstructionConfig 携带（SRC-02 sec 3.6.2）；
5. **静态配置为 build-time 参数（v2 补记）**：
   `load_bus_bytes_per_cycle`、bufa/l0b/amx/bmx slots、
   `a_block_order`、`rd_queue_depth` 兼容字段、各队列/池深度参数
   均属模块实例静态配置（SRC-02 sec 3.8、SRC-04 sec 3），不设
   运行时配置端口、不随 instruction 下发。

**验证**：I0/I1 增量 + b2b 用例（TC-B2B-01/02 向量）。

---

## A-006 ~~不采纳~~ **采纳 `lfsm_req_pipe` 类发送段（v2：2026-10-14 被 A-014 推翻）**

**原 v1（2026-10-13，历史保留）**：DOC_SYNC_QUEUE pending 项
`lfsm_req_payload_pipe`（payload 晚一拍）不采纳，保持 SRC-01 sec 13
的单拍原子提交语义。

**v2（2026-10-14 用户决策，即预登记 A-014）**：推翻 v1——选择与 MEM
下发解耦：§11A mux 载荷（`RdMemRequest` + `LoadPtrUpdate` **同组**）
经 **2-slot 发送队列 req_sched** 在 **issue 拍（grant 次拍）** 原子
发出；内部 grant commit（消费/binding/load_ptr/group/RR）仍在 grant
拍原子；端口`update+request` 同拍原子关系原样保留（sec 13/14.1 端口
口径不变）；`i_shared_mem_ready` 语义落位队列出口（issue 拍采样），
eligibility 改用 `issue_room`。完整规格偏差登记见 A-014 条与
TRACEABILITY GAP-07。

**依据**：境内链过深的时序收口动机（PIPE §8.1）；DOC_SYNC_QUEUE
pending 项本列为 RTL 候选，方向正确，采纳时补全 LoadPtrUpdate 同组、
2-slot 深度与反压闭环。

---

## A-007 存储原语选型：RD Queue/小寄存器组用 `domain.signal` 数组

**陈述**：四路 RD Queue、C FIFO、配置 FIFO、绑定/上下文寄存器组均
以 `domain.signal()` 数组 + head/tail pointer 实现（小并行寄存器
组），不直接使用 `m.fifo` / `m.rv_queue`：

- RD Queue 需要「cycle-start head 可见、拍末 commit 入队、禁止同拍
  bypass、反压保持」的精确相位，用显式寄存器数组最直白可控；
- 全仓库尚无 `m.fifo` 的 V6 设计用户（仅规格 §8 表格），其
  ready/valid 语义与本设计相位未经验证——属潜在原语缺口；
- 若后续评估改用 `m.fifo`，须先按 `AGENTS.md`/`docs/updatePLAN.md`
  gate-first 验证其语义，不做 backend-only 绕过。

**依据**：方法文档 Step 3.6（小结构用 `domain.signal()` 数组）；
PRC-01 §8；计划「风险与注意」。

---

## A-008 evaluate/commit 映射与同拍 bypass 实现

**陈述**：规格两拍语义（SRC-01 sec 5）映射为 V6 cycle-0 组合求值 +
`domain.signal()` 拍末提交：

- candidate/eligibility/grant、`o_load_range_query`、
  `RdMemRequest`/`LoadPtrUpdate` 有效载荷 = cycle-0 组合输出；
- Queue→Assembler 无同拍 bypass = assembler 只读 `domain.signal()`
  寄存的 head 状态；rdgen 拍末 `<<=` 入队，次拍可见；
- Assembler→Packer→Arbiter 同拍 bypass = cycle-0 纯组合链（本拍新
  emit block / 新 candidate 可本拍 fire）；
- 未 grant 时 held candidate 的 valid/payload 经
  `sig.assign(..., when=...)` 保持（SRC-01 sec 5 保持清单）。

**依据**：SRC-01 sec 5；SRC-07；REF-03 `preview_bypass`（Python
侧的等价结构）；计划「模块分解」。

---

## A-009 walker 无 stall 输入与 `walk_stall` 输出

**陈述**：UU baseline 中 walker 无 RDQ 容量 stall（SRC-01 sec 6），
顶层不引 `walk_stall` 输入；`o_walk_stall` 输出恒 0（SRC-01 sec 3.2
兼容观察字段）。共享 walker 逻辑仍按 SRC-03 实现 stall 保持语义
（内部 tie-0），以便与 EFSM/未来扩展复用同一 FSM 描述。

---

## A-010 reset 与 idle 行为

**陈述**：reset 最高优先级（SRC-01 sec 16），清空：walker 状态与
counter、per-lane `rd_id`/`rdgen_id` 序号、四路 Queue、Assembler
context、Packer held candidate、binding/request context、load_ptr、
C FIFO、配置 FIFO、RR cursor（复位值 = A，SRC-04 sec 11）。reset
期间忽略全部输入握手；配置 FIFO 在 reset 后从空开始接受配对。

---

## A-011 验收包络与 worst-legal waiver（人工决策 2026-10-13）

**陈述**：never-full 断言按积压来源分两类界定：

1. **仲裁积压（合法形状固有，与反压无关）**：深度按 TYPICAL 4EU
   子集（TC02/08/13/15/17）+ 4EU b2b（TC-B2B-01/02）在途实测取
   2 幂（A 16 / B 128 / AMX 8 / BMX 4 + 窗口池 2 / C 8，见 A-002
   结论 1）→ never-full **仅在该包络内的形状保证成立**。超出包络
   的合法形状（worst-legal 实测在途：A 60 / B 513 / AMX 61）显式
   排除在保证范围外，作为**已知偏差（waiver）记入 TRACEABILITY
   gap 表**：有界实现与规格「无上限队列」语义在该形状下不等价，
   不静默忽略。深度为参数：覆盖全合法形状只需调参（A 64 /
   B 1024 / AMX 64），不改结构。
2. **反压积压（I5 定向激励）**：`shared_mem_ready=0`（A-014：出口
   req_sched 承接 + `issue_room` 回传）/
   `register_ready=0` / `source_ok=0` / destination busy 的
   **有限长度**序列内 never-full 必须成立；任意长持续反压不保证
   ——与规格「禁止容量反压 ⇒ 容量不得成为限制因素」一致，前向
   进展由系统级（EFSM release/MEM service）保证。

**验证**：TEST_PLAN 按两类分别设 never-full 断言用例；SYSTEM_TEST
记录包络与 waiver 状态，TRACEABILITY gap 表登记 waiver 行。

---

## 假设一览与后续步骤挂钩

| ID | 主题 | 后续步骤落点 |
| :--- | :--- | :--- |
| A-001 | 首访去重计数器条件 | FEATURE_LIST（F-xxx）+ walker/rdgen 伪码 + T-xxx 对拍 |
| A-002 | 在途积压口径 + 深度选型（TYPICAL 包络，**已决策**） | PORT_LIST 参数表 + ALGORITHM_PIPELINED 池尺寸 + TEST_PLAN never-full 断言 |
| A-003 | fire 元数据上限 32/32/**1**（**已决策**） | PORT_LIST 定长数组 |
| A-004 | `o_load_range_query` + 相位契约（**已决策**） | PORT_LIST 新输出 + 集成 TB stub |
| A-005 | 配置存储/配对 + build-time 静态参数（v3：loop 几何 walker 现场生成） | PORT_LIST + config_regs/walker 伪码 |
| A-006 | ~~不采纳~~ 采纳发送段（v2，A-014） | CYCLE §11B/PORT_LIST §5.3/TRACEABILITY GAP-07（端口 issue 拍，sec 13 deviation） |
| A-007 | `domain.signal` 数组选型 | ALGORITHM_PIPELINED 存储原语选型 |
| A-008 | evaluate/commit 映射 | ALGORITHM_PIPELINED cycle 映射 |
| A-009 | walker 无 stall | PORT_LIST（`o_walk_stall` 恒 0） |
| A-010 | reset 优先级 | TEST_PLAN reset 类 |
| A-011 | 验收包络 + worst-legal waiver（**已决策**） | TEST_PLAN / SYSTEM_TEST + TRACEABILITY gap 表 |

---

## A-012 起预登记（Step 4–6 及复查期间的派生决策，Step 7 正式编号提升）

以下决策已落地于 Step 4–6 三份算法文档（2026-10-13/14，多为用户拍板），
`TRACEABILITY.md`（Step 7）复查时按表逐条提升为 A-012 起：

| 项 | 内容 | 落点 |
| :--- | :--- | :--- |
| D-001 | emit-on-demand：DataBlock=merge context 的组合展开视图，物理块池=0；收集/展开槽尺寸定稿（A:1、B:1+2、AMX:4+4、BMX:2×32 src） | SEQ §8/§14.3、PIPE §5（A-002 结论 2 的定稿落点） |
| D-002 | per-inst 几何经 entry 注解下发（B `single`、AMX `span/kgs/is_k_tail`、BMX `span/kgs/nhw2/nblk_*`），assembler 不读当前配置寄存（b2b 混叠安全） | SEQ §14.2、CYCLE §3.2 |
| D-003 | UU 128B 下 `is_partial_beat≡0`、instruction-last partial 不可达（实现保留 + sva） | SEQ §14.4 |
| D-004 | 每 lane ≤1 个 open allocation group；`confirm=group_final` 组合条件 | SEQ §14.4（A-003 同系） |
| D-005 | `cand_seq` per-lane、instruction 首 candidate 清零；golden dump 按 instruction 重排号对拍 | SEQ §15、TEST_PLAN |
| 命名 1（2026-10-14） | `allocator` → **`tag_checker`**（prefix `lfsm_tck`）：直观体现 tag 状态查询/`destination_ok` 职能；语义=规格 DestinationAllocator，接口契约不变 | 五文档同步（CYCLE §10 / PIPE §2/§4/§6 / SEQ §2/§3/§10 / FEATURE_LIST §0/§1.11/§2/§5 / PORT_LIST §9） |
| 命名 2（2026-10-14） | `packer` → **`cand_holder`**（prefix `lfsm_chd`）：直观体现 candidate 持有/寿命管理；语义=规格 BandwidthPacker 的持有职能（满宽判定与块展开在 assembler） | 同上五处同步 |
| 解耦（2026-10-14） | arbiter **纯控制**：输入仅 ballot（`cand_valid/inst/rd_mem_id`）+ dest_ok + 准入；输出仅 `fire/grant_lane/fire_consume`；`RdMemRequest` payload 的 4:1 mux 剥离至顶层组合（CYCLE §11A） | PIPE §3/§4/§6/§8、CYCLE §11/§11A/§13 |
| 边3 严格流水（2026-10-14，**规格偏差**） | cand_holder→arbiter **禁同拍**：仲裁输入束 = held 快照寄存（数据/键类全部同源）+ 当拍 ready 电平；fresh 形成拍不 fire（**链首 +1 拍**），replacement 链维持 1 fire/拍；held 快照一致性不变量（held valid ⇒ asm 视图 == held 内容）；相对 SRC-01 sec 5「Packer→Arbiter 允许同拍 bypass」不再采纳；golden 对拍口径从逐拍精确等价改为**逐笔 fire 元数据等价 + 链首相移** | PIPE §3（分段/性质）、§4/§8、CYCLE §9、SEQ §9/§14.3/§15（D-006）、FEATURE_LIST F-073；TEST_PLAN Step 8 落实回放口径 |
| **发送段 req_sched（2026-10-14，**规格偏差**＝A-014，推翻 A-006 v1）** | 选择与 MEM 下发解耦：§11A mux 载荷（`RdMemRequest`+`LoadPtrUpdate` 同组）经 **2-slot 发送队列**在 **issue 拍（grant 次拍）** 原子发出；内部 grant commit 仍原子；`i_shared_mem_ready` 落位队列出口（issue 拍采样），eligibility 改 `issue_room`；深度 2 保 ready=1 稳态 1 issue/拍；端口「update+request 同拍」原子关系原样保留（sec 13/14.1）；相对 SRC-01 sec 13「grant 拍端口即发」为**端口时序偏差**；golden 对拍口径＝逐笔等价 + 链首相移合计 **+2 拍**；`o_lfsm_idle` 增含队列空 | PIPE §3（三拍分段）、§2/§4/§6/§8.1、CYCLE §11A/§11B/§13/§14、SEQ §10/§12/§14.3/§15（D-007）、FEATURE_LIST F-090/F-092/F-093/F-120、PORT_LIST §4.3/§4.4/§5.3/§9/§10；TRACEABILITY GAP-07；TEST_PLAN 端口断言 |

备注：命名权威 = `designs/LFSM/pycircuit/docs/*`；计划文件
（`.cursor/plans/lfsm_uu_v6_*`）按指示保持冻结不改，其中旧名
（allocator/packer/lfsm_alc/lfsm_pck）按本表映射到现名。
TRACEABILITY 端口矩阵使用 `PORT_LIST.md` §4 端口 key（未受改名影响）。
