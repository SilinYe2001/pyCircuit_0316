# pipeline 划分变体对比（自动产出：balance_report.py）

| 变体 | cap→fire | fire→issue | fire gap | fires | issues | max_logic_depth | reg_bits | wns_min | _v5_bal 寄存器 | _v5_bal bits |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| D0 | 1..4 | 1..5 | 1..4 | 48 | 48 | 47 | 5712 | 465 | 0 | 0 |
| D1 | 1..4 | 1..5 | 1..4 | 48 | 48 | 47 | 5656 | 465 | 0 | 0 |
| D2 | 1..4 | 1..5 | 1..4 | 48 | 48 | 47 | 7909 | 465 | 0 | 0 |
| D3 | 1..4 | 2..2 | 1..4 | 48 | 48 | 26 | 5712 | 486 | 1226 | 10007 |
| D3H | 1..4 | 2..2 | 1..4 | 48 | 48 | 47 | 8420 | 465 | 1314 | 13985 |

## D0

- mirror: `{"variant": "D0", "fires": 48, "issues": 48, "cap_fire_min": 1, "cap_fire_max": 4, "fire_issue_min": 1, "fire_issue_max": 5, "gap_min": 1, "gap_max": 4, "lat_first10": [2, 1, 1, 1, 1, 1, 1, 1, 1, 4], "gaps_first10": [1, 1, 1, 1, 1, 1, 1, 1, 4, 1]}`
- _v5_bal: count=0 bits=0 top10=[]
- per-module compile_stats:

  | module | max_logic_depth | reg_count | reg_bits | wns | tns |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | arbiter | 25 | 1 | 2 | 487 | 0 |
  | assembler_a | 10 | 7 | 60 | 502 | 0 |
  | assembler_amx | 26 | 21 | 389 | 486 | 0 |
  | assembler_b | 18 | 13 | 155 | 494 | 0 |
  | assembler_bmx | 24 | 16 | 381 | 488 | 0 |
  | cand_holder | 5 | 7 | 59 | 507 | 0 |
  | req_sched | 8 | 26 | 4514 | 504 | 0 |
  | tag_checker | 7 | 7 | 152 | 505 | 0 |
  | tb_pd_d0_top | 47 | 0 | 0 | 465 | 0 |

## D1

- mirror: `{"variant": "D1", "fires": 48, "issues": 48, "cap_fire_min": 1, "cap_fire_max": 4, "fire_issue_min": 1, "fire_issue_max": 5, "gap_min": 1, "gap_max": 4, "lat_first10": [1, 1, 1, 1, 1, 1, 1, 1, 1, 4], "gaps_first10": [1, 1, 1, 1, 1, 1, 1, 1, 4, 1]}`
- _v5_bal: count=0 bits=0 top10=[]
- per-module compile_stats:

  | module | max_logic_depth | reg_count | reg_bits | wns | tns |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | arbiter | 25 | 1 | 2 | 487 | 0 |
  | assembler_a | 10 | 7 | 60 | 502 | 0 |
  | assembler_amx | 26 | 21 | 389 | 486 | 0 |
  | assembler_b | 18 | 13 | 155 | 494 | 0 |
  | assembler_bmx | 24 | 16 | 381 | 488 | 0 |
  | cand_holder | 5 | 7 | 59 | 507 | 0 |
  | req_sched | 8 | 26 | 4514 | 504 | 0 |
  | tag_checker_spec | 8 | 5 | 96 | 504 | 0 |
  | tb_pd_d1_top | 47 | 0 | 0 | 465 | 0 |

## D2

