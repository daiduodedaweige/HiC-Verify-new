# RTL 功能分类

统计范围：当前目录直属的 646 个 SystemVerilog 文件，每个文件包含一个模块定义。verification/ 下的 4 个文件为验证层宏定义，不计作模块。

模块数按实际 module 名称计数，数字后缀变体分别统计。实例数为从 ZSystemTestTop 展开的源码层次数量（含顶层自身）；这是静态源码分析结果，未经过指定宏配置的工具 elaboration。父模块和子模块均计入，因此不代表独立验证 DUT 的数量。

| 序号 | 功能类别 | 模块数 | 顶层展开实例数 | 主要验证内容 |
|---|---|---:|---:|---|
| 1 | 系统集成与节点封装 | 13 | 36 | 节点连接、端口映射、系统复位和端到端通信 |
| 2 | 环网节点与目标路由 | 41 | 80 | 节点寻址、目标选择、环向转发和拥塞处理 |
| 3 | 通道接入与注入弹出 | 110 | 632 | 通道注入与弹出、流控、背压和报文保持 |
| 4 | 协议桥接与总线互连 | 31 | 456 | AXI/CHI/TL-UL 转换、突发拆分、事务匹配和响应返回 |
| 5 | Home通道分发与汇聚 | 15 | 164 | REQ/RSP/DAT/SNP/HPR 通道选择、分发、汇聚和握手 |
| 6 | 一致性事务与执行控制 | 24 | 2737 | 事务分配与释放、请求条件、一致性状态转换、侦听、独占和原子操作 |
| 7 | 目录管理与替换策略 | 7 | 848 | 目录查询与更新、命中判断、共享者状态和替换选择 |
| 8 | 数据缓冲与空间分配 | 17 | 202 | 缓冲分配回收、读写数据匹配、分拍组装和掩码处理 |
| 9 | 仲裁选择与优先级编码 | 95 | 4797 | 仲裁互斥、优先级、轮询公平性、条件屏蔽和编码正确性 |
| 10 | 通用队列与流水缓冲 | 146 | 4206 | 入出队顺序、满空判断、吞吐、背压和流水数据保持 |
| 11 | 存储阵列与存储器模板 | 80 | 7645 | 存储寻址、掩码写入、同步读写、双端口冲突和存储模型行为 |
| 12 | 数据校验与纠错 | 7 | 693 | 校验码生成、单比特纠错、双比特检错和错误指示 |
| 13 | 时钟复位与跨时钟域 | 32 | 3332 | 异步队列、跨域握手、复位同步、时钟门控和启动时序 |
| 14 | 地址配置与性能测试辅助 | 23 | 227 | 地址变换、配置寄存器、性能计数、随机延迟和错误响应 |
| 15 | 断言与时序验证辅助 | 5 | 848 | 延迟约束、事件间隔、多周期建立与保持检查 |
| **合计** | **15 类** | **646** | **26903** | |

## 完整模块分配

以下 ×N 表示该模块在 ZSystemTestTop 源码层次中展开后的数量；×0 表示目录保留该定义，但未被此顶层引用。

### 1. 系统集成与节点封装

`ChipWrapper`×1；`HomeCluster`×4；`HomeSlice`×16；`HomeWrapper`×4；`IoWrapperEast`×1；`IoWrapperWest`×1；`MaxiDeviceWrapper`×2；`MiscTop`×1；`PseudoSysTop`×1；`SaxiDeviceWrapper`×2；`ZCI4X8C8P2D2M0R16`×1；`ZRING4X8C8P2D2M0R16`×1；`ZSystemTestTop`×1。

### 2. 环网节点与目标路由

