"""LFSM walker — independent MKN walk FSM (CYCLE §2, SEQ §5).

Deviation note (logged in IMPLEMENTATION_LOG): ``n_len`` / ``k_count`` are
computed **combinationally** from the ``n_base`` / ``k_base`` registers
(``rule(n_hw - n_base)`` / ``min(k_step, k_groups - k_base)``) instead of
being loaded as registers at transitions.  This is exactly the golden
``current_n_len`` / ``current_k_count`` property semantics (recomputed
every cycle from the outer counters) and fixes the Step-6 pseudocode's
off-by-one-block load at N_OUTER/K_OUTER boundaries (9→[4,5], 10→[4,6],
17→[8,4,5], K tails).  Loop geometry stays adder-level (no dividers,
no n_blocks table).
"""
from __future__ import annotations

from pycircuit import (
    CycleAwareCircuit,
    CycleAwareDomain,
    mux,
    u,
)

from .types import (
    INST_ID_W,
    K_IDX_W,
    M_IDX_W,
    N_IDX_W,
    SEQ_W,
    TR_DONE,
    TR_K_LOCAL,
    TR_K_OUTER,
    TR_M_SLICE,
    TR_N_INNER,
    TR_N_OUTER,
    TR_W,
    emit_outs,
    sin,
)


def _n_len_rule(rem):
    """``rem∈{9,10} ? 4 : min(8, rem)`` — SRC-02 sec 3.5.2 balanced split."""
    return mux((rem == u(8, 9)) | (rem == u(8, 10)), u(4, 4),
               mux(rem > u(8, 8), u(4, 8), rem[0:4]))


