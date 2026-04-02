# CSU block — agent implementation requirements

This document instructs an autonomous coding agent on **how to implement the CSU (Coherent System Unit, or project-specific “CSU” as defined in LinxCore950 documentation)** inside the pyCircuit repository.

**Methodology:** `docs/pycircuit_implementation_method.md` (includes **§ From converted Markdown to feature list, step docs, and test plan** — same pipeline as CSU `docs/`).  
**CSU working documents:** this folder (`designs/CSU/docs/`). Detailed **10-step** content is split into the files below so each can evolve independently.

---

## Document index (read order)

| File | Content |
|------|---------|
| **`step1.md` … `step10.md`** | Full **Step 1–10** narrative, checklists, and CSU-specific instructions. |
| **`workflow_substeps.md`** | **Optional finer splits** (2a–2e, 3a–3f, …) when a single step is too large; process-only until you add more tests. |
| **`requirement_sources.md`** | Step 2 — SRC-01…SRC-08 source catalog and extraction checklist. |
| **`converted/`** | Markdown exports of XLSX/DOCX/PDF (`export_specs_to_md.py`); primary text for agents. |
| **`ASSUMPTIONS.md`** | Port directions, reset notes, opcode / XLSX caveats. |
| **`port_list.md`** | Step 3 — clocks, aggregated flit buses, widths, field inventory seeds. |
| **`feature_list.md`** | Step 3 — F-001… feature IDs, priorities, spec trace placeholders. |
| **`function_list.md`** | Step 4 — algorithmic function catalog and call graph. |
| **`test_list.md`** | Step 8 — T-001… directed tests + SYS-xxx system scenarios. |
| **`traceability.md`** | Step 7 — port/feature/test matrices + gap register + sign-off. |
| **`incremental_plan.md`** | Step 9 — Inc-0… backlog and dependency graph. |
| **`cycle_budget.md`** | **Occurrence / `pyc.reg` 预算**；Inc-0 黄金计数；与 `csu.assert_inc0_mlir_cycle_contract` 对齐。 |
| **`system_test_spec.md`** | Step 10 — expanded SYS scenario steps and final checklist. |

**Automation:** `designs/CSU/run_csu_verification.py` runs **Step 1–10 + system** checks without pytest; `designs/CSU/test_csu_steps.py` supports optional `pytest -m stepN`.

---

## Part I — Process, inputs, and repo rules (summary)

### 1. Programming style and API documentation (`docs/`)

Root: **`/Users/mac/Documents/pycircuit2/pyCircuit/docs`** (or `docs/` from repo root).

| Priority | Document | Purpose |
|----------|----------|---------|
| V5 API | `docs/PyCurcit V5_CYCLE_AWARE_API.md` | `CycleAwareCircuit`, `domain.next()`, `state`, `cycle`, `cas`, `mux`. |
| V5 tutorial | `docs/PyCircuit V5 Programming Tutorial.md` | Idioms and patterns. |
| TB | `docs/TESTBENCH.md` | `@testbench`, `Tb`. |
| `@module` | `docs/FRONTEND_API.md`, `docs/tutorial/unified-signal-model.md` | Circuit authoring. |
| Agents | `AGENTS.md`, `docs/updatePLAN.md`, `docs/rfcs/pyc4.0-decisions.md` | Gate-first policy. |

**Import:** `from pycircuit import ...`; `PYTHONPATH=<repo>/compiler/frontend`.

### 2. Example designs (`designs/`)

Path: **`/Users/mac/Documents/pycircuit2/pyCircuit/designs`**. References: `designs/RegisterFile/`, `designs/BypassUnit/`, `designs/IssueQueue/`, `designs/examples/*/`.

### 3. Authoritative CSU specs (this `docs/` folder)

| Artifact | Role |
|----------|------|
| `LinxCore950 CSU Design Specification-AI辅助设计输入.docx` | Behavior, timing, boundary, **port direction**. |
| `CSU 接口Protocol_辅助设计输入.xlsx` | Flit fields, widths (**used in `port_list.md`**). |
| `IHI0050H_amba_chi_architecture_spec.pdf` | CHI reference. |

Conflicts → `designs/CSU/ASSUMPTIONS.md`.

### 4–9. Workflow, rules, layout, non-goals, done criteria, links

- **Workflow:** follow **`step1.md`–`step10.md`** + `docs/pycircuit_implementation_method.md`.  
- **Rules:** gate-first; no backend-only semantics (`AGENTS.md`).  
- **Layout:** `designs/CSU/csu.py`, `tb_csu.py`, `README.md`, `IMPLEMENTATION_LOG.md`.  
- **Done:** all steps complete; gaps closed or waived; TB green — see **`step10.md`** and **`csu_implementation_requirements.md` § below.

---

## Part II — Ten-step summary (detail lives in `stepN.md`)

| Step | Document | One-line result |
|------|----------|-----------------|
| 1 | `step1.md` | V5 primary; `eager=True` bring-up; refs RegisterFile + BypassUnit. |
| 2 | `step2.md` + `requirement_sources.md` | Enumerate SRC-01…08; extraction workflow. |
| 3 | `step3.md` + `port_list.md` + `feature_list.md` | Ports/widths + F-001… baseline features. |
| 4 | `step4.md` + `function_list.md` | Imperative `csu_main_cycle` decomposition. |
| 5 | `step5.md` + **`cycle_budget.md`** | Pipeline S0–S3；**明确 occurrence 段数与 `domain.next()` 次数**；Inc-0 与实现交叉引用。 |
| 6 | `step6.md` | V5 pseudocode skeleton；**实现须满足 `cycle_budget.md` 与 `emit_csu_mlir()` 契约**。 |
| 7 | `step7.md` + `traceability.md` | Matrices + G-xx gaps. |
| 8 | `step8.md` + `test_list.md` | T-001…T-014 + SYS scenarios. |
| 9 | `step9.md` + `incremental_plan.md` | Inc-0…Inc-9 backlog. |
| 10 | `step10.md` + `system_test_spec.md` | System validation + sign-off. |

---

## Definition of done (project)

1. `step1.md`–`step10.md` completed per checklists.  
2. `traceability.md` §4 gaps empty or waived.  
3. `csu.py` / `tb_csu.py` match milestone; `README.md` has run instructions.  
4. Compiler/IR changes obey `AGENTS.md`.

---

**Copyright © 2024–2026 PyCircuit Contributors (methodology); CSU vendor specs remain property of their respective holders.**
