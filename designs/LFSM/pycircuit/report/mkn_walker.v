`timescale 1ns/1ps
// ============================================================================
// mkn_walker.v
//
// [SHARED] Shared MKN walker.
// Spec: docs/shared/01_FSM走法逻辑.md (MKN order, counters, transitions,
//       stall, N-tail), docs/shared/00_TOP模块连接框架.md section 3.6.1
//       (WalkConfig content).
//
// Instantiated twice per 4EU core (docs/shared/00 section 2):
//   - u_lfsm_walker : drives the LFSM load side
//   - u_efsm_walker : drives the EFSM execute side (absent in PEER role)
// Both walkers receive identical WalkConfig content but keep independent
// state, counters and stall.
//
// Behavior (docs/shared/01):
//   - IDLE -> WALK on WalkConfig accept (i_walk_cfg_valid && ready);
//     ready only while idle, so a config handoff never lands mid-walk
//     (matches MknWalkFSM.start raising while active).
//   - WALK: token outputs are combinational from the registered counters
//     (evaluate/commit split, like MknWalkFSM.token()/advance()). Counters
//     update only on i_walk_advance; while advance is low the token, all
//     counters, walk_seq and transition hold (stall, 01 section 12).
//   - Transition priority per advance: N_INNER -> K_LOCAL -> M_SLICE ->
//     N_OUTER -> K_OUTER -> DONE (01 section 10.2).
//   - o_walk_done pulses in the same cycle the last token is advanced
//     (last_mkn && walk_advance, 01 section 11).
//
// The walker consumes an already-validated WalkConfig (TOP / top_config
// owns legality, 01 section 5). k_step_per_outer is derived from m_mode
// (m16 -> 8, m32 -> 4). N-block boundaries are not a table input: the
// frozen 4EU partition (build_n_blocks, n_block_step=1) is a closed form
// of the remaining N4 count, so the walker only needs n_hw_count.
//
// Implementation (addr_gen refactor):
//   - The three token indices n_idx / k_idx / m_idx are each maintained by
//     one addr_gen instance (rtl/prim/addr_gen.v); the walker aggregates
//     the loop-transition conditions into their init/plus/record/return
//     control inputs (one-hot-or-zero per instance by construction: the
//     transition encoder is mutually exclusive and cfg_accept only fires
//     while idle).
//   - N block-end boundary (n_bound) is a plain register: remaining R =
//     n_hw_count - n_bound,
//       len = (R < 9) ? R : (R <= 10) ? 4 : 8
//     so no packed n_blocks table / block-index counter is needed.
//   - K outer boundaries are uniform (k_step, power of two) with a single
//     terminal truncation at k_groups, so the K loop-end tests are
//     stateless ((k_idx+1) low bits / == k_groups) and need no boundary
//     register; K's only dynamic state is the outer-base savepoint inside
//     its addr_gen (the M_SLICE/N_OUTER return target).
//   - bufc_idx (BufC slot select for the core-external BufC, tb/buf_c.v:
//     n_idx - n_base of the current N-block, 0..7) is a fourth addr_gen:
//     init on accept/K_OUTER, += n_span on N_INNER (n_span=2 covers two
//     consecutive slots), return-init 0 on every event that returns n_idx
//     to a block base (K_LOCAL / M_SLICE / N_OUTER).
//   - kn_linear (k*n_hw_count, LFSM rd_addr_gen address assist) is a fifth
//     addr_gen: identical control to u_k_idx with per-K stride
//     n_hw_count instead of +1, so the LFSM commit-cycle cloud needs no
//     multiplier (rtl/4EU_RTL_PLAN.md P4 组合深度预算, second-level
//     option). Cross-checked against a direct multiply in the sim guard.
// ============================================================================

module mkn_walker #(
    parameter INST_ID_W = 8,
    parameter M_IDX_W   = 2,    // m_slice index (m32: 0/1)
    parameter N_IDX_W   = 7,    // N4 index, n_hw_count <= 128
    parameter K_IDX_W   = 5,    // K32B group index, k_groups <= 32
    parameter N_SPAN_W  = 2,    // N4 span per token (1 or 2)
    parameter BUFC_IDX_W = 3,   // BufC slot index (0..7 within an N-block)
    parameter SEQ_W     = 16    // walk_seq width
) (
    input  wire                 clk,
    input  wire                 rst_n,

    // WalkConfig input channel (valid/ready, docs/shared/00 section 3.7)
    input  wire                 i_walk_cfg_valid,
    output wire                 o_walk_cfg_ready,
    input  wire [INST_ID_W-1:0] i_walk_cfg_inst_id,
    input  wire                 i_walk_cfg_m_mode,           // 0: m16, 1: m32
    input  wire [1:0]           i_walk_cfg_m_slice_count,    // 1 or 2
    input  wire [N_IDX_W:0]     i_walk_cfg_n_hw_count,       // 1..128
    input  wire [1:0]           i_walk_cfg_n_step,           // 4EU: load 1, exec 1|2 (B4)
    input  wire [K_IDX_W:0]     i_walk_cfg_k_groups,         // 1..32

    // WalkToken output (docs/shared/01)
    output wire                 o_token_valid,
    output wire [INST_ID_W-1:0] o_token_inst_id,
    output wire [M_IDX_W-1:0]   o_token_m_idx,
    output wire [K_IDX_W-1:0]   o_token_k_idx,
    output wire [N_IDX_W-1:0]   o_token_n_idx,
    output wire [N_SPAN_W-1:0]  o_token_n_span,
    output wire [2:0]           o_token_transition,          // TR_* encoding below
    output wire                 o_token_last_mkn,
    output wire [SEQ_W-1:0]     o_token_walk_seq,

    // BufC slot select for the core-external BufC (tb/buf_c.v):
    // n_idx - n_base of the current N-block, 0..7. Token-aligned like the
    // fields above, but an RTL-side auxiliary output, not a WalkToken
    // contract field (docs/shared/01).
    output wire [BUFC_IDX_W-1:0] o_bufc_idx,

    // k*n_hw_count linear component (P4: LFSM rd_addr_gen B/BMX source
    // addresses — eliminates the k*n_hw multiplier from the commit-cycle
    // cloud by accumulating it cycle-by-cycle, plan "组合深度预算"
    // second-level option). Same control pattern as u_k_idx with the
    // per-K stride n_hw_count instead of +1. RTL-side auxiliary output,
    // not a WalkToken contract field.
    // downstream: u_lfsm.i_token_kn → u_rag（经 fsm_eu4_core 线网
    //             lw_token_kn；仅 u_lfsm_walker 实例接出）
    output wire [K_IDX_W+N_IDX_W-1:0] o_token_kn,

    // Second N4 of the current token's group (plain-B4 execute profile,
    // n_span=2). o_token_n_idx always carries the group's first N4 (both
    // n_step=1 and n_step=2). valid is high only while the token actually
    // covers two N4s (cur_n_span == 2); odd-tail single-N4 tokens and
    // idle drive valid=0 / index=0.
    output wire [N_IDX_W-1:0] o_token_n_index_double,
    output wire               o_token_n_index_double_valid,

    // Consume/advance handshake from the owning FSM
    input  wire                 i_walk_advance,
    output wire                 o_walk_active,
    output wire                 o_walk_done,

    // Latched WalkConfig readout (P4: the LFSM rdgen geometry planner
    // needs k_groups alongside the token stream; the walker's registered
    // copy is per-instruction stable for the whole walk, unlike the
    // lwcfg channel pins which may advance to the next instruction once
    // accepted). Not a WalkToken contract field.
    // downstream: u_lfsm.i_cfg_k_groups（经 fsm_eu4_core 线网；仅
    //             u_lfsm_walker 实例接出，u_efsm_walker 悬空）
    output wire [K_IDX_W:0]     o_cfg_k_groups,
    // Latched n_hw_count readout (B2B config-in-entry: the assembler reads
    // n_hw_count from the queue entry, which lfsm packs from this
    // walk-stable copy at commit time — synchronized with the token even
    // when the next instruction's config has been accepted).
    // downstream: u_lfsm.i_cfg_n_hw_count_w（经 fsm_eu4_core 线网；仅
    //             u_lfsm_walker 实例接出，u_efsm_walker 悬空）
    output wire [N_IDX_W:0]     o_cfg_n_hw_count
);

    // Walk transition encoding (docs/shared/01, docs/four_eu/03 section 7.2)
    localparam TR_N_INNER = 3'd0;
    localparam TR_K_LOCAL = 3'd1;
    localparam TR_M_SLICE = 3'd2;
    localparam TR_N_OUTER = 3'd3;
    localparam TR_K_OUTER = 3'd4;
    localparam TR_DONE    = 3'd5;

    // ==================================================================
    // State: config + walk bookkeeping (01 section 10.1). All state is
    // held in reg_en instances (the only timing in this module, see
    // bottom); the wires below are the instance outputs. The M/K/N token
    // indices live in the three addr_gen instances.
    // ==================================================================
    wire                   active;
    wire [INST_ID_W-1:0]   cfg_inst_id;
    wire                   cfg_m_mode;            // 0: m16, 1: m32
    wire [1:0]             cfg_m_slice_count;
    wire [N_IDX_W:0]       cfg_n_hw_count;
    wire [1:0]             cfg_n_step;
    wire [K_IDX_W:0]       cfg_k_groups;
    wire [SEQ_W-1:0]       walk_seq;

    // N block-end boundary (a single reg_en: init/plus/hold only — the
    // addr_gen savepoint/return machinery would be entirely idle here).
    wire [N_IDX_W:0]       n_bound;

    // ==================================================================
    // Handshake / control aggregation (01 section 3.1, 10.2)
    // ==================================================================
    wire cfg_accept = i_walk_cfg_valid & ~active;
    wire advance    = active & i_walk_advance;
    wire stall      = active & ~i_walk_advance;

    // ==================================================================
    // Token indices, driven by the addr_gen instances below
    // ==================================================================
    wire [N_IDX_W-1:0] n_idx;
    wire [K_IDX_W-1:0] k_idx;
    wire [M_IDX_W-1:0] m_idx;
    wire [BUFC_IDX_W-1:0] bufc_idx;
    wire [K_IDX_W+N_IDX_W-1:0] kn_linear;
    wire               n_ovf;
    wire               k_ovf;
    wire               m_ovf;
    wire               bufc_ovf;
    wire               kn_ovf;

    // ==================================================================
    // Closed-form 4EU N-block partition (build_n_blocks, n_block_step=1):
    // the block length depends only on the remaining N4 count R.
    // ==================================================================
    // R at walk (re)start: config accept samples the input channel (the
    // config registers latch on the same edge), a K_OUTER restart uses
    // the latched config.
    wire [N_IDX_W:0] r_init;
    mux2 #(.WIDTH(N_IDX_W+1)) mux_r_init (
        .i_sel(cfg_accept), .i_d0(cfg_n_hw_count),
        .i_d1(i_walk_cfg_n_hw_count), .o_y(r_init)
    );
    // len = (R < 9) ? R : (R <= 10) ? 4 : 8 — one-hot-ified (each lower
    // way gated by the negation of the higher conditions), preserving the
    // chain semantics exactly.
    wire             r_init_lt9   = (r_init < 8'd9);
    wire             r_init_le10  = (r_init <= 8'd10);
    wire [2:0]       len_init_sel = {~r_init_lt9 & ~r_init_le10,
                                     ~r_init_lt9 &  r_init_le10,
                                     r_init_lt9};
    wire [11:0]      len_init_d   = {4'd8, 4'd4, r_init[3:0]};
    wire [3:0]       len_init;
    mux_onehot #(.WIDTH(4), .N(3)) mux_len_init (
        .i_sel(len_init_sel), .i_d(len_init_d), .o_y(len_init)
    );
    // R at an N_OUTER: n_bound still holds the old block end, so the
    // remaining count is one subtract away.
    wire [N_IDX_W:0] r_next   = cfg_n_hw_count - n_bound;
    wire             r_next_lt9   = (r_next < 8'd9);
    wire             r_next_le10  = (r_next <= 8'd10);
    wire [2:0]       len_next_sel = {~r_next_lt9 & ~r_next_le10,
                                     ~r_next_lt9 &  r_next_le10,
                                     r_next_lt9};
    wire [11:0]      len_next_d   = {4'd8, 4'd4, r_next[3:0]};
    wire [3:0]       len_next;
    mux_onehot #(.WIDTH(4), .N(3)) mux_len_next (
        .i_sel(len_next_sel), .i_d(len_next_d), .o_y(len_next)
    );

    // ==================================================================
    // Current-token combinational view (MknWalkFSM.token())
    // ==================================================================
    // n_span = min(n_step, n_bound - n_idx)  (01 section 7)
    wire [N_IDX_W:0]    n_rem      = n_bound - {1'b0, n_idx};
    wire                n_rem_fits =
        (n_rem <= {{(N_IDX_W-1){1'b0}}, cfg_n_step});
    wire [N_SPAN_W-1:0] cur_n_span;
    mux2 #(.WIDTH(N_SPAN_W)) mux_cur_n_span (
        .i_sel(n_rem_fits), .i_d0(cfg_n_step),
        .i_d1(n_rem[N_SPAN_W-1:0]), .o_y(cur_n_span)
    );

    // Boundary flags (01 section 10.2 / 11)
    wire last_n_inner = n_rem_fits;
    wire last_n_outer = last_n_inner & (n_bound == cfg_n_hw_count);

    // K outer boundaries: uniform k_step (power of two, derived from
    // m_mode) + one terminal truncation at k_groups.
    wire k_step_is_8 = ~cfg_m_mode;     // m16 -> 8, m32 -> 4
    wire [K_IDX_W:0] k_next = {1'b0, k_idx} + {{K_IDX_W{1'b0}}, 1'b1};
    wire k_next_al8 = (k_next[2:0] == 3'b000);
    wire k_next_al4 = (k_next[1:0] == 2'b00);
    wire k_next_aligned;
    mux2 #(.WIDTH(1)) mux_k_next_aligned (
        .i_sel(k_step_is_8), .i_d0(k_next_al4), .i_d1(k_next_al8),
        .o_y(k_next_aligned)
    );
    wire last_k_local = (k_next == cfg_k_groups) | k_next_aligned;
    wire last_k_outer = last_k_local & (k_next == cfg_k_groups);

    wire last_m_slice = ({1'b0, m_idx} + {{M_IDX_W{1'b0}}, 1'b1})
                        >= {1'b0, cfg_m_slice_count};

    reg [2:0] transition;
    always @* begin
        if (!last_n_inner)       transition = TR_N_INNER;
        else if (!last_k_local)  transition = TR_K_LOCAL;
        else if (!last_m_slice)  transition = TR_M_SLICE;
        else if (!last_n_outer)  transition = TR_N_OUTER;
        else if (!last_k_outer)  transition = TR_K_OUTER;
        else                     transition = TR_DONE;
    end

    // ==================================================================
    // Per-transition control aggregation into the addr_gen instances.
    // TR_DONE fires nothing: the counters hold and active clears.
    // ==================================================================
    wire adv_n_inner = advance & (transition == TR_N_INNER);
    wire adv_k_local = advance & (transition == TR_K_LOCAL);
    wire adv_m_slice = advance & (transition == TR_M_SLICE);
    wire adv_n_outer = advance & (transition == TR_N_OUTER);
    wire adv_k_outer = advance & (transition == TR_K_OUTER);

    // ==================================================================
    // n_bound: N block-end boundary register (reg_en instance)
    // ==================================================================
    wire               n_bound_en = cfg_accept | adv_k_outer | adv_n_outer;
    wire               n_bound_reload = cfg_accept | adv_k_outer;
    wire [N_IDX_W:0]   len_init_ext   = {{(N_IDX_W-3){1'b0}}, len_init};
    wire [N_IDX_W:0]   n_bound_accum  = n_bound
                                        + {{(N_IDX_W-3){1'b0}}, len_next};
    wire [N_IDX_W:0]   n_bound_d;
    mux2 #(.WIDTH(N_IDX_W+1)) mux_n_bound_d (
        .i_sel(n_bound_reload), .i_d0(n_bound_accum),
        .i_d1(len_init_ext), .o_y(n_bound_d)
    );
    reg_en #(
        .WIDTH   (N_IDX_W+1),
        .RST_EN  (1),
        .RST_VAL ({(N_IDX_W+1){1'b0}})
    ) reg_n_bound (
        .clk   (clk),
        .rst_n (rst_n),
        .i_en  (n_bound_en),
        .i_d   (n_bound_d),
        .o_q   (n_bound)
    );

    // ==================================================================
    // addr_gen instances: one per M/K/N token index
    // ==================================================================
    // N index: plus n_span within and across blocks (the last token of a
    // block lands exactly on n_bound = next block base, recorded as the
    // new savepoint); return to the block-base savepoint on K_LOCAL /
    // M_SLICE; re-init (address and savepoint) on K_OUTER / config accept.
    wire               n_init_en     = cfg_accept | adv_k_outer;
    wire               n_plus_en     = adv_n_inner | adv_n_outer;
    wire [N_IDX_W-1:0] n_plus_offset = {{(N_IDX_W-N_SPAN_W){1'b0}}, cur_n_span};
    wire               n_ret_en      = adv_k_local | adv_m_slice;
    addr_gen #(
        .ADDR_WIDTH (N_IDX_W),
        .STRIDE_NUM (1),
        .RST_EN     (1)
    ) u_n_idx (
        .clk              (clk),
        .rst_n            (rst_n),
        .i_stall_en       (stall),
        .i_init_en        (n_init_en),
        .i_init_addr      ({N_IDX_W{1'b0}}),
        .i_return_init_en (1'b0),
        .i_plus_en        (n_plus_en),
        .i_plus_offset    (n_plus_offset),
        .i_record_en      (1'b0),
        .i_record_nxt_en  (adv_n_outer),
        .i_return_en      (n_ret_en),
        .i_return_plus_en (1'b0),
        .i_return_offset  ({N_IDX_W{1'b0}}),
        .o_addr_out       (n_idx),
        .o_addr_ovf       (n_ovf)
    );

    // K index: +1 within an outer; return to the outer-base savepoint on
    // M_SLICE / N_OUTER; on K_OUTER (full outers only) +1 lands exactly on
    // the next outer base and records it as the new savepoint.
    wire               k_plus_en = adv_k_local | adv_k_outer;
    wire               k_ret_en  = adv_m_slice | adv_n_outer;
    addr_gen #(
        .ADDR_WIDTH (K_IDX_W),
        .STRIDE_NUM (1),
        .RST_EN     (1)
    ) u_k_idx (
        .clk              (clk),
        .rst_n            (rst_n),
        .i_stall_en       (stall),
        .i_init_en        (cfg_accept),
        .i_init_addr      ({K_IDX_W{1'b0}}),
        .i_return_init_en (1'b0),
        .i_plus_en        (k_plus_en),
        .i_plus_offset    ({{(K_IDX_W-1){1'b0}}, 1'b1}),
        .i_record_en      (1'b0),
        .i_record_nxt_en  (adv_k_outer),
        .i_return_en      (k_ret_en),
        .i_return_plus_en (1'b0),
        .i_return_offset  ({K_IDX_W{1'b0}}),
        .o_addr_out       (k_idx),
        .o_addr_ovf       (k_ovf)
    );

    // k*n_hw_count shadow (P4, LFSM rd_addr_gen B/BMX address assist): identical
    // control to u_k_idx, with the per-K stride n_hw_count in place of
    // +1 — the commit-cycle cloud downstream then needs no multiplier.
    // Savepoint semantics match: record_nxt on K_OUTER captures the new
    // outer base x n_hw; M_SLICE / N_OUTER return to it; cfg_accept
    // re-inits address and savepoint per instruction.
    addr_gen #(
        .ADDR_WIDTH (K_IDX_W+N_IDX_W),   // k*n_hw <= 31*128 = 3968
        .STRIDE_NUM (1),
        .RST_EN     (1)
    ) u_kn_linear (
        .clk              (clk),
        .rst_n            (rst_n),
        .i_stall_en       (stall),
        .i_init_en        (cfg_accept),
        .i_init_addr      ({(K_IDX_W+N_IDX_W){1'b0}}),
        .i_return_init_en (1'b0),
        .i_plus_en        (k_plus_en),
        .i_plus_offset    ({{(K_IDX_W-1){1'b0}}, cfg_n_hw_count}),
        .i_record_en      (1'b0),
        .i_record_nxt_en  (adv_k_outer),
        .i_return_en      (k_ret_en),
        .i_return_plus_en (1'b0),
        .i_return_offset  ({(K_IDX_W+N_IDX_W){1'b0}}),
        .o_addr_out       (kn_linear),
        .o_addr_ovf       (kn_ovf)
    );

    // M index: +1 per slice; back to 0 (return-init) on N_OUTER / K_OUTER.
    wire               m_ret_init_en = adv_n_outer | adv_k_outer;
    addr_gen #(
        .ADDR_WIDTH (M_IDX_W),
        .STRIDE_NUM (1),
        .RST_EN     (1)
    ) u_m_idx (
        .clk              (clk),
        .rst_n            (rst_n),
        .i_stall_en       (stall),
        .i_init_en        (cfg_accept),
        .i_init_addr      ({M_IDX_W{1'b0}}),
        .i_return_init_en (m_ret_init_en),
        .i_plus_en        (adv_m_slice),
        .i_plus_offset    ({{(M_IDX_W-1){1'b0}}, 1'b1}),
        .i_record_en      (1'b0),
        .i_record_nxt_en  (1'b0),
        .i_return_en      (1'b0),
        .i_return_plus_en (1'b0),
        .i_return_offset  ({M_IDX_W{1'b0}}),
        .o_addr_out       (m_idx),
        .o_addr_ovf       (m_ovf)
    );

    // BufC slot index: n_idx - n_base of the current N-block (0..7).
    // Every event that moves n_idx to a block base clears it, so the
    // savepoint machinery stays idle (same shape as u_m_idx):
    //   init        : cfg_accept | K_OUTER (walk / K-outer restart)
    //   plus n_span : N_INNER (n_span=2 covers two consecutive slots)
    //   return-init : K_LOCAL | M_SLICE | N_OUTER (back to the block base)
    wire                  bufc_init_en     = cfg_accept | adv_k_outer;
    wire                  bufc_ret_init_en = adv_k_local | adv_m_slice
                                           | adv_n_outer;
    wire [BUFC_IDX_W-1:0] bufc_plus_offset =
        {{(BUFC_IDX_W-N_SPAN_W){1'b0}}, cur_n_span};
    addr_gen #(
        .ADDR_WIDTH (BUFC_IDX_W),
        .STRIDE_NUM (1),
        .RST_EN     (1)
    ) u_bufc_idx (
        .clk              (clk),
        .rst_n            (rst_n),
        .i_stall_en       (stall),
        .i_init_en        (bufc_init_en),
        .i_init_addr      ({BUFC_IDX_W{1'b0}}),
        .i_return_init_en (bufc_ret_init_en),
        .i_plus_en        (adv_n_inner),
        .i_plus_offset    (bufc_plus_offset),
        .i_record_en      (1'b0),
        .i_record_nxt_en  (1'b0),
        .i_return_en      (1'b0),
        .i_return_plus_en (1'b0),
        .i_return_offset  ({BUFC_IDX_W{1'b0}}),
        .o_addr_out       (bufc_idx),
        .o_addr_ovf       (bufc_ovf)
    );

    // ==================================================================
    // Outputs
    // ==================================================================
    assign o_walk_cfg_ready   = ~active;
    assign o_token_valid      = active;
    assign o_token_inst_id    = cfg_inst_id;
    assign o_token_m_idx      = m_idx;
    assign o_token_k_idx      = k_idx;
    assign o_token_n_idx      = n_idx;
    assign o_token_n_span     = cur_n_span;
    assign o_token_transition = transition;
    assign o_token_last_mkn   = (transition == TR_DONE);
    assign o_token_walk_seq   = walk_seq;
    assign o_bufc_idx         = bufc_idx;
    assign o_token_kn         = kn_linear;
    // n_index_double: the group's second N4 (n_idx + 1) on two-N4 tokens
    // (cur_n_span == 2); otherwise valid=0 and the index drives 0.
    wire                  n_pair = active & (cur_n_span == 2'd2);
    wire [N_IDX_W-1:0]    n_idx_second = n_idx + {{(N_IDX_W-1){1'b0}}, 1'b1};
    assign o_token_n_index_double_valid = n_pair;
    // Zero-input select as an AND gate: 0 unless the token pairs two N4.
    assign o_token_n_index_double = {N_IDX_W{n_pair}} & n_idx_second;
    assign o_walk_active      = active;
    // walk_done: last token successfully advanced (01 section 11)
    assign o_walk_done        = active & i_walk_advance & (transition == TR_DONE);
    // Latched config readout (P4 rdgen geometry planner)
    assign o_cfg_k_groups     = cfg_k_groups;
    assign o_cfg_n_hw_count   = cfg_n_hw_count;

    // ==================================================================
    // State registers: reg_en instances (01 section 10.1/10.2). All
    // update conditions are the aggregated wires above; no always
    // register block remains in this module.
    // ==================================================================
    // Config fields latch on accept: same enable -> ONE reg_en instance,
    // payload packed/unpacked by concatenation (style rule R1).
    // (RST_EN=1, RST_VAL=0)
    localparam CFG_PAYLOAD_W = INST_ID_W + 1 + 2 + (N_IDX_W+1) + 2
                             + (K_IDX_W+1);
    wire [CFG_PAYLOAD_W-1:0] cfg_d;
    wire [CFG_PAYLOAD_W-1:0] cfg_q;
    assign cfg_d = {i_walk_cfg_inst_id,
                    i_walk_cfg_m_mode,
                    i_walk_cfg_m_slice_count,
                    i_walk_cfg_n_hw_count,
                    i_walk_cfg_n_step,
                    i_walk_cfg_k_groups};
    assign {cfg_inst_id,
            cfg_m_mode,
            cfg_m_slice_count,
            cfg_n_hw_count,
            cfg_n_step,
            cfg_k_groups} = cfg_q;
    reg_en #(.WIDTH(CFG_PAYLOAD_W)) reg_cfg (
        .clk(clk), .rst_n(rst_n), .i_en(cfg_accept),
        .i_d(cfg_d), .o_q(cfg_q));

    // active: set on config accept, cleared when the last token advances
    wire active_en = cfg_accept | (advance & (transition == TR_DONE));
    reg_en #(.WIDTH(1)) reg_active (
        .clk(clk), .rst_n(rst_n),
        .i_en(active_en),
        .i_d(cfg_accept), .o_q(active));

    // walk_seq: 0 at accept, +1 per advance (incl. the DONE advance)
    // (zero-input select as an AND gate: accept clears the increment).
    wire               walk_seq_en  = cfg_accept | advance;
    wire [SEQ_W-1:0]   walk_seq_inc = walk_seq + {{(SEQ_W-1){1'b0}}, 1'b1};
    wire [SEQ_W-1:0]   walk_seq_d   = {SEQ_W{~cfg_accept}} & walk_seq_inc;
    reg_en #(.WIDTH(SEQ_W)) reg_walk_seq (
        .clk(clk), .rst_n(rst_n), .i_en(walk_seq_en),
        .i_d(walk_seq_d),
        .o_q(walk_seq));

`ifndef SYNTHESIS
    // ------------------------------------------------------------------
    // Simulation-only guards (synchronous rst_n sample alongside its
    // async-reset use is intentional, same pattern as addr_gen).
    // ------------------------------------------------------------------
    /* verilator lint_off SYNCASYNCNET */
    always @(posedge clk) begin
        if (rst_n) begin
            // Legal walks never overflow the index counters.
            if (n_ovf | k_ovf | m_ovf | bufc_ovf | kn_ovf) begin
                $display("FATAL %m: addr_gen overflow (n=%b k=%b m=%b bufc=%b kn=%b) at %0t",
                         n_ovf, k_ovf, m_ovf, bufc_ovf, kn_ovf, $time);
                $fatal(1);
            end
            // Cross-check the k*n_hw shadow against a direct multiply
            // (the multiply exists only in this assertion, never
            // synthesized): while a walk is active the shadow must equal
            // k_idx * n_hw_count every cycle, stall cycles included.
            if (active &&
                (kn_linear !== ({{(N_IDX_W+1){1'b0}}, k_idx}
                                * cfg_n_hw_count))) begin
                $display("FATAL %m: kn_linear=%0d != k_idx=%0d * n_hw=%0d at %0t",
                         kn_linear, k_idx, cfg_n_hw_count, $time);
                $fatal(1);
            end
            // n_bound sanity: n_idx < n_bound <= n_hw_count while active.
            if (active && (({1'b0, n_idx} >= n_bound)
                           || (n_bound > cfg_n_hw_count))) begin
                $display("FATAL %m: n_bound sanity failed (n_idx=%0d n_bound=%0d n_hw=%0d) at %0t",
                         n_idx, n_bound, cfg_n_hw_count, $time);
                $fatal(1);
            end
        end
    end
    /* verilator lint_on SYNCASYNCNET */
`endif

endmodule