def walker(
    m: CycleAwareCircuit,
    domain: CycleAwareDomain,
    *,
    inputs=None,
    prefix: str = "lfsm_wlk",
) -> dict:
    # ── Cycle 0: state ─────────────────────────────────────────────
    active = domain.signal(width=1, reset_value=0, name=f"{prefix}_active")
    seq = domain.signal(width=SEQ_W, reset_value=0, name=f"{prefix}_seq")
    m_idx = domain.signal(width=M_IDX_W, reset_value=0, name=f"{prefix}_m")
    n_inner = domain.signal(width=4, reset_value=0, name=f"{prefix}_ninner")
    k_local = domain.signal(width=4, reset_value=0, name=f"{prefix}_klocal")
    n_base = domain.signal(width=N_IDX_W, reset_value=0, name=f"{prefix}_nbase")
    k_base = domain.signal(width=K_IDX_W, reset_value=0, name=f"{prefix}_kbase")

    # ── Cycle 0: inputs ────────────────────────────────────────────
    start = sin(inputs, "start", m, domain, prefix=prefix, width=1)
    cfg_inst = sin(inputs, "cfg_inst_id", m, domain, prefix=prefix, width=INST_ID_W)
    cfg_m_mode = sin(inputs, "cfg_m_mode", m, domain, prefix=prefix, width=1)
    cfg_mslice = sin(inputs, "cfg_m_slice", m, domain, prefix=prefix, width=2)
    cfg_nhw = sin(inputs, "cfg_n_hw", m, domain, prefix=prefix, width=8)
    cfg_kgroups = sin(inputs, "cfg_k_groups", m, domain, prefix=prefix, width=6)
    cfg_kstep = sin(inputs, "cfg_k_step", m, domain, prefix=prefix, width=4)
    stall = sin(inputs, "stall", m, domain, prefix=prefix, width=1)

    # ── Cycle 0: combinational ─────────────────────────────────────
    # loop geometry as pure functions of base registers (golden property form)
    n_len = _n_len_rule((cfg_nhw - n_base)[0:8])
    k_count = mux((cfg_kgroups - k_base)[0:6] > cfg_kstep.zext(6),
                  cfg_kstep, (cfg_kgroups - k_base)[0:4])

    last_block = (n_base + n_len)[0:8] == cfg_nhw
    last_outer = (k_base + k_count)[0:6] == cfg_kgroups

    tr = mux(n_inner + u(4, 1) < n_len, u(TR_W, TR_N_INNER),
         mux(k_local + u(4, 1) < k_count, u(TR_W, TR_K_LOCAL),
         mux(m_idx.zext(2) + u(2, 1) < cfg_mslice, u(TR_W, TR_M_SLICE),
         mux(~last_block, u(TR_W, TR_N_OUTER),
         mux(~last_outer, u(TR_W, TR_K_OUTER), u(TR_W, TR_DONE))))))

    advance = active & (~stall)
    tok_done = advance & (tr == u(TR_W, TR_DONE))

    tok_n = (n_base + n_inner)[0:8]
    tok_k = (k_base + k_local)[0:6]

    outs = dict(
        wlk_active=active,
        tok_valid=active,
        tok_advance=advance,
        tok_inst_id=cfg_inst,
        tok_m=m_idx,
        tok_n=tok_n,
        tok_k=tok_k,
        tok_seq=seq,
        tok_first=seq == u(SEQ_W, 0),
        tok_last=tr == u(TR_W, TR_DONE),
        tok_done=tok_done,
        tok_nblk_base=n_base,
        tok_nblk_len=n_len,
        tok_fv_a=(n_base == u(8, 0)) & (n_inner == u(4, 0)),
        tok_fv_b=m_idx == u(1, 0),
        tok_fv_c=(k_base == u(6, 0)) & (k_local == u(4, 0)),
        tok_tr=tr,
    )

    # ── Cycle 0: next-state expressions ────────────────────────────
    active_nxt = mux(tok_done, u(1, 0), mux(start == u(1, 1), u(1, 1), active))
    seq_nxt = mux(start == u(1, 1), u(SEQ_W, 0),
                  mux(advance == u(1, 1), (seq + u(SEQ_W, 1))[0:SEQ_W], seq))

    m_nxt = m_idx
    m_nxt = mux(advance & (tr == u(TR_W, TR_M_SLICE)), (m_idx + u(1, 1))[0:1], m_nxt)
    m_nxt = mux(advance & ((tr == u(TR_W, TR_N_OUTER)) | (tr == u(TR_W, TR_K_OUTER))), u(1, 0), m_nxt)
    m_nxt = mux(start == u(1, 1), u(1, 0), m_nxt)

    ni_nxt = n_inner
    ni_nxt = mux(advance & (tr == u(TR_W, TR_N_INNER)), (n_inner + u(4, 1))[0:4], ni_nxt)
    ni_nxt = mux(advance & (tr != u(TR_W, TR_N_INNER)), u(4, 0), ni_nxt)
    ni_nxt = mux(start == u(1, 1), u(4, 0), ni_nxt)

    kl_nxt = k_local
    kl_nxt = mux(advance & (tr == u(TR_W, TR_K_LOCAL)), (k_local + u(4, 1))[0:4], kl_nxt)
    kl_nxt = mux(advance & ((tr == u(TR_W, TR_M_SLICE)) | (tr == u(TR_W, TR_N_OUTER)) | (tr == u(TR_W, TR_K_OUTER))),
                 u(4, 0), kl_nxt)
    kl_nxt = mux(start == u(1, 1), u(4, 0), kl_nxt)

    nb_nxt = n_base
    nb_nxt = mux(advance & (tr == u(TR_W, TR_N_OUTER)), (n_base + n_len)[0:8], nb_nxt)
    nb_nxt = mux(advance & (tr == u(TR_W, TR_K_OUTER)), u(8, 0), nb_nxt)
    nb_nxt = mux(start == u(1, 1), u(8, 0), nb_nxt)

    kb_nxt = k_base
    kb_nxt = mux(advance & (tr == u(TR_W, TR_K_OUTER)), (k_base + k_count)[0:6], kb_nxt)
    kb_nxt = mux(start == u(1, 1), u(6, 0), kb_nxt)

    domain.next()

    # ── Cycle 1: commits ───────────────────────────────────────────
    active <<= active_nxt
    seq <<= seq_nxt
    m_idx <<= m_nxt
    n_inner <<= ni_nxt
    k_local <<= kl_nxt
    n_base <<= nb_nxt
    k_base <<= kb_nxt

    if inputs is None:
        emit_outs(m, outs, prefix=prefix)
    return outs


walker.__pycircuit_name__ = "walker"
