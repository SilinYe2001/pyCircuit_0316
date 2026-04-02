<!-- **Source:** `LinxCore950 CSU Design Specification-AI辅助设计输入.docx` | **Generated:** 2026-04-01 | pandoc --extract-media=SRC-07_media -->

+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
|                                                          | ![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image1.png){width="4.354166666666667in" |
|                                                          | height="0.8333333333333334in"}                                                                                                      |
+=========================+================================+=====================================================================================================================================+
|                                                          |                                                                                                                                     |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
|                                                          |                                                                                                                                     |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
|                                                          |                                                                                                                                     |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
|                                                          |                                                                                                                                     |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
|                                                          |                                                                                                                                     |
+----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------+
| CSU                                                                                                                                                                                            |
|                                                                                                                                                                                                |
| Design spec                                                                                                                                                                                    |
+-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Issue**               |                                                                                                                                                                      |
+-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| **Date**                |                                                                                                                                                                      |
+-------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                                                                                                |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

+----------------------------------------------------------------------------------------------------------------------------------------------+
| Copyright © HiSilicon Technologies Co., Ltd. All rights reserved.                                                                            |
|                                                                                                                                              |
| No part of this document may be reproduced or transmitted in any form or by any means without prior written consent of HiSilicon             |
| Technologies Co., Ltd.                                                                                                                       |
|                                                                                                                                              |
| Trademarks and Permissions                                                                                                                   |
|                                                                                                                                              |
| ![HI_logo](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image2.jpeg){width="0.2916666666666667in" |
| height="0.28125in"},                                                                                                                         |
| ![hisilicon](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image3.jpeg){width="1.0625in"           |
| height="0.13541666666666666in"}, and other HiSilicon icons are trademarks of HiSilicon Technologies Co., Ltd.                                |
|                                                                                                                                              |
| All other trademarks and trade names mentioned in this document are the property of their respective holders.                                |
|                                                                                                                                              |
| Notice                                                                                                                                       |
|                                                                                                                                              |
| The purchased products, services and features are stipulated by the contract made between HiSilicon and the customer. All or part of the     |
| products, services and features described in this document may not be within the purchase scope or the usage scope. Unless otherwise         |
| specified in the contract, all statements, information, and recommendations in this document are provided \"AS IS\" without warranties,      |
| guarantees or representations of any kind, either express or implied.                                                                        |
|                                                                                                                                              |
| The information in this document is subject to change without notice. Every effort has been made in the preparation of this document to      |
| ensure accuracy of the contents, but all statements, information, and recommendations in this document do not constitute a warranty of any   |
| kind, express or implied.                                                                                                                    |
+==============================================================================================================================================+

+----------------------------------------------------------------------------------------------------+
| HiSilicon Technologies Co., Ltd.                                                                   |
+=====================================+:=============================================================+
| Address:                            | Huawei Industrial Base                                       |
|                                     |                                                              |
|                                     | Bantian, Longgang                                            |
|                                     |                                                              |
|                                     | Shenzhen 518129                                              |
|                                     |                                                              |
|                                     | People\'s Republic of China                                  |
+-------------------------------------+--------------------------------------------------------------+
| Website:                            | <http://www.hisilicon.com>                                   |
+-------------------------------------+--------------------------------------------------------------+
| Email:                              | <support@hisilicon.com>                                      |
+-------------------------------------+--------------------------------------------------------------+

# About This Document {#about-this-document .Heading1-No-Number}

## Purpose {#purpose .Heading2-No-Number}

This document describes the basic functions and specifications of CSU
subsystem.

## Intended Audience {#intended-audience .Heading2-No-Number}

This document is intended for

- RTL design

- UT/Top verification

# Contents {#contents .Contents}