`RingStop__CCN_0x00`×1；`RingStop__CCN_0x02`×1；`RingStop__CCN_0x04`×1；`RingStop__CCN_0x06`×1；`RingStop__CCN_0x0F`×1；`RingStop__CCN_0x11`×1；`RingStop__CCN_0x13`×1；`RingStop__CCN_0x15`×1；`RingStop__HNX_0x01`×1；`RingStop__HNX_0x03`×1；`RingStop__HNX_0x05`×1；`RingStop__HNX_0x07`×1；`RingStop__HNX_0x0E`×1；`RingStop__HNX_0x10`×1；`RingStop__HNX_0x12`×1；`RingStop__HNX_0x14`×1；`RingStop__MRN_0x09`×1；`RingStop__PIP_0x08`×1；`RingStop__PIP_0x0C`×1；`RingStop__PIP_0x0D`×1；`RingStop__PIP_0x16`×1；`RingStop__PIP_0x17`×1；`RingStop__PIP_0x1A`×1；`RingStop__PIP_0x1B`×1；`RingStop__RNI_0x0A`×1；`RingStop__RNI_0x0B`×1；`RingStop__SNF_0x18`×1；`RingStop__SNF_0x19`×1；`TgtSelectorCCN_`×22；`TgtSelectorHNX__CCN_0x00`×2；`TgtSelectorHNX__CCN_0x02`×2；`TgtSelectorHNX__CCN_0x04`×2；`TgtSelectorHNX__CCN_0x06`×2；`TgtSelectorHNX__CCN_0x0F`×2；`TgtSelectorHNX__CCN_0x11`×2；`TgtSelectorHNX__CCN_0x13`×2；`TgtSelectorHNX__CCN_0x15`×2；`TgtSelectorHNX__MRN_0x09`×2；`TgtSelectorHNX__RNI_0x0A`×2；`TgtSelectorHNX__RNI_0x0B`×2；`TgtSelectorSNF_`×8。

### 3. 通道接入与注入弹出

