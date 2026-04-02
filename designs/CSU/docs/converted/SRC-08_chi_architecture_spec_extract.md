# SRC-08 — CHI architecture spec (partial text extract)

**Source:** `IHI0050H_amba_chi_architecture_spec.pdf` (Arm IHI0050H)  
**Generated:** 2026-04-01  
**Tool:** pypdf — **pages 1–150 only** (full PDF is large; use original PDF for normative figures/tables).

## PDF page 1

```text
AMBA® CHI
Architecture Specification
Document number ARM IHI 0050
Document quality Released
Document version Issue H
Document confidentiality Non-confidential
Date of issue 17 Sep 2025
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
```

## PDF page 2

```text
AMBA® CHI Architecture Specification
Release information
Date Version Changes
2025/Sep/17 H • Eleventh public release
2025/Sep/08 G.b • Tenth public release
2024/Mar/01 G • Ninth public release
2024/Feb/28 F.b • Eighth public release
2022/Sep/26 F • Seventh public release
2022/Sep/26 E.c • Sixth public release
2021/Aug/16 E.b • Fifth public release
2020/Aug/19 E.a • Fourth public release
2019/Aug/28 D • Third public release
2018/May/08 C • Second public release
2017/Aug/04 B • First public release
2014/Jun/12 A • First limited release
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
ii
```

## PDF page 3

```text
Non-Confidential Proprietary Notice
This document is protected by copyright and other related rights and the use or implementation of the information contained
in this document may be protected by one or more patents or pending patent applications. No part of this document may be
reproduced in any form by any means without the express prior written permission of Arm Limited (“Arm”).No license, express
or implied, by estoppel or otherwise to any intellectual property rights is granted by this document unless specifically
stated.
Your access to the information in this document is conditional upon your acceptance that you will not use or permit others
to use the information for the purposes of determining whether the subject matter of this document infringes any third party
patents.
The content of this document is informational only. Any solutions presented herein are subject to changing conditions, information,
scope, and data. This document was produced using reasonable efforts based on information available as of the date of issue
of this document. The scope of information in this document may exceed that which Arm is required to provide, and such
additional information is merely intended to further assist the recipient and does not represent Arm’s view of the scope of its
obligations. You acknowledge and agree that you possess the necessary expertise in system security and functional safety and
that you shall be solely responsible for compliance with all legal, regulatory, safety and security related requirements concerning
your products, notwithstanding any information or support that may be provided by Arm herein. In addition, you are responsible
for any applications which are used in conjunction with any Arm technology described in this document, and to minimize risks,
adequate design and operating safeguards should be provided for by you.
This document may include technical inaccuracies or typographical errors. THIS DOCUMENT IS PROVIDED “AS IS”. ARM
PROVIDES NO REPRESENTATIONS AND NO WARRANTIES, EXPRESS, IMPLIED OR STATUTORY , INCLUDING,
WITHOUT LIMITATION, THE IMPLIED WARRANTIES OF MERCHANTABILITY , SATISFACTORY QUALITY ,
NON-INFRINGEMENT OR FITNESS FOR A PARTICULAR PURPOSE WITH RESPECT TO THE DOCUMENT. For the
avoidance of doubt, Arm makes no representation with respect to, and has undertaken no analysis to identify or understand the
scope and content of, any patents, copyrights, trade secrets, trademarks, or other rights.
TO THE EXTENT NOT PROHIBITED BY LAW, IN NO EVENT WILL ARM BE LIABLE FOR ANY DAMAGES,
INCLUDING WITHOUT LIMITATION ANY DIRECT, INDIRECT, SPECIAL, INCIDENTAL, PUNITIVE, OR
CONSEQUENTIAL DAMAGES, HOWEVER CAUSED AND REGARDLESS OF THE THEORY OF LIABILITY , ARISING
OUT OF ANY USE OF THIS DOCUMENT, EVEN IF ARM HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGES.
Reference by Arm to any third party’s products or services within this document is not an express or implied approval or
endorsement of the use thereof.
This document consists solely of commercial items. You shall be responsible for ensuring that any permitted use, duplication, or
disclosure of this document complies fully with any relevant export laws and regulations to assure that this document or any
portion thereof is not exported, directly or indirectly, in violation of such export laws. Use of the word “partner” in reference
to Arm’s customers is not intended to create or refer to any partnership relationship with any other company. Arm may make
changes to this document at any time and without notice.
This document may be translated into other languages for convenience, and you agree that if there is any conflict between the
English version of this document and any translation, the terms of the English version of this document shall prevail.
The validity, construction and performance of this notice shall be governed by English Law.
The Arm corporate logo and words marked with ® or ™ are registered trademarks or trademarks of Arm Limited (or its affiliates)
in the US and/or elsewhere. Please follow Arm’s trademark usage guidelines at http://www.arm.com/company/policies/trademarks.
All rights reserved. Other brands and names mentioned in this document may be the trademarks of their respective owners.
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Arm Limited. Company 02557590 registered in England.
110 Fulbourn Road, Cambridge, England CB1 9NJ.
PRE-21451 version 3
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
iii
```

## PDF page 4

```text
AMBA SPECIFICATION LICENCE
THIS END USER LICENCE AGREEMENT (“LICENCE”) IS A LEGAL AGREEMENT BETWEEN YOU (EITHER A
SINGLE INDIVIDUAL, OR SINGLE LEGAL ENTITY) AND ARM LIMITED (“ARM”) FOR THE USE OF ARM’S
INTELLECTUAL PROPERTY (INCLUDING, WITHOUT LIMITATION, ANY COPYRIGHT) IN THE RELEV ANT AMBA
SPECIFICATION ACCOMPANYING THIS LICENCE. ARM LICENSES THE RELEV ANT AMBA SPECIFICATION TO
YOU ON CONDITION THAT YOU ACCEPT ALL OF THE TERMS IN THIS LICENCE. BY CLICKING “I AGREE” OR
OTHERWISE USING OR COPYING THE RELEV ANT AMBA SPECIFICATION YOU INDICATE THAT YOU AGREE TO
BE BOUND BY ALL THE TERMS OF THIS LICENCE.
“LICENSEE” means You and your Subsidiaries. “Subsidiary” means, if You are a single entity, any company the majority of
whose voting shares is now or hereafter owned or controlled, directly or indirectly, by You. A company shall be a Subsidiary only
for the period during which such control exists.
1. Subject to the provisions of Clauses 2, 3 and 4, Arm hereby grants to LICENSEE a perpetual, non-exclusive,
non-transferable, royalty free, worldwide licence to:
(i) use and copy the relevant AMBA Specification for the purpose of developing and having developed products that
comply with the relevant AMBA Specification;
(ii) manufacture and have manufactured products which either: (a) have been created by or for LICENSEE under the
licence granted in Clause 1(i); or (b) incorporate a product(s) which has been created by a third party(s) under a
licence granted by Arm in Clause 1(i) of such third party’s AMBA Specification Licence; and
(iii) offer to sell, sell, supply or otherwise distribute products which have either been (a) created by or for LICENSEE
under the licence granted in Clause 1(i); or (b) manufactured by or for LICENSEE under the licence granted in
Clause 1(ii).
2. LICENSEE hereby agrees that the licence granted in Clause 1 is subject to the following restrictions:
(i) where a product created under Clause 1(i) is an integrated circuit which includes a CPU then either: (a) such CPU
shall only be manufactured under licence from Arm; or (b) such CPU is neither substantially compliant with nor
marketed as being compliant with the Arm instruction sets licensed by Arm from time to time;
(ii) the licences granted in Clause 1(iii) shall not extend to any portion or function of a product that is not itself compliant
with part of the relevant AMBA Specification; and
(iii) no right is granted to LICENSEE to sublicense the rights granted to LICENSEE under this Agreement.
3. Except as specifically licensed in accordance with Clause 1, LICENSEE acquires no right, title or interest in any Arm
technology or any intellectual property embodied therein. In no event shall the licences granted in accordance with Clause
1 be construed as granting LICENSEE, expressly or by implication, estoppel or otherwise, a licence to use any Arm
technology except the relevant AMBA Specification.
4. THE RELEV ANT AMBA SPECIFICATION IS PROVIDED “AS IS” WITH NO REPRESENTATION OR
W ARRANTIES EXPRESS, IMPLIED OR STATUTORY , INCLUDING BUT NOT LIMITED TO ANY W ARRANTY OF
SATISFACTORY QUALITY , MERCHANTABILITY , NON-INFRINGEMENT OR FITNESS FOR A PARTICULAR
PURPOSE, OR THAT ANY USE OR IMPLEMENTATION OF SUCH ARM TECHNOLOGY WILL NOT INFRINGE
ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADE SECRETS OR OTHER INTELLECTUAL PROPERTY
RIGHTS.
5. NOTWITHSTANDING ANYTHING TO THE CONTRARY CONTAINED IN THIS AGREEMENT, TO THE FULLEST
EXTENT PETMITTED BY LAW, THE MAXIMUM LIABILITY OF ARM IN AGGREGATE FOR ALL CLAIMS MADE
AGAINST ARM, IN CONTRACT, TORT OR OTHERWISE, IN CONNECTION WITH THE SUBJECT MATTER OF
THIS AGREEMENT (INCLUDING WITHOUT LIMITATION (I) LICENSEE’S USE OF THE ARM TECHNOLOGY;
AND (II) THE IMPLEMENTATION OF THE ARM TECHNOLOGY IN ANY PRODUCT CREATED BY LICENSEE
UNDER THIS AGREEMENT) SHALL NOT EXCEED THE FEES PAID (IF ANY) BY LICENSEE TO ARM UNDER
THIS AGREEMENT. THE EXISTENCE OF MORE THAN ONE CLAIM OR SUIT WILL NOT ENLARGE OR EXTEND
THE LIMIT. LICENSEE RELEASES ARM FROM ALL OBLIGATIONS, LIABILITY , CLAIMS OR DEMANDS IN
EXCESS OF THIS LIMITATION.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
iv
```

## PDF page 5

```text
6. No licence, express, implied or otherwise, is granted to LICENSEE, under the provisions of Clause 1, to use the Arm
tradename, or AMBA trademark in connection with the relevant AMBA Specification or any products based thereon.
Nothing in Clause 1 shall be construed as authority for LICENSEE to make any representations on behalf of Arm in respect
of the relevant AMBA Specification.
7. This Licence shall remain in force until terminated by you or by Arm. Without prejudice to any of its other rights
if LICENSEE is in breach of any of the terms and conditions of this Licence then Arm may terminate this Licence
immediately upon giving written notice to You. You may terminate this Licence at any time. Upon expiry or termination of
this Licence by You or by Arm LICENSEE shall stop using the relevant AMBA Specification and destroy all copies of the
relevant AMBA Specification in your possession together with all documentation and related materials. Upon expiry or
termination of this Licence, the provisions of clauses 6 and 7 shall survive.
8. The validity, construction and performance of this Agreement shall be governed by English Law.
PRE-21451 version 3
Confidentiality Status
This document is Non-Confidential. The right to use, copy and disclose this document may be subject to license restrictions in
accordance with the terms of the agreement entered into by Arm and the party that Arm delivered this document to.
Product Status
The information in this document is final, that is for a developed product.
Web Address
http://www.arm.com
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
v
```

## PDF page 6

```text
Contents
AMBA® CHI Architecture Specification
AMBA® CHI Architecture Specification . . . . . . . . . . . . . . . . . . . . . . . . . . . . ii
Release information . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ii
Non-Confidential Proprietary Notice . . . . . . . . . . . . . . . . . . . . . . . . . . iii
AMBA SPECIFICATION LICENCE . . . . . . . . . . . . . . . . . . . . . . . . . . iv
Confidentiality Status . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . v
Product Status . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . v
Web Address . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . v
Part A Preface
About this specification
Intended audience . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xix
Using this specification
Conventions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xxii
Typographical conventions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xxii
Timing diagrams . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xxii
Time-Space diagrams . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xxii
Transaction flow diagrams . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xxiii
Signals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xxiv
Numbers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xxiv
Additional reading . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xxv
Arm publications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xxv
Feedback . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xxvi
Feedback on this specification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . xxvi
Inclusive terminology commitment . . . . . . . . . . . . . . . . . . . . . . . . . . xxvi
Part B Specification
Chapter B1 Introduction
B1.1 Architecture overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
B1.1.1 Components . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
B1.1.2 Key features . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
B1.1.3 Architecture layers . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30
B1.2 Topology . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31
B1.3 Terminology . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32
B1.4 Transaction classification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 35
B1.5 Coherence overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
B1.5.1 Coherency model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
B1.5.2 Cache state model . . . . . . . . . . . . . . . . . . . . . . . . . . . . 39
B1.6 Component naming . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 41
B1.7 Read data source . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43
Chapter B2 Transactions
B2.1 Channels overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 45
B2.2 Channel fields . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 46
B2.2.1 Transaction request fields . . . . . . . . . . . . . . . . . . . . . . . . . 46
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
vi
```

## PDF page 7

```text
Contents
B2.2.2 Response fields . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 49
B2.2.3 Snoop request fields . . . . . . . . . . . . . . . . . . . . . . . . . . . 50
B2.2.4 Data fields . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 51
B2.3 Transaction structure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 54
B2.3.1 Read transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 55
B2.3.2 Write transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 62
B2.3.3 Atomic transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . 83
B2.3.4 Stash transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . 85
B2.3.5 Dataless transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . 88
B2.3.6 Prefetch transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . 90
B2.3.7 DVM transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 91
B2.3.8 Retry . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 92
B2.3.9 Home Initiated transactions . . . . . . . . . . . . . . . . . . . . . . . . 93
B2.4 Transaction identifier fields . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 102
B2.4.1 Target Identifier, TgtID, and Source Identifier, SrcID . . . . . . . . . . 102
B2.4.2 Transaction Identifier, TxnID . . . . . . . . . . . . . . . . . . . . . . . 102
B2.4.3 Data Buffer Identifier, DBID . . . . . . . . . . . . . . . . . . . . . . . . 103
B2.4.4 Return Transaction Identifier, ReturnTxnID . . . . . . . . . . . . . . . 104
B2.4.5 Forward Transaction Identifier, FwdTxnID . . . . . . . . . . . . . . . . 105
B2.4.6 Data Identifier, DataID, and Critical Chunk Identifier, CCID . . . . . . 105
B2.4.7 Logical Processor Identifier, LPID . . . . . . . . . . . . . . . . . . . . 106
B2.4.8 Stash Logical Processor Identifier, StashLPID . . . . . . . . . . . . . 106
B2.4.9 Stash Node Identifier, StashNID . . . . . . . . . . . . . . . . . . . . . 106
B2.4.10 Return Node Identifier, ReturnNID . . . . . . . . . . . . . . . . . . . . 106
B2.4.11 Home Node Identifier, HomeNID . . . . . . . . . . . . . . . . . . . . . 108
B2.4.12 Forward Node Identifier, FwdNID . . . . . . . . . . . . . . . . . . . . 108
B2.4.13 Persistence Group Identifier, PGroupID . . . . . . . . . . . . . . . . . 108
B2.4.14 Stash Group Identifier, StashGroupID . . . . . . . . . . . . . . . . . . 109
B2.4.15 Tag Group Identifier, TagGroupID . . . . . . . . . . . . . . . . . . . . 109
B2.4.16 Cache Line Identifier, CacheLineID . . . . . . . . . . . . . . . . . . . 109
B2.5 Transaction identifier field flows . . . . . . . . . . . . . . . . . . . . . . . . . . . 110
B2.5.1 Read transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 110
B2.5.2 Dataless transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . 118
B2.5.3 Write transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 120
B2.5.4 DVMOp transaction . . . . . . . . . . . . . . . . . . . . . . . . . . . . 128
B2.5.5 Transaction requests with Retry . . . . . . . . . . . . . . . . . . . . . 128
B2.5.6 Protocol Credit Return transaction . . . . . . . . . . . . . . . . . . . . 129
B2.6 Multi-request . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 130
B2.6.1 Examples of multi-request . . . . . . . . . . . . . . . . . . . . . . . . 131
B2.7 Ordering . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 135
B2.7.1 Multi-copy atomicity . . . . . . . . . . . . . . . . . . . . . . . . . . . . 135
B2.7.2 Completion response and ordering . . . . . . . . . . . . . . . . . . . 135
B2.7.3 Completion acknowledgment . . . . . . . . . . . . . . . . . . . . . . . 137
B2.7.4 Ordering semantics of RespSepData and DataSepResp . . . . . . . . 139
B2.7.5 Transaction ordering . . . . . . . . . . . . . . . . . . . . . . . . . . . 140
B2.8 Address, Control, and Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 148
B2.8.1 Address . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 148
B2.8.2 Physical Address Space, PAS . . . . . . . . . . . . . . . . . . . . . . 148
B2.8.3 Memory Attributes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 149
B2.8.4 Transaction attribute combinations . . . . . . . . . . . . . . . . . . . . 152
B2.8.5 Likely Shared . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 154
B2.8.6 Snoop attribute . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 155
B2.8.7 Mismatched Memory attributes . . . . . . . . . . . . . . . . . . . . . . 156
B2.8.8 CopyAtHome attribute . . . . . . . . . . . . . . . . . . . . . . . . . . 158
B2.9 Data transfer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 162
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
vii
```

## PDF page 8

```text
Contents
B2.9.1 Data size . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 162
B2.9.2 Bytes access in memory . . . . . . . . . . . . . . . . . . . . . . . . . 162
B2.9.3 Byte Enables . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 163
B2.9.4 Data packetization . . . . . . . . . . . . . . . . . . . . . . . . . . . . 164
B2.9.5 Limited Data Elision . . . . . . . . . . . . . . . . . . . . . . . . . . . . 166
B2.9.6 Size, Address, and Data alignment in Atomic transactions . . . . . . . 169
B2.9.7 Critical Chunk Identifier . . . . . . . . . . . . . . . . . . . . . . . . . . 171
B2.9.8 Critical Chunk First Wrap order . . . . . . . . . . . . . . . . . . . . . 171
B2.9.9 Data Beat ordering . . . . . . . . . . . . . . . . . . . . . . . . . . . . 172
B2.9.10 Data transfer examples . . . . . . . . . . . . . . . . . . . . . . . . . . 172
B2.10 Request Retry . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 178
B2.10.1 Credit Return . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 180
B2.10.2 Transaction Retry mechanism . . . . . . . . . . . . . . . . . . . . . . 181
B2.10.3 Transaction Retry flow . . . . . . . . . . . . . . . . . . . . . . . . . . 181
Chapter B3 Network Layer
B3.1 System Address Map, SAM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 184
B3.2 Node ID . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 185
B3.3 TgtID determination . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 186
B3.3.1 TgtID determination for Request messages . . . . . . . . . . . . . . . 186
B3.3.2 TgtID determination for Response messages . . . . . . . . . . . . . . 186
B3.3.3 TgtID determination for snoop request messages . . . . . . . . . . . 187
B3.4 Network layer flow examples . . . . . . . . . . . . . . . . . . . . . . . . . . . . 188
B3.4.1 Simple flow . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 188
B3.4.2 Flow with interconnect-based SAM . . . . . . . . . . . . . . . . . . . 188
B3.4.3 Flow with interconnect-based SAM and Retry request . . . . . . . . . 189
Chapter B4 Coherence Protocol
B4.1 Cache line states . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 192
B4.1.1 Empty cache line ownership . . . . . . . . . . . . . . . . . . . . . . . 193
B4.1.2 Ownership of cache line with partial Dirty data . . . . . . . . . . . . . 193
B4.2 Request types . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 194
B4.2.1 Read transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 194
B4.2.2 Dataless transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . 200
B4.2.3 Write transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 208
B4.2.4 Combined Write requests . . . . . . . . . . . . . . . . . . . . . . . . . 215
B4.2.5 Atomic transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . 218
B4.2.6 Other transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 225
B4.3 Snoop request types . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 228
B4.4 Request transactions and corresponding Snoop requests . . . . . . . . . . . . 231
B4.4.1 Number of snoops to send . . . . . . . . . . . . . . . . . . . . . . . . 231
B4.4.2 Selection of snoop to send . . . . . . . . . . . . . . . . . . . . . . . . 231
B4.5 Response types . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 235
B4.5.1 Completion response . . . . . . . . . . . . . . . . . . . . . . . . . . . 235
B4.5.2 WriteData response . . . . . . . . . . . . . . . . . . . . . . . . . . . . 238
B4.5.3 Snoop response . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 240
B4.5.4 Miscellaneous response . . . . . . . . . . . . . . . . . . . . . . . . . 245
B4.6 Silent cache state transitions . . . . . . . . . . . . . . . . . . . . . . . . . . . . 249
B4.7 Cache state transitions at a Requester . . . . . . . . . . . . . . . . . . . . . . 251
B4.7.1 Read request transactions . . . . . . . . . . . . . . . . . . . . . . . . 251
B4.7.2 Dataless request transactions . . . . . . . . . . . . . . . . . . . . . . 260
B4.7.3 Write request transactions . . . . . . . . . . . . . . . . . . . . . . . . 261
B4.7.4 Atomic transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . 263
B4.7.5 Other request transactions . . . . . . . . . . . . . . . . . . . . . . . . 264
B4.8 Cache state transitions at a Snoopee . . . . . . . . . . . . . . . . . . . . . . . 265
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
viii
```

## PDF page 9

```text
Contents
B4.8.1 Non-Forwarding and Non-stash Snoop transactions . . . . . . . . . . 265
B4.8.2 Stash Snoop transactions . . . . . . . . . . . . . . . . . . . . . . . . 269
B4.8.3 Forwarding Snoop transactions . . . . . . . . . . . . . . . . . . . . . 272
B4.9 Returning Data with Snoop response . . . . . . . . . . . . . . . . . . . . . . . 281
B4.10 Do not transition to SD . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 282
B4.11 Hazard conditions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 283
B4.11.1 At the RN-F node . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 283
B4.11.2 At the ICN(HN-F) node . . . . . . . . . . . . . . . . . . . . . . . . . . 284
Chapter B5 Interconnect Protocol Flows
B5.1 Read transaction flows . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 286
B5.1.1 Read transactions with DMT and without snoops . . . . . . . . . . . . 286
B5.1.2 Read transaction with DMT and with snoops . . . . . . . . . . . . . . 286
B5.1.3 Read transaction with DCT . . . . . . . . . . . . . . . . . . . . . . . . 287
B5.1.4 Read transaction without DMT or DCT . . . . . . . . . . . . . . . . . 290
B5.1.5 Read transaction with snoop response with partial data and no memory
update . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 291
B5.1.6 Read transaction with snoop response with partial data and memory
update . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 292
B5.1.7 ReadOnce* and ReadNoSnp with early Home deallocation . . . . . . 293
B5.1.8 ReadNoSnp transaction with DMT and separate Non-data and Data-
only response . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 293
B5.1.9 ReadNoSnp transaction with DMT with ordering and separate Non-
data and Data-only . . . . . . . . . . . . . . . . . . . . . . . . . . . . 294
B5.2 Dataless transaction flows . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 296
B5.2.1 Dataless transaction without memory update . . . . . . . . . . . . . . 296
B5.2.2 Dataless transaction with memory update . . . . . . . . . . . . . . . . 297
B5.2.3 Persistent CMO with snoop and separate Comp and Persist . . . . . 298
B5.2.4 Evict transaction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 299
B5.3 Write transaction flows . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 300
B5.3.1 Write transaction with no snoop and separate responses . . . . . . . 300
B5.3.2 Write transaction with snoop and separate responses . . . . . . . . . 301
B5.3.3 CopyBack Write transaction to memory . . . . . . . . . . . . . . . . . 302
B5.4 Atomic transaction flows . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 304
B5.4.1 Atomic transactions with data return . . . . . . . . . . . . . . . . . . . 304
B5.4.2 Atomic transaction without data return . . . . . . . . . . . . . . . . . . 306
B5.4.3 Atomic operation executed at the Subordinate Node . . . . . . . . . . 308
B5.5 Stash transaction flows . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 311
B5.5.1 Write with Stash hint . . . . . . . . . . . . . . . . . . . . . . . . . . . 311
B5.5.2 Independent Stash request . . . . . . . . . . . . . . . . . . . . . . . . 312
B5.6 Hazard handling examples . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 313
B5.6.1 Snoop request . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 313
B5.6.2 Request . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 315
B5.6.3 Read or Dataless request . . . . . . . . . . . . . . . . . . . . . . . . . 317
B5.6.4 Race hazard . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 318
Chapter B6 Exclusive accesses
B6.1 Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 320
B6.2 Exclusive monitors . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 321
B6.2.1 Snoopable memory location . . . . . . . . . . . . . . . . . . . . . . . 321
B6.2.2 Additional address comparison . . . . . . . . . . . . . . . . . . . . . . 322
B6.2.3 Alternatives to a PoC monitor . . . . . . . . . . . . . . . . . . . . . . 322
B6.2.4 Non-snoopable memory location . . . . . . . . . . . . . . . . . . . . . 323
B6.3 Exclusive transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 324
B6.3.1 Responses to Exclusive requests . . . . . . . . . . . . . . . . . . . . 324
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
ix
```

## PDF page 10

```text
Contents
B6.3.2 System requirements . . . . . . . . . . . . . . . . . . . . . . . . . . . 327
B6.3.3 Exclusive accesses to Snoopable locations . . . . . . . . . . . . . . . 327
B6.3.4 Exclusive accesses to Non-snoopable locations . . . . . . . . . . . . 328
Chapter B7 Cache Stashing
B7.1 Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 331
B7.1.1 Snoop requests and Data Pull . . . . . . . . . . . . . . . . . . . . . . 331
B7.2 Write with Stash hint . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 333
B7.3 Independent Stash request . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 334
B7.4 Stash target identifiers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 336
B7.4.1 Stash target specified . . . . . . . . . . . . . . . . . . . . . . . . . . . 336
B7.4.2 Stash target not specified . . . . . . . . . . . . . . . . . . . . . . . . . 336
B7.5 Stash messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 337
B7.5.1 Supporting REQ packet fields . . . . . . . . . . . . . . . . . . . . . . 337
B7.5.2 Supporting SNP packet fields . . . . . . . . . . . . . . . . . . . . . . 337
B7.5.3 Supporting RSP packet field . . . . . . . . . . . . . . . . . . . . . . . 338
B7.5.4 Supporting DAT packet field . . . . . . . . . . . . . . . . . . . . . . . 338
Chapter B8 DVM Operations
B8.1 Introduction to DVM transactions . . . . . . . . . . . . . . . . . . . . . . . . . . 340
B8.2 DVM transaction flow . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 341
B8.2.1 Non-sync type DVM transaction flow . . . . . . . . . . . . . . . . . . . 341
B8.2.2 Sync type DVM transaction flow . . . . . . . . . . . . . . . . . . . . . 342
B8.2.3 Flow control . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 344
B8.3 DVMOp field value restrictions . . . . . . . . . . . . . . . . . . . . . . . . . . . 346
B8.3.1 Request DVMOp field value restrictions . . . . . . . . . . . . . . . . . 346
B8.3.2 Response DVMOp field value restrictions . . . . . . . . . . . . . . . . 347
B8.3.3 Snoop DVMOp field value restrictions . . . . . . . . . . . . . . . . . . 348
B8.3.4 Data DVMOp field value restrictions . . . . . . . . . . . . . . . . . . . 349
B8.4 DVM messages . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 351
B8.4.1 DVM message payload . . . . . . . . . . . . . . . . . . . . . . . . . . 351
B8.4.2 DVM message packing . . . . . . . . . . . . . . . . . . . . . . . . . . 357
B8.4.3 TLB Invalidate . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 358
B8.4.4 Branch Predictor Invalidate . . . . . . . . . . . . . . . . . . . . . . . . 363
B8.4.5 Instruction Cache Invalidate . . . . . . . . . . . . . . . . . . . . . . . 363
B8.4.6 Synchronization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 365
Chapter B9 Error Handling
B9.1 Packet level . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 368
B9.1.1 Error types . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 368
B9.1.2 Error response fields . . . . . . . . . . . . . . . . . . . . . . . . . . . 368
B9.1.3 Errors and transaction structure . . . . . . . . . . . . . . . . . . . . . 369
B9.1.4 Error response use by transaction type . . . . . . . . . . . . . . . . . 370
B9.2 Sub-packet level . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 381
B9.2.1 Poison . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 381
B9.2.2 Data Check . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 381
B9.2.3 Interoperability of Poison and DataCheck . . . . . . . . . . . . . . . . 382
B9.3 Use of interface parity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 383
B9.3.1 Byte parity check signals . . . . . . . . . . . . . . . . . . . . . . . . . 383
B9.3.2 Error detection behavior . . . . . . . . . . . . . . . . . . . . . . . . . 384
B9.3.3 Interface parity check signals . . . . . . . . . . . . . . . . . . . . . . . 384
B9.4 Hardware and software error categories . . . . . . . . . . . . . . . . . . . . . . 386
B9.4.1 Software-based error . . . . . . . . . . . . . . . . . . . . . . . . . . . 386
B9.4.2 Hardware-based error . . . . . . . . . . . . . . . . . . . . . . . . . . 386
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
x
```

## PDF page 11

```text
Contents
Chapter B10 Realm Management Extension
B10.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 388
B10.2 Physical Address Space, PAS . . . . . . . . . . . . . . . . . . . . . . . . . . . 389
B10.3 Cache maintenance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 390
B10.3.1 Cache Maintenance Operations . . . . . . . . . . . . . . . . . . . . . 390
B10.3.2 Remote invalidation . . . . . . . . . . . . . . . . . . . . . . . . . . . . 390
B10.4 DVM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 391
B10.5 MPAM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 392
B10.6 Memory Encryption Contexts, MEC . . . . . . . . . . . . . . . . . . . . . . . . 393
B10.6.1 MECID field applicability . . . . . . . . . . . . . . . . . . . . . . . . . 393
B10.6.2 Memory accesses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 395
B10.6.3 Stash transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . 395
B10.6.4 Cache Maintenance Operations . . . . . . . . . . . . . . . . . . . . . 395
B10.6.5 MECID correctness and Poison signaling . . . . . . . . . . . . . . . . 395
B10.7 Device Assignment (DA) and Coherent Device Assignment (CDA) . . . . . . . 397
B10.7.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 397
B10.7.2 Field applicability . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 398
B10.7.3 Component requirements . . . . . . . . . . . . . . . . . . . . . . . . . 400
B10.8 Granular Data Isolation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 405
B10.8.1 MECID mismatch resolution . . . . . . . . . . . . . . . . . . . . . . . 405
Chapter B11 System Control, Debug, Trace, and Monitoring
B11.1 Quality of Service (QoS) mechanism . . . . . . . . . . . . . . . . . . . . . . . 409
B11.1.1 Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 409
B11.1.2 QoS priority value . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 409
B11.1.3 Repeating a transaction with a higher QoS value . . . . . . . . . . . . 409
B11.2 Data Source . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 410
B11.2.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 410
B11.2.2 CompleterDistance . . . . . . . . . . . . . . . . . . . . . . . . . . . . 410
B11.2.3 CompleterType . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 410
B11.2.4 HitD . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 411
B11.2.5 Functional . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 412
B11.2.6 Example system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 414
B11.2.7 Driving and modifying DataSource[7:0] . . . . . . . . . . . . . . . . . 415
B11.3 Data Target . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 417
B11.3.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 417
B11.3.2 Field applicability . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 417
B11.4 MPAM . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 421
B11.4.1 MPAMSP . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 422
B11.4.2 MPAM value propagation . . . . . . . . . . . . . . . . . . . . . . . . . 422
B11.4.3 Stash transaction rules . . . . . . . . . . . . . . . . . . . . . . . . . . 422
B11.4.4 Request to Subordinate rules . . . . . . . . . . . . . . . . . . . . . . 422
B11.5 Page-based Hardware Attributes . . . . . . . . . . . . . . . . . . . . . . . . . . 423
B11.5.1 PBHA field applicability . . . . . . . . . . . . . . . . . . . . . . . . . . 423
B11.5.2 Interconnect use of PBHA . . . . . . . . . . . . . . . . . . . . . . . . 423
B11.5.3 Stash transaction rules . . . . . . . . . . . . . . . . . . . . . . . . . . 423
B11.5.4 PBHA value consistency . . . . . . . . . . . . . . . . . . . . . . . . . 423
B11.6 Completer Busy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 425
B11.6.1 Use case . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 425
B11.7 Trace Tag . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 427
B11.7.1 TraceTag usage and rules . . . . . . . . . . . . . . . . . . . . . . . . 427
Chapter B12 Memory Tagging
B12.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 430
B12.2 Message extensions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 431
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xi
```

## PDF page 12

```text
Contents
B12.3 Tag coherency . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 432
B12.4 Read transaction rules . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 433
B12.4.1 TagOp values . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 433
B12.4.2 Permitted initial MTE tag states . . . . . . . . . . . . . . . . . . . . . 435
B12.5 Write transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 437
B12.5.1 Permitted TagOp values . . . . . . . . . . . . . . . . . . . . . . . . . 437
B12.5.2 TagOp, TU, and tags relationship . . . . . . . . . . . . . . . . . . . . 437
B12.6 Dataless transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 439
B12.7 Atomic transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 440
B12.8 Stash transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 441
B12.9 Snoop requests . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 442
B12.9.1 Non-forwarding snoops . . . . . . . . . . . . . . . . . . . . . . . . . . 442
B12.9.2 Forwarding snoops . . . . . . . . . . . . . . . . . . . . . . . . . . . . 442
B12.9.3 Stash snoops . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 443
B12.9.4 Permitted TagOp values in Snoop responses . . . . . . . . . . . . . . 443
B12.10 Home to Subordinate transactions . . . . . . . . . . . . . . . . . . . . . . . . . 445
B12.11 Error response . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 446
B12.11.1 Tag Match . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 446
B12.11.2 Non-Tag Match errors . . . . . . . . . . . . . . . . . . . . . . . . . . . 446
B12.11.3 MTE not supported . . . . . . . . . . . . . . . . . . . . . . . . . . . . 447
B12.12 Requests and permitted tag operations . . . . . . . . . . . . . . . . . . . . . . 448
B12.13 TagOp field use summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 450
Chapter B13 Link Layer
B13.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 453
B13.2 Link . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 454
B13.2.1 Outbound and inbound links . . . . . . . . . . . . . . . . . . . . . . . 454
B13.3 Flit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 455
B13.4 Channel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 456
B13.4.1 Channel dependencies . . . . . . . . . . . . . . . . . . . . . . . . . . 456
B13.5 Port . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 458
B13.6 Node interface definitions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 460
B13.6.1 Request Nodes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 460
B13.6.2 Subordinate Nodes . . . . . . . . . . . . . . . . . . . . . . . . . . . . 461
B13.7 Increasing inter-port bandwidth . . . . . . . . . . . . . . . . . . . . . . . . . . . 462
B13.7.1 Multiple interfaces . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 462
B13.7.2 Replicated channels on a single interface . . . . . . . . . . . . . . . . 463
B13.8 Channel interface signals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 466
B13.8.1 Request, REQ, channel . . . . . . . . . . . . . . . . . . . . . . . . . . 466
B13.8.2 Response, RSP , channel . . . . . . . . . . . . . . . . . . . . . . . . . 467
B13.8.3 Snoop, SNP , channel . . . . . . . . . . . . . . . . . . . . . . . . . . . 468
B13.8.4 Data, DAT, channel . . . . . . . . . . . . . . . . . . . . . . . . . . . . 469
B13.9 Flit packet definitions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 471
B13.9.1 Request flit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 471
B13.9.2 Response flit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 473
B13.9.3 Snoop flit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 474
B13.9.4 Data flit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 475
B13.10 Protocol flit fields . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 477
B13.10.1 Quality of Service, QoS . . . . . . . . . . . . . . . . . . . . . . . . . . 478
B13.10.2 Target Identifier, TgtID . . . . . . . . . . . . . . . . . . . . . . . . . . 478
B13.10.3 Source Identifier, SrcID . . . . . . . . . . . . . . . . . . . . . . . . . . 478
B13.10.4 Home Node Identifier, HomeNID . . . . . . . . . . . . . . . . . . . . . 478
B13.10.5 Return Node Identifier, ReturnNID . . . . . . . . . . . . . . . . . . . . 478
B13.10.6 Forward Node Identifier, FwdNID . . . . . . . . . . . . . . . . . . . . 479
B13.10.7 Logical Processor Identifier, LPID . . . . . . . . . . . . . . . . . . . . 479
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xii
```