[About This Document [i](#about-this-document)](#about-this-document)

[1 Terminology [8](#terminology)](#terminology)

[2 Overview [9](#overview)](#overview)

[3 Microarchitecture [11](#microarchitecture)](#microarchitecture)

> [3.1 Cross Bar [11](#cross-bar)](#cross-bar)
>
> [3.1.1 Topology for CSU [11](#topology-for-csu)](#topology-for-csu)
>
> [3.2 Pipeline [12](#pipeline)](#pipeline)
>
> [3.2.1 Coherence and Flavor Information Storage
> [14](#coherence-and-flavor-information-storage)](#coherence-and-flavor-information-storage)
>
> [3.2.2 Snoop Filter [15](#snoop-filter)](#snoop-filter)
>
> [3.2.3 Data-ram [16](#data-ram)](#data-ram)
>
> [3.2.5 X Write Buffer [19](#x-write-buffer)](#x-write-buffer)
>
> [3.2.6 Hazard Checking and Onpipe Forwarding
> [20](#hazard-checking-and-onpipe-forwarding)](#hazard-checking-and-onpipe-forwarding)
>
> [3.2.7 Serializing [25](#serializing)](#serializing)
>
> [3.2.8 Fill Wakeup [27](#fill-wakeup)](#fill-wakeup)
>
> [3.2.9 Load Cancel [29](#load-cancel)](#load-cancel)
>
> [3.3 Frontend Control [30](#frontend-control)](#frontend-control)
>
> [3.3.1 Frontend Control Flow
> [30](#frontend-control-flow)](#frontend-control-flow)
>
> [3.3.2 Resource Management
> [32](#resource-management)](#resource-management)
>
> [3.3.3 Sleep and Wakeup Control
> [32](#sleep-and-wakeup-control)](#sleep-and-wakeup-control)
>
> [3.3.4 Flush Control [33](#flush-control)](#flush-control)
>
> [3.4 Backend Control [34](#backend-control)](#backend-control)
>
> [3.4.1 BRQ FSM [34](#brq-fsm)](#brq-fsm)
>
> [3.4.2 Bram Write Arbitration
> [37](#bram-write-arbitration)](#bram-write-arbitration)
>
> [3.4.3 Bram Read Arbitration
> [37](#bram-read-arbitration)](#bram-read-arbitration)
>
> [3.6 Master Interface [40](#master-interface)](#master-interface)
>
> [3.6.1 Feature List [40](#feature-list-1)](#feature-list-1)
>
> [3.6.2 Sturcture [41](#sturcture)](#sturcture)
>
> [3.6.3 MRB [43](#mrb)](#mrb)
>
> [3.7 CPU Interface [44](#cpu-interface)](#cpu-interface)
>
> [3.7.1 CPU Slave [44](#cpu-slave)](#cpu-slave)
>
> [3.7.2 Asyn_bridge CHI interface
> [45](#asyn_bridge-chi-interface)](#asyn_bridge-chi-interface)

[4 Feature [47](#feature)](#feature)

> [4.3.1 The Order in Xbar [49](#the-order-in-xbar)](#the-order-in-xbar)
>
> [4.3.2 The Order in Home [49](#the-order-in-home)](#the-order-in-home)

[5 Flow [50](#flow)](#flow)

> [5.1 Streaming [50](#streaming)](#streaming)
>
> [5.4 DVM [53](#dvm)](#dvm)

[6 Algorithm [54](#algorithm)](#algorithm)

> [6.1 LFSR [54](#lfsr)](#lfsr)
>
> [6.1.1 LFSR Overview [54](#lfsr-overview)](#lfsr-overview)
>
> [6.1.2 LFSR [56](#lfsr-1)](#lfsr-1)
>
> [6.2.1 Arbitration solution
> [57](#arbitration-solution)](#arbitration-solution)
>
> [6.2.2 LFSR Generation [60](#lfsr-generation)](#lfsr-generation)
>
> [6.4 Replacement [62](#replacement)](#replacement)
>
> [6.4.1 RRIP [62](#rrip)](#rrip)

[7 Clock and Reset [65](#clock-and-reset)](#clock-and-reset)

> [7.1 Clock domain [65](#clock-domain)](#clock-domain)
>
> [7.2 Reset domain [68](#reset-domain)](#reset-domain)
>
> [7.3 Reset hierarchy control and sequence
> [70](#reset-hierarchy-control-and-sequence)](#reset-hierarchy-control-and-sequence)
>
> [7.4 PIPE Clock and Reset control
> [71](#pipe-clock-and-reset-control)](#pipe-clock-and-reset-control)
>
> [7.4.1 PIPE clock [71](#pipe-clock)](#pipe-clock)
>
> [7.4.2 PIPE reset [71](#pipe-reset)](#pipe-reset)

[8 Interface with CPU core
[72](#interface-with-cpu-core)](#interface-with-cpu-core)

> [8.1 Transaction Type [72](#transaction-type)](#transaction-type)
>
> [8.2 Protocol Compliance
> [72](#protocol-compliance)](#protocol-compliance)
>
> [8.2.1 WriteEvictOrEvict [72](#writeevictorevict)](#writeevictorevict)
>
> [8.2.2 CMO early comp [72](#cmo-early-comp)](#cmo-early-comp)
>
> [8.2.3 DVM feild [72](#dvm-feild)](#dvm-feild)

[9 Interface with SoC [74](#interface-with-soc)](#interface-with-soc)

> [9.1 Transaction Type [74](#transaction-type-1)](#transaction-type-1)
>
> [9.2 Protocol Compliance
> [74](#protocol-compliance-1)](#protocol-compliance-1)

# Figures {#figures .Contents}

> [Fig 3‑1 Main Pipeline [13](#_Ref53247644)](#_Ref53247644)
>
> [Fig 3‑2 Coherence and Flavor Information
> [14](#_Ref200373773)](#_Ref200373773)
>
> [Fig 3‑3 SF index generation [15](#_Ref53427941)](#_Ref53427941)
>
> [Fig 3‑4 Contents of sf-ram [15](#_Ref53475586)](#_Ref53475586)
>
> [Fig 3‑5 Tag-data pipeline relationship under MCP 1+2
> [17](#_Toc200473302)](#_Toc200473302)
>
> [Fig 3‑6 Tag-data pipeline relationship under MCP 2+3
> [17](#_Ref200461104)](#_Ref200461104)
>
> [Fig 3‑7 XWB structure [19](#_Ref53591761)](#_Ref53591761)
>
> [Fig 3‑8 Hazard Checking Window in BEC
> [21](#_Ref69916685)](#_Ref69916685)
>
> [Fig 3‑9 Hazard Checking Window in BEC for Eviction
> [22](#_Ref69918800)](#_Ref69918800)
>
> [Fig 3‑10 SF evicted to BIB 2-cycle hazard window
> [22](#_Ref70411214)](#_Ref70411214)
>
> [Fig 3‑11 XWB Update-Lookup 2-cycle Window
> [23](#_Ref70005363)](#_Ref70005363)
>
> [Fig 3‑12 BFE update to SF_REALLOC 2-cycle Window
> [24](#_Ref70412725)](#_Ref70412725)
>
> [Fig 3‑13 Younger to older forward on pipe due to update to lines
> evicted from SF-ram [24](#_Ref200994402)](#_Ref200994402)
>
> [Fig 3‑14 Younger to older forward on pipe due to update to lines
> evicted from tag-ram [25](#_Ref200994405)](#_Ref200994405)
>
> [Fig 3‑15 Evicted Address is NOT serialized and later request hit on
> it [25](#_Toc200473313)](#_Toc200473313)
>
> [Fig 3‑16 way records and ALEV compare pipeline
> [26](#_Ref206065126)](#_Ref206065126)
>
> [Fig 3‑17 Evicted Address is NOT serialized and later request hit on
> it [26](#_Ref70603857)](#_Ref70603857)
>
> [Fig 3‑18 L3EVICT is invalidated by ALLOC_EVICT with 1-cycle window
> [27](#_Ref70685636)](#_Ref70685636)
>
> [Fig 3‑19 L3EVICT is invalidated by ALLOC_EVICT with 2-cycle window
> [27](#_Ref70687934)](#_Ref70687934)
>
> [Fig 3‑24 T Direction CSU hit LTU 19cycle (mcp 2+4)
> [28](#_Toc225501354)](#_Toc225501354)
>
> [Fig 3‑25 B pipeline stage [28](#_Ref200644153)](#_Ref200644153)
>
> [Fig 3‑26 B pipeline structure [29](#_Ref200644166)](#_Ref200644166)
>
> [Fig 3‑27 Frontend Top Diagram [30](#_Ref53664646)](#_Ref53664646)
>
> [Fig 3‑28 FRQ FSM [31](#_Ref53682395)](#_Ref53682395)
>
> [Fig 3‑29 Bypass Pipeline [31](#_Ref53729363)](#_Ref53729363)
>
> [Fig 3‑30 FRQ FSM with Sleep [33](#_Ref54776459)](#_Ref54776459)
>
> [Fig 3‑36 Flush control FSM [33](#_Toc225501361)](#_Toc225501361)
>
> [Fig 3‑37 Main State Transition [35](#_Ref54621345)](#_Ref54621345)
>
> [Fig 3‑38 TQ FSM State Transition [36](#_Ref54626519)](#_Ref54626519)
>
> [Fig 3‑39 TS FSM State Transition [37](#_Ref54634707)](#_Ref54634707)
>
> [Fig 3‑40 Bram Write Arbitration [37](#_Ref61249616)](#_Ref61249616)
>
> [Fig 3‑41 Bram Read Arbitration [38](#_Ref61251577)](#_Ref61251577)
>
> [Fig 3‑42 fill wakeup and fill data pipeline for 64B data channel
> [39](#_Ref111483626)](#_Ref111483626)
>
> [Fig 3‑43 fill wakeup and fill data pipeline for 32B data channel
> [40](#_Ref111483913)](#_Ref111483913)
>
> [Fig 3‑44 Master Interface Overview
> [42](#_Ref54081980)](#_Ref54081980)
>
> [Fig 3‑45 Structure of Each Channel's transfer
> [43](#_Ref54083900)](#_Ref54083900)
>
> [Fig 3‑46 Structure of CPU slave [45](#_Ref70511190)](#_Ref70511190)
>
> [Fig 3‑47 Structure of TX CHI [45](#_Toc225501372)](#_Toc225501372)
>
> [Fig 3‑48 Structure of RX CHI [46](#_Toc225501373)](#_Toc225501373)
>
> [Fig 4‑1 Alias Handling [47](#_Ref111570913)](#_Ref111570913)
>
> [Fig 4‑2 Cache State Transition with Alias handling
> [48](#_Ref112074409)](#_Ref112074409)
>
> [Fig 5‑1 WRNT without Alias [50](#_Ref112077921)](#_Ref112077921)
>
> [Fig 5‑2 WRNT with Alias [51](#_Ref112077939)](#_Ref112077939)
>
> [Fig 5‑3 VACMO miss L1 without alias
> [51](#_Ref112078276)](#_Ref112078276)
>
> [Fig 5‑4 VACMO miss L1 without alias
> [52](#_Ref112078510)](#_Ref112078510)
>
> [Fig 5‑5 VACMO hit L1D [52](#_Ref112078657)](#_Ref112078657)
>
> [Fig 6‑1 LFSR example [54](#_Toc225501381)](#_Toc225501381)
>
> [Fig 6‑2 Fibonacci LFSR example [54](#_Toc225501382)](#_Toc225501382)
>
> [Fig 6‑3 Galois LFSR example [54](#_Toc225501383)](#_Toc225501383)
>
> [Fig 6‑4 LFSR Feedback polynomial example
> [55](#_Toc225501384)](#_Toc225501384)
>
> [Fig 6‑5 Galois LFSR example with N=3, BASE=2
> [55](#_Toc225501385)](#_Toc225501385)
>
> [Fig 6‑6 Galois LFSR example with BASE=2,POW=2,LFSR_LEN=6
> [56](#_Toc225501386)](#_Toc225501386)
>
> [Fig 6‑7 Pipeline T0 Arbitration [57](#_Toc225501387)](#_Toc225501387)
>
> [Fig 6‑8 Pipeline Arbitration Algorithm
> [58](#_Toc225501388)](#_Toc225501388)
>
> [Fig 6‑9 force rand to reduce chances of starvation
> [59](#_Toc225501389)](#_Toc225501389)
>
> [Fig 6‑10 arbitration algorithm block diagram
> [60](#_Toc225501390)](#_Toc225501390)
>
> [Fig 6‑11 arbitration direction LFSR structure
> [60](#_Toc225501391)](#_Toc225501391)
>
> [Fig 6‑12 arbitration boundary LFSR structure
> [61](#_Toc225501392)](#_Toc225501392)
>
> [Fig 6‑13 arbitration boundary force random LFSR structure
> [61](#_Toc225501393)](#_Toc225501393)
>
> [Fig 6‑14 Sample sets selection for set dueling (core0, thread0)
> [63](#_Ref61686116)](#_Ref61686116)
>
> [Fig 6‑15 Set Dueling Policy [64](#_Toc225501395)](#_Toc225501395)
>
> [Fig 7‑1 Clock Stucture [67](#_Ref53594320)](#_Ref53594320)
>
> [Fig 7‑2 Reset Structure [68](#_Ref53594394)](#_Ref53594394)
>
> [Fig 7‑3 Rest Sequence [70](#_Toc225501398)](#_Toc225501398)
>
> [Fig 7‑4 PIPE Rest Sync and clock management
> [71](#_Toc85529915)](#_Toc85529915)
>
> [Fig 7‑5 PIPE clock structure [71](#_Toc85529916)](#_Toc85529916)

# Tables {#tables .Contents}

> [Tab 2‑1 Key Structure Capability [9](#_Toc225501401)](#_Toc225501401)
>
> [Tab 3‑1 Channel Requirement [11](#_Ref114235377)](#_Ref114235377)
>
> [Tab 3‑3 Coherence bits and encoding state for T
> [14](#_Ref200388243)](#_Ref200388243)
>
> [Tab 3‑4 Field Description of sf-ram
> [15](#_Ref53475624)](#_Ref53475624)
>
> [Tab 3‑5 Memory Latency Configuration
> [16](#_Ref53481154)](#_Ref53481154)
>
> [Tab 3‑6 Memory Latency Configuration
> [32](#_Toc225501406)](#_Toc225501406)
>
> [Tab 3‑8 Main FSM State [34](#_Ref54620476)](#_Ref54620476)
>
> [Tab 3‑9 TQ FSM State [35](#_Ref54626462)](#_Ref54626462)
>
> [Tab 3‑10 TS FSM State [36](#_Ref54634535)](#_Ref54634535)
>
> [Tab 3‑11 Major Properties of Master Interface
> [40](#_Ref54079460)](#_Ref54079460)
>
> [Tab 6‑1 Galois LFSR polynomial with N=3, BASE=2
> [55](#_Toc225501411)](#_Toc225501411)
>
> [Tab 6‑2 Arbitration algorithm control signal
> [58](#_Toc225501412)](#_Toc225501412)

# Terminology

  --------------------------------------------------------------------------------
  **Name**                  **Abbreviation**   **Description**
  ------------------------- ------------------ -----------------------------------
  L3 Cache System           l3sys              L3 Cache System.

  Express                   EXP                Interconnection bus

  Split Buffer              SPB                buffer in CS for getting on ring

  Merge Buffer              MGB                buffer in CS for getting off ring

  Pipe                      pipe               top level of
                                               front-end/pipeline/backend

  Core Frontend Control     CFE                core/acp front-end wrapper

  Core Frontend Request     CFRQ               for each entry of CFE
  Queue                                        

  Snoop Frontend Control    SFE                Snoop front-end wrapper

  Snoop Frontend Request    SFRQ               for each entry of SFE
  Queue                                        

  Backend Request Queue     BRQ                

  Backend Ram               BRAM               RAM of BDQ

  Back Invalidation Buffer  BIB                Request buffer for handling the
                                               un-ser sf eviction

  Tag Write Buffer          TWB                Temporary buffer for updating
                                               tag-ram

  SF Write Buffer           SWB                Temporary buffer for updating snoop
                                               filter ram

  Age Write Buffer          AWB                Temporary buffer for updating
                                               age-ram

  Master Interface          MST                Interface connecting with 1^st^ SoC
                                               Bus, for DMC

  Master Request Tracking   MRT/MRB            Request tracking table in master
  Table                                        interface

  CPU Interface             CPU_INTF           Interface connecting with CPU

  Local Device Interface    LCLDEV             Interface connecting with 2^nd^ SoC
                                               Bus, for peripheral

  Miscellaneous Node        MN                 

  Power Processing Unit     PPU                

  Power Management          PMNG               Module inside MN to handle the flow
                                               of PQ-Channel

  External Interface        EXT_INTF           Interface with system channel

                                               

                                               
  --------------------------------------------------------------------------------

# Overview

This chapter introduces top level CSU and its features.

## Feature list {#feature-list .level-2}

- dual core, Hisi in-house design

- 12M Shared Level2 Cache, 24 way association.

- 4 pipelines interleaving by PA\[7:6\]

- 4banks per pipeline interleaving by PA\[9:8\]

- 28 BEC entries per pipeline

- Interface with each core 2x REQ ports interleaving by PA\[6\], 1x RDAT
  port with 64B width, 1xTDAT port with 64B width;

- Dual core share a single PFL2 port

- Interface with Master 2xREQ port, 2xRXDAT port with 32B width for
  each, 2x TXDAT port with 32B width for each;

- NINE (performance toward inclusive) with L1I/D

- MPAM v1.0 is supported

- Partial Good is supported, 4M granularity, divided by way 0-7, 8-15,
  16-23

- Way-isolation is supported (non restricted)

- LTU 20 cycle

## Compliance {#compliance .level-2}

  -----------------------------------------------------------------------
                                      T
  ----------------------------------- -----------------------------------
  #pipeline                           4

  #bank/pipe                          4

  #master                             2\*32B

  #BEC/pipe                           28

  #CFE/pipe                           7

  #TWB/AWB                            7

  #SWB                                10
  -----------------------------------------------------------------------

  : []{#_Toc225501401 .anchor}Tab 2‑1 Key Structure Capability

# Microarchitecture

Each section should include structure, control flow, FSM, cycle chart,
interface (IO list) etc.

## Cross Bar

### Topology for CSU

In GUANGZHOU, this is changed to 1 cluster, P-cluster connects two cores
LX950 without PL2. The connection requirement of P-cluster is
illustrated in Tab 3‑1.

  -----------------------------------------------------------------------
                                      2xLX950(T)
  ----------------------------------- -----------------------------------
  TXREQ                               2x3(2dmd+1hwp)

  TXDAT                               2x64B\*2

  RXDAT                               2x64B\*2

  TXRSP                               2x1

  RXRSP                               2x2

  RXSNP                               2x1
  -----------------------------------------------------------------------

  : []{#_Ref114235377 .anchor}Tab 3‑1 Channel Requirement

According to Tab 3‑1, the xbar network requirement is listed below.

- REQ Channel

  - HWP Merge Split: 3core x 2island

  - Upstream:

    - (2core+1hwp)x2island\*2pipe, 4 pipe, 2 island

  - Downstream:

    - 4x1\*2, 4 pipe, 2 master

- DAT Channel

  - Upstream

    - TXDAT

      - Option1: 2x2x64B\*2, core has 1x2 DAT, each connects to one
        island

    - RXDAT

      - Upstream:

        - Option1: 2x4x64B\*2, 4 pipe, 4 bank/pipe

  - Downstream

    - TXDAT/RXDAT

      - Option1: 2x2x32B

- RSP Channel

  - Upstream:

    - TXRSP

      - Option1: 5x2\*2

      - Option2: 6x4

    - RXRSP

      - Option1: 2x5\*2\*2

      - Option2: 6x4

  - Downstream

    - TXRSP

      - Option1: 2x4

      - Option2: 2x6

    - RXRSP

      - Option1: 2x4

      - Option2: 2x6

- SNP Channel

  - Upstream:

    - Option1: 2x4\*2

    - Option2: 6x4

  - Downstream

    - Option1: 2x4

    - Option2: 2x6

## Pipeline

This section illustrates the overall pipeline control flow and the main
structure inside. The overall pipe diagram is shown in Fig 3‑1.

![[]{#_Ref53247644 .anchor}Fig 3‑1 Main
Pipeline](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image5.emf)

The Pipeline is connected directly to a cross station, therefore all the
information interaction is through the cross station (green node in the
figure). Generally, the pipeline is divided into 3 major parts, FEC
(Frontend Control), Pipeline, and BEC (Backend Control). FEC and BEC is
composed of multiple buffer entries, FRQ and BRQ, which is tracking part
of the whole lifetime of each request.

Requests from Core goes into CFRQ while snoop requests from downstream
goes into SFRQ. FRQ only tracks the requests which are un-serialized.
After the request is serialized, it will be migrated to BRQ, in which
the rest lifetime will be tracked. BIB[^1] (Back Invalid Buffer) is
responsible to track the requests triggered by snoop filter evictions,
also un-serialized.

XWB (T/S/A Write Buffer) is responsible to buffer the tag/snoop
filter/age updating operation respectively, therefore to schedule the
memory accessing when the memory port is available.

Data access is directly controlled by the tag pipelines at dedicated
slot according to different input/access latency, which is named as
TD-couple[^2].

At T0, requests from CFRQ/SFRQ/BRQ/BIB apply to get on the pipeline.
After resource availability checking, only requests which can get all
the needed resource token can send valid request to the main arbitrator.
Each arbitration allows one request to get on the pipeline, passed to
T1.

At T1, cacheable requests need to lookup the tag-ram and age-ram, while
snoopable requests need to lookup the snoop filter.

At T2, the results read from tag-ram is CAM (Compare and Match) with
online request. To reduce the read hit L3 latency, a speculative read is
sent to dmemctl since the memory input needs 2 cycles. The speculative
read is not qualified with the real hit result due to timing
convergence. A miss request will cancel the memory read at T3. The
hazard result also cancels the speculative read.

The hazard checking with serialized requests in BRQ costs multiple
cycles. All the hazard is merged and transferred to pipeline at T3. The
request with hazard will be flushed at T4.

### Coherence and Flavor Information Storage

CSU stores 3 types of information to complete the control plane
function. Illustrated in Fig 3‑2.

- Address related, tag and pipe-id, pipe id is for PG and ULP function
  only.

- Status and attributes related, this part is in charge of the cache
  state and memory attributes.

- Flavor bits. This part only impacts the performance but not the
  coherent function.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image6.png){width="6.69375in"
height="1.8597222222222223in"}

[]{#_Ref200373773 .anchor}Fig 3‑2 Coherence and Flavor Information

The deployment for the above information may be divided into tag-ram,
sf-ram and age ram. It is also related to the allocation policy of the
Cache, whether it is strictly inclusive with the core. For the coherence
status bit, different deployment has different state explanation.

In T direction, CSU is NINE with upstream, so there is a dedicated
structure of sf-ram which records the lines that inside L1D, L1I is not
recorded in SF, since IC-coherent is disabled. The sf and SF structure
is separated. The bits and encoding is shown in Tab 3‑3.

[]{#_Ref200388243 .anchor}Tab 3‑3 Coherence bits and encoding state for
T

+--------------------------------+-----------------------------------+-------+-------+-------+
| tag                            | sf                                | core0 | core1 | cache |
+----------+----------+----------+----------+----------+-------------+       |       |       |
| cu       | clean    | cp=\|pv  | npu      | cu       | pv          |       |       |       |
+==========+==========+==========+==========+==========+=============+=======+=======+=======+
| 0        | 0        | 0        | 0        | 0        | {0,0}       | I     | I     | I     |
+----------+----------+----------+----------+----------+-------------+-------+-------+-------+
| 1        | 1        | 0        | 0        | 0        | {0,0}       | I     | I     | UC    |
+----------+----------+----------+----------+----------+-------------+-------+-------+-------+
| 1        | 0        | 0        | 0        | 0        | {0,0}       | I     | I     | UD    |
+----------+----------+----------+----------+----------+-------------+-------+-------+-------+
| 0        | 1        | 0        | 0        | 0        | {0,0}       | I     | I     | SC    |
+----------+----------+----------+----------+----------+-------------+-------+-------+-------+
| 1        | 1        | 1        | 0        | 1        | {0,1}       | UX    | I     | UC    |
+----------+----------+----------+----------+----------+-------------+-------+-------+-------+
| 1        | 1        | 1        | 1        | 1        | {0,1}/{1,1} | SC    | I/SC  | UC    |
+----------+----------+----------+----------+----------+-------------+-------+-------+-------+
| 1        | 0        | 1        | 0        | 1        | {0,1}       | UX    | I     | UD    |
+----------+----------+----------+----------+----------+-------------+-------+-------+-------+
| 1        | 0        | 1        | 1        | 1        | {0,1}/{1,1} | SC    | I/SC  | UD    |
+----------+----------+----------+----------+----------+-------------+-------+-------+-------+
| 0        | 0        | 1        | 1        | 0        | {0,1}/{1,1} | SC    | I/SC  | SC    |
+----------+----------+----------+----------+----------+-------------+-------+-------+-------+

The attributes of pbha/shareable is derived from page, should be passed
through to cache together with the request address.

### Snoop Filter

To reduce snoop filter eviction, the index of snoop filter should be
hashed before addressing. Due to the timing issue, the snoop filter is
divided to 2 banks according to dedicated PA bit. The association of
each bank is 8 *[(TBD)]{.underline}*. Totally, there are 16 macros of
sf-ram in each pipeline, each of which is 1RW SRAM. In each bank, half
way uses the original PA bits as the index, while the other half uses
the hashed PA bits as the index. The index generation structure is shown
in Fig 3‑3. For each cache line in the snoop filter, besides tag bits,
corresponding information is stored as well. Fig 3‑4 illustrates the
content of snoop filter ram, while the detailed field description is
listed in Tab 3‑4. The initial value of {cu, npu} is 'h0, which is an
illegal cache state, indicating INVALID state.

![[]{#_Ref53427941 .anchor}Fig 3‑3 SF index
generation](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image7.emf)

![[]{#_Ref53475586 .anchor}Fig 3‑4 Contents of
sf-ram](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image8.emf)

  --------------------------------------------------------------------------------
  Name       Description                              Width
  ---------- ---------------------------------------- ----------------------------
  tag        address tag bits, excluding index bits,  PA_WIDTH-(6+INDEX_WIDTH)+1
             including ns bit                         

  pipe       Pipe bit is part of tag to support ULP   PIPE_WIDTH

  npu        non processor unique indicator           1

  cu         cluster unique indicator                 1

  pv         presence vector                          NUM_CINFS

  ~~pbha~~   ~~page based hardware attribute,         *~~4~~*
             indicating inner/outer                   
             shareable/cacheable, gid~~               

  ecc        ecc bit                                  *7*
  --------------------------------------------------------------------------------

  : []{#_Ref53475624 .anchor}Tab 3‑4 Field Description of sf-ram

### Data-ram

CSU is a unified cache to cover a large scale of capacity, from like
512K to 12M. So the data memory input and access latency is multi-cycle
and configurable. Tab 3‑5 illustrates different configurations of memory
access latency and the corresponding latency/bandwidth. A typical
multi-cycle configuration is 2+3+1, 2 cycles for memory due to the input
RC, 3 cycles for each memory access due to the min cycle of high density
memory cell, and 1 extra cycle to cover the output RC. Therefore, the
hit latency of a read is 6 cycles, and every access costs 3 cycles.
After each access, the memory is not available at the consecutive 2
cycles.

  -------------------------------------------------------------------------
     input       access      register       hit        Access     Bank num
   multicycle    latency       slice      latency     bandwidth   
  ------------ ----------- ------------- ---------- ------------- ---------
       1            2            1           4            2           2

       2            3            1           5            3           4

       2            4            1           6            4           4

       3            4            1           7            4           4
  -------------------------------------------------------------------------

  : []{#_Ref53481154 .anchor}Tab 3‑5 Memory Latency Configuration

3.  **Tag-Data Coupled Structure**

Tag and data pipelines are coupled with each other. The data is banked
by dedicated PA, since consecutive request within the mcp access
configuration is not allowed to get on the tag pipeline. Therefore, when
the request is getting on the tag pipeline, the dedicated slot of data
pipeline is already reserved.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image9.png){width="3.9145220909886262in"
height="3.6425918635170604in"}

[]{#_Toc200473302 .anchor}Fig 3‑5 Tag-data pipeline relationship under
MCP 1+2

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image10.png){width="4.161531058617673in"
height="3.5411220472440945in"}

[]{#_Ref200461104 .anchor}Fig 3‑6 Tag-data pipeline relationship under
MCP 2+3

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image11.png){width="6.69375in"
height="1.425in"}

Fig 3‑8 Tag-data pipeline relationship under MCP 3+4

The tag-data pipeline has co-operation with bram accessing. The access
request from tag-data pipeline to bram read/write has the highest
priority. The read bram setup from tag-data pipeline to bram always
happen at T1, and write bram setup from tag-data pipeline to bram always
happens at the last valid cycle in DRS. For the read hit bec flow, since
the hit information cannot be derived at T1, this flow will be canceled,
and re-scheduled in the BRQ TD control flow.

The dmemctl has its own input FSM and output FSM to drive the dedicated
memory access, shown in Fig 3‑ and Fig 3‑. The start of input FSM is
triggered by push_raw_t2, which is from or-reduction of hit_ways_t2,
without hazard and ecc checking. So there should be some cancel
condition happening at T3 and T4 stage. The start of output FSM is
trigger by input FSM at dedicated stage according to the combination of
IM and AM configuration. When the MCP configuration is 1+2, the output
FSM starts at DI0 with \~cancel_t3 condition, while the output FSM
starts at DI1 with \~cancen_t4 condition with MCP configuration 2+3

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image12.png){width="4.677106299212598in"
height="3.4749245406824145in"}

Fig 3‑8 Input FSM of dmemctl

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image13.png){width="3.572470472440945in"
height="3.0829483814523186in"}

Fig 3‑9 Output FSM of dmemctl

### X Write Buffer

XWB (T/S/A-Write Buffer) is the temporary buffer to store the update
request to the tag-ram, snoop filter and age-ram. Any update to the
tag-ram, snoop filter and age-ram is first pushed into XWB and then
scheduled to the dedicate ram in available slots. Fig 3‑7 illustrates
the structure of XWB. It is composed of WIB (Write Input Buffer) and WOB
(Write Output Buffer). Each request which may need to update the
tag/sf/age ram is required to apply the respective token of XWB and gets
on pipeline only when the token is available. Each update to the XWB
happens at T4 after hazard resolved

![[]{#_Ref53591761 .anchor}Fig 3‑7 XWB
structure](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image14.emf)

When there is an update request valid, it will be pushed into the least
available WIB with the corresponding payload. At each cycle, the least
valid request in the WIB of respective bank is picked out if the
corresponding entry in WOB is empty. Besides, ECC is attached in this
process. When corresponding bank port of memory is available, the
content in WOB can be update to memory. Looking up the SRAM always takes
the higher priority, while the updating only takes the available slots.

There is a corner case that updating to the same position of SRAM
overlaps with each other. It means that, before the prior update is
drained to SRAM, another update to the same position comes. Therefore,
for each ingress request of XWB, it should be CAM with the existing
valid entries in WIB and overwrite the WIB with the latest payload.

The T/S/A-Write Buffer shares the same structure of XWB with different
parameter of the number of WIB entries N and the number of WOB entries
B. currently the number of WIB in each XWB is 7 and will be determined
by CA performance data. The number of WOB for TWB is 2 Corresponding to
PA. The number of WOB for SWB is 2 Corresponding to 2 banks. The number
of WOB for AWB and TWB is 2.

### Hazard Checking and Onpipe Forwarding

The hazard checking divides into two parts, one is done on pipeline,
while the other is done in each BEC entry.

At T1, each request on the pipeline will CAM address with the request at
BEC top which is at T4, together with all the requests in BEC entry. At
T2, the *chaz* is further checked in each entry. At T3, pipeline can get
the hazard result from BEC.

Since CAM all the BEC cannot be achieved in 1 cycle, there is some
windows. The on-pipe hazard checking includes the following points, to
cover the window.

- At T2, each normal cacheable request is compared with the request at
  T3, if they have the same address, the request at T2 will be marked
  hazard. This is to cover the 1 cycle window of BEC hazard lookup.

- At T2, each normal cacheable request is compared with the request at
  T4, if they have the same address, the request at T2 will be marked
  hazard. This is to cover the 2 cycle window of BEC hazard lookup

- At T2, the ordered request is compared with the request at T3. If they
  have matched the hazard condition 1) from same lpid with EO hazard, 2)
  from the same lpid with RO and 8B address overlapping, the request at
  T2 will be marked as hazard. This is also to cover the 1 cycle window
  of BEC hazard lookup.

At T1 cycle, the request on the pipeline will CAM all the addr in BEC to
get if it is with the same address. At T2 cycle, with the CAM result,
the *chaz* is further checked to get valid hazard result. For each
request in BEC, the initial information is allocated at T4 and valid on
T5, so consecutive 3 requests on pipe cannot get the precise addr CAM
result. The *chaz* indication is asserted at T4 in BEC. So consecutive
requests cannot get valid *chaz* result in BEC. Therefore, consecutive 3
request with same cache line address/EO/RO hazard checking should be
flushed on pipe to cover this 1 cycle window. Fig 3‑8 shows the 1-cycle,
2 cycle, 3 cycle windows.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image15.png){width="4.362485783027122in"
height="3.9314391951006122in"}

[]{#_Ref69916685 .anchor}Fig 3‑8 Hazard Checking Window in BEC

- At T2, each cacheable request will compare its address with the
  evicted address at T3 and T4. If they have the same address, the
  request at T2 will be marked as hazard.

Since the evicted address can only be derived with the ALLOC_EVICT
request on pipe after looking up tag. It can only be valid in BEC
*AFTER* T4. Fig 3‑9 shows the 3cycle window.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image16.png){width="4.768576115485565in"
height="3.9427788713910763in"}

[]{#_Ref69918800 .anchor}Fig 3‑9 Hazard Checking Window in BEC for
Eviction

- If a request leads to SF eviction on, the consecutive 2 requests with
  the same address of the eviction should be marked as hazard, otherwise
  they cannot lookup the precise SF information. Fig 3‑10 shows the
  2-cycle hazard window. Since BIB is not a serialized buffer, it is
  part of the SF. So REQ3 can directly update its info to the hit BIB,
  treating it as the normal SF-ram.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image17.png){width="4.580683508311461in"
height="3.797859798775153in"}

[]{#_Ref70411214 .anchor}Fig 3‑10 SF evicted to BIB 2-cycle hazard
window

- For set-way flush at T2, it does not have a valid address. It will
  compare its source with the set-way flush at T3, if here is one, to
  avoid flushing the same cache-line within the consecutive cycles.

All the marked requests will be merged to the hazard condition on T3 on
pipeline, pipeline will use the result to qualify the real action. Due
to timing closure issue, the flush and token release indication will be
sliced to T4.

To improve the pipeline efficiency, we want to avoid the same index
hazard and all-way lock hazard on pipeline. On-pipe forwarding is
realized then. Therefore, to make function works, the ALLOC_EVICT should
get the latest information.

- Consecutive request with same index will get the latest information of
  previous requests

With the help of XWB structure, any update to the index is done in the
first pipe flow (except for the ALLOC_EVICT operation) at T4 and
available at T5. Looking up XWB happens at T2. Therefore, the
consecutive 2 requests after the updating cannot get the latest
information from XWB. Therefore, we can forward the latest information
directly on pipe, so that a request can always get the latest
information without more hazard. Fig 3‑11 shows the 2-cycle window on
pipe.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image18.png){width="5.561031277340333in"
height="3.707353455818023in"}

[]{#_Ref70005363 .anchor}Fig 3‑11 XWB Update-Lookup 2-cycle Window

- For SF_REALLOC request, if the previous request hit it in BIB and
  update it, the re-allocation should get the latest information update
  from T4 on-pipe. Fig 3‑12 shows the 2-cycle forwarding window.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image19.png){width="4.914128390201225in"
height="4.597087707786526in"}

[]{#_Ref70412725 .anchor}Fig 3‑12 BFE update to SF_REALLOC 2-cycle
Window

ALEV/SFUPD from BEC to pipeline are serialized requests that cannot be
flushed except for ECC errors, to avoid live-lock. Therefore, same addr
forwarding is required for ALEV/SFUPD. Part of the forwarding is done.
When the ALEV/SFUPD is updating someone which is already evicted. There
are some scenarios that forwarding is happening from younger request (on
pipeline) to older request. The scenarios are illustrated in Fig 3‑13
and Fig 3‑14.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image20.png){width="6.69375in"
height="4.072916666666667in"}

[]{#_Ref200994402 .anchor}Fig 3‑13 Younger to older forward on pipe due
to update to lines evicted from SF-ram

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image21.png){width="6.69375in"
height="3.4381944444444446in"}

[]{#_Ref200994405 .anchor}Fig 3‑14 Younger to older forward on pipe due
to update to lines evicted from tag-ram

### Serializing

The most significant function of pipeline is to serialize all the
requests. If a request is free of any hazard in both BEC and pipeline,
it can be serialized. Any other request with the same address must be
marked as hazard and flushed back to the FEC. Only after the serialized
request completes, according to the protocol, the request with same
address in FEC can be wake up to try to get serialized again.

The ALLOC_EVICT will change the address in the pass flow. The original
address has been serialized, but the evicted address cannot pass the
hazard checking in this flow since the evicted address can only be
available at T3 on pipeline, which already misses the PA checking at T1
stage. To avoid way-lock flush influencing the pipeline efficiency. The
ALLOC_EVICT is progressing as normal, but not to serialize the evicted
address immediately in this pass flow when the way is under using by
other requests in BEC. The benefit of this option is to release the
hazard of the original address as soon as possible without more hazard
flow. Since the evicted address is not serialized, it will take another
pass flow on the pipeline to check hazard and get serialized

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image22.png){width="2.9363812335958004in"
height="3.155345581802275in"}

[]{#_Toc200473313 .anchor}Fig 3‑15 Evicted Address is NOT serialized and
later request hit on it

Each request hits a way or selects way when requiring allocating a new
cache-line, records the way information in the BEC entry. The
ALLOC_EVICT compares the way and set with each BEC entry. If the
destination way of ALLOC_EVICT hits the same way record in the BEC
entry, the EVICT PA can not be serialized immediately. It will become an
un-serialized L3EV in BEC entry. Fig 3‑16 illustrates the record and
compare pipelines.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image23.png){width="5.242272528433946in"
height="2.4615135608048995in"}

[]{#_Ref206065126 .anchor}Fig 3‑16 way records and ALEV compare pipeline

The evicted address is not serialized, and the original address/data
will be updated to the tag/data without hazard. Therefore, the evicted
address only exists in BEC. It means that the later request which
requires the evicted address should be hit in BEC. The BEC becomes the
shadow of the data cache. Fig 3‑17 shows the hit BEC pipeline window.

![[]{#_Ref70603857 .anchor}Fig 3‑17 Evicted Address is NOT serialized
and later request hit on
it](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image24.png){width="5.794227909011374in"
height="2.344982502187227in"}

The hitting BEC scenarios are listed as below.

- The ALLOC_EVICT flow should hit itself in BEC to get the information
  to update.

- The ALLOC_EVICT flow may hit another un-serialized L3EVICT with the
  same address. Under UD-HD state, ALLOC_EVICT hits L3 to update the
  data. BEC is the shadow cache, so ALLOC_EVICT may hit another L3EVICT
  BEC entry. Under this scenario, the ALLOC_EVICT will re-allocate this
  address back into the tag-ram, so that the L3EVICT entry should be
  invalidated and release. There is also 1-cycle window should be
  covered on pipeline, shown in Fig 3‑18 and Fig 3‑19.

![[]{#_Ref70685636 .anchor}Fig 3‑18 L3EVICT is invalidated by
ALLOC_EVICT with 1-cycle
window](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image25.png){width="5.960279965004374in"
height="2.0263353018372703in"}

![[]{#_Ref70687934 .anchor}Fig 3‑19 L3EVICT is invalidated by
ALLOC_EVICT with 2-cycle
window](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image26.png){width="5.639939851268592in"
height="2.207645450568679in"}

Since the L3EV is un-serialized in BEC entry, it is like part of the
cache. When a new coming request hit the same PA with the un-serialized
L3EV, Treat the L3EV as hazard source for the requests from core.

### Fill Wakeup

To promote performance for load request, CSU can give an early wakeup to
upstream to make the upstream start some preparation work. In CSU
design, the fill wakeup is important to ensure the load to use latency.
The fill wakeup is used inside LSU to wake up the origin load to get on
pipe to get the result bus access right. When the refill data is
arrived, it can be directly used by IEX pipeline. Since CSU needs to
cover from 0.5M to 12M cache capacity, the wakeup generation is quite
different due to different data memory input and output latency.

For T direction, there are 2 cores sharing 12MB cache capacity. With
much bigger floorplan and multiple cores, on the road from core to CSU
home, extra IRS and xbar arbitration is added to cover the RC distance
and multiple core arbitration. The data filling path is as the same as
the request sending path. In the refilling path, the arbitration is
always happening on the early wakeup channel, and the data MUX is
flowing the arbitration result after a fixed of 6 cycles, to cover the
wakeup flow from P1 to E4.

> ![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image27.png){width="4.729150262467192in"
> height="3.7184590988626423in"}

[]{#_Toc225501354 .anchor}Fig 3‑24 T Direction CSU hit LTU 19cycle (mcp
2+4)

- CSU miss wakeup generation on B pipeline

Fig 3‑25 and Fig 3‑26 shows the B pipeline stage and structure. The miss
refill is scheduled through BEC on the B-pipeline. After the data is
received from downstream (ASYC bridge latency is not involved here), one
IRS is in the middle to cover the RC, then set the related BRQ data
ready through txnid match. B0 is the first cycle, picking one of the
ready request is BEC according to SS arb. If there is no other older
valid requests waiting, this request is pass to B1. In B1 stage, the
txnid is mux out from BEC payload and setup the rbuf. Therefore, in B2
stage, all the wakeup information is ready in rbuf, fifo based. In the
next cycle, this information is ready on the interface of L2 and core.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image28.png){width="6.038326771653543in"
height="2.010269028871391in"}

[]{#_Ref200644153 .anchor}Fig 3‑25 B pipeline stage

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image29.png){width="6.69375in"
height="2.578472222222222in"}

[]{#_Ref200644166 .anchor}Fig 3‑26 B pipeline structure

### Load Cancel

When CSU is used as the level 2 cache, the load to use latency should be
carefully optimized. LSU send out the miss request at C1 (E3) stage. The
TLB translation is done at the end of E2. All the legality checking
cannot complete due to timing convergence, so the cancel signal is given
at the next cycle at C2. According to the LTU pipeline, due to different
bypass strategy, the cancel qualification is at different stage. For T
direction, the load can be canceled at T1 by the cancel valid with txnid
available right after the request is picked at T0. Otherwise, the load
can be canceled at FEC. If the load is canceled, the FEC entry is
released then. The gray colored block in Fig 3 29 shows the position to
deal with the load cancel. Besides, since the txnid can be reused in
some scenario, the cancel CAM is only applied with load request. For C
direction, since the earliest bypass is E3T1 alignment, the the cancel
request is only received at T2 stage.

Fig 3 31 Tag pipeline with load cancel qualification for T direction

## Frontend Control 

### Frontend Control Flow

![[]{#_Ref53664646 .anchor}Fig 3‑27 Frontend Top
Diagram](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image30.emf)

Frontend and Backend is divided according to whether a request is
serialized or not. Before serialization, a request is tracked by the
frontend control, while the serialized lifetime is tracked by the
backend. As shown in Fig 3‑27, besides CFE (Core FrontEnd) and SFE
(Snoop FrontEnd) which are tracking the requests from core and
down-stream coherence snoop, BFE is tracking the un-serialized lifetime
of snoop evictions from pipeline. Therefore, BFE is also belonging to
the frontend. They have basically the same structure. The entry number
of each frontend queue can be configurable by parameter, validated
according to the CA performance data. Inside each queue, age-based
arbitration is deployed. The FSM of FRQ is illustrated in Fig 3‑28.
Allocation of a new request will trigger the FSM steps into T0, then
steps into T1 if picked by the pipeline. Flushes from pipeline can make
the FSM go back to T0. ~~(*[TBD: on-pipe hazard and resource hazard
generates flush at T2 like the dashed arrow]{.underline}*)~~. Only the
oldest awake request can participate in pipeline arbitration at T0.

![[]{#_Ref53682395 .anchor}Fig 3‑28 FRQ
FSM](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image31.emf)

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image32.emf)[]{#_Ref53729363
.anchor}

Fig 3‑29 Bypass Pipeline

To reduce the shortest latency, speculative bypass is deployed. When
current requests in FRQ are all not in the T0 state, which is awake and
waiting for picking by pipeline, the new coming request can
speculatively perform an allocation in CFRQ and arbitration at T0 at the
same cycle. The bypass pipeline from receiving the request to getting on
pipeline is shown in

Fig 3‑29. The pend indication generates bypass_vld and directly
participates in T0 arbitration with elevate equaling to 1'b0, which
means lower priority. If there is no other request with elevate equaling
to 1'b1, the speculative bypass request can be picked by T0 arbitration.
The corresponding information is qualified with the real valid
indication.

**Attention:** speculatively bypass has no request type restriction.

### Resource Management

To reduce power consumption caused by flushing due to resource reasons,
Pipeline resource management take the responsibility of collecting the
usage of each resource in the pipeline. When there are any REQs want to
participate in T0 arbitration, it will check that whether all
required-resources can be provided. If not, this REQ cannot participate
in T0 arbitration and will retry at next round. Tab lists all the number
of resource tokens, including the specific constraints for each
allocation or de-allocation or reservation.

  ------------------------------------------------------------------------------
  TOKEN         MAX_TKN   MAX_ALLOC   MAX_REL   remark
  ------------- --------- ----------- --------- --------------------------------
  brq_cnt       32        2           3         According to the total entry
                                                number of BRQ

  brq_snp_cnt   28        1           2         The max tokens can be used by
                                                snp requests in BRQ

  bib_cnt       4         1           1         According to the total entry
                                                number of BIB

  twb_cnt       10        1           2         According to the total entry
                                                number of TWB

  swb_cnt       10        1           2         According to the total entry
                                                number of SWB

  awb_cnt       10        1           2         According to the total entry
                                                number of AWB
  ------------------------------------------------------------------------------

  : []{#_Toc225501406 .anchor}Tab 3‑6 Memory Latency Configuration

**Remark**: 1)MAX_ALLOC: the maximum num of token resources can be
allocated every beat.

2)MAX_REL : the maximum num of token resources can be released every
beat.

### Sleep and Wakeup Control

Sleep and Wakeup Control is used to improve the pipeline utilization.
Requests which are flushed due to serialized requests with same address
or order will go to sleep in FRQ. Therefore, this request will not
participate in pipeline arbitration before wakeup. At the same time, the
BRQ entry which causes the current flush will be recorded. When the
recorded entry its request flow is over, the relative FRQ will wake up
and participate in T0 arbitration again. Besides, the self-wakeup
mechanism is also reserved. When the sleep counter is overflow, the FRQ
will also be wakeup. The FSM control is illustrated in Fig 3‑30.

**Request Sleep Condition**: Same addr/EO request that is flushed
because of hazard with requests reside in BEC.

**Request Wakeup Condition**: BEC requests that cause hazard its
transaction flow is over.

![[]{#_Ref54776459 .anchor}Fig 3‑30 FRQ FSM with
Sleep](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image33.emf)

### Flush Control

Flush control is used to receive software flush and power flush request
and generate flush package to do L3/SF setway flush, it FSM is
illustrated below.

![[]{#_Toc225501361 .anchor}Fig 3‑36 Flush control
FSM](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image34.emf)

Flush control is embedded in the CFE, and all CFRQS buffers are shared
for flush package and core package. So flush package and core package
will compete the CFRQs resource, because the resources of the CFRQ
buffers are limited, so we need to protect both flush flit and core flit
from starvation.

For core package:

During flushing, we do not want the flush request to occupy all the CFRQ
buffers and cause the core request to fail to down from ring for a long
time, so we just monitor the CFRQs usage of flush package. If the CFRQs
usage of flush package has over flow, so the new returned credit will
allocate to core request.

For flush package:

It has a timeout counter to protect flush package, if this counter is
saturated and the CFRQs usage of flush package has not over flow, so
when there is CFRQ credit return, this CFRQ buffer will be occupied by
flush package.

**It should be noted that:**

For TAG power flush, an ACK response is returned only after all
flush-related requests processes in the brqs, cfrqs and dabs are
completed.

For SF power flush, an ACK response is returned only after all
flush-related requests processes in the brqs, cfrqs, and bibs are
completed.

Software tag/sf flush can return ACK only after all flush-related
requests processes in the brqs, cfrqs are completed.

## Backend Control

The Backend Control includes BRQ and BDQ. BRQ takes the responsibility
of tracking the life time of all serialized requests. BDQ is the inner
data-buffer for the on-the-fly data, which is implemented by SRAM to
save power and area.

### BRQ FSM

Each BRQ entry is tracking a specific request which is serialized. The
major function of BRQ is completed through several FSMs.

Tab 3‑8 lists the state of main FSM of BRQ, the corresponding transition
is presented in Fig 3‑37. The reset main state of BRQ is IDLE. A
dedicate BRQ entry is allocated at T1 without triggering the state of
BRQ. If the corresponding request is serialized BRQ without hazard, it
will trigger the main state from IDLE to T4GNT. In most scenarios, after
T4GNT, the main state will go to WAIT state to wait for other conditions
met, such as waiting for TQ/TR/TS state to be idle. It depends on
specific flows of different requests. After all the waiting conditions
are met, the main state will go to TAGREQ if another pass on pipeline is
needed. The TAGREQ will track the lifetime of the current request during
arbitration and on pipe. After all the operations are finished, the main
state will go to TKNREL to release the current resource token to the
token management module and return to IDLE state. The specific state of
2ND is for second cache line needed for ATOMIC and WUPTL, which needs
two cache lines in one request. After the ALU operation is finished,
this entry can be released.

  -----------------------------------------------------------------------
  State          Description
  -------------- --------------------------------------------------------
  IDLE           

  T4GNT          The corresponding request is at T4, allocate to BRQ or
                 replay

  WAIT           Wait for other conditions, such as TQ/TR/TS state etc.

  TAGREQ (T0-T3) The corresponding request is waiting arbitration or at
                 T0\~T3

  2^ND^          The current request is for the 2^nd^ cache line, for
                 ATOMIC/WUPTL

  TKNREL         Release resource token
  -----------------------------------------------------------------------

  : []{#_Ref54620476 .anchor}Tab 3‑8 Main FSM State

![[]{#_Ref54621345 .anchor}Fig 3‑37 Main State
Transition](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image35.png){width="4.457216754155731in"
height="2.661948818897638in"}

The TQ FSM in BRQ is to track the process of sending a request to master
accordingly. Tab 3‑9 lists the states of TQ FSM, the corresponding state
transition is presented in Fig 3‑38. The TQ state is active after T4
allocation only when sending a request to CS is needed for current
request. If the request is performance critical, the request has already
been sent on pipeline, the TQ state will directly go to SENT state to
wait for response or data. Otherwise, the TQ state will go to SEND state
to set the TQ request of the current request and wait for arbitration.
After arbitration is successful, it will then go to SENT. If the request
is retried, master interface takes the responsibility to merge the retry
and p-grant together and send it to the BRQ. If MRB is full, MRB will
trigger the inner retry flow to pipeline using RetryAck response. When
MRB is deallocated, MRB will issue a PGRNT to pipeline. During this
period, BRQ stays in the WAIT_PCRD state. There are some special
scenarios that whether sending a tq request or not is determined after
the snoop response is received. The TQ state will go to WAIT under this
scenario, after the snoop response is valid, it will go to SEND or IDLE
accordingly.

  -----------------------------------------------------------------------
  State          Description
  -------------- --------------------------------------------------------
  IDLE           

  WAIT           Wait to send request after the waiting conditions are
                 met

  SEND           Schedule request to CS, waiting for arbitration

  SEND_NEXT      Schedule request to CS, waiting for arbitration, retried
                 request

  SENT           Sending arbitration is successful, wait for resp/data

  UPDES          When READ merges with the existed PF, send UPDES to
                 master

  WAIT_PCRD      Wait for the PGRNT
  -----------------------------------------------------------------------

  : []{#_Ref54626462 .anchor}Tab 3‑9 TQ FSM State

![[]{#_Ref54626519 .anchor}Fig 3‑38 TQ FSM State
Transition](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image36.emf)

The TS FSM is to track the process of sending snoops to up-stream
accordingly. Tab 3‑10 lists the states of TS FSM, the corresponding
state transition is presented in Fig 3‑39. The TS state is active after
T4 allocation only when sending a snoop to CS is needed for current
request. If the snoop request has been sent on pipeline, the TS state
will go to SENT or WAIT state according to whether another snoop may be
needed in the future. For example, if a SnpNotSharedDirty cannot get the
required data from the snoopee, SnpMakeInvalid is needed to send to
up-stream before sending ReadNotSharedDirty to down-stream. If the first
snoop request has already been sent on pipeline, the FSM will go to SEND
to schedule a snoop request out and wait for arbitration. After
arbitration, it will go to WAIT or SENT according to whether another
snoop is needed. After the waiting conditions is met, the FSM will go to
SEND_DLYED or IDLE accordingly. The FSM state will go to IDLE after all
the outstanding snoops receive their response/data.

  -----------------------------------------------------------------------
  State          Description
  -------------- --------------------------------------------------------
  IDLE           

  WAIT           Wait to send snoop after the waiting conditions are met

  SEND           Schedule snoop to CS, waiting for arbitration

  SEND_DLYED     Schedule snoop to CS, waiting for arbitration (snoops
                 when the conditions are met)

  SENT           Sending arbitration is successful, wait for snoop
                 response/data
  -----------------------------------------------------------------------

  : []{#_Ref54634535 .anchor}Tab 3‑10 TS FSM State

![[]{#_Ref54634707 .anchor}Fig 3‑39 TS FSM State
Transition](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image37.emf)

### Bram Write Arbitration

BRQ is the serialized requests tracking queue, and the Bram is the ram
based data buffer which is bind to each BRQ respectively. Since the
memory has port confliction, we divide the Bram into two banks in each
home pipe, each bank is a TP ram. For each bank in each home pipe,
several sources will access the write port, an arbitration is presented
here, as Fig 3‑40. Request from dmemctl should have the highest
priority. On one hand, the lifetime of DAB should be ensured to reduce
the resources of DAB entries. On the other hand, making the dmemctl as
the highest priority avoids the replaying of accessing data memory.

Data from ring is output from MGB inside CS. To cover the path latency
from MGB to input port of Bram, we have data buffer and skid buffer
behaving as a temporary buffer, in which skid buffer can be bypassed.

![[]{#_Ref61249616 .anchor}Fig 3‑40 Bram Write
Arbitration](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image38.emf)

### Bram Read Arbitration

The similar scenario happens to Bram read arbitration, as illustrated in
Fig 3‑41. The request from dmemctl is also placed as the highest
priority. For the requests coming from each BRQs, it means that the
respective BRQ want to send the data inside backend buffer to outside
the L3Cache. It should be firstly picked from all the BRQs. To make
timing closure, we use a precise pend from each BRQ to do the
arbitration, at B0. After reg the arbitration result, the real valid and
payload comes out and selected by the mux. The address information will
be routed to the memory input as well, at B1. At B2, data comes out from
Bram. It will be routed directly to the dmemctl if the request is from
dmemctl. If it is not, it will be pushed to bram_rbuf at B3. At the same
time, the TD-Merge will receive a valid from BEC to do the arbitration
between BEC and dmemctl. If BEC is picked, the bram_rbuf will be
de-allocated and available for another output data from Bram.

To make the Bram timing closure, which is always critical path in our
design. The ECC check and repair is done after the data is registered in
bram_rbuf, and the original data will be speculatively passed to the
TD-merge with a kill signal. The error original data will be canceled at
SPB in CS before it is sent to ring finally. After ECC repair, the
corrected data will be updated to the bram_rbuf again. This will
definitely block the scheduling of reading bram, but is should be
ignored since the ECC happens in rare cases.

![[]{#_Ref61251577 .anchor}Fig 3‑41 Bram Read
Arbitration](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image39.emf)

## Mixed Data Path {#mixed-data-path .level-2}

CSU is going to be used as the share L2 cache for the middle cores, and
share L3 cache for big core. At the same time, CSU needs to talk to SoC.
The requirement of data bus width is different from different agent. It
means that we have to support both 64B and 32B data width at the same
time. To reduce the design complexity, the internal data path is
designed for 64B data width.

BRAM is the only receiver for 32B data source. The upper and lower bank
of BRAM can be written respectively. DRAM only receives 64B data from
BRAM.

CSU is going to send out data to upstream and downstream only after 64B
of data is ready. For DMEM, there is no access replay scheme. Besides,
the lifetime of DAB should be guaranteed otherwise it will block the
whole pipeline. Therefore, the rdata should be consumed timely to avoid
overwritten by the consecutive load. To make sure the interval between
fill wakeup and fill data fixed, there is 4 cycles opportunity for the
data to be consumed by the target. Otherwise, the data will be written
into BRAM. Fig 3‑42 describes the pipeline. Since the data just follows
the arbitration result of wakeup, the wakeup indication can hold for a
window of 4 cycles for arbitration, corresponding to the multicycle
configuration of the DMEM. If the refill target is 32B width, once a
fill wakeup is successful, it takes 2 cycles for the data to refill. The
adjacent slot is occupied. As shown in Fig 3‑43, the FW shadow means
blocking the next arbitration. If the two 32B data cannot be refilled in
4 cycles, the access multicycle, the two 32B data will be written to
BRAM without blocking.

![[]{#_Ref111483626 .anchor}Fig 3‑42 fill wakeup and fill data pipeline
for 64B data
channel](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image40.png){width="3.3386581364829397in"
height="5.203001968503937in"}

![[]{#_Ref111483913 .anchor}Fig 3‑43 fill wakeup and fill data pipeline
for 32B data
channel](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image41.png){width="3.245287620297463in"
height="4.075655074365704in"}

## Master Interface

### Feature List

Two master ports which support CHI issue E are deployed to access next
cache or main memory in CSU subsystem. Tab 3‑11 shows the major
properties together with the requirement of SoC interconnection. Tab
lists the basic capability corresponding to the master port.

  -------------------------------------------------------------------------------
  CHI property               Supported by the CSU       Interconnect support
                                                        required
  -------------------------- -------------------------- -------------------------
  Atomic_Transactions        YES if BROADCASTATOMIC is  YES if BROADCASTATOMIC is
                             HIGH                       HIGH

  Cache_Stash_Transactions   YES                        YES

  Direct_Memory_Transfer     YES                        YES

  Direct_Cache_Transfer      YES                        OPTIONAL

  Data_Poison                YES if RAS enabled         OPTIONAL

  CCF_Wrap_Order             NO                         NO

  Barrier_Transactions       NO                         NO

  CleanSharedPersist         YES if BROADCASTPERSIST IS YES if BROADCASTPERSIST
                             HIGH                       is HIGH
  -------------------------------------------------------------------------------

  : []{#_Ref54079460 .anchor}Tab 3‑11 Major Properties of Master
  Interface

  ------------------------------------------------------------------------
  Attribute             Value   Comment
  --------------------- ------- ------------------------------------------
  REQ_addr Width        36      If there is a core that has PA width are
                                40, 44, 48 or 52 bits, then this value is
                                48 or 52

  NodeID Width          11      

  Data Width            256     

  Write issuing         124     depends on the number of backend queue and
  capability                    pipe number, maximum 124 ((32-1)\*4),
                                *TBD*

  Read issuing          124     depends on the number of backend queue and
  capability                    pipe number, maximum 124 ((32-1)\*4),
                                *TBD*

  Exclusive hardware    16      Number of hardware threads, depends on the
  access thread                 cores, *TBD*
  capability                    

  Snoop acceptance      256     If support DCT, there is a constraint in
  capability                    snoop transactions. If there are snoops
                                outstanding from 15 different other
                                components in the system, then any snoop
                                from a 16th or further component will not
                                be accepted

  Non-sync SnpDVM       4       
  acceptance capability         

  SnpDVMSync acceptance 1       
  capability                    
  ------------------------------------------------------------------------

### Sturcture

![[]{#_Ref54081980 .anchor}Fig 3‑44 Master Interface
Overview](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image42.png){width="6.69375in"
height="3.140277777777778in"}

The major modules of master interface are shown in Fig 3‑44. Each
module's responsibility is described below.

- Link module, takes the responsibility to active or de-active the CHI
  interface connected with the externnal interconnection.

- PMU module, takes the responsibility to count the events related to
  master access.

- MRB module, takes the responsibility to generate the chi txreq.txnid
  of the normal transaction (except the DVM op and the prefetchTgt), and
  record the original info, like nodeid and txnid of request cpu, and in
  some case, forward the read data or received response rsp to cpu
  directly from master interface.

- Txreq module, takes the responsibility to convert the exp_mst_txreq
  flits received from the internal ring bus to the standard chi txreq
  flits.

- Txdat module, takes the responsibility to convert the exp_mst_txdat
  flits received from the internal ring bus to the standard chi txdat
  flits.

- Txrsp module, takes the responsibility to convert the exp_mst_txrsp
  flits received from the internal ring bus to the standard chi txrsp
  flits.

- RxSnp module, takes the responsibility to convert the standard chi
  rxsnp flits to the internal mst_exp_rxsnp flits sent to the internal
  ring bus.

- Rxrsp module, takes the responsibility to convert the standard chi
  rxrsp flits to the internal mst_exp_rxrsp flits sent to the internal
  ring bus.

- Rxdat module, takes the responsibility to convert the standard chi
  rxdat flits to the internal mst_exp_rxdat flits sent to the internal
  ring bus.

The major function of master interface is to transfer the flits from the
internal ring bus to the standard chi txflits and vice versa. Fig 3‑45
illustrates the detailed microarchitecture.

- There have six modules to process the transaction transferring from
  the exp flit to chi flit and vice versa.

- The mst_exp_rxrsp has two interface to route the received normal CHI
  response, RespSepData which generated from rxdat module when
  forwarding the first beat data directly to cpu, AllDatSent which
  generated from rxdat module when forwarding the last beat data
  directly to cpu, REGACTION which is generated to access master
  registers. The responses is routed to interface 0 when the target
  sub-node-id is even, to interface 1 when the target sub-node-id is
  odd.

- The u_rxsnp has the bypass path to u_txrsp to forward the necessary
  info of snoop transactions which sent to the wrong master port, such
  as SnpDVMop sent to master 1. The u_txrsp will generate the response
  using the forwarded info, like txnid, tgtid and srcid.

- The u_rxrsp has a buffer named retry_buf to track the retried
  transaction. When a Retryack is received, it will be recorded in
  retry_buf instead of sending to specific pipeline .If a retried
  transaction has received both Retryack and PcrdGrant, a
  RetryackWithPcrdGrant response is generated and sent to pipeline.

![[]{#_Ref54083900 .anchor}Fig 3‑45 Structure of Each Channel's
transfer](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image43.emf)

### MRB

## CPU Interface

### CPU Slave

As shown in Fig 3‑46, the CPU slave consists of the following six
modules, which is located between the ring and the int_sys (CPU south
bridge). Each module's responsibility is described below.

1)  rsp_div

> The rsp_div module takes responsibility to receive the packets from
> txrsp1 channel of ring and determines whether the packet is related to
> the power management. If the packet is related to the power
> management, it will be sent to the link module, otherwise it will be
> sent to the rxrsp1 channel of int_sys.

2)  link

> The link module takes responsibility to parse the packets related to
> the power management and send allow_req and slc_pwr_stat signals to
> the txreq channel of int_sys. Besides, the link module is responsible
> for sending the power management acknowledge packet to ring.

3)  rxsnp_ctl

> The rxsnp_ctl module takes responsibility to distribute the snoop
> packets from the ring. When the coherency between the ring and int_sys
> is enabled, the snoop packets will be sent to the rxsnp channel of the
> int_sys. When the coherency is disable, the snoop packets will be
> returned to the ring through txrsp 0 channel of the ring. Besides, it
> is responsible for counting the snoop requests. It\'s worth noting
> that the counter is incremented by one for DVM snoop requests after
> both DVM snoop requests are collected.

4)  txrsp0_arb

> There is an arbiter in the txrsp0_arb module which takes
> responsibility to select one packet of the packet from the txrsp
> channel of the int_sys and the packet from the rxsnp channel of the
> ring and send it to the ring. If the txrsp0_arb module doesn't have
> the credits from the ring, the packet will be pushbacked in the fifo
> in the txrsp0_arb module.

5)  sysco_cnt

> The sysco_cnt module takes responsibility to identify and count the
> packets related to snoop request of txrsp and txdat channel of the
> int_sys.

6)  sysco_ctl

> The sysco_ctl module takes responsibility to enable or disable the
> coherency between the ring and the int_sys.

![[]{#_Ref70511190 .anchor}Fig 3‑46 Structure of CPU
slave](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image44.emf)

### Asyn_bridge CHI interface

1.  TX Direction

[]{#_Toc225501372 .anchor}Fig 3‑47 Structure of TX CHI

The asynchronous bridges that connect L2 and L3, including the north
bridge and south bridge, process cross-clock domain data flows through
the asynchronous FIFO and use the CHI protocol. The asynchronous bridge
has two directions: TX and RX. TX direction includes three channels:
REQ, RSP, and DAT, and RX direction includes three channels: SNP, RSP,
and DAT.

The microstructure design of the three channels in the TX direction is
the same. The difference is that the FIFO depth is different. As shown
in the preceding figure, the chi_in submodule receives data streams from
L2, and the tx submodule write data streams in the asynchronous FIFO.
The rx submodule is responsible for read data from the asynchronous
FIFO, and the chi_out submodule is responsible for sending the read data
from the asynchronous FIFO to the ring.

FIFO depth: REQ 6, DAT 6, RSP 3.

2.  RX Direction

[]{#_Toc225501373 .anchor}Fig 3‑48 Structure of RX CHI

In the RX direction, there are three channels: SNP, RSP, and DAT. The
microstructure design of the three channels in the RX direction is the
same. The difference lies in the FIFO depth. As shown in the preceding
figure, the chi_in submodule receives data streams from the ring, and
the tx submodule writes data streams to the asynchronous FIFO. The rx
submodule is responsible for read data from the asynchronous FIFO, and
the chi_out submodule is responsible for sending the read data from the
asynchronous FIFO to L2.

FIFO depth: SNP 3, DAT 6, RSP 6.

# Feature

## Allocation Policy {#allocation-policy .level-2}

The allocation policy for T direction is NINE, toward inclusive in most
cases, but not strict. Evictions from CSU does not back-invalid L1,
store miss does not allocate in L2.

1.  **NINE**

When core has no level 2 cache, the allocation policy is toward
inclusive as following. The clean eviction will not send data.

- Data load: miss allocate, hit maintain.

- Data store: miss non-allocate, hit de-allocate.

- Instruction/ptw: miss allocate, hit maintain.

- Pre-fetch L1: miss allocate hit maintain

- Pre-fetch L2: miss allocate, hit drop.

## Alias {#alias .level-2}

If CSU is used as the share L2 Cache for middle cores, as described in
HLC, CSU takes the responsibility to cover the alias issue, which is
caused by VIPT L1D. The request issued from core may get a copy inside
L1D. CSU needs to send a snoop to the requester itself according to the
snoop filter. Fig 4‑1 shows the corresponding snoop type for different
request type.

![[]{#_Ref111570913 .anchor}Fig 4‑1 Alias
Handling](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image47.png){width="5.5487718722659665in"
height="2.4367629046369204in"}

For load request, RD-S, RD-M, RC, RO, because of alias, core send out a
false miss. The alias snoop is sent to core according to the snoop
filter lookup. Since the snoop is based on PA, LSU will look up 16 ways
at the same time. The data in snoop response will be given back to L1D
and written into another index. A data movement happens through snoop.

For write request in L1D, MRU is only sent in S state of L1D. Therefore,
alias does not happen here. For streaming write, the whole cache line is
going to be changed, so PTL request is not used currently. Besides, L1
will not allocate this cache line when streaming write is triggered.
Snoop invalid is used to directly invalid the data in L1D. Only after
serialization, DBID can be given back together with the NoAlias/Alias
indication, which is not compatible with the CHI definition here. In
streaming write flow, STL bypass is not enabled, LSU needs to block the
consecutive load before CSU returns the message of alias or not to avoid
using the stale data in L1D.

Alias handling also happens when dealing with CMO request.
SnoopCleanShared and SnoopCleanInvalid is sent to core according to the
CMO type. The alias indication returns back with the early comp message
after serialization in CSU. The alias indication either returns back
with the comp message or with an alias snoop.

The initial state of cache state to send a request should take alias
into consideration, which is beyond the scope of the definition of CHI
protocol. Fig 4‑2 lists all the scenarios of cache state transition
corresponding to the current design scope.

![[]{#_Ref112074409 .anchor}Fig 4‑2 Cache State Transition with Alias
handling](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image48.png){width="6.69375in"
height="4.627083333333333in"}

Since alias does not cost so much logic, CSU is going to support alias
handling all the time regardless of the core connected for
simplification.

## Keep the Order {#keep-the-order .level-2}

Lsu could send the same address requests and delete the read receipt
from keeping order, so HC need keep the order of receiving requests from
core.

The order needs are: the same cacheable address requests from the same
core; the same request order address requests from the same lpid; all
endpoint order requests from the same lpid.

### The Order in Xbar

Since the linklist is used in xbar, the xbar already supports the
function of keeping the same order with the receiving order.

### The Order in Home

The order will be checked before requests enqueue BRQ, order needs
request from cfrq will check if there are older order needs requests in
cfrq when getting on pipeline, if so, the younger request will be
flushed back to cfrq the keep the order.

# Flow

This chapter highlights the flows specific in different design. When CSU
is used as L2Cache or L3Cache, some flows are different. Some specific
flow is described below.

## Streaming

The interaction flow of streaming write without alias is illustrated in
Fig 5‑1. LSU send WRNT to BIU. Before sending out the request to CSU,
BIU increase the counter and mark color on the request. After
serialization on CSU pipeline, CSU responds DBID with noAlias and grant
indication to LSU, which is packed in one response. After receiving the
response, LSU can send out the WRDATA and de-allocate the corresponding
request buffer. Before receiving the response, LSU should block the load
request with same PA to avoid using the stale data in L1D. When the
WRDATA is received by CSU, a Comp response should be returned with
color. BIU should take this response to decrease the counter. Therefore,
LSU can de-allocate the buffer without waiting for the completion of the
entire flow.

![[]{#_Ref112077921 .anchor}Fig 5‑1 WRNT without
Alias](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image49.emf)

For the WRNT with alias flow, the alias indication is also returned with
the DBID response. Besides of that, a snoop should be sent to LSU to
invalid the data in L1D (WRNT-Full). To make LSU to release the load
blocking, the snoop should carry the txnid of the WRNT. Only after the
snoop response is sent, LSU can de-allocate the entry of the WRNT. LSU
use the txnid to link the snoop with the WRNT, so that the loads with
same PA can be blocked to avoid getting the stale data in L1D. The comp
response with color is also taken by BIU. The flow is shown in Fig 5‑2.

![[]{#_Ref112077939 .anchor}Fig 5‑2 WRNT with
Alias](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image50.emf)

## CMO {#cmo .level-2}

The interaction flow of VACMO miss L1 without alias is illustrated in
Fig 5‑3. When VACMO is sent to BIU, BIU takes the responsibility to mark
color and increase the corresponding counter. According to CHI protocol,
CleanShared or CleanInvalid is sent to CSU. After serialization on CSU
pipeline, CSU responds a grant response to BIU, BIU forwards this grant
to LSU. LSU will de-allocate the corresponding entry when grant is
received. When all the actions related to this VACMO is done, CSU
responds CompCMO to BIU with the original color to decrease the
corresponding counter. All the related actions including writing back
the dirty cache-line to down-stream, forwarding the VACMO to down-stream
and receiving the Comp from down-stream.

![[]{#_Ref112078276 .anchor}Fig 5‑3 VACMO miss L1 without
alias](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image51.emf)

Fig 5‑4 describes the interaction flow when VACMO miss L1 with alias.
After the request is serialized on CSU pipe, the alias snoop is sent to
LSU with the corresponding transaction id. Therefore, LSU can deallocate
the corresponding LFB. Before deallocation, the consecutive load with
same address is blocked to avoid getting the stale data in L1D. The
SnpRespData is sent to CSU. When all the actions related to this VACMO
is done, CSU responds CompCMO to BIU with the original color to decrease
the corresponding counter. All the related actions including writing
back the dirty cacheline to down-stream, forwarding the VACMO to
down-stream and receiving the Comp from down-stream.

![[]{#_Ref112078510 .anchor}Fig 5‑4 VACMO miss L1 without
alias](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image52.emf)

If VACMO hit L1D, LSU should send write combined CMO to BIU. BIU send
WriteBackCleanInvalid or WriteCleanCleanShared according to the status
in L1. When the request is serialized on CSU pipe, CSU should respond
DBID with grant to LSU. After sending out the corresponding write data,
LSU can deallocate the entry. Before that, the consecutive load with
same address is blocked to avoid getting the stale data in L1D. Also
after all the corresponding actions done in CSU and down-stream, CompCMO
with color bit is returned back to BIU. BIU will decrease the counter
accordingly. Fig 5‑5 describes the flow.

![[]{#_Ref112078657 .anchor}Fig 5‑5 VACMO hit
L1D](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image53.emf)

## Atomic {#atomic .level-2}

When CSU is used as HLC. The DBM (Dirty Bit Modify) is handled by atomic
flow.

- MMU send the ReadOnce request to CSU

- CSU returns the fill data to MMU. And MMU check whether the page
  allows to do DBM.

- MMU combine the compared data, and new data, and generate an Atomic
  CAS Far request to CSU.

- CSU uses the Atomic flow, finish the write flow inside HLC.

- MMU checks the returned data, check whether the flow is successful.

## DVM

To make the DVM handling inside core compatible, CSU helps to snoop the
request itself. So that the core can treat them in the same way. The
indicator should be given on the request through *snoop_me* field.

# Algorithm 

## LFSR 

### LFSR Overview

![[]{#_Toc225501381 .anchor}Fig 6‑1 LFSR
example](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image54.emf)

LFSR（Linear-feedback shift register）is a [shift
register](https://en.wikipedia.org/wiki/Shift_register) whose input bit
is a [linear
function](https://en.wikipedia.org/wiki/Linear#Boolean_functions) of its
previous state. The most commonly used linear function of single bits is
[exclusive-or](https://en.wikipedia.org/wiki/Exclusive-or) (XOR). Thus,
an LFSR is most often a shift register whose input bit is driven by the
XOR of some bits of the overall shift register value. commonly LFSR that
we use is Fibonacci and Galois.

**Fibonacci LFSR\-\--many-to-one**

![[]{#_Toc225501382 .anchor}Fig 6‑2 Fibonacci LFSR
example](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image55.emf)

**Galois LFSR\-\--one-to-many**

![[]{#_Toc225501383 .anchor}Fig 6‑3 Galois LFSR
example](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image56.emf)

This Version of L3 we use **Galois LFSR** to generate the pseudorandom
number that we need.

**Taps**: The bit positions that affect the next state are called the
taps.

**Feedback polynomial**: The arrangement of taps for feedback in an LFSR
can be expressed in [finite field
arithmetic](https://en.wikipedia.org/wiki/Finite_field_arithmetic) as a
[polynomial](https://en.wikipedia.org/wiki/Polynomial)
[mod](https://en.wikipedia.org/wiki/Modular_arithmetic) 2. This means
that the coefficients of the polynomial must be 1 or 0. For example, if
the taps are at the 16th, 14th, 13th and 11th bits (as shown below), the
**Feedback polynomial** is x\^{16}+x\^{14}+x\^{13}+x\^{11}+1.

![[]{#_Toc225501384 .anchor}Fig 6‑4 LFSR Feedback polynomial
example](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image57.png){width="3.2881113298337707in"
height="0.8272298775153106in"}

**Primitive polynomial**: the maximal-length Feedback polynomial. Not
all Feedback polynomial is primitive. N bits LFSR its maximal-length is
x\^N -1.

There is an N=3 BASE=2 **Galois LFSR** example below:

![[]{#_Toc225501385 .anchor}Fig 6‑5 Galois LFSR example with N=3,
BASE=2](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image58.emf)

+----------------------+-----------------------+-----------------------+
| **M ( x )**          | **R ( x )**           | **Remarks**           |
+:====================:+:=====================:+=======================+
| x\^0                 | x\^0                  | M(x) is input         |
|                      |                       | polynomial            |
|                      |                       |                       |
|                      |                       | G(X) is Feedback      |
|                      |                       | polynomial            |
|                      |                       |                       |
|                      |                       | R(X) is generate      |
|                      |                       | polynomial            |
+----------------------+-----------------------+                       |
| x\^1                 | x\^1                  |                       |
+----------------------+-----------------------+                       |
| x\^2                 | x\^2                  |                       |
+----------------------+-----------------------+                       |
| x\^3                 | x\^2+x\^0             |                       |
+----------------------+-----------------------+                       |
| x\^4                 | x\^2+x\^1+x\^0        |                       |
+----------------------+-----------------------+                       |
| x\^5                 | x\^1+x\^0             |                       |
+----------------------+-----------------------+                       |
| x\^6                 | x\^2+x\^1             |                       |
+----------------------+-----------------------+-----------------------+

: []{#_Toc225501411 .anchor}Tab 6‑1 Galois LFSR polynomial with N=3,
BASE=2

### LFSR

LFSR is to generate pseudo random numbers based on different
configurations. This LFSR has six built-in LFSR_CORE to generate
pseudo-random numbers with different BASE configurations.

The LFSR input configuration is RADIX and LFSR_LEN.at the same time,
there are 6 Prime-Data \[13,11,7,5,3,2\] that corresponds to six
built-in LFSR_CORE. RADIX input will select its Prime-Data and cause
different LFSR_CORE result. The principle of Prime-Data selection is
exact division(整除). this exact division between RADIX and
Prime-Data\[13,11,7,5,3,2\] will select its Prime-Data that we call
**BASE** and its relative **POW** that is number of times that the RADIX
and BASE are exact divided. BASE=2 's LFSR is a binary Galois LFSR and
others are Non-binary Galois LFSR.

LFSR output is the combination of POW\>0 's LFSR_CORE output with
different BASE(Prime-Data).In some cases, we hope that the LFSR output
is one-hot and the number of request is not in the range of
Prime-Data\[13,11,7,5,3,2\], so we need combine the lfsr result. For
example 12 request with RADIX=12 and LFSR_LEN=6,we combine LFSR_CORE
with BASE=2 POW=2 and BASE=3 POW=1(2\*\*2 \* 3=12) to generate a 12 bit
one-hot lfsr output.

The LFSR_CORE input configuration is BASE, POW and LFSR_LEN. These
parameter will generate several key parameter to influence the LFSR
Feedback polynomial**.** Figure below is an example with
BASE=2,POW=2,LFSR_LEN=6:

![[]{#_Toc225501386 .anchor}Fig 6‑6 Galois LFSR example with
BASE=2,POW=2,LFSR_LEN=6](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image59.emf)

**NUM_ELEMS** is the degree of the LFSR**.** (NUM_ELEMS = POW \*
LFSR_LEN)

**ELEM_W** is the number of bits for each ELEM(ELEM_W = \$clog2(BASE)).

**NUM_STAGES** is the Number of LFSR round times

(NUM_STAGES = is_interprime((BASE\*\*POW)\*\*LFSR_LEN-1,POW) ? POW :
POW+1).

**Its Feedback polynomial**: Q（t+1）=T\^k\*Q（t）

Lfsr_Stage\[stage\]\[11:7\]= lfsr_Stage\[stage-1\]\[10:6\]

Lfsr_Stage\[stage\]\[6\]= lfsr_Stage\[stage-1\]\[5\] \^
lfsr_Stage\[stage-1\]\[11\]

Lfsr_Stage\[stage\]\[5\]= lfsr_Stage\[stage-1\]\[4\]

Lfsr_Stage\[stage\]\[4\]= lfsr_Stage\[stage-1\]\[3\] \^
lfsr_Stage\[stage-1\]\[11\]

Lfsr_Stage\[stage\]\[3:2\]= lfsr_Stage\[stage-1\]\[2:1\]

Lfsr_Stage\[stage\]\[1\]= lfsr_Stage\[stage-1\]\[0\] \^
lfsr_Stage\[stage-1\]\[11\]

Lfsr_Stage\[stage\]\[0\]= lfsr_Stage\[stage-1\]\[11\]

The output of the LFSR_CORE that we use is always one-hot and is
relative with BASE, POW and NUM_STAGES. the lfsr_out is the one-hot
decoder of the element specified by NUM_STAGES, the lfsr output of
figure illustrated above is:

Lfsr_out_o\[3:0\]={ lfsr \[1:0\]\[0\]==2'd3,lfsr \[1:0\]\[0\]==2'd2,

lfsr \[1:0\]\[0\]==2'd1,lfsr \[1:0\]\[0\]==2'd0};

## Arbitration  {#arbitration .level-2}

### Arbitration solution

![[]{#_Toc225501387 .anchor}Fig 6‑7 Pipeline T0
Arbitration](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image30.emf)

Each cache slice has a request arbitrator. This L3 request arbitrator
employs an arbiter of RR+LFSR scrambled to select one request in each
cycle. As shown in figure above. CFE contains the requests from the
Cores and ACP port, SFE contains the request from master snoop. The BEC
contains requests generated by BEC while the BFE contains the request
generated from Back Invalidate Buffer.

**Arbitration algorithm (RR+LFSR Scrambled)**

This Version of L3 request arbitrator employs an arbiter of RR+LFSR
scrambled to select one request in each cycle and its arbitration
priority and direction and be dynamically changed by different
pseudorandom sequence.

  -----------------------------------------------------------------------
  Signal name                   Function description
  ----------------------------- -----------------------------------------
  enable_i                      LFSR enable

  req_i\[NUM_REQ-1:0\]          Request that wait to be arbitrated.

  elevate_i\[NUM_REQ-1:0\]      Elevates follow with request. evate_i=1's
                                request have higher priority of
                                arbitration.

  force_rand_i                  Flag to force arbitration boundary to a
                                random value with a higher probability.

  force_arb_i                   Flag to force stop arbitration.
  -----------------------------------------------------------------------

  : []{#_Toc225501412 .anchor}Tab 6‑2 Arbitration algorithm control
  signal

![[]{#_Toc225501388 .anchor}Fig 6‑8 Pipeline Arbitration
Algorithm](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image60.png){width="5.6143274278215225in"
height="4.006738845144357in"}

The pipeline Arbitration Rules is illustrated below:

1.Arbitration boundary（purple color）has the lowest arbitration
priority and is randomly controlled by LFSR.

a\) by default : Arbitration boundary is random value with a lower
probability.

b\) force_rand case: Arbitration boundary is random value with a higher
probability.

2.Arbitration direction is randomly controlled by LFSR.

a\) When arbitration direction is from right to left:

Purple color is arbitration boundary, lowest priority.

Arbitration priority in red is higher than in green.

Arbitration priority on the right is higher than on the left.

b\) When arbitration direction is from left to right:

Purple color is arbitration boundary, lowest priority.

Arbitration priority in red is higher than in green.

Arbitration priority on the left is higher than on the right.

3.Elevate =1's request have higher priority of arbitration. If there are
multiple requests with elevate is 1, these request is arbitrated
according to the preceding rules.

**Arbitration force_rand**

force_rand is controlled outside the Arbitration Algorithm. The
arbitration boundary point (as shown in the purple box in the figure)
can be affected by force_rand(Arbitration input) with a certain
probability. By default , Arbitration boundary is random value with a
lower probability. When force_rand is 1, arbitration boundary is random
value with a higher probability. When this random does not take effect,
the arbitration boundary is the value of previous beat arbitration. When
this random takes effect, the arbitration boundary is random value of
one-hot.

Force_rand is normally used to break some regular pattern on pipeline to
reduce chances of starvation.

**Force rand control condition:**

The awaked request will participate in T0 arbitration at next beat.

![[]{#_Toc225501389 .anchor}Fig 6‑9 force rand to reduce chances of
starvation](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image61.emf){width="6.69375in"
height="3.0680555555555555in"}

### LFSR Generation

![[]{#_Toc225501390 .anchor}Fig 6‑10 arbitration algorithm block
diagram](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image62.emf)

This Version of L3 we use 3 different LFSRs (Gray blocks in the figure
above) to control the request arbitration from different source. This 3
different LFSR circuits is all originated from lfsr_core

1.  **u_lfsr_dir**---RADIX=2 , LFSR_LEN=7

This LFSR circuit is used to generate 2bit random data to control the
arbitration direction and influence the priority of arbitration.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image63.emf)

[]{#_Toc225501391 .anchor}Fig 6‑11 arbitration direction LFSR structure

**Feedback polynomial**: Q（t+1）=T\^k\*Q（t）

lfsrStage\[1\]\[6:2\]= lfsrStage\[0\]\[5:1\]

lfsrStage\[1\]\[1\]= lfsrStage\[0\]\[0\] \^ lfsrStage\[0\]\[6\]

lfsrStage\[1\]\[2\]= lfsrStage\[0\]\[6\]

Lfsr_out_o\[1:0\]={ lfsr\[0\] ==1'd1,lfsr\[0\] ==1'd0}

2.  **u_lfsr_lp**---RADIX=4 , LFSR_LEN=6

This LFSR circuit is used to generate 4bit random one-hot data. This
4bit random one-hot data is used occasionally (influenced by u_lfsr\_
pick_rand) as the priority boundary point for the next beat arbitration.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image59.emf)

[]{#_Toc225501392 .anchor}Fig 6‑12 arbitration boundary LFSR structure

**Feedback polynomial**: Q（t+1）=T\^k\*Q（t）

Lfsr_Stage\[stage\]\[11:7\]= lfsr_Stage\[stage-1\]\[10:6\]

Lfsr_Stage\[stage\]\[6\]= lfsr_Stage\[stage-1\]\[5\] \^
lfsr_Stage\[stage-1\]\[11\]

Lfsr_Stage\[stage\]\[5\]= lfsr_Stage\[stage-1\]\[4\]

Lfsr_Stage\[stage\]\[4\]= lfsr_Stage\[stage-1\]\[3\] \^
lfsr_Stage\[stage-1\]\[11\]

Lfsr_Stage\[stage\]\[3:2\]= lfsr_Stage\[stage-1\]\[2:1\]

Lfsr_Stage\[stage\]\[1\]= lfsr_Stage\[stage-1\]\[0\] \^
lfsr_Stage\[stage-1\]\[11\]

Lfsr_Stage\[stage\]\[0\]= lfsr_Stage\[stage-1\]\[11\]

Lfsr_out_o\[3:0\]={ lfsr \[1:0\]\[0\]==2'd3,lfsr \[1:0\]\[0\]==2'd2,

lfsr \[1:0\]\[0\]==2'd1,lfsr \[1:0\]\[0\]==2'd0}

3.  **u_lfsr\_ pick_rand**---RADIX=13 , LFSR_LEN=3

This LFSR circuit is used to generate 13bit random
data\--pick_random\[12:0\].we use pick_random\[12:6\] or
pick_random\[12\] in different condition to determine whether to use
u_lfsr_lp random out as the priority boundary point for the next beat
arbitration.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image64.emf)

[]{#_Toc225501393 .anchor}Fig 6‑13 arbitration boundary force random
LFSR structure

**Feedback polynomial**: Q（t+1）=T\^k\*Q（t）

Lfsr_Stage\[1\]\[2\]= SUB(lfsr_Stage\[0\]\[1\]\[3:0\],
lfsr_Stage\[0\]\[2\]\[3:0\])

Lfsr_Stage\[1\]\[1\]= lfsr_Stage\[0\]\[0\]\[3:0\]

Lfsr_Stage\[1\]\[0\]= MUL2(lfsr_Stage\[0\]\[2\]\[3:0\])

Lfsr_out_o\[12:0\]={ lfsr \[0\]\[3:0\]==4'd12,lfsr \[0\]\[3:0\]==4'd11,

lfsr \[0\]\[3:0\]==4'd10,lfsr \[0\]\[3:0\]==4'd9,

lfsr\[0\]\[3:0\]==4'd8,lfsr\[0\]\[3:0\]==4'd7,

lfsr\[0\]\[3:0\]==4'd6,lfsr\[0\]\[3:0\]==4'd5,

lfsr\[0\]\[3:0\]==4'd4,lfsr\[0\]\[3:0\]==4'd3,

lfsr\[0\]\[3:0\]==4'd2,lfsr\[0\]\[3:0\]==4'd1,

lfsr\[0\]\[3:0\]==4'd0};

## Snapshot Arbitration  {#snapshot-arbitration .level-2}

Each cache slice BEC's req channel (req/rsp/dat) has a request
arbitrator. This L3 BEC request arbitrator employs a snapshot to select
one request in each cycle when there are multiple requests with same
request channel want to be executed. These requests that are not
arbitrated among multiple requests of the same channel will be recorded.
The recorded request has a higher priority in the next beat arbitration.
The detail arbitration rules is illustrated below:

1\. The arbitration priority of requests that are recorded is higher
than that of requests that are not recorded.

2\. The brq request with a lower brq entry number has a higher
arbitration priority.

3\. when the recorded request is arbitrated successfully, the
corresponding snapshot record will be cleared, and other requests that
are recorded but not arbitrated remain keep its recorded state until be
arbitrated successfully.

4\. Only all snapshot recorded requests are all arbitrated successfully,
then a new snapshot can be updated.

## Replacement

### RRIP

RRIP algorithm attaches each allocated cache line a value to represent
the re-referenced interval. Cache lines which are predicted to be
re-referenced in the near future should be reserved in cache.
Relatively, cache lines which are predicted to be re-referenced in the
distant future should be selected as the victim when new allocation is
needed. This value is referred as age.

In CSU, a 2-bit age from 0 to 3 is assigned to each cache line. Cache
lines with age 0 is predicated to be re-referenced in the distant
future, thus have highest priority to be selected as victims. Cache
lines with age 3 are preferred to be reserved vice versa.

When a cache line is allocated, the age is assigned according to the
following conditions.

- Serialise PASS: Promote the age to 3 when hit.

- Allocate evict PASS:

  - Allocation of L2 evictions.

    1.  When corrip enable, age is carried by L2 ftype field of request.

    2.  When corrip disable, if the evicting cache line is refilled to
        L2 from inside the same CPU cluster, CSU or other cores, the age
        should be 3. Otherwise, according to set-dueling.

  - Promote to 3 in following scenarios:

    1.  Readclean\|readnotsharedirty\|readonce\|atomic\*\|writeunique\*
        hit cluster

    2.  Backinvalid

  - Request from acp

    1.  Update age to 1

  - Other request

    1.  Age of 1 or 0 is assigned according to result of set-dueling

Set-dueling policy is used for allocation of the L2 evictions when
strong confidence is not present for allocating an immediate or
near-immediate re-reference age. Set dueling mechanism dedicates a few
sets of the cache to each of the two competing policies. The policy that
incurs fewer misses on the dedicated sets is used for the remaining
follower sets.

Fig 6‑14 shows the set selection of sample A and B, which belongs to
policy A and B respectively. In CSU, there are 4096 sets in total which
are divided in to 32 groups. In each group, there are 128 sets. For each
core id and thread id, 32 sets are chosen as sample A and 32 are chosen
as sample B. For group 0 to group 15, sampler sets are chosen from the
edge sets in each group, while for group 16 to group 31 they are chosen
from the middle. Fig 6‑14 just shows the sets selection result of core 0
thread 0. For sample A, the selection sets will move toward the higher
sets with an offset of {tid, coreid}, where coreid takes 4 bits and tid
takes 1. For sample B, the selection sets will move toward lower sets
with the same value.

[]{#_Ref61686116 .anchor}Fig 6‑14 Sample sets selection for set dueling
(core0, thread0)

For the sets falling in sample A, they will be assigned with age 1. The
sets in sample B will be assigned with random age. Each miss falling in
sample A increases the policy_sel counter while each miss falling in
sample B decreases the counter. The remaining follower sets will take
age 1 or random age according to this counter. The random age is
generated through a 6-bit counter. When the random age counter equals to
63, the random age takes 1, otherwise 0. This 6-bit counter is counted
when a writing request to victim ram is picked at V0.

![[]{#_Toc225501395 .anchor}Fig 6‑15 Set Dueling
Policy](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image66.emf)

If there is no way available in V4 with age 0, ways with age 1 will be
selected, and so on. After this round of selection, all the ages in the
victim ram of this index should be decreased to ensure that there is at
least one available way is of age 0. This decreasing generates an AGED
request to V0 and disables the RR arbitrator of the current slot.

# Clock and Reset

## Clock domain

The following Fig 7‑1 shows the clock structure of CSU Subsystem.

![](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image67.emf)

![[]{#_Ref53594320 .anchor}Fig 7‑1 Clock
Stucture](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image68.emf)

CSU Subsystem has the following clock inputs：

1)  SCLK

SCLK is the main clock in Namsto Subsystem.

SCLK is controlled by the SOC CRG through a Q Channel for high-level
clock gating (HCG). And SCLK is also output to the CHI asynchronous
bridge of the CPU cores.

SCLK frequency affects the L3 hit latency, therefore, it is important
for achieving good performance.

2)  PERIPHCLK

PERIPHCLK is the working clock for the peripheral logic such as timers,
sri logic, and power management logic.

PERIPHCLK does not support the Q Channel interface.

Note : Each clock above is asynchronous with each other. There are no
clock dividers and no latches in the design. The entire design is rising
edge triggered.

While there is no functional requirement for any of the clocks to have
any relationship to any of the others, the cluster is designed with the
following expectations to achieve an acceptable performance:

• The CORECLK(clock of CPU core) can be dynamically scaled to match the
performance requirements of that core.

• SCLK should run between the maximum CORECLK frequency and
approximately half of the maximum CORECLK frequency.

• SCLK can run at synchronous 1:1 or 2:1 frequencies with the external
interconnect, avoiding the need for an asynchronous bridge between them.

• PERIPHCLK contains the architectural timers, and software performance
can be impacted if reads to these registers take too long. Therefore
recommends that the PERIPHCLK frequency is at least 25% of the maximum
CORECLK frequency.

For more information, please see "*NamstoV500 CRG.vsdx*"

## Reset domain

The following Fig 7‑2 shows the reset structure of CSU Subsystem.

![[]{#_Ref53594394 .anchor}Fig 7‑2 Reset
Structure](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image69.emf)

CSU Subsystem has the following reset inputs

1)  SRESET_N

Warm-reset for SCLK clock domain. SRESET_N resets all logic of SCLK
clock domain except 'u_sb_sclk' logic and 'u_reg' logic (include RAS).

Reset event:

1.  Chip level SPORESET_N from SOC.

2.  Software triggered reset request from SOC.

3.  Chip level SRESET_N from SOC.

Reset constrains:

1.  Reset is low active.

2.  A valid reset must keep at least 16 SCLK cycles.

3.  This reset is located in SCLK domain.

Note: PPU should be reset by SRESET_N.

2)  SPORRESET_N

Cold-reset for SCLK clock domain. SPORRESET_N resets all logic (include
RAS) of SCLK clock domain.

Reset event:

1.  Software triggered reset request from SOC.

2.  Chip level SPORRESET_N from SOC.

Reset constrains:

1.  Reset is active low.

2.  A valid reset must keep at least 16 SCLK cycles.

3.  This reset is located in SCLK domain.

<!-- -->

3)  PERIPHRESET_N

Reset for the PERIPHCLK clock domain.

1.  Software triggered reset request from SOC.

2.  Chip level PERIPHRESET_N from SOC.

Reset constrains:

1.  Reset is active low.

2.  A valid reset must keep at least 16 PERIPHCLK cycles.

3.  This reset is located in PERIPHCLK domain.

<!-- -->

4)  MBISTRESET_N

MBISTRESET_N is a single cluster-wide reset signal that resets all
necessary logic in the cores and cluster for Memory Built-In Self Test
(MBIST) testing. The MBISTRESET_N signal is intended for use by an
external MBIST controller to avoid the need for it to control the reset
logic in the SoC.

1.  Please refer to MBIST test flow for detailed reset constrains.

2.  When the MBISTRESET_N is valid, both SRESET_N and SPORESET_N are
    valid.

## Reset hierarchy control and sequence

The following Fig 7‑2 shows the reset sequence of CSU Subsystem.

![[]{#_Toc225501398 .anchor}Fig 7‑3 Rest
Sequence](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image70.emf)

Reset sequence constraints,

1.  Before the reset is deasserted, must ensure that the corresponding
    clock lasts at least 16 corresponding clock cycles.

2.  There is no special requirement on which SRESET_N and SPORESET_N is
    deasserted first.

Note: Must ensure the SCLK lasts for 16 SCLK cycles before deasserting
SRESET_N or SPORESET_N.

3.  PERIPHRESET_N advised to be deasserted 100 PERIPHCLK cycles after
    SPORESET_N is deasserted.

The purpose is to make sure that clock and reset of Namsto Subsystem are
ready before Namsto Subsystem is powered on, and that some system
configuration are sampled during SRESET_N and SPORESET_N deassertion.

4.  Note that the CPU Core reset must be deasserted after SPORESET_N and
    SRESET_N are deasserted.

5.  When the MBISTRESET_N is valid, both SRESET_N and SPORESET_N are
    valid.

## PIPE Clock and Reset control

As pipe is a single harden to save power and simple backend iteration
process, so pipe have independent module to control pipe clock and
reset.

### PIPE clock

As pipe is a single harden and each pipe have a single power domain and
can be shut down when necessary, So each pipe has Link Layer and Link
credit handshake with relative ring node and each pipe has its private
reset.

Pipe reset contain system reset and pipe power on reset. System reset is
active when L3 is power on, and pipe power on reset is active when it
pipe is power on, L3 pipe's reset need combine them together. For L3
pipe's reset we need open clock several cycles to initial DFF that is
uncontrolled by reset when combined reset is active. its control timing
is illustrated below:

![[]{#_Toc85529915 .anchor}Fig 7‑4 PIPE Rest Sync and clock
management](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image71.emf)

![[]{#_Toc85529916 .anchor}Fig 7‑5 PIPE clock
structure](/Users/mac/Documents/pycircuit2/pyCircuit/designs/CSU/docs/converted/SRC-07_media/media/image72.emf)

The initiative for link active lies in the ring and the initiative for
link de-active lies in the pipe.

When any requests that reside in MGB want to go to pipe, if this pipe is
ready but link de-active, so this ring node need to do link active
handshake first, when the lint handshake is established, the pipe clock
gating will open, then ring request can be received by pipe.

When pipe need go to power down, MISC send a package of link de-active
request to pipe, pipe will do link de-active handshake with relative
ring node when all requests flow in this pipe is over. When all requests
flow except this package of link de-active request is over, then pipe
will send a ACK package of link de-active request to MISC, then all
requests flow in this pipe is over, so pipe will do link de-active
handshake with relative ring node. After this process, Link Layer
between pipe and ring will disconnect and pipe clock will be closed and
pipe can power down.

### PIPE reset

Pipe reset contain system reset and pipe power on reset. System reset is
active when L3 is power on, and pipe power on reset is active when it
pipe is power on, L3 pipe's reset need combine them together.

# Interface with CPU core

## Transaction Type

## Protocol Compliance

*All non-standard items should be illustrated here.*

### WriteEvictOrEvict

For WriteEvictOrEvict request, the legal value of field ExpCompAck is
controlled by the chicken bit (*weoe_opt_no_eca_en*). If the value of
ckb is 0, the value of ExpCompAck must be 1. If the value of ckb is 1,
the value of ExpCompAck depends on whether L2C needs to schedule a
CompAck response to L3C. If ExpCompAck equals 1, L3C won't release the
BRQ until receiving the CompAck response.

### CMO early comp

For CMO request, early comp feature is controlled by the chicken bit
(*CSU_ckb_cmo_ely_deq_en_i*). If *CSU_ckb_cmo_ely_deq_en_i* equals 1,
Comp response must be sent at T4 via BRQ and CompCmo response will be
sent when CMO has been finished. Otherwise, Comp response won't be sent
until receiving all response from upstream and downstream, if needed.

### DVM feild

Table 7-1 and Table 7-2 shows the distribution of the payload in the
DVMOp request and the distribution of the payload in the SnpDVMOp
request.

+-----------+----------------------------------+----------------------------------+
| Addr\[x\] | DVM request                      | DVM Snoop                        |
|           +-----------------+----------------+-----------------+----------------+
|           | Request         | Data           | Part 1          | Part 2         |
+===========+=================+================+=================+================+
| 0         | \-              | Num\[0\]       | \-              | \-             |
+-----------+-----------------+----------------+-----------------+----------------+
| 1         | \-              | Num\[1\]       | \-              | \-             |
+-----------+-----------------+----------------+-----------------+----------------+
| 2         | \-              | Num\[2\]       | \-              | \-             |
+-----------+-----------------+----------------+-----------------+----------------+
| 3         | 0               | Num\[3\]       | 0               | 1              |
+-----------+-----------------+----------------+-----------------+----------------+
| 4         | VA valid        | Scale\[0\]     | VA valid        | Scale\[0\]     |
+-----------+-----------------+----------------+-----------------+----------------+
| 5         | VMID valid      | Scale\[1\]     | VMID valid      | Scale\[1\]     |
+-----------+-----------------+----------------+-----------------+----------------+
| 6         | ASID valid      | TTL\[0\]       | ASID valid      | TTL\[0\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 7         | Security        | TTL\[1\]       | Security        | TTL\[1\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 8         | Security        | TG\[0\]        | Security        | TG\[0\]        |
+-----------+-----------------+----------------+-----------------+----------------+
| 9         | Exception level | TG\[1\]        | Exception level | TG\[1\]        |
+-----------+-----------------+----------------+-----------------+----------------+
| 10        | Exception level | VA\[12\]       | Exception level | VA\[12\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 11        | DVM Op type     | VA\[13\]       | DVM Op type     | VA\[13\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 12        | DVM Op type     | VA\[14\]       | DVM Op type     | VA\[14\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 13        | DVM Op type     | VA\[15\]       | DVM Op type     | VA\[15\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 21:14     | VMID\[7:0\]     | VA\[23:16\]    | VMID\[7:0\]     | VA\[23:16\]    |
+-----------+-----------------+----------------+-----------------+----------------+
| 37:22     | ASID\[15:0\]    | VA\[39:24\]    | ASID\[15:0\]    | VA\[39:24\]    |
+-----------+-----------------+----------------+-----------------+----------------+
| 38        | Stage           | VA\[40\]       | Stage           | VA\[40\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 39        | Stage           | VA\[41\]       | Stage           | VA\[41\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 40        | Leaf            | VA\[42\]       | Leaf            | VA\[42\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 41        | Range           | VA\[43\]       | VA\[46\]        | VA\[43\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 42        | Num\[4\]        | VA\[44\]       | VA\[47\]        | VA\[44\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 43        | \-              | VA\[45\]       | \-              | VA\[45\]       |
+-----------+-----------------+----------------+-----------------+----------------+
| 44        | \-              | VA\[46\]       | \-              | \-             |
+-----------+-----------------+----------------+-----------------+----------------+
| 45        | \-              | VA\[47\]       | \-              | \-             |
+-----------+-----------------+----------------+-----------------+----------------+
| 50:46     | \-              | VA\[52:48\]    | \-              | \-             |
+-----------+-----------------+----------------+-----------------+----------------+
| 51        | \-              | Leaf           | 　              | 　             |
+-----------+-----------------+----------------+-----------------+----------------+
| 52        | \-              | Range          | 　              | 　             |
+-----------+-----------------+----------------+-----------------+----------------+
| 53        | \-              | Num\[4\]       | 　              | 　             |
+-----------+-----------------+----------------+-----------------+----------------+
| 55:54     | \-              | \-             | 　              | 　             |
+-----------+-----------------+----------------+-----------------+----------------+
| 63:56     | \-              | VMID\[15:8\]   | \-              | \-             |
+-----------+-----------------+----------------+-----------------+----------------+

: Table 7-1 DVMOp and SnpDVMOp request payloads

  -----------------------------------------------------------------------------
  FwdNID\[x\]     　                　           Part 1             Part 2
  --------------- ----------------- ------------ ------------------ -----------
  0               　                　           Range              Num\[0\]

  1               　                　           VA\[42\]           Num\[1\]

  2               　                　           VA\[43\]           Num\[2\]

  3               　                　           VA\[44\]           Num\[3\]

  4               　                　           VA\[45\]           Num\[4\]

  　              　                　           　                 　

  FwdTxnID\[x\]   　                　           Part 1             Part 2

  0               　                　           Leaf               VA\[47\]

  1               　                　           VA\[46\]           　
  -----------------------------------------------------------------------------

  : Table 7-2 DVMOp and SnpDVMOp request payloads (cont.)

# Interface with SoC

## Transaction Type

## Protocol Compliance

All non-standard items should be illustrated here.

[^1]: The BIB buffer only exists when the allocation policy with
    upstream is NINE. When CSU is strictly inclusive with L1I/D, BIB is
    parameterized off.

[^2]: TD couple is separately illustrated in another section