`ChannelTapLHPR`×9；`ChannelTapLHPREjectOnly`×8；`ChannelTapLHPRInjectOnly`×2；`ChannelTapLHRQEjectOnly`×10；`ChannelTapLHRQInjectOnly`×8；`ChannelTapLREQ`×9；`ChannelTapLREQEjectOnly`×8；`ChannelTapLREQInjectOnly`×2；`ChannelTapSDAT`×21；`ChannelTapSRSP`×19；`ChannelTapSRSPInjectOnly`×2；`EjectBufferLHPRD4`×34；`EjectBufferLHRQD4`×20；`EjectBufferLREQD4`×34；`EjectBufferSDATD4`×42；`EjectBufferSRSPD4`×38；`InjectBuffer__CCN_0x00_LHPR`×1；`InjectBuffer__CCN_0x00_LREQ`×1；`InjectBuffer__CCN_0x00_SDAT`×1；`InjectBuffer__CCN_0x00_SRSP`×1；`InjectBuffer__CCN_0x02_LHPR`×1；`InjectBuffer__CCN_0x02_LREQ`×1；`InjectBuffer__CCN_0x02_SDAT`×1；`InjectBuffer__CCN_0x02_SRSP`×1；`InjectBuffer__CCN_0x04_LHPR`×1；`InjectBuffer__CCN_0x04_LREQ`×1；`InjectBuffer__CCN_0x04_SDAT`×1；`InjectBuffer__CCN_0x04_SRSP`×1；`InjectBuffer__CCN_0x06_LHPR`×1；`InjectBuffer__CCN_0x06_LREQ`×1；`InjectBuffer__CCN_0x06_SDAT`×1；`InjectBuffer__CCN_0x06_SRSP`×1；`InjectBuffer__CCN_0x0F_LHPR`×1；`InjectBuffer__CCN_0x0F_LREQ`×1；`InjectBuffer__CCN_0x0F_SDAT`×1；`InjectBuffer__CCN_0x0F_SRSP`×1；`InjectBuffer__CCN_0x11_LHPR`×1；`InjectBuffer__CCN_0x11_LREQ`×1；`InjectBuffer__CCN_0x11_SDAT`×1；`InjectBuffer__CCN_0x11_SRSP`×1；`InjectBuffer__CCN_0x13_LHPR`×1；`InjectBuffer__CCN_0x13_LREQ`×1；`InjectBuffer__CCN_0x13_SDAT`×1；`InjectBuffer__CCN_0x13_SRSP`×1；`InjectBuffer__CCN_0x15_LHPR`×1；`InjectBuffer__CCN_0x15_LREQ`×1；`InjectBuffer__CCN_0x15_SDAT`×1；`InjectBuffer__CCN_0x15_SRSP`×1；`InjectBuffer__HNX_0x01_LHRQ`×1；`InjectBuffer__HNX_0x01_SDAT`×1；`InjectBuffer__HNX_0x01_SRSP`×1；`InjectBuffer__HNX_0x03_LHRQ`×1；`InjectBuffer__HNX_0x03_SDAT`×1；`InjectBuffer__HNX_0x03_SRSP`×1；`InjectBuffer__HNX_0x05_LHRQ`×1；`InjectBuffer__HNX_0x05_SDAT`×1；`InjectBuffer__HNX_0x05_SRSP`×1；`InjectBuffer__HNX_0x07_LHRQ`×1；`InjectBuffer__HNX_0x07_SDAT`×1；`InjectBuffer__HNX_0x07_SRSP`×1；`InjectBuffer__HNX_0x0E_LHRQ`×1；`InjectBuffer__HNX_0x0E_SDAT`×1；`InjectBuffer__HNX_0x0E_SRSP`×1；`InjectBuffer__HNX_0x10_LHRQ`×1；`InjectBuffer__HNX_0x10_SDAT`×1；`InjectBuffer__HNX_0x10_SRSP`×1；`InjectBuffer__HNX_0x12_LHRQ`×1；`InjectBuffer__HNX_0x12_SDAT`×1；`InjectBuffer__HNX_0x12_SRSP`×1；`InjectBuffer__HNX_0x14_LHRQ`×1；`InjectBuffer__HNX_0x14_SDAT`×1；`InjectBuffer__HNX_0x14_SRSP`×1；`InjectBuffer__MRN_0x09_LHPR`×1；`InjectBuffer__MRN_0x09_LREQ`×1；`InjectBuffer__MRN_0x09_SDAT`×1；`InjectBuffer__MRN_0x09_SRSP`×1；`InjectBuffer__RNI_0x0A_LHPR`×1；`InjectBuffer__RNI_0x0A_LREQ`×1；`InjectBuffer__RNI_0x0A_SDAT`×1；`InjectBuffer__RNI_0x0A_SRSP`×1；`InjectBuffer__RNI_0x0B_LHPR`×1；`InjectBuffer__RNI_0x0B_LREQ`×1；`InjectBuffer__RNI_0x0B_SDAT`×1；`InjectBuffer__RNI_0x0B_SRSP`×1；`InjectBuffer__SNF_0x18_SDAT`×1；`InjectBuffer__SNF_0x18_SRSP`×1；`InjectBuffer__SNF_0x19_SDAT`×1；`InjectBuffer__SNF_0x19_SRSP`×1；`ScaledChannelTapLHPR`×9；`ScaledChannelTapLHPREjectOnly`×8；`ScaledChannelTapLHPRInjectOnly`×2；`ScaledChannelTapLHRQEjectOnly`×10；`ScaledChannelTapLHRQInjectOnly`×8；`ScaledChannelTapLREQ`×9；`ScaledChannelTapLREQEjectOnly`×8；`ScaledChannelTapLREQInjectOnly`×2；`ScaledChannelTapSDAT`×21；`ScaledChannelTapSRSP`×19；`ScaledChannelTapSRSPInjectOnly`×2；`SingleChannelTapLHPR`×18；`SingleChannelTapLHPREjectOnly`×16；`SingleChannelTapLHPRInjectOnly`×4；`SingleChannelTapLHRQEjectOnly`×20；`SingleChannelTapLHRQInjectOnly`×16；`SingleChannelTapLREQ`×18；`SingleChannelTapLREQEjectOnly`×16；`SingleChannelTapLREQInjectOnly`×4；`SingleChannelTapSDAT`×42；`SingleChannelTapSRSP`×38；`SingleChannelTapSRSPInjectOnly`×4。