## PDF page 13

```text
Contents
B13.10.8 Persistence Group Identifier, PGroupID . . . . . . . . . . . . . . . . . 479
B13.10.9 Stash Node Identifier, StashNID . . . . . . . . . . . . . . . . . . . . . 480
B13.10.10 Stash Node Identifier Valid, StashNIDValid . . . . . . . . . . . . . . . 480
B13.10.11 Stash Logical Processor Identifier, StashLPID . . . . . . . . . . . . . 480
B13.10.12 Stash Logical Processor Identifier Valid, StashLPIDValid . . . . . . . . 480
B13.10.13 Stash Group Identifier, StashGroupID . . . . . . . . . . . . . . . . . . 481
B13.10.14 Transaction Identifier, TxnID . . . . . . . . . . . . . . . . . . . . . . . 481
B13.10.15 Return Transaction Identifier, ReturnTxnID . . . . . . . . . . . . . . . 481
B13.10.16 Forwarding Transaction Identifier, FwdTxnID . . . . . . . . . . . . . . 481
B13.10.17 Data Buffer Identifier, DBID . . . . . . . . . . . . . . . . . . . . . . . . 482
B13.10.18 Channel opcodes, Opcode . . . . . . . . . . . . . . . . . . . . . . . . 482
B13.10.19 Deep persistence, Deep . . . . . . . . . . . . . . . . . . . . . . . . . 487
B13.10.20 Address, Addr . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 487
B13.10.21 Size of transaction data, Size . . . . . . . . . . . . . . . . . . . . . . . 488
B13.10.22 Memory Attribute, MemAttr . . . . . . . . . . . . . . . . . . . . . . . . 488
B13.10.23 Snoop Attribute, SnpAttr . . . . . . . . . . . . . . . . . . . . . . . . . 489
B13.10.24 Do Direct Write Transfer, DoDWT . . . . . . . . . . . . . . . . . . . . 489
B13.10.25 Likely Shared, LikelyShared . . . . . . . . . . . . . . . . . . . . . . . 490
B13.10.26 Ordering requirements, Order . . . . . . . . . . . . . . . . . . . . . . 490
B13.10.27 Exclusive, Excl . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 491
B13.10.28 CopyAtHome, CAH . . . . . . . . . . . . . . . . . . . . . . . . . . . . 491
B13.10.29 Page-based Hardware Attribute, PBHA . . . . . . . . . . . . . . . . . 492
B13.10.30 Endian . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 492
B13.10.31 Allow Retry, AllowRetry . . . . . . . . . . . . . . . . . . . . . . . . . . 493
B13.10.32 Expect Completion Acknowledge, ExpCompAck . . . . . . . . . . . . 493
B13.10.33 SnoopMe . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 493
B13.10.34 Return to Source, RetToSrc . . . . . . . . . . . . . . . . . . . . . . . 494
B13.10.35 Data Pull, DataPull . . . . . . . . . . . . . . . . . . . . . . . . . . . . 494
B13.10.36 Do not transition to SD state, DoNotGoToSD . . . . . . . . . . . . . . 494
B13.10.37 Protocol Credit Type, PCrdType . . . . . . . . . . . . . . . . . . . . . 495
B13.10.38 Tag Operation, TagOp . . . . . . . . . . . . . . . . . . . . . . . . . . . 495
B13.10.39 Tag . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 496
B13.10.40 Tag Update, TU . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 496
B13.10.41 Tag Group Identifier, TagGroupID . . . . . . . . . . . . . . . . . . . . 497
B13.10.42 Trace Tag, TraceTag . . . . . . . . . . . . . . . . . . . . . . . . . . . . 497
B13.10.43 Memory System Resource Partitioning and Monitoring, MPAM . . . . 497
B13.10.44 Virtual Machine Identifier Extension, VMIDExt . . . . . . . . . . . . . 498
B13.10.45 Response Error, RespErr . . . . . . . . . . . . . . . . . . . . . . . . . 498
B13.10.46 Response status, Resp . . . . . . . . . . . . . . . . . . . . . . . . . . 498
B13.10.47 Forward State, FwdState . . . . . . . . . . . . . . . . . . . . . . . . . 501
B13.10.48 Completer Busy, CBusy . . . . . . . . . . . . . . . . . . . . . . . . . . 502
B13.10.49 Data payload, Data . . . . . . . . . . . . . . . . . . . . . . . . . . . . 502
B13.10.50 Critical Chunk Identifier, CCID . . . . . . . . . . . . . . . . . . . . . . 502
B13.10.51 Data Identifier, DataID . . . . . . . . . . . . . . . . . . . . . . . . . . 503
B13.10.52 Byte Enable, BE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 503
B13.10.53 Data check, DataCheck . . . . . . . . . . . . . . . . . . . . . . . . . . 503
B13.10.54 Poison . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 503
B13.10.55 Data source, DataSource . . . . . . . . . . . . . . . . . . . . . . . . . 504
B13.10.56 Data Target, DataTarget . . . . . . . . . . . . . . . . . . . . . . . . . 504
B13.10.57 PrefetchTgt Hint, PrefetchTgtHint . . . . . . . . . . . . . . . . . . . . 504
B13.10.58 Number of DAT packets elided, NumDat . . . . . . . . . . . . . . . . . 505
B13.10.59 Replicate . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 506
B13.10.60 Reserved for Customer Use, RSVDC . . . . . . . . . . . . . . . . . . 506
B13.10.61 Memory Encryption Context Identifier, MECID . . . . . . . . . . . . . 507
B13.10.62 Stream Identifier, StreamID . . . . . . . . . . . . . . . . . . . . . . . . 508
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xiii
```

## PDF page 14

```text
Contents
B13.10.63 Stream Identifier Security State, SecSID1 . . . . . . . . . . . . . . . . 508
B13.10.64 MultiReq . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 508
B13.10.65 NumReq . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 509
B13.10.66 CacheLineID . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 512
B13.10.67 MismatchedMECID . . . . . . . . . . . . . . . . . . . . . . . . . . . . 512
B13.10.68 PAS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 513
B13.11 Link layer Credit Return, LCrdReturn . . . . . . . . . . . . . . . . . . . . . . . 515
Chapter B14 Link Handshake
B14.1 Clock and initialization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 517
B14.1.1 Clock . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 517
B14.1.2 Reset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 517
B14.1.3 Initialization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 517
B14.2 Link layer Credit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 518
B14.2.1 L-Credit flow control . . . . . . . . . . . . . . . . . . . . . . . . . . . . 518
B14.3 Low power signaling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 522
B14.4 Flit level clock gating . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 523
B14.5 Interface activation and deactivation . . . . . . . . . . . . . . . . . . . . . . . . 524
B14.5.1 Request and Acknowledge handshake . . . . . . . . . . . . . . . . . 524
B14.6 Transmit and receive link interaction . . . . . . . . . . . . . . . . . . . . . . . . 530
B14.6.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 530
B14.6.2 Tx and Rx state machines . . . . . . . . . . . . . . . . . . . . . . . . 530
B14.6.3 Expected transitions . . . . . . . . . . . . . . . . . . . . . . . . . . . 532
B14.7 Protocol layer activity indication . . . . . . . . . . . . . . . . . . . . . . . . . . 536
B14.7.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 536
B14.7.2 TXSACTIVE signal . . . . . . . . . . . . . . . . . . . . . . . . . . . . 536
B14.7.3 RXSACTIVE signal . . . . . . . . . . . . . . . . . . . . . . . . . . . . 538
B14.7.4 Relationship between SACTIVE and LINKACTIVE . . . . . . . . . . . 538
Chapter B15 System Coherency Interface
B15.1 Overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 541
B15.2 Handshake . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 542
B15.2.1 Request Node rules . . . . . . . . . . . . . . . . . . . . . . . . . . . . 542
B15.2.2 Interconnect rules . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 543
B15.2.3 Protocol states . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 543
Chapter B16 Properties, Parameters, and Broadcast Signals
B16.1 Interface properties and parameters . . . . . . . . . . . . . . . . . . . . . . . . 546
B16.1.1 Atomic_Transactions . . . . . . . . . . . . . . . . . . . . . . . . . . . 546
B16.1.2 Cache_Stash_Transactions . . . . . . . . . . . . . . . . . . . . . . . 547
B16.1.3 Direct_Memory_Transfer . . . . . . . . . . . . . . . . . . . . . . . . . 547
B16.1.4 Data_Poison . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 547
B16.1.5 Direct_Cache_Transfer . . . . . . . . . . . . . . . . . . . . . . . . . . 548
B16.1.6 Data_Check . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 548
B16.1.7 Check_Type . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 548
B16.1.8 CleanSharedPersistSep_Request . . . . . . . . . . . . . . . . . . . . 549
B16.1.9 MPAM_Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 549
B16.1.10 CCF_Wrap_Order . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 550
B16.1.11 Req_Addr_Width . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 550
B16.1.12 NodeID_Width . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 550
B16.1.13 Data_Width . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 551
B16.1.14 Enhanced_Features . . . . . . . . . . . . . . . . . . . . . . . . . . . 551
B16.1.15 Deferrable_Write . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 551
B16.1.16 RME_Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 552
B16.1.17 Nonshareable_Cache_Maint . . . . . . . . . . . . . . . . . . . . . . . 552
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xiv
```

## PDF page 15

```text
Contents
B16.1.18 Outer_Cacheable_Support . . . . . . . . . . . . . . . . . . . . . . . . 554
B16.1.19 PBHA_Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 555
B16.1.20 Cache_State_UDP . . . . . . . . . . . . . . . . . . . . . . . . . . . . 555
B16.1.21 Cache_State_SD . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 556
B16.1.22 DVM_Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 556
B16.1.23 MTE_Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 556
B16.1.24 Limited_Data_Elision . . . . . . . . . . . . . . . . . . . . . . . . . . . 559
B16.1.25 MEC_Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 559
B16.1.26 MECID_Width . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 560
B16.1.27 DevAssign_Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . 560
B16.1.28 Req_RSVDC_Width . . . . . . . . . . . . . . . . . . . . . . . . . . . 561
B16.1.29 Dat_RSVDC_Width . . . . . . . . . . . . . . . . . . . . . . . . . . . . 562
B16.1.30 GDI_Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 562
B16.1.31 GDI_Non_PE_RNF . . . . . . . . . . . . . . . . . . . . . . . . . . . . 563
B16.1.32 MECID_Mismatch_Resolution_Realm . . . . . . . . . . . . . . . . . . 563
B16.1.33 CleanInvalidStorage_Request . . . . . . . . . . . . . . . . . . . . . . 564
B16.1.34 Num_RP_REQ . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 564
B16.1.35 Shared_Credits_REQ . . . . . . . . . . . . . . . . . . . . . . . . . . . 566
B16.1.36 Num_RP_SNP . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 566
B16.1.37 Shared_Credits_SNP . . . . . . . . . . . . . . . . . . . . . . . . . . . 568
B16.1.38 Retry_Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 569
B16.1.39 MultiReq_Support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 569
B16.1.40 MultiReq_Requester_Retry_Support . . . . . . . . . . . . . . . . . . 571
B16.1.41 MultiReq_Completer_Retry_Support . . . . . . . . . . . . . . . . . . 571
B16.2 Optional interface broadcast signals . . . . . . . . . . . . . . . . . . . . . . . . 573
B16.2.1 BROADCASTINNER and BROADCASTOUTER . . . . . . . . . . . . 573
B16.2.2 BROADCASTCACHEMAINT . . . . . . . . . . . . . . . . . . . . . . . 574
B16.2.3 BROADCASTPERSIST . . . . . . . . . . . . . . . . . . . . . . . . . . 575
B16.2.4 BROADCASTCMOPOPA . . . . . . . . . . . . . . . . . . . . . . . . . 576
B16.2.5 BROADCASTSTORAGE . . . . . . . . . . . . . . . . . . . . . . . . . 577
B16.2.6 BROADCASTATOMIC . . . . . . . . . . . . . . . . . . . . . . . . . . 578
B16.2.7 BROADCASTICINVAL . . . . . . . . . . . . . . . . . . . . . . . . . . 579
B16.2.8 BROADCASTMTE . . . . . . . . . . . . . . . . . . . . . . . . . . . . 579
B16.2.9 BROADCASTTLBIINNER and BROADCASTTLBIOUTER . . . . . . . 580
B16.2.10 BROADCASTLIMELISION . . . . . . . . . . . . . . . . . . . . . . . . 580
B16.2.11 BROADCASTMULTIREQ . . . . . . . . . . . . . . . . . . . . . . . . . 581
B16.3 Atomic transaction support . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 583
B16.3.1 Request Node support . . . . . . . . . . . . . . . . . . . . . . . . . . 583
B16.3.2 Interconnect support . . . . . . . . . . . . . . . . . . . . . . . . . . . 583
B16.3.3 Subordinate Node support . . . . . . . . . . . . . . . . . . . . . . . . 584
Part C Appendices
Chapter C1 Message Field Mappings
C1.1 Request message field mappings . . . . . . . . . . . . . . . . . . . . . . . . . 588
C1.1.1 Read, Dataless, and Miscellaneous . . . . . . . . . . . . . . . . . . . 588
C1.1.2 Write and Combined Write . . . . . . . . . . . . . . . . . . . . . . . . 591
C1.1.3 Stash and Atomic . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 595
C1.2 Response message field mappings . . . . . . . . . . . . . . . . . . . . . . . . 597
C1.3 Snoop Request message field mappings . . . . . . . . . . . . . . . . . . . . . 598
C1.4 Data message field mappings . . . . . . . . . . . . . . . . . . . . . . . . . . . 599
Chapter C2 Communicating Nodes
C2.1 Request communicating nodes . . . . . . . . . . . . . . . . . . . . . . . . . . . 602
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xv
```

## PDF page 16

```text
Contents
C2.2 Snoop communicating nodes . . . . . . . . . . . . . . . . . . . . . . . . . . . . 605
C2.3 Response communicating nodes . . . . . . . . . . . . . . . . . . . . . . . . . . 606
C2.4 Data communicating nodes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 607
Chapter C3 Node Transaction Subsets
C3.1 Request Nodes Subset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 610
C3.2 Subordinate Nodes Subset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 613
Chapter C4 Transaction Summaries
C4.1 AtomicCompare . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 617
C4.2 AtomicLoad . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 618
C4.3 AtomicStore . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 619
C4.4 AtomicSwap . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 620
C4.5 CleanInvalid . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 621
C4.6 CleanInvalidPoPA . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 622
C4.7 CleanInvalidStorage . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 623
C4.8 CleanShared . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 624
C4.9 CleanSharedPersist . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 625
C4.10 CleanSharedPersistSep . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 626
C4.11 CleanUnique . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 627
C4.12 DVMOp . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 628
C4.13 Evict . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 629
C4.14 MakeInvalid . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 630
C4.15 MakeReadUnique . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 631
C4.16 MakeUnique . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 632
C4.17 PCrdReturn . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 633
C4.18 PrefetchTgt . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 634
C4.19 ReadClean . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 635
C4.20 ReadNoSnp . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 636
C4.21 ReadNoSnpSep . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 637
C4.22 ReadNotSharedDirty . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 638
C4.23 ReadOnce . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 639
C4.24 ReadOnceCleanInvalid . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 640
C4.25 ReadOnceMakeInvalid . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 641
C4.26 ReadPreferUnique . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 642
C4.27 ReadShared . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 643
C4.28 ReadUnique . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 644
C4.29 ReqLCrdReturn . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 645
C4.30 StashOnceSepShared . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 646
C4.31 StashOnceSepUnique . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 647
C4.32 StashOnceShared . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 648
C4.33 StashOnceUnique . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 649
C4.34 WriteBackFull . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 650
C4.35 WriteBackFullCleanInv . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 651
C4.36 WriteBackFullCleanInvPoPA . . . . . . . . . . . . . . . . . . . . . . . . . . . . 652
C4.37 WriteBackFullCleanInvStrg . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 653
C4.38 WriteBackFullCleanSh . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 654
C4.39 WriteBackFullCleanShPerSep . . . . . . . . . . . . . . . . . . . . . . . . . . . 655
C4.40 WriteBackPtl . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 656
C4.41 WriteCleanFull . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 657
C4.42 WriteCleanFullCleanSh . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 658
C4.43 WriteCleanFullCleanShPerSep . . . . . . . . . . . . . . . . . . . . . . . . . . . 659
C4.44 WriteEvictFull . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 660
C4.45 WriteEvictOrEvict . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 661
C4.46 WriteNoSnpDef . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 662
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xvi
```

## PDF page 17

```text
Contents
Contents
C4.47 WriteNoSnpFull . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 663
C4.48 WriteNoSnpFullCleanInv . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 664
C4.49 WriteNoSnpFullCleanInvPoPA . . . . . . . . . . . . . . . . . . . . . . . . . . . 665
C4.50 WriteNoSnpFullCleanInvStrg . . . . . . . . . . . . . . . . . . . . . . . . . . . . 666
C4.51 WriteNoSnpFullCleanSh . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 667
C4.52 WriteNoSnpFullCleanShPerSep . . . . . . . . . . . . . . . . . . . . . . . . . . 668
C4.53 WriteNoSnpPtl . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 669
C4.54 WriteNoSnpPtlCleanInv . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 670
C4.55 WriteNoSnpPtlCleanInvPoPA . . . . . . . . . . . . . . . . . . . . . . . . . . . . 671
C4.56 WriteNoSnpPtlCleanSh . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 672
C4.57 WriteNoSnpPtlCleanShPerSep . . . . . . . . . . . . . . . . . . . . . . . . . . . 673
C4.58 WriteNoSnpZero . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 674
C4.59 WriteUniqueFull . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 675
C4.60 WriteUniqueFullCleanInvStrg . . . . . . . . . . . . . . . . . . . . . . . . . . . . 676
C4.61 WriteUniqueFullCleanSh . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 677
C4.62 WriteUniqueFullCleanShPerSep . . . . . . . . . . . . . . . . . . . . . . . . . . 678
C4.63 WriteUniqueFullStash . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 679
C4.64 WriteUniquePtl . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 680
C4.65 WriteUniquePtlCleanSh . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 681
C4.66 WriteUniquePtlCleanShPerSep . . . . . . . . . . . . . . . . . . . . . . . . . . . 682
C4.67 WriteUniquePtlStash . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 683
C4.68 WriteUniqueZero . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 684
Chapter C5 Revisions
C5.1 Changes between Issue A and Issue B . . . . . . . . . . . . . . . . . . . . . . 686
C5.2 Changes between Issue B and Issue C . . . . . . . . . . . . . . . . . . . . . . 687
C5.3 Changes between Issue C and Issue D . . . . . . . . . . . . . . . . . . . . . . 688
C5.4 Changes between Issue D and Issue E.a . . . . . . . . . . . . . . . . . . . . . 690
C5.5 Changes between Issue E.a and Issue E.b . . . . . . . . . . . . . . . . . . . . 693
C5.6 Changes between Issue E.b and Issue E.c . . . . . . . . . . . . . . . . . . . . 695
C5.7 Changes between Issue E.c and Issue F . . . . . . . . . . . . . . . . . . . . . 696
C5.8 Changes between Issue F and Issue F .b . . . . . . . . . . . . . . . . . . . . . 697
C5.9 Changes between Issue F .b and Issue G . . . . . . . . . . . . . . . . . . . . . 700
C5.10 Changes between Issue G and Issue G.b . . . . . . . . . . . . . . . . . . . . . 702
C5.11 Changes between Issue G.b and Issue H . . . . . . . . . . . . . . . . . . . . . 705
Part D Glossary
Chapter D1 Glossary
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xvii
```

## PDF page 18

```text
Part A
Preface
```

## PDF page 19

```text
About this specification
About this specification
This specification describes the AMBA® Coherent Hub Interface (CHI) architecture.
Intended audience
This specification is written for hardware and software engineers who want to become familiar with the CHI
architecture and design systems and modules that are compatible with the CHI architecture.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xix
```

## PDF page 20

```text
Using this specification
Using this specification
The information in this specification is organized into parts, as described in this section:
Chapter B1 Introduction
Read this for an introduction to the CHI architecture and the terminology in this specification.
Chapter B2 Transactions
Read this for an overview of the communication channels between nodes, the associated packet fields,
transaction structures, transaction ID flows, and the supported transaction ordering.
Chapter B3 Network Layer
Read this for a description of the Network layer that is required to determine the node ID of a
destination node.
Chapter B4 Coherence Protocol
Read this for an introduction to the coherence protocol.
Chapter B5 Interconnect Protocol Flows
Read this for examples of protocol flows for different transaction types.
Chapter B6 Exclusive accesses
Read this for a description of the mechanisms that the architecture includes to support Exclusive
accesses.
Chapter B7 Cache Stashing
Read this for a description of the cache stashing mechanism whereby data can be installed in a cache.
Chapter B8 DVM Operations
Read this for a description of DVM operations that the protocol uses to manage virtual memory.
Chapter B9 Error Handling
Read this for a description of the error response requirements.
Chapter B10 Realm Management Extension
Read this for a description of the Realm Management Extension (RME).
Chapter B11 System Control, Debug, Trace, and Monitoring
Read this for a description of the mechanisms that provide additional support for the control,
debugging, tracing, and performance measurement of systems.
Chapter B12 Memory Tagging
Read this for a description of the Memory Tagging Extension (MTE) that provides a mechanism to
check the correct usage of data held in memory.
Chapter B13 Link Layer
Read this for a description of the Link layer that provides a mechanism for packet based
communication between protocol nodes and the interconnect.
Chapter B14 Link Handshake
Read this for a description of the Link layer handshake requirements.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xx
```

## PDF page 21

```text
Using this specification
Chapter B15 System Coherency Interface
Read this for a description of the interface signals that support connecting and disconnecting
components from both the Coherency and DVM domains.
Chapter B16 Properties, Parameters, and Broadcast Signals
Read this for a description of the optional signals that provide flexibility in configuring optional
interface properties.
Chapter C1 Message Field Mappings
Read this for the field mappings for messages.
Chapter C2 Communicating Nodes
Read this for the node pairs that can legally communicate within the protocol.
Chapter C3 Node Transaction Subsets
Read this for node transaction subsets for Requesters and Subordinates.
Chapter C4 Transaction Summaries
Read this for transaction summaries.
Chapter C5 Revisions
Read this for a description of the technical changes between released issues of this specification.
Chapter D1 Glossary
Read this for definitions of terms used in this specification.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xxi
```

## PDF page 22

```text
Using this specification
Conventions
Conventions
Typographical conventions
The typographical conventions are:
italic Highlights important notes, introduces special terminology, and denotes internal
cross-references and citations.
bold Denotes signal names, and is used for terms in descriptive lists, where appropriate.
monospace Used for assembler syntax descriptions, pseudocode, and source code examples.
Also used in the main text for instruction mnemonics and for references to other items
appearing in assembler syntax descriptions, pseudocode, and source code examples.
SMALL CAPITALS Used for a few terms that have specific technical meanings.
Timing diagrams
The components used in timing diagrams are explained in Figure 1. Variations have clear labels, when they occur.
Do not assume any timing information that is not explicit in the diagrams.
Shaded bus and signal areas are undefined, so the bus or signal can assume any value within the shaded area at that
time. The actual level is unimportant and does not affect normal operation.
Clock
HIGH to LOW
Transient
HIGH/LOW to HIGH
Bus stable
Bus to high impedance
Bus change
High impedance to stable bus
Figure 1: Key to timing diagram conventions
Timing diagrams sometimes show single-bit signals as HIGH and LOW at the same time and they look similar to
the bus change shown in Figure 1 diagram conventions. If a timing diagram shows a single-bit signal in this way,
then its value does not affect the accompanying description.
Time-Space diagrams
The Figure 2 figure explains the format used to illustrate protocol flow.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xxii
```

## PDF page 23

```text
Using this specification
Conventions
RN-F HN-F
I->UC
I Allocation
Protocol
nodes
Initial cache
state
REQ
RSP
Direction of
message flow
Lifetime of a
transaction
Allocated but forward
progress is blocked
Forward progress
is unblocked
Deallocation
Cache state
change
Time
Space
Figure 2: Key to Time-Space diagram conventions
In Figure 2:
• The protocol nodes are positioned along the horizontal axis and time is indicated vertically, top to bottom.
• The lifetime of a transaction at a protocol node is shown by an elongated shaded rectangle along the time
axis from allocation to the deallocation time.
• The initial cache state at the node is shown at the top.
• The diamond shape on the timeline indicates arrival of a request and whether its processing is blocked
waiting for another event to complete.
• The cache state transition, upon the occurrence of an event, is indicated by I->UC.
Transaction flow diagrams
The Figure 3 figure explains the format used to illustrate transaction flow diagrams.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xxiii
```

## PDF page 24

```text
Using this specification
Conventions
Node 1
Node 1
Node 2
Node 2
Request message (REQ channel)
Response message (RSP channel)
Snoop request message (SNP channel)
alt [This is alternative transaction ﬂow 1]
Data Response message (DAT channel)
[This is alternative transaction ﬂow 2]
Response message (RSP channel)
Data Response message (DAT channel)
opt [This is an optional message]
Response message (RSP channel)
Response message (RSP channel)
Figure 3: Key to transaction flow diagram conventions
In Figure 3:
• Alternative transaction flows are grouped together with a dotted line separating the different alternative flows.
• Optional transaction flows are grouped together.
• Color-coded arrows are used to represent the different channels.
• Bold arrows represent messages that could require multiple packets to transfer.
Signals
The signal conventions are:
Signal level The level of an asserted signal depends on whether the signal is active-HIGH or active-LOW.
Asserted means:
– HIGH for active-HIGH signals.
– LOW for active-LOW signals.
Lowercase n At the start or end of a signal name denotes an active-LOW signal.
Numbers
Numbers are normally written in decimal. Binary numbers are preceded by 0b, and hexadecimal numbers by 0x.
Both are written in a monospace font.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xxiv
```

## PDF page 25

```text
Using this specification
Additional reading
Additional reading
This section lists publications by Arm and by third parties.
See Arm Developer, http://developer.arm.com for access to Arm documentation.
Arm publications
• AMBA® AXI Protocol Specification (ARM IHI 0022).
• AMBA® CHI Chip-to-Chip (C2C) Architecture Specification(ARM IHI 0098).
• Arm® Architecture Reference Manual for A-profile architecture(ARM DDI 0487).
• Arm® Realm Management Extension (RME) System Architecture (ARM DEN 0129).
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xxv
```

## PDF page 26

```text
Using this specification
Feedback
Feedback
Arm welcomes feedback on its documentation.
Feedback on this specification
If you have any comments or queries about our documentation, create a ticket at
https://support.developer.arm.com.
As part of the ticket, please include:
• The title (AMBA® CHI Architecture Specification).
• The number (ARM IHI 0050 Issue H).
• The section name to which your comments refer.
• The page number(s) to which your comments refer.
• A concise explanation of your comments.
Arm also welcomes general suggestions for additions and improvements.
Inclusive terminology commitment
Arm values inclusive communities. Arm recognizes that we and our industry have used terms that can be offensive.
Arm strives to lead the industry and create change.
Previous issues of this document included terms that can be offensive. We have replaced these terms. If you find
offensive terms in this document, please contact terms@arm.com.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
xxvi
```

## PDF page 27

```text
Part B
Specification
```

## PDF page 28

```text
Chapter B1
Introduction
This chapter introduces the CHI architecture and the terminology used throughout this specification. It contains
the following sections:
• B1.1 Architecture overview
• B1.2 Topology
• B1.3 Terminology
• B1.4 Transaction classification
• B1.5 Coherence overview
• B1.6 Component naming
• B1.7 Read data source
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
28
```

## PDF page 29

```text
Chapter B1. Introduction
B1.1. Architecture overview
B1.1 Architecture overview
The CHI architecture is a scalable, coherent hub interface and on-chip interconnect used by multiple components.
The CHI architecture allows for flexible topologies of component connections, driven by performance, power, and
area system requirements.
B1.1.1 Components
The components of CHI-based systems can comprise of:
• Standalone processors
• Processor clusters
• Graphic processors
• Memory controllers
• IO bridges
• PCIe subsystems
• Interconnects
B1.1.2 Key features
The key features of the architecture are:
• Scalable architecture, enabling modular designs that scale from small to large systems.
• Independent layered approach, comprising of Protocol, Network, and Link layer, with distinct functionalities.
• Packet-based communication.
• All transactions handled by an interconnect-based Home Node that co-ordinates required snoops, cache, and
memory accesses.
• The CHI coherence protocol supports:
– Coherency granule of 64-byte cache line.
– Snoop filter and directory-based systems for snoop scaling.
– Both MESI and MOESI cache models with forwarding of data from any cache state.
– Additional partial and empty cache line states.
• The CHI transaction set includes:
– Enriched transaction types that permit performance, area, and power efficient system cache
implementation.
– Support for atomic operations and synchronization within the interconnect.
– Support for the efficient execution of Exclusive accesses.
– Transactions for the efficient movement and placement of data, to move data in a timely manner closer
to the point of anticipated use.
– Virtual memory management through Distributed Virtual Memory (DVM) operations.
• Protocol resource management with Request Retry and Resource Planes.
• Support for end-to-end Quality of Service (QoS).
• Support for the Arm Memory Tagging Extension (MTE).
• Support for the Arm Realm Management Extension (RME).
• Configurable data width to meet the requirements of the system.
• ARM TrustZone™ support on a transaction-by-transaction basis.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
29
```

## PDF page 30

```text
Chapter B1. Introduction
B1.1. Architecture overview
• Optimized transaction flow for coherent writes with a producer-consumer ordering model.
• Error reporting and propagation across components and interconnect for system reliability and integrity.
• Handling sub cache line Data Errors using Data Poisoning and per byte error indication.
• Power-aware signaling on the component interface:
– Enabling flit-level clock gating.
– Component activation and deactivation sequence for clock-gate and power-gate control.
– Protocol activity indication for power and clock control.
B1.1.3 Architecture layers
Functionality is grouped into the following layers:
• Protocol
• Network
• Link
Table B1.1 describes the primary function of each layer.
Table B1.1: Layers of the CHI architecture
Layer Communication granularity Primary function
Protocol Transaction The Protocol layer is the topmost layer in the CHI architecture. The
function of the Protocol layer is to:
– Generate and process requests and responses at the protocol
nodes.
– Define the permitted cache state transitions at the protocol
nodes that include caches.
– Define the transaction flows for each request type.
– Manage the protocol level flow control.
Network Packet The function of the Network layer is to:
– Packetize the protocol message.
– Determine the source and target node IDs required to route the
packet over the interconnect to the required destination and add
to the packet.
Link Flit The function of the Link layer is to:
– Provide flow control between network devices.
– Manage link channels to provide deadlock-free switching
across the network.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
30
```

## PDF page 31

```text
Chapter B1. Introduction
B1.2. Topology
B1.2 Topology
The CHI architecture is primarily topology-independent. However, certain topology-dependent optimizations are
included in this specification to make implementation more efficient. Figure B1.1 shows three examples of
topologies selected to show the range of interconnect bandwidth and scalability options that are available.
Ring
4×4 Mesh
0 1 2 33210
7654
111098
15141312
Protocol node such as processor complex, memory controller, or IO complex
Router
3
2
1
0
4×4
Crossbar
7654
Figure B1.1: Example interconnect topologies
Crossbar Crossbar topology is simple to build and naturally provides an ordered network with low latency.
Crossbar topology is suitable where the wire counts are still relatively small. Crossbar topology is
suitable for an interconnect with a small number of nodes.
Ring Ring topology provides a trade-off between interconnect wiring efficiency and latency. The latency
increases linearly with the number of nodes on the ring. Ring topology is suitable for a medium sized
interconnect.
Mesh Mesh topology provides greater bandwidth at the cost of more wires. Mesh topology is very modular
and can be easily scaled to larger systems by adding more rows and columns of switches. Mesh
topology is suitable for a larger scale interconnect.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
31
```

## PDF page 32

```text
Chapter B1. Introduction
B1.3. Terminology
B1.3 Terminology
The following terms have a specific meaning within this specification:
Transaction
A transaction carries out a single operation. Typically, a transaction either reads from memory or writes
to memory.
Message
A message is a protocol layer term that defines the granule-of-exchange between two components.
Examples are:
• Request
• Data response
• Snoop request
A single Data response message can be made up of a number of packets.
Packet
A packet is the granule-of-transfer over the interconnect between endpoints. A message could be made
up of one or more packets. For example, a single Data response message can be made up of 1 to 4
packets. Each packet contains routing information, such as destination ID and source ID, allowing for
independent routing over the interconnect.
Flit
FLow control unIT (Flit) is the smallest flow control unit. A packet can be made up of one or more flits.
All the flits of a given packet follow the same path through the interconnect.
Note
For CHI, all packets consist of a single flit.
Phit
PHysical layer transfer unIT (Phit) is one transfer between two adjacent network devices. A flit can be
made up of one or more phits.
Note
For CHI, all flits consist of a single phit.
PoS
Point of Serialization (PoS) is a point within the interconnect where the ordering between requests from
different agents is determined.
PoC
Point of Coherence (PoC) is a point at which all agents that can access memory are guaranteed to see
the same copy of a memory location. In a typical CHI-based system, the PoC is the HN-F in the
interconnect.
PoE
Point of Encryption (PoE) is the point in a memory system where any writes that have reached that
point are encrypted.
PoP
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
32
```

## PDF page 33

```text
Chapter B1. Introduction
B1.3. Terminology
Point of Persistence(PoP) is a potential point in a memory system at or beyond the Point of Coherency,
where a write to memory is maintained when system power is removed, and reliably recovered when
power is restored to the affected locations in memory.
PoDP
Point of Deep Persistence(PoDP) is a point in the memory system where the data is preserved even
when the power and the back up battery fail simultaneously.
PoPA
Point of Physical Aliasing (PoPA) is a point where updates to a location in one Physical Address Space
(PAS) are visible to all other Physical Address Spaces.
PoPS
Point of Physical Storage(PoPS) is a point furthest in the memory hierarchy away from a PE or another
observer to which a write transaction could propagate, that is, memory.
Downstream cache
A downstream cache is defined from the perspective of a Request Node. A downstream cache for a
Request is a cache that the Request accesses using CHI request transactions. A Request Node can send
a request with data to allocate data into a downstream cache.
Requester
A component that starts a transaction by issuing a request message. The term Requester can be used for
a component that independently initiates transactions. The term Requester can also be used for an
interconnect component that issues a downstream Request message independently or as a side-effect of
other transactions that are occurring in the system.
Completer
Any component that responds to a received transaction from another component. A Completer can
either be an interconnect component, such as a Home Node or a Miscellaneous Node, or a component,
such as a Subordinate, that is outside of the interconnect.
Subordinate
An agent that receives transactions and completes them appropriately. Typically, a Subordinate is the
most downstream agent in a system. A Subordinate can also be referred to as a Completer or Endpoint.
Endpoint
Another name for a Subordinate component. An Endpoint is the final destination for a transaction.
Protocol Credit
A credit, or guarantee, from a Completer that it will accept a transaction.
Link layer Credit, L-Credit
A credit, or guarantee, that a flit will be accepted on the other side of the link. An L-Credit is a credit
for a single hop at the Link layer.
ICN
Interconnect (ICN) is the CHI transport mechanism that is used for communication between protocol
nodes. An interconnect can include an IMPLEMENTATION SPECIFIC fabric of switches connected in a
ring, mesh, crossbar, or another topology. The interconnect can also include protocol nodes, such as
Home Node and Miscellaneous Node.
IPA
Intermediate Physical Address (IPA). In two-stage address translation:
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
33
```

