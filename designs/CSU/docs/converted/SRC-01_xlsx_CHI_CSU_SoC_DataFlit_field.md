# SRC-01 — XLSX sheet `CHI CSU_SoC_DataFlit field`

**Source:** `CSU 接口Protocol_辅助设计输入.xlsx`  
**Generated:** 2026-04-01  
**Tool:** `designs/CSU/scripts/export_specs_to_md.py` (openpyxl)

| RXDATFLIT |  |  |  |
| --- | --- | --- | --- |
| Field | Field width | END BIT | START BIT |
| QoS | 4 | 3 | 0 |
| TgtID | 6 | 5 | 0 |
| SrcID | 6 | 11 | 6 |
| TxnID | 8 | 7 | 0 |
| HomeNID | 6 | 13 | 8 |
| Opcode | 4 | 17 | 14 |
| RespErr | 2 | 19 | 18 |
| Resp | 3 | 22 | 20 |
| FwdState | 3 | 25 | 23 |
| DataPull | 0 | 25 | 26 |
| DataSource | 0 | 25 | 26 |
| Cbusy | 0 | 25 | 26 |
| DBID | 8 | 33 | 26 |
| CCID | 2 | 35 | 34 |
| DataID | 2 | 37 | 36 |
| TagOp | 0 | 37 | 38 |
| Tag | 0 | 37 | 38 |
| TU | 0 | 37 | 38 |
| TraceTag | 1 | 38 | 38 |
| RSVDC | 0 | 38 | 39 |
| BE | 32 | 70 | 39 |
| Data | 256 | 294 | 39 |
| DataCheck | 0 | 294 | 295 |
| Poison | 1 | 295 | 295 |
| HitMInfo | 1 | 295 | 295 |
|  |  |  | 296 |
| TXDATFLIT（HC） |  |  |  |
| Field | Field width | END BIT | START BIT |
| QoS | 4 | 3 | 0 |
| TgtID | 6 | 5 | 0 |
| SrcID | 0 | 5 | 6 |
| TxnID | 8 | 13 | 6 |
| HomeNID | 4 | 17 | 14 |
| {2‘b00 | 2 | 19 | 18 |
| PBHA[3:0]} | 4 | 23 | 20 |
| Opcode | 4 | 21 | 18 |
| RespErr | 2 | 23 | 22 |
| Resp | 3 | 26 | 24 |
| FwdState | 3 | 29 | 27 |
| DataPull | 0 | 29 | 30 |
| DataSource | 0 | 29 | 30 |
| Cbusy | 0 | 29 | 30 |
| DBID | 8 | 37 | 30 |
| CCID | 2 | 28 | 27 |
| DataID | 2 | 30 | 29 |
| TagOp | 0 | 30 | 31 |
| Tag | 0 | 30 | 31 |
| TU | 0 | 30 | 31 |
| TraceTag | 1 | 29 | 29 |
| RSVDC | 0 | 29 | 30 |
| BE | 64 | 92 | 29 |
| Data | 512 | 604 | 93 |
| DataCheck | 0 | 604 | 605 |
| Poison | 1 | 605 | 605 |
| Datavld | 2 | 606 | 605 |
| Mstx | 1 | 607 | 607 |
|  |  |  | 608 |
| TXDATFLIT（LIT CLUSTER） |  |  |  |
| Field | Field width | END BIT | START BIT |
| QoS | 4 | 3 | 0 |
| TgtID | 6 | 5 | 0 |
| SrcID | 0 | 5 | 6 |
| TxnID | 8 | 13 | 6 |
| HomeNID | 4 | 17 | 14 |
| {2‘b00 | 2 | 19 | 18 |
| PBHA[3:0]} | 4 | 23 | 20 |
| Opcode | 4 | 21 | 18 |
| RespErr | 2 | 23 | 22 |
| Resp | 3 | 26 | 24 |
| FwdState | 3 | 29 | 27 |
| DataPull | 0 | 29 | 30 |
| DataSource | 0 | 29 | 30 |
| Cbusy | 0 | 29 | 30 |
| DBID | 8 | 37 | 30 |
| CCID | 2 | 28 | 27 |
| DataID | 2 | 30 | 29 |
| TagOp | 0 | 30 | 31 |
| Tag | 0 | 30 | 31 |
| TU | 0 | 30 | 31 |
| TraceTag | 1 | 29 | 29 |
| RSVDC | 0 | 29 | 30 |
| BE | 32 | 62 | 31 |
| Data | 256 | 318 | 63 |
| DataCheck | 0 | 318 | 319 |
| Poison | 1 | 319 | 319 |
|  |  |  | 319 |
