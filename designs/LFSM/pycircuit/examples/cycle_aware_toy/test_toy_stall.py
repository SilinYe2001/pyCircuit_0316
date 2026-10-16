"""Unit TB: toy_pipe_stall（.assign(when=) 条件保持）— V6 cycle-aware 教程配套。

逐拍验证教程文档中的论断：
stall=1 期间全部状态经 assign(when=) 条件保持 —— y 冻结、dbg_prod 不变，
无需任何独立反压状态机；stall 释放后流水线从冻结点继续。

时间线（beat0 = (3,4,5)，beat1 = (9,9,9)）：
    c0 灌 beat0；c1 stall 拉起并灌 beat1；c2-c3 保持 stall；
    c3 末释放；c4 beat0 结果出管（35）；c5 beat1 结果出管（162）。

Run standalone:  python3 designs/LFSM/pycircuit/examples/cycle_aware_toy/test_toy_stall.py
Run via pytest:  pytest designs/LFSM/pycircuit/examples/cycle_aware_toy/test_toy_stall.py
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
from pycircuit import CycleAwareTb, Tb, testbench  # noqa: E402

from toy_pipeline import toy_pipe_stall  # noqa: E402


def build(m, domain):
    return toy_pipe_stall(m, domain)


build.__pycircuit_name__ = "tb_toy_stall_top"


@testbench
def tb(t: Tb) -> None:
    tb = CycleAwareTb(t)
    tb.clock("clk")
    tb.reset("rst", cycles_asserted=2, cycles_deasserted=1)
    tb.timeout(32)

    # ── cycle 0：灌 beat0 (3,4,5)，stall=0 正常运行 ──────────────
    tb.drive("toys_a", 3)
    tb.drive("toys_b", 4)
    tb.drive("toys_c", 5)
    tb.drive("toys_stall", 0)

    tb.next()  # → cycle 1：s1<=7 已提交；拉起 stall，灌 beat1 (9,9,9)
    tb.drive("toys_a", 9)
    tb.drive("toys_b", 9)
    tb.drive("toys_c", 9)
    tb.drive("toys_stall", 1)
    tb.expect("toys_dbg_s1", 7, phase="pre", msg="c1 s1(beat0)")
    tb.expect("toys_dbg_prod", 35, phase="pre", msg="c1 prod=7*5")

    tb.next()  # → cycle 2：stall 生效 —— 全部状态保持
    tb.expect("toys_y", 0, phase="pre", msg="c2 y 冻结（复位值）")
    tb.expect("toys_dbg_s1", 7, phase="pre", msg="c2 s1 保持")
    tb.expect("toys_dbg_prod", 35, phase="pre", msg="c2 prod 保持（状态不变⟹组合不变）")

    tb.next()  # → cycle 3：继续 stall 一拍，仍在冻结
    tb.expect("toys_y", 0, phase="pre", msg="c3 y 仍冻结")
    tb.expect("toys_dbg_s1", 7, phase="pre", msg="c3 s1 仍保持")
    tb.drive("toys_stall", 0)  # c3 末释放 stall

    tb.next()  # → cycle 4：释放后 s2<=35 提交，beat0 结果出管
    tb.expect("toys_y", 35, phase="pre", msg="c4 y(beat0) 解冻输出")
    tb.expect("toys_dbg_s1", 18, phase="pre", msg="c4 s1(beat1)=9+9")
    tb.expect("toys_dbg_prod", 162, phase="pre", msg="c4 prod=18*9")

    tb.next()  # → cycle 5：beat1 结果出管
    tb.expect("toys_y", 162, phase="pre", msg="c5 y(beat1)")

    tb.finish()


# ── pytest / standalone entry ───────────────────────────────────────────────
def test_toy_stall_tb():
    from lfsm_tb_common import build_and_run
    build_and_run(Path(__file__).resolve())


if __name__ == "__main__":
    from lfsm_tb_common import build_and_run
    print(build_and_run(Path(__file__).resolve()))