## PDF page 34

```text
Chapter B1. Introduction
B1.3. Terminology
• Stage 1 provides an Intermediate Physical Address (IPA).
• Stage 2 provides the Physical Address (PA).
RN
Request Node (RN) generates protocol transactions, including reads and writes, to the interconnect.
HN
Home Node (HN) is a node within the interconnect that receives protocol transactions from Request
Nodes, completes the required coherency action, and returns a response.
SN
Subordinate Node (SN) is a node that receives a Request from a Home Node, completes the required
action, and returns a response.
MN
Miscellaneous or Misc Node (MN) is a node located within the interconnect that receives DVM
messages from Request Nodes, completes the required action, and returns a response.
IO Coherent node
A Request Node that generates a subset of Snoopable requests in addition to Non-snoopable requests.
The Snoopable requests that an IO Coherent node generates do not result in the caching of the received
data in a coherent state. Therefore, an IO Coherent node does not receive any Snoop requests.
Snoopee
A Request Node that is receiving a snoop.
Write-Invalidate protocol
A protocol in which a Request Node writing to a shared cache line in the system must invalidate all
copies before proceeding with the write. The CHI protocol is a Write-Invalidate protocol.
In a timely manner
The protocol cannot define an absolute time within which something must occur. A sufficiently idle
system can progress and complete without explicit action.
Inapplicable
A field value that indicates that the field is not used in the processing of the message.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
34
```

## PDF page 35

```text
Chapter B1. Introduction
B1.4. Transaction classification
B1.4 Transaction classification
The protocol transactions that this specification supports, and their major classification, are listed in Table B1.2.
Table B1.2: Transaction classification
Classification Supporting transactions
Read ReadNoSnp
ReadNoSnpSep
ReadOnce
ReadOnceCleanInvalid
ReadOnceMakeInvalid
ReadClean
ReadNotSharedDirty
ReadShared
ReadUnique
ReadPreferUnique
MakeReadUnique
Dataless CleanUnique
MakeUnique
Evict
StashOnceUnique
StashOnceSepUnique
StashOnceShared
StashOnceSepShared
CleanShared
CleanSharedPersist
CleanSharedPersistSep
CleanInvalid
CleanInvalidPoPA
CleanInvalidStorage
MakeInvalid
Write WriteNoSnpPtl
WriteNoSnpFull
WriteNoSnpZero
WriteNoSnpDef
WriteUniquePtl
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
35
```

## PDF page 36

```text
Chapter B1. Introduction
B1.4. Transaction classification
Table B1.2 – Continued from previous page
Classification Supporting transactions
WriteUniqueFull
WriteUniqueZero
WriteUniquePtlStash
WriteUniqueFullStash
WriteBackPtl
WriteBackFull
WriteCleanFull
WriteEvictFull
WriteEvictOrEvict
Combined Write WriteNoSnpPtlCleanInv
WriteNoSnpPtlCleanSh
WriteNoSnpPtlCleanShPerSep
WriteNoSnpPtlCleanInvPoPA
WriteNoSnpFullCleanInv
WriteNoSnpFullCleanSh
WriteNoSnpFullCleanShPerSep
WriteNoSnpFullCleanInvPoPA
WriteNoSnpFullCleanInvStrg
WriteUniquePtlCleanSh
WriteUniquePtlCleanShPerSep
WriteUniqueFullCleanSh
WriteUniqueFullCleanShPerSep
WriteUniqueFullCleanInvStrg
WriteBackFullCleanInv
WriteBackFullCleanSh
WriteBackFullCleanShPerSep
WriteBackFullCleanInvPoPA
WriteBackFullCleanInvStrg
WriteCleanFullCleanSh
WriteCleanFullCleanShPerSep
Atomic AtomicStore
AtomicLoad
AtomicSwap
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
36
```

## PDF page 37

```text
Chapter B1. Introduction
B1.4. Transaction classification
Table B1.2 – Continued from previous page
Classification Supporting transactions
AtomicCompare
Other DVMOp
PrefetchTgt
PCrdReturn
Snoop SnpOnceFwd
SnpOnce
SnpStashUnique
SnpStashShared
SnpCleanFwd
SnpClean
SnpNotSharedDirtyFwd
SnpNotSharedDirty
SnpSharedFwd
SnpShared
SnpUniqueFwd
SnpUnique
SnpPreferUniqueFwd
SnpPreferUnique
SnpUniqueStash
SnpCleanShared
SnpCleanInvalid
SnpMakeInvalid
SnpMakeInvalidStash
SnpQuery
SnpDVMOp
Table B1.3 shows the representations of transactions.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
37
```

## PDF page 38

```text
Chapter B1. Introduction
B1.4. Transaction classification
Table B1.3: Representation of transactions
Specification use Represents collectively
ReadOnce* ReadOnce, ReadOnceCleanInvalid, and ReadOnceMakeInvalid
WriteNoSnp WriteNoSnpPtl and WriteNoSnpFull
WriteUnique WriteUniquePtl, WriteUniqueFull, WriteUniquePtlStash, and WriteUniqueFullStash
WriteNoSnpPtl* WriteNoSnpPtl, WriteNoSnpPtlCleanInv, WriteNoSnpPtlCleanInvPoPA,
WriteNoSnpPtlCleanSh, and WriteNoSnpPtlCleanShPerSep
WriteNoSnp*CMO WriteNoSnpPtlCleanInv, WriteNoSnpPtlCleanInvPoPA, WriteNoSnpPtlCleanSh,
WriteNoSnpPtlCleanShPerSep, WriteNoSnpFullCleanInv,
WriteNoSnpFullCleanInvPoPA, WriteNoSnpFullCleanInvStrg,
WriteNoSnpFullCleanSh, and WriteNoSnpFullCleanShPerSep
WriteUnique*CMO WriteUniquePtlCleanSh, WriteUniquePtlCleanShPerSep, WriteUniqueFullCleanSh,
WriteUniqueFullCleanShPerSep, and WriteUniqueFullCleanInvStrg
WriteBack*CMO WriteBackFullCleanInv, WriteBackFullCleanSh, WriteBackFullCleanShPerSep,
WriteBackFullCleanInvPoPA, and WriteBackFullCleanInvStrg
WriteBack WriteBackPtl and WriteBackFull
StashOnce StashOnceUnique and StashOnceShared
StashOnceSep StashOnceSepUnique and StashOnceSepShared
StashOnce* StashOnce and StashOnceSep
StashOnce*Shared StashOnceShared and StashOnceSepShared
StashOnce*Unique StashOnceUnique and StashOnceSepUnique
CleanSharedPersist* CleanSharedPersist and CleanSharedPersistSep
Atomic* AtomicStore, AtomicLoad, AtomicSwap, AtomicCompare
SnpStash* SnpStashUnique and SnpStashShared
DBIDResp* DBIDResp and DBIDRespOrd
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
38
```

## PDF page 39

```text
Chapter B1. Introduction
B1.5. Coherence overview
B1.5 Coherence overview
Hardware coherency enables system components to share memory without the requirement of software cache
maintenance to maintain coherency.
Regions of memory are coherent if writes to the same memory location by two components are observable in the
same order by all components.
B1.5.1 Coherency model
Figure B1.2 shows an example coherent system that includes three Requester components, each with a local cache
and coherent protocol node. The protocol permits cached copies of the same memory location to reside in the local
cache of one or more Requester components.
Coherent interconnect (ICN)
RN-F
Requester 1
RN-F
Requester 2
RN-F
Requester 3
SN-F
Subordinate 1
ICN
Optional 
cache
CacheCacheCache
Main 
memory
Cache
Figure B1.2: Example coherency model
The coherence protocol enforces that no more than one copy of a data value exists whenever a store occurs at an
address location. The coherence protocol ensures all Requesters observe the correct data value at any given
address location. After each store to a location, other Requesters can obtain a new copy of the data for their own
local cache to permit multiple cached copies to exist.
A cache line is defined as a 64-byte aligned memory region. All coherency is maintained at cache line granularity.
Main memory is only required to be updated before a copy of the memory location is no longer held in any cache.
The coherence protocol does not require main memory to be up to date at all times.
Note
Although not a requirement, it is permitted to update main memory while cached copies still exist.
The coherence protocol enables Requester components to determine whether a cache line is the only copy of a
particular memory location or if other copies of the same location exist. The coherence protocol ensures:
• If a cache line is the only copy, a Requester component can change the value of the cache line without
notifying any other Requester components in the system.
• If a cache line can also be present in another cache, a Requester component must notify the other caches
using an appropriate transaction.
B1.5.2 Cache state model
When a component accesses a cache line, the protocol defines cache states to determine whether an action is
required. Each cache state is based on the following cache line characteristics:
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
39
```

## PDF page 40

```text
Chapter B1. Introduction
B1.5. Coherence overview
Valid, Invalid When Valid, the cache line is present in the cache.
When Invalid, the cache line is not present in the cache.
Unique, Shared When Unique, the cache line exists only in the Unique cache.
When Shared, the cache line can exist in more than one cache. The cache line is not
guaranteed to exist in more than once cache.
Clean, Dirty When Clean, the cache does not have responsibility for updating main memory.
When Dirty, the cache line has been modified with respect to main memory. The Dirty
cache must ensure that main memory is eventually updated.
Full, Partial, Empty A Full cache line has all bytes valid.
A Partial cache line can have some bytes valid, where some include none or all bytes.
An Empty cache line has no bytes valid.
Figure B1.3 shows the seven state cache model. B4.1 Cache line states gives further information about each cache
state.
A valid cache state name that is not Partial or Empty is considered to be Full. In Figure B1.3, UC, UD, SC, and SD
are all Full cache line states.
I
UC
UCE
UD
UDP
SC
SD
Unique Shared
Valid Invalid
Clean
Dirty
Figure B1.3: Cache state model
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
40
```

## PDF page 41

```text
Chapter B1. Introduction
B1.6. Component naming
B1.6 Component naming
The components in the CHI protocol are classified by node type:
RN Request Node. Generates protocol transactions, including reads and writes, to the interconnect. A Request
Node is further categorized as:
RN-F Fully Coherent Request Node:
– Includes a hardware-coherent cache.
– Permitted to generate all transactions defined by the protocol, except for ReadNoSnpSep.
– Supports all Snoop transactions.
RN-D IO Coherent Request Node with DVM support:
– Does not include a hardware-coherent cache.
– Receives DVM transactions.
– Generates a subset of transactions defined by the protocol. See C3.1 Request Nodes Subset for
further details.
RN-I IO Coherent Request Node:
– Does not include a hardware-coherent cache.
– Does not receive DVM transactions.
– Generates a subset of transactions defined by the protocol. See C3.1 Request Nodes Subset for
further details.
– Does not require snoop functionality.
HN Home Node. Node located within the interconnect that receives protocol transactions from Request Nodes.
A Home Node is further categorized as:
HN-F Fully Coherent Home Node:
– Expected to receive all request types, except DVMOp.
– Includes a Point of Coherence (PoC) that manages coherency by snooping the required RN-F
nodes, consolidating the Snoop responses for a transaction, and sending a single response to the
requesting Request Node.
– Expected to be the Point of Serialization (PoS) that manages order between memory requests.
– Could include a directory or snoop filter to reduce redundant snoops.
Note
IMPLEMENTATION SPECIFIC , can include an integrated interconnect cache.
HN-I Non-coherent Home Node:
– Processes a limited subset of request types defined by the protocol.
– Does not include a PoC and is not capable of processing a Snoopable request. On receipt of a
Snoopable request, HN-I must respond with a protocol compliant message.
– Expected to be the PoS that manages order between IO requests targeting the IO subsystem.
MN Miscellaneous Node.
Receives a DVM transaction from a Request Node, completes the required action, and returns a
response.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
41
```

## PDF page 42

```text
Chapter B1. Introduction
B1.6. Component naming
SN Subordinate Node. Receives a request from a Home Node, completes the required action, and returns a
response. A Subordinate Node is further categorized as:
SN-F Subordinate Node.
– Used for Normal memory.
– Can process Non-snoopable Read, Write, and Atomic requests, including exclusive variants of
them, and Cache Maintenance Operation (CMO) requests. See C3.2 Subordinate Nodes Subset for
further details.
SN-I Subordinate Node.
– Used for peripherals or Normal memory.
– Can process Non-snoopable Read, Write, and Atomic requests, including exclusive variants of
them, and CMO requests. See C3.2 Subordinate Nodes Subset for further details.
Figure B1.4 shows various protocol node types connected through an interconnect.
ICN
HN-I HN-F
MN
HN-F
RN-F0 RN-F1 RN-F2
SN-I SN-F
RN-I
Requesters
(Fully coherent)
Subordinates
Subordinate
(Normal Memory)
Subordinate
(Peripheral or Normal 
Memory, or both)
Requester
(IO coherent)
Figure B1.4: Protocol node examples
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
42
```

## PDF page 43

```text
Chapter B1. Introduction
B1.7. Read data source
B1.7 Read data source
In a CHI-based system, a Read request can obtain data from different sources. Figure B1.5 shows that these
sources are:
• Cache within the interconnect
• Subordinate Node
• Peer RN-F
Requester
ICN
Data
Req
RN-F
Snoop
Data
RN-F
Home
Subordinate
Data
Req Data providers
Figure B1.5: Possible Data providers for a Read request
One option for the Home is to request that the RN-F or Subordinate Node returns data only to Home. The Home,
in turn, forwards a copy of the received data to the Requester. A hop in obtaining Data in the Read transaction flow
can be removed if the Data provider is enabled to forward the Data response directly to the Requester instead of
through the Home.
Several techniques can be used to reduce the number of hops to complete a transaction. The reduction in the
number of hops results in Read and Write latency savings and interconnect bandwidth utilization. The techniques
are categorized as:
Direct Memory Transfer (DMT)
Defines the feature that permits the Subordinate Node to send data directly
to the Requester.
Direct Cache Transfer (DCT)
Defines the feature which permits a peer RN-F to send data directly to the
Requester. The Data provider in the DCT Read transaction flows has to
inform the Home that Data has been sent to the Requester. In some cases,
the Data provider also has to send a copy of data to the Home.
Direct Write-data Transfer (DWT)
Defines the feature which permits the requesting Request Node to send
write data directly to the Subordinate Node.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
43
```

## PDF page 44

```text
Chapter B2
Transactions
This chapter gives an overview of the communication channels between nodes, the associated packet fields, and
the transaction structure. It contains the following sections:
• B2.1 Channels overview
• B2.2 Channel fields
• B2.3 Transaction structure
• B2.4 Transaction identifier fields
• B2.6 Multi-request
• B2.5 Transaction identifier field flows
• B2.7 Ordering
• B2.8 Address, Control, and Data
• B2.9 Data transfer
• B2.10 Request Retry
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
44
```

## PDF page 45

```text
Chapter B2. Transactions
B2.1. Channels overview
B2.1 Channels overview
This section uses shorthand naming for the channels to describe the transaction structure. Table B2.1 shows the
shorthand name and the physical channel name that exists on the Request Node or Subordinate Node component.
Communication between nodes is channel-based. Table B2.1 shows the channel naming and the channel
designations at the Request Nodes and Subordinate Nodes.
See B13.4 Channel for the mapping of physical channels on the Request Node and Subordinate Node components.
Table B2.1: Channel naming and designation at the Request Node and Subordinate Node
Channel Request Node channel designation Subordinate Node channel designation
REQ TXREQ. Outbound Request. RXREQ. Inbound Request.
WDAT TXDAT. Outbound Data.
Use for write data, atomic data, snoop data,
forward data.
RXDAT. Inbound Data.
Use for write data, atomic data.
SRSP TXRSP. Outbound Response.
Use for snoop response and completion
acknowledge.
-
CRSP RXRSP. Inbound Response.
Use for responses from the Completer.
TXRSP. Outbound Response.
Use for responses from the Completer.
RDAT RXDAT. Inbound Data.
Use for read data, atomic data.
TXDAT. Outbound Data.
Use for read data, atomic data.
SNP RXSNP. Inbound Snoop request. -
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
45
```

## PDF page 46

```text
Chapter B2. Transactions
B2.2. Channel fields
B2.2 Channel fields
This section gives a brief overview of the channel fields and indicates which fields affect the transaction structure.
The associated fields with each channel are described in the following sections:
• B2.2.1 Transaction request fields
• B2.2.2 Response fields
• B2.2.3 Snoop request fields
• B2.2.4 Data fields
The term Transaction Structure is used to describe the different packets that form a transaction. The transaction
structure can vary depending on several factors.
B2.2.1 Transaction request fields
Table B2.2 shows the Request fields associated with a Request packet.
More information on the different transaction structures can be found in B2.3 Transaction structure and B13.9 Flit
packet definitions.
Table B2.2: Request channel fields
Field Affects structure Description
QoS No Quality of Service priority. Specifies one of 16 possible priority levels
for the transaction with ascending values of QoS indicating higher
priority levels. See B13.10.1 Quality of Service, QoS.
TgtID No Target Identifier. The node identifier of the port on the component to
which the packet is targeted. See B2.4.1 Target Identifier, TgtID, and
Source Identifier, SrcIDand B3.1 System Address Map, SAM.
SrcID No Source Identifier. The node identifier of the port on the component from
which the packet was sent. See B2.4.1 Target Identifier, TgtID, and
Source Identifier, SrcID.
TxnID No Transaction Identifier. A transaction has a unique transaction identifier
per source node. See B2.4.2 Transaction Identifier, TxnID.
ReturnNID No Return Node Identifier. The recipient node identifier for the Data
response, Persist response, or TagMatch response. See B2.4.10 Return
Node Identifier, ReturnNID.
StashNID No Stash Node Identifier. The node identifier of the Stash target. See B2.4.9
Stash Node Identifier, StashNIDand B13.10.9 Stash Node Identifier,
StashNID.
DataTarget No Data target. Forwards placement and usage hints from Requesters to the
caches in the interconnect. See B11.3 Data Target.
StashNIDValid Yes Stash Node Identifier Valid. Indicates that the StashNID field has a valid
Stash target value. See B13.10.10 Stash Node Identifier Valid,
StashNIDValid.
Endian No Endianness. Indicates the endianness of data in the data packet for
Atomic transactions. See B2.9.6.3 Endianness.
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
46
```

## PDF page 47

```text
Chapter B2. Transactions
B2.2. Channel fields
Table B2.2 – Continued from previous page
Field Affects structure Description
Deep No Deep persistence. Indicates that the Persist response must not be sent
until all earlier writes are written to the final destination. See B4.2.2.2.3
Deep Persistent CMO.
PrefetchTgtHint No PrefetchTgt Hint. Indicates that the original request had an associated
PrefetchTgt request. A Chip-to-Chip link receiver can use this field to
recreate the PrefetchTgt request if it is known that the original
PrefetchTgt was dropped at the Chip-to-Chip link transmitter. See
B13.10.57 PrefetchTgt Hint, PrefetchTgtHint.
ReturnTxnID No Return Transaction Identifier. The unique transaction identifier that
conveys the value of TxnID in the data response from the Subordinate.
See B2.4.4 Return Transaction Identifier, ReturnTxnID.
StashLPIDValid No Stash Logical Processor Identifier Valid. Indicates that the StashLPID
field value is the Stash target. See B13.10.12 Stash Logical Processor
Identifier Valid, StashLPIDValid.
StashLPID No Stash Logical Processor Identifier. The identifier of the Logical
Processor (LP) at the Stash target. See B13.10.11 Stash Logical
Processor Identifier, StashLPID.
Opcode Yes Request opcode. Specifies the transaction type and is the primary field
that determines the transaction structure. See B4.2 Request types and
B13.10.18.1 REQ channel opcodes.
MultiReq Yes Multi-request transaction. Used with NumReq to indicate the total
amount of Data associated with the transaction. See B13.10.64
MultiReq.
NumReq Yes Number of requests. Used with MultiReq to indicate the total amount of
Data associated with the transaction. See B13.10.65 NumReq.
Size Yes Data size. Specifies the size of the data associated with the transaction
and determines the number of data packets within the transaction. See
B2.9 Data transfer.
Addr No Address. The address of the memory location being accessed for Read
and Write requests. See B2.8.1 Address and B13.10.20 Address, Addr.
PAS No Physical Address Space. Indicates the PAS that the transaction is
targeting. See B13.10.68 PAS.
LikelyShared No Likely Shared. Provides an allocation hint for downstream caches. See
B2.8.5 Likely Shared.
AllowRetry Yes Allow Retry. Determines if a target that supports Request Retry is
permitted to give a RetryAck response. See B2.10 Request Retry and
Retry_Support.
Order Yes Order requirement. Determines the ordering requirement for a request
with respect to other requests from the same agent. See B2.7 Ordering.
PCrdType No Protocol Credit Type. Indicates the type of Protocol Credit being used
by a request when the B13.10.31 Allow Retry, AllowRetry field is 0. See
B2.10 Request Retry.
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
47
```

## PDF page 48

```text
Chapter B2. Transactions
B2.2. Channel fields
Table B2.2 – Continued from previous page
Field Affects structure Description
MemAttr No Memory attribute. Determines the memory attributes associated with the
transaction. See B2.8.3 Memory Attributes.
SnpAttr No Snoop attribute. Specifies the snoop attributes associated with the
transaction. See B2.8.6 Snoop attribute.
DoDWT Yes Do Direct Write Transfer. Supports Direct Write-data Transfer and the
handling of Combined Writes. See B13.10.24 Do Direct Write Transfer,
DoDWT.
PGroupID No Persistence Group Identifier. Indicates the set of CleanSharedPersistSep
transactions to which the request applies. See B13.10.8 Persistence
Group Identifier, PGroupID.
StashGroupID No Stash Group Identifier. Indicates the set of StashOnceSep transactions to
which the request applies. See B13.10.13 Stash Group Identifier,
StashGroupID.
TagGroupID No Tag Group Identifier. Precise contents are IMPLEMENTATION SPECIFIC .
Typically expected to contain Exception Level,Translation Table Base
Register (TTBR) value, and CPU identifier. See B13.10.41 Tag Group
Identifier, TagGroupID.
LPID No Logical Processor Identifier. Used with the SrcID field to uniquely
identify the LP that generated the request. See B2.4.7 Logical Processor
Identifier, LPID.
Excl No Exclusive access. Indicates that the corresponding transaction is an
Exclusive access transaction. See Chapter B6 Exclusive accesses.
SnoopMe No Snoop Me. Indicates that Home must determine whether to send a
snoop to the Requester during an Atomic transaction. See B2.3.3
Atomic transactions.
CAH Yes CopyAtHome. In CopyBack requests, CAH indicates to the Home if the
Requester modifies the line or MTE tags since Home indicated a copy of
the line was kept. See B13.10.28 CopyAtHome, CAH.
ExpCompAck Yes Expect CompAck. Indicates that the transaction includes a completion
acknowledge message. See B2.3 Transaction structure and B2.7
Ordering.
TagOp Yes Tag Operation. Indicates the operation to be performed and on the tags
present in the corresponding DAT channel. See B13.10.38 Tag
Operation, TagOp.
TraceTag No Trace Tag. Provides extra support for the debugging, tracing, and
performance measurement of systems. See Chapter B11 System Control,
Debug, Trace, and Monitoring.
MPAM No Memory System Resource Partitioning and Monitoring. Efficiently
utilizes the memory resources among users and monitors their use. See
B11.4 MPAM.
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
48
```

## PDF page 49

```text
Chapter B2. Transactions
B2.2. Channel fields
Table B2.2 – Continued from previous page
Field Affects structure Description
PBHA No Page-based Hardware Attributes. 4 bits from the translation tables that
can be used for IMPLEMENTATION DEFINED hardware control. See
B11.5 Page-based Hardware Attributes.
MECID No Memory Encryption Context Identifier. Used by a memory encryption
engine as an index into a table of encryption contexts, either keys or
tweaks, that contribute to the external memory encryption. See B10.6
Memory Encryption Contexts, MEC.
StreamID No Stream Identifier. Used as a unique identifier of a stream of requests
originating from one or a set of Requesters associated with the same
System MMU context. See B13.10.62 Stream Identifier, StreamID.
SecSID1 No Security State. Qualifies the Security state of the StreamID. See
B13.10.63 Stream Identifier Security State, SecSID1
RSVDC No User-defined. See B13.10.60 Reserved for Customer Use, RSVDC.
B2.2.2 Response fields
Table B2.3 describes the fields associated with a Response packet.
Table B2.3: Response packet fields
Field Description
QoS Quality of Service priority. As defined in Table B2.2. See B11.1 Quality
of Service (QoS) mechanism.
TgtID Target Identifier. As defined in Table B2.2. See B2.4.1 Target Identifier,
TgtID, and Source Identifier, SrcID.
SrcID Source Identifier. As defined in Table B2.2. See B2.4.1 Target Identifier,
TgtID, and Source Identifier, SrcID.
TxnID Transaction Identifier. As defined in Table B2.2. See B2.4.2 Transaction
Identifier, TxnID.
Opcode Response opcode. Specifies response type. See B13.10.18.2 RSP
channel opcodes.
RespErr Response Error status. As defined in Table B2.5. See Chapter B6
Exclusive accesses and B9.1.2 Error response fields.
Resp Response status. As defined in Table B2.5. See B4.5 Response types.
FwdState Forward State. As defined in Table B2.5. See B13.10.47 Forward State,
FwdState.
DataPull Data Pull. As defined in Table B2.5. See B7.1.1 Snoop requests and
Data Pull.
CBusy Completer Busy. As defined in Table B2.5. See B11.6 Completer Busy.
DBID Data Buffer Identifier. As defined in Table B2.5. See B2.4.3 Data Buffer
Identifier, DBIDand B2.7 Ordering.
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
49
```

## PDF page 50

```text
Chapter B2. Transactions
B2.2. Channel fields
Table B2.3 – Continued from previous page
Field Description
PGroupID Persistence Group Identifier. As defined in Table B2.2. See B13.10.8
Persistence Group Identifier, PGroupID.
StashGroupID Stash Group Identifier. As defined in Table B2.2. See B13.10.13 Stash
Group Identifier, StashGroupID.
TagGroupID Tag Group Identifier. As defined in Table B2.2. See B13.10.41 Tag
Group Identifier, TagGroupID.
PCrdType Protocol Credit Type. See B2.10.2.2 PCrdType.
TagOp Tag Operation. As defined in Table B2.2. See B13.10.38 Tag Operation,
TagOp.
TraceTag Trace Tag. As defined in Table B2.2. See Chapter B11 System Control,
Debug, Trace, and Monitoring.
CacheLineID Cache line identifier. See B13.10.66 CacheLineID.
B2.2.3 Snoop request fields
Table B2.4 shows the Snoop request fields. Many of the Snoop request fields are the same as fields defined for the
Request channel.
Table B2.4: Snoop request fields
Field Affects structure Description
QoS No Quality of Service priority. As defined in Table B2.2. See B11.1 Quality
of Service (QoS) mechanism.
SrcID No Source Identifier. As defined in Table B2.2. See B2.4.1 Target Identifier,
TgtID, and Source Identifier, SrcID.
TxnID No Transaction Identifier. As defined in Table B2.2. See B2.4.2 Transaction
Identifier, TxnID.
FwdNID No Forward Node Identifier. The node identifier of the original Requester.
See B2.4.12 Forward Node Identifier, FwdNID.
PBHA No Page-based Hardware Attributes. 4 bits from the translation tables that
can be used for IMPLEMENTATION DEFINED hardware control. See
B11.5 Page-based Hardware Attributes.
FwdTxnID No Forward Transaction Identifier. The transaction identifier used in the
Request by the original Requester. See B2.4.5 Forward Transaction
Identifier, FwdTxnID.
StashLPIDValid No Stash Logical Processor Identifier Valid. As defined in Table B2.2. See
B7.5 Stash messages.
StashLPID No Stash Logical Processor Identifier. As defined in Table B2.2. See B7.5
Stash messages.
VMIDExt No Virtual Machine Identifier Extension. See B8.3.3 Snoop DVMOp field
value restrictions.
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
50
```

## PDF page 51

```text
Chapter B2. Transactions
B2.2. Channel fields
Table B2.4 – Continued from previous page
Field Affects structure Description
Opcode Yes Snoop opcode. See B13.10.18.3 SNP channel opcodes.
Addr No Address. The address of the memory location being accessed for Snoop
requests. See B2.8.1 Address and B13.10.20 Address, Addr.
PAS No Physical Address Space. See B13.10.68 PAS.
DoNotGoToSD No Do Not Go To SD state. Controls Snoopee use of SD state. See B4.10
Do not transition to SD.
RetToSrc Yes Return to Source. Instructs the Receiver of the snoop to return data with
the Snoop response. See B4.9 Returning Data with Snoop response.
TraceTag No Trace Tag. As defined in Table B2.2. See Chapter B11 System Control,
Debug, Trace, and Monitoring.
MPAM No Memory System Resource Partitioning and Monitoring. As defined in
Table B2.2. See B11.4 MPAM.
MECID No Memory Encryption Context Identifier. Used by a memory encryption
engine as an index into a table of encryption contexts, either keys or
tweaks, that contribute to the external memory encryption. See B10.6
Memory Encryption Contexts, MEC.
Note
This specification does not define a TgtID field for the Snoop request. See B3.3 TgtID determination.
B2.2.4 Data fields
Table B2.5 describes the fields associated with a Data packet. Data packets can be sent on the RDAT or WDAT
channels. The fields in a Data packet do not affect the transaction structure.
Table B2.5: Data packet fields
Field Description
QoS Quality of Service priority. As defined in Table B2.2. See B11.1 Quality
of Service (QoS) mechanism.
TgtID Target Identifier. As defined in Table B2.2. See B2.4.1 Target Identifier,
TgtID, and Source Identifier, SrcID.
SrcID Source Identifier. As defined in Table B2.2. See B2.4.1 Target Identifier,
TgtID, and Source Identifier, SrcID.
TxnID Transaction Identifier. As defined in Table B2.2. See B2.4.2 Transaction
Identifier, TxnID.
HomeNID Home Node Identifier. The node identifier of the target of the CompAck
response to be sent from the Requester. See B2.4.11 Home Node
Identifier, HomeNID.
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
51
```

## PDF page 52

```text
Chapter B2. Transactions
B2.2. Channel fields
Table B2.5 – Continued from previous page
Field Description
MismatchedMECID Mismatched Memory Encryption Context ID. See B13.10.67
MismatchedMECID.
PBHA Page-based Hardware Attributes. 4 bits from the translation tables that
can be used for IMPLEMENTATION DEFINED hardware control. See
B11.5 Page-based Hardware Attributes.
Opcode Data opcode. Indicates, for example, if the data packet is related to a
Read transaction, a Write transaction, or a Snoop transaction. See
B13.10.18.4 DAT channel opcodes.
RespErr Response Error status. Indicates the error status associated with a data
transfer. See Chapter B6 Exclusive accesses and B9.1.2 Error response
fields.
Resp Response status. Indicates the cache line state associated with a data
transfer. See B4.5 Response types.
DataSource Data Source. The value indicates the source of the data in a Read Data
response, and can provide additional information on the state of the data
in a system. See B11.2 Data Source.
FwdState Forward State. Indicates the cache line state associated with a data
transfer to the Requester from the receiver of the snoop. See B13.10.47
Forward State, FwdState.
DataPull Data Pull. Indicates the inclusion of an implied Read request in the Data
response. See B7.1.1 Snoop requests and Data Pull.
CBusy Completer Busy. Indicates the current level of activity at the Completer.
See B11.6 Completer Busy.
MECID Memory Encryption Context Identifier. Used by a memory encryption
engine as an index into a table of encryption contexts, either keys or
tweaks, that contribute to the external memory encryption. See B10.6
Memory Encryption Contexts, MEC.
DBID Data Buffer Identifier. The identifier to be used as the TxnID in the
response to the Data message. See B2.4.3 Data Buffer Identifier, DBID
and B2.7 Ordering.
CCID Critical Chunk Identifier. Replicates the address offset of the original
Transaction request. See B2.9 Data transfer.
DataID Data Identifier. Provides the address offset of the data provided in the
packet. See B2.9 Data transfer.
CacheLineID Cache line identifier. See B13.10.66 CacheLineID.
TagOp Tag Operation. As defined in Table B2.2. See B13.10.38 Tag Operation,
TagOp.
Tag Memory Tag. Provides sets of 4-bit tags. Each tag is associated with an
aligned 16-byte of data See B13.10.39 Tag.
TU Tag Update. Indicates which of the Allocation Tags must be updated.
See B13.10.40 Tag Update, TU.
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
52
```

## PDF page 53

```text
Chapter B2. Transactions
B2.2. Channel fields
Table B2.5 – Continued from previous page
Field Description
TraceTag Trace Tag. As defined in Table B2.2. See Chapter B11 System Control,
Debug, Trace, and Monitoring.
CAH CopyAtHome. In responses from Home or a Snoopee, indicates if the
Home keeps a copy of the line that is provided to the Requester. Also
defined in Table B2.2. For more information, see B13.10.28
CopyAtHome, CAH.
NumDat Indicates the number of additional DAT packets represented by the
transferred packet when using Limited Data Elision. See B13.10.58
Number of DAT packets elided, NumDat.
Replicate Used in combination with NumDat to establish the field values for any
elided DAT packets. See B13.10.59 Replicate.
RSVDC User-defined. See B13.10.60 Reserved for Customer Use, RSVDC.
BE Byte Enable. For a data write, or data provided in response to a snoop,
indicates which bytes are valid. See B2.9 Data transfer.
Data Data payload. See B2.9 Data transfer.
DataCheck Data Check. Detects Data Errors in the DAT packet. See B9.2.2 Data
Check.
Poison Poison. Indicates that a set of data bytes has previously been corrupted.
See B9.2.1 Poison.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
53
```

## PDF page 54

```text
Chapter B2. Transactions
B2.3. Transaction structure
B2.3 Transaction structure
This section describes the ways that a transaction can complete. This section describes all the permitted options
that can be used by the various components that participate in a transaction.
All transaction types, except PCrdReturn and PrefetchTgt, can have a Retry sequence at the start of the transaction.
For ease of presentation, the Retry sequence is described separately, see B2.3.8 Retry.
Other independent transactions may need to be performed to complete certain transactions, such as a snoop or
memory transaction. These transactions are described separately in the later section, B2.3.9 Home Initiated
transactions.
Some transactions from Home to Subordinate support the use of a separate ReturnNID and ReturnTxnID field,
which allow certain responses to be returned to the original Requester rather than the Home. It is permitted, but
not required, to set the ReturnNID and ReturnTxnID fields, such that they are equal to the SrcID and TxnID. This
means all responses are returned to the Home. In this instance, the transaction from Home to Subordinate is
considered as if it were an independent transaction. See B2.3.9 Home Initiated transactions for more details.
Typically, a field or opcode in the request determines whether a particular message can be included in the
transaction flow, described as Optional. Optional messages do not express whether a sender chooses to send the
message.
The term Requester is always used to refer to the original Requester of a transaction in this section. Requester does
not refer to an intermediate agent that issues a secondary request to complete the original transaction. The term
Requester always refers to a Request Node, RN-F, RN-I, or RN-D.
In this section, a diagram with an arrow containing multiple message labels indicates any one of the messages can
be sent in a flow. Requirements of when a particular message can be used in the transaction flow can be derived
from elsewhere in the specification.
The flows described in this section are intended to include a complete description of the messages that can be
included in a transaction flow. The following is not included:
• The channel that is used for a particular transaction.
• A description of when a transaction can be issued or what the reason is for using a particular transaction.
• A description of which combinations of fields can be used in a request. Request fields are only highlighted
when they affect the options for completing a transaction.
Dependencies described in this section use the following approach:
• An implicit dependency exists for each component when first participating in a transaction sequence. Except
for the original Requester, any other component must receive a first message associated with a transaction
before any subsequent messages are sent for that transaction.
• Where a component sends multiple messages associated with the same transaction, the messages are
assumed to be sent in any order. The messages are also assumed to be received in any order, unless an
explicit dependency is described.
• Data transfers are shown in the diagrams as a single message. This message can consist of multiple data
transfers, see B2.9 Data transfer for more details. Where a dependency is described, the dependency is from
the first data transfer received, except when the dependency is explicitly stated to be different.
• Where a required or permitted dependency exists in one direction between two components, a dependency in
the opposite direction is not permitted. The text in this section only describes the dependency in one
direction.
• The amount of detail in a dependency rule is context dependent. When the source of the dependency and
what is dependent is obvious, the agents are not included.
• For any agent that has one or more outputs:
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
54
```

