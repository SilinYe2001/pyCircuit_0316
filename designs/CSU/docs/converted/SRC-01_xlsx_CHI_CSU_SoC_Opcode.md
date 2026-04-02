# SRC-01 — XLSX sheet `CHI CSU_SoC_Opcode`

**Source:** `CSU 接口Protocol_辅助设计输入.xlsx`  
**Generated:** 2026-04-01  
**Tool:** `designs/CSU/scripts/export_specs_to_md.py` (openpyxl)

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| REQ_OPCODE[6:0] | Transaction Type | P HC supports（950） |  | RESP_OPCODE[4:0] | Transaction Type | supports(TX) |
| 0x00 | ReqLCrdReturn | Yes |  | 0x00 | RespLCrdReturn | Yes |
| 0x01 | ReadShared | No |  | 0x01 | SnpResp | Yes |
| 0x02 | ReadClean | Yes |  | 0x02 | CompAck | Yes |
| 0x03 | ReadOnce | Yes |  | 0x03 | RetryAck | No |
| 0x04 | ReadNoSnp | Yes |  | 0x04 | Comp | No |
| 0x05 | PCrdReturn | No |  | 0x05 | CompDBIDResp | No |
| 0x06 | Reserved | Reserved |  | 0x06 | DBIDResp | No |
| 0x07 | ReadUnique | Yes |  | 0x07 | PCrdGrant | No |
| 0x08 | CleanShared | Yes |  | 0x08 | ReadReceipt | No |
| 0x09 | CleanInvalid | Yes |  | 0x09 | SnpRespFwded | No |
| 0x0A | MakeInvalid | No |  | 0x0A | TagMatch | No |
| 0x0B | CleanUnique | Yes(950发不出来) |  | 0x0B | RespSepData | No |
| 0x0C | MakeUnique | Yes |  | 0x0C | Persist | No |
| 0x0D | Evict | Yes |  | 0x0D | CompPersist | No |
| 0x0E | Reserved (EOBarrier) | Reserved |  | 0x0E | DBIDRespOrd | No |
| 0x0F | Reserved (ECBarrier) | Reserved |  | 0x0F | Reserved | Reserved |
| 0x10 | Reserved | Reserved |  | 0x10 | StashDone | No |
| 0x11 | ReadNoSnpSep | No |  | 0x11 | CompStashDone | No |
| 0x12 | Reserved | Reserved |  | 0x12 | Reserved | Reserved |
| 0x13 | CleanSharedPersistSep | No |  | 0x13 | Reserved | Reserved |
| 0x14 | DVMOp | Yes |  | 0x14 | CompCMO | No |
| 0x15 | WriteEvictFull | Yes |  | 0x15~0x1F | Reserved | Reserved |
| 0x16 | Reserved (WriteCleanPtl) | Reserved |  |  |  |  |
| 0x17 | WriteCleanFull | Yes |  |  |  |  |
| 0x18 | WriteUniquePtl | No |  | RESP_OPCODE[4:0] | Transaction Type | supports(RX) |
| 0x19 | WriteUniqueFull | Yes |  | 0x00 | RespLCrdReturn | Yes |
| 0x1A | WriteBackPtl | No |  | 0x01 | SnpResp | No |
| 0x1B | WriteBackFull | Yes |  | 0x02 | CompAck | No |
| 0x1C | WriteNoSnpPtl | Yes |  | 0x03 | RetryAck | Yes |
| 0x1D | WriteNoSnpFull | Yes |  | 0x04 | Comp | Yes |
| 0x1E | Reserved | Reserved |  | 0x05 | CompDBIDResp | Yes |
| 0x1F | Reserved | Reserved |  | 0x06 | DBIDResp | Yes |
| 0x20 | WriteUniqueFullStash | No |  | 0x07 | PCrdGrant | Yes |
| 0x21 | WriteUniquePtlStash | No |  | 0x08 | ReadReceipt | Yes |
| 0x22 | StashOnceShared | No |  | 0x09 | SnpRespFwded | No |
| 0x23 | StashOnceUnique | No |  | 0x0A | TagMatch | No |
| 0x24 | ReadOnceCleanInvalid | No |  | 0x0B | RespSepData | Yes |
| 0x25 | ReadOnceMakeInvalid | No |  | 0x0C | Persist | No |
| 0x26 | ReadNotSharedDirty | Yes |  | 0x0D | CompPersist | No |
| 0x27 | CleanSharedPersist | Yes |  | 0x0E | DBIDRespOrd | No |
| 0x28-0x2F | AtomicStore | No |  | 0x0F | Reserved | Reserved |
| 0x30-0x37 | AtomicLoad | No |  | 0x10 | StashDone | No |
| 0x38 | AtomicSwap | No |  | 0x11 | CompStashDone | No |
| 0x39 | AtomicCompare | No |  | 0x12 | Reserved | Reserved |
| 0x3A | PrefetchTgt | No |  | 0x13 | Reserved | Reserved |
| 0x3B-0x3F | Reserved | Reserved |  | 0x14 | CompCMO | Yes |
| 0x40 | Reserved | Reserved |  | 0x1b | CompDBIDRespCMO | Yes |
| 0x41 | MakeReadUnique | Yes |  | 0x15~0x1F | Reserved | Reserved |
| 0x42 | WriteEvictOrEvict | Yes |  |  |  |  |
| 0x43 | WriteUniqueZero | Yes |  | DATA_OPCODE[3:0] | Transaction Type | supports(TX) |
| 0x44 | WriteNoSnpZero | Yes |  | 0x00 | DataLCrdReturn | Yes |
| 0x45 | Reserved | Reserved |  | 0x01 | SnpRespData | Yes |
| 0x46 | Reserved | Reserved |  | 0x02 | CopyBackWrData | Yes |
| 0x47 | StashOnceSepShared | No |  | 0x03 | NonCopyBackWrData | Yes |
| 0x48 | StashOnceSepUnique | No |  | 0x04 | CompData | No |
| 0x49 | Reserved | Reserved |  | 0x05 | SnpRespDataPtl | No |
| 0x4A | Reserved | Reserved |  | 0x06 | SnpRespDataFwded | No |
| 0x4B | Reserved | Reserved |  | 0x07 | WriteDataCancel | No |
| 0x4C | ReadPreferUnique | No |  | 0x08 | Reserved | Reserved |
| 0x4D | Reserved | Reserved |  | 0x09 | Reserved | Reserved |
| 0x4E | WriteNoSnpDef | Yes |  | 0x0A | Reserved | Reserved |
| 0x4F | Reserved | Reserved |  | 0x0B | DataSepResp | No |
| 0x50 | WriteNoSnpFullCleanSh | No |  | 0x0C | NCBWrDataCompAck | No |
| 0x51 | WriteNoSnpFullCleanInv | No |  | 0x0D | Reserved | Reserved |
| 0x52 | WriteNoSnpFullCleanShPerSep | No |  | 0x0E | Reserved | Reserved |
| 0x53 | Reserved | Reserved |  | 0x0F | Reserved | Reserved |
| 0x54 | WriteUniqueFullCleanSh | No |  |  |  |  |
| 0x55 | Reserved | Reserved |  | DATA_OPCODE[3:0] | Transaction Type | supports(RX) |
| 0x56 | WriteUniqueFullCleanShPerSep | No |  | 0x00 | DataLCrdReturn | Yes |
| 0x57 | Reserved | Reserved |  | 0x01 | SnpRespData | No |
| 0x58 | WriteBackFullCleanSh | No |  | 0x02 | CopyBackWrData | No |
| 0x59 | WriteBackFullCleanInv | Yes |  | 0x03 | NonCopyBackWrData | No |
| 0x5a | WriteBackFullCleanShPerSep | No |  | 0x04 | CompData | Yes |
| 0x5b | Reserved | Reserved |  | 0x05 | SnpRespDataPtl | No |
| 0x5c | WriteCleanFullCleanSh | Yes |  | 0x06 | SnpRespDataFwded | No |
| 0x5d | Reserved | Reserved |  | 0x07 | WriteDataCancel | No |
| 0x5e | WriteCleanFullCleanShPerSep | No |  | 0x08 | Reserved | Reserved |
| 0x5f | Reserved | Reserved |  | 0x09 | Reserved | Reserved |
| 0x60 | WriteNoSnpPtlCleanSh | No |  | 0x0A | Reserved | Reserved |
| 0x61 | WriteNoSnpPtlCleanInv | No |  | 0x0B | DataSepResp | Yes |
| 0x62 | WriteNoSnpPtlCleanShPerSep | No |  | 0x0C | NCBWrDataCompAck | No |
| 0x63 | Reserved | Reserved |  | 0x0D | Reserved | Reserved |
| 0x64 | WriteUniquePtlCleanSh | No |  | 0x0E | Reserved | Reserved |
| 0x65 | Reserved | Reserved |  | 0x0F | Reserved | Reserved |
| 0x66 | WriteUniquePtlCleanShPerSep | No |  |  |  |  |
| 0x67 | Reserved | Reserved |  |  |  |  |
|  |  |  |  | SNP_OPCODE[4:0] | Transaction Type | supports |
|  |  |  |  | 0x00 | SnpLCrdReturn | Yes |
|  |  |  |  | 0x01 | SnpShared | No |
|  |  |  |  | 0x02 | SnpClean | Yes |
|  |  |  |  | 0x03 | SnpOnce | Yes |
|  |  |  |  | 0x04 | SnpNotSharedDirty | Yes |
|  |  |  |  | 0x05 | SnpUniqueStash | No |
|  |  |  |  | 0x06 | SnpMakeInvalidStash | No |
|  |  |  |  | 0x07 | SnpUnique | Yes |
|  |  |  |  | 0x08 | SnpCleanShared | Yes |
|  |  |  |  | 0x09 | SnpCleanInvalid | Yes |
|  |  |  |  | 0x0A | SnpMakeInvalid | Yes |
|  |  |  |  | 0x0B | SnpStashUnique | No |
|  |  |  |  | 0x0C | SnpStashShared | No |
|  |  |  |  | 0x0D | SnpDVMOp | Yes |
|  |  |  |  | 0x0E | Reserved | Reserved |
|  |  |  |  | 0x0F | Reserved | Reserved |
|  |  |  |  | 0x10 | SnpQuery | No |
|  |  |  |  | 0x11 | SnpSharedFwd | No |
|  |  |  |  | 0x12 | SnpCleanFwd | No |
|  |  |  |  | 0x13 | SnpOnceFwd | No |
|  |  |  |  | 0x14 | SnpNotSharedDirtyFwd | No |
|  |  |  |  | 0x15 | SnpPreferUnique | No |
|  |  |  |  | 0x16 | SnpPreferUniqueFwd | No |
|  |  |  |  | 0x17 | SnpUniqueFwd | No |
|  |  |  |  | 0x18~0x1F | Reserved | Reserved |
