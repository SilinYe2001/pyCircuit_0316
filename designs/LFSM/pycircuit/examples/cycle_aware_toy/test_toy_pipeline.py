"""Unit TB: toy_pipe（基准两级流水）— V6 cycle-aware 教程配套。

逐拍验证教程文档中的三条核心论断：
1. 同拍 = 纯组合：drive 当拍即可见 dbg_sum（加法器零延迟穿透）。
2. 跨拍 = 寄存提交：s1/c_d 的值次拍才出现在 Q 端；y 延迟 2 拍（s1 → s2 两级）。
3. II=1 连发流水：连续两拍灌入两拍数据，y 连续两拍吐出对应结果。
外加一次 phase="post" 观测，演示「cycle N post == cycle N+1 pre」的相位关系。

Run standalone:  python3 designs/LFSM/pycircuit/examples/cycle_aware_toy/test_toy_pipeline.py
Run via pytest:  pytest designs/LFSM/pycircuit/examples/cycle_aware_toy/test_toy_pipeline.py
"""
from __future__ import annotations

import sys
from pathlib import Path

_DIR = Path(__file__).resolve().parent
_PYC = _DIR.parents[1]                       # designs/LFSM/pycircuit
_TESTS = _PYC / "tests"
for _p in (str(_DIR), str(_PYC), str(_TESTS)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import lfsm_tb_common  # noqa: E402,F401  (sys.path bootstrap)
from pycircuit import CycleAwareTb, Tb, compile_cycle_aware, testbench  # noqa: E402

from toy_pipeline import toy_pipe, toy_pipe_bal, toy_pipe_stall  # noqa: E402


def build(m, domain):
    return toy_pipe(m, domain)


build.__pycircuit_name__ = "tb_toy_pipe_top"


@testbench
def tb(t: Tb) -> None:
    tb = CycleAwareTb(t)
    tb.clock("clk")
    tb.reset("rst", cycles_asserted=2, cycles_deasserted=1)
    tb.timeout(32)

    # ── cycle 0：灌入第一拍数据 (a,b,c) = (3,4,5) ─────────────────
    tb.drive("toy_a", 3)
    tb.drive("toy_b", 4)
    tb.drive("toy_c", 5)
    # 论断1 同拍=纯组合：3+4 当拍可见（pre = 沿前观测组合值）
    tb.expect("toy_dbg_sum", 7, phase="pre", msg="c0 同拍组合 sum")

    tb.next()  # → cycle 1：s1/c_d 在沿上提交；同时灌入第二拍 (10,20,2)
    tb.drive("toy_a", 10)
    tb.drive("toy_b", 20)
    tb.drive("toy_c", 2)
    # 论断2 跨拍=寄存：上拍数据次拍出现在寄存器 Q 端
    tb.expect("toy_dbg_s1", 7, phase="pre", msg="c1 s1 Q端")
    tb.expect("toy_dbg_c_d", 5, phase="pre", msg="c1 c_d Q端")
    # 论断1 组合穿透寄存器 Q 端：stage-2 乘法当拍算出 7*5
    tb.expect("toy_dbg_prod", 35, phase="pre", msg="c1 同拍组合 prod")
    tb.expect("toy_dbg_sum", 30, phase="pre", msg="c1 同拍组合 sum(beat1)")
    # 相位演示：cycle 1 post（提交后）== cycle 2 pre（沿前）
    tb.expect("toy_y", 35, phase="post", msg="c1 post == c2 pre")

    tb.next()  # → cycle 2：第一拍结果出管；第二拍进入 stage-2
    # 论断2 延迟=2 拍（寄存器链深度 2：s1 → s2）
    tb.expect("toy_y", 35, phase="pre", msg="c2 y(beat0)")
    tb.expect("toy_dbg_s1", 30, phase="pre", msg="c2 s1(beat1)")
    tb.expect("toy_dbg_prod", 60, phase="pre", msg="c2 prod(beat1)")

    tb.next()  # → cycle 3：II=1，第二拍结果紧随其后
    # 论断3 连发：稳态每拍出一个结果
    tb.expect("toy_y", 60, phase="pre", msg="c3 y(beat1)")

    tb.finish()


# ── pytest / standalone entry ───────────────────────────────────────────────
def _mlir(fn, name):
    return compile_cycle_aware(fn, name=name, eager=True).emit_mlir()


def test_toy_pipe_mlir_clean():
    """结构断言：基准变体恰好 3 个 pyc.reg，零自动平衡寄存器。"""
    import re

    mlir = _mlir(toy_pipe, "toy_pipe")
    assert len(re.findall(r"\bpyc\.reg\b", mlir)) == 3
    assert "_v5_bal" not in mlir


def test_toy_pipe_stall_mlir_clean():
    """结构断言：stall 变体同样 3 个 pyc.reg、零 _v5_bal；
    assign(when=)  lowering 为 pyc.mux 反馈（保持=组合逻辑显式写出）。"""
    import re

    mlir = _mlir(toy_pipe_stall, "toy_pipe_stall")
    assert len(re.findall(r"\bpyc\.reg\b", mlir)) == 3
    assert "_v5_bal" not in mlir
    assert "pyc.mux" in mlir


def test_toy_pipe_bal_inserts_balancing_reg():
    """结构断言：bal 变体 2 个 pyc.reg —— 1 个显式 sum_d + 1 个自动 _v5_bal。"""
    import re

    mlir = _mlir(toy_pipe_bal, "toy_pipe_bal")
    assert len(re.findall(r"\bpyc\.reg\b", mlir)) == 2
    assert len(set(re.findall(r"_v5_bal_\d+", mlir))) == 1


def test_toy_pipe_tb():
    from lfsm_tb_common import build_and_run
    build_and_run(Path(__file__).resolve())


if __name__ == "__main__":
    from lfsm_tb_common import build_and_run
    print(build_and_run(Path(__file__).resolve()))