## PDF page 55

```text
Chapter B2. Transactions
B2.3. Transaction structure
– If the agent is the original Requester of the transaction, dependencies are described for each input to that
agent.
– If the agent is not the original Requester of the transaction, dependencies are described for each input to
that agent after the first input that agent received. Every output is considered dependent on the first input.
• This section does not describe all dependencies across different transactions, even when they are both to the
same address. See B2.7 Ordering and B4.11 Hazard conditions.
The conventions used to describe actions in this section are:
Issues Used only for the first message in a transaction, for example:
The Requester issues a WriteNoSnp request...
Sends A message sent by an agent in a direction away from the Requester.
Sends a downstream A message relayed by an intermediate agent in a direction away from the Requester,
for example:
The Home sends a downstream Read request to the Subordinate.
Returns A message sent by an agent in a direction towards the Requester.
Provides A message sent by an agent in response to a snoop, for example:
...provides a snoop response.
Permitted, but not required The action is not encouraged nor discouraged, and is compliant in either case.
Not permitted The action described would cause non-compliance to the specification. For
example:
The Home is not permitted to wait for...before sending...
B2.3.1 Read transactions
Read transactions are grouped into the following types:
• B2.3.1.1 Allocating Read
• B2.3.1.2 Non-allocating Read
B2.3.1.1 Allocating Read
Figure B2.1 shows the possible transaction flows for an Allocating Read transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
55
```

## PDF page 56

```text
Chapter B2. Transactions
B2.3. Transaction structure
Requester
Requester
Home
Home
Subordinate
Subordinate
Snoopee
Snoopee
ReadClean, ReadNotSharedDirty, ReadShared,
ReadUnique, ReadPreferUnique, MakeReadUnique
alt [1. Combined response from Home]
CompData
[2. Separate Data and Response from Home]
RespSepData
DataSepResp
[3. Combined response from Subordinate]
ReadNoSnp
opt [Order != 00]
ReadReceipt
CompData
[4. Response from Home, Data from Subordinate]
RespSepData
ReadNoSnpSep
ReadReceipt
DataSepResp
[5. Forwarding snoop]
Snp*Fwd
alt [5a. With response to Home]
CompData
SnpRespFwded
[5b. With data to Home]
CompData
SnpRespDataFwded
[5c. Failed through RSP channel, must use alternative]
SnpResp
Use alternative
[5d. Failed through DAT channel, must use alternative]
SnpRespData, SnpRespDataPtl
Use alternative
[6. MakeReadUnique only]
Comp
CompAck
Figure B2.1: Allocating Read
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
56
```

## PDF page 57

```text
Chapter B2. Transactions
B2.3. Transaction structure
The sequence for the Allocating Read transaction is:
• The transaction starts with the Requester issuing an Allocating Read request to the Home. The initial request
is one of the following:
– ReadClean
– ReadNotSharedDirty
– ReadShared
– ReadUnique
– ReadPreferUnique
– MakeReadUnique
• Alternatives 1-6 show different ways that the Home can process the transaction:
1. Combined response from Home
The Home returns a combined response and read data, CompData, to the Requester. Typically, this
option is used by the Home when data and response can be returned at the same time. An example is
when the data is cached locally.
2. Separate data and response from Home
The Home returns a separate response, RespSepData, and read data, DataSepResp, to the Requester.
Typically, this option is used by the Home when a response can be returned quicker than the Home can
provide the data.
3. Combined response from Subordinate
– The Home sends a downstream read request, ReadNoSnp, to the Subordinate.
– Optionally, when the Home requests a ReadReceipt response, the Subordinate returns a read receipt,
ReadReceipt, to the Home.
– The Subordinate returns a combined response and read data, CompData, to the Requester.
Typically, this option is used by the Home either to reduce the message count or reduce design
complexity.
4. Response from Home, Data from Subordinate
– The Home returns a separate response, RespSepData, to the Requester.
– The Home sends a downstream read data only request, ReadNoSnpSep, to the Subordinate.
– The Subordinate returns a read receipt, ReadReceipt, to the Home. It is permitted, but not required,
for the Home to wait for ReadReceipt from the Subordinate before sending RespSepData to the
Requester.
– The Subordinate returns read data, DataSepResp, to the Requester. Typically, this option is used by
the Home when a response can be returned quickly. However, the Home does not have the data
available and requires the Subordinate to return the data.
Note
In many circumstances, the Requester receives RespSepData far in advance to DataSepResp.
The Requester is permitted, but not required, to send the CompAck response after receiving
RespSepData without waiting for DataSepResp. The prompt response from the Requester,
and potentially receiving ReadReceipt around the same time, permits the Home to complete
the transaction faster than when using combined completion and data responses from the
Subordinate.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
57
```

## PDF page 58

```text
Chapter B2. Transactions
B2.3. Transaction structure
5. Forwarding snoop
– The Home requests a Snoopee to forward read data, Snp*Fwd, to the Requester. See B4.4 Request
transactions and corresponding Snoop requests to determine which Snp*Fwd transactions can be
used. Typically, this option is used by the Home when the data is not cached locally and the Home
determines that a Snoopee is likely to have a copy.
– Alternatives 5a-5d show how the Snoopee can process the transaction:
Alt 5a. With response to Home
– The Snoopee returns a combined response and read data, CompData, to the Requester.
– The Snoopee provides a snoop response, SnpRespFwded, to the Home. Typically, this option
is used by the Snoopee when data can be forwarded to the Requester and is not required to
provide a copy of data to the Home.
Alt 5b. With data to Home
– The Snoopee returns a combined response and read data, CompData, to the Requester.
– The Snoopee provides a snoop response with data, SnpRespDataFwded, to the Home.
Note
Typically, this option is used by the Snoopee when data can be forwarded to the Requester
while also providing a copy of data to the Home. For example, when the Snoopee holds a
Dirty copy of the cache line, but the data returned to the Requester must be Clean. This
option can also happen when the Home has requested a copy of the data.
Alt 5c. Failed through RSP channel, must use alternative
The Snoopee provides a snoop response, SnpResp, to the Home. The Home must use another
alternative described in this section to complete the transaction to the Requester.
Alt 5d. Failed through DAT channel, must use alternative
The Snoopee provides a snoop response with data, SnpRespData or SnpRespDataPtl, to the
Home. The Home must use another alternative described in this section to complete the
transaction to the Requester.
6. MakeReadUnique only
The Home returns a completion response, Comp, to the Requester. This option is only applicable for a
MakeReadUnique transaction when a read data message is not required.
• The transaction ends when the Requester sends a completion acknowledge, CompAck, to the Home. The
CompAck must only be sent after a CompData, Comp, or RespSepData is received. If RespSepData has been
received, it is permitted, but not required, for the Requester to wait for DataSepResp before sending
CompAck.
B2.3.1.2 Non-allocating Read
Figure B2.2 shows the possible transaction flows for a Non-allocating Read transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
58
```

## PDF page 59

```text
Chapter B2. Transactions
B2.3. Transaction structure
Requester
Requester
Home
Home
Subordinate
Subordinate
Snoopee
Snoopee
ReadNoSnp, ReadOnce,
ReadOnceCleanInvalid, ReadOnceMakeInvalid
alt [1. Combined response from Home]
opt [Order != 00]
ReadReceipt
CompData
[2. Separate Data and Response from Home]
RespSepData
DataSepResp
[3. Combined response from Subordinate]
opt [Order != 00]
ReadReceipt
ReadNoSnp
opt [Order != 00]
ReadReceipt
CompData
[4. Response from Home, Data from Subordinate]
RespSepData
ReadNoSnpSep
opt [Order != 00]
ReadReceipt
DataSepResp
[5. Forwarding snoop]
opt [Order != 00]
ReadReceipt
Snp*Fwd
alt [5a. With response to Home]
CompData
SnpRespFwded
[5b. With data to Home]
CompData
SnpRespDataFwded
[5c. Failed, must use alternative]
SnpResp
Use alternative
[5d. Failed, must use alternative]
SnpRespData, SnpRespDataPtl
Use alternative
opt [ExpCompAck == 1]
CompAck
Figure B2.2: Non-allocating Read
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
59
```

## PDF page 60

```text
Chapter B2. Transactions
B2.3. Transaction structure
The sequence for the Non-allocating Read transactions is:
• The transaction starts with the Requester issuing a Read request to the Home. The Non-allocating Read
transactions are:
– ReadNoSnp
– ReadOnce
– ReadOnceCleanInvalid
– ReadOnceMakeInvalid
The request contains the following fields which affect the transaction flow:
– Order
– ExpCompAck
• Alternatives 1-6 show how the Home can process the transaction. For a description of the typical use of the
different alternatives, see B2.3.1.1 Allocating Read.
1. Combined response from Home
– Optionally, when the original request has an ordering requirement, the Home returns a read receipt,
ReadReceipt, to the Requester.
– The Home returns a combined response and read data, CompData, to the Requester.
2. Separate data and response from Home
The Home returns a separate response, RespSepData, and read data, DataSepResp, to the Requester.
This alternative cannot be used if the request has an ordering requirement and a completion
acknowledge is not required.
3. Combined response from Subordinate
– Optionally, when the original request has an ordering requirement, the Home returns a read receipt,
ReadReceipt, to the Requester.
– The Home sends a downstream read request, ReadNoSnp, to the Subordinate.
– Optionally, when the Home requests a ReadReceipt response, the Subordinate returns ReadReceipt
to the Home. The Home must do this when a completion acknowledge is not required. It is
permitted, but not required, for the Home to wait for ReadReceipt from the Subordinate before
returning ReadReceipt to the Requester.
– The Subordinate returns a combined response and read data, CompData, to the Requester.
This alternative cannot be used if the request has an ordering requirement and a completion
acknowledge is not required.
4. Response from Home, data from Subordinate
– The Home returns a separate response, RespSepData, to the Requester and sends a downstream read
data only request, ReadNoSnpSep, to the Subordinate.
– Optionally, when the Home requests a ReadReceipt response, the Subordinate returns a read receipt,
ReadReceipt, to the Home. The Home must request a ReadReceipt unless the original request
indicates a requirement for both ordering and a completion acknowledge. It is permitted, but not
required, for the Home to wait for ReadReceipt from the Subordinate before returning RespSepData
to the Requester.
– The Subordinate returns read data, DataSepResp, to the Requester.
This alternative cannot be used if the request has an ordering requirement and a completion
acknowledge is not required.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
60
```

## PDF page 61

```text
Chapter B2. Transactions
B2.3. Transaction structure
5. Forwarding snoop
– Optionally, when the original request has an ordering requirement, the Home returns a read receipt,
ReadReceipt, to the Requester.
– The Home requests a Snoopee to forward read data, Snp*Fwd, to the Requester. See B4.4 Request
transactions and corresponding Snoop requests to determine which Snp*Fwd transactions can be
used.
– The alternatives, 5a-5d, show how the Snoopee can process the transaction:
Alt 5a. With response to Home
– The Snoopee provides a combined response and read data, CompData, to the Requester.
– The Snoopee provides a snoop response, SnpRespFwded, to the Home.
Alt 5b. With data to Home
– The Snoopee provides a combined response and read data, CompData, to the Requester.
– The Snoopee provides a Snoop response with data, SnpRespDataFwded, to the Home.
Alt 5c. Failed, must use alternative
– The Snoopee provides a snoop response, SnpResp, to the Home.
– The Home must use another alternative described in this section to complete the transaction to
the Requester.
Alt 5d. Failed, must use alternative
– The Snoopee provides a snoop response with data, SnpRespData or SnpRespDataPtl, to the
Home.
– The Home must use another alternative described in this section to complete the transaction to
the Requester.
– If the original request has ExpCompAck = 1, the Requester must only provide a CompAck response
after one of the following:
* At least one CompData packet is received.
* RespSepData, if the request does not have an ordering requirement.
The request is permitted, but not required, to wait for DataSepResp.
* RespSepData and at least one DataSepResp packet, if the request has an ordering requirement.
If the original request has an ordering requirement, it is permitted, but not required, for the Requester to wait for
ReadReceipt before sending CompAck.
Table B2.6 lists the permitted DMT and DCT transactions for ReadNoSnp and ReadOnce* from a Request Node.
The following key is used:
Y Yes, permitted
N No, not permitted
- The flow is not used in the transaction
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
61
```

## PDF page 62

```text
Chapter B2. Transactions
B2.3. Transaction structure
Table B2.6: Permitted DMT and DCT for ReadNoSnp and ReadOnce* from a Request Node
Order[1:0] ExpCompAck DMT DCT Notes
00 0 Y Y Home does not need to be notified of transaction completion.
For DMT, Home must request a ReadReceipt from the
Subordinate Node. The ReadReceipt from the Subordinate
Node confirms the Subordinate Node will not send a future
RetryAck response for the transaction.
1 Y Y When not using DMT, Home does not need to be notified of
transaction completion.
For DMT, to establish that the request from the Home to the
Subordinate Node will not see a future a RetryAck response:
• When using ReadNoSnp to the Subordinate Node,
Home must either request and receive a ReadReceipt
from the Subordinate Node or wait for the CompAck
response from the Request Node.
• When using ReadNoSnpSep to the Subordinate Node,
Home must request and receive a ReadReceipt from the
Subordinate Node.
01 - - - Not permitted.
10
11
0 N Y For DCT, Home uses the SnpRespFwded or
SnpRespDataFwded snoop response to determine transaction
completion.
1 Y Y For DMT, Home uses the CompAck response to determine
transaction completion.
For DCT, Home uses the SnpRespFwd or
SnpRespDataFwded snoop response to determine transaction
completion.
For partial ReadNoSnp or ReadOnce* transactions, that is, where the size is less than 64B:
• The Home cannot use a DCT flow.
• If a DMT flow is used to forward data directly from Subordinate to Requester, the Home must use a partial
ReadNoSnp request to the Subordinate.
• If the Home does not request a DMT flow, a full cache line or partial cache line ReadNoSnp can be used.
The Home must only return the requested number of DAT packets to the Requester, regardless of the number
of DAT packets it receives from the Subordinate. For more information, see B2.9.4Data packetization.
B2.3.2 Write transactions
Write transactions are grouped into the following types:
• B2.3.2.1 Immediate Write
• B2.3.2.2 Write Zero
• B2.3.2.3 CopyBack Write
• B2.3.2.4 Combined Immediate Write and CMO
• B2.3.2.5 Combined Immediate Write and Persist CMO
• B2.3.2.6 Combined CopyBack Write and CMO
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
62
```

## PDF page 63

```text
Chapter B2. Transactions
B2.3. Transaction structure
B2.3.2.1 Immediate Write
Figure B2.3 shows the possible transaction flows for an Immediate Write transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
63
```

## PDF page 64

```text
Chapter B2. Transactions
B2.3. Transaction structure
Requester
Requester
Home
Home
Subordinate
Subordinate
WriteNoSnpPtl, WriteNoSnpFull, WriteNoSnpDef, WriteUniquePtl, WriteUniqueFull,
WriteUniquePtlStash, WriteUniqueFullStash
alt [1. DWT]
WriteNoSnpPtl, WriteNoSnpFull, WriteNoSnpDef
(DoDWT=1)
DBIDResp
NonCopyBackWriteData, WriteDataCancel
Comp
Comp
opt [TagOp == Match]
TagMatch
[2. No DWT, no CompAck]
alt [2a1. Separate responses from the Home]
DBIDResp, DBIDRespOrd
Comp
[2a2. Combined response from the Home]
CompDBIDResp
NonCopyBackWriteData, WriteDataCancel
opt [TagOp == Match]
alt [2b1. TagMatch from Home]
TagMatch
[2b2. TagMatch from Subordinate]
WriteNoSnpPtl, WriteNoSnpFull
(DoDWT=0)
alt [2b2a. Separate responses from the Subordinate]
DBIDResp
Comp
[2b2b. Combined response from the Subordinate]
CompDBIDResp
NonCopyBackWriteData, WriteDataCancel
TagMatch
[3. No DWT, with CompAck]
alt [3a1. Separate responses from the Home]
DBIDResp, DBIDRespOrd
Comp
[3a2. Combined response from the Home]
CompDBIDResp
alt [3b1. Separate response from the Requester]
NonCopyBackWriteData, WriteDataCancel
CompAck
[3b2. Combined response from the Requester]
NonCopyBackWriteDataCompAck
opt [TagOp == Match]
alt [3c1. TagMatch from Home]
TagMatch
[3c2. TagMatch from Subordinate]
WriteNoSnpPtl, WriteNoSnpFull
(DoDWT=0)
alt [3c2a. Separate responses from the Subordinate]
DBIDResp
Comp
[3c2b. Combined response from the Subordinate]
CompDBIDResp
NonCopyBackWriteData, WriteDataCancel
TagMatch
Figure B2.3: Immediate Write
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
64
```

## PDF page 65

```text
Chapter B2. Transactions
B2.3. Transaction structure
The sequence for Immediate Write transactions is:
• The transaction starts with the Requester issuing an Immediate Write request to the Home. The Immediate
Write transactions are:
– WriteNoSnpPtl
– WriteNoSnpFull
– WriteNoSnpDef
– WriteUniquePtl
– WriteUniqueFull
– WriteUniquePtlStash
– WriteUniqueFullStash
Snoop requests that are generated to complete these transactions are considered independent transactions
from the Home and are not shown in this flow. Write requests that are generated to downstream Subordinates,
which are not part of the DWT flow, are considered as independent transactions and are not shown in this
flow. See B2.3.9 Home Initiated transactions for more details of independent transactions from the Home.
Stash snoops that are generated to complete the WriteUniquePtlStash or WriteUniqueFullStash transactions
are described in the later section on Stash transactions, see B2.3.4 Stash transactions.
The request contains the following fields which affect the transaction flow:
– ExpCompAck
– TagOp
• The Home can choose to complete the transaction using DWT or without DWT. The remainder of the
transaction flow depends on whether the original request requires a completion acknowledge response, as
determined by the ExpCompAck field. The combinations are described in alternatives 1-3:
1. DWT
The Home uses DWT.
– The Home sends a downstream write request, WriteNoSnpPtl, WriteNoSnpFull, or WriteNoSnpDef,
with DoDWT = 1 to the Subordinate.
– The Subordinate returns a data request, DBIDResp, to the Requester.
– The Requester sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to
the Subordinate. The Requester must only send this after receiving DBIDResp.
– The Subordinate returns a completion response, Comp, to the Home. It is permitted, but not
required, for the Subordinate to wait for write data, NonCopyBackWriteData, or a cancellation,
WriteDataCancel, from the Requester before returning Comp to the Home.
– The Home returns a completion response, Comp, to the Requester. It is permitted, but not required,
for the Home to wait for Comp from the Subordinate before returning Comp to the Requester.
– Optionally, when the request requires a TagMatch response, the Subordinate returns a tag match
response, TagMatch, to the Requester. It is permitted, but not required, to wait for write data before
returning TagMatch.
2. No DWT, no CompAck
The Home does not use DWT for a request that does not require a completion acknowledge, CompAck.
– The Home has two alternatives to send the completion response and the data request response to the
Requester.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
65
```

## PDF page 66

```text
Chapter B2. Transactions
B2.3. Transaction structure
Alt 2a1. Separate responses from the Home
The Home does both the following:
– Returns a data request, DBIDResp or DBIDRespOrd, to the Requester.
– Returns a completion response, Comp, to the Requester. It is permitted, but not required, to
wait for write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, before
returning Comp.
Alt 2a2. Combined response from the Home
The Home returns a combined data request and completion response, CompDBIDResp, to the
Requester.
– The Requester sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to
the Home. The Requester must only send this after receiving DBIDResp, DBIDRespOrd, or
CompDBIDResp.
– Optionally, when the request requires a TagMatch response, the Home has two alternatives.
Alt 2b1. TagMatch from Home
The Home returns a tag match response, TagMatch, to the Requester. It is permitted, but not
required, to wait for write data before returning TagMatch.
Alt 2b2. TagMatch from Subordinate
– The Home sends a downstream write request, WriteNoSnpPtl or WriteNoSnpFull, with
DoDWT = 0 to the Subordinate. The Subordinate has two alternatives to send return data
request and completion response to the Home.
Alt 2b2a. Separate responses from the Subordinate
The Subordinate does both the following:
– Returns a data request, DBIDResp, to the Home.
– Returns a completion response, Comp, to the Home.
It is permitted, but not required, for the Subordinate to wait for write data from the Home
before returning Comp to the Home.
Alt 2b2b. Combined response from the Subordinate
The Subordinate returns a combined data request and completion response,
CompDBIDResp, to the Home.
– The Home sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to
the Subordinate. The Home must only send this after receiving DBIDResp or
CompDBIDResp.
– The Subordinate returns a tag match response, TagMatch, to the Requester. It is permitted, but
not required, to wait for write data before returning TagMatch.
3. No DWT, with CompAck
The Home does not use DWT for a request that does require a completion acknowledge, CompAck.
• The Home has two alternatives to return the completion response and the data request response to the
Requester.
Alt 3a1. Separate response from the Home
The Home does both the following:
– Returns a data request, DBIDResp or DBIDRespOrd, to the Requester.
– Returns a completion response, Comp, to the Requester.
It is permitted, but not required, to wait for write data, NonCopyBackWriteData, or a cancellation,
WriteDataCancel, before returning Comp.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
66
```

## PDF page 67

```text
Chapter B2. Transactions
B2.3. Transaction structure
Alt 3a2. Combined response from the Home
The Home returns a combined data request and completion response, CompDBIDResp, to the
Requester.
• The Requester has two alternatives to send write data and completion acknowledge to the Home.
Alt 3b1. Separate response from the Requester
The Requester does both the following:
– Sends write data, NonCopyBackWriteData, or a write cancellation, WriteDataCancel, to the
Home.
The Requester must only send this after receiving DBIDResp, DBIDRespOrd, or
CompDBIDResp.
– Sends a completion acknowledge, CompAck, to the Home. The Requester must only send this
after it has received DBIDResp, DBIDRespOrd, CompDBIDResp, or Comp. It is permitted, but
not required, to wait for DBIDResp or DBIDRespOrd before sending CompAck. It is not
permitted to wait for Comp before sending CompAck. It is permitted, but not expected, to wait
for TagMatch before returning CompAck.
Alt 3b2. Combined response from the Requester
The Requester sends a combined write data and completion acknowledge,
NonCopyBackWriteDataCompAck, to the Home.
The Requester must only send this after it has received DBIDResp, DBIDRespOrd, or
CompDBIDResp.
It is not permitted to wait for Comp before sending NCBWRrDataCompAck if DBIDResp or
DBIDRespOrd have been received.
• Optionally, when the request requires a TagMatch response, the Home has two alternatives to return the
response.
Alt 3c1. TagMatch from Home
The Home returns a tag match response, TagMatch, to the Requester. It is permitted, but not
required, to wait for write data before returning TagMatch.
Alt 3c2. TagMatch from Subordinate
– The Home sends a downstream write request, WriteNoSnpPtl or WriteNoSnpFull, with DoDWT
= 0 to the Subordinate. The Subordinate has two alternatives to return data request and
completion response to the Home.
Alt 3c2a. Separate responses from Subordinate
The Subordinate does both the following:
– Returns a data request, DBIDResp, to the Home.
– Returns a completion response, Comp, to the Home.
It is permitted, but not required, for the Subordinate to wait for write data before sending
Comp to the Home.
Alt 3c2b. Combined response from Subordinate
The Subordinate returns a combined data request and completion response, CompDBIDResp,
to the Home.
– The Home sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to the
Subordinate.
The Home must only send this after receiving DBIDResp or CompDBIDResp.
– The Subordinate returns a tag match response, TagMatch, to the Requester. It is permitted, but
not required, to wait for write data before returning TagMatch.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
67
```

## PDF page 68

```text
Chapter B2. Transactions
B2.3. Transaction structure
The Completer of a Write transaction is permitted to return a Comp response when a WriteDataCancel response is
received without dependency on either the processing of the write request or the completion of any snoops sent
due to the write.
B2.3.2.2 Write Zero
Figure B2.4 shows the possible transaction flows for a Write Zero transaction.
Requester
Requester
Home
Home
WriteNoSnpZero, WriteUniqueZero
alt [1. Separate response from Home]
DBIDResp, DBIDRespOrd
Comp
[2. Combined response from Home]
CompDBIDResp
Figure B2.4: Write Zero
• The transaction starts with the Requester issuing a Write Zero request to the Home. The Write Zero
transactions are:
– WriteUniqueZero
– WriteNoSnpZero
• The Home has two alternatives to send the completion response and the data request response to the
Requester.
1. Separate response from Home
– The Home returns a data request response, DBIDResp or DBIDRespOrd, to the Requester.
– The Home returns a completion response, Comp, to the Requester.
2. Combined response from Home
The Home returns a combined data request and completion response, CompDBIDResp, to the Requester.
B2.3.2.3 CopyBack Write
Figure B2.5 shows the possible transaction flows for a CopyBack Write transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
68
```

## PDF page 69

```text
Chapter B2. Transactions
B2.3. Transaction structure
Requester
Requester
Home
Home
WriteBackFull, WriteBackPtl, WriteCleanFull, WriteEvictOrEvict, WriteEvictFull
alt [1 WriteEvictOrEvict or CopyAtHome request]
alt [1a. Without data transfer]
Comp
CompAck
[1b. With data transfer]
CompDBIDResp
CopyBackWriteData
[2 Not WriteEvictOrEvict and not CopyAtHome request]
CompDBIDResp
CopyBackWriteData
Figure B2.5: CopyBack Write
The sequence for CopyBack Write is:
• The transaction starts with the Requester issuing a CopyBack Write request to the Home. The CopyBack
Write transactions are:
– WriteBackPtl
– WriteBackFull
– WriteCleanFull
– WriteEvictFull
– WriteEvictOrEvict
The request contains the following fields which affect the transaction flow:
– CAH
– Opcode
• The Home can choose to complete the transaction with a Comp or CompDBIDResp response. The choice of
response from the Home is determined by the request type and CAH value. The combinations are described
in alternatives 1-2:
1. WriteEvictOrEvict or CopyAtHome request
The request is WriteEvictOrEvict or the CAH bit value in the request is set to 1.
The Home has two alternative responses to return to the Requester:
Alt 1a. Without data transfer
– The Home returns a completion response, Comp, to the Requester to avoid the data transfer.
– The Requester sends a completion acknowledge, CompAck.
The Requester must send this regardless of the ExpCompAck value in the original request and
only after receiving the Comp response.
Alt 1b. With data transfer
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
69
```

## PDF page 70

```text
Chapter B2. Transactions
B2.3. Transaction structure
– The Home returns a combined data request and completion response, CompDBIDResp, to the
Requester.
– The Requester sends write data, CopyBackWriteData, to the Home.
The Requester must only send this after receiving the CompDBIDResp response.
2. Not WriteEvictOrEvict and not CopyAtHome request
The request is not WriteEvictOrEvict and the CAH bit value in the request is set to 0.
– The Home sends a combined data request and completion response, CompDBIDResp, to the
Requester.
– The Requester sends write data, CopyBackWriteData, to the Home. The Requester must only send
this after receiving the CompDBIDResp response.
B2.3.2.4 Combined Immediate Write and CMO
Figure B2.6 shows the possible transaction flows for a Combined Write and CMO transaction. This only covers
Non-persist Cache Maintenance Operations, see B2.3.2.5 Combined Immediate Write and Persist CMO for
transaction flows for a Combined Immediate Write and Persist CMO transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
70
```

## PDF page 71

```text
Chapter B2. Transactions
B2.3. Transaction structure
Requester
Requester
Home
Home
Subordinate
Subordinate
WriteNoSnpPtlCleanInv, WriteNoSnpFullCleanInv,
WriteNoSnpPtlCleanSh, WriteNoSnpFullCleanSh,
WriteUniquePtlCleanSh, WriteUniqueFullCleanSh,
WriteNoSnpPtlCleanInvPoPA, WriteNoSnpFullCleanInvPoPA,
WriteUniqueFullCleanInvStrg, WriteNoSnpFullCleanInvStrg
alt [1. Combined Write to Subordinate with DWT]
WriteNoSnpPtlCleanInv, WriteNoSnpFullCleanInv,
WriteNoSnpPtlCleanSh, WriteNoSnpFullCleanSh,
WriteNoSnpPtlCleanInvPoPA, WriteNoSnpFullCleanInvPoPA,
WriteNoSnpFullCleanInvStrg
DoDWT = 1
DBIDResp
NonCopyBackWriteData, WriteDataCancel
Comp
Comp
CompCMO
CompCMO
[2. Non-combined write to Subordinate with DWT]
WriteNoSnpPtl, WriteNoSnpFull
(DoDWT=1)
DBIDResp
NonCopyBackWriteData, WriteDataCancel
Comp
Comp
CompCMO
[3. No DWT]
alt [3a1. Separate responses from Home]
DBIDResp, DBIDRespOrd
Comp
[3a2. Combined response from Home]
CompDBIDResp
alt [3b1. No CompAck required]
NonCopyBackWriteData, WriteDataCancel
[3b2. CompAck required]
alt [3b2a. Separate response from Requester]
NonCopyBackWriteData, WriteDataCancel
CompAck
[3b2b. Combined response from Requester]
NonCopyBackWriteDataCompAck
CompCMO
Figure B2.6: Combined Immediate Write and CMO
The sequence for the Combined Immediate Write with CMO transactions is:
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
71
```

## PDF page 72

```text
Chapter B2. Transactions
B2.3. Transaction structure
• The transaction starts with the Requester issuing a Combined Write and CMO request to the Home. The
Combined Immediate Write and CMO transactions are:
– WriteNoSnpPtlCleanInv
– WriteNoSnpFullCleanInv
– WriteNoSnpPtlCleanSh
– WriteNoSnpFullCleanSh
– WriteUniquePtlCleanSh
– WriteUniqueFullCleanSh
– WriteNoSnpPtlCleanInvPoPA
– WriteNoSnpFullCleanInvPoPA
– WriteUniqueFullCleanInvStrg
– WriteNoSnpFullCleanInvStrg
Snoop requests that are generated to complete these transactions are considered as independent transactions
from the Home and are not shown in this flow. Write requests that are generated to downstream Subordinates,
which are not part of the DWT flow, are considered as independent transactions and are not shown in this
flow. Also, CMO requests that only return responses to the Home and are generated to downstream
Subordinates are considered independent transactions. See B2.3.9 Home Initiated transactions for more
details on independent transactions from the Home. See B2.3.9.2 Home to Subordinate Write transactions
for more details on independent Combined Write and CMO transactions from the Home.
The request contains the following fields which affect the transaction flow:
– Opcode
– ExpCompAck
Note
A TagOp value of Match is not permitted in a Combined Immediate Write and CMO transaction,
therefore no TagMatch responses are permitted and the TagOp field does not affect the transaction flow.
• The Home has three alternatives to choose from to complete the transaction:
– Combined Write to Subordinate with DWT.
– Non-combined Write to Subordinate with DWT.
– Without DWT.
The three approaches are described in the alternatives 1-3.
• The remainder of the transaction flow depends on whether the original request required a completion
acknowledge, as determined by the ExpCompAck.
1. Combined Write to Subordinate with DWT
The Home uses a Combined Write with DWT.
– The Home sends a downstream combined write request with DoDWT = 1 to the Subordinate.
– The Subordinate returns a data request, DBIDResp, to the Requester.
– The Requester sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to
the Subordinate. The Requester must only send this after receiving DBIDResp.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
72
```

## PDF page 73

```text
Chapter B2. Transactions
B2.3. Transaction structure
– The Subordinate returns a completion response, Comp, to the Home. It is permitted, but not
required, for the Subordinate to wait for write data, NonCopyBackWriteData, or a cancellation,
WriteDataCancel, from the Requester before returning Comp to the Home.
– The Home returns a completion response, Comp, to the Requester. It is permitted, but not required,
for the Home to wait for Comp from the Subordinate before returning Comp to the Requester.
– The Subordinate returns a CMO completion response, CompCMO, to the Home. It is permitted, but
not required, for the Subordinate to wait for write data from the Requester before returning
CompCMO to the Home.
– The Home returns a CMO completion response, CompCMO, to the Requester. It is permitted, but
not required, for the Home to wait for Comp or CompCMO from the Subordinate before returning
CompCMO to the Requester. If there is an observer downstream of the Home, the Home must wait
for the CompCMO response from the Subordinate before returning CompCMO to the Requester.
2. Non-combined Write to Subordinate with DWT
The Home uses a Non-combined Write with DWT.
– The Home sends a downstream WriteNoSnpPtl or WriteNoSnpFull, with DoDWT = 1 to the
Subordinate.
– The Subordinate returns a data request, DBIDResp, to the Requester.
– The Requester sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to
the Subordinate. The Requester must only send this after receiving DBIDResp.
– The Subordinate returns a completion response, Comp, to the Home. It is permitted, but not
required, for the Subordinate to wait for write data, NonCopyBackWriteData, or a cancellation,
WriteDataCancel, from the Requester before returning Comp to the Home.
– The Home returns a completion response, Comp, to the Requester. It is permitted, but not required,
for the Home to wait for Comp from the Subordinate before returning Comp to the Requester.
– The Home returns a CMO completion response, CompCMO, to the Requester. It is permitted, but
not required, for the Home to wait for Comp from the Subordinate before returning CompCMO to
the Requester.
3. No DWT
– The Home does not use DWT.
– The Home has two alternatives to request write data.
Alt 3a1. Separate responses from Home
The Home does both the following:
– Returns a data request, DBIDResp or DBIDRespOrd, to the Requester.
– Returns a completion response, Comp, to the Requester.
It is permitted, but not required, to wait for write data, NonCopyBackWriteData, or a
cancellation, WriteDataCancel, before returning Comp.
Alt 3a2. Combined response from Home
The Home returns a combined data request and completion response, CompDBIDResp, to the
Requester.
– The Requester has several alternatives to send write data depending on whether the transaction
requires a completion acknowledge.
Alt 3b1. No CompAck required
A completion acknowledge, CompAck, is not required and the Requester sends write data,
NonCopyBackWriteData, or a write cancellation, WriteDataCancel, to the Home. The Requester
must only send this after receiving DBIDResp, DBIDRespOrd, or CompDBIDResp.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
73
```

## PDF page 74

