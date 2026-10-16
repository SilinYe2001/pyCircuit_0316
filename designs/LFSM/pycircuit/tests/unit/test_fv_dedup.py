"""Scratch TB: A-001 first-visit dedup equivalence (F-020/F-025; sharpens T-029/T-030/T-031).

A-001 replaces the spec's ``generated_data_keys[lane]`` set (a CAM) with
walker counter first-visit conditions.  This scratch TB proves the swap is
functionally transparent with the smallest possible DUT and an independent
golden reference inside the TB:

- DUT (minimal chain): ``walker`` counters → ``tok_fv_a/b/c`` → ``rdgen``
  enqueue gating — exactly the A-001 signal path, no queues/assemblers.
- Reference (the CAM being replaced): a per-(inst,lane) **set-based** dedup
  model with golden ``_needed_rds``/``_c_needed`` semantics (evaluate per
  token, register on commit; UU: every token commits).  Keys:
  A/AMX ``(inst,m,k)``, B/BMX ``(inst,k,n)``, C ``(inst,m,n)``.
- Per-cycle compare of BOTH the walker ``fv_*`` flags and the rdgen enqueue
  stream (valid + inst + rdgen_id + rd_id + m/n/k identity) against the set
  model — a mismatch stops at the exact (case, token, cycle, lane).
- Coverage (A-001 §7): m16/m32 x single/multi n_outer block x K-outer
  revisits (N tails 9->[4,5] / 10->[4,6] / 17->[8,4,5], K tails), MX span
  {1,2,4}, single-token instruction, and full b2b chaining (every case
  starts in the previous case's drain cycle: per-inst set reset + rd_id
  clear).

Run standalone:  python3 tests/unit/test_fv_dedup.py
Run via pytest:  pytest designs/LFSM/pycircuit/tests/unit/test_fv_dedup.py
"""
from __future__ import annotations

import sys
from pathlib import Path

_PYC = Path(__file__).resolve().parents[2]
if str(_PYC) not in sys.path:
    sys.path.insert(0, str(_PYC))
_TESTS = _PYC / "tests"
if str(_TESTS) not in sys.path:
    sys.path.insert(0, str(_TESTS))

import lfsm_tb_common  # noqa: E402,F401  (sys.path bootstrap)
from pycircuit import CycleAwareTb, Tb, compile_cycle_aware, testbench  # noqa: E402

from lfsm.rdgen import rdgen  # noqa: E402
from lfsm.types import emit_outs  # noqa: E402
from lfsm.walker import walker  # noqa: E402
from lfsm_tb_common import golden_walk_tokens  # noqa: E402

# (m_mode, m_slice, n_hw, k_groups, mx_span) — mx_span 0 = non-MX (B8/B4-class).
CASES = [
    (16, 1, 1, 1, 0),      # single-token instruction: first==last, enq & done same cycle
    (16, 1, 8, 8, 0),      # single n_outer, single K outer (baseline)
    (16, 1, 8, 24, 0),     # single n_outer, 3 K outers (K-outer revisit)
    (16, 1, 9, 12, 0),     # N tail [4,5], K tail [8,4]
    (16, 1, 17, 10, 0),    # N [8,4,5], K tail [8,2]
    (32, 2, 8, 16, 0),     # m32 dual-slice: every (k,n) revisited at m_idx=1
    (32, 2, 9, 9, 0),      # m32 return-base regression: N tail [4,5], K tail [4,4,1]
    (32, 1, 10, 10, 0),    # m32 partial m_slice=1: B/BMX new every token
    (16, 1, 9, 12, 1),     # MXFP8 span=1: AMX/BMX lanes on, N tail, K tail
    (32, 2, 17, 9, 2),     # MXFP4 span=2, m32, N [8,4,5], K tail
    (16, 1, 10, 12, 4),    # HIF4 span=4, N tail [4,6], K tail
]


def build(m, domain):
    # inputs={} (not None): all pins are auto-created as top-level lfsm_wlk_*
    # / lfsm_rdg_* ports in both flat and hierarchical (CLI) modes, and the
    # submodules do NOT self-emit their outs — the root emits them below so
    # they are TB-visible top-level ports in both modes.
    wlk = domain.call(walker, inputs={}, prefix="lfsm_wlk")
    # rdgen composed on the walker token stream; "start" + cfg_* keys are
    # intentionally omitted so they become standalone lfsm_rdg_* pins.
    rdg = domain.call(rdgen, inputs={
        "tok_valid": wlk["tok_valid"],
        "tok_advance": wlk["tok_advance"],
        "tok_m": wlk["tok_m"], "tok_n": wlk["tok_n"], "tok_k": wlk["tok_k"],
        "tok_seq": wlk["tok_seq"], "tok_done": wlk["tok_done"],
        "tok_nblk_base": wlk["tok_nblk_base"], "tok_nblk_len": wlk["tok_nblk_len"],
        "tok_fv_a": wlk["tok_fv_a"], "tok_fv_b": wlk["tok_fv_b"],
        "tok_fv_c": wlk["tok_fv_c"],
    }, prefix="lfsm_rdg")
    emit_outs(m, wlk, prefix="lfsm_wlk")
    emit_outs(m, rdg, prefix="lfsm_rdg")
    return rdg


