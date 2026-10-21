# pyCircuit 语法查找手册

审查或编写 pyCircuit 代码时按类别对照本表。每类给出**写法 → 说明 → 源码/文档链接**（链接相对本文件，`#L数字` 为源码行锚点）。

- 主指南：[新手 Agent 操作指南](prompts.md) · 命令：[Agent 命令参考](commands.md)
- 权威契约：[PRIMITIVES.md](../PRIMITIVES.md)（`pyc_*` 原语 C++/Verilog 双实现约定）、[FRONTEND_API.md](../FRONTEND_API.md)、[PyCircuit_V5_Spec.md](../PyCircuit_V5_Spec.md)

## 1. 字面量与常量

| 写法 | 说明 | 链接 |
|---|---|---|
| `u(width, value)` / `s(width, value)` | 无符号/有符号定宽字面量 | [literals.py](../../compiler/frontend/pycircuit/literals.py#L58) |
| `U(value)` / `S(value)` | 自动推宽字面量 | [literals.py](../../compiler/frontend/pycircuit/literals.py#L50) |
| `m.const(value, width=...)` | 模块内常量（支持 list → vector） | [hw.py](../../compiler/frontend/pycircuit/hw.py#L1102) |
| `@const` | 常量生成函数装饰器 | [design.py](../../compiler/frontend/pycircuit/design.py#L169) · [CONST_METAPROGRAMMING.md](../CONST_METAPROGRAMMING.md) |

### 1.1 编译期整数工具（`pycircuit.ct`，host 侧纯 Python，不生成硬件）

写地址运算、位宽计算时用，全部在 Python 层求值：

| 写法 | 说明 | 链接 |
|---|---|---|
| `ct.clog2(n)` / `ct.flog2(n)` | ⌈log₂⌉ / ⌊log₂⌋ | [ct.py](../../compiler/frontend/pycircuit/ct.py#L14) |
| `ct.div_ceil(a, b)` / `ct.align_up(v, a)` | 整除向上取整 / 对齐 | [ct.py](../../compiler/frontend/pycircuit/ct.py#L30) |
| `ct.pow2_ceil(n)` / `ct.pow2_floor(n)` / `ct.is_pow2(n)` | 2 的幂工具 | [ct.py](../../compiler/frontend/pycircuit/ct.py#L46) |
| `ct.bitmask(w)` / `ct.onehot(i, w)` / `ct.decode_mask(ids, w)` | 掩码 / one-hot / 解码常量 | [ct.py](../../compiler/frontend/pycircuit/ct.py#L55) |
| `ct.wrap_inc/wrap_dec(v, mod, step)` | 环形计数 | [ct.py](../../compiler/frontend/pycircuit/ct.py#L103) |
| `ct.slice_width(msb, lsb)` / `ct.bits_for_enum(n)` | 切片宽 / 枚举编码宽 | [ct.py](../../compiler/frontend/pycircuit/ct.py#L121) |
| `ct.gcd/lcm/clamp` | 整数工具 | [ct.py](../../compiler/frontend/pycircuit/ct.py#L76) |

## 2. 组合逻辑运算符（`Wire` / `Reg` 上直接用）

| 类别 | 写法 | 说明 | 链接 |
|---|---|---|---|
| 算术 | `a + b` `a - b` `a * b` | 无除法/取模 | [hw.py `Wire`](../../compiler/frontend/pycircuit/hw.py#L251) |
| 位运算 | `a & b` `a \| b` `a ^ b` `~a` | — | [hw.py](../../compiler/frontend/pycircuit/hw.py#L301) |
| 移位 | `a << n` `a >> n` | 移位量可为 int 或 Wire | [hw.py](../../compiler/frontend/pycircuit/hw.py#L325) |
| 比较 | `== != < <= > >=` | 默认无符号；有符号用 `s()` 字面量 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L353) |
| 位选/切片 | `w[i]` `w[hi:lo]` `w[i][j]` | vector 端口支持多维下标 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L512) |
| `Reg` 读写 | `r.out()` / `r.set(next, when=...)` | `.out()` 读当前值，`.set()` 写下期值 | [hw.py `Reg`](../../compiler/frontend/pycircuit/hw.py#L730) |

向量（多 lane）运算符的打包约定见 [vec-operators.md](../vec-operators.md)。

## 3. 选择、拼接与位宽变换

| 写法 | 说明 | 链接 |
|---|---|---|
| `cond.select(a, b)` | 二选一（`Wire`/`Reg` 方法） | [hw.py](../../compiler/frontend/pycircuit/hw.py#L464) |
| `mux(cond, a, b)` | V5 选择（保持周期标签） | [v5.py](../../compiler/frontend/pycircuit/v5.py#L1751) |
| `priority_mux(sel_vals, default)` | 优先级多路选择 | [v5.py](../../compiler/frontend/pycircuit/v5.py#L1822) |
| `cat(a, b, ...)` | 位拼接（高位在前） | [hw.py](../../compiler/frontend/pycircuit/hw.py#L2578) · V5 [v5.py](../../compiler/frontend/pycircuit/v5.py#L1856) |
| `zext/sext/trunc(v, width=W)` | 零扩/符扩/截断 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L2627) |
| `unsigned(v)` | 显式去符号位解释 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L2642) |

## 4. 端口声明

| 写法 | 说明 | 链接 |
|---|---|---|
| `m.input("en", width=1)` | 输入端口（支持 `shape=` 向量、`signed=`） | [hw.py](../../compiler/frontend/pycircuit/hw.py#L1035) |
| `m.output("count", wire_of(sig))` | 输出端口；V5 中 `wire_of()` **只允许**用在这里 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L1116) · [v5.py `wire_of`](../../compiler/frontend/pycircuit/v5.py#L1109) |
| `m.clock("clk")` / `m.reset("rst")` | 时钟/复位端口（定义在基类 `Module` 上） | [dsl.py](../../compiler/frontend/pycircuit/dsl.py#L104) |
| `m.wire(sig)` / `m.named_wire(name, width=)` | 中间连线声明 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L1141) |
| `m.inputs(s, prefix=)` / `m.outputs(s, x, prefix=)` / `m.state(s, clk=, rst=, prefix=)` / `m.connect(a, b)` | 按 spec 批量声明端口/状态并连接（结构化 IO 主路径） | [hw.py](../../compiler/frontend/pycircuit/hw.py#L1695) · 例 [pipeline_builder.py](../../designs/examples/pipeline_builder/pipeline_builder.py) |
| `submodule_input(inputs, key, m, domain, ...)` | V5 双模式输入（独立=端口，被调用=读父级 dict） | [v5.py](../../compiler/frontend/pycircuit/v5.py#L1058) |

## 5. 寄存器与状态

| 写法 | 说明 | 链接 |
|---|---|---|
| `m.reg(clk, rst, en, next, init)` | 底层寄存器：`rst→q<=init`，否则 `en→q<=d` | [hw.py](../../compiler/frontend/pycircuit/hw.py#L1370) · [pyc_reg.v](../../runtime/verilog/pyc_reg.v) |
| `m.out("x", domain=cd, width=W, init=0)` | 命名状态变量（推荐），返回 `Reg` | [hw.py](../../compiler/frontend/pycircuit/hw.py#L1288) |
| `domain.signal(width=W, reset_value=0, name="x")` | V5 寄存器声明 | [v5.py](../../compiler/frontend/pycircuit/v5.py#L209) |
| `sig <<= expr` / `sig.assign(expr, when=cond)` | V5 寄存器写；读拍与写拍差 1→DFF，差 0→组合别名 | [PyCircuit_V5_Spec.md](../PyCircuit_V5_Spec.md) |
| `domain.next()` | 推进一个周期 | [v5.py](../../compiler/frontend/pycircuit/v5.py#L152) |

## 6. 存储原语

| 写法 | 说明 | 注意 | 链接 |
|---|---|---|---|
| `m.sync_mem(clk, rst, ren=, raddr=, wvalid=, waddr=, wdata=, wstrb=, depth=, name=)` | 1R1W **同步读**存储 | 读有 1 拍延迟；同地址读写返回**旧数据**；复位不清内容 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L2277) · [pyc_sync_mem.v](../../runtime/verilog/pyc_sync_mem.v) |
| `m.sync_mem_dp(...)` | 2R1W 同步读存储 | 两个读口均为旧数据语义 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L2306) · [pyc_sync_mem_dp.v](../../runtime/verilog/pyc_sync_mem_dp.v) |
| `m.byte_mem(clk, rst, raddr=, wvalid=, waddr=, wdata=, wstrb=, depth=, name=)` | 字节寻址存储 | **组合读**、同步写；复位不清内容 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L2250) · [pyc_byte_mem.v](../../runtime/verilog/pyc_byte_mem.v) |
| `lib.SRAM(m, cd, ren, raddr, wvalid, waddr, wdata, wstrb, depth=...)` | `sync_mem` 封装，返回 `rdata` | 同上 | [lib/sram.py](../../compiler/frontend/pycircuit/lib/sram.py) |
| `lib.Mem2Port(m, cd, ren0, raddr0, ren1, raddr1, ..., depth=...)` | `sync_mem_dp` 封装，返回 `rdata0/rdata1` | 同上 | [lib/mem2port.py](../../compiler/frontend/pycircuit/lib/mem2port.py) |

语义细则：[PRIMITIVES.md §4](../PRIMITIVES.md)。

## 7. 队列与握手（ready/valid）

| 写法 | 说明 | 注意 | 链接 |
|---|---|---|---|
| `m.fifo(clk, rst, in_valid=, in_data=, out_ready=, depth=)` | 单时钟严格 ready/valid FIFO | 空时 `out_data=0`；`valid&&ready` 握手 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L2370) · [pyc_fifo.v](../../runtime/verilog/pyc_fifo.v) |
| `m.async_fifo(in_clk, in_rst, out_clk, out_rst, ...)` | 双时钟 FIFO | **深度必须 2 的幂且 ≥2**；无跨域组合路径 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L2339) · [pyc_async_fifo.v](../../runtime/verilog/pyc_async_fifo.v) |
| `m.rv_queue(name, domain=cd, width=, depth=)` | ready/valid 队列对象封装 | 用法：`q.push(x, when=in_valid)` 返回是否接收；`p = q.pop(when=out_ready)` 返回 `Pop(valid, data, fire)` | [hw.py `rv_queue`](../../compiler/frontend/pycircuit/hw.py#L2405) · [`RvQueue`/`Pop`](../../compiler/frontend/pycircuit/hw.py#L2483) |
| `lib.FIFO(m, cd, in_valid, in_data, out_ready, depth=2)` | `m.fifo` 封装，返回 `in_ready/out_valid/out_data` | — | [lib/queue.py](../../compiler/frontend/pycircuit/lib/queue.py) |
| `lib.StreamSig(name=..., payload=...)` | 生成 ready/valid 流接口签名（生产者视角，`flip()` 得消费者） | — | [lib/stream.py](../../compiler/frontend/pycircuit/lib/stream.py) · [SPEC_STRUCTURES.md](../SPEC_STRUCTURES.md) |

## 8. 跨时钟域（CDC）

| 写法 | 说明 | 链接 |
|---|---|---|
| `m.cdc_sync(clk, rst, a, stages=...)` | 目的时钟域同步器；**跨域信号必须走它**，不能直接连 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L2363) · [pyc_cdc_sync.v](../../runtime/verilog/pyc_cdc_sync.v) |

## 9. 仲裁与处理器结构

| 写法 | 说明 | 注意 | 链接 |
|---|---|---|---|
| `lib.Picker(m, req, width=...)` | 固定优先级仲裁：**最低位优先**，返回 `valid/grant(one-hot)/index` | — | [lib/picker.py](../../compiler/frontend/pycircuit/lib/picker.py) |
| `lib.RegFile(m, cd, raddr_bus, wen_bus, waddr_bus, wdata_bus, ptag_count=, const_count=, nr=, nw=)` | 处理器式寄存器堆（打包总线） | ⚠️ 同拍多写口写同一 ptag = **未定义行为**；`[0,const_count)` 读出常量（地址值）；越界读返回 0 | [lib/regfile.py](../../compiler/frontend/pycircuit/lib/regfile.py) |
| `lib.Cache(m, cd, req_valid, req_addr, ..., ways=4, sets=64)` | 结构化 cache 基线 | ⚠️ 骨架级：`line_bytes/write_back/write_allocate/replacement/req_wmask` **未实现**，仅 `ways/sets/addr_width/data_width` 生效 | [lib/cache.py](../../compiler/frontend/pycircuit/lib/cache.py) |
| `logic.onehot_mux(sel, vals)` / `logic.priority_pick(bits, n=)` / `logic.match_any(...)` | onehot 选择、优先级选取、键匹配辅助 | — | [logic/__init__.py](../../compiler/frontend/pycircuit/logic/__init__.py) |

## 10. 层次化与模块组合

| 写法 | 说明 | 链接 |
|---|---|---|
| `@module` / `@function` | 模块/纯函数装饰器（`@module` 是层次边界，1:1 映射仿真对象） | [design.py](../../compiler/frontend/pycircuit/design.py#L108) |
| `m.instance(...)` | 实例化子模块 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L2219) |
| `domain.call(sub_fn, inputs={...}, prefix=...)` | V5 调子模块（自动 push/pop 周期隔离） | [v5.py](../../compiler/frontend/pycircuit/v5.py#L270) |
| `cas(domain, m.input(...), cycle=0)` | 给输入打周期标签 | [v5.py](../../compiler/frontend/pycircuit/v5.py#L1890) |
| `compile_cycle_aware(build, name=..., eager=True, hierarchical=..., **params)` | 主编译入口：Python → MLIR；`eager=False` 走 JIT 追踪，`hierarchical=True` 保留层次 | [v5.py](../../compiler/frontend/pycircuit/v5.py) · [PyCircuit_V5_Spec.md](../PyCircuit_V5_Spec.md) |
| `pycircuit.compile` / `JitError` | `@module` 路径的 JIT 追踪编译（把 Python `if`/`for` 降为静态硬件） | [jit.py](../../compiler/frontend/pycircuit/jit.py) |
| `hierarchical.HierarchicalModuleSpec` | 声明式层次组合（子模块 + 连接 + 参数）与 spec 推断 | [hierarchical.py](../../compiler/frontend/pycircuit/hierarchical.py) |
| 参考例子 | 单模块 `counter`，层次化 `hier_modules`，spec 管线 `pipeline_builder` | [designs/examples/](../../designs/examples/) |

## 11. 结构化接口（Bundle / Spec / 位域 / 枚举）

| 写法 | 说明 | 链接 |
|---|---|---|
| `m.bundle_connector(a=..., b=...)` / `Bundle` | 命名字段容器（类似 Verilog struct），`b["a"]` 取字段、`b.pack()` 打包 | [hw.py](../../compiler/frontend/pycircuit/hw.py#L1633) · [`Bundle.pack`](../../compiler/frontend/pycircuit/hw.py#L2454) |
| `spec.bundle/struct/signature(name)` → `.field(...).build()` | 流式 spec 构建器 | [spec/builders.py](../../compiler/frontend/pycircuit/spec/builders.py#L188) |
| `spec.stage_pipe(name)` / `spec.params()` / `spec.ruleset()` / `spec.module_family(...)` / `spec.valueclass` | 流水线 spec / 参数空间 / 译码规则 / 模块族 / 值类 | [spec/builders.py](../../compiler/frontend/pycircuit/spec/builders.py#L200) |
| spec 变换：`.remove_field()` `.rename_field()` `.select_fields()` `.flatten()` | spec 派生与字段选择 | [spec/types.py](../../compiler/frontend/pycircuit/spec/types.py) · 例 [pipeline_builder.py](../../designs/examples/pipeline_builder/pipeline_builder.py) |
| `spec.dse.named_variant(...)` / `spec.dse.product({...})` | 参数空间枚举（DSE），配合 build 的 `--param` 覆盖 | [spec/dse.py](../../compiler/frontend/pycircuit/spec/dse.py) |
| `StructSpec` / `BundleSpec` / `SignatureSpec` | 结构化接口规格（`spec` 包） | [spec/types.py](../../compiler/frontend/pycircuit/spec/types.py#L120) · [SPEC_STRUCTURES.md](../SPEC_STRUCTURES.md) |
| `BitfieldSpec` / `BitfieldView` | 位域切片视图 | [bitfield.py](../../compiler/frontend/pycircuit/bitfield.py#L169) |
| `PycEnum` / `enumeration(...)` / `EnumSignal` | 枚举类型信号 | [enums.py](../../compiler/frontend/pycircuit/enums.py#L69) |
| `Connector` / `WireConnector` / `RegConnector` | 连接器（`connectors.py`、`wiring` 包） | [connectors.py](../../compiler/frontend/pycircuit/connectors.py) · [wiring/connect.py](../../compiler/frontend/pycircuit/wiring/connect.py) |

## 12. 测试台（`@testbench` / `Tb`）

| 写法 | 说明 | 链接 |
|---|---|---|
| `t.clock("clk")` / `t.reset("rst", ...)` | 时钟、复位（拉起/放开拍数） | [tb.py](../../compiler/frontend/pycircuit/tb.py#L198) |
| `t.drive(port, value, at=cyc)` | 某拍驱动输入 | [tb.py](../../compiler/frontend/pycircuit/tb.py#L217) |
| `t.expect(port, value, at=cyc, phase="pre"\|"post")` | 某拍检查输出（pre=TICK-OBS，post=XFER-OBS） | [tb.py](../../compiler/frontend/pycircuit/tb.py#L228) |
| `t.random(port, seed=, start=, every=)` | 确定性伪随机激励 | [tb.py](../../compiler/frontend/pycircuit/tb.py#L284) |
| `t.sva_assert(expr, clock=, reset=)` + `sva.*` | SVA 跨周期断言（`sva.past/rose/fell/stable`） | [tb.py](../../compiler/frontend/pycircuit/tb.py#L262) · 例 [sva_rob.py](../../designs/XiangShan-pyc/sva/sva_rob.py) |
| `t.timeout(n)` / `t.finish(at=cyc)` | 超时兜底 / 正常结束 | [tb.py](../../compiler/frontend/pycircuit/tb.py#L250) |
| `CycleAwareTb(t)` + `tb.next()` | 隐式周期推进（推荐写法） | [v5.py](../../compiler/frontend/pycircuit/v5.py#L2198) |
| 完整 API 文档 | — | [TESTBENCH.md](../TESTBENCH.md) |

## 13. 观测与调试

| 写法 | 说明 | 链接 |
|---|---|---|
| `@probe(target=...)` | 独立探针定义，TB 中经 `TbProbes` 消费 | [design.py](../../compiler/frontend/pycircuit/design.py#L221) · [probe.py](../../compiler/frontend/pycircuit/probe.py) |
| `--trace-config trace.json` | trace DSL（实例 glob + tag + 窗口），C++/SV 双端 VCD | [trace_dsl.py](../../compiler/frontend/pycircuit/trace_dsl.py) · 例 [reset_invalidate_order_smoke_trace.json](../../designs/examples/reset_invalidate_order_smoke/reset_invalidate_order_smoke_trace.json) |
| `PYC_TRACE_DIR=... ./pyc_tb` | C++ 仿真开 VCD（仅 C++ 路径，`Vtb_*` 无效） | [命令参考](commands.md) |

## 14. 底层 `pyc_*` 原语对照表（只读，不手写）

发射器的目标库，C++ 模板与 Verilog 模块同名同端口，保证双后端等价。用户**不直接实例化**，但其语义决定上表各 `m.*` 调用。

| 原语 | Verilog | C++ |
|---|---|---|
| `pyc_reg` | [pyc_reg.v](../../runtime/verilog/pyc_reg.v) | [pyc_primitives.hpp](../../runtime/cpp/pyc_primitives.hpp) |
| `pyc_fifo` / `pyc_async_fifo` | [pyc_fifo.v](../../runtime/verilog/pyc_fifo.v) · [pyc_async_fifo.v](../../runtime/verilog/pyc_async_fifo.v) | [pyc_primitives.hpp](../../runtime/cpp/pyc_primitives.hpp) · [pyc_async_fifo.hpp](../../runtime/cpp/pyc_async_fifo.hpp) |
| `pyc_byte_mem` / `pyc_sync_mem` / `pyc_sync_mem_dp` | [pyc_byte_mem.v](../../runtime/verilog/pyc_byte_mem.v) · [pyc_sync_mem.v](../../runtime/verilog/pyc_sync_mem.v) · [pyc_sync_mem_dp.v](../../runtime/verilog/pyc_sync_mem_dp.v) | [pyc_byte_mem.hpp](../../runtime/cpp/pyc_byte_mem.hpp) · [pyc_sync_mem.hpp](../../runtime/cpp/pyc_sync_mem.hpp) |
| `pyc_cdc_sync` | [pyc_cdc_sync.v](../../runtime/verilog/pyc_cdc_sync.v) | [pyc_cdc_sync.hpp](../../runtime/cpp/pyc_cdc_sync.hpp) |
| `pyc_add/mux/and/or/xor/not`（组合，发射器通常内联为表达式） | [runtime/verilog/](../../runtime/verilog/) | [pyc_primitives.hpp](../../runtime/cpp/pyc_primitives.hpp) |

契约全文：[PRIMITIVES.md](../PRIMITIVES.md)。

## 15. 注意事项速查（审查代码时重点核对）

| # | 规则 | 出处 |
|---|---|---|
| 1 | `sync_mem` 读延迟 1 拍、同地址读写返回旧值；`byte_mem` 才是组合读 | [PRIMITIVES.md §4](../PRIMITIVES.md) |
| 2 | 所有 `*_mem` 复位不清内容；仿真默认初始化为 0 | [PRIMITIVES.md §4](../PRIMITIVES.md) |
| 3 | `RegFile` 同拍写同一 ptag = 未定义行为，框架不检查 | [lib/regfile.py](../../compiler/frontend/pycircuit/lib/regfile.py) |
| 4 | `Cache` 是骨架，写/替换策略参数不生效 | [lib/cache.py](../../compiler/frontend/pycircuit/lib/cache.py) |
| 5 | `async_fifo` 深度必须 2 的幂 ≥2；跨域信号必须过 `cdc_sync` | [PRIMITIVES.md §3/§5](../PRIMITIVES.md) |
| 6 | 寄存器语义：`rst` 优先于 `en`（同步复位） | [pyc_reg.v](../../runtime/verilog/pyc_reg.v) |
| 7 | V5 中 `wire_of()` 只允许出现在 `m.output()` 边界；`domain.state()` 已移除，用 `domain.signal()` | [PyCircuit_V5_Spec.md](../PyCircuit_V5_Spec.md) |
| 8 | 语义问题只在 MLIR 方言/verifier 层修，不做后端单点修补 | [AGENTS.md](../../AGENTS.md) |
