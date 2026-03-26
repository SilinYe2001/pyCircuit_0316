---
name: pycircuit-output-files
description: >-
  Organizes pyCircuit, pycc, Verilator, and verification outputs under
  output_files_YYYY-MM-DD with Level 2 module folders and Level 3
  generated_code/, compile/, verification/, and logs/. Covers PYC_OUTPUT_ROOT,
  testbench RTL under verification/, and keeping build artifacts out of
  source trees. Use when emitting Verilog or MLIR, running simulations,
  writing or updating shell/Python build scripts, moving or naming
  generated_artifacts, counter_sim, find_max outputs, or when the user mentions
  output_files, output_files_0324, artifact layout, compile paths, tutorial
  generated folders, or log placement for pyCircuit runs.
---

# pyCircuit output file layout

## When this applies

Use this skill for **any** new or updated workflow that writes **emit/pycc/simulation** artifacts in this repo: shell wrappers, CI steps, docs that cite output paths, or moving batch outputs.

## Rules (do this)

1. **Level 1 — dated root**  
   Use `output_files_YYYY-MM-DD/` at repo root (or path in `PYC_OUTPUT_ROOT`). Optional symlink alias such as `output_files_MMDD` is fine if the team already uses it.

2. **Level 2 — folder naming**  
   - **Sub-agent workflow** (planner + implementation + verification planning for the same block): use **exactly one** Level 2 folder **`<module>__subagent`** (e.g. `arith_shifter__subagent`). It holds **everything** for that workflow: **`docs/`**, **`pycircuit/`** (or other DUT source), **`rtl/`** if any, **`compile/`**, **`verification/`**, **`logs/`**, optional **`generated_code/`**. **Do not** create a **second** parallel **`module/`** without `__subagent` for the same block—that duplicates two workflows.  
   - **Runs that never use sub-agents** may still use plain **`module`** (no `__subagent` suffix); that is a different convention, not a sibling of the same IP.  
   Avoid vague names (`run1`, `tmp`).

3. **Level 3 — layout under each Level 2 folder**  
   Use the following directories (all **siblings** under Level 2):

   | Directory | Put here |
   |-----------|----------|
   | `docs/` | **Sub-agent workflow** (`module__subagent`): **Handoff = Markdown only** — `docs/plans/…/architecture.md`, `docs/test_plans/…/test_plan.md`. `docs/design/*.md` = optional implementation notes. **`docs/monitor/<run_slug>/`** = **monitor** agent reports (`execution_digest*.md`, `spec_consistency_report*.md`); not spec handoff, same Level 3 `docs/` tree. **Not** for repo-root tutorial content. |
   | `generated_code/` | Optional **MLIR / IR** exports and similar; **do not** put planner or test-plan Markdown here. |
   | `compile/` | `*.pyc`, pycc `*.v`, `*.stats.json`, cpp manifests from the compiler pipeline |
   | `verification/` | Testbench Verilog/SystemVerilog (`tb_*.v`, `tb_*.sv`), Verilator `obj_*` dirs, `*.vcd` / `*.fst`, golden vectors, bulky sim artifacts |
   | `logs/` | Text logs, regression summaries, PASS/FAIL notes |

   **Split principle (sub-agent tree):** planning prose → **`module__subagent/docs/`**; DUT **Python/RTL sources** → **`module__subagent/pycircuit/`**, **`module__subagent/rtl/`**, etc.; compiler outputs → **`module__subagent/compile/`**; sim trees → **`module__subagent/verification/`**; logs → **`module__subagent/logs/`**.

4. **Testbenches**  
   Keep RTL TB alongside verification artifacts: `<project>/verification/tb_…` in the **source** tree when the TB is versioned; dated `output_files/…/verification/` may hold **obj**/**vcd** and optionally a **copy** of TB only for self-contained drops—do not maintain two diverging TB copies without a process.

5. **Scripts**  
   Resolve paths as:

   ```bash
   REPO="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
   OUT_ROOT="${PYC_OUTPUT_ROOT:-$REPO/output_files_YYYY-MM-DD}"
   # sub-agent IP: "$OUT_ROOT/<module>__subagent/{compile,verification,logs}/…"
   ```

   Document the default date folder or tell users to `export PYC_OUTPUT_ROOT=…`.

6. **Docs and READMEs**  
   Use **repo-relative** paths (from `REPO`), not machine-specific absolutes.

7. **Sub-agent / workflow**  
   Sub-agent **docs** live under **`OUT_ROOT/<module>__subagent/docs/…`** (see `docs/sub_agent_docs/subagent_collaboration_workflow.md`), **sibling** to **`generated_code/`**, not inside it. **Emit, pycc, sim logs, and `verification/` build trees** for that same workflow stay under the **same** **`OUT_ROOT/<module>__subagent/{compile,verification,logs}/`**. Repo-wide **tutorial / policy** may also live under **`docs/`**; **output layout prose** is **`docs/sub_agent_docs/output_files_management.md`**.

## Checklist before merging script or doc changes

- [ ] Sub-agent workflow uses **one** `OUT_ROOT/<module>__subagent/` tree: `docs/`, optional `generated_code/`, plus `compile/`, `verification/`, `logs/`, and DUT source dirs (`pycircuit/`, `rtl/`, …)—**no** duplicate `OUT_ROOT/<module>/` for the same IP.
- [ ] TB paths point at `…/verification/tb_…` (or an agreed subfolder under `verification/`).
- [ ] `PYC_OUTPUT_ROOT` is honored where other project scripts already use it.
- [ ] No new default that dumps `*.v` / `obj_*` next to **design source** without team agreement.

## Full specification

For the canonical narrative, examples, and Chinese prose, read **`docs/sub_agent_docs/output_files_management.md`** in this repository (use the Read tool on that path when implementing or auditing layout).