build.__pycircuit_name__ = "tb_fv_dedup_top"


def set_dedup_model(toks, mx_en, inst_id):
    """The CAM A-001 replaces: golden set-based dedup (SRC-01 sec 7.2).

    One key set per (inst, lane); a need is emitted when the token's key is
    not yet in the set; the key is registered on commit (UU: every token
    advances, so evaluate+commit collapse to per-token).  Returns one
    expectation dict per token.
    """
    seen = {l: set() for l in ("A", "AMX", "B", "BMX", "C")}
    rid = {l: 0 for l in ("A", "AMX", "B", "BMX")}
    out = []
    for t in toks:
        mm, nn, kk = t["m_idx"], t["n_idx"], t["k_idx"]
        e = {"m": mm, "n": nn, "k": kk, "seq": t["walk_seq"]}
        key_a = (inst_id, mm, kk)
        key_b = (inst_id, kk, nn)
        key_c = (inst_id, mm, nn)
        for lane, key, on in (("a", key_a, True), ("amx", key_a, mx_en),
                              ("b", key_b, True), ("bmx", key_b, mx_en)):
            L = lane.upper()
            new = bool(on) and key not in seen[L]
            seen[L].add(key)
            e[lane] = new
            if new:
                e[f"{lane}_rid"] = rid[L]
                rid[L] += 1
        e["c"] = key_c not in seen["C"]
        seen["C"].add(key_c)
        out.append(e)
    return out


