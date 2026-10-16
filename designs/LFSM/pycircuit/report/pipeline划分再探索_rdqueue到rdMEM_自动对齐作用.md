# Pipeline 划分再探索：rd_queue→4:1 rd MEM 链路（含自动对齐作用实录）

> 汇报材料 · LFSM（4EU UU mode）PyCircuit V6 设计
> 事项：A-004 v4 两拍查询契约落地后，重估 rd_queue 出口 → 4:1 rd MEM 输出链路的
> pipeline 划分是否有优化空间；并把 V6 自动周期平衡（`_v5_bal`）作为探索仪器
> 全程实战——变体快速原型、划分建议读出、假设完备性检查
> 计划来源：[pipeline划分再探索与自动对齐计划](../../../../.cursor/plans/pipeline_dccbaad9.plan.md)
> 前置改造：[A-004 v4 两拍契约改造结果](A-004v4_tag查询两拍契约_改造结果与寄存器层数分析.md)
> 实验代码：`designs/LFSM/pycircuit/explore/pipe_div/`（隔离目录，主 RTL 未动）
> 整理日期：2026-10-16

---

## 1. 一句话结论

**D1（投机查询）以 −56bit 的代价回收了 A-004 v4 的全部延迟代价**（allocation
候选 cap→fire 从 2 拍回到 1 拍，功能经链路 TB 全项验证），建议走 gate-first
流程落地；D2（付运快照）按 Step 9 时序评估再触发；D3（框架自动重定时）在
MLIR 层达成全部探索目标，同时暴露一个 C++ 后端仿真 bug（已取证上报）——
这一正一反两组结果共同验证了"生产代码 `_v5_bal=0` 纪律 + 探索期放开使用"
的分工是成立的。

## 2. 探索问题与基线

A-004 v4 把 tag 查询改为"第一拍查询、第二拍返回"（断 R1 同拍环），代价是
链首 +1 拍。探索问题：① 释放的决策环时序预算能否回收该代价；② 自动对齐
在探索中怎么发挥作用。

基线链（D0 = 现状）：

```mermaid
flowchart LR
    QH["q head 寄存"] -->|边1 无 bypass| AV["asm view 组合 T"]
    AV -->|边2 同拍| CH["held 捕获 拍末 T"]
    CH -->|"held Q T+1"| TCK["query 出模块 T+1"]
    TCK -->|"回答 T+2（v4）"| ARB["dest_ok+仲裁+11A mux T+2"]
    ARB --> RQP["req_sched push 拍末 T+2"]
    RQP -->|"front 直出 T+3"| MEM["o_mem_req"]
```

## 3. 关键语义发现（修正 v4 代价的口径）

**v4 的 +1 拍只落在 `planned_advance>0` 的 allocation 候选上；split/续写候选
（`advance=0`）依 A-004 语义本就不查 destination（`dest_ok` 恒 1、无 guard
等待），首拍即可 fire。** A lane 一个 owner 16 个 block 里只有 block0 付代价：
mirror 实测（`lat_first10`）D0 = `[2,1,1,1,1,1,1,1,1,...]`（block0 2 拍、
其余全 1 拍），链路 TB 逐拍验证一致。即"per-lane 1 fire/2拍"应精确表述为
"per-allocation-候选 +1 拍"——真实负载下吞吐损失远小于字面。[A-004 v4 报告](A-004v4_tag查询两拍契约_改造结果与寄存器层数分析.md)
§5 的表述以此为准，cand_holder/tag_checker docstring 已含"pa=0 恒 1"条款。

## 4. 探索基建（explore/pipe_div/）