### 4. 协议桥接与总线互连

`AXI4Buffer`×240；`Axi2Chi`×2；`AxiBridge`×2；`AxiBridgeBank`×2；`AxiBridgeCtrlMachine`×64；`AxiBuffer`×2；`AxiBufferChain`×2；`AxiBufferChain_2`×2；`AxiBuffer_2`×2；`AxiCmEnqExtraCalc`×2；`AxiDevSplit`×4；`AxiLite2TLUL`×1；`AxiLiteBridge`×1；`AxiLiteBridgeAxiTxArb`×4；`AxiLiteBridgeBank`×1；`AxiLiteBridgeBank_1`×1；`AxiLiteBridgeBank_2`×1；`AxiLiteBridgeBank_3`×1；`AxiLiteBridgeChiXbar`×1；`AxiLiteBridgeCtrlMachine`×32；`AxiMultiplexer`×1；`AxiRdSlave`×2；`AxiWrSlave`×2；`ChiBuffer`×32；`ChiBuffer_8`×8；`ChiRdMaster`×2；`ChiWrMaster`×2；`SAxiXbar`×2；`SnfAxiXbar`×2；`TLULBridge`×4；`TLULBridgeCtrlMachine`×32。

### 5. Home通道分发与汇聚

`HomeChiXbar`×4；`HomePerfTxDemux`×4；`HomeRXPortSelectorDAT`×8；`HomeRXPortSelectorHPR`×8；`HomeRXPortSelectorREQ`×8；`HomeRXPortSelectorRSP`×8；`HomeRxDemux`×8；`HomeRxMux`×16；`HomeRxMux_4`×4；`HomeTxDemux`×16；`HomeTxMux`×8；`HomeTxPortSelectorDAT`×20；`HomeTxPortSelectorREQ`×16；`HomeTxPortSelectorRSP`×20；`HomeTxPortSelectorSNP`×16。

### 6. 一致性事务与执行控制

`AtomicUnit`×32；`DBIDCtrlMachine`×256；`DataCtrlMachine`×256；`EXUWrapper`×16；`ExclusiveMonitor`×16；`ExclusiveMonitorEntry`×136；`ExclusiveMonitor_4`×1；`ExuNormal`×256；`FlushController`×16；`Frontend`×16；`IssuePtrCtrl`×40；`PoS`×16；`PosEntry`×256；`REQMSHR`×256；`ReadCtrlMachine`×256；`ReqCondLookup`×32；`ReqTransLookupOne`×256；`SnoopCtrlMachine`×256；`TaskBuffer`×16；`TaskEntryNormal`×48；`TaskEntryRVHPR`×16；`TaskIssue`×16；`TaskPipe`×16；`WriteCtrlMachine`×256。

### 7. 目录管理与替换策略

`DirectoryLLC`×16；`DirectorySF`×16；`DirectoryWrapper`×16；`PlruWayMask`×32；`Replace`×256；`ReplaceLLC`×256；`ReplaceSF`×256。

### 8. 数据缓冲与空间分配

`AxiDataBuffer`×2；`AxiDataBufferFreelist`×2；`AxiDataBufferRam`×2；`AxiDataBufferSRAMMemory`×2；`BeatStorage`×64；`ChiDataBufferFreelist`×4；`ChiDataBufferRdRam`×2；`ChiDataBufferWrRam`×2；`DataBlock`×16；`DataBuffer`×16；`DataBufferAllocReqSelector`×2；`DataBufferForRead`×2；`DataBufferForWrite`×2；`DataBuffer_1`×16；`HomeDatRam`×64；`RNIRdSRAMMemory`×2；`RNIWrSRAMMemory`×2。

### 9. 仲裁选择与优先级编码