def _drive_cfg(tb, m_mode, m_slice, n_hw, k_groups, mx_span, inst_id):
    k_step = 4 if m_mode == 32 else 8
    span = mx_span if mx_span else 1   # rdgen muls by span; unused when mx_en=0
    tb.drive("lfsm_wlk_cfg_inst_id", inst_id)
    tb.drive("lfsm_wlk_cfg_m_mode", 1 if m_mode == 32 else 0)
    tb.drive("lfsm_wlk_cfg_m_slice", m_slice)
    tb.drive("lfsm_wlk_cfg_n_hw", n_hw)
    tb.drive("lfsm_wlk_cfg_k_groups", k_groups)
    tb.drive("lfsm_wlk_cfg_k_step", k_step)
    tb.drive("lfsm_rdg_cfg_inst_id", inst_id)
    tb.drive("lfsm_rdg_cfg_mx_en", 1 if mx_span else 0)
    tb.drive("lfsm_rdg_cfg_span", mx_span)
    tb.drive("lfsm_rdg_cfg_rg_len", ((k_groups * span + 3) // 4) * 32)
    tb.drive("lfsm_rdg_cfg_n_hw", n_hw)
    tb.drive("lfsm_rdg_cfg_n_hw2", n_hw + (n_hw & 1))
    tb.drive("lfsm_rdg_cfg_k_groups", k_groups)
    tb.drive("lfsm_rdg_cfg_a_base", 0x0000_0000)
    tb.drive("lfsm_rdg_cfg_a_mx_base", 0x2000_0000)
    tb.drive("lfsm_rdg_cfg_b_base", 0x1000_0000)
    tb.drive("lfsm_rdg_cfg_b_mx_base", 0x3000_0000)
    tb.drive("lfsm_rdg_cfg_l0c_base", 0x4000_0000)


def _expect_token(tb, e, done, mx_en, inst_id, tag):
    # (1) walker fv_* flags vs the SET model — the A-001 core claim:
    #     counter first-visit condition ⟺ set-based "key not seen".
    tb.expect("lfsm_wlk_tok_valid", 1, phase="pre", msg=f"valid {tag}")
    tb.expect("lfsm_wlk_tok_fv_a", int(e["a"]), phase="pre", msg=f"fv_a {tag}")
    tb.expect("lfsm_wlk_tok_fv_b", int(e["b"]), phase="pre", msg=f"fv_b {tag}")
    tb.expect("lfsm_wlk_tok_fv_c", int(e["c"]), phase="pre", msg=f"fv_c {tag}")
    # (2) rdgen enqueue stream vs the SET model (dedup decision + identity).
    for lane in ("a", "amx", "b", "bmx"):
        p = f"lfsm_rdg_enq_{lane}"
        tb.expect(f"{p}_valid", int(e[lane]), phase="pre", msg=f"{lane} valid {tag}")
        if not e[lane]:
            continue
        tb.expect(f"{p}_inst", inst_id, phase="pre", msg=f"{lane} inst {tag}")
        tb.expect(f"{p}_rdgen", e["seq"] + 1, phase="pre", msg=f"{lane} rdgen {tag}")
        tb.expect(f"{p}_rd_id", e[f"{lane}_rid"], phase="pre", msg=f"{lane} rid {tag}")
        if lane == "amx":
            tb.expect(f"{p}_m", e["m"], phase="pre", msg=f"amx m {tag}")
            tb.expect(f"{p}_k", e["k"], phase="pre", msg=f"amx k {tag}")
        elif lane == "b":
            tb.expect(f"{p}_n", e["n"], phase="pre", msg=f"b n {tag}")
            tb.expect(f"{p}_k", e["k"], phase="pre", msg=f"b k {tag}")
        elif lane == "bmx":
            tb.expect(f"{p}_k", e["k"], phase="pre", msg=f"bmx k {tag}")
    # (3) C path entry vs the SET model.
    tb.expect("lfsm_rdg_c_enq_valid", int(e["c"]), phase="pre", msg=f"c valid {tag}")
    if e["c"]:
        tb.expect("lfsm_rdg_c_enq_inst", inst_id, phase="pre", msg=f"c inst {tag}")
        tb.expect("lfsm_rdg_c_enq_rdgen", e["seq"] + 1, phase="pre", msg=f"c rdgen {tag}")
        tb.expect("lfsm_rdg_c_enq_m", e["m"], phase="pre", msg=f"c m {tag}")
        tb.expect("lfsm_rdg_c_enq_n", e["n"], phase="pre", msg=f"c n {tag}")
    # (4) LaneLoadEnd strobes at the DONE token (F-024 boundary preserved).
    tb.expect("lfsm_rdg_end_a", done, phase="pre", msg=f"end_a {tag}")
    tb.expect("lfsm_rdg_end_b", done, phase="pre", msg=f"end_b {tag}")
    tb.expect("lfsm_rdg_end_amx", done & mx_en, phase="pre", msg=f"end_amx {tag}")
    tb.expect("lfsm_rdg_end_bmx", done & mx_en, phase="pre", msg=f"end_bmx {tag}")


@testbench
def tb(t: Tb) -> None:
    tb = CycleAwareTb(t)
    tb.clock("clk")
    tb.reset("rst", cycles_asserted=2, cycles_deasserted=1)
    per_case = [golden_walk_tokens(mm, ms, nh, kg, inst_id=i)
                for i, (mm, ms, nh, kg, _sp) in enumerate(CASES)]
    tb.timeout(sum(len(x) for x in per_case) + 4 * len(CASES) + 16)

    tb.drive("lfsm_wlk_stall", 0)   # A-009: UU baseline ties stall 0
    tb.drive("lfsm_wlk_start", 0)
    tb.drive("lfsm_rdg_start", 0)

    for i, (m_mode, m_slice, n_hw, k_groups, mx_span) in enumerate(CASES):
        inst_id = i
        mx_en = 1 if mx_span else 0
        toks = per_case[i]
        exp = set_dedup_model(toks, mx_en, inst_id)

        # b2b: this start cycle coincides with the previous case's drain
        # cycle — per-inst set reset + rd_id clear are exercised every case.
        _drive_cfg(tb, m_mode, m_slice, n_hw, k_groups, mx_span, inst_id)
        tb.drive("lfsm_wlk_start", 1)
        tb.drive("lfsm_rdg_start", 1)
        tb.next()
        tb.drive("lfsm_wlk_start", 0)
        tb.drive("lfsm_rdg_start", 0)

        for j, e in enumerate(exp):
            tag = f"i{inst_id} tok{j}(m{e['m']},n{e['n']},k{e['k']}) c{tb.cycle}"
            _expect_token(tb, e, int(j == len(exp) - 1), mx_en, inst_id, tag)
            tb.next()

        # drain: walker idle, no residual enqueues (next case starts here).
        cyc = tb.cycle
        tb.expect("lfsm_wlk_tok_valid", 0, phase="pre", msg=f"drain valid i{inst_id} c{cyc}")
        for lane in ("a", "amx", "b", "bmx"):
            tb.expect(f"lfsm_rdg_enq_{lane}_valid", 0, phase="pre",
                      msg=f"drain {lane} i{inst_id} c{cyc}")
        tb.expect("lfsm_rdg_c_enq_valid", 0, phase="pre", msg=f"drain c i{inst_id} c{cyc}")

    tb.finish()


# ── pytest / standalone entry ───────────────────────────────────────────────
def test_fv_dedup_mlir_clean():
    """Structural: compiles, no balancing registers inserted."""
    mlir = compile_cycle_aware(build, name="tb_fv_dedup_top", eager=True).emit_mlir()
    assert "func.func" in mlir
    assert "_v5_bal" not in mlir


def test_fv_dedup_tb():
    from lfsm_tb_common import build_and_run
    build_and_run(Path(__file__).resolve())


if __name__ == "__main__":
    from lfsm_tb_common import build_and_run
    print(build_and_run(Path(__file__).resolve()))
