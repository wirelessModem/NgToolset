#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngnrgridui.py
Description:
    UI for 5GNR resource grid.
Change History:
    2018-10-28  v0.1    created.    github/zhenggao2
'''

import time
from collections import OrderedDict
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QTabWidget, QWidget, QScrollArea
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class NgNrGridUi(QDialog):
    def __init__(self, ngwin):
        super().__init__()
        self.ngwin = ngwin
        self.args = dict()
        self.initUi()

    def initUi(self):
        #TODO
        #initialize global parameters
        self.initGlobalPar()

        #-->(1) Grid settings tab
        #---->(1.1) Carrier Grid Configurations
        self.nrCarrierBandLabel = QLabel('Operating band:')
        self.nrCarrierBandComb = QComboBox()
        self.nrCarrierBandComb.addItems(list(self.nrOpBands.keys()))

        self.nrCarrierBandInfoLabel = QLabel()

        self.nrCarrierScsLabel = QLabel('Subcarrier spacing:')
        self.nrCarrierScsComb = QComboBox()

        self.nrCarrierBwLabel = QLabel('Transmission bandwidth:')
        self.nrCarrierBwComb = QComboBox()

        self.nrCarrierNumRbLabel = QLabel('N_RB(carrierBandwidth):')
        self.nrCarrierNumRbEdit = QLineEdit()
        #self.nrCarrierNumRbEdit.setFocusPolicy(Qt.NoFocus)

        self.nrMinGuardBandLabel = QLabel('Min guard band(offsetToCarrier):')
        self.nrMinGuardBandEdit = QLineEdit()

        carrierGridGrpBox = QGroupBox()
        carrierGridGrpBox.setTitle('Carrier Grid(SCS-SpecificCarrier)')
        carrierGridGrpBoxLayout = QGridLayout()
        carrierGridGrpBoxLayout.addWidget(self.nrCarrierScsLabel, 0, 0)
        carrierGridGrpBoxLayout.addWidget(self.nrCarrierScsComb, 0, 1)
        carrierGridGrpBoxLayout.addWidget(self.nrCarrierBwLabel, 1, 0)
        carrierGridGrpBoxLayout.addWidget(self.nrCarrierBwComb, 1, 1)
        carrierGridGrpBoxLayout.addWidget(self.nrCarrierNumRbLabel, 2, 0)
        carrierGridGrpBoxLayout.addWidget(self.nrCarrierNumRbEdit, 2, 1)
        carrierGridGrpBoxLayout.addWidget(self.nrMinGuardBandLabel, 3, 0)
        carrierGridGrpBoxLayout.addWidget(self.nrMinGuardBandEdit, 3, 1)
        carrierGridGrpBox.setLayout(carrierGridGrpBoxLayout)

        #---->(1.2) SSB Grid Configurations
        self.nrSsbScsLabel = QLabel('Subcarrier spacing:')
        self.nrSsbScsComb = QComboBox()

        self.nrSsbPatternLabel = QLabel('SSB pattern:')
        self.nrSsbPatternEdit = QLineEdit()
        self.nrSsbPatternEdit.setEnabled(False)

        self.nrSsbMinGuardBandScs240kLabel = QLabel('Min guard band(scs=240K):')
        self.nrSsbMinGuardBandScs240kEdit = QLineEdit()
        self.nrSsbMinGuardBandScs240kEdit.setEnabled(False)

        self.nrSsbKssbLabel = QLabel('k_SSB[0-23]:')
        self.nrSsbKssbEdit = QLineEdit()
        self.nrSsbKssbEdit.setText('0')

        self.nrSsbNCrbSsbLabel = QLabel('n_CRB_SSB:')
        self.nrSsbNCrbSsbEdit = QLineEdit()
        self.nrSsbNCrbSsbEdit.setEnabled(False)

        ssbGridGrpBox = QGroupBox()
        ssbGridGrpBox.setTitle('SSB Grid')
        ssbGridGrpBoxLayout = QGridLayout()
        ssbGridGrpBoxLayout.addWidget(self.nrSsbScsLabel, 0, 0)
        ssbGridGrpBoxLayout.addWidget(self.nrSsbScsComb, 0, 1)
        ssbGridGrpBoxLayout.addWidget(self.nrSsbPatternLabel, 1, 0)
        ssbGridGrpBoxLayout.addWidget(self.nrSsbPatternEdit, 1, 1)
        ssbGridGrpBoxLayout.addWidget(self.nrSsbMinGuardBandScs240kLabel, 2, 0)
        ssbGridGrpBoxLayout.addWidget(self.nrSsbMinGuardBandScs240kEdit, 2, 1)
        ssbGridGrpBoxLayout.addWidget(self.nrSsbKssbLabel, 3, 0)
        ssbGridGrpBoxLayout.addWidget(self.nrSsbKssbEdit, 3, 1)
        ssbGridGrpBoxLayout.addWidget(self.nrSsbNCrbSsbLabel, 4, 0)
        ssbGridGrpBoxLayout.addWidget(self.nrSsbNCrbSsbEdit, 4, 1)
        ssbGridGrpBox.setLayout(ssbGridGrpBoxLayout)

        gridLayoutResGridCfg = QGridLayout()
        gridLayoutResGridCfg.addWidget(self.nrCarrierBandLabel, 0, 0)
        gridLayoutResGridCfg.addWidget(self.nrCarrierBandComb, 0, 1)
        gridLayoutResGridCfg.addWidget(self.nrCarrierBandInfoLabel, 1, 0, 1, 2)
        gridLayoutResGridCfg.addWidget(carrierGridGrpBox, 2, 0, 1, 2)
        gridLayoutResGridCfg.addWidget(ssbGridGrpBox, 3, 0, 1, 2)

        gridCfgWidget = QWidget()
        gridCfgLayout = QVBoxLayout()
        gridCfgLayout.addLayout(gridLayoutResGridCfg)
        gridCfgLayout.addStretch()
        gridCfgWidget.setLayout(gridCfgLayout)
        
        #-->(2) SSB settings tab
        #---->(2.1) SSB configurations
        self.nrSsbInOneGrpLabel = QLabel('inOneGroup(ssb-PositionsInBurst):')
        self.nrSsbInOneGrpEdit = QLineEdit()
        self.nrSsbInOneGrpEdit.setPlaceholderText('11111111')
        
        self.nrSsbGrpPresenceLabel = QLabel('groupPresence(ssb-PositionsInBurst):')
        self.nrSsbGrpPresenceEdit = QLineEdit()
        self.nrSsbGrpPresenceEdit.setPlaceholderText('11111111')
        
        self.nrSsbPeriodicityLabel = QLabel('ssb-PeriodicityServingCell:')
        self.nrSsbPeriodicityComb = QComboBox()
        self.nrSsbPeriodicityComb.addItems(['5ms', '10ms', '20ms', '40ms', '80ms', '160ms'])
        #refer to 3GPP 38.213 4.1
        #For initial cell selection, a UE may assume that half frames with SS/PBCH blocks occur with a periodicity of 2 frames.
        self.nrSsbPeriodicityComb.setCurrentIndex(2)    #default to 20ms
        
        ssbGrpBox = QGroupBox()
        ssbGrpBox.setTitle('SSB(ServingCellConfigCommonSIB)')
        ssbGrpBoxLayout = QGridLayout()
        ssbGrpBoxLayout.addWidget(self.nrSsbInOneGrpLabel, 0, 0)
        ssbGrpBoxLayout.addWidget(self.nrSsbInOneGrpEdit, 0, 1)
        ssbGrpBoxLayout.addWidget(self.nrSsbGrpPresenceLabel, 1, 0)
        ssbGrpBoxLayout.addWidget(self.nrSsbGrpPresenceEdit, 1, 1)
        ssbGrpBoxLayout.addWidget(self.nrSsbPeriodicityLabel, 2, 0)
        ssbGrpBoxLayout.addWidget(self.nrSsbPeriodicityComb, 2, 1)
        ssbGrpBox.setLayout(ssbGrpBoxLayout)
        
        self.nrSsbPciLabel = QLabel('PCI[0-1007]:')
        self.nrSsbPciEdit = QLineEdit()
        self.nrSsbPciEdit.setText('0')
        
        #---->(2.2) MIB configurations
        self.nrMibSfnLabel = QLabel('SFN[0-1023]:')
        self.nrMibSfnEdit = QLineEdit()
        self.nrMibSfnEdit.setText('0')
        
        self.nrMibDmRsTypeAPosLabel = QLabel('dmrs-TypeA-Position:')
        self.nrMibDmRsTypeAPosComb = QComboBox()
        self.nrMibDmRsTypeAPosComb.addItems(['pos2', 'pos3'])
        self.nrMibDmRsTypeAPosComb.setCurrentIndex(0)
        
        self.nrMibScsCommonLabel = QLabel('subCarrierSpacingCommon:')
        self.nrMibScsCommonComb = QComboBox()
        self.nrMibScsCommonComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        self.nrMibScsCommonComb.setEnabled(False)
        
        self.nrMibCoreset0Label = QLabel('coresetZero(PDCCH-ConfigSIB1)[0-15]:')
        self.nrMibCoreset0Edit = QLineEdit()
        self.nrMibCoreset0Edit.setText('0')
        
        self.nrMibCss0Label = QLabel('searchSpaceZero(PDCCH-ConfigSIB1)[0-15]:')
        self.nrMibCss0Edit = QLineEdit()
        self.nrMibCss0Edit.setText('0')
        
        mibGrpBox = QGroupBox()
        mibGrpBox.setTitle('MIB')
        mibGrpBoxLayout = QGridLayout()
        mibGrpBoxLayout.addWidget(self.nrMibSfnLabel, 0, 0)
        mibGrpBoxLayout.addWidget(self.nrMibSfnEdit, 0, 1)
        mibGrpBoxLayout.addWidget(self.nrMibDmRsTypeAPosLabel, 1, 0)
        mibGrpBoxLayout.addWidget(self.nrMibDmRsTypeAPosComb, 1, 1)
        mibGrpBoxLayout.addWidget(self.nrMibScsCommonLabel, 2, 0)
        mibGrpBoxLayout.addWidget(self.nrMibScsCommonComb, 2, 1)
        mibGrpBoxLayout.addWidget(self.nrMibCoreset0Label, 3, 0)
        mibGrpBoxLayout.addWidget(self.nrMibCoreset0Edit, 3, 1)
        mibGrpBoxLayout.addWidget(self.nrMibCss0Label, 4, 0)
        mibGrpBoxLayout.addWidget(self.nrMibCss0Edit, 4, 1)
        mibGrpBox.setLayout(mibGrpBoxLayout)
        
        #---->(2.3) TDD UL/DL Configurations
        self.nrTddCfgRefScsLabel = QLabel('referenceSubcarrierSpacing:')
        self.nrTddCfgRefScsComb = QComboBox()
        self.nrTddCfgRefScsComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        self.nrTddCfgRefScsComb.setEnabled(False)
        
        self.nrTddCfgPat1PeriodLabel = QLabel('dl-UL-TransmissionPeriodicity:')
        self.nrTddCfgPat1PeriodComb = QComboBox()
        self.nrTddCfgPat1PeriodComb.addItems(['0.5ms', '0.625ms', '1ms', '1.25ms', '2ms', '2.5ms', '3ms', '4ms', '5ms', '10ms'])
        self.nrTddCfgPat1PeriodComb.setCurrentIndex(8)
        
        self.nrTddCfgPat1NumDlSlotsLabel = QLabel('nrofDownlinkSlots[0-80]:')
        self.nrTddCfgPat1NumDlSlotsEdit = QLineEdit()
        self.nrTddCfgPat1NumDlSlotsEdit.setText('3')
        
        self.nrTddCfgPat1NumDlSymbsLabel = QLabel('nrofDownlinkSymbols[0-13]:')
        self.nrTddCfgPat1NumDlSymbsEdit = QLineEdit()
        self.nrTddCfgPat1NumDlSymbsEdit.setText('10')
        
        self.nrTddCfgPat1NumUlSymbsLabel = QLabel('nrofUplinkSymbols[0-13]:')
        self.nrTddCfgPat1NumUlSymbsEdit = QLineEdit()
        self.nrTddCfgPat1NumUlSymbsEdit.setText('2')
        
        self.nrTddCfgPat1NumUlSlotsLabel = QLabel('nrofUplinkSlots[0-80]:')
        self.nrTddCfgPat1NumUlSlotsEdit = QLineEdit()
        self.nrTddCfgPat1NumUlSlotsEdit.setText('1')
        
        self.nrTddCfgPat2PeriodLabel = QLabel('dl-UL-TransmissionPeriodicity:')
        self.nrTddCfgPat2PeriodComb = QComboBox()
        self.nrTddCfgPat2PeriodComb.addItems(['not used', '0.5ms', '0.625ms', '1ms', '1.25ms', '2ms', '2.5ms', '3ms', '4ms', '5ms', '10ms'])
        self.nrTddCfgPat2PeriodComb.setCurrentIndex(0)
        
        self.nrTddCfgPat2NumDlSlotsLabel = QLabel('nrofDownlinkSlots:')
        self.nrTddCfgPat2NumDlSlotsEdit = QLineEdit()
        self.nrTddCfgPat2NumDlSlotsEdit.setPlaceholderText('0~80')
        
        self.nrTddCfgPat2NumDlSymbsLabel = QLabel('nrofDownlinkSymbols:')
        self.nrTddCfgPat2NumDlSymbsEdit = QLineEdit()
        self.nrTddCfgPat2NumDlSymbsEdit.setPlaceholderText('0~13')
        
        self.nrTddCfgPat2NumUlSymbsLabel = QLabel('nrofUplinkSymbols:')
        self.nrTddCfgPat2NumUlSymbsEdit = QLineEdit()
        self.nrTddCfgPat2NumUlSymbsEdit.setPlaceholderText('0~13')
        
        self.nrTddCfgPat2NumUlSlotsLabel = QLabel('nrofUplinkSlots:')
        self.nrTddCfgPat2NumUlSlotsEdit = QLineEdit()
        self.nrTddCfgPat2NumUlSlotsEdit.setPlaceholderText('0~80')
        
        tddCfgTabWidget = QTabWidget()
        
        tddCfgPat1Widget = QWidget()
        gridLayoutTddCfgPat1 = QGridLayout()
        gridLayoutTddCfgPat1.addWidget(self.nrTddCfgPat1PeriodLabel, 0, 0)
        gridLayoutTddCfgPat1.addWidget(self.nrTddCfgPat1PeriodComb, 0, 1)
        gridLayoutTddCfgPat1.addWidget(self.nrTddCfgPat1NumDlSlotsLabel, 1, 0)
        gridLayoutTddCfgPat1.addWidget(self.nrTddCfgPat1NumDlSlotsEdit, 1, 1)
        gridLayoutTddCfgPat1.addWidget(self.nrTddCfgPat1NumDlSymbsLabel, 2, 0)
        gridLayoutTddCfgPat1.addWidget(self.nrTddCfgPat1NumDlSymbsEdit, 2, 1)
        gridLayoutTddCfgPat1.addWidget(self.nrTddCfgPat1NumUlSymbsLabel, 3, 0)
        gridLayoutTddCfgPat1.addWidget(self.nrTddCfgPat1NumUlSymbsEdit, 3, 1)
        gridLayoutTddCfgPat1.addWidget(self.nrTddCfgPat1NumUlSlotsLabel, 4, 0)
        gridLayoutTddCfgPat1.addWidget(self.nrTddCfgPat1NumUlSlotsEdit, 4, 1)
        tddCfgPat1Widget.setLayout(gridLayoutTddCfgPat1)
        
        tddCfgPat2Widget = QWidget()
        gridLayoutTddCfgPat2 = QGridLayout()
        gridLayoutTddCfgPat2.addWidget(self.nrTddCfgPat2PeriodLabel, 0, 0)
        gridLayoutTddCfgPat2.addWidget(self.nrTddCfgPat2PeriodComb, 0, 1)
        gridLayoutTddCfgPat2.addWidget(self.nrTddCfgPat2NumDlSlotsLabel, 1, 0)
        gridLayoutTddCfgPat2.addWidget(self.nrTddCfgPat2NumDlSlotsEdit, 1, 1)
        gridLayoutTddCfgPat2.addWidget(self.nrTddCfgPat2NumDlSymbsLabel, 2, 0)
        gridLayoutTddCfgPat2.addWidget(self.nrTddCfgPat2NumDlSymbsEdit, 2, 1)
        gridLayoutTddCfgPat2.addWidget(self.nrTddCfgPat2NumUlSymbsLabel, 3, 0)
        gridLayoutTddCfgPat2.addWidget(self.nrTddCfgPat2NumUlSymbsEdit, 3, 1)
        gridLayoutTddCfgPat2.addWidget(self.nrTddCfgPat2NumUlSlotsLabel, 4, 0)
        gridLayoutTddCfgPat2.addWidget(self.nrTddCfgPat2NumUlSlotsEdit, 4, 1)
        tddCfgPat2Widget.setLayout(gridLayoutTddCfgPat2)
        
        tddCfgTabWidget.addTab(tddCfgPat1Widget, 'Pattern 1')
        tddCfgTabWidget.addTab(tddCfgPat2Widget, 'Pattern 2')
        
        tddCfgGrpBox = QGroupBox()
        tddCfgGrpBox.setTitle('TDD-UL-DL-ConfigCommon')
        tddCfgGrpBoxLayout = QVBoxLayout()
        tddCfgRefScsLayout = QHBoxLayout()
        tddCfgRefScsLayout.addWidget(self.nrTddCfgRefScsLabel)
        tddCfgRefScsLayout.addWidget(self.nrTddCfgRefScsComb)
        tddCfgRefScsLayout.addStretch()
        tddCfgGrpBoxLayout.addLayout(tddCfgRefScsLayout)
        tddCfgGrpBoxLayout.addWidget(tddCfgTabWidget)
        tddCfgGrpBox.setLayout(tddCfgGrpBoxLayout)
        
        pciLayout = QHBoxLayout()
        pciLayout.addWidget(self.nrSsbPciLabel)
        pciLayout.addWidget(self.nrSsbPciEdit)
        pciLayout.addStretch()
        
        gridLayoutSsbCfg = QGridLayout()
        gridLayoutSsbCfg.addWidget(ssbGrpBox, 0, 0, 1, 2)
        gridLayoutSsbCfg.addWidget(mibGrpBox, 1, 0, 1, 2)
        gridLayoutSsbCfg.addWidget(tddCfgGrpBox, 2, 0, 1, 2)
        
        ssbCfgWidget = QWidget()
        ssbCfgLayout = QVBoxLayout()
        ssbCfgLayout.addLayout(pciLayout)
        ssbCfgLayout.addLayout(gridLayoutSsbCfg)
        ssbCfgLayout.addStretch()
        ssbCfgWidget.setLayout(ssbCfgLayout)
        
        #-->(3) PDCCH settings tab
        #---->(3.1) CSS0 configurations
        self.nrCss0AggLevelLabel = QLabel('Aggregation level:')
        self.nrCss0AggLevelComb = QComboBox()
        self.nrCss0AggLevelComb.addItems(['4', '8', '16'])
        self.nrCss0AggLevelComb.setCurrentIndex(0)
        
        self.nrCss0NumCandidatesLabel = QLabel('Num of candidates:')
        self.nrCss0NumCandidatesComb = QComboBox()
        self.nrCss0NumCandidatesComb.addItems(['n1', 'n2', 'n4'])
        self.nrCss0NumCandidatesComb.setCurrentIndex(2)
        
        css0GrpBox = QGroupBox()
        css0GrpBox.setTitle('Type 0 CSS')
        css0GrpBoxLayout = QGridLayout()
        css0GrpBoxLayout.addWidget(self.nrCss0AggLevelLabel, 0, 0)
        css0GrpBoxLayout.addWidget(self.nrCss0AggLevelComb, 0, 1)
        css0GrpBoxLayout.addWidget(self.nrCss0NumCandidatesLabel, 1, 0)
        css0GrpBoxLayout.addWidget(self.nrCss0NumCandidatesComb, 1, 1)
        css0GrpBox.setLayout(css0GrpBoxLayout)
        
        #---->(3.2) CORESET1 configurations
        self.nrCoreset1FreqResourcesLabel = QLabel('frequencyDomainResources:')
        self.nrCoreset1FreqResourcesEdit = QLineEdit()
        self.nrCoreset1FreqResourcesEdit.setFixedWidth(52 * self.fontMetrics().width('0'))
        self.nrCoreset1FreqResourcesEdit.setPlaceholderText('00000000,00000000,00000000,00000000,00000000,00000')
        
        self.nrCoreset1DurationLabel = QLabel('duration:')
        self.nrCoreset1DurationComb = QComboBox()
        self.nrCoreset1DurationComb.addItems(['1', '2', '3'])
        self.nrCoreset1DurationComb.setCurrentIndex(0)
        
        self.nrCoreset1CceRegMapLabel = QLabel('cce-REG-MappingType:')
        self.nrCoreset1CceRegMapComb = QComboBox()
        self.nrCoreset1CceRegMapComb.addItems(['interleaved', 'nonInterleaved'])
        self.nrCoreset1CceRegMapComb.setCurrentIndex(0)
        
        self.nrCoreset1RegBundleSizeLabel = QLabel('reg-BundleSize(L):')
        self.nrCoreset1RegBundleSizeComb = QComboBox()
        self.nrCoreset1RegBundleSizeComb.addItems(['n2', 'n3', 'n6'])
        self.nrCoreset1RegBundleSizeComb.setCurrentIndex(0)
        
        self.nrCoreset1InterleaverSizeLabel = QLabel('interleaverSize(R):')
        self.nrCoreset1InterleaverSizeComb = QComboBox()
        self.nrCoreset1InterleaverSizeComb.addItems(['n2', 'n3', 'n6'])
        self.nrCoreset1InterleaverSizeComb.setCurrentIndex(0)
        
        self.nrCoreset1ShiftIndexLabel = QLabel('shiftIndex[0-274]:')
        self.nrCoreset1ShiftIndexEdit = QLineEdit()
        self.nrCoreset1ShiftIndexEdit.setText('0')
        
        self.nrCoreset1PrecoderGranularityLabel = QLabel('precoderGranularity:')
        self.nrCoreset1PrecoderGranularityComb = QComboBox()
        self.nrCoreset1PrecoderGranularityComb.addItems(['sameAsREG-bundle', 'allContiguousRBs'])
        self.nrCoreset1PrecoderGranularityComb.setCurrentIndex(0)
        
        coreset1Widget = QWidget()
        coreset1Layout = QGridLayout()
        coreset1Layout.addWidget(self.nrCoreset1FreqResourcesLabel, 0, 0)
        coreset1Layout.addWidget(self.nrCoreset1FreqResourcesEdit, 0, 1)
        coreset1Layout.addWidget(self.nrCoreset1DurationLabel, 1, 0)
        coreset1Layout.addWidget(self.nrCoreset1DurationComb, 1, 1)
        coreset1Layout.addWidget(self.nrCoreset1CceRegMapLabel, 2, 0)
        coreset1Layout.addWidget(self.nrCoreset1CceRegMapComb, 2, 1)
        coreset1Layout.addWidget(self.nrCoreset1RegBundleSizeLabel, 3, 0)
        coreset1Layout.addWidget(self.nrCoreset1RegBundleSizeComb, 3, 1)
        coreset1Layout.addWidget(self.nrCoreset1InterleaverSizeLabel, 4, 0)
        coreset1Layout.addWidget(self.nrCoreset1InterleaverSizeComb, 4, 1)
        coreset1Layout.addWidget(self.nrCoreset1ShiftIndexLabel, 5, 0)
        coreset1Layout.addWidget(self.nrCoreset1ShiftIndexEdit, 5, 1)
        coreset1Layout.addWidget(self.nrCoreset1PrecoderGranularityLabel, 6, 0)
        coreset1Layout.addWidget(self.nrCoreset1PrecoderGranularityComb, 6, 1)
        coreset1Widget.setLayout(coreset1Layout) 
        
        #---->(3.3) USS configuratons
        self.nrUssPeriodicityLabel = QLabel('monitoringSlotPeriodicity:')
        self.nrUssPeriodicityComb = QComboBox()
        self.nrUssPeriodicityComb.addItems(['sl1', 'sl2', 'sl4', 'sl5', 'sl8', 'sl10', 'sl16', 'sl20',
                                            'sl40', 'sl80', 'sl160', 'sl320', 'sl640', 'sl1280', 'sl2560'])
        self.nrUssPeriodicityComb.currentIndexChanged[int].connect(self.onUssPeriodicityCombCurrentIndexChanged)
        self.nrUssPeriodicityComb.setCurrentIndex(0)
        
        self.nrUssSlotOffsetLabel = QLabel('monitoringSlotOffset:')
        self.nrUssSlotOffsetEdit = QLineEdit()
        self.nrUssSlotOffsetEdit.setText('0')
        
        self.nrUssDurationLabel = QLabel('duration:')
        self.nrUssDurationEdit = QLineEdit()
        self.nrUssDurationEdit.setText('1')
        
        self.nrUssFirstSymbsLabel = QLabel('monitoringSymbolsWithinSlot:')
        self.nrUssFirstSymbsEdit = QLineEdit()
        self.nrUssFirstSymbsEdit.setPlaceholderText('1111111,1111111')
        
        self.nrUssAggLevelLabel = QLabel('aggregationLevel:')
        self.nrUssAggLevelComb = QComboBox()
        self.nrUssAggLevelComb.addItems(['1', '2', '4', '8', '16'])
        self.nrUssAggLevelComb.setCurrentIndex(2)
        
        self.nrUssNumCandidatesLabel = QLabel('nrofCandidates:')
        self.nrUssNumCandidatesComb = QComboBox()
        self.nrUssNumCandidatesComb.addItems(['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n8'])
        
        ussWidget = QWidget()
        ussLayout = QGridLayout()
        ussLayout.addWidget(self.nrUssPeriodicityLabel, 0, 0)
        ussLayout.addWidget(self.nrUssPeriodicityComb, 0, 1)
        ussLayout.addWidget(self.nrUssSlotOffsetLabel, 1, 0)
        ussLayout.addWidget(self.nrUssSlotOffsetEdit, 1, 1)
        ussLayout.addWidget(self.nrUssDurationLabel, 2, 0)
        ussLayout.addWidget(self.nrUssDurationEdit, 2, 1)
        ussLayout.addWidget(self.nrUssFirstSymbsLabel, 3, 0)
        ussLayout.addWidget(self.nrUssFirstSymbsEdit, 3, 1)
        ussLayout.addWidget(self.nrUssAggLevelLabel, 4, 0)
        ussLayout.addWidget(self.nrUssAggLevelComb, 4, 1)
        ussLayout.addWidget(self.nrUssNumCandidatesLabel, 5, 0)
        ussLayout.addWidget(self.nrUssNumCandidatesComb, 5, 1)
        ussWidget.setLayout(ussLayout)
        
        pdcchTabWidget = QTabWidget()
        pdcchTabWidget.addTab(coreset1Widget, 'CORESET 1')
        pdcchTabWidget.addTab(ussWidget, 'USS')
        
        #---->(3.4) DCI configurations
        #refer to 3GPP 38.321 vf30
        #Table 7.1-1: RNTI values.
        '''
        Value (hexa-decimal)	RNTI
        0                       N/A
        0001–FFEF               RA-RNTI, Temporary C-RNTI, C-RNTI, MCS-C-RNTI, CS-RNTI, TPC-PUCCH-RNTI, TPC-PUSCH-RNTI, TPC-SRS-RNTI, INT-RNTI, SFI-RNTI, and SP-CSI-RNTI
        FFF0–FFFD               Reserved
        FFFE                    P-RNTI
        FFFF                    SI-RNTI
        '''
        #DCI 1_0 with SI-RNTI for SIB1
        self.nrDci10Sib1RntiLabel = QLabel('RNTI(SI-RNTI):')
        self.nrDci10Sib1RntiEdit = QLineEdit('0xFFFF')
        self.nrDci10Sib1RntiEdit.setEnabled(False)
        
        self.nrDci10Sib1MuPdcchLabel = QLabel('u_PDCCH[0-3]:')
        self.nrDci10Sib1MuPdcchEdit = QLineEdit()
        self.nrDci10Sib1MuPdcchEdit.setEnabled(False)
        
        self.nrDci10Sib1MuPdschLabel = QLabel('u_PDSCH[0-3]:')
        self.nrDci10Sib1MuPdschEdit = QLineEdit()
        self.nrDci10Sib1MuPdschEdit.setEnabled(False)
        
        self.nrDci10Sib1TimeAllocFieldLabel = QLabel('Time domain resource assignment[0-15]:')
        self.nrDci10Sib1TimeAllocFieldEdit = QLineEdit()
        
        self.nrDci10Sib1TimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrDci10Sib1TimeAllocMappingTypeComb = QComboBox()
        self.nrDci10Sib1TimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        
        self.nrDci10Sib1TimeAllocK0Label = QLabel('K0:')
        self.nrDci10Sib1TimeAllocK0Edit = QLineEdit()
        
        self.nrDci10Sib1TimeAllocSlivLabel = QLabel('SLIV:')
        self.nrDci10Sib1TimeAllocSlivEdit = QLineEdit()
        
        self.nrDci10Sib1TimeAllocSLabel = QLabel('S(of SLIV):')
        self.nrDci10Sib1TimeAllocSEdit = QLineEdit()
        
        self.nrDci10Sib1TimeAllocLLabel = QLabel('L(of SLIV):')
        self.nrDci10Sib1TimeAllocLEdit = QLineEdit()
        
        self.nrDci10Sib1FreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrDci10Sib1FreqAllocTypeComb = QComboBox()
        self.nrDci10Sib1FreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrDci10Sib1FreqAllocTypeComb.setCurrentIndex(1)
        
        self.nrDci10Sib1FreqAllocFieldLabel = QLabel('Frequency domain resource assignment:')
        self.nrDci10Sib1FreqAllocFieldEdit = QLineEdit()
        
        self.nrDci10Sib1FreqAllocType1RbStartLabel = QLabel('RB_start(of RIV):')
        self.nrDci10Sib1FreqAllocType1RbStartEdit = QLineEdit()
        
        self.nrDci10Sib1FreqAllocType1LRbsLabel = QLabel('L_RBs(of RIV):')
        self.nrDci10Sib1FreqAllocType1LRbsEdit = QLineEdit()
        
        self.nrDci10Sib1FreqAllocType1VrbPrbMapppingTypeLabel = QLabel('VRB-to-PRB mapping type:')
        self.nrDci10Sib1FreqAllocType1VrbPrbMappingTypeComb = QComboBox()
        self.nrDci10Sib1FreqAllocType1VrbPrbMappingTypeComb.addItems(['nonInterleaved', 'interleaved'])
        self.nrDci10Sib1FreqAllocType1VrbPrbMappingTypeComb.setCurrentIndex(1)
        
        self.nrDci10Sib1FreqAllocType1BundleSizeLabel = QLabel('L(vrb-ToPRB-Interleaver):')
        self.nrDci10Sib1FreqAllocType1BundleSizeComb = QComboBox()
        self.nrDci10Sib1FreqAllocType1BundleSizeComb.addItems(['n2', 'n4'])
        self.nrDci10Sib1FreqAllocType1BundleSizeComb.setCurrentIndex(0)
        
        self.nrDci10Sib1McsLabel = QLabel('Modulation and coding scheme(CW0)[0-31]:')
        self.nrDci10Sib1McsEdit = QLineEdit()
        
        self.nrDci10Sib1TbsLabel = QLabel('Transport block size(bits):')
        self.nrDci10Sib1TbsEdit = QLineEdit()
        self.nrDci10Sib1TbsEdit.setEnabled(False)
        
        dci10Sib1TimeAllocWidget = QWidget()
        dci10Sib1TimeAllocLayout = QGridLayout()
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocFieldLabel, 0, 0)
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocFieldEdit, 0, 1)
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocMappingTypeLabel, 1, 0)
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocMappingTypeComb, 1, 1)
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocK0Label, 2, 0)
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocK0Edit, 2, 1)
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocSlivLabel, 3, 0)
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocSlivEdit, 3, 1)
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocSLabel, 4, 0)
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocSEdit, 4, 1)
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocLLabel, 5, 0)
        dci10Sib1TimeAllocLayout.addWidget(self.nrDci10Sib1TimeAllocLEdit, 5, 1)
        dci10Sib1TimeAllocWidget.setLayout(dci10Sib1TimeAllocLayout)
        
        dci10Sib1FreqAllocWidget = QWidget()
        dci10Sib1FreqAllocLayout = QGridLayout()
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocTypeLabel, 0, 0)
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocTypeComb, 0, 1)
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocFieldLabel, 1, 0)
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocFieldEdit, 1, 1)
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocType1RbStartLabel, 2, 0)
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocType1RbStartEdit, 2, 1)
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocType1LRbsLabel, 3, 0)
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocType1LRbsEdit, 3, 1)
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocType1VrbPrbMapppingTypeLabel, 4, 0)
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocType1VrbPrbMappingTypeComb, 4, 1)
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocType1BundleSizeLabel, 5, 0)
        dci10Sib1FreqAllocLayout.addWidget(self.nrDci10Sib1FreqAllocType1BundleSizeComb, 5, 1)
        dci10Sib1FreqAllocWidget.setLayout(dci10Sib1FreqAllocLayout)
        
        dci10Sib1RaTabWidget = QTabWidget()
        dci10Sib1RaTabWidget.addTab(dci10Sib1TimeAllocWidget, 'Time-domain assignment')
        dci10Sib1RaTabWidget.addTab(dci10Sib1FreqAllocWidget, 'Frequency-domain assignment')
        
        dci10Sib1Widget = QWidget()
        dci10Sib1GridLayout = QGridLayout()
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1RntiLabel, 0, 0)
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1RntiEdit, 0, 1)
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1MuPdcchLabel, 1, 0)
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1MuPdcchEdit, 1, 1)
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1MuPdschLabel, 2, 0)
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1MuPdschEdit, 2, 1)
        dci10Sib1GridLayout.addWidget(dci10Sib1RaTabWidget, 3, 0, 1, 2)
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1McsLabel, 4, 0)
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1McsEdit, 4, 1)
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1TbsLabel, 5, 0)
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1TbsEdit, 5, 1)
        dci10Sib1Layout = QVBoxLayout()
        dci10Sib1Layout.addLayout(dci10Sib1GridLayout)
        dci10Sib1Layout.addStretch()
        dci10Sib1Widget.setLayout(dci10Sib1Layout)
        
        dci10Sib1Scroll = QScrollArea()
        dci10Sib1Scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        dci10Sib1Scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        dci10Sib1Scroll.setWidgetResizable(True)
        dci10Sib1Scroll.setWidget(dci10Sib1Widget)
        
        #DCI 1_0 with RA-RNTI for Msg2(RAR)
        self.nrDci10Msg2RntiLabel = QLabel('RNTI(RA-RNTI)[0x0001-FFEF]:')
        self.nrDci10Msg2RntiEdit = QLineEdit('0x0001')
        
        self.nrDci10Msg2MuPdcchLabel = QLabel('u_PDCCH[0-3]:')
        self.nrDci10Msg2MuPdcchEdit = QLineEdit()
        self.nrDci10Msg2MuPdcchEdit.setEnabled(False)
        
        self.nrDci10Msg2MuPdschLabel = QLabel('u_PDSCH[0-3]:')
        self.nrDci10Msg2MuPdschEdit = QLineEdit()
        self.nrDci10Msg2MuPdschEdit.setEnabled(False)
        
        self.nrDci10Msg2TimeAllocFieldLabel = QLabel('Time domain resource assignment[0-15]:')
        self.nrDci10Msg2TimeAllocFieldEdit = QLineEdit()
        
        self.nrDci10Msg2TimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrDci10Msg2TimeAllocMappingTypeComb = QComboBox()
        self.nrDci10Msg2TimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        
        self.nrDci10Msg2TimeAllocK0Label = QLabel('K0:')
        self.nrDci10Msg2TimeAllocK0Edit = QLineEdit()
        
        self.nrDci10Msg2TimeAllocSlivLabel = QLabel('SLIV:')
        self.nrDci10Msg2TimeAllocSlivEdit = QLineEdit()
        
        self.nrDci10Msg2TimeAllocSLabel = QLabel('S(of SLIV):')
        self.nrDci10Msg2TimeAllocSEdit = QLineEdit()
        
        self.nrDci10Msg2TimeAllocLLabel = QLabel('L(of SLIV):')
        self.nrDci10Msg2TimeAllocLEdit = QLineEdit()
        
        self.nrDci10Msg2FreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrDci10Msg2FreqAllocTypeComb = QComboBox()
        self.nrDci10Msg2FreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrDci10Msg2FreqAllocTypeComb.setCurrentIndex(1)
        
        self.nrDci10Msg2FreqAllocFieldLabel = QLabel('Frequency domain resource assignment:')
        self.nrDci10Msg2FreqAllocFieldEdit = QLineEdit()
        
        self.nrDci10Msg2FreqAllocType1RbStartLabel = QLabel('RB_start(of RIV):')
        self.nrDci10Msg2FreqAllocType1RbStartEdit = QLineEdit()
        
        self.nrDci10Msg2FreqAllocType1LRbsLabel = QLabel('L_RBs(of RIV):')
        self.nrDci10Msg2FreqAllocType1LRbsEdit = QLineEdit()
        
        self.nrDci10Msg2FreqAllocType1VrbPrbMapppingTypeLabel = QLabel('VRB-to-PRB mapping type:')
        self.nrDci10Msg2FreqAllocType1VrbPrbMappingTypeComb = QComboBox()
        self.nrDci10Msg2FreqAllocType1VrbPrbMappingTypeComb.addItems(['nonInterleaved', 'interleaved'])
        self.nrDci10Msg2FreqAllocType1VrbPrbMappingTypeComb.setCurrentIndex(1)
        
        self.nrDci10Msg2FreqAllocType1BundleSizeLabel = QLabel('L(vrb-ToPRB-Interleaver):')
        self.nrDci10Msg2FreqAllocType1BundleSizeComb = QComboBox()
        self.nrDci10Msg2FreqAllocType1BundleSizeComb.addItems(['n2', 'n4'])
        self.nrDci10Msg2FreqAllocType1BundleSizeComb.setCurrentIndex(0)
        
        self.nrDci10Msg2McsLabel = QLabel('Modulation and coding scheme(CW0)[0-31]:')
        self.nrDci10Msg2McsEdit = QLineEdit()
        
        self.nrDci10Msg2TbScalingLabel = QLabel('TB Scaling[0-3]:')
        self.nrDci10Msg2TbScalingEdit = QLineEdit()
        
        self.nrDci10Msg2TbsLabel = QLabel('Transport block size(bits):')
        self.nrDci10Msg2TbsEdit = QLineEdit()
        self.nrDci10Msg2TbsEdit.setEnabled(False)
        
        dci10Msg2TimeAllocWidget = QWidget()
        dci10Msg2TimeAllocLayout = QGridLayout()
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocFieldLabel, 0, 0)
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocFieldEdit, 0, 1)
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocMappingTypeLabel, 1, 0)
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocMappingTypeComb, 1, 1)
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocK0Label, 2, 0)
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocK0Edit, 2, 1)
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocSlivLabel, 3, 0)
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocSlivEdit, 3, 1)
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocSLabel, 4, 0)
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocSEdit, 4, 1)
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocLLabel, 5, 0)
        dci10Msg2TimeAllocLayout.addWidget(self.nrDci10Msg2TimeAllocLEdit, 5, 1)
        dci10Msg2TimeAllocWidget.setLayout(dci10Msg2TimeAllocLayout)
        
        dci10Msg2FreqAllocWidget = QWidget()
        dci10Msg2FreqAllocLayout = QGridLayout()
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocTypeLabel, 0, 0)
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocTypeComb, 0, 1)
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocFieldLabel, 1, 0)
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocFieldEdit, 1, 1)
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocType1RbStartLabel, 2, 0)
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocType1RbStartEdit, 2, 1)
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocType1LRbsLabel, 3, 0)
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocType1LRbsEdit, 3, 1)
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocType1VrbPrbMapppingTypeLabel, 4, 0)
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocType1VrbPrbMappingTypeComb, 4, 1)
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocType1BundleSizeLabel, 5, 0)
        dci10Msg2FreqAllocLayout.addWidget(self.nrDci10Msg2FreqAllocType1BundleSizeComb, 5, 1)
        dci10Msg2FreqAllocWidget.setLayout(dci10Msg2FreqAllocLayout)
        
        dci10Msg2RaTabWidget = QTabWidget()
        dci10Msg2RaTabWidget.addTab(dci10Msg2TimeAllocWidget, 'Time-domain assignment')
        dci10Msg2RaTabWidget.addTab(dci10Msg2FreqAllocWidget, 'Frequency-domain assignment')
        
        dci10Msg2Widget = QWidget()
        dci10Msg2GridLayout = QGridLayout()
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2RntiLabel, 0, 0)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2RntiEdit, 0, 1)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2MuPdcchLabel, 1, 0)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2MuPdcchEdit, 1, 1)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2MuPdschLabel, 2, 0)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2MuPdschEdit, 2, 1)
        dci10Msg2GridLayout.addWidget(dci10Msg2RaTabWidget, 3, 0, 1, 2)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2McsLabel, 4, 0)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2McsEdit, 4, 1)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2TbScalingLabel, 5, 0)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2TbScalingEdit, 5, 1)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2TbsLabel, 6, 0)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2TbsEdit, 6, 1)
        dci10Msg2Layout = QVBoxLayout()
        dci10Msg2Layout.addLayout(dci10Msg2GridLayout)
        dci10Msg2Layout.addStretch()
        dci10Msg2Widget.setLayout(dci10Msg2Layout)
        
        dci10Msg2Scroll = QScrollArea()
        dci10Msg2Scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        dci10Msg2Scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        dci10Msg2Scroll.setWidgetResizable(True)
        dci10Msg2Scroll.setWidget(dci10Msg2Widget)
        
        #DCI 1_0 with TC-RNTI for Msg4
        self.nrDci10Msg4RntiLabel = QLabel('RNTI(TC-RNTI)[0x0001-FFEF]:')
        self.nrDci10Msg4RntiEdit = QLineEdit('0x0001')
        
        self.nrDci10Msg4MuPdcchLabel = QLabel('u_PDCCH[0-3]:')
        self.nrDci10Msg4MuPdcchEdit = QLineEdit()
        self.nrDci10Msg4MuPdcchEdit.setEnabled(False)
        
        self.nrDci10Msg4MuPdschLabel = QLabel('u_PDSCH[0-3]:')
        self.nrDci10Msg4MuPdschEdit = QLineEdit()
        self.nrDci10Msg4MuPdschEdit.setEnabled(False)
        
        self.nrDci10Msg4TimeAllocFieldLabel = QLabel('Time domain resource assignment[0-15]:')
        self.nrDci10Msg4TimeAllocFieldEdit = QLineEdit()
        
        self.nrDci10Msg4TimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrDci10Msg4TimeAllocMappingTypeComb = QComboBox()
        self.nrDci10Msg4TimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        
        self.nrDci10Msg4TimeAllocK0Label = QLabel('K0:')
        self.nrDci10Msg4TimeAllocK0Edit = QLineEdit()
        
        self.nrDci10Msg4TimeAllocSlivLabel = QLabel('SLIV:')
        self.nrDci10Msg4TimeAllocSlivEdit = QLineEdit()
        
        self.nrDci10Msg4TimeAllocSLabel = QLabel('S(of SLIV):')
        self.nrDci10Msg4TimeAllocSEdit = QLineEdit()
        
        self.nrDci10Msg4TimeAllocLLabel = QLabel('L(of SLIV):')
        self.nrDci10Msg4TimeAllocLEdit = QLineEdit()
        
        self.nrDci10Msg4FreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrDci10Msg4FreqAllocTypeComb = QComboBox()
        self.nrDci10Msg4FreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrDci10Msg4FreqAllocTypeComb.setCurrentIndex(1)
        
        self.nrDci10Msg4FreqAllocFieldLabel = QLabel('Frequency domain resource assignment:')
        self.nrDci10Msg4FreqAllocFieldEdit = QLineEdit()
        
        self.nrDci10Msg4FreqAllocType1RbStartLabel = QLabel('RB_start(of RIV):')
        self.nrDci10Msg4FreqAllocType1RbStartEdit = QLineEdit()
        
        self.nrDci10Msg4FreqAllocType1LRbsLabel = QLabel('L_RBs(of RIV):')
        self.nrDci10Msg4FreqAllocType1LRbsEdit = QLineEdit()
        
        self.nrDci10Msg4FreqAllocType1VrbPrbMapppingTypeLabel = QLabel('VRB-to-PRB mapping type:')
        self.nrDci10Msg4FreqAllocType1VrbPrbMappingTypeComb = QComboBox()
        self.nrDci10Msg4FreqAllocType1VrbPrbMappingTypeComb.addItems(['nonInterleaved', 'interleaved'])
        self.nrDci10Msg4FreqAllocType1VrbPrbMappingTypeComb.setCurrentIndex(1)
        
        self.nrDci10Msg4FreqAllocType1BundleSizeLabel = QLabel('L(vrb-ToPRB-Interleaver):')
        self.nrDci10Msg4FreqAllocType1BundleSizeComb = QComboBox()
        self.nrDci10Msg4FreqAllocType1BundleSizeComb.addItems(['n2', 'n4'])
        self.nrDci10Msg4FreqAllocType1BundleSizeComb.setCurrentIndex(0)
        
        self.nrDci10Msg4McsLabel = QLabel('Modulation and coding scheme(CW0)[0-31]:')
        self.nrDci10Msg4McsEdit = QLineEdit()
        
        self.nrDci10Msg4TbsLabel = QLabel('Transport block size(bits):')
        self.nrDci10Msg4TbsEdit = QLineEdit()
        self.nrDci10Msg4TbsEdit.setEnabled(False)
        
        self.nrDci10Msg4DeltaPriLabel = QLabel('PUCCH resource indicator[0-7]:')
        self.nrDci10Msg4DeltaPriEdit = QLineEdit()
        
        self.nrDci10Msg4K1Label = QLabel('K1(PDSCH-to-HARQ_feedback timing indicator)[0-7]:')
        self.nrDci10Msg4K1Edit = QLineEdit()
        
        dci10Msg4TimeAllocWidget = QWidget()
        dci10Msg4TimeAllocLayout = QGridLayout()
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocFieldLabel, 0, 0)
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocFieldEdit, 0, 1)
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocMappingTypeLabel, 1, 0)
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocMappingTypeComb, 1, 1)
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocK0Label, 2, 0)
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocK0Edit, 2, 1)
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocSlivLabel, 3, 0)
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocSlivEdit, 3, 1)
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocSLabel, 4, 0)
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocSEdit, 4, 1)
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocLLabel, 5, 0)
        dci10Msg4TimeAllocLayout.addWidget(self.nrDci10Msg4TimeAllocLEdit, 5, 1)
        dci10Msg4TimeAllocWidget.setLayout(dci10Msg4TimeAllocLayout)
        
        dci10Msg4FreqAllocWidget = QWidget()
        dci10Msg4FreqAllocLayout = QGridLayout()
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocTypeLabel, 0, 0)
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocTypeComb, 0, 1)
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocFieldLabel, 1, 0)
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocFieldEdit, 1, 1)
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocType1RbStartLabel, 2, 0)
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocType1RbStartEdit, 2, 1)
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocType1LRbsLabel, 3, 0)
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocType1LRbsEdit, 3, 1)
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocType1VrbPrbMapppingTypeLabel, 4, 0)
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocType1VrbPrbMappingTypeComb, 4, 1)
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocType1BundleSizeLabel, 5, 0)
        dci10Msg4FreqAllocLayout.addWidget(self.nrDci10Msg4FreqAllocType1BundleSizeComb, 5, 1)
        dci10Msg4FreqAllocWidget.setLayout(dci10Msg4FreqAllocLayout)
        
        dci10Msg4RaTabWidget = QTabWidget()
        dci10Msg4RaTabWidget.addTab(dci10Msg4TimeAllocWidget, 'Time-domain assignment')
        dci10Msg4RaTabWidget.addTab(dci10Msg4FreqAllocWidget, 'Frequency-domain assignment')
        
        dci10Msg4Widget = QWidget()
        dci10Msg4GridLayout = QGridLayout()
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4RntiLabel, 0, 0)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4RntiEdit, 0, 1)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4MuPdcchLabel, 1, 0)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4MuPdcchEdit, 1, 1)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4MuPdschLabel, 2, 0)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4MuPdschEdit, 2, 1)
        dci10Msg4GridLayout.addWidget(dci10Msg4RaTabWidget, 3, 0, 1, 2)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4McsLabel, 4, 0)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4McsEdit, 4, 1)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4TbsLabel, 5, 0)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4TbsEdit, 5, 1)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4DeltaPriLabel, 6, 0)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4DeltaPriEdit, 6, 1)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4K1Label, 7, 0)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4K1Edit, 7, 1)
        dci10Msg4Layout = QVBoxLayout()
        dci10Msg4Layout.addLayout(dci10Msg4GridLayout)
        dci10Msg4Layout.addStretch()
        dci10Msg4Widget.setLayout(dci10Msg4Layout)
        
        dci10Msg4Scroll = QScrollArea()
        dci10Msg4Scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        dci10Msg4Scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        dci10Msg4Scroll.setWidgetResizable(True)
        dci10Msg4Scroll.setWidget(dci10Msg4Widget)
        
        #DCI 1_1 with C-RNTI for normal PDSCH
        self.nrDci11PdschRntiLabel = QLabel('RNTI(C-RNTI)[0x0001-FFEF]:')
        self.nrDci11PdschRntiEdit = QLineEdit('0x0001')
        
        self.nrDci11PdschMuPdcchLabel = QLabel('u_PDCCH[0-3]:')
        self.nrDci11PdschMuPdcchEdit = QLineEdit()
        self.nrDci11PdschMuPdcchEdit.setEnabled(False)
        
        self.nrDci11PdschMuPdschLabel = QLabel('u_PDSCH[0-3]:')
        self.nrDci11PdschMuPdschEdit = QLineEdit()
        self.nrDci11PdschMuPdschEdit.setEnabled(False)
        
        self.nrDci11PdschActBwpLabel= QLabel('Active DL BWP[0-1]:')
        self.nrDci11PdschActBwpEdit = QLineEdit()
        self.nrDci11PdschActBwpEdit.setEnabled(False)
        
        self.nrDci11PdschIndicatedBwpLabel = QLabel('Bandwidth part indicator[0-1]:')
        self.nrDci11PdschIndicatedBwpEdit = QLineEdit()
        self.nrDci11PdschIndicatedBwpEdit.setEnabled(False)
        
        self.nrDci11PdschTimeAllocFieldLabel = QLabel('Time domain resource assignment[0-15]:')
        self.nrDci11PdschTimeAllocFieldEdit = QLineEdit()
        
        self.nrDci11PdschTimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrDci11PdschTimeAllocMappingTypeComb = QComboBox()
        self.nrDci11PdschTimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        
        self.nrDci11PdschTimeAllocK0Label = QLabel('K0:')
        self.nrDci11PdschTimeAllocK0Edit = QLineEdit()
        
        self.nrDci11PdschTimeAllocSlivLabel = QLabel('SLIV:')
        self.nrDci11PdschTimeAllocSlivEdit = QLineEdit()
        
        self.nrDci11PdschTimeAllocSLabel = QLabel('S(of SLIV):')
        self.nrDci11PdschTimeAllocSEdit = QLineEdit()
        
        self.nrDci11PdschTimeAllocLLabel = QLabel('L(of SLIV):')
        self.nrDci11PdschTimeAllocLEdit = QLineEdit()
        
        self.nrDci11PdschFreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrDci11PdschFreqAllocTypeComb = QComboBox()
        self.nrDci11PdschFreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrDci11PdschFreqAllocTypeComb.setCurrentIndex(1)
        
        self.nrDci11PdschFreqAllocFieldLabel = QLabel('Frequency domain resource assignment:')
        self.nrDci11PdschFreqAllocFieldEdit = QLineEdit()
        
        self.nrDci11PdschFreqAllocType1RbStartLabel = QLabel('RB_start(of RIV):')
        self.nrDci11PdschFreqAllocType1RbStartEdit = QLineEdit()
        
        self.nrDci11PdschFreqAllocType1LRbsLabel = QLabel('L_RBs(of RIV):')
        self.nrDci11PdschFreqAllocType1LRbsEdit = QLineEdit()
        
        self.nrDci11PdschFreqAllocType1VrbPrbMapppingTypeLabel = QLabel('VRB-to-PRB mapping type:')
        self.nrDci11PdschFreqAllocType1VrbPrbMappingTypeComb = QComboBox()
        self.nrDci11PdschFreqAllocType1VrbPrbMappingTypeComb.addItems(['nonInterleaved', 'interleaved'])
        self.nrDci11PdschFreqAllocType1VrbPrbMappingTypeComb.setCurrentIndex(1)
        
        self.nrDci11PdschFreqAllocType1BundleSizeLabel = QLabel('L(vrb-ToPRB-Interleaver):')
        self.nrDci11PdschFreqAllocType1BundleSizeComb = QComboBox()
        self.nrDci11PdschFreqAllocType1BundleSizeComb.addItems(['n2', 'n4'])
        self.nrDci11PdschFreqAllocType1BundleSizeComb.setCurrentIndex(0)
        
        self.nrDci11PdschCw0McsLabel = QLabel('Modulation and coding scheme(CW0)[0-31]:')
        self.nrDci11PdschCw0McsEdit = QLineEdit()
        
        self.nrDci11PdschCw1McsLabel = QLabel('Modulation and coding scheme(CW1)[0-31]:')
        self.nrDci11PdschCw1McsEdit = QLineEdit()
        
        self.nrDci11PdschTbsLabel = QLabel('Transport block size(bits):')
        self.nrDci11PdschTbsEdit = QLineEdit()
        self.nrDci11PdschTbsEdit.setEnabled(False)
        
        self.nrDci11PdschDeltaPriLabel = QLabel('PUCCH resource indicator[0-7]:')
        self.nrDci11PdschDeltaPriEdit = QLineEdit()
        
        self.nrDci11PdschK1Label = QLabel('K1(PDSCH-to-HARQ_feedback timing indicator)[0-7]:')
        self.nrDci11PdschK1Edit = QLineEdit()
        
        self.nrDci11PdschAntPortsFieldLabel = QLabel('Antenna port(s)[0-15/0-31/0-63]:')
        self.nrDci11PdschAntPortsFieldEdit = QLineEdit('0')
        
        dci11PdschTimeAllocWidget = QWidget()
        dci11PdschTimeAllocLayout = QGridLayout()
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocFieldLabel, 0, 0)
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocFieldEdit, 0, 1)
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocMappingTypeLabel, 1, 0)
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocMappingTypeComb, 1, 1)
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocK0Label, 2, 0)
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocK0Edit, 2, 1)
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocSlivLabel, 3, 0)
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocSlivEdit, 3, 1)
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocSLabel, 4, 0)
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocSEdit, 4, 1)
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocLLabel, 5, 0)
        dci11PdschTimeAllocLayout.addWidget(self.nrDci11PdschTimeAllocLEdit, 5, 1)
        dci11PdschTimeAllocWidget.setLayout(dci11PdschTimeAllocLayout)
        
        dci11PdschFreqAllocWidget = QWidget()
        dci11PdschFreqAllocLayout = QGridLayout()
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocTypeLabel, 0, 0)
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocTypeComb, 0, 1)
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocFieldLabel, 1, 0)
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocFieldEdit, 1, 1)
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocType1RbStartLabel, 2, 0)
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocType1RbStartEdit, 2, 1)
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocType1LRbsLabel, 3, 0)
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocType1LRbsEdit, 3, 1)
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocType1VrbPrbMapppingTypeLabel, 4, 0)
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocType1VrbPrbMappingTypeComb, 4, 1)
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocType1BundleSizeLabel, 5, 0)
        dci11PdschFreqAllocLayout.addWidget(self.nrDci11PdschFreqAllocType1BundleSizeComb, 5, 1)
        dci11PdschFreqAllocWidget.setLayout(dci11PdschFreqAllocLayout)
        
        dci11PdschRaTabWidget = QTabWidget()
        dci11PdschRaTabWidget.addTab(dci11PdschTimeAllocWidget, 'Time-domain assignment')
        dci11PdschRaTabWidget.addTab(dci11PdschFreqAllocWidget, 'Frequency-domain assignment')
        
        dci11PdschWidget = QWidget()
        dci11PdschGridLayout = QGridLayout()
        dci11PdschGridLayout.addWidget(self.nrDci11PdschRntiLabel, 0, 0)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschRntiEdit, 0, 1)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschMuPdcchLabel, 1, 0)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschMuPdcchEdit, 1, 1)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschMuPdschLabel, 2, 0)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschMuPdschEdit, 2, 1)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschActBwpLabel, 3, 0)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschActBwpEdit, 3, 1)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschIndicatedBwpLabel, 4, 0)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschIndicatedBwpEdit, 4, 1)
        dci11PdschGridLayout.addWidget(dci11PdschRaTabWidget, 5, 0, 1, 2)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschCw0McsLabel, 6, 0)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschCw0McsEdit, 6, 1)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschCw1McsLabel, 7, 0)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschCw1McsEdit, 7, 1)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschTbsLabel, 8, 0)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschTbsEdit, 8, 1)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschDeltaPriLabel, 9, 0)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschDeltaPriEdit, 9, 1)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschK1Label, 10, 0)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschK1Edit, 10, 1)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschAntPortsFieldLabel, 11, 0)
        dci11PdschGridLayout.addWidget(self.nrDci11PdschAntPortsFieldEdit, 11, 1)
        dci11PdschLayout = QVBoxLayout()
        dci11PdschLayout.addLayout(dci11PdschGridLayout)
        dci11PdschLayout.addStretch()
        dci11PdschWidget.setLayout(dci11PdschLayout)
        
        dci11PdschScroll = QScrollArea()
        dci11PdschScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        dci11PdschScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        dci11PdschScroll.setWidgetResizable(True)
        dci11PdschScroll.setWidget(dci11PdschWidget)
        
        #DCI 0_1 with C-RNTI for normal PUSCH
        self.nrDci01PuschRntiLabel = QLabel('RNTI(C-RNTI)[0x0001-FFEF]:')
        self.nrDci01PuschRntiEdit = QLineEdit('0x0001')
        
        self.nrDci01PuschMuPdcchLabel = QLabel('u_PDCCH[0-3]:')
        self.nrDci01PuschMuPdcchEdit = QLineEdit()
        self.nrDci01PuschMuPdcchEdit.setEnabled(False)
        
        self.nrDci01PuschMuPuschLabel = QLabel('u_PUSCH[0-3]:')
        self.nrDci01PuschMuPuschEdit = QLineEdit()
        self.nrDci01PuschMuPuschEdit.setEnabled(False)
        
        self.nrDci01PuschActBwpLabel= QLabel('Active UL BWP[0-1]:')
        self.nrDci01PuschActBwpEdit = QLineEdit()
        self.nrDci01PuschActBwpEdit.setEnabled(False)
        
        self.nrDci01PuschIndicatedBwpLabel = QLabel('Bandwidth part indicator[0-1]:')
        self.nrDci01PuschIndicatedBwpEdit = QLineEdit()
        self.nrDci01PuschIndicatedBwpEdit.setEnabled(False)
        
        self.nrDci01PuschTimeAllocFieldLabel = QLabel('Time domain resource assignment[0-15]:')
        self.nrDci01PuschTimeAllocFieldEdit = QLineEdit()
        
        self.nrDci01PuschTimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrDci01PuschTimeAllocMappingTypeComb = QComboBox()
        self.nrDci01PuschTimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        
        self.nrDci01PuschTimeAllocK2Label = QLabel('K2:')
        self.nrDci01PuschTimeAllocK2Edit = QLineEdit()
        
        self.nrDci01PuschTimeAllocSlivLabel = QLabel('SLIV:')
        self.nrDci01PuschTimeAllocSlivEdit = QLineEdit()
        
        self.nrDci01PuschTimeAllocSLabel = QLabel('S(of SLIV):')
        self.nrDci01PuschTimeAllocSEdit = QLineEdit()
        
        self.nrDci01PuschTimeAllocLLabel = QLabel('L(of SLIV):')
        self.nrDci01PuschTimeAllocLEdit = QLineEdit()
        
        self.nrDci01PuschFreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrDci01PuschFreqAllocTypeComb = QComboBox()
        self.nrDci01PuschFreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrDci01PuschFreqAllocTypeComb.setCurrentIndex(1)
        
        self.nrDci01PuschFreqAllocFhLabel= QLabel('Frequency hopping flag:')
        self.nrDci01PuschFreqAllocFhComb = QComboBox()
        self.nrDci01PuschFreqAllocFhComb.addItems(['disabled', 'intra-slot', 'inter-slot'])
        self.nrDci01PuschFreqAllocFhComb.setCurrentIndex(0)
        
        self.nrDci01PuschFreqAllocFieldLabel = QLabel('Frequency domain resource assignment:')
        self.nrDci01PuschFreqAllocFieldEdit = QLineEdit()
        
        self.nrDci01PuschFreqAllocType1RbStartLabel = QLabel('RB_start(of RIV):')
        self.nrDci01PuschFreqAllocType1RbStartEdit = QLineEdit()
        
        self.nrDci01PuschFreqAllocType1LRbsLabel = QLabel('L_RBs(of RIV):')
        self.nrDci01PuschFreqAllocType1LRbsEdit = QLineEdit()
        
        self.nrDci01PuschCw0McsLabel = QLabel('Modulation and coding scheme(CW0)[0-31]:')
        self.nrDci01PuschCw0McsEdit = QLineEdit()
        
        self.nrDci01PuschTbsLabel = QLabel('Transport block size(bits):')
        self.nrDci01PuschTbsEdit = QLineEdit()
        self.nrDci01PuschTbsEdit.setEnabled(False)
        
        self.nrDci01PuschSriFieldLabel = QLabel('SRS resource indicator[0-1/0-3/0-7/0-15]:')
        self.nrDci01PuschSriFieldEdit = QLineEdit('0')
        
        self.nrDci01PuschAntPortsFieldLabel = QLabel('Antenna port(s)[0-15/0-31/0-63]:')
        self.nrDci01PuschAntPortsFieldEdit = QLineEdit('0')
        
        dci01PuschTimeAllocWidget = QWidget()
        dci01PuschTimeAllocLayout = QGridLayout()
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocFieldLabel, 0, 0)
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocFieldEdit, 0, 1)
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocMappingTypeLabel, 1, 0)
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocMappingTypeComb, 1, 1)
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocK2Label, 2, 0)
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocK2Edit, 2, 1)
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocSlivLabel, 3, 0)
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocSlivEdit, 3, 1)
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocSLabel, 4, 0)
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocSEdit, 4, 1)
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocLLabel, 5, 0)
        dci01PuschTimeAllocLayout.addWidget(self.nrDci01PuschTimeAllocLEdit, 5, 1)
        dci01PuschTimeAllocWidget.setLayout(dci01PuschTimeAllocLayout)
        
        dci01PuschFreqAllocWidget = QWidget()
        dci01PuschFreqAllocLayout = QGridLayout()
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocTypeLabel, 0, 0)
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocTypeComb, 0, 1)
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocFhLabel, 1, 0)
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocFhComb, 1, 1)
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocFieldLabel, 2, 0)
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocFieldEdit, 2, 1)
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocType1RbStartLabel, 3, 0)
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocType1RbStartEdit, 3, 1)
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocType1LRbsLabel, 4, 0)
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocType1LRbsEdit, 4, 1)
        dci01PuschFreqAllocWidget.setLayout(dci01PuschFreqAllocLayout)
        
        dci01PuschRaTabWidget = QTabWidget()
        dci01PuschRaTabWidget.addTab(dci01PuschTimeAllocWidget, 'Time-domain assignment')
        dci01PuschRaTabWidget.addTab(dci01PuschFreqAllocWidget, 'Frequency-domain assignment')
        
        dci01PuschWidget = QWidget()
        dci01PuschGridLayout = QGridLayout()
        dci01PuschGridLayout.addWidget(self.nrDci01PuschRntiLabel, 0, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschRntiEdit, 0, 1)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschMuPdcchLabel, 1, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschMuPdcchEdit, 1, 1)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschMuPuschLabel, 2, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschMuPuschEdit, 2, 1)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschActBwpLabel, 3, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschActBwpEdit, 3, 1)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschIndicatedBwpLabel, 4, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschIndicatedBwpEdit, 4, 1)
        dci01PuschGridLayout.addWidget(dci01PuschRaTabWidget, 5, 0, 1, 2)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschCw0McsLabel, 6, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschCw0McsEdit, 6, 1)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschTbsLabel, 7, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschTbsEdit, 7, 1)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschSriFieldLabel, 8, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschSriFieldEdit, 8, 1)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschAntPortsFieldLabel, 9, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschAntPortsFieldEdit, 9, 1)
        dci01PuschLayout = QVBoxLayout()
        dci01PuschLayout.addLayout(dci01PuschGridLayout)
        dci01PuschLayout.addStretch()
        dci01PuschWidget.setLayout(dci01PuschLayout)
        
        dci01PuschScroll = QScrollArea()
        dci01PuschScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        dci01PuschScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        dci01PuschScroll.setWidgetResizable(True)
        dci01PuschScroll.setWidget(dci01PuschWidget)
        
        #RAR UL grant for Msg3 PUSCH
        self.nrMsg3PuschMuPuschLabel = QLabel('u_PUSCH[0-3]:')
        self.nrMsg3PuschMuPuschEdit = QLineEdit()
        self.nrMsg3PuschMuPuschEdit.setEnabled(False)
        
        self.nrMsg3PuschTimeAllocFieldLabel = QLabel('Time domain resource assignment[0-15]:')
        self.nrMsg3PuschTimeAllocFieldEdit = QLineEdit()
        
        self.nrMsg3PuschTimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrMsg3PuschTimeAllocMappingTypeComb = QComboBox()
        self.nrMsg3PuschTimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        
        self.nrMsg3PuschTimeAllocK2Label = QLabel('K2:')
        self.nrMsg3PuschTimeAllocK2Edit = QLineEdit()
        
        self.nrMsg3PuschTimeAllocDeltaLabel= QLabel('Delta:')
        self.nrMsg3PuschTimeAllocDeltaEdit = QLineEdit()
        
        self.nrMsg3PuschTimeAllocSlivLabel = QLabel('SLIV:')
        self.nrMsg3PuschTimeAllocSlivEdit = QLineEdit()
        
        self.nrMsg3PuschTimeAllocSLabel = QLabel('S(of SLIV):')
        self.nrMsg3PuschTimeAllocSEdit = QLineEdit()
        
        self.nrMsg3PuschTimeAllocLLabel = QLabel('L(of SLIV):')
        self.nrMsg3PuschTimeAllocLEdit = QLineEdit()
        
        self.nrMsg3PuschFreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrMsg3PuschFreqAllocTypeComb = QComboBox()
        self.nrMsg3PuschFreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrMsg3PuschFreqAllocTypeComb.setCurrentIndex(1)
        
        self.nrMsg3PuschFreqAllocFhLabel= QLabel('Frequency hopping flag:')
        self.nrMsg3PuschFreqAllocFhComb = QComboBox()
        self.nrMsg3PuschFreqAllocFhComb.addItems(['disabled', 'enabled'])
        self.nrMsg3PuschFreqAllocFhComb.setCurrentIndex(0)
        
        self.nrMsg3PuschFreqAllocFieldLabel = QLabel('Frequency domain resource assignment:')
        self.nrMsg3PuschFreqAllocFieldEdit = QLineEdit()
        
        self.nrMsg3PuschFreqAllocType1RbStartLabel = QLabel('RB_start(of RIV):')
        self.nrMsg3PuschFreqAllocType1RbStartEdit = QLineEdit()
        
        self.nrMsg3PuschFreqAllocType1LRbsLabel = QLabel('L_RBs(of RIV):')
        self.nrMsg3PuschFreqAllocType1LRbsEdit = QLineEdit()
        
        self.nrMsg3PuschCw0McsLabel = QLabel('Modulation and coding scheme(CW0)[0-31]:')
        self.nrMsg3PuschCw0McsEdit = QLineEdit()
        
        self.nrMsg3PuschTbsLabel = QLabel('Transport block size(bits):')
        self.nrMsg3PuschTbsEdit = QLineEdit()
        self.nrMsg3PuschTbsEdit.setEnabled(False)
        
        msg3PuschTimeAllocWidget = QWidget()
        msg3PuschTimeAllocLayout = QGridLayout()
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocFieldLabel, 0, 0)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocFieldEdit, 0, 1)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocMappingTypeLabel, 1, 0)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocMappingTypeComb, 1, 1)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocK2Label, 2, 0)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocK2Edit, 2, 1)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocDeltaLabel, 3, 0)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocDeltaEdit, 3, 1)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocSlivLabel, 4, 0)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocSlivEdit, 4, 1)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocSLabel, 5, 0)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocSEdit, 5, 1)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocLLabel, 6, 0)
        msg3PuschTimeAllocLayout.addWidget(self.nrMsg3PuschTimeAllocLEdit, 6, 1)
        msg3PuschTimeAllocWidget.setLayout(msg3PuschTimeAllocLayout)
        
        msg3PuschFreqAllocWidget = QWidget()
        msg3PuschFreqAllocLayout = QGridLayout()
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocTypeLabel, 0, 0)
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocTypeComb, 0, 1)
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocFhLabel, 1, 0)
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocFhComb, 1, 1)
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocFieldLabel, 2, 0)
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocFieldEdit, 2, 1)
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocType1RbStartLabel, 3, 0)
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocType1RbStartEdit, 3, 1)
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocType1LRbsLabel, 4, 0)
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocType1LRbsEdit, 4, 1)
        msg3PuschFreqAllocWidget.setLayout(msg3PuschFreqAllocLayout)
        
        msg3PuschRaTabWidget = QTabWidget()
        msg3PuschRaTabWidget.addTab(msg3PuschTimeAllocWidget, 'Time-domain assignment')
        msg3PuschRaTabWidget.addTab(msg3PuschFreqAllocWidget, 'Frequency-domain assignment')
        
        msg3PuschWidget = QWidget()
        msg3PuschGridLayout = QGridLayout()
        msg3PuschGridLayout.addWidget(self.nrMsg3PuschMuPuschLabel, 0, 0)
        msg3PuschGridLayout.addWidget(self.nrMsg3PuschMuPuschEdit, 0, 1)
        msg3PuschGridLayout.addWidget(msg3PuschRaTabWidget, 1, 0, 1, 2)
        msg3PuschGridLayout.addWidget(self.nrMsg3PuschCw0McsLabel, 2, 0)
        msg3PuschGridLayout.addWidget(self.nrMsg3PuschCw0McsEdit, 2, 1)
        msg3PuschGridLayout.addWidget(self.nrMsg3PuschTbsLabel, 3, 0)
        msg3PuschGridLayout.addWidget(self.nrMsg3PuschTbsEdit, 3, 1)
        msg3PuschLayout = QVBoxLayout()
        msg3PuschLayout.addLayout(msg3PuschGridLayout)
        msg3PuschLayout.addStretch()
        msg3PuschWidget.setLayout(msg3PuschLayout)
        
        msg3PuschScroll = QScrollArea()
        msg3PuschScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        msg3PuschScroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        msg3PuschScroll.setWidgetResizable(True)
        msg3PuschScroll.setWidget(msg3PuschWidget)
        
        dciTabWidget = QTabWidget()
        dciTabWidget.addTab(dci10Sib1Scroll, 'DCI 1_0(SIB1)')
        dciTabWidget.addTab(dci10Msg2Scroll, 'DCI 1_0(Msg2)')
        dciTabWidget.addTab(dci10Msg4Scroll, 'DCI 1_0(Msg4)')
        dciTabWidget.addTab(dci11PdschScroll, 'DCI 1_1(PDSCH)')
        dciTabWidget.addTab(msg3PuschScroll, 'Msg3 PUSCH')
        dciTabWidget.addTab(dci01PuschScroll, 'DCI 0_1(PUSCH)')
        
        pdcchCfgWidget = QWidget()
        pdcchCfgLayout = QVBoxLayout()
        pdcchCfgLayout.addWidget(css0GrpBox)
        pdcchCfgLayout.addWidget(pdcchTabWidget)
        pdcchCfgLayout.addWidget(dciTabWidget)
        pdcchCfgLayout.addStretch()
        pdcchCfgWidget.setLayout(pdcchCfgLayout)
        
        #-->(4) BWP settings tab
        '''
        initial active DL BWP(CORESET0): dmrs for sib1
        initial active DL BWP(SIB1): bwp generic and dmrs for msg2/msg4
        initial active UL BWP(SIB1): bwp generic and prach for msg1, pucch for msg4 harq, dmrs for msg3 pusch
        dedicated active DL BWP: bwp generic and dmrs for normal pdsch, ptrs for pdsch, csi-rs(?), pdcch(defined in CORESET1/USS)
        dedicated active UL BWP: bwp generic and dmrs for normal pusch, ptrs for pusch, srs, pucch for harq/csi feedback 
        '''
        #---->(4.1) initial active DL BWP as specified in CORESET0/SIB1
        #DM-RS for SIB1
        self.nrDmrsSib1DmrsTypeLabel = QLabel('dmrs-Type:')
        self.nrDmrsSib1DmrsTypeComb = QComboBox()
        self.nrDmrsSib1DmrsTypeComb.addItems(['Type 1', 'Type 2'])
        self.nrDmrsSib1DmrsTypeComb.setCurrentIndex(0)
        
        self.nrDmrsSib1AddPosLabel = QLabel('dmrs-additionalPosition:')
        self.nrDmrsSib1AddPosComb = QComboBox()
        self.nrDmrsSib1AddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        
        self.nrDmrsSib1MaxLengthLabel = QLabel('maxLength:')
        self.nrDmrsSib1MaxLengthComb = QComboBox()
        self.nrDmrsSib1MaxLengthComb.addItems(['len1', 'len2'])
        self.nrDmrsSib1MaxLengthComb.setCurrentIndex(0)
        
        self.nrDmrsSib1DmrsPortsLabel = QLabel('DMRS port(s)[1000+x]:')
        self.nrDmrsSib1DmrsPortsEdit = QLineEdit()
        self.nrDmrsSib1DmrsPortsEdit.setEnabled(False)
        
        self.nrDmrsSib1CdmGroupsWoDataLabel = QLabel('CDM group(s) without data:')
        self.nrDmrsSib1CdmGroupsWoDataEdit = QLineEdit()
        self.nrDmrsSib1CdmGroupsWoDataEdit.setEnabled(False)
        
        self.nrDmrsSib1FrontLoadSymbsLabel = QLabel('Number of front-load symbols:')
        self.nrDmrsSib1FrontLoadSymbsEdit = QLineEdit('1')
        self.nrDmrsSib1FrontLoadSymbsEdit.setEnabled(False)
        
        dmrsSib1Widget = QWidget()
        dmrsSib1GridLayout = QGridLayout()
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1DmrsTypeLabel, 0, 0)
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1DmrsTypeComb, 0, 1)
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1AddPosLabel, 1, 0)
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1AddPosComb, 1, 1)
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1MaxLengthLabel, 2, 0)
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1MaxLengthComb, 2, 1)
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1DmrsPortsLabel, 3, 0)
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1DmrsPortsEdit, 3, 1)
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1CdmGroupsWoDataLabel, 4, 0)
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1CdmGroupsWoDataEdit, 4, 1)
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1FrontLoadSymbsLabel, 5, 0)
        dmrsSib1GridLayout.addWidget(self.nrDmrsSib1FrontLoadSymbsEdit, 5, 1)
        dmrsSib1Layout = QVBoxLayout()
        dmrsSib1Layout.addLayout(dmrsSib1GridLayout)
        dmrsSib1Layout.addStretch()
        dmrsSib1Widget.setLayout(dmrsSib1Layout)
        
        #DM-RS for Msg2
        self.nrDmrsMsg2DmrsTypeLabel = QLabel('dmrs-Type:')
        self.nrDmrsMsg2DmrsTypeComb = QComboBox()
        self.nrDmrsMsg2DmrsTypeComb.addItems(['Type 1', 'Type 2'])
        self.nrDmrsMsg2DmrsTypeComb.setCurrentIndex(0)
        
        self.nrDmrsMsg2AddPosLabel = QLabel('dmrs-additionalPosition:')
        self.nrDmrsMsg2AddPosComb = QComboBox()
        self.nrDmrsMsg2AddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        
        self.nrDmrsMsg2MaxLengthLabel = QLabel('maxLength:')
        self.nrDmrsMsg2MaxLengthComb = QComboBox()
        self.nrDmrsMsg2MaxLengthComb.addItems(['len1', 'len2'])
        self.nrDmrsMsg2MaxLengthComb.setCurrentIndex(0)
        
        self.nrDmrsMsg2DmrsPortsLabel = QLabel('DMRS port(s)[1000+x]:')
        self.nrDmrsMsg2DmrsPortsEdit = QLineEdit()
        self.nrDmrsMsg2DmrsPortsEdit.setEnabled(False)
        
        self.nrDmrsMsg2CdmGroupsWoDataLabel = QLabel('CDM group(s) without data:')
        self.nrDmrsMsg2CdmGroupsWoDataEdit = QLineEdit()
        self.nrDmrsMsg2CdmGroupsWoDataEdit.setEnabled(False)
        
        self.nrDmrsMsg2FrontLoadSymbsLabel = QLabel('Number of front-load symbols:')
        self.nrDmrsMsg2FrontLoadSymbsEdit = QLineEdit('1')
        self.nrDmrsMsg2FrontLoadSymbsEdit.setEnabled(False)
        
        dmrsMsg2Widget = QWidget()
        dmrsMsg2GridLayout = QGridLayout()
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2DmrsTypeLabel, 0, 0)
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2DmrsTypeComb, 0, 1)
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2AddPosLabel, 1, 0)
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2AddPosComb, 1, 1)
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2MaxLengthLabel, 2, 0)
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2MaxLengthComb, 2, 1)
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2DmrsPortsLabel, 3, 0)
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2DmrsPortsEdit, 3, 1)
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2CdmGroupsWoDataLabel, 4, 0)
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2CdmGroupsWoDataEdit, 4, 1)
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2FrontLoadSymbsLabel, 5, 0)
        dmrsMsg2GridLayout.addWidget(self.nrDmrsMsg2FrontLoadSymbsEdit, 5, 1)
        dmrsMsg2Layout = QVBoxLayout()
        dmrsMsg2Layout.addLayout(dmrsMsg2GridLayout)
        dmrsMsg2Layout.addStretch()
        dmrsMsg2Widget.setLayout(dmrsMsg2Layout)
        
        #DM-RS for Msg4
        self.nrDmrsMsg4DmrsTypeLabel = QLabel('dmrs-Type:')
        self.nrDmrsMsg4DmrsTypeComb = QComboBox()
        self.nrDmrsMsg4DmrsTypeComb.addItems(['Type 1', 'Type 2'])
        self.nrDmrsMsg4DmrsTypeComb.setCurrentIndex(0)
        
        self.nrDmrsMsg4AddPosLabel = QLabel('dmrs-additionalPosition:')
        self.nrDmrsMsg4AddPosComb = QComboBox()
        self.nrDmrsMsg4AddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        
        self.nrDmrsMsg4MaxLengthLabel = QLabel('maxLength:')
        self.nrDmrsMsg4MaxLengthComb = QComboBox()
        self.nrDmrsMsg4MaxLengthComb.addItems(['len1', 'len2'])
        self.nrDmrsMsg4MaxLengthComb.setCurrentIndex(0)
        
        self.nrDmrsMsg4DmrsPortsLabel = QLabel('DMRS port(s)[1000+x]:')
        self.nrDmrsMsg4DmrsPortsEdit = QLineEdit()
        self.nrDmrsMsg4DmrsPortsEdit.setEnabled(False)
        
        self.nrDmrsMsg4CdmGroupsWoDataLabel = QLabel('CDM group(s) without data:')
        self.nrDmrsMsg4CdmGroupsWoDataEdit = QLineEdit()
        self.nrDmrsMsg4CdmGroupsWoDataEdit.setEnabled(False)
        
        self.nrDmrsMsg4FrontLoadSymbsLabel = QLabel('Number of front-load symbols:')
        self.nrDmrsMsg4FrontLoadSymbsEdit = QLineEdit('1')
        self.nrDmrsMsg4FrontLoadSymbsEdit.setEnabled(False)
        
        dmrsMsg4Widget = QWidget()
        dmrsMsg4GridLayout = QGridLayout()
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4DmrsTypeLabel, 0, 0)
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4DmrsTypeComb, 0, 1)
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4AddPosLabel, 1, 0)
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4AddPosComb, 1, 1)
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4MaxLengthLabel, 2, 0)
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4MaxLengthComb, 2, 1)
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4DmrsPortsLabel, 3, 0)
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4DmrsPortsEdit, 3, 1)
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4CdmGroupsWoDataLabel, 4, 0)
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4CdmGroupsWoDataEdit, 4, 1)
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4FrontLoadSymbsLabel, 5, 0)
        dmrsMsg4GridLayout.addWidget(self.nrDmrsMsg4FrontLoadSymbsEdit, 5, 1)
        dmrsMsg4Layout = QVBoxLayout()
        dmrsMsg4Layout.addLayout(dmrsMsg4GridLayout)
        dmrsMsg4Layout.addStretch()
        dmrsMsg4Widget.setLayout(dmrsMsg4Layout)
        
        iniDlBwpDmrsTabWidget = QTabWidget()
        iniDlBwpDmrsTabWidget.addTab(dmrsSib1Widget, 'DM-RS(SIB1)')
        iniDlBwpDmrsTabWidget.addTab(dmrsMsg2Widget, 'DM-RS(Msg2)')
        iniDlBwpDmrsTabWidget.addTab(dmrsMsg4Widget, 'DM-RS(Msg4)')
        
        #initial dl bwp as indicated in sib1
        self.nrIniDlBwpGenericBwpIdLabel = QLabel('bwp-Id[0-3]:')
        self.nrIniDlBwpGenericBwpIdEdit = QLineEdit()
        self.nrIniDlBwpGenericBwpIdEdit.setText('0')
        
        self.nrIniDlBwpGenericScsLabel = QLabel('subcarrierSpacing:')
        self.nrIniDlBwpGenericScsComb = QComboBox()
        self.nrIniDlBwpGenericScsComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        
        self.nrIniDlBwpGenericCpLabel = QLabel('cyclicPrefix:')
        self.nrIniDlBwpGenericCpComb = QComboBox()
        self.nrIniDlBwpGenericCpComb.addItems(['normal', 'extended'])
        self.nrIniDlBwpGenericCpComb.setCurrentIndex(0)
        
        self.nrIniDlBwpGenericLocAndBwLabel = QLabel('locationAndBandwidth[0-37949]:')
        self.nrIniDlBwpGenericLocAndBwEdit = QLineEdit()
        
        self.nrIniDlBwpGenericRbStartLabel = QLabel('RB_start:')
        self.nrIniDlBwpGenericRbStartEdit = QLineEdit()
        self.nrIniDlBwpGenericRbStartEdit.setEnabled(False)
        
        self.nrIniDlBwpGenericLRbsLabel = QLabel('L_RBs:')
        self.nrIniDlBwpGenericLRbsEdit = QLineEdit()
        self.nrIniDlBwpGenericLRbsEdit.setEnabled(False)
        
        iniDlBwpSib1GrpBox = QGroupBox()
        iniDlBwpSib1GrpBox.setTitle('Initial active DL BWP(SIB1)')
        iniDlBwpSib1GrpBoxGridLayout = QGridLayout()
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericBwpIdLabel, 0, 0)
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericBwpIdEdit, 0, 1)
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericScsLabel, 1, 0)
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericScsComb, 1, 1)
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericCpLabel, 2, 0)
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericCpComb, 2, 1)
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericLocAndBwLabel, 3, 0)
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericLocAndBwEdit, 3, 1)
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericRbStartLabel, 4, 0)
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericRbStartEdit, 4, 1)
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericLRbsLabel, 5, 0)
        iniDlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniDlBwpGenericLRbsEdit, 5, 1)
        iniDlBwpSib1GrpBox.setLayout(iniDlBwpSib1GrpBoxGridLayout)
        
        iniDlBwpWidget = QWidget()
        iniDlBwpLayout = QVBoxLayout()
        iniDlBwpLayout.addWidget(iniDlBwpSib1GrpBox)
        iniDlBwpLayout.addWidget(iniDlBwpDmrsTabWidget)
        iniDlBwpLayout.addStretch()
        iniDlBwpWidget.setLayout(iniDlBwpLayout)
        
        #---->(4.2) initial active ul bwp as specified in SIB1
        #initial ul bwp as indicated in sib1
        self.nrIniUlBwpGenericBwpIdLabel = QLabel('bwp-Id[0-3]:')
        self.nrIniUlBwpGenericBwpIdEdit = QLineEdit()
        self.nrIniUlBwpGenericBwpIdEdit.setText('0')
        
        self.nrIniUlBwpGenericScsLabel = QLabel('subcarrierSpacing:')
        self.nrIniUlBwpGenericScsComb = QComboBox()
        self.nrIniUlBwpGenericScsComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        
        self.nrIniUlBwpGenericCpLabel = QLabel('cyclicPrefix:')
        self.nrIniUlBwpGenericCpComb = QComboBox()
        self.nrIniUlBwpGenericCpComb.addItems(['normal', 'extended'])
        self.nrIniUlBwpGenericCpComb.setCurrentIndex(0)
        
        self.nrIniUlBwpGenericLocAndBwLabel = QLabel('locationAndBandwidth[0-37949]:')
        self.nrIniUlBwpGenericLocAndBwEdit = QLineEdit()
        
        self.nrIniUlBwpGenericRbStartLabel = QLabel('RB_start:')
        self.nrIniUlBwpGenericRbStartEdit = QLineEdit()
        self.nrIniUlBwpGenericRbStartEdit.setEnabled(False)
        
        self.nrIniUlBwpGenericLRbsLabel = QLabel('L_RBs:')
        self.nrIniUlBwpGenericLRbsEdit = QLineEdit()
        self.nrIniUlBwpGenericLRbsEdit.setEnabled(False)
        
        iniUlBwpSib1GrpBox = QGroupBox()
        iniUlBwpSib1GrpBox.setTitle('Initial active UL BWP(SIB1)')
        iniUlBwpSib1GrpBoxGridLayout = QGridLayout()
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericBwpIdLabel, 0, 0)
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericBwpIdEdit, 0, 1)
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericScsLabel, 1, 0)
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericScsComb, 1, 1)
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericCpLabel, 2, 0)
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericCpComb, 2, 1)
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericLocAndBwLabel, 3, 0)
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericLocAndBwEdit, 3, 1)
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericRbStartLabel, 4, 0)
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericRbStartEdit, 4, 1)
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericLRbsLabel, 5, 0)
        iniUlBwpSib1GrpBoxGridLayout.addWidget(self.nrIniUlBwpGenericLRbsEdit, 5, 1)
        iniUlBwpSib1GrpBox.setLayout(iniUlBwpSib1GrpBoxGridLayout)
        
        #prach for msg1
        self.nrRachGenericPrachConfIdLabel = QLabel('prach-ConfigurationIndex[0-255]:')
        self.nrrachgenericPrachConfIdEdit = QLineEdit()
        self.nrrachgenericPrachConfIdEdit.setText('0')
        
        self.nrRachGenericPrachFmtLabel = QLabel('Preamble format:')
        self.nrRachGenericPrachFmtEdit = QLineEdit()
        self.nrRachGenericPrachFmtEdit.setEnabled(False)
        
        self.nrRachGenericScsLabel = QLabel('msg1-SubcarrierSpacing:')
        self.nrrachgenericScsComb = QComboBox()
        self.nrrachgenericScsComb.addItems(['1.25KHz', '5KHz', '15KHz', '30KHz', '60KHz', '120KHz'])
        
        self.nrRachGenericMsg1FdmLabel = QLabel('msg1-FDM:')
        self.nrRachGenericMsg1FdmComb = QComboBox()
        self.nrRachGenericMsg1FdmComb.addItems(['1', '2', '4', '8'])
        
        self.nrRachGenericMsg1FreqStartLabel = QLabel('msg1-FrequencyStart[0-274]:')
        self.nrRachGenericMsg1FreqStartEdit = QLineEdit()
        
        rachGenericGrpBox = QGroupBox()
        rachGenericGrpBox.setTitle('RACH-ConfigGeneric')
        rachGenericGrpBoxGridLayout = QGridLayout()
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericPrachConfIdLabel, 0, 0)
        rachGenericGrpBoxGridLayout.addWidget(self.nrrachgenericPrachConfIdEdit, 0, 1)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericPrachFmtLabel, 1, 0)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericPrachFmtEdit, 1, 1)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericScsLabel, 2, 0)
        rachGenericGrpBoxGridLayout.addWidget(self.nrrachgenericScsComb, 2, 1)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericMsg1FdmLabel, 3, 0)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericMsg1FdmComb, 3, 1)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericMsg1FreqStartLabel, 4, 0)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericMsg1FreqStartEdit, 4, 1)
        rachGenericGrpBox.setLayout(rachGenericGrpBoxGridLayout)
        
        self.nrRachNumRaPreamblesLabel = QLabel('totalNumberOfRA-Preambles[1-64]:')
        self.nrRachNumRaPreamblesEdit = QLineEdit()
        self.nrRachNumRaPreamblesEdit.setText('64')
        
        self.nrRachSsbPerRachOccasionLabel = QLabel('ssb-perRACH-Occasion:')
        self.nrRachSsbPerRachOccasionComb = QComboBox()
        self.nrRachSsbPerRachOccasionComb.addItems(['1/8', '1/4', '1/2', '1', '2', '4', '8' '16'])
        
        self.nrRachCbPreamblesPerSsbLabel = QLabel('CB-PreamblesPerSSB:')
        self.nrRachCbPreamblesPerSsbEdit = QLineEdit()
        
        #prach time-domain allocation and freq-domain allocation are determined internally
        
        prachWidget = QWidget()
        prachWidgetGridLayout = QGridLayout()
        prachWidgetGridLayout.addWidget(rachGenericGrpBox, 0, 0, 1, 2)
        prachWidgetGridLayout.addWidget(self.nrRachNumRaPreamblesLabel, 1, 0)
        prachWidgetGridLayout.addWidget(self.nrRachNumRaPreamblesEdit, 1, 1)
        prachWidgetGridLayout.addWidget(self.nrRachSsbPerRachOccasionLabel, 2, 0)
        prachWidgetGridLayout.addWidget(self.nrRachSsbPerRachOccasionComb, 2, 1)
        prachWidgetGridLayout.addWidget(self.nrRachCbPreamblesPerSsbLabel, 3, 0)
        prachWidgetGridLayout.addWidget(self.nrRachCbPreamblesPerSsbEdit, 3, 1)
        prachWidget.setLayout(prachWidgetGridLayout)
        
        #dmrs for msg3 pusch
        self.nrDmrsMsg3DmrsTypeLabel = QLabel('dmrs-Type:')
        self.nrDmrsMsg3DmrsTypeComb = QComboBox()
        self.nrDmrsMsg3DmrsTypeComb.addItems(['Type 1', 'Type 2'])
        self.nrDmrsMsg3DmrsTypeComb.setCurrentIndex(0)
        
        self.nrDmrsMsg3AddPosLabel = QLabel('dmrs-additionalPosition:')
        self.nrDmrsMsg3AddPosComb = QComboBox()
        self.nrDmrsMsg3AddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        
        self.nrDmrsMsg3MaxLengthLabel = QLabel('maxLength:')
        self.nrDmrsMsg3MaxLengthComb = QComboBox()
        self.nrDmrsMsg3MaxLengthComb.addItems(['len1', 'len2'])
        self.nrDmrsMsg3MaxLengthComb.setCurrentIndex(0)
        
        self.nrDmrsMsg3DmrsPortsLabel = QLabel('DMRS port(s)[x]:')
        self.nrDmrsMsg3DmrsPortsEdit = QLineEdit()
        self.nrDmrsMsg3DmrsPortsEdit.setEnabled(False)
        
        self.nrDmrsMsg3CdmGroupsWoDataLabel = QLabel('CDM group(s) without data:')
        self.nrDmrsMsg3CdmGroupsWoDataEdit = QLineEdit()
        self.nrDmrsMsg3CdmGroupsWoDataEdit.setEnabled(False)
        
        self.nrDmrsMsg3FrontLoadSymbsLabel = QLabel('Number of front-load symbols:')
        self.nrDmrsMsg3FrontLoadSymbsEdit = QLineEdit('1')
        self.nrDmrsMsg3FrontLoadSymbsEdit.setEnabled(False)
        
        dmrsMsg3Widget = QWidget()
        dmrsMsg3GridLayout = QGridLayout()
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3DmrsTypeLabel, 0, 0)
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3DmrsTypeComb, 0, 1)
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3AddPosLabel, 1, 0)
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3AddPosComb, 1, 1)
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3MaxLengthLabel, 2, 0)
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3MaxLengthComb, 2, 1)
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3DmrsPortsLabel, 3, 0)
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3DmrsPortsEdit, 3, 1)
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3CdmGroupsWoDataLabel, 4, 0)
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3CdmGroupsWoDataEdit, 4, 1)
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3FrontLoadSymbsLabel, 5, 0)
        dmrsMsg3GridLayout.addWidget(self.nrDmrsMsg3FrontLoadSymbsEdit, 5, 1)
        dmrsMsg3Layout = QVBoxLayout()
        dmrsMsg3Layout.addLayout(dmrsMsg3GridLayout)
        dmrsMsg3Layout.addStretch()
        dmrsMsg3Widget.setLayout(dmrsMsg3Layout)
        
        #pucch for msg4 harq feedback
        self.nrPucchSib1PucchResCommonLabel = QLabel('pucch-ResourceCommon[0-15]:')
        self.nrPucchSib1PucchResCommonEdit = QLineEdit('0')
        
        self.nrPucchSib1PucchFmtLabel = QLabel('PUCCH format:')
        self.nrPucchSib1PucchFmtComb = QComboBox()
        self.nrPucchSib1PucchFmtComb.addItems(['format 0', 'format 1', 'format 2', 'format 3', 'format 4'])
        self.nrPucchSib1PucchFmtComb.setCurrentIndex(0)
        self.nrPucchSib1PucchFmtComb.setEnabled(False)
        
        self.nrPucchSib1StartingSymbLabel = QLabel('First symbol:')
        self.nrPucchSib1StartingSymbEdit = QLineEdit('12')
        self.nrPucchSib1StartingSymbEdit.setEnabled(False)
        
        self.nrPucchSib1NumSymbsLabel = QLabel('Number of symbols:')
        self.nrPucchSib1NumSymbsEdit = QLineEdit('2')
        self.nrPucchSib1NumSymbsEdit.setEnabled(False)
        
        self.nrPucchSib1PrbOffsetLabel = QLabel('PRB offset:')
        self.nrPucchSib1PrbOffsetEdit = QLineEdit('0')
        self.nrPucchSib1PrbOffsetEdit.setEnabled(False)
        
        self.nrPucchSib1IniCsIndexesSetLabel = QLabel('Set of initial CS indexes:')
        self.nrPucchSib1IniCsIndexesSetEdit = QLineEdit('{0, 3}')
        self.nrPucchSib1IniCsIndexesSetEdit.setEnabled(False)
        
        pucchSib1Widget = QWidget()
        pucchSib1WidgetGridLayout = QGridLayout()
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1PucchResCommonLabel, 0, 0)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1PucchResCommonEdit, 0, 1)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1PucchFmtLabel, 1, 0)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1PucchFmtComb, 1, 1)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1StartingSymbLabel, 2, 0)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1StartingSymbEdit, 2, 1)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1NumSymbsLabel, 3, 0)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1NumSymbsEdit, 3, 1)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1IniCsIndexesSetLabel, 4, 0)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1IniCsIndexesSetEdit, 4, 1)
        pucchSib1WidgetLayout = QVBoxLayout()
        pucchSib1WidgetLayout.addLayout(pucchSib1WidgetGridLayout)
        pucchSib1WidgetLayout.addStretch()
        pucchSib1Widget.setLayout(pucchSib1WidgetLayout)
        
        iniUlBwpMsg1DmrsPucchTabWidget = QTabWidget()
        iniUlBwpMsg1DmrsPucchTabWidget.addTab(prachWidget, 'RACH-ConfigCommon(Msg1)')
        iniUlBwpMsg1DmrsPucchTabWidget.addTab(dmrsMsg3Widget, 'DM-RS(Msg3)')
        iniUlBwpMsg1DmrsPucchTabWidget.addTab(pucchSib1Widget, 'PUCCH-ConfigCommon(Msg4 HARQ)')
        
        iniUlBwpWidget = QWidget()
        iniUlBwpLayout = QVBoxLayout()
        iniUlBwpLayout.addWidget(iniUlBwpSib1GrpBox)
        iniUlBwpLayout.addWidget(iniUlBwpMsg1DmrsPucchTabWidget)
        iniUlBwpLayout.addStretch()
        iniUlBwpWidget.setLayout(iniUlBwpLayout)
        
        bwpCfgTabWidget = QTabWidget()
        bwpCfgTabWidget.addTab(iniDlBwpWidget, 'Initial DL BWP')
        bwpCfgTabWidget.addTab(iniUlBwpWidget, 'Initial UL BWP')
        
        #-->(4) PDSCH settings tab
        
        #-->(5) PRACH settings tab
        
        #-->(6) PUCCH settings tab
        
        #-->(7) SRS settings tab
        
        #-->(8) PUSCH settings tab
        
        
        
        #-->(10) CSI-RS settings tab
        #TODO CSI-RS is not supported!

        #connect signals to slots
        self.nrCarrierBwComb.currentIndexChanged[int].connect(self.onCarrierBwCombCurrentIndexChanged)
        self.nrCarrierScsComb.currentIndexChanged[int].connect(self.onCarrierScsCombCurrentIndexChanged)
        self.nrCarrierBandComb.currentIndexChanged[int].connect(self.onCarrierBandCombCurrentIndexChanged)
        self.nrSsbScsComb.currentIndexChanged[int].connect(self.onSsbScsCombCurrentIndexChanged)
        self.nrMibCoreset0Edit.editingFinished.connect(self.onMibCoreset0EditEditingFinished)
        self.nrSsbKssbEdit.editingFinished.connect(self.onSsbKssbEditEditingFinished)
        self.nrCarrierBandComb.setCurrentText('n77')

        #-->Tab Widgets
        tabWidget = QTabWidget()
        tabWidget.addTab(gridCfgWidget, 'Grid Settings')
        tabWidget.addTab(ssbCfgWidget, 'SSB Settings')
        tabWidget.addTab(pdcchCfgWidget, 'PDCCH Settings')
        tabWidget.addTab(bwpCfgTabWidget, 'BWP Settings')

        #-->Buttons
        self.okBtn = QPushButton('OK')
        self.cancelBtn = QPushButton('Cancel')
        self.okBtn.clicked.connect(self.onOkBtnClicked)
        self.cancelBtn.clicked.connect(self.reject)

        layoutBtns = QHBoxLayout()
        layoutBtns.addStretch()
        layoutBtns.addWidget(self.okBtn)
        layoutBtns.addWidget(self.cancelBtn)

        #-->Main Layout
        layout = QVBoxLayout()
        layout.addWidget(tabWidget)
        layout.addLayout(layoutBtns)

        self.setLayout(layout)
        self.setWindowTitle('5GNR Resource Grid')
        
    def initGlobalPar(self):
        #refer to 3GPP 38.104 vf30
        #Table 5.2-1: NR operating bands in FR1
        #Table 5.2-2: NR operating bands in FR2
        self.nrOpBands = OrderedDict((
            ('n1', ('1920 MHz-1980 MHz', '2110 MHz-2170 MHz', 'FDD',4)),
            ('n2', ('1850 MHz-1910 MHz', '1930 MHz-1990 MHz', 'FDD',4)),
            ('n3', ('1710 MHz-1785 MHz', '1805 MHz-1880 MHz', 'FDD',4)),
            ('n5', ('824 MHz-849 MHz', '869 MHz-894 MHz', 'FDD',4)),
            ('n7', ('2500 MHz-2570 MHz', '2620 MHz-2690 MHz', 'FDD',4)),
            ('n8', ('880 MHz-915 MHz', '925 MHz-960 MHz', 'FDD',4)),
            ('n12', ('699 MHz-716 MHz', '729 MHz-746 MHz', 'FDD',4)),
            ('n20', ('832 MHz-862 MHz', '791 MHz-821 MHz', 'FDD',4)),
            ('n25', ('1850 MHz-1915 MHz', '1930 MHz-1995 MHz', 'FDD',4)),
            ('n28', ('703 MHz-748 MHz', '758 MHz-803 MHz', 'FDD',4)),
            ('n34', ('2010 MHz-2025 MHz', '2010 MHz-2025 MHz', 'TDD',4)),
            ('n38', ('2570 MHz-2620 MHz', '2570 MHz-2620 MHz', 'TDD',4)),
            ('n39', ('1880 MHz-1920 MHz', '1880 MHz-1920 MHz', 'TDD',4)),
            ('n40', ('2300 MHz-2400 MHz', '2300 MHz-2400 MHz', 'TDD',4)),
            ('n41', ('2496 MHz-2690 MHz', '2496 MHz-2690 MHz', 'TDD',4)),
            ('n50', ('1432 MHz-1517 MHz', '1432 MHz-1517 MHz', 'TDD',4)),
            ('n51', ('1427 MHz-1432 MHz', '1427 MHz-1432 MHz', 'TDD',4)),
            ('n66', ('1710 MHz-1780 MHz', '2110 MHz-2200 MHz', 'FDD',4)),
            ('n70', ('1695 MHz-1710 MHz', '1995 MHz-2020 MHz', 'FDD',4)),
            ('n71', ('663 MHz-698 MHz', '617 MHz-652 MHz', 'FDD',4)),
            ('n74', ('1427 MHz-1470 MHz', '1475 MHz-1518 MHz', 'FDD',4)),
            ('n75', ('N/A', '1432 MHz-1517 MHz', 'SDL',4)),
            ('n76', ('N/A', '1427 MHz-1432 MHz', 'SDL',4)),
            ('n77', ('3300 MHz-4200 MHz', '3300 MHz-4200 MHz', 'TDD',8)),
            ('n78', ('3300 MHz-3800 MHz', '3300 MHz-3800 MHz', 'TDD',8)),
            ('n79', ('4400 MHz-5000 MHz', '4400 MHz-5000 MHz', 'TDD',8)),
            ('n80', ('1710 MHz-1785 MHz', 'N/A', 'SUL ',0)),
            ('n81', ('880 MHz-915 MHz', 'N/A', 'SUL ',0)),
            ('n82', ('832 MHz-862 MHz', 'N/A', 'SUL ',0)),
            ('n83', ('703 MHz-748 MHz', 'N/A', 'SUL',0)),
            ('n84', ('1920 MHz-1980 MHz', 'N/A', 'SUL',0)),
            ('n86', ('1710 MHz-1780 MHz', 'N/A', 'SUL',0)),
            ('n257', ('26500 MHz-29500 MHz', '26500 MHz-29500 MHz', 'TDD',64)),
            ('n258', ('24250 MHz-27500 MHz', '24250 MHz-27500 MHz', 'TDD',64)),
            ('n260', ('37000 MHz-40000 MHz', '37000 MHz-40000 MHz', 'TDD',64)),
            ('n261', ('27500 MHz-28350 MHz', '27500 MHz-28350 MHz', 'TDD',64)),
            ))
        
        self.nrBwSetFr1 = ('5MHz', '10MHz', '15MHz', '20MHz', '25MHz', '30MHz', '40MHz', '50MHz', '60MHz', '70MHz', '80MHz', '90MHz', '100MHz')
        self.nrBwSetFr2 = ('50MHz', '100MHz', '200MHz', '400MHz')
        
        #refer to 3GPP 38.104 vf30
        #Table 5.3.5-1: BS channel bandwidths and SCS per operating band in FR1
        self.nrBandScs2BwFr1 = OrderedDict((
            ('n1_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n1_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n1_60', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n2_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n2_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n2_60', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n3_15', (1,1,1,1,1,1,0,0,0,0,0,0,0)),
            ('n3_30', (0,1,1,1,1,1,0,0,0,0,0,0,0)),
            ('n3_60', (0,1,1,1,1,1,0,0,0,0,0,0,0)),
            ('n5_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n5_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n5_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n7_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n7_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n7_60', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n8_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n8_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n8_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n12_15', (1,1,1,0,0,0,0,0,0,0,0,0,0)),
            ('n12_30', (0,1,1,0,0,0,0,0,0,0,0,0,0)),
            ('n12_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n20_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n20_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n20_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n25_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n25_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n25_60', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n28_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n28_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n28_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n34_15', (1,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n34_30', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n34_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n38_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n38_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n38_60', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n39_15', (1,1,1,1,1,1,1,0,0,0,0,0,0)),
            ('n39_30', (0,1,1,1,1,1,1,0,0,0,0,0,0)),
            ('n39_60', (0,1,1,1,1,1,1,0,0,0,0,0,0)),
            ('n40_15', (1,1,1,1,1,1,1,1,0,0,0,0,0)),
            ('n40_30', (0,1,1,1,1,1,1,1,1,0,1,0,1)),
            ('n40_60', (0,1,1,1,1,1,1,1,1,0,1,0,1)),
            ('n41_15', (0,1,1,1,0,0,1,1,0,0,0,0,0)),
            ('n41_30', (0,1,1,1,0,0,1,1,1,1,1,1,1)),
            ('n41_60', (0,1,1,1,0,0,1,1,1,1,1,1,1)),
            ('n50_15', (1,1,1,1,0,0,1,1,0,0,0,0,0)),
            ('n50_30', (0,1,1,1,0,0,1,1,1,0,1,0,0)),
            ('n50_60', (0,1,1,1,0,0,1,1,1,0,1,0,0)),
            ('n51_15', (1,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n51_30', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n51_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n66_15', (1,1,1,1,0,0,1,0,0,0,0,0,0)),
            ('n66_30', (0,1,1,1,0,0,1,0,0,0,0,0,0)),
            ('n66_60', (0,1,1,1,0,0,1,0,0,0,0,0,0)),
            ('n70_15', (1,1,1,1,1,0,0,0,0,0,0,0,0)),
            ('n70_30', (0,1,1,1,1,0,0,0,0,0,0,0,0)),
            ('n70_60', (0,1,1,1,1,0,0,0,0,0,0,0,0)),
            ('n71_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n71_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n71_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n74_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n74_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n74_60', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n75_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n75_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n75_60', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n76_15', (1,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n76_30', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n76_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n77_15', (0,1,1,1,0,1,1,1,0,0,0,0,0)),
            ('n77_30', (0,1,1,1,0,1,1,1,1,1,1,1,1)),
            ('n77_60', (0,1,1,1,0,1,1,1,1,1,1,1,1)),
            ('n78_15', (0,1,1,1,0,1,1,1,0,0,0,0,0)),
            ('n78_30', (0,1,1,1,0,1,1,1,1,1,1,1,1)),
            ('n78_60', (0,1,1,1,0,1,1,1,1,1,1,1,1)),
            ('n79_15', (0,0,0,0,0,0,1,1,0,0,0,0,0)),
            ('n79_30', (0,0,0,0,0,0,1,1,1,0,1,0,1)),
            ('n79_60', (0,0,0,0,0,0,1,1,1,0,1,0,1)),
            ('n80_15', (1,1,1,1,1,1,0,0,0,0,0,0,0)),
            ('n80_30', (0,1,1,1,1,1,0,0,0,0,0,0,0)),
            ('n80_60', (0,1,1,1,1,1,0,0,0,0,0,0,0)),
            ('n81_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n81_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n81_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n82_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n82_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n82_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n83_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n83_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n83_60', (0,0,0,0,0,0,0,0,0,0,0,0,0)),
            ('n84_15', (1,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n84_30', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n84_60', (0,1,1,1,0,0,0,0,0,0,0,0,0)),
            ('n86_15', (1,1,1,1,0,0,1,0,0,0,0,0,0)),
            ('n86_30', (0,1,1,1,0,0,1,0,0,0,0,0,0)),
            ('n86_60', (0,1,1,1,0,0,1,0,0,0,0,0,0)),
            ))
        #Table 5.3.5-2: BS channel bandwidths and SCS per operating band in FR2
        self.nrBandScs2BwFr2 = OrderedDict(( 
            ('n257_60', (1,1,1,0)),
            ('n257_120', (1,1,1,1)),
            ('n258_60', (1,1,1,0)),
            ('n258_120', (1,1,1,1)),
            ('n260_60', (1,1,1,0)),
            ('n260_120', (1,1,1,1)),
            ('n261_60', (1,1,1,0)),
            ('n261_120', (1,1,1,1)),
            ))
        self.validateScsPerBandFr1()
        
        #refer to 3GPP 38.104 vf30
        #Table 5.3.2-1: Transmission bandwidth configuration N_RB for FR1
        self.nrNrbFr1 = {
            15: (25, 52, 79, 106, 133, 160, 216, 270, 0, 0, 0, 0, 0),
            30: (11, 24, 38, 51, 65, 78, 106, 133, 162, 189, 217, 245, 273),
            60: (0, 11, 18, 24, 31, 38, 51, 65, 79, 93, 107, 121, 135),
            }
        #Table 5.3.2-2: Transmission bandwidth configuration N_RB for FR2
        self.nrNrbFr2 = {
            60: (66, 132, 264, 0),
            120: (32, 66, 132, 264),
            }
        
        #refer to 3GPP 38.104 vf30
        #Table 5.3.3-1: Minimum guardband (kHz) (FR1)
        self.nrMinGuardBandFr1 = {
            15: (2, 2, 3, 3, 3, 4, 4, 4, 0, 0, 0, 0, 0),
            30: (2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3),
            60: (0, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 2, 2),
            }
        #Table: 5.3.3-2: Minimum guardband (kHz) (FR2)
        self.nrMinGuardBandFr2 = {
            60: (2, 4, 7, 0),
            120: (2, 2, 4, 7),
            }
        
        #refer to 3GPP 38.104 vf30
        #Table: 5.3.3-3: Minimum guardband (kHz) of SCS 240 kHz SS/PBCH block (FR2)
        self.nrSsbMinGuardBandScs240k = (0, 2, 3, 6)
        
        #refer to 3GPP 38.104 vf30
        #Table 5.4.3.3-1: Applicable SS raster entries per operating band (FR1)
        #Table 5.4.3.3-2: Applicable SS raster entries per operating band (FR2)
        self.nrSsbRasters = {
            'n1': (('15KHz', 'Case A', '5279-<1>-5419'),),
            'n2': (('15KHz', 'Case A', '4829-<1>-4969'),),
            'n3': (('15KHz', 'Case A', '4517-<1>-4693'),),
            'n5': (('15KHz', 'Case A', '2177-<1>-2230'), ('30KHz', 'Case B', '2183-<1>-2224')),
            'n7': (('15KHz', 'Case A', '6554-<1>-6718'),),
            'n8': (('15KHz', 'Case A', '2318-<1>-2395'),),
            'n12': (('15KHz', 'Case A', '1828-<1>-1858'),),
            'n20': (('15KHz', 'Case A', '1982-<1>-2047'),),
            'n25': (('15KHz', 'Case A', '4829-<1>-4981'),),
            'n28': (('15KHz', 'Case A', '1901-<1>-2002'),),
            'n34': (('15KHz', 'Case A', '5030-<1>-5056'),),
            'n38': (('15KHz', 'Case A', '6431-<1>-6544'),),
            'n39': (('15KHz', 'Case A', '4706-<1>-4795'),),
            'n40': (('15KHz', 'Case A', '5756-<1>-5995'),),
            'n41': (('15KHz', 'Case A', '6246-<3>-6717'), ('30KHz', 'Case C', '6252-<3>-6714')),
            'n50': (('15KHz', 'Case A', '3584-<1>-3787'),),
            'n51': (('15KHz', 'Case A', '3572-<1>-3574'),),
            'n66': (('15KHz', 'Case A', '5279-<1>-5494'), ('30KHz', 'Case B', '5285-<1>-5488')),
            'n70': (('15KHz', 'Case A', '4993-<1>-5044'),),
            'n71': (('15KHz', 'Case A', '1547-<1>-1624'),),
            'n74': (('15KHz', 'Case A', '3692-<1>-3790'),),
            'n75': (('15KHz', 'Case A', '3584-<1>-3787'),),
            'n76': (('15KHz', 'Case A', '3572-<1>-3574'),),
            'n77': (('30KHz', 'Case C', '7711-<1>-8329'),),
            'n78': (('30KHz', 'Case C', '7711-<1>-8051'),),
            'n79': (('30KHz', 'Case C', '8480-<16>-8880'),),
            'n257': (('120KHz', 'Case D', '22388-<1>-22558'), ('240KHz', 'Case E', '22390-<2>-22556')),
            'n258': (('120KHz', 'Case D', '22257-<1>-22443'), ('240KHz', 'Case E', '22258-<2>-22442')),
            'n260': (('120KHz', 'Case D', '22995-<1>-23166'), ('240KHz', 'Case E', '22996-<2>-23164')),
            'n261': (('120KHz', 'Case D', '22446-<1>-22492'), ('240KHz', 'Case E', '22446-<2>-22490')),
            }
        
        #refer to 3GPP 38.213 vf30
        #Table 13-1: Set of resource blocks and slot symbols of control resource set for Type0-PDCCH search space when {SS/PBCH block, PDCCH} subcarrier spacing is {15, 15} kHz for frequency bands with minimum channel bandwidth 5 MHz or 10 MHz
        #Table 13-2: Set of resource blocks and slot symbols of control resource set for Type0-PDCCH search space when {SS/PBCH block, PDCCH} subcarrier spacing is {15, 30} kHz for frequency bands with minimum channel bandwidth 5 MHz or 10 MHz
        #Table 13-3: Set of resource blocks and slot symbols of control resource set for Type0-PDCCH search space when {SS/PBCH block, PDCCH} subcarrier spacing is {30, 15} kHz for frequency bands with minimum channel bandwidth 5 MHz or 10 MHz
        #Table 13-4: Set of resource blocks and slot symbols of control resource set for Type0-PDCCH search space when {SS/PBCH block, PDCCH} subcarrier spacing is {30, 30} kHz for frequency bands with minimum channel bandwidth 5 MHz or 10 MHz
        #table for FR1 with minimum channel bandwidth of 5MHz/10MHz
        self.nrCoreset0Fr1MinChBw5m10m = {
            '15_15_0' : (1,24,2,(0,)),
            '15_15_1' : (1,24,2,(2,)),
            '15_15_2' : (1,24,2,(4,)),
            '15_15_3' : (1,24,3,(0,)),
            '15_15_4' : (1,24,3,(2,)),
            '15_15_5' : (1,24,3,(4,)),
            '15_15_6' : (1,48,1,(12,)),
            '15_15_7' : (1,48,1,(16,)),
            '15_15_8' : (1,48,2,(12,)),
            '15_15_9' : (1,48,2,(16,)),
            '15_15_10' : (1,48,3,(12,)),
            '15_15_11' : (1,48,3,(16,)),
            '15_15_12' : (1,96,1,(38,)),
            '15_15_13' : (1,96,2,(38,)),
            '15_15_14' : (1,96,3,(38,)),
            '15_15_15' : None,
            '15_30_0' : (1,24,2,(5,)),
            '15_30_1' : (1,24,2,(6,)),
            '15_30_2' : (1,24,2,(7,)),
            '15_30_3' : (1,24,2,(8,)),
            '15_30_4' : (1,24,3,(5,)),
            '15_30_5' : (1,24,3,(6,)),
            '15_30_6' : (1,24,3,(7,)),
            '15_30_7' : (1,24,3,(8,)),
            '15_30_8' : (1,48,1,(18,)),
            '15_30_9' : (1,48,1,(20,)),
            '15_30_10' : (1,48,2,(18,)),
            '15_30_11' : (1,48,2,(20,)),
            '15_30_12' : (1,48,3,(18,)),
            '15_30_13' : (1,48,3,(20,)),
            '15_30_14' : None,
            '15_30_15' : None,
            '30_15_0' : (1,48,1,(2,)),
            '30_15_1' : (1,48,1,(6,)),
            '30_15_2' : (1,48,2,(2,)),
            '30_15_3' : (1,48,2,(6,)),
            '30_15_4' : (1,48,3,(2,)),
            '30_15_5' : (1,48,3,(6,)),
            '30_15_6' : (1,96,1,(28,)),
            '30_15_7' : (1,96,2,(28,)),
            '30_15_8' : (1,96,3,(28,)),
            '30_15_9' : None,
            '30_15_10' : None,
            '30_15_11' : None,
            '30_15_12' : None,
            '30_15_13' : None,
            '30_15_14' : None,
            '30_15_15' : None,
            '30_30_0' : (1,24,2,(0,)),
            '30_30_1' : (1,24,2,(1,)),
            '30_30_2' : (1,24,2,(2,)),
            '30_30_3' : (1,24,2,(3,)),
            '30_30_4' : (1,24,2,(4,)),
            '30_30_5' : (1,24,3,(0,)),
            '30_30_6' : (1,24,3,(1,)),
            '30_30_7' : (1,24,3,(2,)),
            '30_30_8' : (1,24,3,(3,)),
            '30_30_9' : (1,24,3,(4,)),
            '30_30_10' : (1,48,1,(12,)),
            '30_30_11' : (1,48,1,(14,)),
            '30_30_12' : (1,48,1,(16,)),
            '30_30_13' : (1,48,2,(12,)),
            '30_30_14' : (1,48,2,(14,)),
            '30_30_15' : (1,48,2,(16,)),
            }
            
        #Table 13-5: Set of resource blocks and slot symbols of control resource set for Type0-PDCCH search space when {SS/PBCH block, PDCCH} subcarrier spacing is {30, 15} kHz for frequency bands with minimum channel bandwidth 40MHz
        #Table 13-6: Set of resource blocks and slot symbols of control resource set for Type0-PDCCH search space when {SS/PBCH block, PDCCH} subcarrier spacing is {30, 30} kHz for frequency bands with minimum channel bandwidth 40MHz
        #table for FR1 with minimum channel bandwidth of 40MHz
        self.nrCoreset0Fr1MinChBw40m = {
            '30_15_0' : (1,48,1,(4,)),
            '30_15_1' : (1,48,2,(4,)),
            '30_15_2' : (1,48,3,(4,)),
            '30_15_3' : (1,96,1,(0,)),
            '30_15_4' : (1,96,1,(56,)),
            '30_15_5' : (1,96,2,(0,)),
            '30_15_6' : (1,96,2,(56,)),
            '30_15_7' : (1,96,3,(0,)),
            '30_15_8' : (1,96,3,(56,)),
            '30_15_9' : None,
            '30_15_10' : None,
            '30_15_11' : None,
            '30_15_12' : None,
            '30_15_13' : None,
            '30_15_14' : None,
            '30_15_15' : None,
            '30_30_0' : (1,24,2,(0,)),
            '30_30_1' : (1,24,2,(4,)),
            '30_30_2' : (1,24,3,(0,)),
            '30_30_3' : (1,24,3,(4,)),
            '30_30_4' : (1,48,1,(0,)),
            '30_30_5' : (1,48,1,(28,)),
            '30_30_6' : (1,48,2,(0,)),
            '30_30_7' : (1,48,2,(28,)),
            '30_30_8' : (1,48,3,(0,)),
            '30_30_9' : (1,48,3,(28,)),
            '30_30_10' : None,
            '30_30_11' : None,
            '30_30_12' : None,
            '30_30_13' : None,
            '30_30_14' : None,
            '30_30_15' : None,
            }
        
        #Table 13-7: Set of resource blocks and slot symbols of control resource set for Type0-PDCCH search space when {SS/PBCH block, PDCCH} subcarrier spacing is {120, 60} kHz
        #Table 13-8: Set of resource blocks and slot symbols of control resource set for Type0-PDCCH search space when {SS/PBCH block, PDCCH} subcarrier spacing is {120, 120} kHz
        #Table 13-9: Set of resource blocks and slot symbols of control resource set for Type0-PDCCH search space when {SS/PBCH block, PDCCH} subcarrier spacing is {240, 60} kHz
        #Table 13-10: Set of resource blocks and slot symbols of control resource set for Type0-PDCCH search space when {SS/PBCH block, PDCCH} subcarrier spacing is {240, 120} kHz
        #table for FR2
        self.nrCoreset0Fr2 = {
            '120_60_0' : (1,48,1,(0,)),
            '120_60_1' : (1,48,1,(8,)),
            '120_60_2' : (1,48,2,(0,)),
            '120_60_3' : (1,48,2,(8,)),
            '120_60_4' : (1,48,3,(0,)),
            '120_60_5' : (1,48,3,(8,)),
            '120_60_6' : (1,96,1,(28,)),
            '120_60_7' : (1,96,2,(28,)),
            '120_60_8' : (2,48,1,(-41,-42,)),
            '120_60_9' : (2,48,1,(49,)),
            '120_60_10' : (2,96,1,(-41,-42,)),
            '120_60_11' : (2,96,1,(97,)),
            '120_60_12' : None,
            '120_60_13' : None,
            '120_60_14' : None,
            '120_60_15' : None,
            '120_120_0' : (1,24,2,(0,)),
            '120_120_1' : (1,24,2,(4,)),
            '120_120_2' : (1,48,1,(14,)),
            '120_120_3' : (1,48,2,(14,)),
            '120_120_4' : (3,24,2,(-20,-21,)),
            '120_120_5' : (3,24,2,(24,)),
            '120_120_6' : (3,48,2,(-20,-21,)),
            '120_120_7' : (3,48,2,(48,)),
            '120_120_8' : None,
            '120_120_9' : None,
            '120_120_10' : None,
            '120_120_11' : None,
            '120_120_12' : None,
            '120_120_13' : None,
            '120_120_14' : None,
            '120_120_15' : None,
            '240_60_0' : (1,96,1,(0,)),
            '240_60_1' : (1,96,1,(16,)),
            '240_60_2' : (1,96,2,(0,)),
            '240_60_3' : (1,96,2,(16,)),
            '240_60_4' : None,
            '240_60_5' : None,
            '240_60_6' : None,
            '240_60_7' : None,
            '240_60_8' : None,
            '240_60_9' : None,
            '240_60_10' : None,
            '240_60_11' : None,
            '240_60_12' : None,
            '240_60_13' : None,
            '240_60_14' : None,
            '240_60_15' : None,
            '240_120_0' : (1,48,1,(0,)),
            '240_120_1' : (1,48,1,(8,)),
            '240_120_2' : (1,48,2,(0,)),
            '240_120_3' : (1,48,2,(8,)),
            '240_120_4' : (2,24,1,(-41,-42,)),
            '240_120_5' : (2,24,1,(25,)),
            '240_120_6' : (2,48,1,(-41,-42,)),
            '240_120_7' : (2,48,1,(49,)),
            '240_120_8' : None,
            '240_120_9' : None,
            '240_120_10' : None,
            '240_120_11' : None,
            '240_120_12' : None,
            '240_120_13' : None,
            '240_120_14' : None,
            '240_120_15' : None,
            }
        
        #offset of CORESET0 w.r.t. SSB
        self.nrCoreset0Offset = 0
        #minimum channel bandwidth
        self.minChBw = 0
        
    def validateScsPerBandFr1(self):
        self.nrScsPerBandFr1 = dict()
        for key,val in self.nrBandScs2BwFr1.items():
            if val.count(1) == 0:
                continue
            band, scs = key.split('_')
            #FIXME 60KHz scs is not supported, although 60KHz is specified in transmission bandwidth table of FR1 in 38.104 vf3  
            if scs == '60':
                continue
            if not band in self.nrScsPerBandFr1:
                self.nrScsPerBandFr1[band] = [scs+'KHz']
            else:
                self.nrScsPerBandFr1[band].append(scs+'KHz')
        
        '''
        for key,val in self.nrScsPerBandFr1.items():
            self.ngwin.logEdit.append('key=%s,val=%s' % (key,val))
        '''

    def updateKSsbAndNCrbSsb(self, offset):
        #NOTE:
        #(a) offset in scsCommon, which equals to scsCarrier;
        #(b) and offset > 0;
        if not self.nrMinGuardBandEdit.text():
            return
        
        #refer to 3GPP 38.211 vf30
        #7.4.3.1	Time-frequency structure of an SS/PBCH block
        '''
        For FR1, k_ssb and n_crb_ssb based on 15k
        For FR2, k_ssb based on carrier_scs, n_crb_ssb based on 60k

        FR1/FR2   carrier_scs   ssb_scs     k_ssb	n_crb_ssb
        -----------------------------------------------------------
        FR1	        15k         15k         0~11	minGuardBand+offset
                    15k         30k         0~11	minGuardBand+offset
                    30k         15k         0~23	2*(minGuardBand+offset)
                    30k         30k         0~23	2*(minGuardBand+offset)
        FR2         60k         120k        0~11	minGuardBand+offset
                    60k         240k        0~11	max(minGuardBand+offset,4*minGuardBand240k)
                    120k        120k        0~11	2*(minGuardBand+offset)
                    120k        240k        0~11	max(2*(minGuardBand+offset),4*minGuardBand240k)
        -----------------------------------------------------------
        '''
        key = self.nrCarrierScsComb.currentText()[:-3] + '_' + self.nrSsbScsComb.currentText()[:-3]
        minGuardBand = int(self.nrMinGuardBandEdit.text())
        if key in ('15_15', '15_30', '60_120'):
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            self.nrSsbNCrbSsbEdit.setText(str(minGuardBand+offset))
        elif key in ('30_15', '30_30'):
            self.nrSsbKssbLabel.setText('k_SSB[0-23]:')
            self.nrSsbNCrbSsbEdit.setText(str(2*(minGuardBand+offset)))
        elif key == '60_240':
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            minGuardBand240k = int(self.nrSsbMinGuardBandScs240kEdit.text())
            self.nrSsbNCrbSsbEdit.setText(str(max(minGuardBand+offset, 4*minGuardBand240k)))
        elif key == '120_120':
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            self.nrSsbNCrbSsbEdit.setText(str(2*(minGuardBand+offset)))
        elif key == '120_240':
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            minGuardBand240k = int(self.nrSsbMinGuardBandScs240kEdit.text())
            self.nrSsbNCrbSsbEdit.setText(str(max(2*(minGuardBand+offset), 4*minGuardBand240k)))
        else:
            pass
    
    def onCarrierBandCombCurrentIndexChanged(self, index):
        self.ngwin.logEdit.append('-->inside onCarrierBandCombCurrentIndexChanged, index=%d' % index)
        if index < 0:
            return

        #(1) update band info
        ulBand, dlBand, self.duplexMode, self.maxL = self.nrOpBands[self.nrCarrierBandComb.currentText()]
        self.freqRange = 'FR1' if int(self.nrCarrierBandComb.currentText()[1:]) <= 256 else 'FR2'
        if self.duplexMode == 'TDD':
            self.nrCarrierBandInfoLabel.setText('<font color=green>UL/DL: %s, %s, %s</font>' % (ulBand, self.duplexMode, self.freqRange))
        else:
            self.nrCarrierBandInfoLabel.setText('<font color=green>UL: %s, DL: %s, %s, %s</font>' % (ulBand, dlBand, self.duplexMode, self.freqRange))

        if self.duplexMode in ('SUL', 'SDL'):
            self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: SUL/SDL bands (3GPP 38.104 vf30, SDL: n75/n76, SUL: n80/n81/n82/n83/n84/n86)'
                                      ' are not supported!' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            return

        #(2) update SSB sucarrier spacing
        #nrScsSet = ('15Khz', '30KHz', '60KHz', '120KHz', '240KHz')
        ssbScsSubset = [v[0] for v in self.nrSsbRasters[self.nrCarrierBandComb.currentText()]]
        self.nrSsbScsComb.clear()
        self.nrSsbScsComb.addItems(ssbScsSubset)
        self.nrSsbScsComb.setCurrentIndex(0)

        #(3) update carrier subcarrier spacing
        #nrScsSet = ('15Khz', '30KHz', '60KHz', '120KHz', '240KHz')
        if self.freqRange == 'FR1':
            scsSubset = self.nrScsPerBandFr1[self.nrCarrierBandComb.currentText()]
        else:
            scsSubset = ('60KHz', '120KHz')
        self.nrCarrierScsComb.clear()
        self.nrCarrierScsComb.addItems(scsSubset)
        self.nrCarrierScsComb.setCurrentIndex(0)
        
        #(4) update SSB
        if self.maxL in (4, 8):
            self.nrSsbInOneGrpEdit.setText('11110000' if self.maxL == 4 else '11111111')
            self.nrSsbGrpPresenceEdit.setText('NA')
            self.nrSsbGrpPresenceEdit.setEnabled(False)
        else:
            self.nrSsbInOneGrpEdit.setText('11111111')
            self.nrSsbGrpPresenceEdit.setText('11111111')
            self.nrSsbGrpPresenceEdit.setEnabled(True)

    def onCarrierScsCombCurrentIndexChanged(self, index):
        self.ngwin.logEdit.append('-->inside onCarrierScsCombCurrentIndexChanged, index=%d' % index)
        if index < 0:
            return
        
        #(1) update scsCommon and refScs
        self.nrMibScsCommonComb.setCurrentText(self.nrCarrierScsComb.currentText())
        self.nrTddCfgRefScsComb.setCurrentText(self.nrCarrierScsComb.currentText())

        #(2) update transmission bandwidth
        key = self.nrCarrierBandComb.currentText() + '_' + self.nrCarrierScsComb.currentText()[:-3]
        if not key in self.nrBandScs2BwFr1 and not key in self.nrBandScs2BwFr2:
            return
        if self.freqRange == 'FR1':
            bwSubset = [self.nrBwSetFr1[i] for i in range(len(self.nrBwSetFr1)) if self.nrBandScs2BwFr1[key][i]]
        else:
            bwSubset = [self.nrBwSetFr2[i] for i in range(len(self.nrBwSetFr2)) if self.nrBandScs2BwFr2[key][i]]
        
        #min channel bw used in Type-0 CSS determination
        self.minChBw = int(bwSubset[0][:-3]) if len(bwSubset) > 0 else 0 

        self.nrCarrierBwComb.clear()
        self.nrCarrierBwComb.addItems(bwSubset)
        self.nrCarrierBwComb.setCurrentIndex(0)
        
        #(3) validate CORESET0 and update n_CRB_SSB when necessary
        if self.nrMibCoreset0Edit.text():
            self.flagCoreset0 = self.validateCoreset0()
            if self.flagCoreset0:
                self.updateKSsbAndNCrbSsb(offset=0 if self.nrCoreset0Offset <= 0 else self.nrCoreset0Offset)

    def onCarrierBwCombCurrentIndexChanged(self, index):
        self.ngwin.logEdit.append('-->inside onCarrierBwCombCurrentIndexChanged, index=%d' % index)
        if index < 0:
            return

        #(1) update N_RB w.r.t carrierScs and carrierBw
        key = int(self.nrCarrierScsComb.currentText()[:-3])
        if not key in self.nrNrbFr1 and not key in self.nrNrbFr2:
            return

        if self.freqRange == 'FR1':
            numRb = self.nrNrbFr1[key][self.nrBwSetFr1.index(self.nrCarrierBwComb.currentText())]
        else:
            numRb = self.nrNrbFr2[key][self.nrBwSetFr2.index(self.nrCarrierBwComb.currentText())]
        self.nrCarrierNumRbEdit.setText(str(numRb))

        #(2) update minGuardBand w.r.t carrierScs and carrierBw
        if self.freqRange == 'FR1':
            minGuardBand = self.nrMinGuardBandFr1[key][self.nrBwSetFr1.index(self.nrCarrierBwComb.currentText())]
        else:
            minGuardBand = self.nrMinGuardBandFr2[key][self.nrBwSetFr2.index(self.nrCarrierBwComb.currentText())]
        self.nrMinGuardBandEdit.setText(str(minGuardBand))

        #(3) update minGuardBandScs240k w.r.t. ssbScs and carrierBw
        if self.freqRange == 'FR2' and self.nrSsbScsComb.currentText() == '240KHz':
            carrierBw = int(self.nrCarrierBwComb.currentText()[:-3])
            if carrierBw < 100:
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Minimum transmission bandwidth is 100MHz when SSB'
                                          ' subcarrier spacing is 240KHz!' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                self.nrSsbMinGuardBandScs240kEdit.setText('NA')
            else:
                self.nrSsbMinGuardBandScs240kEdit.setText(str(self.nrSsbMinGuardBandScs240k[self.nrCarrierBwComb.currentIndex()]))
                
        #(4) validate CORESET0 and update n_CRB_SSB when necessary
        if self.nrMibCoreset0Edit.text():
            self.flagCoreset0 = self.validateCoreset0()
            if self.flagCoreset0:
                self.updateKSsbAndNCrbSsb(offset=0 if self.nrCoreset0Offset <= 0 else self.nrCoreset0Offset)

    def onSsbScsCombCurrentIndexChanged(self, index):
        self.ngwin.logEdit.append('-->inside onSsbScsCombCurrentIndexChanged, index=%d' % index)
        if index < 0:
            return

        #(1) update SSB pattern
        ssbScs, ssbPat, ssbGscn = self.nrSsbRasters[self.nrCarrierBandComb.currentText()][self.nrSsbScsComb.currentIndex()]
        self.nrSsbPatternEdit.setText(ssbPat)

        #(2) update minGuardBandScs240k
        if ssbScs == '240KHz':
            carrierBw = int(self.nrCarrierBwComb.currentText()[:-3])
            if carrierBw < 100:
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Minimum transmission bandwidth is 100MHz when SSB'
                                          'subcarrier spacing is 240KHz!' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                self.nrSsbMinGuardBandScs240kEdit.setText('NA')
                return
            else:
                self.nrSsbMinGuardBandScs240kEdit.setText(str(self.nrSsbMinGuardBandScs240k[self.nrCarrierBwComb.currentIndex()]))
        else:
            self.nrSsbMinGuardBandScs240kEdit.setText('NA')
        
        #(3) validate CORESET0 and update n_CRB_SSB when necessary
        if self.nrMibCoreset0Edit.text():
            self.flagCoreset0 = self.validateCoreset0()
            if self.flagCoreset0:
                self.updateKSsbAndNCrbSsb(offset=0 if self.nrCoreset0Offset <= 0 else self.nrCoreset0Offset)
    
    def onUssPeriodicityCombCurrentIndexChanged(self, index):
        self.ngwin.logEdit.append('-->inside onUssPeriodicityCombCurrentIndexChanged, index=%d' % index)
        if index < 0:
            return
        
        period = int(self.nrUssPeriodicityComb.currentText()[2:])
        self.nrUssSlotOffsetEdit.clear()
        self.nrUssDurationEdit.clear()
        if period > 1:
            self.nrUssSlotOffsetLabel.setText('monitoringSlotOffset[0-%s]:' % str(period-1))
        else:
            self.nrUssSlotOffsetLabel.setText('monitoringSlotOffset[0]:')
                
        self.nrUssSlotOffsetEdit.setText('0')
        
        if period in (1, 2):
            self.nrUssDurationLabel.setText('duration[1]:')
            self.nrUssDurationEdit.setText('1')
        else:
            self.nrUssDurationLabel.setText('duration[1-%s]:' % str(period-1))
            self.nrUssDurationEdit.setText(str(period-1))
            
    def validateCoreset0(self):
        self.ngwin.logEdit.append('-->inside validateCoreset0')
        #(1) validate controlResourceSetZero
        key = self.nrSsbScsComb.currentText()[:-3] + '_' + self.nrMibScsCommonComb.currentText()[:-3] + '_' + self.nrMibCoreset0Edit.text()
        if self.freqRange == 'FR1' and self.minChBw in (5, 10):
            if not key in self.nrCoreset0Fr1MinChBw5m10m.keys():
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid key(=%s) when referring nrCoreset0Fr1MinChBw5m10m!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return False 
            
            if self.nrCoreset0Fr1MinChBw5m10m[key] is None:
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid value of controlResourceSetZero(=%s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrMibCoreset0Edit.text()))
                return False
            
            val = self.nrCoreset0Fr1MinChBw5m10m[key]
        elif self.freqRange == 'FR1' and self.minChBw == 40:
            if not key in self.nrCoreset0Fr1MinChBw40m.keys():
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid key(=%s) when referring nrCoreset0Fr1MinChBw40m!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return False
            
            if self.nrCoreset0Fr1MinChBw40m[key] is None:
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid value of controlResourceSetZero(=%s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrMibCoreset0Edit.text()))
                return False
            
            val = self.nrCoreset0Fr1MinChBw40m[key]
        elif self.freqRange == 'FR2':
            if not key in self.nrCoreset0Fr2.keys():
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid key(=%s) when referring nrCoreset0Fr2!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return False
            
            if self.nrCoreset0Fr2[key] is None:
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid value of controlResourceSetZero(=%s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrMibCoreset0Edit.text()))
                return False
            
            val = self.nrCoreset0Fr2[key]
        else:
            return False
            
        #(2) validate CORESET0 bw against carrier bw
        self.nrSsbCoreset0MultiplexingPat, self.nrCoreset0NumRbs, self.nrCoreset0NumSymbs, self.nrCoreset0OffsetList = val
        if int(self.nrCarrierNumRbEdit.text()) < self.nrCoreset0NumRbs:
            self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid CORESET0 setting: CORESET0 numRBs=%d, while carrier numRBs=%s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrCoreset0NumRbs, self.nrCarrierNumRbEdit.text()))
            return False
        
        #(3) if k_ssb is configured, further validate CORESET0
        if self.nrSsbKssbEdit.text():
            kSsb = int(self.nrSsbKssbEdit.text())
            if len(self.nrCoreset0OffsetList) == 2:
                self.nrCoreset0Offset = self.nrCoreset0OffsetList[0] if kSsb == 0 else self.nrCoreset0OffsetList[1] 
            else:
                self.nrCoreset0Offset = self.nrCoreset0OffsetList[0]
                
            '''
            if offset > 0, min bw = max(self.nrCoreset0NumRbs, offset + 20 * scsSsb / scsPdcch), and n_CRB_SSB needs update w.r.t to offset
            if offset <= 0, min bw = self.nrCoreset0NumRbs - offset, and don't have to update n_CRB_SSB
            '''
            if self.nrCoreset0Offset > 0:
                minBw = max(self.nrCoreset0NumRbs, self.nrCoreset0Offset + 20 * int(self.nrSsbScsComb.currentText()[:-3]) / int(self.nrCarrierScsComb.currentText()[:-3]))
            else:
                minBw = self.nrCoreset0NumRbs - self.nrCoreset0Offset
            
            if int(self.nrCarrierNumRbEdit.text()) < minBw:
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid CORESET0 setting: CORESET0 numRBs=%d, offset=%d, minBw = %d, while carrier numRBs=%s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrCoreset0NumRbs, self.nrCoreset0Offset, minBw, self.nrCarrierNumRbEdit.text()))
                return False
        
        #when validation passed
        return True
    
    def onMibCoreset0EditEditingFinished(self):
        self.ngwin.logEdit.append('-->inside onMibCoreset0EditEditingFinished')
        #(1) validate CORESET0 and update n_CRB_SSB when necessary
        if self.nrMibCoreset0Edit.text():
            self.flagCoreset0 = self.validateCoreset0()
            if self.flagCoreset0:
                self.updateKSsbAndNCrbSsb(offset=0 if self.nrCoreset0Offset <= 0 else self.nrCoreset0Offset)
                
    def onSsbKssbEditEditingFinished(self):
        self.ngwin.logEdit.append('-->inside onSsbKssbEditEditingFinished')
        #(1) validate CORESET0 and update n_CRB_SSB when necessary
        if self.nrMibCoreset0Edit.text():
            self.flagCoreset0 = self.validateCoreset0()
            if self.flagCoreset0:
                self.updateKSsbAndNCrbSsb(offset=0 if self.nrCoreset0Offset <= 0 else self.nrCoreset0Offset)

    def onOkBtnClicked(self):
        self.ngwin.logEdit.append('-->inside onOkBtnClicked')
        #TODO
        self.accept()