`Arbiter2_CMTaskBdl`×256；`Arbiter2_RReqFlit`×25；`Arbiter2_ReqFlit`×256；`Arbiter3_DataTaskBdl`×256；`Arbiter3_RespFlit`×256；`ConditionVipArbiter`×2；`ConditionVipArbiter_1`×4；`ConditionVipArbiter_6`×4；`ConditionVipArbiter_7`×8；`Encoder_l1_0`×16；`Encoder_l3`×256；`Encoder_req_l0_0`×16；`Encoder_req_reply_l2`×256；`Encoder_req_wrData_l2`×256；`FastArbiter`×2；`FastArbiter_1`×2；`HnArbiter`×256；`HnArbiter_1`×256；`HnArbiter_2`×256；`HnArbiter_3`×256；`HnVipArbiter`×16；`HnVipArbiter_1`×16；`HnVipArbiter_12`×16；`HnVipArbiter_2`×16；`HnVipArbiter_3`×16；`HnVipArbiter_4`×16；`HnVipArbiter_5`×64；`HnVipArbiter_9`×48；`OneStageConditionArbiter`×8；`OneStageConditionArbiter_10`×1；`OneStageConditionArbiter_11`×1；`OneStageConditionArbiter_12`×6；`OneStageConditionArbiter_18`×8；`OneStageConditionArbiter_8`×1；`OneStageConditionArbiter_9`×1；`PriorityEncoderOneHotLow16`×416；`PriorityEncoderOneHotLow2`×128；`PriorityEncoderOneHotLow32`×48；`PriorityEncoderOneHotLow4`×64；`PriorityEncoderOneHotLow8`×194；`RRArbiter1_BFlit`×4；`RRArbiter1_RFlit`×4；`RRArbiter2_BFlit`×2；`RRArbiter2_BFlit_2`×2；`RRArbiter2_RFlit`×2；`RRArbiter2_RFlit_2`×2；`RRArbiter2_RingFlit`×21；`RRArbiter2_RingFlit_1`×34；`RRArbiter2_RingFlit_2`×19；`RRArbiter3_BFlit`×1；`RRArbiter3_RFlit`×1；`SelNto1`×2；`SelNto1_1`×4；`SelNto1_20`×2；`SelNto1_22`×1；`SelNto1_23`×1；`SelNto1_3`×2；`SelNto1_8`×4；`SelNto1_9`×8；`VipArbiter`×16；`VipArbiter_1`×16；`VipArbiter_10`×16；`VipArbiter_11`×64；`VipArbiter_15`×48；`VipArbiter_18`×16；`VipArbiter_19`×17；`VipArbiter_2`×64；`VipArbiter_23`×8；`VipArbiter_24`×4；`VipArbiter_25`×2；`VipArbiter_26`×4；`VipArbiter_28`×2；`VipArbiter_35`×8；`VipArbiter_46`×16；`VipArbiter_6`×16；`VipArbiter_7`×16；`VipArbiter_8`×16；`VipArbiter_9`×16；`VipTable`×42；`VipTable_2`×88；`VipTable_4`×38；`XsRRArbiter`×8；`XsRRArbiter_18`×8；`XsRRArbiter_19`×8；`XsRRArbiter_20`×8；`XsRRArbiter_21`×8；`XsRRArbiter_26`×44；`XsRRArbiter_28`×20；`XsRRArbiter_29`×20；`XsRRArbiter_47`×1；`XsRRArbiter_48`×1；`XsRRArbiter_49`×1；`XsRRArbiter_50`×1；`XsRRArbiter_51`×1；`XsRRArbiter_8`×40。

### 10. 通用队列与流水缓冲

