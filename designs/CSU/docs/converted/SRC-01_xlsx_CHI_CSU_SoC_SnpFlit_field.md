# SRC-01 — XLSX sheet `CHI CSU_SoC_SnpFlit field`

**Source:** `CSU 接口Protocol_辅助设计输入.xlsx`  
**Generated:** 2026-04-01  
**Tool:** `designs/CSU/scripts/export_specs_to_md.py` (openpyxl)

| SNPFLIT |  |  |  |
| --- | --- | --- | --- |
| Field | Field width | END BIT | START BIT |
| QoS | 4 | 3 | 0 |
| SrcID | 6 | 5 | 0 |
| TxnID | 8 | 13 | 6 |
| FwdNID | 6 | 19 | 14 |
| FwdTxnID | 8 | 27 | 20 |
| {0b00, | 0 | 27 | 28 |
| StashLPIDValid, | 0 | 27 | 28 |
| StashLPID[4:0]} | 0 | 27 | 28 |
| {VMIDExt[7:0]} | 0 | #REF! | #REF! |
| Opcode | 5 | 32 | 28 |
| Addr | 33 | 65 | 33 |
| NS | 1 | 66 | 66 |
| DoNotGoToSD | 1 | 67 | 67 |
| DoNotDataPull | 0 | 67 | 68 |
| RetToSrc | 1 | 67 | 67 |
| TraceTag | 1 | 67 | 67 |
| MPAM | 0 | 67 | 68 |
| PBHA | 0 | 67 | 68 |
|  |  |  | 67 |
