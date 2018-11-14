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
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QTabWidget, QWidget
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
        gridCfgWidget = QWidget()
        gridCfgLayout = QVBoxLayout()

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

        gridCfgLayout.addLayout(gridLayoutResGridCfg)
        gridCfgLayout.addStretch()
        gridCfgWidget.setLayout(gridCfgLayout)
        
        #-->(2) SSB settings tab
        ssbCfgWidget = QWidget()
        ssbCfgLayout = QVBoxLayout()
        
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
        
        ssbCfgLayout.addLayout(pciLayout)
        ssbCfgLayout.addLayout(gridLayoutSsbCfg)
        ssbCfgLayout.addStretch()
        ssbCfgWidget.setLayout(ssbCfgLayout)
        
        #-->(3) PDCCH settings tab
        pdcchCfgWidget = QWidget()
        pdcchCfgLayout = QVBoxLayout()
        
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
        
        pdcchTabWidget = QTabWidget()
        
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
        
        pdcchTabWidget.addTab(coreset1Widget, 'CORESET 1')
        pdcchTabWidget.addTab(ussWidget, 'USS')
        
        pdcchCfgLayout.addWidget(css0GrpBox)
        pdcchCfgLayout.addWidget(pdcchTabWidget)
        pdcchCfgLayout.addStretch()
        pdcchCfgWidget.setLayout(pdcchCfgLayout)
        
        #-->(4) PDSCH settings tab
        
        #-->(5) PRACH settings tab
        
        #-->(6) PUCCH settings tab
        
        #-->(7) SRS settings tab
        
        #-->(8) PUSCH settings tab
        
        #-->(9) BWP settings tab
        #including initial active DL BWP, dedicated active DL BWP, initial active UL BWP, dedicated active UL BWP
        
        
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
        if self.maxL < 64:
            self.nrSsbGrpPresenceEdit.setText('NA')
            self.nrSsbGrpPresenceEdit.setEnabled(False)
        else:
            self.nrSsbGrpPresenceEdit.setEnabled(True)
            self.nrSsbGrpPresenceEdit.clear()
            self.nrSsbGrpPresenceEdit.setPlaceholderText('11111111')

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
