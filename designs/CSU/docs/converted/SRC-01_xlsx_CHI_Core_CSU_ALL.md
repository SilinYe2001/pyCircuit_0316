# SRC-01 — XLSX sheet `CHI_Core_CSU_ALL`

**Source:** `CSU 接口Protocol_辅助设计输入.xlsx`  
**Generated:** 2026-04-01  
**Tool:** `designs/CSU/scripts/export_specs_to_md.py` (openpyxl)

| TXREQ |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | CSU视角 |  |  |  |  |  |  |  |  |  |
|  | width | MSB | LSB |  |  |  |  |  |  |  |
| REQFLIT_QOS | 4 | 3 | 0 |  |  |  |  |  |  |  |
| REQFLIT_TGTID |  |  |  |  |  |  |  |  |  |  |
| REQFLIT_SRCID | 6 | 9 | 4 |  |  |  |  |  |  |  |
| REQFLIT_TXNID | 10 | 19 | 10 |  |  |  |  |  |  |  |
| REQFLIT_ENDIAN | 1 | 20 | 20 |  |  |  |  |  |  |  |
| REQFLIT_OPCODE | 7 | 27 | 21 |  |  |  |  |  |  |  |
| REQFLIT_SIZE | 3 | 30 | 28 |  |  |  |  |  |  |  |
| REQFLIT_ADDR | 36 | 66 | 31 |  |  |  |  |  |  |  |
| REQFLIT_NS | 1 | 67 | 67 |  |  |  |  |  |  |  |
| REQFLIT_NSE |  |  |  |  |  |  |  |  |  |  |
| REQFLIT_ORDER | 2 | 69 | 68 |  |  |  |  |  |  |  |
| REQFLIT_MEMATTR | 4 | 73 | 70 |  |  |  |  |  |  |  |
| REQFLIT_SNPATTR | 1 | 74 | 74 |  |  |  |  |  |  |  |
| REQFLIT_LPID | 2 | 76 | 75 |  |  |  |  |  |  |  |
| REQFLIT_GROUPIDEXT | 1 | 77 | 77 |  |  |  |  |  |  |  |
| REQFLIT_EXCL/SNOOPME | 1 | 78 | 78 |  |  |  |  |  |  |  |
| REQFLIT_EXPCOMPACK | 1 | 79 | 79 |  |  |  |  |  |  |  |
| REQFLIT_TRACETAG | 1 | 80 | 80 |  |  |  |  |  |  |  |
| REQFLIT_MPAM | 4 | 84 | 81 |  |  |  |  |  |  |  |
| REQFLIT_PBHA | 4 | 88 | 85 |  |  |  |  |  |  |  |
| REQFLIT_RSVDC_ELYDQ_VLD | 1 | 89 | 89 |  |  |  |  |  |  |  |
| REQFLIT_RSVDC_FLITTYPE | 4 | 93 | 90 |  |  |  |  |  |  |  |
| REQFLIT_RSVDC_HOTDATA | 1 | 94 | 94 |  |  |  |  |  |  |  |
| REQFLIT_RSVDC_128HINT | 1 | 95 | 95 |  |  |  |  |  |  |  |
| REQFLIT_RSVDC_TGTL3 |  |  |  |  |  |  |  |  |  |  |
| REQFLIT_RSVDC_NCCMO | 1 | 96 | 96 |  |  |  |  |  |  |  |
| REQFLIT_W | 97 | 96 | 0 |  |  |  |  |  |  |  |
| TXREQ_PEND |  |  |  |  |  |  |  |  |  |  |
|  | HC视角 |  |  |  |  |  |  |  |  |  |
|  | width | MSB | LSB |  |  |  |  |  |  |  |
| REQPENDFLIT_PA7 | 2 | 1 | 0 |  |  |  |  |  |  |  |
| TXRSP |  |  |  |  |  |  |  |  |  |  |
|  | HC视角 |  |  |  |  |  |  |  |  |  |
|  | width | MSB | LSB |  |  |  |  |  |  |  |
| RSPFLIT_TGTID | 5 | 4 | 0 |  |  |  |  |  |  |  |
| RSPFLIT_SRCID | 5 | 9 | 5 |  |  |  |  |  |  |  |
| RSPFLIT_TXNID | 10 | 19 | 10 |  |  |  |  |  |  |  |
| RSPFLIT_OPCODE | 4 | 23 | 20 |  |  |  |  |  |  |  |
| RSPFLIT_RESPERR | 2 | 25 | 24 |  |  |  |  |  |  |  |
| RSPFLIT_RESP | 3 | 28 | 26 |  |  |  |  |  |  |  |
| RSPFLIT_FWDSTATE/DATAPUL |  |  |  |  |  |  |  |  |  |  |
| RSPFLIT_TRACETAG |  |  |  |  |  |  |  |  |  |  |
| RSPFLIT_HITMINFO | 1 | 29 | 29 |  |  |  |  |  |  |  |
| RSPFLIT_W | 30 | 29 | 0 |  |  |  |  |  |  |  |
| RXRSP |  |  |  |  |  |  |  |  |  |  |
|  | HC视角 |  |  |  |  |  |  |  |  |  |
|  | width | MSB | LSB |  |  |  |  |  |  |  |
| RSPFLIT_SRCID | 5 | 4 | 0 |  |  |  |  |  |  |  |
| RSPFLIT_TXNID | 10 | 14 | 5 |  |  |  |  |  |  |  |
| RSPFLIT_OPCODE | 5 | 19 | 15 |  |  |  |  |  |  |  |
| RSPFLIT_RESPERR | 2 | 21 | 20 |  |  |  |  |  |  |  |
| RSPFLIT_RESP | 3 | 24 | 22 |  |  |  |  |  |  |  |
| RSPFLIT_DBID | 10 | 34 | 25 |  |  |  |  |  |  |  |
| RSPFLIT_TRACETAG | 1 | 35 | 35 |  |  |  |  |  |  |  |
| RSPFLIT_RSVDC_ALIAS | 1 | 36 | 36 |  |  |  |  |  |  |  |
| RSPFLIT_HITINFO_MOD | 1 | 37 | 37 |  |  |  |  |  |  |  |
| RSPFLIT_HITINFO_FAR/HIT | 1 | 38 | 38 |  |  |  |  |  |  |  |
| RSPFLIT_HITINFO_NEAR | 1 | 39 | 39 |  |  |  |  |  |  |  |
| RSPFLIT_RSVDC_REFILL_WR | 1 | 40 | 40 |  |  |  |  |  |  |  |
| RSPFLIT_RSVDC_REFILL_PRFM | 1 | 41 | 41 |  |  |  |  |  |  |  |
| RSPFLIT_W | 42 | 41 | 0 |  |  |  |  |  |  |  |
| TXDAT |  |  |  |  |  |  |  |  |  |  |
|  | HC视角 |  |  |  |  |  |  |  |  |  |
|  | width | MSB | LSB |  |  |  |  |  |  |  |
| DATFLIT_TGTID | 5 | 4 | 0 |  |  |  |  |  |  |  |
| DATFLIT_SRCID | 5 | 9 | 5 |  |  |  |  |  |  |  |
| DATFLIT_TXNID | 10 | 19 | 10 |  |  |  |  |  |  |  |
| DATFLIT_HNID |  |  |  |  |  |  |  |  |  |  |
| DATFLIT_PBHA | 4 | 23 | 20 |  |  |  |  |  |  |  |
| DATFLIT_OPCODE | 4 | 27 | 24 |  |  |  |  |  |  |  |
| DATFLIT_RESP | 3 | 30 | 28 |  |  |  |  |  |  |  |
| DATFLIT_FWDSTATE/DATASOURCE |  |  |  |  |  |  |  |  |  |  |
| DATFLIT_DBID |  |  |  |  |  |  |  |  |  |  |
| DATFLIT_CCID |  |  |  |  |  |  |  |  |  |  |
| DATFLIT_DATAID |  |  |  |  |  |  |  |  |  |  |
| DATFLIT_TRACETAG |  |  |  |  |  |  |  |  |  |  |
| DATFLIT_BE | 64 | 94 | 31 |  |  |  |  |  |  |  |
| DATFLIT_DATA | 512 | 606 | 95 |  |  |  |  |  |  |  |
| DATFLIT_POISON | 8 | 614 | 607 |  |  |  |  |  |  |  |
| DATFLIT_W | 615 | 614 | 0 |  |  |  |  |  |  |  |
| RXDAT |  |  |  |  |  |  |  |  |  |  |
|  | HC视角 |  |  |  |  |  |  |  |  |  |
|  | width | MSB | LSB |  |  |  |  |  |  |  |
| DATFLIT_TXNID | 10 | 9 | 0 |  |  |  |  |  |  |  |
| DATFLIT_HNID | 5 | 14 | 10 |  |  |  |  |  |  |  |
| DATFLIT_OPCODE | 4 | 18 | 15 |  |  |  |  |  |  |  |
| DATFLIT_RESPERR | 2 | 20 | 19 |  |  |  |  |  |  |  |
| DATFLIT_RESP | 3 | 23 | 21 |  |  |  |  |  |  |  |
| DATFLIT_DATASOURCE/FWDSTATE | 3 | 26 | 24 |  |  |  |  |  |  |  |
| DATFLIT_DBID | 10 | 36 | 27 |  |  |  |  |  |  |  |
| DATFLIT_CCID | 2 | 38 | 37 |  |  |  |  |  |  |  |
| DATFLIT_DATAID | 0 | 38 | 39 |  |  |  |  |  |  |  |
| DATFLIT_TRACETAG/ | 1 | 39 | 39 |  |  |  |  |  |  |  |
| DATFLIT_ECC_VLD | 1 | 40 | 40 |  |  |  |  |  |  |  |
| DATFLIT_ECC | 20 | 60 | 41 |  |  |  |  |  |  |  |
| DATFLIT_DATA | 512 | 572 | 61 |  |  |  |  |  |  |  |
| DATFLIT_POISON | 8 | 580 | 573 |  |  |  |  |  |  |  |
| DATFLIT_HITMINFO | 1 | 581 | 581 |  |  |  |  |  |  |  |
| RSPFLIT_RSVDC_CHL_VLD | 1 | 582 | 582 |  |  |  |  |  |  |  |
| RSPFLIT_RSVDC_SEC_VLD | 1 | 583 | 583 |  |  |  |  |  |  |  |
| DATFLIT_W | 584 | 583 | 0 |  |  |  |  |  |  |  |
| RXWKUP |  |  |  |  |  |  |  |  |  |  |
|  | HC视角 |  |  |  |  |  |  |  |  |  |
|  | width | MSB | LSB |  |  |  |  |  |  |  |
| WKUPFLIT_TXNID | 10 | 9 | 0 |  |  |  |  |  |  |  |
| WKUPFLIT_CHL | 1 | 10 | 10 |  |  |  |  |  |  |  |
| WKUPFLIT_CHL_PA5 | 1 | 11 | 11 |  |  |  |  |  |  |  |
| WKUPFLIT_RESENT | 1 | 12 | 12 |  |  |  |  |  |  |  |
| WKUPFLIT_STAGE | 2 | 14 | 13 |  |  |  |  |  |  |  |
| WKUPFLIT_PIPE | 2 | 16 | 15 |  |  |  |  |  |  |  |
| WKUPFLIT_PIPE_HINT | 1 | 17 | 17 |  |  |  |  |  |  |  |
| WKUPFLIT_W | 18 | 17 | 0 |  |  |  |  |  |  |  |
| RXERR |  |  |  |  |  |  |  |  |  |  |
|  | HC视角 |  |  |  |  |  |  |  |  |  |
|  | width | MSB | LSB |  |  |  |  |  |  |  |
| ERR_FLIT_INDICATE | 1 | 0 | 0 |  |  |  |  |  |  |  |
| ERR_FLIT_BITERR | 1 | 1 | 1 |  |  |  |  |  |  |  |
| RXFILL |  |  |  |  |  |  |  |  |  |  |
|  | HC视角 |  |  |  |  |  |  |  |  |  |
|  | width | MSB | LSB |  |  |  |  |  |  |  |
| FILLFLIT_RESP | 3 | 2 | 0 |  |  |  |  |  |  |  |
| FILLFLIT_W | 3 | 2 | 0 |  |  |  |  |  |  |  |
| RXSNP |  |  |  |  |  |  |  |  |  |  |
|  | HC视角 |  |  |  |  |  |  |  |  |  |
|  | width | MSB | LSB |  |  |  |  |  |  |  |
| SNPFLIT_SRCID | 5 | 4 | 0 |  |  |  |  |  |  |  |
| SNPFLIT_TXNID | 10 | 14 | 5 |  |  |  |  |  |  |  |
| SNPFLIT_FWDNID | 5 | 19 | 15 |  |  |  |  |  |  |  |
| SNPFLIT_VMIDEXT/FWDTXNID | 10 | 29 | 20 |  |  |  |  |  |  |  |
| SNPFLIT_OPCODE | 5 | 34 | 30 |  |  |  |  |  |  |  |
| SNPFLIT_ADDR | 33 | 67 | 35 |  |  |  |  |  |  |  |
| SNPFLIT_NS | 1 | 68 | 68 |  |  |  |  |  |  |  |
| SNPFLIT_NSE |  |  |  |  |  |  |  |  |  |  |
| SNPFLIT_RETTOSRC |  |  |  |  |  |  |  |  |  |  |
| SNPFLIT_TRACETAG |  |  |  |  |  |  |  |  |  |  |
| SNPFLIT_ALIAS | 1 | 69 | 69 |  |  |  |  |  |  |  |
| SNPFLIT_ALIAS_TXNID | 10 | 79 | 70 |  |  |  |  |  |  |  |
| SNPFLIT_SNP_TO_LSU | 1 | 80 | 80 |  |  |  |  |  |  |  |
| SNPFLIT_SNP_NEED_NUKE | 1 | 81 | 81 |  |  |  |  |  |  |  |
| SNPFLIT_W | 82 | 81 | 0 | CompCMO | Comp |  | miss info | CompStashDone |  |  |
|  |  |  |  |  | write nt | nc/dev write |  | pfl3 | pfsc miss l3 | pfsc hit l3 |
|  |  |  |  | 0 | 0 | 0 | 0 | 1 | 1 | 1 |
| RXRSP1(用作CompCMO,stash_done streaming等性能特性) |  |  |  | rsv | HitInfo_NEAR | rsv | txnid | rsv | rsv | rsv |
|  | L2内部 |  |  | rsv | HitInfo_FAR | rsv |  | rsv | rsv | rsv |
|  | width | range |  | rsv | HitInfo_Modified | rsv |  | rsv | rsv | rsv |
| RSP1FLIT_BIT0 | 1 | 0 | 0 | rsv | rsv | rsv |  | rsv | rsv | rsv |
| RSP1FLIT_BIT1 | 1 | 1 | 1 | rsv | rsv | rsv |  | rsv | rsv | rsv |
| RSP1FLIT_BIT2 | 2 | 3 | 2 | rsv | rsv | rsv |  | rsv | rsv | rsv |
| RSP1FLIT_BIT3 |  |  |  | rsv | rsv | rsv |  | tid | tid | tid |
| RSP1FLIT_BIT4_5 |  |  |  | rsv | rsv | rsv |  |  |  |  |
| RSP1FLIT_BIT6_8 |  |  |  | rsv | rsv | rsv |  | 0 | 1 | 1 |
| RSP1FLIT_BIT9 |  |  |  | rsv | rsv | rsv |  | homeID | homeID | homeID |
| RSP1FLIT_BIT10_17 |  |  |  | rsv | rsv | rsv | rsv |  |  |  |
| RSP1FLIT_BIT18 |  |  |  | 2'b00 | 2'b01 | 2'b10 | 2'b11 |  |  |  |
| RSP1FLIT_W | 4 | 3 | 0 |  |  |  |  | l3_utils | l3_utils | l3_utils |
|  |  |  |  | resp error | resp error | resp error | rsv |  |  |  |
|  |  |  |  |  |  |  | rsv | hit/miss | sc hit/miss | hit/miss |
|  |  |  |  | color | color | color | color |  |  |  |
|  |  |  |  | tid | tid | tid | tid | pftype |  | 0 |
|  |  |  |  |  |  |  |  |  | 1: from sc | 0: from l3/hc |