| 文件 | 作用 |
| :--- | :--- |
| [pd_lib.py](../explore/pipe_div/pd_lib.py) | 参数化链路 top（D0–D3H 五变体）：复刻 lfsm_top 的 fw 接线，真 assembler×4 + cand_holder×4 + tag_checker（可换变体）+ arbiter + §11A mux + req_sched；queue head 由 TB 直驱 |
| [tag_checker_spec.py](../explore/pipe_div/tag_checker_spec.py) | D1 投机查询：查询源 = assembler `view_next_*`（与 cand_holder 捕获同源）+ 内部 `load_ptr/load_ptr_post` mux；`dest_ok = rq_v ? idle : 1` 无 guard |
| [payload_snap.py](../explore/pipe_div/payload_snap.py) | D2 付运快照：per-lane 自由采样 payload view（≈2.2Kb/lane），§11A mux 源改寄存器 |
| [payload_delay.py](../explore/pipe_div/payload_delay.py) | D3H 托管延迟：cycle-1 零锚点迫使框架在每 lane 子模块内自动放 `_v5_bal`（零手写寄存器） |
| [tb_pd_common.py](../explore/pipe_div/tb_pd_common.py) | A-lane 精确 mirror（asm 块游标/chd/tck 两变体公式/arb/rqp 2-slot）+ 全反应式驱动 + `metrics_only` 独立指标 |
| [balance_report.py](../explore/pipe_div/balance_report.py) → [balance_report.md](../explore/pipe_div/balance_report.md) | MLIR `_v5_bal` 计数/位宽/top10 + compile_stats 汇总 + mirror 指标 → markdown |

功能验证口径：A-lane 精确 mirror（48 fire / 48 issue 全程逐拍 expect，含
payload 摘要、LoadPtrUpdate 字段与 req_sched 环形槽物理探针
cnt/pr/pw/push/pop/s0/s1）；多 lane 聚合仲裁由既有
[test_cand_tck_arb_pipe.py](../tests/integration/test_cand_tck_arb_pipe.py) 覆盖。
观测摘要 dg = payload 15 字段 xor-fold（探测错位/串扰类错误），TB 为编译期
schedule（无运行时回读，全部期望来自 mirror）。
回归：`pytest designs/LFSM/pycircuit/tests/unit` = **28 passed**（主 RTL 未动）。

## 5. 变体对比总表（实测）

| 变体 | 划分假设 | alloc cap→fire | fire→issue | regs（折算 module×instance） | `_v5_bal` | 仿真 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D0 基线 | 现状三拍 + v4 两拍查询 | 2 拍（split 1） | 1 拍（反压 ≤5） | 5712b（基准） | 0 | 通过 |
| D1 投机查询 | 查询源改 `view_next_*`，回答落首个 held 拍 | **1 拍** | 1 拍 | **5656b（−56b）** | 0 | **通过** |
| D2 付运快照 | payload 每拍采样，mux 源改快照 | 2 拍（split 1） | 1 拍 | ≈14500b（+8788b） | 0 | 通过 |
| D3 自动重定时（flat） | payload 域整体标 cycle-1 | 2 拍 | 2 拍 | — | **1226 个 / 10007b** | **PYC992 拒编译** |
| D3H 托管自动重定时 | 同上，bal 托管进 4 个小模块 | 2 拍 | 2 拍 | ≈15000b | 1314 个 / 13985b | 编译过；**仿真命中后端 bug**（§8） |

数据口径：`compile_stats.json`（每模块 `max_logic_depth/reg_bits`，模块去重
——表中已按实例数折算）；延迟/节奏来自 mirror（经 TB 逐拍验证一致）；
`max_logic_depth=47` 各变体相同——该值被探索 harness 的 digest xor-fold 云
主导（观测逻辑伪影，非设计路径），R2 真实环路深度需在 Step 10 sign-off
流程上评估，不在本次结论中使用。

## 6. D1 投机查询（推荐落地）

**机制**：查询不再从 held 快照发，而从 assembler `view_next_*` 发出——与
cand_holder 捕获条件（`view_next_formable & (fire | ~h_v)`）严格同源，查询
目标 = 下一拍将被 held 的候选；planned_base 用 `fire_consume ? load_ptr_post :
load_ptr` 内部 mux（与 cand_holder 锁存规则一致）。held 候选无新捕获时从
held `planned_*` 重发（busy 重查）。回答寄存一拍后恰好落在候选首个 held 拍，
`dest_ok = rq_v ? idle : 1` **无需 match guard**（在途回答按构造恒描述当前
held 候选）。

**验证**（[tb_pd_d1.py](../explore/pipe_div/tb_pd_d1.py)，全项通过）：
- alloc 候选 cap→fire = 1 拍（mirror `[1,1,1,...]`，TB 一致）——v4 代价全回收；
- busy→idle 窗口、mem_ready 反压窗口、3 owner×16 block 全程 48 fire/48 issue
  无丢失、payload 摘要逐笔一致；
