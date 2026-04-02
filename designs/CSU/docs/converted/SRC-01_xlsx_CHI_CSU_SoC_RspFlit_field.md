# SRC-01 — XLSX sheet `CHI CSU_SoC_RspFlit field`

**Source:** `CSU 接口Protocol_辅助设计输入.xlsx`  
**Generated:** 2026-04-01  
**Tool:** `designs/CSU/scripts/export_specs_to_md.py` (openpyxl)

| TXRSPFLIT |  |  |  |
| --- | --- | --- | --- |
| Field | Field width | END BIT | START BIT |
| QoS | 4 | 3 | 0 |
| TgtID | 6 | 5 | 0 |
| SrcID | 0 | 5 | 6 |
| TxnID | 8 | 13 | 6 |
| Opcode | 5 | 18 | 14 |
| RespErr | 2 | 20 | 19 |
| Resp | 3 | 23 | 21 |
| FwdState | 3 | 26 | 24 |
| DataPull | 0 | 26 | 27 |
| Cbusy | 3 | 29 | 27 |
| DBID | 8 | 34 | 27 |
| {4b0, | 0 | 34 | 35 |
| GroupIDExt | 0 | 34 | 35 |
| LPID} | 0 | 34 | 35 |
| PCrdType | 4 | 38 | 35 |
| TagOp | 0 | 38 | 39 |
| TraceTag | 1 | 35 | 35 |
| HitMInfo | 1 | 24 | 24 |
|  |  |  | 25 |
| RXRSPFLIT |  |  |  |
| Field | Field width | END BIT | START BIT |
| QoS | 4 | 3 | 0 |
| TgtID | 6 | 5 | 0 |
| SrcID | 6 | 5 | 0 |
| TxnID | 8 | 13 | 6 |
| Opcode | 5 | 18 | 14 |
| RespErr | 2 | 20 | 19 |
| Resp | 3 | 23 | 21 |
| FwdState | 3 | 26 | 24 |
| DataPull | 0 | 26 | 27 |
| Cbusy | 3 | 29 | 27 |
| DBID | 8 | 34 | 27 |
| {4b0, | 0 | 34 | 35 |
| GroupIDExt | 0 | 34 | 35 |
| LPID} | 0 | 34 | 35 |
| PCrdType | 4 | 38 | 35 |
| TagOp | 0 | 38 | 39 |
| TraceTag | 1 | 39 | 39 |
| HitInfo_Modified | 1 | 40 | 40 |
| HitInfo_Hit | 1 | 41 | 41 |
|  |  |  | 42 |
