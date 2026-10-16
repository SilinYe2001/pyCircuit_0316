"""V6 cycle-aware 教程玩具电路 — y = (a + b) * c 两级数据流水线。

配套教程：designs/LFSM/pycircuit/report/V6_CycleAware入门_玩具流水线与LFSM对照.md

四个变体（每个隔离演示一个 cycle-aware 特性）：

1. ``toy_pipe``       基准两级流水 —— LFSM 四段式骨架的微缩版：
                      cycle 0 纯组合求值 → 恰好一次 ``domain.next()`` →
                      cycle 1 统一 ``<<=`` 提交。代码中没有一行"寄存器"字样，
                      3 个 DFF 全部由"读 cycle 0 / 写 cycle 1"推导出来。
2. ``toy_pipe_bal``   自动周期平衡 —— 把 cycle-1 信号与 cycle-0 信号组合，
                      编译器自动给较早的信号补 ``_v5_bal`` DFF（max 规则）。
3. ``toy_pipe_stall`` ``.assign(when=)`` 条件保持 —— stall=1 时全部状态
                      保持（寄存器使能），无任何独立反压 FSM。
4. ``toy_pipe_bad``   反例：在 cycle 0 写入一个 cycle-1 的值（规范判为
                      "向过去赋值"错误）。实际运行显示 eager 前端**不静态
                      报错**，而是静默把 v_d 的 Q 端接进 x 的 D —— 生成两级
                      级联 DFF（语义 = 两拍延迟链，未必是设计意图）。这正是
                      需要 authoring 纪律 + 结构断言防线的原因（见教程文档）。

运行（打印四份编译结果与 pyc.reg / _v5_bal 统计）：

    python3 designs/LFSM/pycircuit/examples/cycle_aware_toy/toy_pipeline.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# ── sys.path 引导：定位仓库的 compiler/frontend（pycircuit 包）─────────────
_d = Path(__file__).resolve()
_repo = next(p for p in _d.parents if (p / "compiler" / "frontend" / "pycircuit").is_dir())
if str(_repo / "compiler" / "frontend") not in sys.path:
    sys.path.insert(0, str(_repo / "compiler" / "frontend"))

from pycircuit import (  # noqa: E402
    CycleAwareCircuit,
    CycleAwareDomain,
    cas,
    compile_cycle_aware,
    mux,
    u,
    wire_of,
)


def _emit_outs(m, outs, *, prefix):
    """独立模式：把 outs 字典每个键发射为输出端口（LFSM emit_outs 同款）。"""
    for k, v in outs.items():
        m.output(f"{prefix}_{k}", wire_of(v))


# ─────────────────────────────────────────────────────────────────────────────
# 变体 1：基准两级流水线（四段式骨架）
# ─────────────────────────────────────────────────────────────────────────────
def toy_pipe(
    m: CycleAwareCircuit,
    domain: CycleAwareDomain,
    *,
    inputs=None,
    prefix: str = "toy",
) -> dict:
    # ── Cycle 0: state ─────────────────────────────────────────────
    # domain.signal() 声明即读：Q 端在 cycle 0 立刻可参与组合表达式。
    # 此刻还没有任何寄存器——寄存器由后面的读写周期差推导。
    s1 = domain.signal(width=9, reset_value=0, name=f"{prefix}_s1")
    s2 = domain.signal(width=16, reset_value=0, name=f"{prefix}_s2")
    c_d = domain.signal(width=8, reset_value=0, name=f"{prefix}_c_d")

    # ── Cycle 0: inputs ────────────────────────────────────────────
    # m.input() 返回裸 Wire，必须 cas() 包装并显式标注周期才能参与 CAS 运算。
    a = cas(domain, m.input(f"{prefix}_a", width=8), cycle=0)
    b = cas(domain, m.input(f"{prefix}_b", width=8), cycle=0)
    c = cas(domain, m.input(f"{prefix}_c", width=8), cycle=0)

    # ── Cycle 0: combinational ─────────────────────────────────────
    # 同一 cycle 内的信号链 = 零延迟纯组合（同拍穿透）。
    sum_ab = a.zext(9) + b.zext(9)        # stage-1：本拍新值（@cycle 0）
    prod = s1.zext(16) * c_d.zext(16)     # stage-2：读 s1/c_d 的 Q 端（上拍提交值）
    outs = dict(y=s2, dbg_sum=sum_ab, dbg_s1=s1, dbg_c_d=c_d, dbg_prod=prod)

    # ── 唯一的时序分界 ──────────────────────────────────────────────
    domain.next()

    # ── Cycle 1: commits ───────────────────────────────────────────
    # 读 cycle 0 / 写 cycle 1 ⟹ 每个 signal 推导出一级反馈寄存器（DFF）。
    s1 <<= sum_ab
    c_d <<= c
    s2 <<= prod

    if inputs is None:
        _emit_outs(m, outs, prefix=prefix)
    return outs


# ─────────────────────────────────────────────────────────────────────────────
# 变体 2：自动周期平衡（混周期组合 → _v5_bal DFF）
# ─────────────────────────────────────────────────────────────────────────────
def toy_pipe_bal(
    m: CycleAwareCircuit,
    domain: CycleAwareDomain,
    *,
    inputs=None,
    prefix: str = "toybal",
) -> dict:
    a = cas(domain, m.input(f"{prefix}_a", width=8), cycle=0)
    b = cas(domain, m.input(f"{prefix}_b", width=8), cycle=0)
    c = cas(domain, m.input(f"{prefix}_c", width=8), cycle=0)

    sum_ab = a.zext(9) + b.zext(9)                       # @cycle 0
    # domain.cycle() = 显式单级 DFF；返回裸 Wire，用 cas(cycle=1) 重新标注。
    sum_d = cas(domain, domain.cycle(sum_ab, name=f"{prefix}_sum_d"), cycle=1)
    # max(cycle)=1 规则：c(@0) 自动补 1 级 _v5_bal DFF 对齐到 cycle 1。
    y = sum_d.zext(16) * c.zext(16)
    outs = dict(y=y, dbg_sum_d=sum_d)

    if inputs is None:
        _emit_outs(m, outs, prefix=prefix)
    return outs


# ─────────────────────────────────────────────────────────────────────────────
# 变体 3：.assign(when=) 条件保持（stall 反压，无状态机）
# ─────────────────────────────────────────────────────────────────────────────
def toy_pipe_stall(
    m: CycleAwareCircuit,
    domain: CycleAwareDomain,
    *,
    inputs=None,
    prefix: str = "toys",
) -> dict:
    # ── Cycle 0: state ─────────────────────────────────────────────
    s1 = domain.signal(width=9, reset_value=0, name=f"{prefix}_s1")
    s2 = domain.signal(width=16, reset_value=0, name=f"{prefix}_s2")
    c_d = domain.signal(width=8, reset_value=0, name=f"{prefix}_c_d")

    # ── Cycle 0: inputs ────────────────────────────────────────────
    a = cas(domain, m.input(f"{prefix}_a", width=8), cycle=0)
    b = cas(domain, m.input(f"{prefix}_b", width=8), cycle=0)
    c = cas(domain, m.input(f"{prefix}_c", width=8), cycle=0)
    stall = cas(domain, m.input(f"{prefix}_stall", width=1), cycle=0)

    # ── Cycle 0: combinational ─────────────────────────────────────
    sum_ab = a.zext(9) + b.zext(9)
    prod = s1.zext(16) * c_d.zext(16)
    run = ~stall
    outs = dict(y=s2, dbg_s1=s1, dbg_prod=prod)

    domain.next()

    # ── Cycle 1: commits ───────────────────────────────────────────
    # assign(when=) = 寄存器使能：when 不成立的拍末不更新，值保持。
    s1.assign(sum_ab, when=run)
    c_d.assign(c, when=run)
    s2.assign(prod, when=run)

    if inputs is None:
        _emit_outs(m, outs, prefix=prefix)
    return outs


# ─────────────────────────────────────────────────────────────────────────────
# 变体 4（反例）：向过去赋值 —— 在 cycle 0 写入一个 cycle-1 的值。
# 规范 §4 推导规则表把"写周期 < 读周期"判为编译错误；当前 eager 前端的
# 真实行为是**不报错**：<<= 只连接 D 端，cycle 标签不参与写侧检查，
# 结果是 v_d（一级 DFF）的 Q 再串一级 x（第二级 DFF）—— 静默的语义漂移。
# ─────────────────────────────────────────────────────────────────────────────
def toy_pipe_bad(
    m: CycleAwareCircuit,
    domain: CycleAwareDomain,
    *,
    inputs=None,
    prefix: str = "toybad",
) -> dict:
    x = domain.signal(width=8, reset_value=0, name=f"{prefix}_x")
    v = cas(domain, m.input(f"{prefix}_v", width=8), cycle=0)
    # v_d 是 cycle-1 信号（显式 DFF 之后）。
    v_d = cas(domain, domain.cycle(v, name=f"{prefix}_v_d"), cycle=1)
    # 当前 cycle_index = 0：把"未来"的值写进寄存器 —— 规范判定为编译错误，
    # 但 eager 前端静默接受（生成 v_d → x 两级级联 DFF）。
    x <<= v_d
    outs = dict(y=x)
    if inputs is None:
        _emit_outs(m, outs, prefix=prefix)
    return outs


toy_pipe.__pycircuit_name__ = "toy_pipe"
toy_pipe_bal.__pycircuit_name__ = "toy_pipe_bal"
toy_pipe_stall.__pycircuit_name__ = "toy_pipe_stall"
toy_pipe_bad.__pycircuit_name__ = "toy_pipe_bad"


if __name__ == "__main__":
    import re

    for fn, name in (
        (toy_pipe, "toy_pipe"),
        (toy_pipe_bal, "toy_pipe_bal"),
        (toy_pipe_stall, "toy_pipe_stall"),
    ):
        mlir = compile_cycle_aware(fn, name=name, eager=True).emit_mlir()
        n_reg = len(re.findall(r"\bpyc\.reg\b", mlir))
        bal = sorted(set(re.findall(r"_v5_bal_\d+", mlir)))
        print(f"===== {name}: pyc.reg={n_reg}, _v5_bal regs={len(bal)} {bal} =====")
        print(mlir)

    print("===== toy_pipe_bad（向过去赋值 —— 规范判错，eager 前端静默接受）=====")
    try:
        mlir = compile_cycle_aware(toy_pipe_bad, name="toy_pipe_bad", eager=True).emit_mlir()
        print("[实际行为] 前端未静态报错：v_d 的 Q 串进 x 的 D，生成两级级联 DFF：")
        print(mlir)
    except Exception as e:  # noqa: BLE001 - 教程反例：展示真实报错
        print(f"{type(e).__name__}: {e}")