- `_v5_bal = 0`（纪律内实现）。

**代价与影响**：tag_checker 每 lane +2 输入（`view_next_formable/advance`，
4 lane 共 8 根线，源在 lfsm_top 已是现成信号）；寄存器 −56b（guard 三元组
寄存器 60b → 在途有效位 4b）；`o_load_range_query` 相位提前一拍（外部
Buf/RAM 视角：查询描述的是"次拍候选"，sync-RAM 读契约不变）；A-004 v4 的
`valid=0 ⟹ 答 1`、fresh_idle_guard 均不受影响。**落地路径**：gate-first——
先改 PORT_LIST/伪码 §10/FEATURE_LIST F-083 相位条款，再改 RTL + 集成 TB
时相平移（链首 +2 → +1，比 v4 前还少一拍）+ golden 再生成。

## 7. D2 付运快照（条件触发）

payload（5 组 32-lane 向量 + 标量 + binding）每拍自由采样进 per-lane 快照
寄存器，§11A mux 源改为寄存器——R2 数据环（BMX 32-slot mem-pad + ≤32 writes
dest_base 加法链）整体移出 grant 路径。控制时序与 D0 完全一致（fire/issue
逐拍一致，TB 通过）。代价 +8788b（4×2197b，即工作记录"P1 全量"量级；
"P1-lite"= 只对 BMX/AMX 两 lane 快照 ≈ +4394b，A/B 浅 lane 保持组合）。
**触发条件不变**：Step 9 时序评估显示数据环 → req_sched 写端超标时启用，
优先 lite。与 D1 正交，可叠加（D1 的 view_next 查询不受快照影响）。

## 8. D3/D3H：自动对齐实战记录（用户点名部分）

### 8.1 三角色兑现情况

| 角色 | 设计 | 兑现 |
| :--- | :--- | :--- |
| 变体快速原型 | 目标域标 cycle-1（零锚点法），框架 `_align→delay_to` 自动补全 | D3 flat：一次编译出 1226 个 `_v5_bal`（10007b）的可仿真网表（MLIR 级）；零手工寄存器 |
| 划分建议读出器 | 解析 `_v5_bal_*` 位置/位宽 | 读出 = "全 payload 路径（含 keys/fire/grant/upd）+ req_sched 内 state 侧"——与 D2 手工快照的内容清单逐项吻合，另多出**控制信号**（fire/grant/room/pw）——提示该假设把控制也拖进了数据延迟域 |
| 假设完备性检查 | 意外 bal = 遗漏依赖 | 见 §8.2/§8.3 两个实锤 |

### 8.2 发现一：PYC992 编译预算（flat 形态）

D3 flat 把 1226 个 bal（≈10Kb）集中进单个 flat top 模块，
`predicted_compile_cost=6.9e4 > 4.0e4` 触发 PYC992 硬预算拒编译
（pycc.cpp:1160 硬编码常量）。托管形态（D3H，每 lane 一个 ~2.2Kb 子模块）
即过——**同一重定时假设，"放哪"决定可编译性；这本身就是 D2 式分散快照
优于集中打拍的一个量化证据**。

### 8.3 发现二：跨路径一致性框架不管（push_valid 教训）

D3H 首版仿真失败（issue 早一拍）：`push_valid`（c0）进 req_sched 后，cnt
路径纯 c0 不补延迟、slot 写使能路径被 payload（c1）对齐补 1 拍——**框架按
组合点局部对齐，不保证跨路径的控制/数据一致性**。修复 = `push_valid` 与
payload 一起重锚 cycle-1（[pd_lib.py](../explore/pipe_div/pd_lib.py) 注释处）。
这正是"延迟位置决定行为处必须显式"准则（与前次讨论的结论）的实证。

### 8.4 发现三：C++ 后端仿真 bug（已取证）

D3H 修复后网表经 MLIR 逐级核查**结构正确**（slot 写数据 = bal'd 上拍 key、
写使能 = bal'd push&pw），但 C++ 仿真在 c4 给出**同拍同源自相矛盾**读数：

```
f_dbg_s0  = v_get s_key_seq[0]        = 0   ✓（与 mirror 一致）
f_dbg_pr  = pr                        = 0   ✓（与 mirror 一致）
f_i_key_seq = mux(pr, s[1], s[0])     = 1   ✗（同步逻辑下恒等于 s[0]=0）
```