```text
Chapter B2. Transactions
B2.3. Transaction structure
Alt 3b2. CompAck required
A completion acknowledge is required. The Requester has two alternatives to send write data and
completion acknowledge to the Home.
Alt 3b2a. Separate response from Requester
The Requester does both the following:
– Sends write data, NonCopyBackWriteData, or a write cancellation, WriteDataCancel, to the
Home. The Requester must only send this after receiving DBIDResp, DBIDRespOrd, or
CompDBIDResp.
– Sends CompAck to the Home. The Requester must only send this after it has received
DBIDResp, DBIDRespOrd, CompDBIDResp, or Comp. It is permitted, but not required, to
wait for DBIDResp or DBIDRespOrd before sending CompAck. It is not permitted to wait
for Comp or CompCMO before sending CompAck.
Alt 3b2b. Combined response from Requester
The Requester sends a combined write data and completion acknowledge,
NonCopyBackWriteDataCompAck, to the Home. The Requester must only send this after it
has received DBIDResp, DBIDRespOrd, or CompDBIDResp. It is not permitted to wait for
Comp before sending NonCopyBackWriteDataCompAck if DBIDResp or DBIDRespOrd have
been received. It is not permitted to wait for CompCMO before sending
NonCopyBackWriteDataCompAck.
– The Home returns a CMO completion response, CompCMO, to the Requester. It is permitted, but not
required, for the Home to wait for write data from the Requester before returning CompCMO.
B2.3.2.5 Combined Immediate Write and Persist CMO
Figure B2.7 shows the possible transaction flows for Combined Immediate Write and Persist CMO transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
74
```

## PDF page 75

```text
Chapter B2. Transactions
B2.3. Transaction structure
Requester
Requester
Home
Home
Subordinate
Subordinate
WriteNoSnpPtlCleanShPerSep, WriteNoSnpFullCleanShPerSep,
WriteUniquePtlCleanShPerSep, WriteUniqueFullCleanShPerSep
alt [1. Combined Write to Subordinate with DWT]
WriteNoSnpPtlCleanShPerSep, WriteNoSnpFullCleanShPerSep
(DoDWT=1)
DBIDResp
NonCopyBackWriteData, WriteDataCancel
Comp
Comp
CompCMO
CompCMO
Persist
[2. Non-combined write to Subordinate with DWT]
WriteNoSnpPtl, WriteNoSnpFull
(DoDWT=1)
DBIDResp
NonCopyBackWriteData, WriteDataCancel
Comp
Comp
alt [2a. Persist CMO to Subordinate]
CleanSharedPersistSep
Comp
CompCMO
Persist
[2b. No CMO to Subordinate as part of transaction]
alt [2b1. Separate response from Home]
CompCMO
Persist
[2b2. Combined response from Home]
CompPersist
[3. No DWT]
alt [3a1. Separate responses from Home]
DBIDResp, DBIDRespOrd
Comp
[3a2. Combined response from Home]
CompDBIDResp
alt [3b1. No CompAck required]
NonCopyBackWriteData, WriteDataCancel
[3b2. CompAck required]
alt [3b2a. Separate response from Requester]
NonCopyBackWriteData, WriteDataCancel
CompAck
[3b2b. Combined response from Requester]
NonCopyBackWriteDataCompAck
alt [3c1. Combined write without DWT to Subordinate]
WriteNoSnpPtlCleanShPerSep, WriteNoSnpFullCleanShPerSep
(DoDWT=0)
alt [3c1a. Separate responses from Subordinate]
DBIDResp
Comp
[3c1b. Combined response from Subordinate]
CompDBIDResp
NonCopyBackWriteData, WriteDataCancel
CompCMO
CompCMO
Persist
[3c2. All CMO responses from Home]
alt [3c2a. Separate response from Home]
CompCMO
Persist
[3c2b. Combined response from Home]
CompPersist
[3c3. Only CMO transaction to Subordinate]
CleanSharedPersistSep
Comp
CompCMO
Persist
Figure B2.7: Combined Immediate Write and Persist CMO
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
75
```

## PDF page 76

```text
Chapter B2. Transactions
B2.3. Transaction structure
The sequence for Combined Immediate Write and Persist CMO is:
• The transaction starts with the Requester issuing a Combined Immediate Write and Persist CMO request to
the Home.
The Combined Immediate Write and Persist CMO transactions are:
– WriteNoSnpPtlCleanShPerSep
– WriteNoSnpFullCleanShPerSep
– WriteUniquePtlCleanShPerSep
– WriteUniqueFullCleanShPerSep
Snoop requests that are generated to complete these transactions are considered as independent transactions
from the Home and are not shown in this flow. Write requests that are generated to downstream Subordinates,
which are not part of the DWT flow, are considered as independent transactions and are not shown in this
flow. Also, CMO requests that only return responses to the Home and are generated to downstream
Subordinates are considered independent transactions. See B2.3.9 Home Initiated transactions for more
details on independent transactions from the Home. See B2.3.9.2 Home to Subordinate Write transactions
for more details on independent Combined Write and CMO transactions from the Home.
The request contains the following fields which affect the transaction flow:
– Opcode
– ExpCompAck
Note
A TagOp value of Match is not permitted in a Combined Immediate Write and Persist CMO
transaction. Therefore, no TagMatch responses are permitted and the TagOp field does not affect the
transaction flow.
• The Home can choose to complete the transaction using a:
– Combined Write to the Subordinate with DWT.
– Non-combined Write to the Subordinate with DWT.
– Without DWT.
The three approaches are described in alternatives 1-3.
The remainder of the transaction flow depends on whether the original request required a completion
acknowledge, as determined by the ExpCompAck field.
1. Combined Write to Subordinate with DWT
– The Home sends a downstream combined write request with DoDWT = 1 to the Subordinate.
– The Subordinate returns a data request, DBIDResp, to the Requester.
– The Requester sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to
the Subordinate. The Requester must only send this after receiving DBIDResp.
– The Subordinate returns a completion response, Comp, to the Home. It is permitted, but not
required, for the Subordinate to wait for write data, NonCopyBackWriteData, or a cancellation,
WriteDataCancel, from the Requester before returning Comp to the Home.
– The Home returns a completion response, Comp, to the Requester. It is permitted, but not required,
for the Home to wait for Comp from the Subordinate before returning Comp to the Requester.
– The Subordinate returns a CMO completion response, CompCMO, to the Home. It is permitted, but
not required, for the Subordinate to wait for write data from the Requester before returning
CompCMO to the Home.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
76
```

## PDF page 77

```text
Chapter B2. Transactions
B2.3. Transaction structure
– The Home returns a CMO completion response, CompCMO, to the Requester. It is permitted, but
not required, for the Home to wait for Comp or CompCMO from the Subordinate before returning
CompCMO to the Requester. If there is an observer downstream of the Home, the Home must wait
for the CompCMO response from the Subordinate before returning CompCMO to the Requester.
– The Subordinate returns a persist response, Persist, to the Requester. It is permitted, but not
required, to wait for write data before returning Persist.
2. Non-combined Write to Subordinate with DWT
– The Home sends a downstream Non-combined Write request, WriteNoSnpPtl or WriteNoSnpFull,
with DoDWT = 1 to the Subordinate.
– The Subordinate returns a data request, DBIDResp, to the Requester.
– The Requester sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to
the Subordinate. The Requester must only send this after receiving DBIDResp.
– The Subordinate returns a completion response, Comp, to the Home. It is permitted, but not
required, for the Subordinate to wait for write data, NonCopyBackWriteData, or a cancellation,
WriteDataCancel, from the Requester before returning Comp to the Home.
– The Home returns a completion response, Comp, to the Requester. It is permitted, but not required,
for the Home to wait for Comp from the Subordinate before returning Comp to the Requester.
– The Home has two alternatives to send the CMO responses to the Requester.
Alt 2a. Persist CMO to Subordinate
– The Home sends a downstream request, CleanSharedPersistSep, to the Subordinate.
– The Subordinate returns a completion response, Comp, to the Home.
– The Home returns a CMO completion response, CompCMO, to the Requester.
If there is an observer downstream of the Home, the Home must wait for the Comp response
from the Subordinate before returning CompCMO to the Requester.
– The Subordinate returns a persist response, Persist, to the Requester.
Alt 2b. No CMO to Subordinate as part of transaction
The Home sends all the CMO responses to the Requester. All CMO responses can be sent from
the Home in two alternative ways.
Alt 2b1. Separate responses from Home
The Home does both the following:
– Returns a CMO completion response, CompCMO, to the Requester.
– Returns a persist response, Persist, to the Requester.
Alt 2b2. Combined response from Home
The Home returns a combined completion and persist response, CompPersist, to the Requester.
3. No DWT
The Home does not use DWT.
– The Home has two alternatives to request write data.
Alt 3a1. Separate responses from Home
The Home does both the following:
– Returns a data request, DBIDResp or DBIDRespOrd, to the Requester.
– Returns a completion response, Comp, to the Requester. It is permitted, but not required, to
wait for write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, before
returning Comp.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
77
```

## PDF page 78

```text
Chapter B2. Transactions
B2.3. Transaction structure
Alt 3a2. Combined response from Home
The Home returns a combined data request and completion response, CompDBIDResp, to the
Requester.
– The Requester has several alternatives to send write data depending on whether the transaction
requires a completion acknowledge.
Alt 3b1. No CompAck required
The Requester sends write data, NonCopyBackWriteData, or a write cancellation,
WriteDataCancel, to the Home. The Requester must only send this after receiving DBIDResp,
DBIDRespOrd, or CompDBIDResp.
Alt 3b2. CompAck required
A completion acknowledge response, CompAck, is required. The Requester has two alternatives
to send write data and CompAck to the Home.
Alt 3b2a. Separate responses from Requester
The Requester does both the following:
– Sends write data, NonCopyBackWriteData, or a write cancellation, WriteDataCancel, to the
Home.
The Requester must only send this after receiving DBIDResp, DBIDRespOrd, or
CompDBIDResp.
– Sends a completion acknowledge, CompAck, to the Home. The Requester must only send
this after it has received DBIDResp, DBIDRespOrd, CompDBIDResp, or Comp. It is
permitted, but not required, to wait for DBIDResp or DBIDRespOrd before sending
CompAck. It is not permitted to wait for Comp, CompCMO, or Persist before sending
CompAck.
Alt 3b2b. Combined response from Requester
The Requester sends a combined write data and completion acknowledge,
NonCopyBackWriteDataCompAck, to the Home. The Requester must only send this after it
has received DBIDResp, DBIDRespOrd, or CompDBIDResp. It is not permitted to wait for
Comp before sending NonCopyBackWriteDataCompAck if DBIDResp or DBIDRespOrd have
been received. It is not permitted to wait for CompCMO or Persist before sending
NonCopyBackWriteDataCompAck.
– The Home has several alternatives to complete the remainder of the transaction.
Alt 3c1. Combined Write without DWT to Subordinate
– The Home sends a Combined Write without DWT to the Subordinate.
– The Subordinate has two alternatives to request write data.
Alt 3c1a. Separate responses from Subordinate
The Subordinate does both the following:
– Returns a data request, DBIDResp, to the Home.
– Returns a completion response, Comp, to the Home.
It is permitted, but not required, to wait for write data, NonCopyBackWriteData, or a
cancellation, WriteDataCancel, before returning Comp.
Alt 3c1b. Combined response from Subordinate
The Subordinate returns a combined data request and completion response,
CompDBIDResp, to the Home.
– The Home sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to
the Subordinate. The Home must only send this after receiving DBIDResp or
CompDBIDResp.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
78
```

## PDF page 79

```text
Chapter B2. Transactions
B2.3. Transaction structure
– The Subordinate returns a CMO completion response, CompCMO, to the Home. It is
permitted, but not required, to wait for write data before returning CompCMO.
– The Home returns a CMO completion response, CompCMO, to the Requester. It is permitted,
but not required, for the Home to wait for CompCMO from the Subordinate before returning
CompCMO to the Requester.
– The Subordinate returns a persist response, Persist, to the Requester. It is permitted, but not
required, to wait for write data before returning Persist.
Alt 3c2. All CMO transactions from Home
The Home has two alternatives to send all CMO responses to the Requester.
Alt 3c2a. Separate responses from Home
The Home does both the following:
– Returns a CMO completion response, CompCMO, to the Requester.
– Returns a persist response, Persist, to the Requester.
Alt 3c2b. Combined response from Home
The Home returns a combined completion and persist response, CompPersist, to the Requester.
Alt 3c3. Only CMO transactions to Subordinate
– The Home sends a downstream request, CleanSharedPersistSep, to the Subordinate.
Typically, this alternative would only be used where a write to the Subordinate has been
previously sent as an independent transaction.
– The Subordinate returns a completion response, Comp, to the Home.
– The Home returns a CMO completion response, CompCMO, to the Requester.
If there is an observer downstream of the Home, the Home must wait for the Comp response
from the Subordinate before returning CompCMO to the Requester.
– The Subordinate returns a persist response, Persist, to the Requester.
B2.3.2.6 Combined CopyBack Write and CMO
Figure B2.8 shows the possible transaction flows for a Combined CopyBack Write and CMO transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
79
```

## PDF page 80

```text
Chapter B2. Transactions
B2.3. Transaction structure
Requester
Requester
Home
Home
Subordinate
Subordinate
alt [1. Without Persist]
WriteBackFullCleanInv,
WriteBackFullCleanSh,
WriteCleanFullCleanSh,
WriteBackFullCleanInvPoPA,
WriteBackFullCleanInvStrg
alt [1a. CopyAtHome request]
alt [1a1. Without data transfer]
Comp
CompAck
[1a2. With data transfer]
CompDBIDResp
CopyBackWriteData
[1b. No CopyAtHome request]
CompDBIDResp
CopyBackWriteData
CompCMO
[2. With Persist]
WriteBackFullCleanShPerSep,
WriteCleanFullCleanShPerSep
alt [2a1. CopyAtHome request]
alt [2a1a. Without data transfer]
Comp
CompAck
[2a1b. With data trasnfer]
CompDBIDResp
CopyBackWriteData
[2a2. No CopyAtHome request]
CompDBIDResp
CopyBackWriteData
alt [2b1. Persist from Home]
alt [2b1a Separate response from Home]
CompCMO
Persist
[2b1b. Combined response from Home]
CompPersist
[2b2. Persist from Subordinate]
WriteNoSnpPtlCleanShPerSep,
WriteNoSnpFullCleanShPerSep
alt [2b2a. Separate response]
DBIDResp
Comp
[2b2b. Combined response]
CompDBIDResp
NonCopyBackWriteData, WriteDataCancel
CompCMO
CompCMO
Persist
[2b3. Only CMO transaction to Subordinate]
CleanSharedPersistSep
Comp
CompCMO
Persist
Figure B2.8: Combined CopyBack Write and CMO
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
80
```

## PDF page 81

```text
Chapter B2. Transactions
B2.3. Transaction structure
There are two possible sequences for Combined CopyBack and CMO transactions.
Write requests that are generated to downstream Subordinates and not part of the DWT or persist flow. These write
requests are considered independent transactions and are not shown in this flow. CMO requests that are generated
to downstream Subordinates, which only return responses to the Home, are considered as independent transactions
and are not shown in this flow. See B2.3.9 Home Initiated transactions for more details on independent
transactions from the Home. See B2.3.9.4 Home to Subordinate Combined Write and CMO transactions for more
details on independent Combined Write and CMO transactions from the Home.
The request contains the following field which affects the transaction flow:
• Opcode
• CAH
1. Without Persist
The Combined CopyBack Write and CMO transactions without persist are:
• WriteBackFullCleanInv
• WriteBackFullCleanSh
• WriteCleanFullCleanSh
• WriteBackFullCleanInvPoPA
• WriteBackFullCleanInvStrg
The Requester issues a Combined CopyBack Write and CMO request without Persist response.
• The Requester issues a request to the Home.
Alt 1a. CopyAtHome request
The CAH bit value in the request is set to 1.
The Home has two alternative responses to return to the Requester.
Alt 1a1. Without data transfer
– The Home returns a completion response, Comp, to the Requester to avoid the data transfer.
– The Requester sends a completion acknowledge, CompAck.
The Requester must send this regardless of the ExpCompAck value in the original request and
only after receiving the Comp response.
Alt 1a2. With data transfer
– The Home returns a combined data request and completion response, CompDBIDResp, to the
Requester.
– The Requester sends write data, CopyBackWriteData, to the Home.
The Requester must only send this after receiving CompDBIDResp.
Alt 1b. No CopyAtHome request
The CAH bit value in the request is set to 0.
– The Home sends a combined data request and completion response, CompDBIDResp, to the
Requester.
– The Requester sends write data, CopyBackWriteData, to the Home. The Requester must only
send this after receiving CompDBIDResp.
• The Home returns a CMO completion response, CompCMO, to the Requester. It is permitted, but not
required, to wait for CopyBackWriteData or CompAck before returning CompCMO.
2. With Persist
The Combined CopyBack write and CMO transactions are:
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
81
```

## PDF page 82

```text
Chapter B2. Transactions
B2.3. Transaction structure
• WriteBackFullCleanShPerSep
• WriteCleanFullCleanShPerSep
The Requester issues a Combined CopyBack Write and CMO request with Persist response.
• The Requester issues a request to the Home.
Alt 2a1. CopyAtHome request
The CAH bit value in the request is set to 1. The Home has two alternative responses to return to the
Requester.
Alt 2a1a. Without data transfer
– The Home returns a completion response, Comp, to the Requester to avoid the data transfer.
– The Requester sends a completion acknowledge, CompAck. The Requester must send this
regardless of the ExpCompAck value in the original request and only after receiving the Comp
response.
Alt 2a1b. With data transfer
– The Home returns a combined data request and completion response, CompDBIDResp, to the
Requester.
– The Requester sends write data, CopyBackWriteData, to the Home. The Requester must only
send this after receiving CompDBIDResp.
Alt 2a2. No CopyAtHome request
The CAH bit value in the request is set to 0.
– The Home sends a combined data request and completion response, CompDBIDResp, to the
Requester.
– The Requester sends write data, CopyBackWriteData, to the Home. The Requester must only send
this after receiving CompDBIDResp.
The Home has three alternatives to complete the transaction, with the persist response either coming from the
Home or from the Subordinate.
Alt 2b1. Persist from Home
The Home has two alternatives to send the CMO completion response and persist response. It is
permitted, but not required, for the Home to wait for CopyBackWriteData or CompAck before returning
CompCMO, Persist, or CompPersist.
Alt 2b1a. Separate response from Home
– Returns a CMO completion response, CompCMO, to the Requester.
– Returns a persist response, Persist, to the Requester.
Alt 2b2b. Combined response from Home
The Home returns a combined CMO completion response and persist response, CompPersist, to the
Requester.
Alt 2b2. Persist from Subordinate
When a Combined Write is sent to the Subordinate and the Persist response is returned to the Requester,
the following happens:
– The Home sends a downstream write request, WriteNoSnpPtlCleanShPerSep or
WriteNoSnpFullCleanShPerSep, to the Subordinate.
It is permitted, but not required, for the Home to wait for CopyBackWriteData or CompAck before
sending the downstream write request.
– The Subordinate has two alternatives to return the completion response and the data request
response to the Home.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
82
```

## PDF page 83

```text
Chapter B2. Transactions
B2.3. Transaction structure
Alt 2b2a. Separate response
The Subordinate does both the following:
– Returns a data request, DBIDResp, to the Home.
– Returns a completion response, Comp, to the Home. It is permitted, but not required, to wait
for write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, before returning
Comp.
Alt 2b2b. Combined response
The Subordinate returns a combined data request and completion response, CompDBIDResp, to
the Home.
– The Home sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to the
Subordinate.
The Home must only send this after receiving DBIDResp or CompDBIDResp.
– The Subordinate returns a CMO completion response, CompCMO, to the Home.
It is permitted, but not required, to wait for write data before returning CompCMO.
– The Home returns a CMO completion response, CompCMO, to the Requester.
It is permitted, but not required, for the Home to wait for CompCMO from the Subordinate before
returning CompCMO to the Requester.
– The Subordinate returns a persist response, Persist, to the Requester.
It is permitted, but not required, to wait for write data before returning Persist.
Alt 2b3. Only CMO transaction to Subordinate
When a persist CMO is sent to the Subordinate and the Persist response is returned to the Requester, the
following happens:
– The Home sends a downstream request, CleanSharedPersistSep, to the Subordinate.
Typically, this alternative would only be used where a write to the Subordinate has been previously
sent as an independent transaction or the write has been canceled.
– The Subordinate returns a completion response, Comp, to the Home.
– The Home returns a completion response, CompCMO, to the Requester.
If there is an observer downstream of the Home, Home must wait for the Comp response from the
Subordinate before returning CompCMO to the Requester.
– The Subordinate returns a persist response, Persist, to the Requester.
B2.3.3 Atomic transactions
Figure B2.9 shows the possible transaction flows for an Atomic transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
83
```

## PDF page 84

```text
Chapter B2. Transactions
B2.3. Transaction structure
Requester
Requester
Home
Home
alt [1. AtomicStore]
AtomicStore
alt [1a. Separate responses]
DBIDResp, DBIDRespOrd
Comp
[1b. Combined response]
CompDBIDResp
NonCopyBackWriteData
opt [TagMatch response]
TagMatch
[2. Other Atomic Transactions]
AtomicLoad, AtomicSwap, or AtomicCompare
DBIDResp, DBIDRespOrd
NonCopyBackWriteData
CompData
opt [TagMatch response]
TagMatch
Figure B2.9: Atomic transactions
There are two possible sequences for the Atomic transactions.
The Requester alternatives are:
1. AtomicStore
For an AtomicStore transaction:
• The Requester sends an AtomicStore request to the Home.
• The Home has two alternatives to send the completion response and the data request response to the
Requester.
Alt 1a. Separate responses
The Home does both the following:
– Returns a data request, DBIDResp or DBIDRespOrd, to the Requester.
– Returns a completion response, Comp, to the Requester. It is permitted, but not required, to wait
for write data before returning Comp.
Alt 1b. Combined response
The Home returns a combined data request and completion response, CompDBIDResp, to the
Requester.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
84
```

## PDF page 85

```text
Chapter B2. Transactions
B2.3. Transaction structure
• The Requester sends write data, NonCopyBackWriteData, to the Home. The Requester must only send
this after receiving DBIDResp, DBIDRespOrd, or CompDBIDResp.
• Optionally, when the request requires a TagMatch response, the Home returns a tag match response,
TagMatch, to the Requester. It is permitted, but not required, to wait for write data before returning
TagMatch.
2. Other Atomic transactions
For an AtomicLoad, AtomicSwap, or AtomicCompare transaction:
• The Requester sends an AtomicLoad, AtomicSwap, or AtomicCompare request to the Home.
• The Home sends a data request response, DBIDResp or DBIDRespOrd, to the Requester.
• The Requester sends write data, NonCopyBackWriteData, to the Home. The Requester must only send
this after receiving DBIDResp or DBIDRespOrd. The Requester must not wait to receive CompData
before write data is sent.
• The Home returns a combined data and completion response, CompData, to the Requester. It is
permitted, but not required, to wait for write data before returning CompData.
• Optionally, when the request requires a TagMatch response, the Home returns a tag match response,
TagMatch, to the Requester. It is permitted, but not required, to wait for write data before returning
TagMatch.
B2.3.4 Stash transactions
Figure B2.10 shows the possible transaction flows for stash transactions.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
85
```

## PDF page 86

```text
Chapter B2. Transactions
B2.3. Transaction structure
Requester
Requester
Home
Home
Stashee
Stashee
alt [1. Write with Stash Hint]
WriteUniquePtlStash, WriteUniqueFullStash
See Immediate Write for details of WriteUnique completion.
opt
alt [1a. SnpUniqueStash]
SnpUniqueStash
alt [1a1. No DataPull]
SnpResp
SnpRespData, SnpRespDataPtl
[1a2. DataPull]
SnpResp
SnpRespData, SnpRespDataPtl
See Allocating Read for details of read completion.
[1b. Other stash snoops]
SnpMakeInvalidStash, SnpStashUnique, SnpStashShared
alt [1b1. No DataPull]
SnpResp
[1b2. DataPull]
SnpResp
See Allocating Read for details of read completion.
[2. Independent Stash without StashDone response]
StashOnceUnique, StashOnceShared
opt
SnpStashUnique, SnpStashShared
alt [2a. No DataPull]
SnpResp
[2b. DataPull]
SnpResp
See Allocating Read for details of read completion.
Comp
[3. Independent Stash with StashDone response]
StashOnceSepUnique, StashOnceSepShared
opt
SnpStashUnique, SnpStashShared
alt [3a1. No DataPull]
SnpResp
[3a2. DataPull]
SnpResp
See Allocating Read for details of read completion.
alt [3b1. Separate response from Home]
Comp
StashDone
[3b2. Combined response from Home]
CompStashDone
Figure B2.10: Stash transactions
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
86
```

## PDF page 87

```text
Chapter B2. Transactions
B2.3. Transaction structure
There are three possible sequences for Stash transactions.
The following can affect transaction flow:
• The Home is permitted to ignore the Stash request and not perform any stash snoops.
• The Stashee is permitted to ignore the Stash request and not request a data pull to complete the transaction.
• StashOnceSepUnique and StashOnceSepShared can have a separate StashDone response or combined
CompStashDone response.
1. Write with Stash Hint
A write with Stash hint starts the transaction. The write with Stash hint requests are:
• WriteUniquePtlStash
• WriteUniqueFullStash
The WriteUnique uses the same transaction flows as an Immediate Write, see B2.3.2.1 Immediate Write for
details.
The Home can optionally send a stash snoop request.
Alt 1a. SnpUniqueStash
– The Home sends SnpUniqueStash to the Stashee.
Typically the Home sends SnpUniqueStash for a partial line write. Other snoops, including other
stash snoops, are permitted.
– The Stashee has two alternatives to respond to the stash snoop request.
Alt 1a1. No DataPull
Not request a data pull.
Alt 1a2. DataPull
Request a data pull.
The completion of a request with data pull is identical to the completion of an Allocating Read
transaction, see B2.3.1.1 Allocating Read for details.
Alt 1b. Other stash snoops
– Send SnpMakeInvalidStash, SnpStashShared, or SnpStashUnique, to the Stashee.
Typically, the Home sends SnpMakeInvalidStash for a full line write. Other snoops, including other
stash snoops, are permitted.
– The Stashee has two alternatives to respond to the stash snoop request.
Alt 1b1. No DataPull
Not request a data pull
Alt 1b2. DataPull
Request a data pull.
The completion of a request with data pull is identical to the completion of an Allocating Read
transaction, see B2.3.1.1 Allocating Read for details.
2. Independent Stash without StashDone response
An independent Stash without a StashDone response starts the transaction. The independent Stash requests
without a StashDone response are:
• StashOnceUnique
• StashOnceShared
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
87
```

## PDF page 88

```text
Chapter B2. Transactions
B2.3. Transaction structure
The Home can optionally send a stash snoop request, SnpStashUnique or SnpStashShared, to the Stashee.
Typically the Home sends SnpStashUnique when the original request is StashOnceUnique and
SnpStashShared when the original request is StashOnceShared.
• The Stashee has two alternatives to respond to the stash snoop request.
Alt 2a. No DataPull
Not request a data pull.
Alt 2b. DataPull
Request a data pull.
The completion of a request with data pull is identical to the completion of an Allocating Read
transaction, see B2.3.1.1 Allocating Read for details.
The transaction completes with the Home returning a completion response, Comp, to the original Requester.
It is permitted, but not required, to wait for the stash transaction to complete before the Comp response is
returned.
3. Independent Stash with StashDone response
An independent Stash with a StashDone response starts the transaction. The independent Stash requests with
a StashDone response are:
• StashOnceSepUnique
• StashOnceSepShared
The Home can optionally send a stash snoop request, SnpStashUnique or SnpStashShared, to the Stashee.
Typically the Home sends SnpStashUnique when the original request is StashOnceSepUnique and
SnpStashShared when the original request is StashOnceSepShared.
• The Stashee has two alternatives to respond to the stash snoop request.
Alt 3a1. No DataPull
Not request a data pull.
Alt 3a2. DataPull
Request a data pull.
The completion of a request with data pull is identical to the completion of an Allocating Read
transaction, see B2.3.1.1 Allocating Read for details.
The Home has two alternatives to complete the transaction.
Alt 3b1. Separate responses from Home
The Home does both the following:
– Returns a completion response, Comp, to the Requester.
– Returns a stash done response, StashDone, to the Requester.
Alt 3b2. Combined response from Home
The Home returns a combined completion and stash done response, CompStashDone, to the Requester.
B2.3.5 Dataless transactions
Figure B2.11 shows the transaction flow for a Dataless transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
88
```

## PDF page 89

```text
Chapter B2. Transactions
B2.3. Transaction structure
Requester
Requester
Home
Home
Subordinate
Subordinate
alt [1. Transactions without CompAck or Persist]
CleanInvalid, CleanInvalidPoPA, CleanInvalidStorage, MakeInvalid, CleanShared,
CleanSharedPersist, Evict
Comp
[2. Transactions with CompAck]
CleanUnique, MakeUnique
Comp
CompAck
[3. Transactions with Persist]
CleanSharedPersistSep
alt [3a. Separate response from Home]
Comp
Persist
[3b.Combined response from Home]
CompPersist
[3c. Response from Home and Subordinate]
CleanSharedPersistSep
Comp
Comp
Persist
Figure B2.11: Dataless transactions
There are three possible sequences for Dataless transactions.
1. Transactions without CompAck or Persist
The Dataless transactions without CompAck or Persist are:
• CleanInvalid
• CleanInvalidPoPA
• CleanInvalidStorage
• MakeInvalid
• CleanShared
• CleanSharedPersist
• Evict
The Requester sends the request to the Home.
The Home returns a completion response, Comp, to the Requester.
2. Transactions with CompAck
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
89
```

## PDF page 90

```text
Chapter B2. Transactions
B2.3. Transaction structure
The Dataless transactions with CompAck are:
• CleanUnique
• MakeUnique
The Requester sends the request to the Home.
The Home returns a completion response, Comp, to the Requester.
The Requester sends a completion acknowledge, CompAck, to the Home.
The Requester must only send this after receiving Comp.
3. Transactions with Persist
The Dataless transaction with Persist is:
• CleanSharedPersistSep
The Requester sends the request to the Home.
The Home has three alternatives to complete the transaction.
Alt 3a. Separate responses from the Home
The Home does both the following:
– Returns a completion response, Comp, to the Requester.
– Returns a persist response, Persist, to the Requester.
Alt 3b. Combined response from Home
The Home returns a combined completion and persist response, CompPersist, to the Requester.
Alt 3c. Response from Home and Subordinate
With the Persist response from the Subordinate, the following happens:
– The Home sends a downstream request, CleanSharedPersistSep, to the Subordinate.
– The Subordinate returns a completion response, Comp, to the Home.
– The Home returns a completion response, Comp, to the Requester. If there is an observer
downstream of the Home, the Home must wait for the Comp response from the Subordinate before
returning the Comp response to the Requester.
– The Subordinate returns a persist response, Persist, to the Requester.
B2.3.6 Prefetch transactions
Figure B2.12 shows the transaction flow for a Prefetch transaction.
Requester
Requester
Subordinate
Subordinate
PrefetchTgt
Figure B2.12: Prefetch transactions
The sequence for the Prefetch transaction is:
• The Requester sends a PrefetchTgt request directly to the Subordinate.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
90
```

## PDF page 91

```text
Chapter B2. Transactions
B2.3. Transaction structure
Note
No response is given.
B2.3.7 DVM transactions
Figure B2.13 shows the transaction flows for a DVM transaction.
Requester
Requester
Home
Home
DVMOp
alt [1. Non-sync DVMOp]
alt [1a. Separate responses from the Home]
DBIDResp
NonCopyBackWriteData
Comp
[1b. Combined responses from Home]
CompDBIDResp
NonCopyBackWriteData
[2. Sync DVMOp]
DBIDResp
NonCopyBackWriteData
Comp
Figure B2.13: DVM transactions
Snoop requests that are generated to complete a DVM transaction are considered as independent transactions from
the Home and are not shown in this flow. See B2.3.9.8 Home to Snoopee DVM transactions for more details.
The sequence for the DVM transaction is:
• The transaction starts with the Requester issuing a DVMOp request to the Home.
• The Home has two alternatives to send the completion response and the data request response to the
Requester:
1. Non-sync DVMOp
Alt 1a. Separate responses from the Home
The Home does both the following:
– Returns a data request, DBIDResp, to the Requester.
– The Requester sends write data, NonCopyBackWriteData, to the Home.
The Requester must only send this after receiving DBIDResp
– Returns a completion response, Comp, to the Requester. It is permitted, but not required, to wait for
write data before returning Comp.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
91
```

## PDF page 92

```text
Chapter B2. Transactions
B2.3. Transaction structure
Alt 1b. Combined response from the Home
– The Home returns a combined data request and completion response, CompDBIDResp, to the
Requester.
– The Requester sends write data, NonCopyBackWriteData, to the Home.
The Requester must only send this after receiving CompDBIDResp.
2. Sync DVMOp
The Home must return separate responses.
• The Home returns a data request, DBIDResp, to the Requester.
• The Requester sends write data, NonCopyBackWriteData, to the Home. The Requester must only send
this after receiving DBIDResp.
• The Home returns a completion response, Comp, to the Requester. The Home must only return this after
receiving write data.
B2.3.8 Retry
Figure B2.14 shows the possible transaction flows for a Retry sequence.
Requester
Requester
Completer
Completer
Request without Credit
RetryAck
PCrdGrant
alt [1. Request re-sent]
Request with Credit
[2. Request canceled]
PCrdReturn
Figure B2.14: Retry transactions
A request transaction is first sent without a Protocol Credit (P-Credit). If the transaction cannot be accepted at the
Completer, a RetryAck response is given indicating that the transaction is not accepted and can be sent again when
an appropriate credit is provided. The transaction includes a credit when it is sent a second time, and is guaranteed
to be accepted.
The sequence for the Retry transaction is:
• The Requester issues a request without credit.
• The Completer returns a retry response, RetryAck, to the Requester.
• The Completer returns a protocol credit grant, PCrdGrant, to the Requester. Typically the protocol credit
grant is returned a significant time after the Retry response. However, in an atypical case, the PCrdGrant
response can be returned before the Retry response.
• The Requester has two alternatives to conclude the Retry sequence. This step must only occur after the
Requester has received both RetryAck and PCrdGrant.
1. Resend the original request
The Requester issues a request with credit.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
92
```

## PDF page 93

```text
Chapter B2. Transactions
B2.3. Transaction structure
2. Cancel the request and return the credit
The Requester sends a protocol credit return, PCrdReturn, to the Completer.
B2.3.9 Home Initiated transactions
The Home Initiated transactions are:
• B2.3.9.1 Home to Subordinate Read transactions
• B2.3.9.2 Home to Subordinate Write transactions
• B2.3.9.3 Home to Subordinate Write Zero transactions
• B2.3.9.4 Home to Subordinate Combined Write and CMO transactions
• B2.3.9.5 Home to Subordinate Dataless transactions
• B2.3.9.6 Home to Subordinate Atomic transactions
• B2.3.9.7 Home to Snoopee transactions
• B2.3.9.8 Home to Snoopee DVM transactions
B2.3.9.1 Home to Subordinate Read transactions
Figure B2.15 shows the possible transaction flows for a Home to Subordinate Read transaction.
Home
Home
Subordinate
Subordinate
alt [1. Combined response from Subordinate]
ReadNoSnp
opt [Order != 00]
ReadReceipt
CompData
[2. Separate response from Subordinate]
ReadNoSnpSep
opt [Order != 00]
ReadReceipt
DataSepResp
Figure B2.15: Home to Subordinate Read transactions
There are two possible sequences for Home Read transactions.
1. Combined response from Subordinate
• For a ReadNoSnp transaction, the Home issues the request to the Subordinate.
• Optionally, when the request has Order set to non-zero the Subordinate returns a ReadReceipt response.
• The Subordinate returns a combined completion response and read data, CompData, to the Home.
2. Separate responses from Subordinate
• For a ReadNoSnpSep transaction, the Home issues the request to the Subordinate.
• Optionally, when the request has Order set to non-zero, the Subordinate returns a ReadReceipt response.
• The Subordinate returns read data, DataSepResp, to the Home.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
93
```

