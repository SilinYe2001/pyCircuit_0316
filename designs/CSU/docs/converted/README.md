# Converted CSU specifications (Markdown)

Binary sources under `designs/CSU/docs/` are exported here so agents and text tools can search and cite them.

| Artifact | Original | Converted output |
|----------|----------|------------------|
| SRC-01 | `CSU 接口Protocol_辅助设计输入.xlsx` | `SRC-01_xlsx_*.md` (6 sheets) |
| SRC-07 | `LinxCore950 CSU Design Specification-AI辅助设计输入.docx` | `SRC-07_linxcore950_csu_design_spec.md` + `SRC-07_media/` |
| SRC-08 | `IHI0050H_amba_chi_architecture_spec.pdf` | `SRC-08_chi_architecture_spec_extract.md` (first pages only) |

**Regenerate:** `python3 designs/CSU/scripts/export_specs_to_md.py` from repo root.

**DOCX export:** OK (pandoc)  
**PDF extract:** OK (pypdf)

Figures in DOCX are referenced from `SRC-07_media/`; equation-heavy PDF pages may have imperfect text layout — always keep the original PDF for sign-off.
