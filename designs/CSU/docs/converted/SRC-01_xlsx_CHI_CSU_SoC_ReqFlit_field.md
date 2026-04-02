# SRC-01 — XLSX sheet `CHI CSU_SoC_ReqFlit field`

**Source:** `CSU 接口Protocol_辅助设计输入.xlsx`  
**Generated:** 2026-04-01  
**Tool:** `designs/CSU/scripts/export_specs_to_md.py` (openpyxl)

| REQFLIT |  |  |  |
| --- | --- | --- | --- |
| Field | Field width | END BIT | START BIT |
| QoS | 4 | 3 | 0 |
| TgtID | 6 | 9 | 4 |
| SrcID | 0 | 3 | 4 |
| TxnID | 8 | 11 | 4 |
| ReturnNID | 6 | 17 | 12 |
| StashNID | 0 | 17 | 18 |
| Endian | 1 | 12 | 12 |
| StashNIDValid | 0 | 12 | 13 |
| deep | 0 | 12 | 13 |
| ReturnTxnID | 8 | 20 | 13 |
| {0b00, | 0 | 20 | 21 |
| StashLPIDValid, | 0 | 20 | 21 |
| StashLPID[4:0]} | 0 | 20 | 21 |
| Opcode | 7 | 18 | 12 |
| Size | 3 | 21 | 19 |
| Addr | 36 | 57 | 22 |
| NS | 1 | 58 | 58 |
| LikelyShared | 1 | 59 | 59 |
| AllowRetry | 1 | 59 | 59 |
| Order | 2 | 61 | 60 |
| PCrdType | 4 | 65 | 62 |
| MemAttr | 4 | 69 | 66 |
| SnpAttr | 1 | 70 | 70 |
| DoNotDWT | 0 | 70 | 71 |
| LPID | 4 | 74 | 71 |
| PGroupID | 0 | 74 | 75 |
| GroupIDExt | 0 | 74 | 75 |
| Excl | 1 | 75 | 75 |
| SnoopMe | 0 | 75 | 76 |
| ExpCompAck | 1 | 76 | 76 |
| TagOp | 0 | 76 | 77 |
| TraceTag | 1 | 77 | 77 |
| MPAM | 4 | 81 | 78 |
| PBHA | 4 | 85 | 82 |
| RSVDC_pass_dirty/is_dirty | 0 | 85 | 86 |
| RSVDC_is_copyback/migratable | 0 | 85 | 86 |
| RSVDC_to_pp | 1 | 86 | 86 |
| RSVDC_subsource | 0 | 86 | 87 |
| RSVDC_prf | 0 | 86 | 87 |
| RSVDC_trans | 0 | 86 | 87 |
| RSVDC_outer_shareable | 0 | 86 | 87 |
| RSVDC_flittype | 4 | 90 | 87 |
|  |  |  | 91 |