## PDF page 94

```text
Chapter B2. Transactions
B2.3. Transaction structure
B2.3.9.2 Home to Subordinate Write transactions
Figure B2.16 shows the possible transaction flows for a Home to Subordinate Write transaction.
Home
Home
Subordinate
Subordinate
WriteNoSnpPtl, WriteNoSnpFull, WriteNoSnpDef
alt [1. Separate response]
DBIDResp
Comp
[2. Combined response]
CompDBIDResp
NonCopyBackWriteData, WriteDataCancel
opt [TagMatch response]
TagMatch
Figure B2.16: Home to Subordinate Write transactions
The sequence for the Home to Subordinate Write transaction is:
• The transaction starts with the Home issuing a WriteNoSnpPtl, WriteNoSnpFull, or WriteNoSnpDef request
to the Subordinate.
• The Subordinate has two alternatives to return the completion response and the data request response to the
Home.
1. Separate response
The Subordinate does both the following:
– Returns a Data request response, DBIDResp, to the Home.
– Returns a completion response, Comp, to the Home. It is permitted, but not required, to wait for
write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, before returning Comp.
2. Combined response
The Subordinate returns a combined data request and completion response, CompDBIDResp, to the
Home.
• The Home sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to the
Subordinate. The Home must only send this after receiving DBIDResp or CompDBIDResp.
• Optionally, when the request requires a TagMatch response, the Subordinate returns a Tag match response,
TagMatch, to the Home. It is permitted, but not required, to wait for write data before returning TagMatch.
B2.3.9.3 Home to Subordinate Write Zero transactions
Figure B2.17 shows the possible transaction flows for a Home to Subordinate Write Zero transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
94
```

## PDF page 95

```text
Chapter B2. Transactions
B2.3. Transaction structure
Home
Home
Subordinate
Subordinate
WriteNoSnpZero
alt [1. Seperate response from Home]
DBIDResp
Comp
[2. Combined response from Home]
CompDBIDResp
Figure B2.17: Home to Subordinate Write Zero transactions
The sequence for Write Zero is:
• The transaction starts with the Home issuing a Write Zero request to the Subordinate. The Write Zero
transaction is:
– WriteNoSnpZero
• The Subordinate has two alternatives to return the completion response and data request response to the
Home.
1. Separate response from Home
The Subordinate does both the following:
– Returns a data request response, DBIDResp, to the Home.
– Returns a completion response, Comp, to the Home.
2. Combined response from Home
The Subordinate returns a combined data request and completion response, CompDBIDResp, to the
Home.
B2.3.9.4 Home to Subordinate Combined Write and CMO transactions
Figure B2.18 shows the possible transaction flows for a Home to Subordinate Combined Write and CMO
transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
95
```

## PDF page 96

```text
Chapter B2. Transactions
B2.3. Transaction structure
Home
Home
Subordinate
Subordinate
WriteNoSnpPtlCleanInv, WriteNoSnpFullCleanInv,
WriteNoSnpPtlCleanSh, WriteNoSnpFullCleanSh,
WriteNoSnpPtlCleanShPerSep, WriteNoSnpFullCleanShPerSep,
WriteNoSnpPtlCleanInvPoPA, WriteNoSnpFullCleanInvPoPA,
WriteNoSnpFullCleanInvStrg
alt [1a. Separate responses from Subordinate]
DBIDResp
Comp
[1b. Combined response from Subordinate]
CompDBIDResp
NonCopyBackWriteData, WriteDataCancel
alt [2a. Non-persist CMO]
CompCMO
[2b. Persist CMO]
alt [2b1. Separate response from Subordinate]
CompCMO
Persist
[2b2. Combined response from Subordinate]
CompPersist
Figure B2.18: Home to Subordinate Combined Write and CMO transactions
The sequence for the Home to Subordinate Combined Write with CMO transaction is:
• The transaction starts with the Home issuing a Combined Write and CMO request to the Subordinate. The
Home Combined Write and CMO transactions are:
– WriteNoSnpPtlCleanInv
– WriteNoSnpFullCleanInv
– WriteNoSnpPtlCleanSh
– WriteNoSnpFullCleanSh
– WriteNoSnpPtlCleanShPerSep
– WriteNoSnpFullCleanShPerSep
– WriteNoSnpPtlCleanInvPoPA
– WriteNoSnpFullCleanInvPoPA
– WriteNoSnpFullCleanInvStrg
• The Subordinate has two alternatives to send the completion response and the data request response to the
Home.
Alt 1a. Separate responses from Subordinate
The Subordinate does both the following:
– Returns a data request, DBIDResp, to the Home.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
96
```

## PDF page 97

```text
Chapter B2. Transactions
B2.3. Transaction structure
– Returns a completion response, Comp, to the Home.
It is permitted, but not required, to wait for write data, NonCopyBackWriteData, or a cancellation,
WriteDataCancel, before returning Comp.
Alt 1b. Combined response from Subordinate
The Subordinate returns a combined data request and completion response, CompDBIDResp, to the
Home.
• The Home sends write data, NonCopyBackWriteData, or a cancellation, WriteDataCancel, to the
Subordinate. The Home must only send this after receiving DBIDResp or CompDBIDResp.
• There are two alternatives for the Subordinate to return the CMO response depending on whether or not a
persist response, Persist, is required. It is permitted, but not required, for the Subordinate to wait for write
data before returning CompCMO, Persist, or CompPersist.
Alt 2a. Non-persist CMO
When a persist response is not required, the Subordinate returns a CMO completion response,
CompCMO, to the Home.
Alt 2b. Persist CMO
When a persist response is required, the Subordinate has two alternatives to send the CMO completion
response and persist response.
Alt 2b1. Separate response from Subordinate
The Subordinate does both the following:
– Returns a CMO completion response, CompCMO, to the Home.
– Returns a persist response, Persist, to the Home.
Alt 2b2. Combined response from Subordinate
The Subordinate returns a combined CMO completion response and persist response, CompPersist,
to the Home.
B2.3.9.5 Home to Subordinate Dataless transactions
Figure B2.19 shows the transaction flows for a Home to Subordinate Dataless transaction.
Home
Home
Subordinate
Subordinate
alt [1. Transactions without separate Persist]
CleanInvalid, CleanInvalidPoPA, CleanInvalidStorage,
MakeInvalid,CleanShared, CleanSharedPersist
Comp
[2. Transactions with separate Persist]
CleanSharedPersistSep
alt [2a. Separate response from Subordinate]
Comp
Persist
[2b.Combined response from Subordinate]
CompPersist
Figure B2.19: Home to Subordinate Dataless transactions
There are two possible sequences for Home to Subordinate Dataless transactions.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
97
```

## PDF page 98

```text
Chapter B2. Transactions
B2.3. Transaction structure
1. Transactions without separate Persist
The Home to Subordinate Dataless transactions without separate Persist are:
• CleanInvalid
• CleanInvalidPoPA
• CleanInvalidStorage
• MakeInvalid
• CleanShared
• CleanSharedPersist
The Home sends the request to the Subordinate.
The Subordinate returns a completion response, Comp, to the Requester.
2. Transactions with separate Persist
The Home to Subordinate Dataless transaction with separate Persist is:
• CleanSharedPersistSep
The Home sends the request to the Subordinate.
The Subordinate has two alternatives to complete the transaction.
Alt 2a. Separate response from Subordinate
The Subordinate does both the following:
– Returns a completion response, Comp, to the Home.
– Returns a persist response, Persist, to the Home.
Use of separate completion response, Comp, and persist response, Persist, allows a Completer to
send an early Comp without waiting for Persist. Typically, Persist takes much longer.
Alt 2b. Combined response from Subordinate
The Subordinate returns a combined completion and persist response, CompPersist, to the Home.
B2.3.9.6 Home to Subordinate Atomic transactions
Figure B2.20 shows the possible transaction flows for Home to Subordinate Atomic transactions.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
98
```

## PDF page 99

```text
Chapter B2. Transactions
B2.3. Transaction structure
Home
Home
Subordinate
Subordinate
alt [1. AtomicStore]
AtomicStore
alt [1a. Separate responses]
DBIDResp
Comp
[1b. Combined response]
CompDBIDResp
NonCopyBackWriteData
opt [TagOp == Match]
TagMatch
[2. Not Atomic Store]
AtomicLoad, AtomicSwap, or AtomicCompare
DBIDResp
NonCopyBackWriteData
CompData
opt [TagOp == Match]
TagMatch
Figure B2.20: Home to Subordinate Atomic transactions
There are two alternatives for the Home Atomic transactions.
When the Subordinate supports the execution of atomic operations, the Home is permitted, but not required, to
forward Atomic transactions to the Subordinate.
1. AtomicStore
• The Home sends an AtomicStore request to the Subordinate.
• The Subordinate has two alternatives to send the completion response and data request response to the Home.
Alt 1a. Separate responses
The Subordinate does both the following:
– Returns a data request, DBIDResp, to the Home.
– Returns a completion response, Comp, to the Home.
It is permitted, but not required, to wait for write data before returning Comp.
Alt 1b. Combined response
The Subordinate returns a combined data request and completion response, CompDBIDResp, to the
Home.
• The Home sends write data, NonCopyBackWriteData, to the Subordinate. The Home must only send this
after receiving DBIDResp or CompDBIDResp. The Home must not wait for Comp before sending write data.
• Optionally, when the request requires a tag match response, the Subordinate returns a TagMatch response to
the Home. It is permitted, but not required, to wait for write data before returning TagMatch.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
99
```

## PDF page 100

```text
Chapter B2. Transactions
B2.3. Transaction structure
2. Not AtomicStore
• The Home sends an AtomicLoad, AtomicSwap, or AtomicCompare request to the Subordinate.
• The Subordinate sends a data request response, DBIDResp, to the Home.
• The Home sends write data, NonCopyBackWriteData, to the Subordinate. The Home must only send this
after receiving DBIDResp. The Home must not wait to receive CompData before write data is sent.
• The Subordinate returns a combined data and completion response, CompData, to the Home. It is permitted,
but not required, to wait for write data before returning CompData.
• Optionally, when the request requires a TagMatch response, the Subordinate returns a tag match response,
TagMatch, to the Home. It is permitted, but not required, to wait for write data before returning TagMatch.
B2.3.9.7 Home to Snoopee transactions
Figure B2.21 shows the possible transaction flows for a Home to Snoopee transaction.
Home
Home
Snoopee
Snoopee
Snp*, Snp*Fwd
alt [1. Response to home]
SnpResp
[2. Data to home]
SnpRespData, SnpRespDataPtl
Figure B2.21: Home to Snoopee transactions
The following transactions must use this transaction flow.
• SnpOnce
• SnpClean
• SnpNotSharedDirty
• SnpShared
• SnpUnique
• SnpPreferUnique
• SnpCleanShared
• SnpCleanInvalid
• SnpMakeInvalid
• SnpQuery
The following transactions are also permitted, but not required, to use this transaction flow.
• SnpOnceFwd
• SnpCleanFwd
• SnpNotSharedDirtyFwd
• SnpSharedFwd
• SnpUniqueFwd
• SnpPreferUniqueFwd
The sequence the Home to Snoopee transaction is:
• The transaction starts with the Home issuing a Snoop request to the Snoopee.
• The Snoopee has two alternatives to complete the transaction:
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
100
```

## PDF page 101

```text
Chapter B2. Transactions
B2.3. Transaction structure
1. The Snoopee provides a snoop response, SnpResp, to the Home. This is the only permitted alternative
for a SnpMakeInvalid transaction.
2. The Snoopee provides a snoop response with data, SnpRespData or SnpRespDataPtl.
B2.3.9.8 Home to Snoopee DVM transactions
Figure B2.22 shows the transaction flow for a Home to Snoopee DVM transaction, SnpDVMOp.
Home
Home
Snoopee
Snoopee
SnpDVMOp
SnpDVMOp
SnpResp
Figure B2.22: Home to Snoopee DVM transactions
The sequence for the Home to Snoopee DVM transaction is:
• The Home issues two Snoop DVM requests, SnpDVMOp, to the Snoopee.
• The Snoopee provides a single Snoop response, SnpResp. The Snoopee must only provide the Snoop
response after receiving both Snoop DVM requests.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
101
```

## PDF page 102

```text
Chapter B2. Transactions
B2.4. Transaction identifier fields
B2.4 Transaction identifier fields
Each transaction consists of a number of different packets that are transferred across the interconnect. A set of
identifier fields, within a packet, are used to provide additional information about a packet.
The field that routes packets across the interconnect:
• B2.4.1 Target Identifier, TgtID, and Source Identifier, SrcID
The fields that relate all the packets associated with a single transaction are:
• B2.4.2 Transaction Identifier, TxnID
• B2.4.3 Data Buffer Identifier, DBID
• B2.4.4 Return Transaction Identifier, ReturnTxnID
• B2.4.5 Forward Transaction Identifier, FwdTxnID
The field that identifies the individual data packets within a transaction:
• B2.4.6 Data Identifier, DataID, and Critical Chunk Identifier, CCID
The fields that identify individual processing agents within a single Requester:
• B2.4.7 Logical Processor Identifier, LPID
• B2.4.8 Stash Logical Processor Identifier, StashLPID
The field that identifies the target node for a Stash transaction:
• B2.4.9 Stash Node Identifier, StashNID
The field that identifies the recipient node for the Data response, Persist response, or TagMatch response:
• B2.4.10 Return Node Identifier, ReturnNID
The field that identifies the recipient node for the Data response:
• B2.4.12 Forward Node Identifier, FwdNID
The field that is used to identify the recipient node for the CompAck response:
• B2.4.11 Home Node Identifier, HomeNID
The field that is used to identify different sets of transactions:
• B2.4.13 Persistence Group Identifier, PGroupID
• B2.4.14 Stash Group Identifier, StashGroupID
• B2.4.15 Tag Group Identifier, TagGroupID
The field that is used to identify which cache line a Response or Data message relates to within a multi-request
transaction:
• B2.4.16 Cache Line Identifier, CacheLineID
Identifier values in use at an interface by packets on one RP must not be re-used by packets on a different RP,
except when explicitly permitted by this specification for packets originating from the same interface on the same
RP. For more information on Resource Planes, see B14.2.1.2Flow control with Resource Planes.
B2.4.1 Target Identifier, TgtID, and Source Identifier, SrcID
A transaction request includes a TgtID that identifies the target node, and a SrcID that identifies the source node.
These identifiers are used to route packets across the interconnect.
B2.4.2 Transaction Identifier, TxnID
A transaction request includes a TxnID that is used to identify the transaction from a given Requester. It is
required that the TxnID, except for PrefetchTgt, must be unique for a given Requester. The Requester is identified
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
102
```

## PDF page 103

```text
Chapter B2. Transactions
B2.4. Transaction identifier fields
by the SrcID. This ensures that any returning read data or response information can be associated with the correct
transaction.
A 12-bit field is defined for the TxnID with the number of outstanding transactions limited to 1024. A Requester is
permitted to reuse a TxnID value after receiving either:
• All responses associated with a previous transaction that have used the TxnID value from the request that is
not subject to a request retry.
Note
A Requester is permitted to reuse a TxnID when there is still an outstanding TagMatch, StashDone, or
Persist response.
The TxnID in TagMatch, StashDone, and Persist responses is inapplicable and must be set to 0. The
mapping of these responses back to their original transaction is achieved through the TagGroupID,
StashGroupID and PGroupID fields.
• A RetryAck response for a previous transaction that used the TxnID value from the request.
B2.5 Transaction identifier field flowsgives more detailed rules for the different transaction types. The TxnID field
is not applicable in a PrefetchTgt request and must be 0.
A value used in the TxnID field of a Request from Home to Subordinate can be reused by Home once all responses
that are required to deallocate the request are received or a RetryAck response is received.
A transaction that is retried is not required to use the same TxnID. See B2.10 Request Retry.
B2.4.3 Data Buffer Identifier, DBID
The DBID field permits the Completer of a transaction to provide its own identifier for a transaction. The
Completer sends a response that includes a DBID. The DBID value is used as the TxnID field value in the:
• WriteData response of Immediate Write, CopyBack Write, Combined Write, Atomic, and DVMOp
transactions.
• CompData response of Stash transactions for Data Pull purposes.
• CompAck response of:
– Read, Dataless, WriteNoSnp, WriteUnique, and Immediate Combined Write transcations that include a
CompAck response.
– CopyBack transactions that complete without a data transfer.
The DBID value used by a Completer in responses of a given transaction must be unique for a given Requester in
the following cases:
• DBIDResp or DBIDRespOrd or CompDBIDResp for all Write transactions, except in WriteNoSnpZero and
WriteUniqueZero.
• DBIDResp or DBIDRespOrd or CompDBIDResp for all Combined Write transactions.
• DBIDResp or DBIDRespOrd or CompDBIDResp for Atomic* transactions.
• DBIDResp or DBIDRespOrd or CompDBIDResp for DVMOp transactions.
• CompData or RespSepData for Read transactions that include CompAck, except in the case when
ReadOnce* and ReadNoSnp do not use the resultant CompAck for deallocation of the request at Home.
• Comp for:
– Dataless transactions that include CompAck.
– CopyBack transactions that complete without a data transfer.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
103
```

## PDF page 104

```text
Chapter B2. Transactions
B2.4. Transaction identifier fields
The DBID value is applicable in the DataSepResp response to Read requests that include CompAck, and it must
be the same as the DBID value in the associated RespSepData response.
A Comp response message sent separate from a DBIDResp or DBIDRespOrd message for a Write or Combined
Write transaction must include the same DBID field value in the Comp and DBIDResp or DBIDRespOrd message
when the two messages originate from the same source.
A Comp response message sent separate from a DBIDResp or DBIDRespOrd message for a Atomic transaction is
permitted, but is not required, to include the same DBID field value in the Comp and DBIDResp or DBIDRespOrd
message.
A Completer is permitted, but not required, to use the same DBID value for two transactions with different
Requesters. A Completer is permitted to reuse a DBID value after it has received all packets required to deallocate
a previous transaction that has used the same value. B2.5 Transaction identifier field flowsgives more detailed
rules for the different transaction types.
The DBID value used by a Snoop Completer in response to a Stash snoop that includes a Data Pull must be unique
with respect to:
• The DBID values in other Snoop responses to Stash snoops that use Data Pull.
• The TxnID of any outstanding request from that Snoop Completer.
The Completer is not required to utilize the DBID field, and is permitted to set the DBID to any value in:
• WriteNoSnpZero and WriteUniqueZero transactions.
• Read transactions without CompAck.
• Dataless transactions without CompAck.
• SnpResp response to either:
– Stash snoop that does not include a Data Pull.
– Non-stash snoop.
Note
The advantage of using the DBID assigned by the Completer, instead of the TxnID assigned by the
Requester, is that the Completer can use the DBID to index into its request structure instead of performing a
lookup using TxnID and SrcID to determine which transaction write data or completion acknowledge is
associated with which request.
If a Completer is using the same DBID value for different Requesters, which it must do if its operation
requires more than 1024 DBID responses to be active at the same time, SrcID with DBID must be used to
determine which request should be associated with a write data or response message.
The DBID field is inapplicable and must be zero for the following responses:
• SnpRespData and SnpRespDataPtl when DataPull is 0.
• SnpRespDataFwded.
The DBIDResp response is also used to provide certain ordering guarantees relating to the transaction. See B2.7.5
Transaction ordering.
B2.4.4 Return Transaction Identifier, ReturnTxnID
A transaction request from Home to Subordinate also includes a ReturnTxnID field to convey the value of TxnID
in the data response and the DBIDResp response from the Subordinate.
Its value, when applicable, must be either:
• The TxnID generated by Home, when the ReturnNID is the node ID of the Home.
• The TxnID of the original Requester, when the ReturnNID is the node ID of the original Requester.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
104
```

## PDF page 105

```text
Chapter B2. Transactions
B2.4. Transaction identifier fields
ReturnTxnID is only applicable in a ReadNoSnp, ReadNoSnpSep, WriteNoSnp, Combined Write, and Atomic*
requests from Home to Subordinate. The field is inapplicable and must be zero in all other requests from Home to
Subordinate.
ReturnTxnID is inapplicable and must be zero in all requests from Requester to Home, and Requester to
Subordinate.
The following are the expected and permitted values for ReturnTxnID in requests from the Home Node to the
Subordinate Node.
In ReadNoSnp and ReadNoSnpSep:
• Expected value is the original Requester TxnID but permitted to be the Home TxnID.
• Used as the TxnID in the CompData and DataSepResp responses.
In Atomic with TagOp Invalid or Match:
• For AtomicStore, the ReturnTxnID can take any value, and the value is not used in any response.
• For Non-store Atomics, the ReturnTxnID must be the Home TxnID. The value is used as the TxnID in the
CompData response.
In WriteNoSnp with any TagOp value:
• When DoDWT = 0, ReturnTxnID can take any value, and the value is not used in any response.
• When DoDWT = 1, the ReturnTxnID value is expected to be the original Requester TxnID but is permitted
to be the Home TxnID. Used as the TxnID in the DBIDResp response.
In WriteNoSnpDef:
• When DoDWT = 0, ReturnTxnID can take any value, and the value is not used in any response.
• When DoDWT = 1, the ReturnTxnID value is expected to be the original Requester TxnID but is permitted
to be the Home TxnID. Used as the TxnID in the DBIDResp response.
In Combined Write:
• When DoDWT = 0, ReturnTxnID can take any value, and the value is not used in any response.
• When DoDWT = 1, the ReturnTxnID value is expected to be the original Requester TxnID but is permitted
to be the Home TxnID. Used as the TxnID in the DBIDResp response.
B2.4.5 Forward Transaction Identifier, FwdTxnID
A Snoop request from Home to RN-F also includes a FwdTxnID field to convey the value of TxnID in the Data
response from the Snoopee. Its value must be the TxnID of the original Request.
The FwdTxnID field is only applicable in:
• SnpSharedFwd
• SnpCleanFwd
• SnpOnceFwd
• SnpNotSharedDirtyFwd
• SnpUniqueFwd
• SnpPreferUniqueFwd
The FwdTxnID field is inapplicable and must be zero in all other snoops.
B2.4.6 Data Identifier, DataID, and Critical Chunk Identifier, CCID
These fields identify the individual data packets within a transaction.
See B2.9.4 Data packetization and B2.9.7 Critical Chunk Identifier.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
105
```

## PDF page 106

```text
Chapter B2. Transactions
B2.4. Transaction identifier fields
B2.4.7 Logical Processor Identifier, LPID
This field is used when a single Requester contains more than one logically separate processing agent. The SrcID
is used with LPID to uniquely identify the LP that generated the request.
The LPID must be set to the correct value for the following transactions:
• For any Non-snoopable Non-cacheable or Device access:
– ReadNoSnp
– WriteNoSnp
– WriteNoSnpDef
• For Exclusive accesses, that can be one of the following transaction types:
– ReadClean
– ReadShared
– ReadNotSharedDirty
– ReadPreferUnique
– MakeReadUnique
– CleanUnique
– ReadNoSnp
– WriteNoSnp
See Chapter B6 Exclusive accesses for further details.
For other transactions, the LPID value is permitted, but not required, to indicate the original LP that caused a
transaction to be issued.
In requests, when applicable, the same bits in the packet are used for TagGroupID, PGroupID, and StashGroupID.
B2.4.8 Stash Logical Processor Identifier, StashLPID
The StashLPID field can be used to specify a particular LP within the Request Node specified by StashNID, when
the corresponding StashLPIDValid bit is 1. See B13.10.11 Stash Logical Processor Identifier, StashLPID.
See B7.5.1 Supporting REQ packet fields for the permitted combinations of StashLPIDValid and StashNIDValid.
B2.4.9 Stash Node Identifier, StashNID
The StashNID field provides the Request Node that is the target of the Stash transaction when the corresponding
StashNIDValid bit is 1. See B13.10.9 Stash Node Identifier, StashNID.
B2.4.10 Return Node Identifier, ReturnNID
A transaction request from Home to Subordinate includes a ReturnNID that is used to determine the TgtID for the
following responses from the Subordinate Node:
• Data response
• DBIDResp response
• Persist response
• TagMatch response
Its value must be either the node ID of Home or the node ID of the original Requester.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
106
```

## PDF page 107

```text
Chapter B2. Transactions
B2.4. Transaction identifier fields
ReturnNID is only applicable in a ReadNoSnp, ReadNoSnpSep, CleanSharedPersistSep, WriteNoSnp, Combined
Write, and Atomic requests from Home to Subordinate. The field is inapplicable and must be zero in all other
requests from Home to Subordinate.
ReturnNID is inapplicable and must be zero in all requests from Requester to Home and Requester to Subordinate.
The following are the expected and permitted values for the ReturnNID in requests from the Home Node to the
Subordinate Node.
In ReadNoSnp, ReadNoSnpSep, and CleanSharedPersistSep:
• Expected value is the original Requester Node ID but is permitted to be the Home Node ID.
• Used as the TgtID in CompData, DataSepResp, and Persist responses.
In Atomic with TagOp Invalid:
• For AtomicStore, ReturnNID can take any value and the value is not used in any responses.
• For Non-store Atomics, the ReturnNID must be the Home Node ID. The value is used as the TgtID in
CompData.
In Atomic with TagOp Match:
• ReturnNID must be the Home Node ID.
• The value is used as the TgtID in CompData and TagMatch responses.
In WriteNoSnp with TagOp not Match:
• When DoDWT = 0, the ReturnNID can take any value, and the value is not used in any responses.
• When DoDWT = 1, the ReturnNID value is expected to be the original Requester Node ID but is permitted to
be the Home Node ID. Used as the TgtID in the DBIDResp response.
In WriteNoSnp with TagOp Match:
• Irrespective of the value of DoDWT, the ReturnNID value is expected to be the original Requester Node ID
but is permitted to be the Home Node ID.
• When DoDWT = 0, the ReturnNID value is used as the TgtID in the TagMatch response only.
• When DoDWT = 1, the ReturnNID value is used as the TgtID in the DBIDResp and TagMatch responses.
In WriteNoSnpDef:
• When DoDWT = 0, ReturnNID can take any value, and the value is not used in any response.
• When DoDWT = 1, the ReturnNID value is expected to be the original Requester Node ID but is permitted to
be the Home Node ID. Used as the TgtID in the DBIDResp response.
In Non-PCMO Combined Write:
• When DoDWT = 0, ReturnNID can take any value, and the value is not used in any responses.
• When DoDWT = 1, the ReturnNID value is expected to be the original Requester Node ID but is permitted to
be the Home Node ID. Used as the TgtID in the DBIDResp response.
In WriteNoSnpFullClnShPer and WriteNoSnpPtlClnShPer:
• Irrespective of the value of DoDWT, the ReturnNID value is expected to be the original Requester Node ID
but is permitted to be the Home Node ID.
• When DoDWT = 0, the ReturnNID value is used as the TgtID in the Persist response only.
• When DoDWT = 1, the ReturnNID value is used as the TgtID in the DBIDResp and Persist responses.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
107
```

## PDF page 108

```text
Chapter B2. Transactions
B2.4. Transaction identifier fields
B2.4.11 Home Node Identifier, HomeNID
CompData includes the HomeNID field that is used by the Requester to identify the target of CompAck that the
Requester could need to send in response to CompData. HomeNID is applicable in CompData and DataSepResp
and is inapplicable and must be zero for all other Data messages.
Note
There is no functional requirement for the HomeNID and DBID fields in the DataSepResp response because
the values that are provided in the RespSepData response are identical and can always be used. However, it
is required that these values are included to help with debugging and protocol checking.
B2.4.12 Forward Node Identifier, FwdNID
A Snoop request from Home to RN-F includes a FwdNID that is used to determine the TgtID for the Data
response from the Snoopee. Its value must be the node ID of the original Requester.
The FwdNID field is only applicable in:
• SnpSharedFwd
• SnpCleanFwd
• SnpOnceFwd
• SnpNotSharedDirtyFwd
• SnpUniqueFwd
• SnpPreferUniqueFwd
The FwdNID field is inapplicable and must be zero in all other snoops, except range-based Translation Lookaside
Buffer Invalidate (TLBI) DVM operations. For range-based TLBI operations, the bits in the field are used for
DVM payload.
B2.4.13 Persistence Group Identifier, PGroupID
A CleanSharedPersistSep and Combined Write with Persistent CMO (PCMO) request includes a PGroupID to
identify the Persistence Group that the request belongs to. If a Requester has persistent CMO requests from
different functional agents that it would like to identify for performant persistent CMO handling, it can assign a
different PGroupID value to each group of Persist requests. Use of this 8-bit field is applicable in
CleanSharedPersistSep and Combined Write with PCMO transactions. It is also applicable in Persist and
CompPersist responses. It is inapplicable and must be zero in all other requests and responses. See B13.10.8
Persistence Group Identifier, PGroupID:
• PGroupID must be sent in the CleanSharedPersistSep request and a Combined Write request that includes a
PCMO.
• The PGroupID value returned in the Persist response can be used by a Requester to separately track
completions of Persist responses from each group.
• It is expected that a Requester that does not support multiple persistence groups sets the PGroupID value to 0.
• Typically, a Requester that is making use of PGroupID for passing a barrier does not reuse a PGroupID value
until all the earlier sent CleanSharedPersistSep requests from that group have received Persist responses.
• The Completer is required to reflect back PGroupID in the Persist and CompPersist responses, and the
responses of Combined Write requests that include a PCMO.
• The PGroupID field in the Comp and CompCMO response from both the Home and Subordinate is
inapplicable and must be zero.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
108
```

## PDF page 109

```text
Chapter B2. Transactions
B2.4. Transaction identifier fields
B2.4.14 Stash Group Identifier, StashGroupID
To identify the Stash Group that the request belongs to, a StashOnceSep request includes a StashGroupID. The
same StashGroupID value from the request is later used by a StashDone response in the transaction flow. If a
Requester has StashOnceSep requests from different functional agents that can be identified for performant stash
handling, a different StashGroupID value to each group of Stash requests can be assigned.
Use of this 8-bit field is applicable in the StashOnceSep request and StashDone response. StashGroupID is
inapplicable and must be zero in all other requests and responses.
• StashGroupID must be sent in the StashOnceSep request.
• The StashGroupID value returned in the StashDone response can be used by a Requester to separately track
completions of Stash transactions from each group.
• It is expected that a Requester that does not support multiple stash groups sets the StashGroupID value to 0.
• The Completer is required to reflect back StashGroupID in the StashDone response.
See B13.10.13 Stash Group Identifier, StashGroupID.
B2.4.15 Tag Group Identifier, TagGroupID
To identify the Tag group that the request belongs to, a Write request where TagOp is set toMatch includes a
TagGroupID. The same TagGroupID value from the request is later used by a TagMatch response in the
transaction flow to notify the Requester if the TagMatch operation passed or failed.
Use of this 8-bit field is applicable in Write requests where TagOp is set toMatch, and in a TagMatch response.
TagGroupID is inapplicable and must be zero in all other requests and responses.
• TagGroupID must be sent in a Write request where TagOp is set to Match.
• The precise contents of TagGroupID are IMPLEMENTATION SPECIFIC . Typically, TagGroupID is expected to
contain an Exception Level, TTBR value, and PE identifier.
See B13.10.41 Tag Group Identifier, TagGroupID.
B2.4.16 Cache Line Identifier, CacheLineID
The CacheLineID field is used on the RSP and DAT channels to identify to which cache line a Response or Data
message corresponds.
For both multi-request and single-request transactions, when the MultiReq_Support property is True or
CacheLineID_Accurate, the CacheLineID field, when applicable, must match the relevant bits of the associated
request or snoop address. This enables differentiation of multiple cache line responses that share the same
transaction identifier, particularly in multi-request transaction flows.
See B13.10.66 CacheLineID and B2.6 Multi-request for more information.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
109
```

## PDF page 110

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
B2.5 Transaction identifier field flows
This section shows the transaction identifier field flows for the different transaction types:
• B2.5.1 Read transactions
• B2.5.2 Dataless transactions
• B2.5.3 Write transactions
• B2.5.4 DVMOp transaction
• B2.5.5 Transaction requests with Retry
• B2.5.6 Protocol Credit Return transaction
In the associated figures:
• The fields included in each packet are:
– For a Request packet: TgtID, SrcID, TxnID, StashNID, StashLPID, ReturnNID, ReturnTxnID,
PGroupID, StashGroupID, and TagGroupID.
– For a Response packet: TgtID, SrcID, TxnID, DBID, PGroupID, StashGroupID, and TagGroupID.
– For a Data packet: TgtID, SrcID, TxnID, HomeNID, and DBID.
– For a Snoop packet: SrcID, TxnID, FwdNID, FwdTxnID, and StashLPID.
• All fields with the same color are the same value.
• The curved loop-back arrows show how the Requester and Completer use fields from earlier packets to
generate fields for subsequent packets.
• A box containing an asterisk [*] indicates when a field is first generated, that is, indicating the agent that
determines the original value of the field.
• A field enclosed in parentheses indicates that the value is effectively a fixed value. Typically this is the case
for the SrcID field when a packet is sent, and the TgtID field when a packet arrives at its destination.
• A field that is crossed-out indicates that the field is not valid.
• It is permitted for the TgtID of the original transaction to be remapped by the interconnect to a new value.
This is shown by a box containing the letter R. This is explained in more detail in Chapter B3 Network Layer.
Note
An identifier field, in every packet sent, belongs to one of the following categories:
• New value. An asterisk indicates that a new value is generated.
• Generated from an earlier packet. A loop back arrow indicates the source.
• Fixed value. The value is enclosed in brackets.
• Not valid. The field is crossed-out.
In the following examples, any transaction identifiers that are not relevant for the example are sometimes omitted
for clarity.
B2.5.1 Read transactions
This section shows the identifier field flows in Read transactions with and without Direct Data Transfer:
• B2.5.1.1 ID value transfer with DMT
• B2.5.1.2 ID value transfer with DMT and separate Comp and Data
• B2.5.1.3 ID value transfer with DCT
• B2.5.1.4 ID value transfer without Direct Data Transfer
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
110
```

## PDF page 111

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
B2.5.1.1 ID value transfer with DMT
Figure B2.23 shows how the Target and Transaction ID values in the DMT transaction messages are derived. For
example, the value of SrcID in the ReadNoSnp request from the interconnect is assigned by the interconnect.
Whereas the ReturnNID, used as TgtID in the Data response, is set to the value of SrcID of the received Read
request.
RN
Read ReadNoSnp
CompAck
ICN SN
CompData CompData
SrcID
TxnID
(TgtID)
ReturnNID
ReturnTxnID
TgtID*
(SrcID)*
TxnID*
TgtID
TxnID
HomeNID
DBID
(SrcID)
(TgtID)
SrcID
DBID
HomeNID
TxnID
TgtID
TxnID
(SrcID)
DBID
SrcID
TxnID
ReturnNID
ReturnTxnID
(TgtID)
TgtID
TxnID
(SrcID)
DBID
(SrcID)*
TxnID*
TgtID* R
To RN
ReadReceipt
(Optional)
Figure B2.23: ID value transfer in a DMT transaction
The required steps in the flow that Figure B2.23 shows are:
1. The Requester starts the transaction by sending a Request packet.
The identifier fields of the request are generated as follows:
• The TgtID is determined by the destination of the Request.
Note
The TgtID field can be remapped to a different value by the interconnect.
• The SrcID is a fixed value for the Requester.
• The Requester generates a TxnID field that is unique for that Requester.
2. The recipient Home Node in the interconnect generates a Request to the Subordinate Node.
The identifier fields of the request are generated as follows:
• The TgtID is set to the value required for the Subordinate.
• The SrcID is a fixed value for the Home.
• The TxnID is a unique value generated by the Home.
• The ReturnNID is set to the same value as the SrcID of the original request.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
111
```