`FastQueue`×42；`FastQueue_10`×22；`FastQueue_11`×21；`FastQueue_12`×21；`FastQueue_2`×68；`FastQueue_23`×8；`FastQueue_240`×96；`FastQueue_241`×96；`FastQueue_248`×86；`FastQueue_249`×82；`FastQueue_253`×40；`FastQueue_254`×32；`FastQueue_311`×2；`FastQueue_312`×2；`FastQueue_313`×8；`FastQueue_314`×8；`FastQueue_315`×4；`FastQueue_316`×11；`FastQueue_318`×12；`FastQueue_324`×4；`FastQueue_325`×4；`FastQueue_351`×4；`FastQueue_355`×4；`FastQueue_359`×1；`FastQueue_360`×5；`FastQueue_361`×5；`FastQueue_362`×5；`FastQueue_363`×4；`FastQueue_367`×4；`FastQueue_375`×1；`FastQueue_388`×2；`FastQueue_389`×2；`FastQueue_395`×2；`FastQueue_396`×2；`FastQueue_397`×2；`FastQueue_398`×2；`FastQueue_399`×8；`FastQueue_4`×38；`FastQueue_400`×2；`FastQueue_401`×2；`FastQueue_402`×2；`FastQueue_403`×2；`FastQueue_405`×8；`FastQueue_406`×8；`FastQueue_412`×4；`FastQueue_6`×20；`MergeReg`×2；`MimoQueue`×2；`Pipe3_TaskBdl`×16；`Queue14_UInt1`×11；`Queue14_UInt4`×1；`Queue1_ARFlit`×10；`Queue1_ARFlit_18`×5；`Queue1_ARFlit_19`×5；`Queue1_ARFlit_2`×8；`Queue1_ARFlit_28`×8；`Queue1_ARFlit_29`×8；`Queue1_AWFlit`×10；`Queue1_AWFlit_18`×5；`Queue1_AWFlit_19`×5；`Queue1_AWFlit_2`×8；`Queue1_AWFlit_28`×8；`Queue1_AWFlit_29`×8；`Queue1_AxiDataBufferAllocReq`×2；`Queue1_AxiDataBufferAllocReq_1`×2；`Queue1_AxiDataBufferReadReq`×6；`Queue1_AxiDataBufferTxReq`×2；`Queue1_AxiRdEntry`×2；`Queue1_AxiRdEntry_1`×2；`Queue1_AxiWrEntry`×2；`Queue1_AxiWrEntry_1`×2；`Queue1_BFlit`×4；`Queue1_BFlit_1`×4；`Queue1_BFlit_16`×2；`Queue1_BFlit_17`×2；`Queue1_BFlit_20`×8；`Queue1_BFlit_21`×8；`Queue1_BFlit_8`×4；`Queue1_BFlit_9`×4；`Queue1_DFlit`×4；`Queue1_DFlit_1`×1；`Queue1_DataFlit`×108；`Queue1_DataFlit_1`×86；`Queue1_HReqFlit`×32；`Queue1_HReqFlit_1`×32；`Queue1_RBundle`×2；`Queue1_RBundle_1`×2；`Queue1_RFlit`×4；`Queue1_RFlit_1`×4；`Queue1_RFlit_16`×2；`Queue1_RFlit_17`×2；`Queue1_RFlit_20`×4；`Queue1_RFlit_21`×4；`Queue1_RFlit_8`×4；`Queue1_RFlit_9`×4；`Queue1_RReqFlit`×115；`Queue1_RReqFlit_1`×82；`Queue1_RdDBEntry`×2；`Queue1_RdDBEntry_1`×2；`Queue1_RdDBWrEntry`×2；`Queue1_RdDBWrEntry_1`×2；`Queue1_ReqFlit`×5；`Queue1_RespDataBdl`×96；`Queue1_RespDataBdl_1`×96；`Queue1_RespDataBdl_4`×64；`Queue1_RespFlit`×104；`Queue1_RespFlit_1`×96；`Queue1_RingFlit`×147；`Queue1_RingFlit_10`×90；`Queue1_RingFlit_16`×135；`Queue1_RingFlit_18`×59；`Queue1_RingFlit_2`×63；`Queue1_RingFlit_24`×68；`Queue1_RingFlit_26`×28；`Queue1_RingFlit_8`×226；`Queue1_SnoopFlit`×40；`Queue1_SnoopFlit_1`×40；`Queue1_UInt1`×30；`Queue1_UInt2`×8；`Queue1_UInt3`×2；`Queue1_UInt4`×2；`Queue1_UInt5`×4；`Queue1_UInt8`×8；`Queue1_WFlit`×16；`Queue1_WFlit_16`×5；`Queue1_WFlit_17`×5；`Queue1_WFlit_3`×12；`Queue1_readRdDataBuffer`×6；`Queue1_readWrDataBuffer`×6；`Queue1_respDataBuffer`×4；`Queue2_AXI4BundleAR`×240；`Queue2_AXI4BundleAW`×240；`Queue2_AXI4BundleB`×240；`Queue2_AXI4BundleR`×240；`Queue2_AXI4BundleW`×240；`Queue2_WriteBeatBdl`×32；`Queue30_UInt5`×2；`Queue32_UInt32`×2；`Queue3_DataFlit`×2；`Queue3_WFlit`×2；`Queue3_respDataBuffer`×2；`Queue6_UInt1`×4；`Queue6_UInt2`×4；`Queue6_UInt3`×1；`Queue6_UInt8`×4；`SendReg`×2。