同一拍、同一寄存器组、同一选择信号，直读与经 mux 读给出不同值——电路级
不可能，且全部 dbg 探针（cnt/pr/pw/push/pop/s0/s1，环形槽物理模型）与
mirror 完全一致（D0/D1/D2 同套探针全绿，证明 mirror 与 TB 相位无误）。
对照实验：不加 `PYC_DISABLE_INSTANCE_EVAL_CACHE` 宏（cache-on 路径）
重建后 `pyc_tb` 直接 `stack smashing detected` 崩溃；加宏（仓库标准绕过）
则稳定复现上述不一致。**结论：设计无误；当前后端对 bal 密集 + 跨 cycle
混合电路的仿真求值不可信**（疑与已记录的 instance eval-cache 问题同源，
且 cache-off 路径亦有残留）。证据：`/tmp/pd_d3h_nocache/`（崩溃复现）、
`python3 explore/pipe_div/tb_pd_d3h.py`（c4 自相矛盾稳定复现）。
建议作为 toolchain issue 上报。这也反向坐实了生产侧 `_v5_bal=0` 结构
断言的现实必要性：后端修复前，bal 密集设计无法被现有仿真流程门禁。

### 8.5 自动对齐使用准则（本次验证版）

| 场景 | 结论 |
| :--- | :--- |
| 探索期前馈重定时原型（"如果把这段推迟一拍会怎样"） | 好用：零手工寄存器、立即可编译（MLIR 级）、placement 可读 |
| 读出框架建议的割断位置并与手工划分对照 | 好用且与 D2 手工清单吻合 |
| 暴露假设的全部代价（遗漏依赖、控制被拖入） | 好用（§8.2/§8.3） |
| 含回边/控制环的重定时 | 不适用：框架局部对齐不保跨路径一致（§8.3），反压环（room）需显式预留 |
| 依赖当前 C++ 后端仿真门禁 bal 密集设计 | 暂不可用（§8.4），修后端或限 MLIR 级分析 |
| 生产定稿代码 | 维持 `_v5_bal=0` 显式纪律 + 结构断言 |

## 9. 结论与后续项

1. **推荐落地 D1（投机查询）**：−56b 成本回收 v4 全部延迟，链路 TB 全项
   验证。走 gate-first：PORT_LIST/PSEUDOCODE §10/F-083 相位条款 → RTL →
   集成 TB 时相（链首 +2→+1）与 golden 再生成。
2. **D2 触发条件保持**：Step 9 数据环超标时上 P1-lite（≈+4.4Kb），可与 D1 叠加。
3. **D3 类自动重定时**：作为探索手段成立（§8.5 前三行）；作为生产手段需
   待后端仿真修复，且须补跨路径一致性设计（push/room 显式预留）。
4. **toolchain**：上报 C++ 后端仿真 bug（§8.4，复现与证据齐）。

## 10. 链接索引

| 类别 | 条目 |
| :--- | :--- |
| 探索代码 | [explore/pipe_div/](../explore/pipe_div/)（pd_lib / tag_checker_spec / payload_snap / payload_delay / tb_pd_common / tb_pd_d0..d3h / balance_report） |
| 自动产出 | [balance_report.md](../explore/pipe_div/balance_report.md) |
| 生产 RTL | [lfsm/tag_checker.py](../lfsm/tag_checker.py)、[lfsm/cand_holder.py](../lfsm/cand_holder.py)、[lfsm/lfsm_top.py](../lfsm/lfsm_top.py) |
| 既有验证 | [tests/integration/test_cand_tck_arb_pipe.py](../tests/integration/test_cand_tck_arb_pipe.py)、[tests/unit/test_tag_checker.py](../tests/unit/test_tag_checker.py) |
| 背景文档 | [pipeline 工作记录](pipeline划分修改工作记录与下一步方向评估.md)（方向1 P1-lite 预评估）、[A-004 v4 改造报告](A-004v4_tag查询两拍契约_改造结果与寄存器层数分析.md)、[ASSUMPTIONS.md](../docs/ASSUMPTIONS.md) A-004 v4 段 |
| 计划 | [pipeline划分再探索与自动对齐](../../../../.cursor/plans/pipeline_dccbaad9.plan.md) |