## PDF page 112

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
• The ReturnTxnID is set to the same value as the TxnID of the original request.
3. If the request to the Subordinate requires a ReadReceipt, the Subordinate provides the read receipt.
The identifier fields of the ReadReceipt response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Subordinate. This also matches the TgtID received.
• The TxnID is set to the same value as the TxnID of the request.
• The DBID field is not valid.
4. The Subordinate provides the read data.
The identifier fields of the Read data response are generated as follows:
• The TgtID is set to the same value as the ReturnNID of the request.
• The SrcID is a fixed value for the Subordinate. This also matches the TgtID received.
• The TxnID is set to the same value as the ReturnTxnID of the request.
• The HomeNID is set to the same value as the SrcID of the request.
• The DBID is set to the same value as the TxnID of the request.
5. The Requester receives the read data and sends a completion acknowledge, CompAck, response.
The identifier fields of the CompAck are generated as follows:
• The TgtID is set to the same value as the HomeNID of the read data.
• The SrcID is a fixed value for the Requester. This also matches the TgtID that was received.
• The TxnID is set to the same value as the DBID of the read data.
• The DBID field is not valid.
The CompAck response from Requester to Home is not required for all requests.
If the original request requires a ReadReceipt, the following additional step is included:
• The Home receives the Request packet and provides the read receipt. The identifier fields of the ReadReceipt
response are generated as follows:
– The TgtID is set to the same value as the SrcID of the request.
– The SrcID is a fixed value for the Completer. This also matches the TgtID received.
– The TxnID is set to the same value as the TxnID of the request.
– The DBID field is not valid.
B2.4 Transaction identifier fieldsdetails when the TxnID value and DBID value can be reused.
B2.5.1.2 ID value transfer with DMT and separate Comp and Data
Figure B2.24 shows how the identifier field values are derived in DMT transaction messages that use separate
Comp and Data.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
112
```

## PDF page 113

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
RN SN
DataSepResp
CompAck
RespSepData
Read
ReadNoSnpSep
DataSepResp
TxnID*
TgtID* R
(SrcID)*
TgtID
TxnID
(SrcID)
DBIDTgtID
(SrcID)
DBID
TxnID
SrcID
TxnID
ReturnNID
ReturnTxnID
(TgtID)
TgtID
TxnID
(SrcID)
HomeNID
DBID
(TgtID)
TxnID
SrcID
HomeNID
DBID
ReadReceipt
SrcID
TxnID
DBID
(TgtID)
ICN
ReturnNID
ReturnTxnID
(SrcID)*
TxnID*
TgtID*
SrcID
TxnID
(TgtID)
TxnID
TgtID
(SrcID)
* DBID
To RN
Figure B2.24: ID value transfer in a DMT transaction with separate Comp and Data
The required steps in the flow that Figure B2.24 shows are:
1. The Requester starts the transaction by sending a Request packet.
The identifier fields of the request are generated as follows:
• The TgtID is determined by the destination of the Request.
Note
The TgtID field can be remapped to a different value by the interconnect.
• The SrcID is a fixed value for the Requester.
• The Requester generates a TxnID field that is unique for that Requester.
2. The recipient Home Node in the interconnect generates a request to the Subordinate Node.
The identifier fields of the request are generated as follows:
• The TgtID is set to the value required for the Subordinate.
• The SrcID is a fixed value for the Home.
• The TxnID is a unique value generated by the Home.
• The ReturnNID is set to the same value as the SrcID of the original request.
• The ReturnTxnID is set to the same value as the TxnID of the original request.
3. The recipient Home Node in the interconnect provides the separate Read response.
The identifier fields of the read response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
113
```

## PDF page 114

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
• The SrcID is a fixed value for the Home.
• The TxnID is set to the same value as the TxnID of the original request.
• The DBID value is a unique value generated by the Home and is the same value as the TxnID in the
request to the Subordinate.
4. The Requester receives the Read response and sends a completion acknowledge, CompAck, response.
The identifier fields of the CompAck are generated as follows:
• The TgtID is set to the same value as the SrcID of the read response.
• The SrcID is a fixed value for the Requester.
• The TxnID is set to the unique DBID value generated by the Home.
• The DBID value is not valid.
5. The request to the Subordinate requires a ReadReceipt. The Subordinate provides the read receipt.
The identifier fields of the ReadReceipt response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Subordinate. This also matches the TgtID received.
• The TxnID is set to the same value as the TxnID of the request.
6. The Subordinate provides the separate read data.
The identifier fields of the read data are generated as follows:
• The TgtID is set to the same value as the ReturnNID of the request.
• The SrcID is a fixed value for the Subordinate. This also matches the TgtID received.
• The TxnID is set to the same value as the ReturnTxnID of the request.
• The HomeNID is set to the same value as the SrcID of the request.
• The DBID is set to the same value as the TxnID of the request.
B2.5.1.3 ID value transfer with DCT
Figure B2.25 shows how the identifier field values are derived in DCT transaction messages. In this example, the
data is forwarded to a Request Node and a Snoop response is sent to HN-F with or without data.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
114
```

## PDF page 115

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
RN
Read Snp[*]Fwd
CompAck
ICN RN-F
To HN-FTo HN-F
CompData
SrcID
TxnID
(TgtID)
FwdNID
FwdTxnID
(SrcID)*
TxnID*
SrcID
TxnID
FwdNID
FwdTxnID
TgtID
TxnID
HomeNID
DBID
(SrcID)*
(TgtID)
TxnID
DBID
HomeNID
SrcID
TgtID
TxnID
(SrcID)*
DBID
TgtID
TxnID
(SrcID)
DBID
(SrcID)*
TxnID*
TgtID* R
To RN
SnpRespFwded
or
SnpRespDataFwded
CompData
Figure B2.25: ID value transfer in a DCT transaction
The required steps in the flow that Figure B2.25 shows are:
1. The Requester starts the transaction by sending a Request packet.
The identifier fields of the request are generated as follows:
• The TgtID is determined by the destination of the Request.
Note
The TgtID field can be remapped to a different value by the interconnect.
• The SrcID is a fixed value for the Requester.
• The Requester generates a TxnID field that is unique for that Requester.
2. The recipient Home Node in the interconnect generates a Forwarding snoop to the RN-F node.
The identifier fields of the snoop are generated as follows:
• The SrcID is a fixed value for the Home.
• The TxnID is a unique value generated by the Home.
• The FwdNID is set to the same value as the SrcID of the original request.
• The FwdTxnID is set to the same value as the TxnID of the original request.
3. The RN-F provides the read data.
The identifier fields of the Read data response are generated as follows:
• The TgtID is set to the same value as the FwdNID of the snoop.
• The SrcID is a fixed value for the RN-F.
• The TxnID is set to the same value as the FwdTxnID of the snoop.
• The HomeNID is set to the same value as the SrcID of the snoop.
• The DBID is set to the same value as the TxnID of the snoop.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
115
```

## PDF page 116

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
4. The RN-F also provides a response to Home, either with or without read data.
The identifier fields of the response are generated as follows:
• The TgtID is set to the same value as the SrcID of the snoop.
• The SrcID is a fixed value for the RN-F.
• The TxnID is set to the same value as the TxnID of the snoop.
• The DBID field is not valid.
5. The Requester receives the read data and sends a completion acknowledge, CompAck, response.
The identifier fields of the CompAck are generated as follows:
• The TgtID is set to the same value as the HomeNID of the read data.
• The SrcID is a fixed value for the Requester. This also matches the TgtID that was received.
• The TxnID is set to the same value as the DBID of the read data.
• The DBID field is not valid.
Note
An optional ReadReceipt from the interconnect to Requester can also be included.
B2.5.1.4 ID value transfer without Direct Data Transfer
This section gives an example of a Read identifier field flow without DMT or DCT and describes the use of the
TxnID and DBID fields for Read transactions.
The Requester and Completer in this example are a Request Node and an HN-F respectively.
The identifier field flow includes an optional ReadReceipt response from the Completer, and an optional CompAck
response from the Requester.
For Read transactions that include a CompAck response, the DBID is used by the Completer to associate the
CompAck with the original transaction.
A Read transaction that does not include a CompAck response does not require a valid DBID field in the data
response.
Figure B2.26 shows the ID value transfer.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
116
```

## PDF page 117

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
ReadReq
Requester
CompAck
Completer
ReadReceipt
Optional
Optional
CompData
(TgtID)
SrcID
TxnID
(SrcID)
TgtID
TxnID
DBID
DBIDDBID
(TgtID)
SrcID
TxnID
DBID
(TgtID)
SrcID
TxnID
TgtID
(SrcID)
TxnID
TgtID
(SrcID)
TxnID
DBID *
(HomeNID) *
(TgtID)
SrcID
TxnID
DBID
HomeNID
(SrcID)*
TxnID*
TgtID R*
Figure B2.26: ID value transfer in a Read request with ReadReceipt and CompAck
The required steps in the flow that Figure 2-26 shows are:
1. The Requester starts the transaction by sending a Request packet.
The identifier fields of the request are generated as follows:
• The TgtID is determined by the destination of the Request.
Note
The TgtID field can be re-mapped to a different value by the interconnect.
• The SrcID is a fixed value for the Requester.
• The Requester generates a TxnID field that is unique for that Requester.
2. If the transaction includes a ReadReceipt, the Completer receives the Request packet and provides the read
receipt.
The identifier fields of the ReadReceipt response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Completer. This also matches the TgtID received.
• The TxnID is set to the same value as the TxnID of the request.
• The DBID field is not valid.
3. The Completer receives the Request packet and provides the read data.
The identifier fields of the read data response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Completer. This also matches the TgtID received.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
117
```

## PDF page 118

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
• The TxnID is set to the same value as the TxnID of the request.
• The HomeNID is a fixed value for the Completer. This also matches the TgtID received.
• The Completer generates a unique DBID value if ExpCompAck in the request is 1.
4. The Requester receives the read data and sends a completion acknowledge, CompAck, response.
The identifier fields of the CompAck are generated as follows:
• The TgtID is set to the same value as the HomeNID of the read data.
• The SrcID is a fixed value for the Requester. This also matches the TgtID that was received.
• The TxnID is set to the same value as the DBID of the read data.
• The DBID field is not valid.
B2.5.2 Dataless transactions
For Dataless transactions, except for CleanSharedPersistSep and StashOnceSep, the use of identifier fields is
similar to B2.5.1.4 ID value transfer without Direct Data Transfer. The only difference is that the response from
the Completer to the Requester is sent as a single packet on the CRSP channel instead of multiple packets on the
RDAT channel.
For StashOnceSep transactions, the StashGroupID value is sent in the request from the Request Node to the
interconnect and the value is returned in the StashDone and CompStashDone responses. The TxnID value in the
StashDone response is inapplicable and must be zero.
The description of ID value transfer in a CleanSharedPersistSep transaction follows.
B2.5.2.1 ID value transfer in a CleanSharedPersistSep transaction
Figure B2.27 shows how the identifier field values are derived in CleanSharedPersistSep transaction messages that
use separate Comp and Persist responses. In Figure B2.27, PCMOSep represents CleanSharedPersistSep.
RN
PCMOSep
PCMOSep
ICN SN
Comp
PersistPersist
TgtID* R
(SrcID)*
TxnID*
PGroupID*
SrcID
TxnID
(TgtID)
PGroupID
ReturnNID
TgtID*
(SrcID)*
TxnID*
PGroupID
ReturnTxnID
SrcID
TxnID
ReturnNID
(TgtID)
PGroupID
ReturnTxnID
TgtID
TxnID
(SrcID)
TgtID
PGroupID
(SrcID)
TxnID
(TgtID)
SrcID
PGroupID
TxnID
Comp
TgtID
TxnID
(SrcID)
TgtID
TxnID
(SrcID)
(TgtID)
TxnID
SrcID
To RN
Figure B2.27: ID value transfer in a CleanSharedPersistSep transaction
The required steps in the flow that Figure B2.27 shows are:
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
118
```

## PDF page 119

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
1. The Requester starts the transaction by sending a Request packet.
The identifier fields of the Request are generated as follows:
• The TgtID is determined by the destination of the Request.
Note
The TgtID field can be remapped to a different value by the interconnect.
• The SrcID is a fixed value for the Requester.
• The Requester generates a TxnID value that is unique for that Requester.
The TxnID value can be reused by the Requester after receiving the Comp response.
• The Requester generates a new PGroupID value, or reuses a PGroupID value currently in use.
2. The recipient Home Node in the interconnect generates a request to the Subordinate.
The identifier fields of the request to the Subordinate Node are generated as follows:
• The TgtID is set to the value required for the Subordinate.
• The SrcID is a fixed value for the Home.
• The TxnID is a unique value generated by the Home.
The TxnID value can be reused by the Home after receiving the Comp response.
• The ReturnNID is set to the same value as the SrcID of the original request.
• The ReturnTxnID is inapplicable and must be zero.
• The PGroupID is set to the same value as the PGroupID of the original request.
3. The recipient Home Node in the interconnect sends a Comp response to the Requester.
The identifier fields of the Comp response to the Requester are generated as follows:
• The TgtID is set to the same value as the SrcID of the original request.
• The SrcID is a fixed value for the Home.
• The TxnID is set to the same value as the TxnID of the original request.
4. The recipient Home Node can optionally send a Persist response to the Requester.
The identifier fields of the optional Persist response from the Home Node to the Requester, not shown in
Figure B2.27, are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Home Node.
• The TxnID is inapplicable and must be zero.
• The PGroupID is set to the same value as the PGroupID of the request.
The recipient Home Node can optionally send a combined CompPersist response to the Requester, instead of
separate Comp and Persist responses.
The identifier fields in the CompPersist response are generated as follows:
• The TgtID is set to the same value as the SrcID of the original request.
• The SrcID is a fixed value for the Home.
• The TxnID is set to the same value as the TxnID of the original request.
• The PGroupID is set to the same value as the PGroupID of the original request.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
119
```

## PDF page 120

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
5. The Subordinate Node generates a Comp to the Home Node.
The identifier fields of the Comp response from the Subordinate Node are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Subordinate.
• The TxnID is set to the same value as the TxnID of the request.
6. The Subordinate Node also generates a Persist response to either to the Requester or the Home.
The identifier fields of the Persist response from the Subordinate Node are generated as follows:
• The TgtID is set to the same value as the ReturnNID of the request.
• The SrcID is a fixed value for the Subordinate.
• The TxnID is inapplicable and must be zero.
• The PGroupID is set to the same value as the PGroupID of the request.
7. The Subordinate Node can optionally send a combined CompPersist response to the Home Node, instead of
separate Comp and Persist responses if the ReturnNID and SrcID of the request are the same value.
The identifier fields of the CompPersist response from the Subordinate are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Subordinate.
• The TxnID is set to the same value as the TxnID of the request.
• The PGroupID is set to the same value as the PGroupID of the request.
B2.5.3 Write transactions
This section describes the use of TxnID and DBID fields for Write transactions:
• B2.5.3.1 CopyBack
• B2.5.3.2 WriteNoSnp transaction
• B2.5.3.3 WriteUnique transaction
• B2.5.3.4 StashOnce or StashOnceSep transaction
B2.5.3.1 CopyBack
This section describes the use of the identifier fields for a CopyBack transaction.
Figure B2.28 shows the identifier value transfer.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
120
```

## PDF page 121

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
CopyBack
Requester
CompDBIDResp
Completer
WriteData
TgtID
(SrcID)
TxnID
DBID *
(TgtID)
SrcID
TxnID
(TgtID)
SrcID
TxnID
DBID
*
*
(SrcID)
TxnID
TgtID R*
TgtID
(SrcID)
TxnID
DBID
(TgtID)
SrcID
TxnID
DBID
Figure B2.28: ID value transfer in a CopyBack
The required steps in the flow that Figure B2.28 shows are:
1. The Requester starts the transaction by sending a Request packet.
The identifier fields of the request are generated as follows:
• The TgtID is determined by the destination of the Request.
Note
The TgtID field can be remapped to a different value by the interconnect.
• The SrcID is a fixed value for the Requester.
• The Requester generates a unique TxnID field.
2. The Completer receives the Request packet and generates a CompDBIDResp response.
The identifier fields of the response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Completer. This also matches the TgtID received.
• The TxnID is set to the same value as the TxnID of the request.
• The Completer generates a unique DBID value.
3. The Requester receives the CompDBIDResp response and sends the write data.
The identifier fields of the write data are generated as follows:
• The TgtID is set to the same value as the SrcID of the CompDBIDResp response. This can be different
from the original TgtID of the request if the value was remapped by the interconnect.
• The SrcID is a fixed value for the Requester.
• The TxnID is set to the same value as the DBID value provided in the CompDBIDResp response.
• The DBID field in the write data is not used.
• The TgtID, SrcID, and TxnID fields must be the same for all write data packets.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
121
```

## PDF page 122

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
After receiving the CompDBIDResp response, the Requester can reuse the same TxnID value used in the
request packet for another transaction.
4. The Completer receives the write data and uses the TxnID field, which now contains the DBID value that the
Completer generated. This helps to determine which transaction to associate the write data.
After receiving all write data packets, the Completer can reuse the same DBID value for another transaction.
B2.5.3.2 WriteNoSnp transaction
This section describes the use of the identifier fields for a WriteNoSnp transaction.
Figure B2.29 does not show the Memory Tagging supported TagGroupID flow. For TagGroupID transfer details,
see B12.5 Write transactions.
Figure B2.29 shows the identifier value transfer for separate Comp and DBIDResp. The Completer can
opportunistically combine the Comp and DBIDResp into a single CompDBIDResp response. The Requester can
opportunistically combine NonCopyBackWriteData with CompAck.
WriteNoSnp
Requester
DBIDResp
Completer
Comp
(TgtID)
SrcID
TxnID
TgtID
(SrcID)
TxnID
DBID
(TgtID)
SrcID
TxnID
DBID
(TgtID)
SrcID
TxnID
DBID
TgtID
(SrcID)
TxnID
DBID *
TgtID
(SrcID)
TxnID
DBID
(TgtID)
SrcID
TxnID
DBID
CompAck
TgtID
(SrcID)
TxnID
DBID
TxnID*
(SrcID)*
TgtID R*
Optional
Optional
NCBWrData
NCBWrDataCompAck
NCBWrData = NonCopyBackWriteData
NCBWrDataCompAck = NonCopyBackWriteDataCompAck
TgtID
(SrcID)
TxnID
DBID
TgtID
(SrcID)
TxnID
DBID
TgtID
(SrcID)
TxnID
DBID
Figure B2.29: ID value transfer in a WriteNoSnp
The uses of the identifier fields are the same as for a transaction with a combined response with the additional
requirements that:
• The identifier fields used for the separate DBIDResp and Comp responses must be identical.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
122
```

## PDF page 123

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
• The TxnID value must only be reused by a Requester when both the DBIDResp and Comp responses have
been received.
The required steps in the flow that Figure B2.29 shows are:
1. The Requester starts the transaction by sending a Request packet.
The identifier fields of the request are generated as follows:
• The TgtID is determined by the destination of the Request.
Note
The TgtID field can be remapped to a different value by the interconnect.
• The SrcID is a fixed value for the Requester.
• The Requester generates a unique TxnID field.
2. The Completer receives the Request packet and generates a DBIDResp response.
The identifier fields of the response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Completer. This also matches the TgtID received.
• The TxnID is set to the same value as the TxnID of the request.
• The Completer generates a unique DBID value.
3. The Requester receives the DBIDResp response and sends the write data.
The identifier fields of the write data are generated as follows:
• The TgtID is set to the same value as the SrcID of the DBIDResp response. This can be different from
the original TgtID of the request if the value was remapped by the interconnect.
• The SrcID is a fixed value for the Requester.
• The TxnID is set to the same value as the DBID value provided in the DBIDResp response.
• The DBID field in the write data is not used.
• The TgtID, SrcID, and TxnID fields must be the same for all write data packets.
4. The Completer receives the write data and uses the TxnID field, which now contains the DBID value that the
Completer generated, to determine which transaction the write data is associated with.
5. The Completer generates a Comp response when the transaction is complete.
The identifier fields of the Comp response must be the same as the DBIDResp response and are generated as
follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Completer. This also matches the TgtID received.
• The TxnID is set to the same value as the TxnID of the request.
• The Completer uses the same DBID value as is used in the DBIDResp response.
6. The Requester sends a CompAck message, if required by the transaction, after receiving DBIDResp or
Comp.
The identifier fields of the CompAck are generated as follows:
• The TgtID is set to the same value as the SrcID of the DBIDResp or Comp response.
• The SrcID is a fixed value for the Requester. This also matches the TgtID that was received.
• The TxnID is set to the same value as the DBID of the DBIDResp or Comp response.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
123
```

## PDF page 124

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
• The DBID field is not valid.
After receiving both the Comp and DBIDResp response, the Requester can reuse the same TxnID value for
another transaction.
After receiving all the write data packets, the Completer can reuse the same DBID value for another transaction.
Note
There is no ordering requirement between the separate DBIDResp and Comp responses. It is required that
the values used are identical when the two messages originate from the same source.
B2.5.3.3 WriteUnique transaction
This section describes the use of the identifier fields for a WriteUnique transaction.
Figure B2.30 does not show the Memory Tagging supported TagGroupID flow. For TagGroupID transfer details,
see B12.5 Write transactions.
Under certain circumstances, the WriteUnique transaction can also include a CompAck response from the
Requester to the Completer. In this case, the additional rules for the use of the identifier fields are:
• The TgtID, SrcID, and TxnID identifier fields of the CompAck response from the Requester to the Completer
must be the same as the fields used for the write data, that is:
– The TgtID is set to the same value as the SrcID of the CompDBIDResp response. If separate Comp and
DBIDResp responses are given, the TgtID is set to the same value as the SrcID of either the Comp or
DBIDResp response because the SrcID value in both must be identical. However, this can be different
from the original TgtID of the request if the value has been remapped by the interconnect.
– The SrcID is a fixed value for the Requester.
– The TxnID is set to the same value as the DBID value provided in the CompDBIDResp response. If
separate Comp and DBIDResp responses are given, the TxnID is set to the same value as the DBID of
either the Comp or DBIDResp response because the DBID value in both must be identical.
– The DBID field in the WriteData and in the CompAck is not used.
– If a combined WriteData and CompAck response is sent, the TgtID is set to the same value as the SrcID
in the Comp, DBIDResp, or CompDBIDResp, and the TxnID in the combined response is set to the
same value as the DBID in Comp, DBIDResp, or CompDBIDResp.
• The Completer must receive all items of write data and the CompAck response before reusing the same
DBID value for another transaction.
Figure B2.30 shows the identifier value transfer with a combined CompDBIDResp response.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
124
```

## PDF page 125

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
WriteUnique
Requester
CompDBIDResp
Completer
CompAck
WriteData
(TgtID)
SrcID
TxnID
DBID
(TgtID)
SrcID
TxnID
TgtID
(SrcID)
TxnID
DBID
(TgtID)
SrcID
TxnID
DBID
TgtID
(SrcID)
TxnID
DBID *
TgtID
(SrcID)
TxnID
DBID
(TgtID)
SrcID
TxnID
DBID
(SrcID)*
TxnID*
TgtID R*
Figure B2.30: ID value transfer with a combined CompDBIDResp response
Figure B2.31 shows the identifier value transfer with a combined WriteData and CompAck response.
WriteUnique
Requester
CompDBIDResp
Completer
(TgtID)
SrcID
TxnID
(TgtID)
SrcID
TxnID
DBID
TgtID
(SrcID)
TxnID
DBID *
TgtID
(SrcID)
TxnID
DBID
(TgtID)
SrcID
TxnID
DBID
(SrcID)*
TxnID*
TgtID R*
Alternative combined WriteData and CompAck
NCBWrDataCompAck
NCBWrDataCompAck = NonCopyBackWriteDataCompAck
Figure B2.31: ID value transfer with a combined WriteData and CompAck response
B2.5.3.4 StashOnce or StashOnceSep transaction
This section describes the use of the identifier fields for a StashOnce or StashOnceSep transaction with DataPull.
Figure B2.32 shows the identifier value transfer.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
125
```

## PDF page 126

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
TxnID
RN
StashOnce or 
StashOnceSep
Snp[*]Stash
ICN
RN-F
SnpResp_I_Read
CompAck
CompData
StashLPID
(SrcID)*
TxnID*
SrcID
TxnID
StashLPID
SrcID
(TgtID)
DBID
TgtID
TxnID
(SrcID)
DBID*
(HomeNID)*
SrcID
(TgtID)
DBID
TxnID
HomeNID
StashGroupID*
StashLPID*
StashNID*
TxnID*
(SrcID)*
TgtID* R
SrcID
TxnID
StashLPID
StashNID
(TgtID)
StashGroupID RN-F Node ID
same as
StashNID
(SrcID)
TgtID
DBID *
(SrcID)
TxnID
TgtID
DBID
Comp
StashGroupID
TgtID
TgtID
TxnID
TgtID
TxnID
StashGroupID
CompStashDone
Alternative combined 
Comp and 
StashDone
StashDone
For StashOnceSep TxnID TxnID
Figure B2.32: ID value transfer in a Stash transaction
The required steps in the flow that Figure B2.32 shows are:
1. The Requester starts the transaction by sending a Stash request packet.
The identifier fields of the request are generated as follows:
• The TgtID is determined by the destination of the Request.
Note
The TgtID field can be remapped to a different value by the interconnect.
• The SrcID is a fixed value for the Requester.
• The Requester generates a TxnID field that is unique for that Requester.
• The Requester includes the StashNID field to indicate to which RN-F to send the Stash.
• The Requester includes the StashLPID field to indicate the LP within the RN-F.
2. The Home Node in the interconnect receives the Stash request packet and sends the Comp response to the
Request Node.
The identifier fields of the Comp response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
126
```

## PDF page 127

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
• The TxnID is set to the same value as the TxnID of the request.
3. The Home Node in the interconnect, for the StashOnceSep request, sends the StashDone response to the
Request Node.
The identifier fields of the StashDone response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The TxnID is not valid.
• StashGroupID is set to the same value as the StashGroupID of the request.
Alternatively for the StashOnceSep request, the Home Node in the interconnect sends the combined
CompStashDone response instead of separate Comp and StashDone responses to the Request Node.
The identifier fields of the CompStashDone response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The TxnID is set to the same value as the TxnID of the request.
• The StashGroupID is set to the same value as the StashGroupID of the request.
4. The Home Node in the interconnect generates a snoop with Stash to the appropriate RN-F.
The identifier fields of the request are generated as follows:
• The SrcID is a fixed value for the Home.
• The TxnID is a unique value generated by the Home.
• The StashLPID is set to the same value as the StashLPID of the original request.
Note
A Snoop request does not include a TgtID field.
5. The snooped RN-F generates a Snoop response. In this example, a Data Pull indication is included.
The identifier fields of the Snoop response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the RN-F.
• The TxnID is set to the same value as the TxnID of the request.
• The DBID field is a unique value generated by the RN-F.
6. The Home provides the read data.
The identifier fields of the read Data response are generated as follows:
• The TgtID is set to the same value as the SrcID of the Snoop response.
• The SrcID is a fixed value for the Home.
Note
In this example, the read data is being provided by the Home.
• The TxnID is set to the same value as the DBID of the Snoop response.
• The DBID field is a unique value generated by Home.
• The HomeNID is a fixed value for the Home.
7. The RN-F receives the read data and sends a completion acknowledge, CompAck, response.
The identifier fields of the CompAck are generated as follows:
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
127
```