### 11. 存储阵列与存储器模板

`AXI4RAM`×2；`AxiRam`×2；`AxiRamInner`×2；`BankedDualPortSramTemplate`×2；`BankedDualPortSramTemplate_2`×2；`BankedDualPortSramTemplate_3`×2；`DualPortSramTemplate`×16；`DualPortSramTemplate_1`×16；`DualPortSramTemplate_12`×8；`DualPortSramTemplate_2`×16；`DualPortSramTemplate_3`×16；`DualPortSramTemplate_4`×4；`DualPortSramTemplate_8`×8；`GENERIC_RAM_1P1024D480W4MD`×16；`GENERIC_RAM_1P1024D64W16MD`×16；`GENERIC_RAM_1P2048D144W16MD`×16；`GENERIC_RAM_1P2048D464W4MD`×16；`GENERIC_RAM_1P8192D288W2MD`×64；`GENERIC_RAM_2P1024D15W1MD`×16；`GENERIC_RAM_2P16D256W1MD`×8；`GENERIC_RAM_2P16D256W32MD`×8；`GENERIC_RAM_2P2048D15W1MD`×16；`GENERIC_RAM_2P32D256W1MD`×4；`GENERIC_RAM_2P32D256W32MD`×32；`SRAMTemplate`×16；`SRAMTemplate_1`×16；`SRAMTemplate_12`×4；`SRAMTemplate_16`×8；`SRAMTemplate_2`×16；`SRAMTemplate_20`×8；`SRAMTemplate_3`×16；`SRAMTemplate_4`×16；`SRAMTemplate_5`×16；`SRAMTemplate_6`×16；`SRAMTemplate_7`×16；`SRAMTemplate_8`×64；`SinglePortSramTemplate`×16；`SinglePortSramTemplate_1`×16；`SinglePortSramTemplate_2`×16；`SinglePortSramTemplate_3`×16；`SparseMemA39D256M32`×2；`maskRam_64x32`×2；`ram_14x1`×11；`ram_14x4`×1；`ram_2x1`×1120；`ram_2x2`×960；`ram_2x256`×512；`ram_2x3`×960；`ram_2x32`×272；`ram_2x4`×1024；`ram_30x5`×2；`ram_32x32`×2；`ram_3x12`×10；`ram_3x2`×6；`ram_3x256`×6；`ram_3x3`×4；`ram_3x32`×6；`ram_3x4`×6；`ram_3x6`×4；`ram_6x1`×4；`ram_6x2`×4；`ram_6x3`×1；`ram_6x8`×4；`ram_DataSource_3x8`×2；`ram_addr_2x44`×480；`ram_id_2x5`×960；`ram_last_3x1`×4；`ram_len_2x8`×480；`sram_array_1p1024x480m120s1h1l2p_llc_tag`×16；`sram_array_1p1024x64m4s1h1l2p_llc_meta`×16；`sram_array_1p2048x144m9s1h1l2p_sf_meta`×16；`sram_array_1p2048x464m116s1h1l2p_sf_tag`×16；`sram_array_1p8192x288m144s2h1l2p_llc_dat`×64；`sram_array_2p1024x15m15s1h1l2p_llc_repl`×16；`sram_array_2p16x256m256s1h1l2_rni_rdb`×8；`sram_array_2p16x256m8s1h1l2_rni_wdb`×8；`sram_array_2p2048x15m15s1h1l2p_sf_repl`×16；`sram_array_2p32x256m256s1h1l2_sn_db`×4；`sram_array_2p32x256m8s1h1l2p_llc_db0`×16；`sram_array_2p32x256m8s1h1l2p_llc_db1`×16。