- mirror: `{"variant": "D2", "fires": 48, "issues": 48, "cap_fire_min": 1, "cap_fire_max": 4, "fire_issue_min": 1, "fire_issue_max": 5, "gap_min": 1, "gap_max": 4, "lat_first10": [2, 1, 1, 1, 1, 1, 1, 1, 1, 4], "gaps_first10": [1, 1, 1, 1, 1, 1, 1, 1, 4, 1]}`
- _v5_bal: count=0 bits=0 top10=[]
- per-module compile_stats:

  | module | max_logic_depth | reg_count | reg_bits | wns | tns |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | arbiter | 25 | 1 | 2 | 487 | 0 |
  | assembler_a | 10 | 7 | 60 | 502 | 0 |
  | assembler_amx | 26 | 21 | 389 | 486 | 0 |
  | assembler_b | 18 | 13 | 155 | 494 | 0 |
  | assembler_bmx | 24 | 16 | 381 | 488 | 0 |
  | cand_holder | 5 | 7 | 59 | 507 | 0 |
  | payload_snap | 1 | 13 | 2197 | 511 | 0 |
  | req_sched | 8 | 26 | 4514 | 504 | 0 |
  | tag_checker | 7 | 7 | 152 | 505 | 0 |
  | tb_pd_d2_top | 47 | 0 | 0 | 465 | 0 |

## D3

- mirror: `{"variant": "D3", "fires": 48, "issues": 48, "cap_fire_min": 1, "cap_fire_max": 4, "fire_issue_min": 2, "fire_issue_max": 2, "gap_min": 1, "gap_max": 4, "lat_first10": [2, 1, 1, 1, 1, 1, 1, 1, 1, 1], "gaps_first10": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}`
- _v5_bal: count=1226 bits=10007 top10=[('_v5_bal_26', 32), ('_v5_bal_27', 32), ('_v5_bal_28', 32), ('_v5_bal_29', 32), ('_v5_bal_33', 32), ('_v5_bal_34', 32), ('_v5_bal_35', 32), ('_v5_bal_36', 32), ('_v5_bal_40', 32), ('_v5_bal_41', 32)]
- per-module compile_stats:

  | module | max_logic_depth | reg_count | reg_bits | wns | tns |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | arbiter | 25 | 1 | 2 | 487 | 0 |
  | assembler_a | 10 | 7 | 60 | 502 | 0 |
  | assembler_amx | 26 | 21 | 389 | 486 | 0 |
  | assembler_b | 18 | 13 | 155 | 494 | 0 |
  | assembler_bmx | 24 | 16 | 381 | 488 | 0 |
  | cand_holder | 5 | 7 | 59 | 507 | 0 |
  | req_sched | 8 | 26 | 4514 | 504 | 0 |
  | tag_checker | 7 | 7 | 152 | 505 | 0 |

## D3H

- mirror: `{"variant": "D3H", "fires": 48, "issues": 48, "cap_fire_min": 1, "cap_fire_max": 4, "fire_issue_min": 2, "fire_issue_max": 2, "gap_min": 1, "gap_max": 4, "lat_first10": [2, 1, 1, 1, 1, 1, 1, 1, 1, 1], "gaps_first10": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]}`
- _v5_bal: count=1314 bits=13985 top10=[('_v5_bal_1296', 1024), ('_v5_bal_1298', 1024), ('_v5_bal_1308', 352), ('_v5_bal_1310', 352), ('_v5_bal_1300', 256), ('_v5_bal_1302', 256), ('_v5_bal_1304', 256), ('_v5_bal_1306', 256), ('_v5_bal_1312', 256), ('_v5_bal_1314', 256)]
- per-module compile_stats:

  | module | max_logic_depth | reg_count | reg_bits | wns | tns |
  | :--- | :--- | :--- | :--- | :--- | :--- |
  | arbiter | 25 | 1 | 2 | 487 | 0 |
  | assembler_a | 10 | 7 | 60 | 502 | 0 |
  | assembler_amx | 26 | 21 | 389 | 486 | 0 |
  | assembler_b | 18 | 13 | 155 | 494 | 0 |
  | assembler_bmx | 24 | 16 | 381 | 488 | 0 |
  | cand_holder | 5 | 7 | 59 | 507 | 0 |
  | payload_delay | 1 | 168 | 2197 | 511 | 0 |
  | req_sched | 8 | 26 | 4514 | 504 | 0 |
  | tag_checker | 7 | 7 | 152 | 505 | 0 |
  | tb_pd_d3h_top | 47 | 510 | 511 | 465 | 0 |