## PDF page 128

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
• The TgtID is set to the same value as the HomeNID of the read data.
• The SrcID is a fixed value for the RN-F. This also matches the TgtID received.
• The TxnID is set to the same value as the DBID of the read data.
• The DBID field is not valid.
B2.5.4 DVMOp transaction
The use of TgtID, SrcID, TxnID, and DBID identifier fields for a DVMOp transaction is identical to those in the
B2.5.3.2 WriteNoSnp transaction.
B2.5.5 Transaction requests with Retry
For transactions that receive a RetryAck response, there are specific rules on how the identifier fields are used.
See B2.10 Request Retry, for more details on the Retry mechanism, and B2.5.6 Protocol Credit Return transaction
for rules about the return of unused credits.
Figure B2.33 shows the identifier value transfer.
Request
Requester
*
*
RetryAck
PCrdGrant
Completer
Request with Credit
(SrcID)
TxnID
TgtID R*
(TgtID)
SrcID
TxnID
PCrdType
DBID
(SrcID)
PCrdType
RTgtID
TxnID*
(TgtID)
SrcID
TxnID
TgtID
(SrcID)
TxnID
DBID
PCrdType *
(TgtID)
SrcID
TxnID
PCrdType
(TgtID)
SrcID
PCrdType
DBID
TxnID
(TgtID)
SrcID
PCrdType
DBID
TxnID
Figure B2.33: ID value transfer in a transaction request with retry
The required steps in the flow that Figure B2.33 shows are:
1. The Requester starts the transaction by sending a Request packet.
The identifier fields of the request are generated as follows:
• The TgtID is determined by the destination of the Request.
Note
The TgtID field can be remapped to a different value by the interconnect.
• The SrcID is a fixed value for the Requester.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
128
```

## PDF page 129

```text
Chapter B2. Transactions
B2.5. Transaction identifier field flows
• The Requester generates a unique TxnID field.
2. The Completer receives the Request packet and determines that a RetryAck response will be sent.
The identifier fields of the RetryAck response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Completer. This also matches the TgtID received.
• The TxnID is set to the same value as the TxnID of the request.
• The DBID field is not valid.
• The Completer uses a PCrdType value that indicates the type of credit required to retry the transaction.
3. When the Completer is able to accept the retried transaction of a given PCrdType, a credit to the Requester is
sent using the PCrdGrant response.
The identifier fields of the PCrdGrant response are generated as follows:
• The TgtID is set to the same value as the SrcID of the request.
• The SrcID is a fixed value for the Completer. This also matches the TgtID of the request.
• The TxnID field is not used and must be zero.
• The DBID field is not used and must be zero.
• The PCrdType value is set to the type required to issue the original transaction again.
4. The Requester receives the credit grant and reissues the original transaction by sending a Request packet.
The identifier fields of the request are generated as follows:
• The TgtID is set to either the same value as the SrcID of the RetryAck response, which is also the same
as the SrcID of the PCrdGrant response, or the value used in the original request.
• The SrcID is a fixed value for the Requester.
• The Requester generates a unique TxnID field. This is permitted, but not required, to be different from
the original request that received a RetryAck response.
• The PCrdType value is set to the PCrdType value in the RetryAck response to the original request,
which is also the same as the PCrdType of the PCrdGrant response.
B2.5.6 Protocol Credit Return transaction
A P-Credit Return transaction uses the PCrdReturn Request to return a granted, but no longer required, credit. The
TgtID, SrcID, and TxnID requirements are:
• The Requester sends the Protocol Credit Return transaction by sending a PCrdReturn Request packet. The
identifier fields of the request are generated as follows:
– The TgtID must match the SrcID of the credit that was obtained.
– The SrcID is a fixed value for the Requester.
– The TxnID field is not used and must be zero.
The PCrdType must match the value of the PCrdType in the original PCrdGrant that was required to issue the
original transaction again.
There is no response or use made of the DBID field associated with Protocol Credit Return transactions.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
129
```

## PDF page 130

```text
Chapter B2. Transactions
B2.6. Multi-request
B2.6 Multi-request
The Multi-request feature enables optimization of the Request channel bandwidth by permitting a single request to
target up to 64 cache lines. Subordinate Nodes that support newer memory technology with larger burst lengths
can benefit from knowing that more than 64-bytes of contiguous Data is being requested.
The reduction in Request channel bandwidth increases CHI C2C link efficiency as extra container granules can be
available for use by Data messages. See AMBA® CHI Chip-to-Chip (C2C) Architecture Specificationfor more
information.
Multiple 64-byte requests with the same attributes to a contiguous address region can be combined into a single
multi-request. A multi-request can be considered the same as a Requester issuing a series of requests with an
incrementing address.
The responses to a multi-request transaction remain constrained to a cache line. For example, a Read request
targeting 256 bytes, or 4 cache lines, will see four separate CompData, and RespSepData or DataSepResp
messages.
The Multi-request feature has no impact on the coherency granule, which remains at 64 bytes.
A multi-request transaction is permitted to be divided into any combination of smaller size multi-requests and
single requests at an intermediate point.
It is not expected, but is permitted, for a Home to combine a number of smaller requests into a larger multi-request
which is then sent on to the Subordinate. In this situation, the DMT or DWT flows cannot be used as the original
Requester will have used different TxnID field values for the smaller requests.
Support for the Multi-request feature is determined by the MultiReq_Support property. When Multi-request is
supported, the MultiReq, NumReq, and Size fields are used indicate the total amount of data associated with the
transaction. The CacheLineID field is used to indicate to which cache line a Response or Data message relates to
within a multi-request transaction flow.
The following CHI transactions are permitted to use the Multi-request feature:
• Non-coherent transactions:
– ReadNoSnp
– ReadNoSnpSep
– WriteNoSnpFull
– WriteNoSnpPtl
– WriteNoSnpZero
• IO coherent transactions:
– ReadOnce
– ReadOnceCleanInvalid
– ReadOnceMakeInvalid
– WriteUniqueFull
– WriteUniquePtl
– WriteUniqueZero
The start address for a multi-request transaction is required to be aligned to a cache line boundary. The transaction
must not cross a 4KB boundary.
Additional total size and boundary constraints may apply depending on the value of BROADCASTMULTIREQ
or alternative control registers.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
130
```

## PDF page 131

```text
Chapter B2. Transactions
B2.6. Multi-request
Exclusive transactions are not permitted to use the Multi-request feature.
B2.6.1 Examples of multi-request
This section provides some non-exhaustive examples to show the potential use of the Multi-request feature across
the DMT, DCT, and DWT flows.
B2.6.1.1 DMT
Figure B2.34 shows how the Multi-request feature can be used as part of a DMT transaction flow.
Requester
Requester
Snoopee
Snoopee
Home
Home
Subordinate
Subordinate
ReadOnce
NumReq = 0x3 (4 cache lines)
Addr = 0x0
TxnID=0x0
ReadNoSnp
NumReq = 0x3 (4 cache lines)
Addr = 0x0
ReturnTxnID=0x0
TxnID=0x8
ReadReceipt
CacheLineID=0x0
TxnID = 0x8
CompData_UC
CacheLineID=0x0
TxnID = 0x0
ReadReceipt
CacheLineID=0x1
TxnID = 0x8
CompData_UC
CacheLineID=0x1
TxnID = 0x0
ReadReceipt
CacheLineID=0x2
TxnID = 0x8
CompData_UC
CacheLineID=0x2
TxnID = 0x0
ReadReceipt
CacheLineID=0x3
TxnID = 0x8
CompData_UC
CacheLineID=0x3
TxnID = 0x0
Figure B2.34: ReadOnce targeting 4 cache lines using DMT flow
B2.6.1.2 DCT
Figure B2.35 shows how the Multi-request feature can be used as part of a DCT transaction flow.
The Snoop channel does not support the Multi-request feature. However, a DCT flow can still be used in
multi-request scenarios, when the Snoopee MultiReq_Support property is set to True or CacheLineID_Accurate.
A Snoopee with either True or CacheLineID_Accurate MultiReq_Support property values is required to drive the
correct CacheLineID value for responses it generates. This ensures that the Home and Requester can correctly
identify each cache line within the multi-request transaction.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
131
```

## PDF page 132

```text
Chapter B2. Transactions
B2.6. Multi-request
Requester
Requester
Snoopee
Snoopee
Home
Home
Subordinate
Subordinate
ReadOnce
NumReq = 0x3 (4 cache lines)
Addr = 0x0
TxnID=0x0
SnpOnceFwd
Addr = 0x00
FwdTxnID = 0x0
TxnID = 0x8
CompData_I
CacheLineID = 0x0
TxnID = 0x0
SnpResp_SC_Fwded_I
TxnID = 0x8
SnpOnceFwd
Addr = 0x40
FwdTxnID = 0x0
TxnID = 0xA
CompData_I
CacheLineID = 0x1
TxnID = 0x0
SnpResp_SC_Fwded_I
TxnID = 0xA
SnpOnceFwd
Addr = 0x80
FwdTxnID = 0x0
TxnID = 0xD
CompData_I
CacheLineID = 0x2
TxnID = 0x0
SnpResp_SC_Fwded_I
TxnID = 0xD
SnpOnceFwd
Addr = 0xC0
FwdTxnID = 0x0
TxnID = 0x7
CompData_I
CacheLineID = 0x3
TxnID = 0x0
SnpResp_SC_Fwded_I
TxnID = 0x7
Figure B2.35: ReadOnce targeting 4 cache lines using DCT flow
B2.6.1.3 DMT and DCT
Figure B2.36 shows how the Multi-request feature can be used with a combination of DMT and DCT transaction
flows.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
132
```

## PDF page 133

```text
Chapter B2. Transactions
B2.6. Multi-request
Requester
Requester
Snoopee
Snoopee
Home
Home
Subordinate
Subordinate
ReadOnce
NumReq = 0x3 (4 cache lines)
Addr = 0x0
TxnID=0x0
ReadNoSnp
NumReq = 0x1 (2 cache lines)
Addr = 0x0
ReturnTxnID=0x0
TxnID=0x8
ReadReceipt
TxnID = 0x8
CacheLineID=0x0
CompData_UC
TxnID = 0x0
CacheLineID=0x0
ReadReceipt
TxnID = 0x8
CacheLineID=0x1
CompData_UC
TxnID = 0x0
CacheLineID=0x1
SnpOnceFwd
Addr = 0x80
FwdTxnID = 0x0
TxnID = 0xD
CompData_I
TxnID = 0x0
CacheLineID = 0x2
SnpResp_SC_Fwded_I
TxnID = 0xD
SnpOnceFwd
Addr = 0xC0
FwdTxnID = 0x0
TxnID = 0x7
CompData_I
TxnID = 0x0
CacheLineID = 0x3
SnpResp_SC_Fwded_I
TxnID = 0x7
Figure B2.36: ReadOnce targeting 4 cache lines using DMT and DCT flows
B2.6.1.4 DWT
Figure B2.37 shows how the Multi-request feature can be used as part of a DWT transaction flow.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
133
```

## PDF page 134

```text
Chapter B2. Transactions
B2.6. Multi-request
Requester
Requester
Snoopee
Snoopee
Home
Home
Subordinate
Subordinate
WriteNoSnpFull
NumReq = 0x3 (4 cache lines)
Addr = 0x0
TxnID=0x0
WriteNoSnpFull
NumReq = 0x3 (4 cache lines)
Addr = 0x0
ReturnTxnID=0x0
TxnID=0x8
DBIDResp
CacheLineID=0
TxnID = 0x0
DBID = 0xAA
NonCopyBackWriteData
TxnID = 0xAA
Comp
CacheLineID=0
TxnID = 0x8
Comp
CacheLineID=0
TxnID = 0x0
DBIDResp
CacheLineID=1
TxnID = 0x0
DBID = 0xBB
NonCopyBackWriteData
TxnID = 0xBB
Comp
CacheLineID=1
TxnID = 0x8
Comp
CacheLineID=1
TxnID = 0x0
DBIDResp
CacheLineID=2
TxnID = 0x0
DBID = 0xCC
NonCopyBackWriteData
TxnID = 0xCC
Comp
CacheLineID=2
TxnID = 0x8
Comp
CacheLineID=2
TxnID = 0x0
DBIDResp
CacheLineID=3
TxnID = 0x0
DBID = 0xDD
NonCopyBackWriteData
TxnID = 0xDD
Comp
CacheLineID=3
TxnID = 0x8
Comp
CacheLineID=3
TxnID = 0x0
Figure B2.37: WriteNoSnpFull targeting 4 cache lines using DWT flow
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
134
```

## PDF page 135

```text
Chapter B2. Transactions
B2.7. Ordering
B2.7 Ordering
This section describes the mechanisms that the protocol includes to support system ordering requirements. It
contains the following sections:
• B2.7.1 Multi-copy atomicity
• B2.7.2 Completion response and ordering
• B2.7.3 Completion acknowledgment
• B2.7.4 Ordering semantics of RespSepData and DataSepResp
• B2.7.5 Transaction ordering
For the meaning of the terms EW A, Device, and Cacheable, see B2.8.3Memory Attributes.
B2.7.1 Multi-copy atomicity
The memory model used in this specification requires multi-copy atomicity. All compliant components must
ensure that all write requests are multi-copy atomic. A write is defined as multi-copy atomic if both of the
following conditions are true:
• All writes to the same location are serialized, therefore observed in the same order by all Requesters. Some
Requesters could not observe all of the writes.
• A read of a location does not return the value of a write until all Requesters observe that write.
In this specification, two addresses are considered to be the same with respect to coherence, observability, and
hazarding if their cache line addresses and Physical Address Space (PAS) attributes are the same.
B2.7.2 Completion response and ordering
Table B2.7 shows the various transaction responses and any ordering guarantees they provide with respect to later
transactions, either from the same agent or from another agent.
Table B2.7: Completion response and ordering
Transaction Location Response Outcome
Read Cacheable CompData
DataSepResp
RespSepData_UC
RespSepData_SC
RespSepData_UD_PD
RespSepData_SD_PD
The transaction is observable to a later transaction
from any agent to the same location.
Cacheable RespSepData_I No earlier transaction will send a snoop to this
Requester. All later transactions send a snoop only
if required after the Home receives the CompAck
response for this transaction.
Non-cacheable or
Device
RespSepData
CompData
The transaction is observable to a later transaction
from any agent to the same endpoint address
range.
Write or Atomic Cacheable Comp
CompData
The transaction is observable to a later transaction
from any agent to the same location.
Non-cacheable or
Device
Comp
CompData
The transaction is observable to a later transaction
from any agent to the same endpoint range.
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
135
```

## PDF page 136

```text
Chapter B2. Transactions
B2.7. Ordering
Table B2.7 – Continued from previous page
Transaction Location Response Outcome
Dataless except for
StashOnceSep,
CleanInvalidPoPA, and
CleanInvalidStorage
Comp The transaction is observable to a later transaction
from any agent to the same memory location.
CleanSharedPersist Comp Any data written earlier to the same memory
location is made persistent.
CleanInvalidPoPA Comp The transaction is observable to a later transaction
from any agent to the same memory location in
any PAS. Additional Cache Maintenance
Operations could be required in the other Physical
Address Spaces to ensure any data written earlier
is fully visible to those Physical Address Spaces.
CleanInvalidStorage Comp The data written earlier is now at the furthest point
in the memory hierarchy away from a PE or other
observer to which a write transaction could
propagate, that is, memory.
Combined Write CompCMO
(non-PoPA and
Non-storage CMO)
CMO, PCMO, and write operations are observable
to a later transaction from any agent to the same
memory location.
CompCMO (PoPA
CMO)
CMO and write operations are observable to a
later transaction from any agent to the same
memory location in any PAS. Additional Cache
Maintenance Operations could be required in the
other Physical Address Spaces to ensure that any
data written earlier is fully visible to those
Physical Address Spaces.
CompCMO (Storage
CMO)
CMO and write operations are now at the furthest
point in the memory hierarchy away from a PE or
other observer to which a write transaction could
propagate, that is, memory.
Comp See outcome of Comp for Write transaction within
this table.
CleanSharedPersistSep Persist The data written earlier to the same memory
location is made persistent.
Combined Write with
PCMO
Persist The data write in the Combined Write is made
persistent. All earlier writes on the same line are
also made persistent.
StashOnceSep Comp The Completer accepts the request and does not
send a RetryAck response.
StashDone The transaction is observable to a later transaction
from any agent to the same memory location.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
136
```

## PDF page 137

```text
Chapter B2. Transactions
B2.7. Ordering
Note
The size of the endpoint address range is IMPLEMENTATION DEFINED . Typically, this is:
• The size of a peripheral device, for a region used for peripherals.
• The size of a cache line, for a region used for memory.
A Cacheable location can be determined by the MemAttr[2] Cacheable bit = 1 in the request. A
Non-cacheable or Device location can be determined by the MemAttr[2] Cacheable bit = 0 in the request.
In a combined Ordered Write Observation (OWO) Write request, if the write is canceled and the Requester sends a
WriteDataCancel, the required cache maintenance on the write data is not carried out. The Requester must resend
both the Write request and the CMO:
• If a Write with PCMO had its write canceled:
– The Persist response for the combined request does not indicate that the write data is made persistent.
– The Requester must resend the PCMO either combined with the re-sent Write request or after the re-sent
Write request succeeds.
• If a Write with CMO had its write canceled:
– The Requester must resend the CMO, either combined with the re-sent Write request or after the re-sent
Write request succeeds.
A component must only give a Comp or CompDBIDResp response when all observers are guaranteed see the
result of the atomic operation.
A Comp response in a canceled write only implies that the transaction loop is completed and makes no statement
regarding the completion of coherency action initiated by the write. Therefore, the Completer is permitted to send
a Comp as soon as receiving a WriteDataCancel response without dependency on either the processing of the write
request or the completion of any snoops sent due to the write.
B2.7.3 Completion acknowledgment
The relative ordering of transactions issued by a Requester, and Snoop transactions caused by transactions from
different Requesters, is controlled by the use of a completion acknowledge, CompAck, response. This ensures that
a Snoop transaction that is ordered after the transaction from the Requester is guaranteed to be received after the
transaction response.
The sequencing of the completion of a Read transaction and the sending of CompAck is as follows:
1. An RN-F sends a CompAck after receiving Comp, RespSepData, or CompData, or both RespSepData and
DataSepResp.
2. An HN-F, except in the case of ReadNoSnp and ReadOnce*, waits for CompAck before sending a
subsequent snoop to the same address. For CopyBack transactions, WriteData acts as an implicit CompAck
and an HN-F must wait for WriteData before sending a snoop to the same address.
This sequence guarantees that an RN-F receives completion for a transaction and a snoop to the same cache line in
the same order as they are sent from an HN-F. This ensures transactions to the same cache line are observed in the
correct order.
When an RN-F has a transaction in progress that uses CompAck, except for ReadNoSnp and ReadOnce*, a Snoop
request is guaranteed to not be received to the same address between the point that Comp is received and the point
that CompAck is sent.
For WriteNoSnp, WriteUnique, and their Combined Write variants, that require a CompAck message, a Request
Node sends the CompAck after receiving the Comp, DBIDResp, or CompDBIDResp response.
The use of CompAck for a transaction is determined by the Requester setting the ExpCompAck field in the
original request. The rules for a Request Node setting the ExpCompAck field and generating a CompAck response
are as follows:
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
137
```

## PDF page 138

```text
Chapter B2. Transactions
B2.7. Ordering
• An RN-F must include a CompAck response in all Read transactions except ReadNoSnp and ReadOnce*.
• An RN-F is permitted, but not required, to include a CompAck response in ReadNoSnp and ReadOnce*
transactions.
• An RN-F must not include a CompAck response in StashOnce*, CMO, Atomic, or Evict transactions.
• An RN-I or RN-D is permitted, but not required, to include a CompAck response in Read transactions.
• An RN-I or RN-D must not include a CompAck response in Dataless or Atomic transactions.
• A Request Node that wants to make use of DMT must include a CompAck response in ordered ReadNoSnp
and ReadOnce* transactions.
• For Write transactions, CompAck can only be used for:
– WriteUnique, WriteNoSnp, and their Combined Write variants, when they require OWO guarantees.
See B2.7.5.3 Streaming Ordered Write transactions.
– CopyBack write transactions where Home has provided a Comp response, indicating that the Requester
must not send CopyBackWriteData. When Home provides a Comp response, a CompAck must be sent
by the Requester regardless of the original ExpCompAck value. See B2.3.2.3 CopyBack Write.
For transactions between a Request Node and a Home Node, where the Home Node is the Completer, the Home
Node must support the use of CompAck for all transactions that are required or permitted to use CompAck.
A Subordinate Node is not required to support the use of CompAck.
A Requester, such as an HN-F or HN-I that communicates with an SN-F or SN-I respectively, must not send a
CompAck response.
Table B2.8 shows the Request types that require a CompAck response, and the corresponding Requester types that
are required to provide that response. The following key is used:
Y Yes, required
N No, not required
H Dependent on transaction flow chosen by Home in response to the CopyBack Write request
O Optional
- Not applicable
Table B2.8: Requester CompAck requirement
Request type CompAck required
RN-F RN-D, RN-I
ReadNoSnp O O
ReadOnce* O O
ReadClean Y -
ReadNotSharedDirty Y -
ReadShared Y -
ReadUnique Y -
ReadPreferUnique Y -
MakeReadUnique Y -
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
138
```

## PDF page 139

```text
Chapter B2. Transactions
B2.7. Ordering
Table B2.8 – Continued from previous page
Request type CompAck required
RN-F RN-D, RN-I
CleanUnique Y -
MakeUnique Y -
CleanShared N N
CleanSharedPersist* N N
CleanInvalid N N
CleanInvalidPoPA N N
CleanInvalidStorage N N
MakeInvalid N N
WriteBack H -
WriteCleanFull H -
WriteUnique O O
WriteUniqueZero N N
Evict N -
WriteEvictFull H -
WriteEvictOrEvict H -
WriteNoSnp O O
WriteNoSnpDef N N
WriteNoSnpZero N N
Atomic* N N
StashOnce* N N
In a Combined Write transaction, the CompAck requirement is the same as the CompAck requirement for the type
of Write in the Combined Write transaction.
B2.7.4 Ordering semantics of RespSepData and DataSepResp
When a Requester receives the first DataSepResp, the Read transaction can be considered to be globally observed.
This is because there is no action which can modify the read data received.
When a Requester receives a RespSepData response from Home, the relevant request has been ordered at Home.
The Requester does not receive any snoops to the same location for transactions that are scheduled before the
RespSepData response. Before sending RespSepData response to the Requester, the Home must ensure that no
Snoop transactions are outstanding to that Requester to the same address.
When a Requester receives:
• RespSepData with a Resp field value of Invalid, the Read transaction cannot be considered to be globally
observed. That is, RespSepData_I does not guarantee that Home has completed snooping of other agents in
the system.
• RespSepData with any legal Resp field value other than Invalid, the Read transaction can be considered to be
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
139
```

## PDF page 140

```text
Chapter B2. Transactions
B2.7. Ordering
globally observed.
When the Requester gives a completion acknowledge, CompAck, response, it is required to hazard snoops for any
transaction that is scheduled after the CompAck response. The following rules apply:
• For all transactions, except as described immediately below, the CompAck must be sent after the
RespSepData response is received. It is permitted, but not required, to wait for the DataSepResp response
before the CompAck is given.
• For ReadOnce and ReadNoSnp transactions with an ordering requirement, that is, Order field is set to 0b10
or 0b11 and the ExpCompAck field is 1, it is required that the CompAck is given only after both
DataSepResp and RespSepData responses are received.
Note
It is required that CompAck must not be given when only DataSepResp is received.
B2.7.5 Transaction ordering
In addition to using a Comp response to order a sequence of requests from a Requester, this specification also
defines mechanisms for ordering of requests between a Request Node, Home Node pair and an HN-I, SN-I pair.
Between an HN-F, SN-F pair and HN-I, SN-I pair, the order field is used to obtain a Request Accepted
acknowledgment.
Requester Order between an RN, HN pair and an HN-I, SN-I pair is supported by the Order field in a request. The
Order field indicates that the transaction requires one of the following forms of ordering:
Request Order This guarantees the order of multiple transactions, from the same agent, to
the same address location.
Endpoint Order This guarantees the order of multiple transactions, from the same agent, to
the same endpoint address range.
Ordered Write Observation, OWO This guarantees the observation order by other agents in the system, for a
sequence of Write transactions from a single agent.
Request Accepted This guarantees that the Completer sends a positive acknowledgment only
when accepting the Read request.
Table B2.9 shows the Order field encodings.
The following key is used:
- Not applicable.
Table B2.9: Order value encodings
Order[1:0] Description Permitted between Permitted for
Multi-request
0b00 No ordering required All Yes
0b01 Request accepted HN-F to SN-F, and HN-I to SN-I Yes
Reserved RN to HN -
0b10 Request Order or OWO RN to HN a Yes
Request Order HN-I to SN-I Yes
Reserved HN-F to SN-F -
Continued on next page
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
140
```

## PDF page 141

```text
Chapter B2. Transactions
B2.7. Ordering
Table B2.9 – Continued from previous page
Order[1:0] Description Permitted between Permitted for
Multi-request
0b11 Endpoint Order RN to HN, and HN-I to SN-I -
Reserved HN-F to SN-F -
a Request Order when ExpCompAck = 0. OWO when ExpCompAck = 1.
For any multi-request that uses a non-zero value of Order, the hazarding guarantees are the same as though the
multi-request transaction was issued using separate 64-byte cache line-aligned requests.
Note
It is permitted to over-address hazard to assist with logic complexity. A non-exhaustive list of how this could
be implemented includes hazarding at:
• Twice the overall transaction size, to assist with any address un-alignment compared to the natural
multi-request boundary.
• A granular 64-byte level up to a certain multi-request size and then a full 4-KB range afterwards.
• A full 4-KB range for any multi-request.
A sequence of transactions that rely on the Order field for same agent ordering must use the same REQ channel RP.
For more information on Resource Planes, see B14.2.1.2 Flow control with Resource Planes.
B2.7.5.1 Ordering requirements
A Requester that changes the ordering requirements of a transaction to a stronger ordering requirement, is required
to be consistent in changing the ordering requirement of Request Order to Endpoint Order on all its transactions.
The Order field must only be set to a non-0 value for the following transactions:
• ReadNoSnp
• ReadNoSnpSep
• ReadOnce*
• WriteNoSnp
• WriteNoSnpDef
• WriteNoSnp*CMO
• WriteNoSnpZero
• WriteUnique
• WriteUnique*CMO
• WriteUniqueZero
• Atomic*
When a ReadNoSnp or ReadOnce* transaction requires Request Order or Endpoint Order:
• The Requester requires a ReadReceipt to determine when it can send the next ordered request.
• At the Completer a ReadReceipt means the request has reached the next ordering point that maintains
requests in the order they were received:
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
141
```

## PDF page 142

```text
Chapter B2. Transactions
B2.7. Ordering
– Requests that require Request Order maintain order between requests to the same address from the same
source.
– Requests that require Endpoint Order maintain order between requests to the same endpoint address
range from the same source.
• A Completer that is capable of sending separate Non-data and Data-only responses can send RespSepData
response instead of ReadReceipt and achieve the same functional behavior.
When a WriteNoSnp, WriteNoSnpDef, WriteNoSnpZero, or a Non-snoopable Atomic transaction requires
Request Order or Endpoint Order:
• The Requester requires a DBIDResp or DBIDRespOrd to determine when sending the next ordered request.
• The Completer sending a DBIDResp or DBIDRespOrd response means that a data buffer is available, and
that the Write request has reached a PoS that maintains requests in the order they were received:
– For requests that require Request Order, the Completer maintains order between requests to the same
address from the same source.
– For requests that require Endpoint Order, the Completer maintains order between requests to the same
endpoint address range from the same source.
When a WriteUnique transaction without ExpCompAck = 1, or a WriteUniqueZero or a Snoopable Atomic
transaction requires Request Order:
• The Requester requires a DBIDResp or DBIDRespOrd to determine when sending the next ordered request.
• The Completer sending a DBIDResp or DBIDRespOrd response means that maintains order between
requests to the same address from the same source.
Additionally, when a Completer sends DBIDRespOrd for a request with a no order or Request Order requirement,
the Completer guarantees to order all subsequent no order or Request Order received requests to the same address
from the same source against this request, where these later received requests are of any transaction type, not
necessarily Write transactions. When the write includes a CMO, the order is guaranteed against both the write and
the CMO.
When a WriteUnique, WriteNoSnp, or one of their Combined Write variants requires OWO:
• CompAck is required. The Request Node has ExpCompAck = 1.
• The Request Node requires a DBIDResp or DBIDRespOrd.
• The Completer is a PoS. A PoS sending DBIDResp or DBIDRespOrd means:
– A data buffer is available.
– The PoS guarantees that the completion of the coherence action on this write does not depend on
completion of the coherence action on a subsequent write that requires OWO.
– The write is not made visible until CompAck is received.
All architectural mechanisms applicable to increasing streaming efficiency and corresponding constraints are
defined in B2.7.5.3 Streaming Ordered Write transactions.
When a ReadNoSnp or ReadNoSnpSep has the Order field set to 0b01, a ReadReceipt response from the
Completer guarantees that the Completer has accepted the request and does not send a RetryAck response.
B2.7.5.1.1 Read Request order example
Figure B2.38 shows the request ordering of three Read requests.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
142
```

## PDF page 143

```text
Chapter B2. Transactions
B2.7. Ordering
HNRN
ReadNoSnp-1
ReadReceipt-1
ReadNoSnp-2
RetryAck-2
PCrdGrant
ReadNoSnp-2
ReadReceipt-2
ReadNoSnp-3
ReadNoSnp-2 waits 
for a CreditGrant
Request 
accepted
Request gets  
a Retry 
response
ReadNoSnp-2 is sent 
after ReadReceipt-1
is received
ReadReceipt-3
ReadNoSnp-3 
continues waiting 
for ReadNoSnp-2 to 
make progress
ReadNoSnp-3 is sent 
after Read Receipt-2
is received
Figure B2.38: Series of ordered Read requests
Three ordered requests are sent from Request Node to Home Node in Figure B2.38 as follows:
1. The Request Node sends the ReadNoSnp-1 request to the Home Node.
2. The Home Node accepts the request and returns the ReadReceipt-1 response to the Request Node.
3. After the ReadReceipt-1 response is received, the Request Node sends the ReadNoSnp-2 request to the
Home Node.
4. The Home Node cannot immediately accept the ReadNoSnp-2 request and returns the RetryAck-2 response
to the Request Node.
5. The Request Node must now wait for a PCrdGrant to be sent from the Home Node before resending the
ReadNoSnp-2 request. The Request Node does not send ReadNoSnp-3 at this point, to order ReadNoSnp-3
behind ReadNoSnp-2. This ordering requires that ReadNoSnp-2 must be accepted at the Home Node before
ReadNoSnp-3 is sent to the Home Node.
6. After receipt of an appropriate PCrdGrant, the Request Node resends the ReadNoSnp-2 request.
7. The Home Node accepts the request and returns a ReadReceipt-2 response to the Request Node.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
143
```

## PDF page 144

```text
Chapter B2. Transactions
B2.7. Ordering
8. After receipt of the ReadReceipt-2 response, the Request Node sends the ReadNoSnp-3 request to the Home
Node.
9. The Home Node accepts the request and returns the ReadReceipt-3 response to the Request Node.
10. Each of the read transactions is completed with the Requester receiving a completion and data. This is not
shown in Figure B2.38.
Note
Figure B2.38 shows a single ordered stream of three reads from the Request Node. However, a Request
Node can have multiple streams of reads, so requests must be ordered within a stream. However, ordering
dependency does not exist between streams. For example, when the streams are from different threads
within the Request Node. In this case, the Request Node waits for the ReadReceipt of the previous request
from the same thread only before sending out the next ordered request from that stream.
B2.7.5.2 CopyBack Request order
An RN-F must wait for the CompDBIDResp or Comp response to be received for an outstanding CopyBack
transaction before issuing another request to the same cache line.
• It is permitted for an Atomic transaction with SnoopMe = 1 to be issued before the CompDBIDResp or
Comp response is received for an outstanding CopyBack to the same cache line.
• It is permitted for a CopyBack transaction to be issued before the CompDBIDResp or Comp response is
received for an outstanding Atomic transaction, with SnoopMe = 1, to the same cache line.
B2.7.5.3 Streaming Ordered Write transactions
The architectural mechanisms applicable to increasing Ordered Write Observation (OWO) Write streaming
efficiency, and the corresponding constraints, are applicable to WriteUnique and WriteNoSnp transactions only.
If a Requester requires a sequence of Write transactions to be observed in the same order as they are issued, the
Requester can wait for completion for a write before issuing the next write in the sequence. Such an observation
ordering is typically termed OWO. This specification provides a mechanism termed Streaming Ordered Writes to
more efficiently stream such ordered Write transactions.
The Streaming Ordered Write mechanism relies on the use of the OWO ordering requirement and CompAck.
When utilizing the Streaming Ordered Write solution, the following requirements apply to the Requesters and
HN-F:
• The Requester must set the Order field to 0b10 and set ExpCompAck on the Write request.
• The OWO requirement in a Write request indicates to the HN-F that the completion of coherence action on
this write must not depend on completion of coherence action on a subsequent write.
• The Requester must wait for DBIDResp, DBIDRespOrd, CompDBIDResp, or Comp for a Write transaction
before sending the next Write request.
• The Requester must send a CompAck response after receiving DBIDResp, DBIDRespOrd, CompDBIDResp,
or Comp responses for the corresponding writes and Comp or CompDBIDResp responses for all earlier
related ordered writes. If write data is to be sent, the Requester is permitted, but not required, to combine the
CompAck response with the WriteData response into a NonCopyBackWriteDataCompAck response. When
the Requester uses the combined CompAck and WriteData response for a transaction, a combined response
must be sent for all WriteData transfers in that transaction. The method by which a Requester determines if a
group of ordered writes are related is IMPLEMENTATION SPECIFIC .
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
144
```

## PDF page 145

```text
Chapter B2. Transactions
B2.7. Ordering
Note
Waiting to send CompAck response until all previously related ordered writes have received their Comp
responses ensures the operations at their respective HN-F nodes have completed. Any Requester observing
the write associated with the CompAck response also observes all prior, related ordered writes.
• The Requester that receives DBIDResp* and is ready to send CompAck must not wait for Comp to send
CompAck.
• HN-F must wait for a CompAck response from the Request Node before deallocating a Write transaction and
making the write visible to other observers.
B2.7.5.3.1 Optimized Streaming Ordered Write transactions
The writes in this section refer to WriteUnique or WriteNoSnp only. The Streaming Ordered Writes mechanism
can be further optimized. If a previously sent write is to a different target, the Requester does not need to wait for
the DBIDResp* for the request before sending the next ordered write. However, if the interconnect can remap the
TgtID, the Requester must presume that all Write transactions are targeting the same HN-F and must not use the
optimized version of the Streaming Ordered Writes flow.
An implementation using an optimized or non-optimized Streaming Ordered Writes solution must avoid deadlock
and livelock situations.
Note
A technique for avoiding resource-related deadlock or livelock issues is to limit Streaming Ordered Writes
optimization to one Requester in the system. All other Requesters in the system can use the Streaming
Ordered Writes solution without the optimization.
In a typical system, the optimized Streaming Ordered Writes solution is most beneficial to an RN-I that is a
conduit for PCIe style, non-relaxed order, Snoopable writes. In most systems, one RN-I hosting this type of
PCIe traffic is adequate.
OWO Writes can be used by more than one Requester by making use of WriteDataCancel messages to avoid
resource related deadlocks and livelocks.
Figure B2.39 shows a typical transaction flow in which an RN-I uses Streaming Ordered WriteUnique transactions.
This flow prevents a read acquiring the new value of Write-B before Write-A has completed.
Note
For clarity, the Write-B DBIDResp* and the NonCopyBackWriteData flow is omitted from Figure B2.39.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
145
```

## PDF page 146

```text
Chapter B2. Transactions
B2.7. Ordering
RN-IHN-FRN-F1
WriteUnique-A
DBIDResp-A
CompAck-A
RN-F2
SnpResp_I-A 
SnpCleanInvalid-A
Comp-A
III
NCBWrData-A
WriteUnique-B
SnpCleanInvalid-A
SnpResp_I-A 
SnpCleanInvalid-B
SnpResp_I-B SnpCleanInvalid-B
SnpResp_I-B 
Comp-B
CompAck-B
CompAck for B is 
not sent until the 
Comp for A is 
received
Request B is sent 
after receiving 
DBIDResp for 
request A
NCBWrData = NonCopyBackWriteData
Figure B2.39: Streaming Ordered WriteUnique transactions flow
The Streaming Ordered WriteUnique transaction flow is as follows:
1. RN-I issues WriteUnique-A to the Home.
2. The Home responds with DBIDResp and issues SnpCleanInvalid-A to RN-F1 and RN-F2.
3. RN-I sends the write data associated with WriteUnique-A and issues the next ordered WriteUnique request
to the Home, shown in Figure B2.39 as WriteUnique-B.
4. WriteUnique-A and WriteUnique-B are to different addresses. The Home sends out SnpCleanInvalid-B
snoops to RN-F1 and RN-F2 for WriteUnique-B without waiting for responses for WriteUnique-A
transaction snoops.
5. The Snoop responses for the WriteUnique-B transaction are received by the Home before the Snoop
responses for the WriteUnique-A transaction are received. Home sends Comp to RN-I for the
WriteUnique-B transaction.
6. The Home waits for Snoop responses for the WriteUnique-A transaction to be received. Once received, the
Home can send Comp to RN-I for the WriteUnique-A transaction.
7. The Requester, RN-I, receives Comp-B and waits to receive Comp-A before proceeding with the next
response.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
146
```

## PDF page 147

```text
Chapter B2. Transactions
B2.7. Ordering
8. The RN-I sends a CompAck response for the WriteUnique-A transaction when it is ready to make the write
observable.
9. The RN-I sends a CompAck response for the WriteUnique-B transaction when it is ready to make the write
observable.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
147
```

## PDF page 148

```text
Chapter B2. Transactions
B2.8. Address, Control, and Data
B2.8 Address, Control, and Data
A transaction includes attributes defining the manner in which the transaction is handled by the interconnect.
These include the address, memory attributes, snoop attributes, and data formatting. Each attribute is defined in
this section.
In this section, unless explicitly stated otherwise, a reference to a Write transaction includes both the individual
Write transaction and the corresponding Combined Write transaction.
B2.8.1 Address
The CHI protocol supports:
• Physical Address (PA) of 44 bits to 52 bits, in 1 bit increments.
• Virtual Address (V A) of 49 bits to 53 bits.
The REQ and SNP packet Addr fields are specified as follows:
• REQ channel: Address[(MPA-1):0]
• SNP channel: Address[(MPA-1):3]
MPA is the Maximum PA supported.
Table B2.10 shows the relationship between the physical address field width and the supported virtual address.
Table B2.10: Addr field width and supported Physical Address and Virtual Address size
REQ Addr field width (bits) Maximum supported (bits)
Physical Address Virtual Address
44 44 49
45 45 51
46 to 52 46 to 52 53
See B8.3 DVMOp field value restrictionsfor DVM payload mapping in the REQ and SNP fields with different
Addr field widths.
The Req_Addr_Width parameter is used to specify the maximum PA in bits that is supported by a component.
Valid values for this parameter are 44 to 52, when not specified, the parameter takes the default value of 44.
B2.8.2 Physical Address Space, PAS
The Physical Address Space (PAS) of an access is determined using the PAS field value.
See B13.10.68 PAS for more information.
For Snoopable transactions, the PAS can be considered additional address information that defines multiple
address spaces. Any aliasing between the different Physical Address Spaces must be handled correctly.
Note
Hardware coherency does not manage coherency between the various address spaces. See B2.7.1 Multi-copy
atomicity.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
148
```

## PDF page 149

```text
Chapter B2. Transactions
B2.8. Address, Control, and Data
B2.8.3 Memory Attributes
The Memory Attributes (MemAttr) consist of Early Write Acknowledgment (EW A), Device, Cacheable, and
Allocate.
B2.8.3.1 EWA
EW A indicates whether the Write completion response for a transaction:
• Can come from an intermediate point in the interconnect, such as a Home Node.
• Must come from the final endpoint at the target destination.
When EW A is 1, the Write completion response for the transaction can come from an intermediate point or from
the endpoint. A completion that comes from an intermediate point must provide the same guarantees required by a
Comp as described in B2.7.2 Completion response and ordering.
When EW A is 0, the write completion response for the transaction must come from the endpoint.
Note
It is permitted, but not required, for an implementation not to use the EW A attribute. In this instance,
completion must be given from the endpoint.
The requirements for EW A are:
• Can take any value in:
– WriteNoSnpDef.
Note
For a WriteNoSnpDef transaction, it is expected that the response comes from the final target
endpoint, regardless of EW A value.
An early response from an intermediate component can stop the original Requester observing a
valid Defer response from the final endpoint, reducing the effectiveness of the deferrable write
transaction.
– WriteNoSnp.
– ReadNoSnp.
– ReadNoSnpSep.
– Atomic* transactions.
• Must be 1 in any:
– Read transaction that is not a ReadNoSnp or ReadNoSnpSep.
– Dataless transaction.
– Write transaction that is not a WriteNoSnp or WriteNoSnpDef.
• Is inapplicable and must be 0 in any:
– DVMOp.
– PCrdReturn.
– PrefetchTgt.
B2.8.3.2 Device
Device attribute indicates if the memory type is either Device or Normal.
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
149
```

## PDF page 150

```text
Chapter B2. Transactions
B2.8. Address, Control, and Data
B2.8.3.2.1 Device memory type
Device memory type must be used for locations that exhibit side-effects. Use of Device memory type for locations
that do not exhibit side-effects is permitted.
The requirements for a transaction to a Device type memory location are:
• A Read transaction must not read more data than requested.
• Prefetching from a Device memory location is not permitted.
• A read must get its data from the endpoint. A read must not be forwarded data from a write to the same
address location that completed at an intermediate point.
• Combining requests to different locations into one request, or combining different requests to the same
location into one request, is not permitted.
• Writes must not be merged.
• Writes to Device memory that obtain completion from an intermediate point must make the write data visible
to the endpoint in a timely manner.
Accesses to Device memory must use the following types, exclusive variants are permitted:
• Read accesses to a Device memory location must use ReadNoSnp.
• Write accesses to a Device memory location must use WriteNoSnpPtl, WriteNoSnpFull, WriteNoSnpZero,
or WriteNoSnpDef.
• Atomic* transactions are permitted to Device memory locations.
• The PrefetchTgt transaction is not permitted to Device memory locations. The MemAttr field is inapplicable
and must be 0 in the PrefetchTgt transaction.
CMO transactions are not permitted to Device memory.
B2.8.3.2.2 Normal memory type
Normal memory type is appropriate for memory locations that do not exhibit side-effects.
Accesses to Normal memory do not have the same restrictions regarding prefetching or forwarding as Device type
memory:
• A Read transaction that has EW A = 1 can obtain read data from a Write transaction that has sent its
completion from an intermediate point and is to the same address location.
• Writes can be merged.
Any Read, Dataless, Write, PrefetchTgt, or Atomic transaction type can be used to access a Normal memory
location. The transaction type used is determined by the memory operation to be accomplished, and the Snoopable
attributes.
B2.8.3.3 Cacheable
The Cacheable attribute indicates if a transaction must perform a cache lookup:
• When Cacheable is 1, the transaction must perform a cache lookup.
• When Cacheable is 0, the transaction must access the final destination.
The Cacheable attribute value requirements are:
• Must be 1 for any:
– Read transaction except ReadNoSnp and ReadNoSnpSep.
– Dataless transaction.
– Write transaction, except WriteNoSnpFull, WriteNoSnpPtl, WriteNoSnpZero, and WriteNoSnpDef.
• Must be 0 for any:
ARM IHI 0050
Issue H
Copyright © 2014, 2017-2025 Arm Limited or its affiliates. All rights reserved.
Non-confidential
150
```