### 12. 数据校验与纠错

`DataCheckGen`×21；`HammingSecdedDecoder_d108_e8`×64；`HammingSecdedDecoder_d112_e8`×64；`HammingSecdedDecoder_d64_e8`×256；`HammingSecdedEncoder_d108_e8`×16；`HammingSecdedEncoder_d112_e8`×16；`HammingSecdedEncoder_d64_e8`×256。

### 13. 时钟复位与跨时钟域

`AsyncQueueSink_UInt116`×8；`AsyncQueueSink_UInt120`×16；`AsyncQueueSink_UInt416`×16；`AsyncQueueSink_UInt74`×16；`AsyncQueueSource_UInt116`×8；`AsyncQueueSource_UInt120`×16；`AsyncQueueSource_UInt416`×16；`AsyncQueueSource_UInt74`×16；`AsyncResetSynchronizerPrimitiveShiftReg_d3_i0`×896；`AsyncResetSynchronizerShiftReg_w1_d3_i0`×448；`AsyncResetSynchronizerShiftReg_w4_d3_i0`×112；`AsyncValidSync`×448；`BitSynchronizer`×24；`ChiAsyncDevSide`×8；`ChiAsyncIcnSide`×8；`ChiDecoupledSocketDevSide`×8；`ChiSocketIcnSide`×8；`ClockBuffer`×41；`ClockCrossingReg_w116`×8；`ClockCrossingReg_w120`×16；`ClockCrossingReg_w416`×16；`ClockCrossingReg_w74`×16；`ClockGate`×488；`DoubleCounterICG`×16；`DoubleCounterICG_4`×4；`MbistClockGateCell`×212；`ResetDevice`×1；`ResetGenInnerS2`×157；`ResetGenS2`×157；`SramResetGen`×48；`SramResetGen_3`×48；`SramResetGen_6`×32。

### 14. 地址配置与性能测试辅助

`AXI4Delayer`×2；`AddrModifier`×4；`AxiErrorDevice`×2；`AxiErrorDevice_2`×2；`AxiErrorDevice_4`×2；`FullAddrToSliceAddr`×32；`LFSRNoiseMaker`×8；`LFSRNoiseMaker_1`×4；`LFSRNoiseMaker_18`×4；`LFSRNoiseMaker_19`×2；`LFSRNoiseMaker_2`×4；`LFSRNoiseMaker_27`×10；`LFSRNoiseMaker_3`×8；`LFSRNoiseMaker_4`×8；`LFSRNoiseMaker_5`×8；`LFSRNoiseMaker_6`×8；`MaxPeriodFibonacciLFSR`×76；`PerfController`×4；`PerfRegister`×4；`SliceAddrToFullAddr`×32；`ZhujiangAddrConfigDevice`×1；`ZhujiangAddrConfigRegisters`×1；`ZhujiangConfigXbar`×1。

### 15. 断言与时序验证辅助

`_SVA_EventInterval2`×212；`_SVA_HoldMulticycle`×148；`_SVA_Latency2`×212；`_SVA_SetupMulticycle2`×64；`_SVA_SetupMulticycle2BYPASS_CLOCKGATE`×212。
