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
from PyQt5.QtGui import QColor, QIntValidator
from PyQt5.QtCore import Qt

class NgNrGridUi(QDialog):
    def __init__(self, ngwin):
        super().__init__()
        self.ngwin = ngwin
        self.args = dict()
        self.initUi()

    def initUi(self):
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
        self.nrCarrierNumRbEdit.setEnabled(False)

        self.nrMinGuardBandLabel = QLabel('Min guard band(offsetToCarrier):')
        self.nrMinGuardBandEdit = QLineEdit()
        self.nrMinGuardBandEdit.setEnabled(False)

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
        self.nrSsbKssbEdit = QLineEdit('0')
        self.nrSsbKssbEdit.setValidator(QIntValidator(0, 23))

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
        self.nrSsbPciEdit = QLineEdit('0')
        self.nrSsbPciEdit.setValidator(QIntValidator(0, 1007))
        
        #---->(2.2) MIB configurations
        self.nrMibSfnLabel = QLabel('SFN[0-1023]:')
        self.nrMibSfnEdit = QLineEdit('0')
        self.nrMibSfnEdit.setValidator(QIntValidator(0, 1023))
        
        self.nrMibDmRsTypeAPosLabel = QLabel('dmrs-TypeA-Position:')
        self.nrMibDmRsTypeAPosComb = QComboBox()
        self.nrMibDmRsTypeAPosComb.addItems(['pos2', 'pos3'])
        self.nrMibDmRsTypeAPosComb.setCurrentIndex(0)
        
        self.nrMibScsCommonLabel = QLabel('subCarrierSpacingCommon:')
        self.nrMibScsCommonComb = QComboBox()
        self.nrMibScsCommonComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        self.nrMibScsCommonComb.setEnabled(False)
        
        self.nrMibCoreset0Label = QLabel('coresetZero(PDCCH-ConfigSIB1)[0-15]:')
        self.nrMibCoreset0Edit = QLineEdit('0')
        self.nrMibCoreset0Edit.setValidator(QIntValidator(0, 15))
        
        self.nrMibCss0Label = QLabel('searchSpaceZero(PDCCH-ConfigSIB1)[0-15]:')
        self.nrMibCss0Edit = QLineEdit('0')
        self.nrMibCss0Edit.setValidator(QIntValidator(0, 15))
        
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
        self.nrTddCfgPat1NumDlSlotsEdit = QLineEdit('3')
        self.nrTddCfgPat1NumDlSlotsEdit.setValidator(QIntValidator(0, 80))
        
        self.nrTddCfgPat1NumDlSymbsLabel = QLabel('nrofDownlinkSymbols[0-13]:')
        self.nrTddCfgPat1NumDlSymbsEdit = QLineEdit('10')
        self.nrTddCfgPat1NumDlSymbsEdit.setValidator(QIntValidator(0, 13))
        
        self.nrTddCfgPat1NumUlSymbsLabel = QLabel('nrofUplinkSymbols[0-13]:')
        self.nrTddCfgPat1NumUlSymbsEdit = QLineEdit('2')
        self.nrTddCfgPat1NumUlSymbsEdit.setValidator(QIntValidator(0, 13))
        
        self.nrTddCfgPat1NumUlSlotsLabel = QLabel('nrofUplinkSlots[0-80]:')
        self.nrTddCfgPat1NumUlSlotsEdit = QLineEdit('1')
        self.nrTddCfgPat1NumUlSlotsEdit.setValidator(QIntValidator(0, 80))
        
        self.nrTddCfgPat2PeriodLabel = QLabel('dl-UL-TransmissionPeriodicity:')
        self.nrTddCfgPat2PeriodComb = QComboBox()
        self.nrTddCfgPat2PeriodComb.addItems(['not used', '0.5ms', '0.625ms', '1ms', '1.25ms', '2ms', '2.5ms', '3ms', '4ms', '5ms', '10ms'])
        self.nrTddCfgPat2PeriodComb.setCurrentIndex(0)
        
        self.nrTddCfgPat2NumDlSlotsLabel = QLabel('nrofDownlinkSlots[0-80]:')
        self.nrTddCfgPat2NumDlSlotsEdit = QLineEdit()
        self.nrTddCfgPat2NumDlSlotsEdit.setValidator(QIntValidator(0, 80))
        
        self.nrTddCfgPat2NumDlSymbsLabel = QLabel('nrofDownlinkSymbols[0-13]:')
        self.nrTddCfgPat2NumDlSymbsEdit = QLineEdit()
        self.nrTddCfgPat2NumDlSymbsEdit.setValidator(QIntValidator(0, 13))
        
        self.nrTddCfgPat2NumUlSymbsLabel = QLabel('nrofUplinkSymbols[0-13]:')
        self.nrTddCfgPat2NumUlSymbsEdit = QLineEdit()
        self.nrTddCfgPat2NumUlSymbsEdit.setValidator(QIntValidator(0, 13))
        
        self.nrTddCfgPat2NumUlSlotsLabel = QLabel('nrofUplinkSlots[0-80]:')
        self.nrTddCfgPat2NumUlSlotsEdit = QLineEdit()
        self.nrTddCfgPat2NumUlSlotsEdit.setValidator(QIntValidator(0, 80))
        
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
        self.nrCoreset1ShiftIndexEdit = QLineEdit('0')
        self.nrCoreset1ShiftIndexEdit.setValidator(QIntValidator(0, 274))
        
        self.nrCoreset1PrecoderGranularityLabel = QLabel('precoderGranularity:')
        self.nrCoreset1PrecoderGranularityComb = QComboBox()
        self.nrCoreset1PrecoderGranularityComb.addItems(['sameAsREG-bundle', 'allContiguousRBs'])
        self.nrCoreset1PrecoderGranularityComb.setCurrentIndex(0)
        
        coreset1Widget = QWidget()
        coreset1GridLayout = QGridLayout()
        coreset1GridLayout.addWidget(self.nrCoreset1FreqResourcesLabel, 0, 0)
        coreset1GridLayout.addWidget(self.nrCoreset1FreqResourcesEdit, 0, 1)
        coreset1GridLayout.addWidget(self.nrCoreset1DurationLabel, 1, 0)
        coreset1GridLayout.addWidget(self.nrCoreset1DurationComb, 1, 1)
        coreset1GridLayout.addWidget(self.nrCoreset1CceRegMapLabel, 2, 0)
        coreset1GridLayout.addWidget(self.nrCoreset1CceRegMapComb, 2, 1)
        coreset1GridLayout.addWidget(self.nrCoreset1RegBundleSizeLabel, 3, 0)
        coreset1GridLayout.addWidget(self.nrCoreset1RegBundleSizeComb, 3, 1)
        coreset1GridLayout.addWidget(self.nrCoreset1InterleaverSizeLabel, 4, 0)
        coreset1GridLayout.addWidget(self.nrCoreset1InterleaverSizeComb, 4, 1)
        coreset1GridLayout.addWidget(self.nrCoreset1ShiftIndexLabel, 5, 0)
        coreset1GridLayout.addWidget(self.nrCoreset1ShiftIndexEdit, 5, 1)
        coreset1GridLayout.addWidget(self.nrCoreset1PrecoderGranularityLabel, 6, 0)
        coreset1GridLayout.addWidget(self.nrCoreset1PrecoderGranularityComb, 6, 1)
        coreset1Layout = QVBoxLayout()
        coreset1Layout.addLayout(coreset1GridLayout)
        coreset1Layout.addStretch()
        coreset1Widget.setLayout(coreset1Layout) 
        
        #---->(3.3) USS configuratons
        self.nrUssPeriodicityLabel = QLabel('monitoringSlotPeriodicity:')
        self.nrUssPeriodicityComb = QComboBox()
        self.nrUssPeriodicityComb.addItems(['sl1', 'sl2', 'sl4', 'sl5', 'sl8', 'sl10', 'sl16', 'sl20',
                                            'sl40', 'sl80', 'sl160', 'sl320', 'sl640', 'sl1280', 'sl2560'])
        self.nrUssPeriodicityComb.currentIndexChanged[int].connect(self.onUssPeriodicityCombCurrentIndexChanged)
        self.nrUssPeriodicityComb.setCurrentIndex(0)
        
        self.nrUssSlotOffsetLabel = QLabel('monitoringSlotOffset:')
        self.nrUssSlotOffsetEdit = QLineEdit('0')
        
        self.nrUssDurationLabel = QLabel('duration:')
        self.nrUssDurationEdit = QLineEdit('1')
        
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
        ussGridLayout = QGridLayout()
        ussGridLayout.addWidget(self.nrUssPeriodicityLabel, 0, 0)
        ussGridLayout.addWidget(self.nrUssPeriodicityComb, 0, 1)
        ussGridLayout.addWidget(self.nrUssSlotOffsetLabel, 1, 0)
        ussGridLayout.addWidget(self.nrUssSlotOffsetEdit, 1, 1)
        ussGridLayout.addWidget(self.nrUssDurationLabel, 2, 0)
        ussGridLayout.addWidget(self.nrUssDurationEdit, 2, 1)
        ussGridLayout.addWidget(self.nrUssFirstSymbsLabel, 3, 0)
        ussGridLayout.addWidget(self.nrUssFirstSymbsEdit, 3, 1)
        ussGridLayout.addWidget(self.nrUssAggLevelLabel, 4, 0)
        ussGridLayout.addWidget(self.nrUssAggLevelComb, 4, 1)
        ussGridLayout.addWidget(self.nrUssNumCandidatesLabel, 5, 0)
        ussGridLayout.addWidget(self.nrUssNumCandidatesComb, 5, 1)
        ussLayout = QVBoxLayout()
        ussLayout.addLayout(ussGridLayout)
        ussLayout.addStretch()
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
        self.nrDci10Sib1McsEdit.setValidator(QIntValidator(0, 31))
        
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
        self.nrDci10Msg2McsEdit.setValidator(QIntValidator(0, 31))
        
        self.nrDci10Msg2TbScalingLabel = QLabel('TB Scaling[0-3]:')
        self.nrDci10Msg2TbScalingEdit = QLineEdit()
        self.nrDci10Msg2TbScalingEdit.setValidator(QIntValidator(0, 3))
        
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
        self.nrDci10Msg4McsEdit.setValidator(QIntValidator(0, 31))
        
        self.nrDci10Msg4TbsLabel = QLabel('Transport block size(bits):')
        self.nrDci10Msg4TbsEdit = QLineEdit()
        self.nrDci10Msg4TbsEdit.setEnabled(False)
        
        self.nrDci10Msg4DeltaPriLabel = QLabel('PUCCH resource indicator[0-7]:')
        self.nrDci10Msg4DeltaPriEdit = QLineEdit()
        self.nrDci10Msg4DeltaPriEdit.setValidator(QIntValidator(0, 7))
        
        self.nrDci10Msg4K1Label = QLabel('K1(PDSCH-to-HARQ_feedback timing indicator)[0-7]:')
        self.nrDci10Msg4K1Edit = QLineEdit()
        self.nrDci10Msg4K1Edit.setValidator(QIntValidator(0, 7))
        
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
        self.nrDci11PdschCw0McsEdit.setValidator(QIntValidator(0, 31))
        
        self.nrDci11PdschCw1McsLabel = QLabel('Modulation and coding scheme(CW1)[0-31]:')
        self.nrDci11PdschCw1McsEdit = QLineEdit()
        self.nrDci11PdschCw1McsEdit.setValidator(QIntValidator(0, 31))
        
        self.nrDci11PdschTbsLabel = QLabel('Transport block size(bits):')
        self.nrDci11PdschTbsEdit = QLineEdit()
        self.nrDci11PdschTbsEdit.setEnabled(False)
        
        self.nrDci11PdschDeltaPriLabel = QLabel('PUCCH resource indicator[0-7]:')
        self.nrDci11PdschDeltaPriEdit = QLineEdit()
        self.nrDci11PdschDeltaPriEdit.setValidator(QIntValidator(0, 7))
        
        self.nrDci11PdschK1Label = QLabel('K1(PDSCH-to-HARQ_feedback timing indicator)[0-7]:')
        self.nrDci11PdschK1Edit = QLineEdit()
        self.nrDci11PdschK1Edit.setValidator(QIntValidator(0, 7))
        
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
        
        self.nrDci01PuschFreqAllocFreqHopLabel= QLabel('Frequency hopping flag:')
        self.nrDci01PuschFreqAllocFreqHopComb = QComboBox()
        self.nrDci01PuschFreqAllocFreqHopComb.addItems(['disabled', 'intra-slot', 'inter-slot'])
        self.nrDci01PuschFreqAllocFreqHopComb.setCurrentIndex(0)
        
        self.nrDci01PuschFreqAllocFieldLabel = QLabel('Frequency domain resource assignment:')
        self.nrDci01PuschFreqAllocFieldEdit = QLineEdit()
        
        self.nrDci01PuschFreqAllocType1RbStartLabel = QLabel('RB_start(of RIV):')
        self.nrDci01PuschFreqAllocType1RbStartEdit = QLineEdit()
        
        self.nrDci01PuschFreqAllocType1LRbsLabel = QLabel('L_RBs(of RIV):')
        self.nrDci01PuschFreqAllocType1LRbsEdit = QLineEdit()
        
        self.nrDci01PuschCw0McsLabel = QLabel('Modulation and coding scheme(CW0)[0-31]:')
        self.nrDci01PuschCw0McsEdit = QLineEdit()
        self.nrDci01PuschCw0McsEdit.setValidator(QIntValidator(0, 31))
        
        self.nrDci01PuschTbsLabel = QLabel('Transport block size(bits):')
        self.nrDci01PuschTbsEdit = QLineEdit()
        self.nrDci01PuschTbsEdit.setEnabled(False)
        
        self.nrDci01PuschSriFieldLabel = QLabel('SRS resource indicator[0-1/0-3/0-7/0-15]:')
        self.nrDci01PuschSriFieldEdit = QLineEdit('0')
        
        self.nrDci01PuschAntPortsFieldLabel = QLabel('Antenna port(s)[0-15/0-31/0-63]:')
        self.nrDci01PuschAntPortsFieldEdit = QLineEdit('0')
        
        self.nrDci01PuschPtrsDmrsMappingLabel = QLabel('PTRS-DMRS association[0-3]:')
        self.nrDci01PuschPtrsDmrsMappingEdit = QLineEdit('0')
        self.nrDci01PuschPtrsDmrsMappingEdit.setValidator(QIntValidator(0, 3))
        
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
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocFreqHopLabel, 1, 0)
        dci01PuschFreqAllocLayout.addWidget(self.nrDci01PuschFreqAllocFreqHopComb, 1, 1)
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
        dci01PuschGridLayout.addWidget(self.nrDci01PuschPtrsDmrsMappingLabel, 10, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschPtrsDmrsMappingEdit, 10, 1)
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
        
        self.nrMsg3PuschFreqAllocFreqHopLabel= QLabel('Frequency hopping flag:')
        self.nrMsg3PuschFreqAllocFreqHopComb = QComboBox()
        self.nrMsg3PuschFreqAllocFreqHopComb.addItems(['disabled', 'enabled'])
        self.nrMsg3PuschFreqAllocFreqHopComb.setCurrentIndex(0)
        
        self.nrMsg3PuschFreqAllocFieldLabel = QLabel('Frequency domain resource assignment:')
        self.nrMsg3PuschFreqAllocFieldEdit = QLineEdit()
        
        self.nrMsg3PuschFreqAllocType1RbStartLabel = QLabel('RB_start(of RIV):')
        self.nrMsg3PuschFreqAllocType1RbStartEdit = QLineEdit()
        
        self.nrMsg3PuschFreqAllocType1LRbsLabel = QLabel('L_RBs(of RIV):')
        self.nrMsg3PuschFreqAllocType1LRbsEdit = QLineEdit()
        
        self.nrMsg3PuschCw0McsLabel = QLabel('Modulation and coding scheme(CW0)[0-31]:')
        self.nrMsg3PuschCw0McsEdit = QLineEdit()
        self.nrMsg3PuschCw0McsEdit.setValidator(QIntValidator(0, 31))
        
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
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocFreqHopLabel, 1, 0)
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocFreqHopComb, 1, 1)
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
        self.nrrachgenericPrachConfIdEdit.setValidator(QIntValidator(0, 255))
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
        self.nrRachNumRaPreamblesEdit.setValidator(QIntValidator(1, 64))
        self.nrRachNumRaPreamblesEdit.setText('64')
        
        self.nrRachSsbPerRachOccasionLabel = QLabel('ssb-perRACH-Occasion:')
        self.nrRachSsbPerRachOccasionComb = QComboBox()
        self.nrRachSsbPerRachOccasionComb.addItems(['1/8', '1/4', '1/2', '1', '2', '4', '8', '16'])
        
        self.nrRachCbPreamblesPerSsbLabel = QLabel('CB-PreamblesPerSSB:')
        self.nrRachCbPreamblesPerSsbEdit = QLineEdit()
        
        self.nrRachMsg3TpLabel = QLabel('msg3-transformPrecoder:')
        self.nrRachMsg3TpComb = QComboBox()
        self.nrRachMsg3TpComb.addItems(['enabled', 'disabled'])
        self.nrRachMsg3TpComb.setCurrentIndex(1)
        
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
        prachWidgetGridLayout.addWidget(self.nrRachMsg3TpLabel, 4, 0)
        prachWidgetGridLayout.addWidget(self.nrRachMsg3TpComb, 4, 1)
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
        self.nrPucchSib1PucchResCommonEdit.setValidator(QIntValidator(0, 15))
        
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
        
        #---->(4.3) dedicated active dl bwp as specified in ServingCellConfig IE
        #dedicated dl bwp
        self.nrDedDlBwpGenericBwpIdLabel = QLabel('bwp-Id[0-3]:')
        self.nrDedDlBwpGenericBwpIdEdit = QLineEdit()
        self.nrDedDlBwpGenericBwpIdEdit.setText('1')
        
        self.nrDedDlBwpGenericScsLabel = QLabel('subcarrierSpacing:')
        self.nrDedDlBwpGenericScsComb = QComboBox()
        self.nrDedDlBwpGenericScsComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        
        self.nrDedDlBwpGenericCpLabel = QLabel('cyclicPrefix:')
        self.nrDedDlBwpGenericCpComb = QComboBox()
        self.nrDedDlBwpGenericCpComb.addItems(['normal', 'extended'])
        self.nrDedDlBwpGenericCpComb.setCurrentIndex(0)
        
        self.nrDedDlBwpGenericLocAndBwLabel = QLabel('locationAndBandwidth[0-37949]:')
        self.nrDedDlBwpGenericLocAndBwEdit = QLineEdit()
        
        self.nrDedDlBwpGenericRbStartLabel = QLabel('RB_start:')
        self.nrDedDlBwpGenericRbStartEdit = QLineEdit()
        self.nrDedDlBwpGenericRbStartEdit.setEnabled(False)
        
        self.nrDedDlBwpGenericLRbsLabel = QLabel('L_RBs:')
        self.nrDedDlBwpGenericLRbsEdit = QLineEdit()
        self.nrDedDlBwpGenericLRbsEdit.setEnabled(False)
        
        dedDlBwpGrpBox = QGroupBox()
        dedDlBwpGrpBox.setTitle('Dedicated active DL BWP')
        dedDlBwpGrpBoxGridLayout = QGridLayout()
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericBwpIdLabel, 0, 0)
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericBwpIdEdit, 0, 1)
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericScsLabel, 1, 0)
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericScsComb, 1, 1)
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericCpLabel, 2, 0)
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericCpComb, 2, 1)
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericLocAndBwLabel, 3, 0)
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericLocAndBwEdit, 3, 1)
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericRbStartLabel, 4, 0)
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericRbStartEdit, 4, 1)
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericLRbsLabel, 5, 0)
        dedDlBwpGrpBoxGridLayout.addWidget(self.nrDedDlBwpGenericLRbsEdit, 5, 1)
        dedDlBwpGrpBox.setLayout(dedDlBwpGrpBoxGridLayout)
        
        #dedicated pdsch settings as specified in PDSCH-Config IE
        #assume there is only one entry in pdsch-TimeDomainAllocationList, and it can be accessed by setting the 'Time domain resource assignment' field of DCI 1_1 to a value other than 0~15
        #that's, use default common time-domain allocation if 'Time domain resource assignment' field is 0-15, and use self-defined (dedicated) time-domain allocation otherwise
        self.nrDedPdschCfgAggFactorLabel = QLabel('pdsch-AggregationFactor:')
        self.nrDedPdschCfgAggFactorComb = QComboBox()
        self.nrDedPdschCfgAggFactorComb.addItems(['n1', 'n2', 'n4', 'n8'])
        self.nrDedPdschCfgAggFactorComb.setCurrentIndex(0)
        
        self.nrDedPdschCfgRbgConfigLabel = QLabel('rbg-Size:')
        self.nrDedPdschCfgRbgConfigComb = QComboBox()
        self.nrDedPdschCfgRbgConfigComb.addItems(['config1', 'config2'])
        self.nrDedPdschCfgRbgConfigComb.setCurrentIndex(0)
        
        self.nrDedPdschCfgRbgSizeLabel = QLabel('Nominal size of RBG(P):')
        self.nrDedPdschCfgRbgSizeEdit = QLineEdit()
        
        self.nrDedPdschCfgMcsTableLabel = QLabel('mcs-Table:')
        self.nrDedPdschCfgMcsTableComb = QComboBox()
        self.nrDedPdschCfgMcsTableComb.addItems(['64QAM', '256QAM', '64QAMLowSE'])
        self.nrDedPdschCfgMcsTableComb.setCurrentIndex(0)
        
        dedPdschCfgWidget = QWidget()
        dedPdschCfgGridLayout = QGridLayout()
        dedPdschCfgGridLayout.addWidget(self.nrDedPdschCfgAggFactorLabel, 0, 0)
        dedPdschCfgGridLayout.addWidget(self.nrDedPdschCfgAggFactorComb, 0, 1)
        dedPdschCfgGridLayout.addWidget(self.nrDedPdschCfgRbgConfigLabel, 1, 0)
        dedPdschCfgGridLayout.addWidget(self.nrDedPdschCfgRbgConfigComb, 1, 1)
        dedPdschCfgGridLayout.addWidget(self.nrDedPdschCfgRbgSizeLabel, 2, 0)
        dedPdschCfgGridLayout.addWidget(self.nrDedPdschCfgRbgSizeEdit, 2, 1)
        dedPdschCfgGridLayout.addWidget(self.nrDedPdschCfgMcsTableLabel, 3, 0)
        dedPdschCfgGridLayout.addWidget(self.nrDedPdschCfgMcsTableComb, 3, 1)
        dedPdschCfgLayout = QVBoxLayout()
        dedPdschCfgLayout.addLayout(dedPdschCfgGridLayout)
        dedPdschCfgLayout.addStretch()
        dedPdschCfgWidget.setLayout(dedPdschCfgLayout)
        
        #DM-RS for dedicated pdsch, including PT-RS
        self.nrDmrsDedPdschDmrsTypeLabel = QLabel('dmrs-Type:')
        self.nrDmrsDedPdschDmrsTypeComb = QComboBox()
        self.nrDmrsDedPdschDmrsTypeComb.addItems(['Type 1', 'Type 2'])
        self.nrDmrsDedPdschDmrsTypeComb.setCurrentIndex(0)
        
        self.nrDmrsDedPdschAddPosLabel = QLabel('dmrs-additionalPosition:')
        self.nrDmrsDedPdschAddPosComb = QComboBox()
        self.nrDmrsDedPdschAddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        
        self.nrDmrsDedPdschMaxLengthLabel = QLabel('maxLength:')
        self.nrDmrsDedPdschMaxLengthComb = QComboBox()
        self.nrDmrsDedPdschMaxLengthComb.addItems(['len1', 'len2'])
        self.nrDmrsDedPdschMaxLengthComb.setCurrentIndex(0)
        
        #start ptrs
        self.nrPtrsPdschTimeDensityLabel = QLabel('timeDensity(L_PTRS):')
        self.nrPtrsPdschTimeDensityComb = QComboBox()
        self.nrPtrsPdschTimeDensityComb.addItems(['1', '2', '4'])
        
        self.nrPtrsPdschFreqDensityLabel = QLabel('frequencyDensity(K_PTRS):')
        self.nrPtrsPdschFreqDensityComb = QComboBox()
        self.nrPtrsPdschFreqDensityComb.addItems(['2', '4'])
        
        self.nrPtrsPdschReOffsetLabel = QLabel('resourceElementOffset')
        self.nrPtrsPdschReOffsetComb = QComboBox()
        self.nrPtrsPdschReOffsetComb.addItems(['offset00', 'offset01', 'offset10', 'offset11'])
        
        self.nrPtrsPdschDmrsAntPortLabel = QLabel('Associated DMRS port[1000+x]:')
        self.nrPtrsPdschDmrsAntPortEdit = QLineEdit()
        self.nrPtrsPdschDmrsAntPortEdit.setEnabled(False)
        #end ptrs
        
        self.nrDmrsDedPdschDmrsPortsLabel = QLabel('DMRS port(s)[1000+x]:')
        self.nrDmrsDedPdschDmrsPortsEdit = QLineEdit()
        
        self.nrDmrsDedPdschCdmGroupsWoDataLabel = QLabel('CDM group(s) without data:')
        self.nrDmrsDedPdschCdmGroupsWoDataEdit = QLineEdit()
        
        self.nrDmrsDedPdschFrontLoadSymbsLabel = QLabel('Number of front-load symbols:')
        self.nrDmrsDedPdschFrontLoadSymbsEdit = QLineEdit()
        
        ptrsPdschWidget = QGroupBox()
        ptrsPdschWidget.setTitle('PT-RS for PDSCH')
        ptrsPdschWidgetGridLayout = QGridLayout()
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschTimeDensityLabel, 0, 0)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschTimeDensityComb, 0, 1)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschFreqDensityLabel, 1, 0)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschFreqDensityComb, 1, 1)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschReOffsetLabel, 2, 0)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschReOffsetComb, 2, 1)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschDmrsAntPortLabel, 3, 0)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschDmrsAntPortEdit, 3, 1)
        ptrsPdschWidget.setLayout(ptrsPdschWidgetGridLayout)
        
        dmrsDedPdschWidget = QWidget()
        dmrsDedPdschGridLayout = QGridLayout()
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschDmrsTypeLabel, 0, 0)
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschDmrsTypeComb, 0, 1)
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschAddPosLabel, 1, 0)
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschAddPosComb, 1, 1)
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschMaxLengthLabel, 2, 0)
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschMaxLengthComb, 2, 1)
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschDmrsPortsLabel, 3, 0)
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschDmrsPortsEdit, 3, 1)
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschCdmGroupsWoDataLabel, 4, 0)
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschCdmGroupsWoDataEdit, 4, 1)
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschFrontLoadSymbsLabel, 5, 0)
        dmrsDedPdschGridLayout.addWidget(self.nrDmrsDedPdschFrontLoadSymbsEdit, 5, 1)
        dmrsDedPdschGridLayout.addWidget(ptrsPdschWidget, 6, 0, 1, 2)
        dmrsDedPdschLayout = QVBoxLayout()
        dmrsDedPdschLayout.addLayout(dmrsDedPdschGridLayout)
        dmrsDedPdschLayout.addStretch()
        dmrsDedPdschWidget.setLayout(dmrsDedPdschLayout)
        
        #csi-rs settings
        #TODO
        self.csirsTempLabel = QLabel('<font color=red>Note: CSI-RS will be implemented later!</font>')
        
        csirsWidget = QWidget()
        csirsGridLayout = QGridLayout()
        csirsGridLayout.addWidget(self.csirsTempLabel, 0, 0)
        csirsLayout = QVBoxLayout()
        csirsLayout.addLayout(csirsGridLayout)
        csirsLayout.addStretch()
        csirsWidget.setLayout(csirsLayout)
        
        dedDlBwpTabWidget = QTabWidget()
        dedDlBwpTabWidget.addTab(dedPdschCfgWidget, 'PDSCH-Config')
        dedDlBwpTabWidget.addTab(dmrsDedPdschWidget, 'DM-RS(PDSCH)')
        dedDlBwpTabWidget.addTab(csirsWidget, 'CSI-RS')
        
        dedDlBwpWidget = QWidget()
        dedDlBwpLayout = QVBoxLayout()
        dedDlBwpLayout.addWidget(dedDlBwpGrpBox)
        dedDlBwpLayout.addWidget(dedDlBwpTabWidget)
        dedDlBwpLayout.addStretch()
        dedDlBwpWidget.setLayout(dedDlBwpLayout)
        
        #---->(4.4) dedicated active ul bwp as specified in ServingCellConfig IE
        #dedicated ul bwp
        self.nrDedUlBwpGenericBwpIdLabel = QLabel('bwp-Id[0-3]:')
        self.nrDedUlBwpGenericBwpIdEdit = QLineEdit()
        self.nrDedUlBwpGenericBwpIdEdit.setText('1')
        
        self.nrDedUlBwpGenericScsLabel = QLabel('subcarrierSpacing:')
        self.nrDedUlBwpGenericScsComb = QComboBox()
        self.nrDedUlBwpGenericScsComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        
        self.nrDedUlBwpGenericCpLabel = QLabel('cyclicPrefix:')
        self.nrDedUlBwpGenericCpComb = QComboBox()
        self.nrDedUlBwpGenericCpComb.addItems(['normal', 'extended'])
        self.nrDedUlBwpGenericCpComb.setCurrentIndex(0)
        
        self.nrDedUlBwpGenericLocAndBwLabel = QLabel('locationAndBandwidth[0-37949]:')
        self.nrDedUlBwpGenericLocAndBwEdit = QLineEdit()
        self.nrDedUlBwpGenericLocAndBwEdit.setValidator(QIntValidator(0, 37949))
        
        self.nrDedUlBwpGenericRbStartLabel = QLabel('RB_start:')
        self.nrDedUlBwpGenericRbStartEdit = QLineEdit()
        self.nrDedUlBwpGenericRbStartEdit.setEnabled(False)
        
        self.nrDedUlBwpGenericLRbsLabel = QLabel('L_RBs:')
        self.nrDedUlBwpGenericLRbsEdit = QLineEdit()
        self.nrDedUlBwpGenericLRbsEdit.setEnabled(False)
        
        dedUlBwpGrpBox = QGroupBox()
        dedUlBwpGrpBox.setTitle('Dedicated active UL BWP')
        dedUlBwpGrpBoxGridLayout = QGridLayout()
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericBwpIdLabel, 0, 0)
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericBwpIdEdit, 0, 1)
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericScsLabel, 1, 0)
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericScsComb, 1, 1)
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericCpLabel, 2, 0)
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericCpComb, 2, 1)
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericLocAndBwLabel, 3, 0)
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericLocAndBwEdit, 3, 1)
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericRbStartLabel, 4, 0)
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericRbStartEdit, 4, 1)
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericLRbsLabel, 5, 0)
        dedUlBwpGrpBoxGridLayout.addWidget(self.nrDedUlBwpGenericLRbsEdit, 5, 1)
        dedUlBwpGrpBox.setLayout(dedUlBwpGrpBoxGridLayout)
        
        #dedicated pusch settings as specified in PUSCH-Config IE
        #assume there is only one entry in pusch-TimeDomainAllocationList, and it can be accessed by setting the 'Time domain resource assignment' field of DCI 1_1 to a value other than 0~15
        #that's, use default common time-domain allocation if 'Time domain resource assignment' field is 0-15, and use self-defined (dedicated) time-domain allocation otherwise
        self.nrDedPuschCfgTxCfgLabel = QLabel('txConfig:')
        self.nrDedPuschCfgTxCfgComb = QComboBox()
        self.nrDedPuschCfgTxCfgComb.addItems(['codebook', 'nonCodebook'])
        self.nrDedPuschCfgTxCfgComb.setCurrentIndex(0)
        
        self.nrDedPuschCfgCbSubsetLabel = QLabel('codebookSubset:')
        self.nrDedPuschCfgCbSubsetComb = QComboBox()
        self.nrDedPuschCfgCbSubsetComb.addItems(['fullyAndPartialAndNonCoherent', 'partialAndNonCoherent', 'nonCoherent'])
        self.nrDedPuschCfgCbSubsetComb.setCurrentIndex(0)
        
        self.nrDedPuschCfgCbMaxRankLabel = QLabel('CB maxRank[1-4]:')
        self.nrDedPuschCfgCbMaxRankEdit = QLineEdit()
        self.nrDedPuschCfgCbMaxRankEdit.setValidator(QIntValidator(1, 4))
        
        #note: Lmax is the number of srs resources transmitted by ue, which is ue capability as defined in 38.306
        self.nrDedPuschCfgNonCbMaxLayersLabel = QLabel('non-CB maxLayers(Lmax)[1-4]:')
        self.nrDedPuschCfgNonCbMaxLayersEdit = QLineEdit()
        self.nrDedPuschCfgNonCbMaxLayersEdit.setValidator(QIntValidator(1, 4))
        
        self.nrDedPuschCfgFreqHopOffsetLabel = QLabel('frequencyHoppingOffset[0-274]:')
        self.nrDedPuschCfgFreqHopOffsetEdit = QLineEdit()
        self.nrDedPuschCfgFreqHopOffsetEdit.setValidator(QIntValidator(0, 274))
        
        self.nrDedPuschCfgTpLabel = QLabel('transformPrecoder:')
        self.nrDedPuschCfgTpComb = QComboBox()
        self.nrDedPuschCfgTpComb.addItems(['enabled', 'disabled'])
        self.nrDedPuschCfgTpComb.setCurrentIndex(1)
        
        self.nrDedPuschCfgAggFactorLabel = QLabel('pusch-AggregationFactor:')
        self.nrDedPuschCfgAggFactorComb = QComboBox()
        self.nrDedPuschCfgAggFactorComb.addItems(['n1', 'n2', 'n4', 'n8'])
        self.nrDedPuschCfgAggFactorComb.setCurrentIndex(0)
        
        self.nrDedPuschCfgRbgConfigLabel = QLabel('rbg-Size:')
        self.nrDedPuschCfgRbgConfigComb = QComboBox()
        self.nrDedPuschCfgRbgConfigComb.addItems(['config1', 'config2'])
        self.nrDedPuschCfgRbgConfigComb.setCurrentIndex(0)
        
        self.nrDedPuschCfgRbgSizeLabel = QLabel('Nominal size of RBG(P):')
        self.nrDedPuschCfgRbgSizeEdit = QLineEdit()
        
        self.nrDedPuschCfgMcsTableLabel = QLabel('mcs-Table:')
        self.nrDedPuschCfgMcsTableComb = QComboBox()
        self.nrDedPuschCfgMcsTableComb.addItems(['64QAM', '256QAM', '64QAMLowSE'])
        self.nrDedPuschCfgMcsTableComb.setCurrentIndex(0)
        
        dedPuschCfgWidget = QWidget()
        dedPuschCfgGridLayout = QGridLayout()
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgTxCfgLabel, 0, 0)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgTxCfgComb, 0, 1)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgCbSubsetLabel, 1, 0)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgCbSubsetComb, 1, 1)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgCbMaxRankLabel, 2, 0)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgCbMaxRankEdit, 2, 1)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgNonCbMaxLayersLabel, 3, 0)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgNonCbMaxLayersEdit, 3, 1)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgFreqHopOffsetLabel, 4, 0)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgFreqHopOffsetEdit, 4, 1)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgTpLabel, 5, 0)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgTpComb, 5, 1)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgAggFactorLabel, 6, 0)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgAggFactorComb, 6, 1)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgRbgConfigLabel, 7, 0)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgRbgConfigComb, 7, 1)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgRbgSizeLabel, 8, 0)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgRbgSizeEdit, 8, 1)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgMcsTableLabel, 9, 0)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgMcsTableComb, 9, 1)
        dedPuschCfgLayout = QVBoxLayout()
        dedPuschCfgLayout.addLayout(dedPuschCfgGridLayout)
        dedPuschCfgLayout.addStretch()
        dedPuschCfgWidget.setLayout(dedPuschCfgLayout)
        
        #DM-RS for dedicated pusch, including PT-RS
        self.nrDmrsDedPuschDmrsTypeLabel = QLabel('dmrs-Type:')
        self.nrDmrsDedPuschDmrsTypeComb = QComboBox()
        self.nrDmrsDedPuschDmrsTypeComb.addItems(['Type 1', 'Type 2'])
        self.nrDmrsDedPuschDmrsTypeComb.setCurrentIndex(0)
        
        self.nrDmrsDedPuschAddPosLabel = QLabel('dmrs-additionalPosition:')
        self.nrDmrsDedPuschAddPosComb = QComboBox()
        self.nrDmrsDedPuschAddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        
        self.nrDmrsDedPuschMaxLengthLabel = QLabel('maxLength:')
        self.nrDmrsDedPuschMaxLengthComb = QComboBox()
        self.nrDmrsDedPuschMaxLengthComb.addItems(['len1', 'len2'])
        self.nrDmrsDedPuschMaxLengthComb.setCurrentIndex(0)
        
        self.nrDmrsDedPuschRankLabel = QLabel('Transmission rank:')
        self.nrDmrsDedPuschRankEdit = QLineEdit()
        
        #start ptrs
        self.nrPtrsPuschTimeDensityLabel = QLabel('timeDensity(L_PTRS):')
        self.nrPtrsPuschTimeDensityComb = QComboBox()
        self.nrPtrsPuschTimeDensityComb.addItems(['1', '2', '4'])
        
        self.nrPtrsPuschFreqDensityLabel = QLabel('frequencyDensity(K_PTRS):')
        self.nrPtrsPuschFreqDensityComb = QComboBox()
        self.nrPtrsPuschFreqDensityComb.addItems(['2', '4'])
        
        self.nrPtrsPuschReOffsetLabel = QLabel('resourceElementOffset')
        self.nrPtrsPuschReOffsetComb = QComboBox()
        self.nrPtrsPuschReOffsetComb.addItems(['offset00', 'offset01', 'offset10', 'offset11'])
        
        self.nrPtrsPuschMaxNumPortsLabel = QLabel('maxNrofPorts:')
        self.nrPtrsPuschMaxNumPortsComb = QComboBox()
        self.nrPtrsPuschMaxNumPortsComb.addItems(['n1', 'n2'])
        
        #assume value format: dmrs_port_for_ptrs_port0[, dmrs_port_for_ptrs_port1]
        self.nrPtrsPuschDmrsAntPortsLabel = QLabel('Associated DMRS port(s)[x]:')
        self.nrPtrsPuschDmrsAntPortsEdit = QLineEdit()
        self.nrPtrsPuschDmrsAntPortsEdit.setEnabled(False)
        
        self.nrPtrsPuschTpTimeDensityLabel = QLabel('timeDensity(L_PTRS):')
        self.nrPtrsPuschTpTimeDensityComb = QComboBox()
        self.nrPtrsPuschTpTimeDensityComb.addItems(['1', '2', '4'])
        
        self.nrPtrsPuschTpGroupPatLabel = QLabel('PT-RS group pattern:')
        self.nrPtrsPuschTpGroupPatComb = QComboBox()
        self.nrPtrsPuschTpGroupPatComb.addItems(['pattern 0', 'pattern 1', 'pattern 2', 'pattern 3', 'pattern 4'])
        self.nrPtrsPuschTpGroupPatComb.setCurrentIndex(0)
        
        self.nrPtrsPuschTpNumGroupsLabel = QLabel('Number of groups:')
        self.nrPtrsPuschTpNumGroupsEdit = QLineEdit('2')
        self.nrPtrsPuschTpNumGroupsEdit.setEnabled(False)
        
        self.nrPtrsPuschTpSamplesPerGroupLabel = QLabel('Number of samples per group:')
        self.nrPtrsPuschTpSamplesPerGroupEdit = QLineEdit('2')
        self.nrPtrsPuschTpSamplesPerGroupEdit.setEnabled(False)
        
        self.nrPtrsPuschTpDmrsAntPortsLabel = QLabel('Associated DMRS port[x]:')
        self.nrPtrsPuschTpDmrsAntPortsEdit = QLineEdit()
        self.nrPtrsPuschTpDmrsAntPortsEdit.setEnabled(False)
        #end ptrs
        
        self.nrDmrsDedPuschDmrsPortsLabel = QLabel('DMRS port(s)[x]:')
        self.nrDmrsDedPuschDmrsPortsEdit = QLineEdit()
        
        self.nrDmrsDedPuschCdmGroupsWoDataLabel = QLabel('CDM group(s) without data:')
        self.nrDmrsDedPuschCdmGroupsWoDataEdit = QLineEdit()
        
        self.nrDmrsDedPuschFrontLoadSymbsLabel = QLabel('Number of front-load symbols:')
        self.nrDmrsDedPuschFrontLoadSymbsEdit = QLineEdit()
        
        ptrsPuschWidget = QWidget()
        ptrsPuschGridLayout = QGridLayout()
        ptrsPuschGridLayout.addWidget(self.nrPtrsPuschTimeDensityLabel, 0, 0)
        ptrsPuschGridLayout.addWidget(self.nrPtrsPuschTimeDensityComb, 0, 1)
        ptrsPuschGridLayout.addWidget(self.nrPtrsPuschFreqDensityLabel, 1, 0)
        ptrsPuschGridLayout.addWidget(self.nrPtrsPuschFreqDensityComb, 1, 1)
        ptrsPuschGridLayout.addWidget(self.nrPtrsPuschReOffsetLabel, 2, 0)
        ptrsPuschGridLayout.addWidget(self.nrPtrsPuschReOffsetComb, 2, 1)
        ptrsPuschGridLayout.addWidget(self.nrPtrsPuschMaxNumPortsLabel, 3, 0)
        ptrsPuschGridLayout.addWidget(self.nrPtrsPuschMaxNumPortsComb, 3, 1)
        ptrsPuschGridLayout.addWidget(self.nrPtrsPuschDmrsAntPortsLabel, 4, 0)
        ptrsPuschGridLayout.addWidget(self.nrPtrsPuschDmrsAntPortsEdit, 4, 1)
        ptrsPuschLayout = QVBoxLayout()
        ptrsPuschLayout.addLayout(ptrsPuschGridLayout)
        ptrsPuschLayout.addStretch()
        ptrsPuschWidget.setLayout(ptrsPuschLayout)
        
        ptrsPuschTpWidget = QWidget()
        ptrsPuschTpGridLayout = QGridLayout()
        ptrsPuschTpGridLayout.addWidget(self.nrPtrsPuschTpTimeDensityLabel, 0, 0)
        ptrsPuschTpGridLayout.addWidget(self.nrPtrsPuschTpTimeDensityComb, 0, 1)
        ptrsPuschTpGridLayout.addWidget(self.nrPtrsPuschTpGroupPatLabel, 1, 0)
        ptrsPuschTpGridLayout.addWidget(self.nrPtrsPuschTpGroupPatComb, 1, 1)
        ptrsPuschTpGridLayout.addWidget(self.nrPtrsPuschTpNumGroupsLabel, 2, 0)
        ptrsPuschTpGridLayout.addWidget(self.nrPtrsPuschTpNumGroupsEdit, 2, 1)
        ptrsPuschTpGridLayout.addWidget(self.nrPtrsPuschTpSamplesPerGroupLabel, 3, 0)
        ptrsPuschTpGridLayout.addWidget(self.nrPtrsPuschTpSamplesPerGroupEdit, 3, 1)
        ptrsPuschTpGridLayout.addWidget(self.nrPtrsPuschTpDmrsAntPortsLabel, 4, 0)
        ptrsPuschTpGridLayout.addWidget(self.nrPtrsPuschTpDmrsAntPortsEdit, 4, 1)
        ptrsPuschTpLayout = QVBoxLayout()
        ptrsPuschTpLayout.addLayout(ptrsPuschTpGridLayout)
        ptrsPuschTpLayout.addStretch()
        ptrsPuschTpWidget.setLayout(ptrsPuschTpLayout)
        
        ptrsPuschTabWidget = QTabWidget()
        ptrsPuschTabWidget.addTab(ptrsPuschWidget, 'CP-OFDM')
        ptrsPuschTabWidget.addTab(ptrsPuschTpWidget, 'DFT-S-OFDM')
        
        ptrsPuschGrpBox = QGroupBox()
        ptrsPuschGrpBox.setTitle('PT-RS for PUSCH')
        ptrsPuschGrpBoxLayout = QVBoxLayout()
        ptrsPuschGrpBoxLayout.addWidget(ptrsPuschTabWidget)
        ptrsPuschGrpBoxLayout.addStretch()
        ptrsPuschGrpBox.setLayout(ptrsPuschGrpBoxLayout)
        
        dmrsDedPuschWidget = QWidget()
        dmrsDedPuschGridLayout = QGridLayout()
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschDmrsTypeLabel, 0, 0)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschDmrsTypeComb, 0, 1)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschAddPosLabel, 1, 0)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschAddPosComb, 1, 1)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschMaxLengthLabel, 2, 0)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschMaxLengthComb, 2, 1)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschRankLabel, 3, 0)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschRankEdit, 3, 1)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschDmrsPortsLabel, 4, 0)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschDmrsPortsEdit, 4, 1)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschCdmGroupsWoDataLabel, 5, 0)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschCdmGroupsWoDataEdit, 5, 1)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschFrontLoadSymbsLabel, 6, 0)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschFrontLoadSymbsEdit, 6, 1)
        dmrsDedPuschGridLayout.addWidget(ptrsPuschGrpBox, 7, 0, 1, 2)
        dmrsDedPuschLayout = QVBoxLayout()
        dmrsDedPuschLayout.addLayout(dmrsDedPuschGridLayout)
        dmrsDedPuschLayout.addStretch()
        dmrsDedPuschWidget.setLayout(dmrsDedPuschLayout)
        
        #srs settings
        #SRS-Resource item 0
        self.nrSrsRes0ResourceIdLabel = QLabel('srs-ResourceId[0-63]:')
        self.nrSrsRes0ResourceIdEdit = QLineEdit()
        self.nrSrsRes0ResourceIdEdit.setText('0')
        self.nrSrsRes0ResourceIdEdit.setEnabled(False)
        
        self.nrSrsRes0NumAntPortsLabel = QLabel('nrofSRS-Ports:')
        self.nrSrsRes0NumAntPortsComb = QComboBox()
        self.nrSrsRes0NumAntPortsComb.addItems(['port1', 'port2', 'port4'])
        self.nrSrsRes0NumAntPortsComb.setCurrentIndex(0)
        
        self.nrSrsRes0NumCombLabel = QLabel('transmissionComb:')
        self.nrSrsRes0NumCombComb= QComboBox()
        self.nrSrsRes0NumCombComb.addItems(['n2', 'n4'])
        self.nrSrsRes0NumCombComb.setCurrentIndex(0)
        
        self.nrSrsRes0CombOffsetLabel = QLabel('combOffset[0-1]:')
        self.nrSrsRes0CombOffsetEdit = QLineEdit('0')
        self.nrSrsRes0CombOffsetEdit.setValidator(QIntValidator(0, 1))
        
        self.nrSrsRes0StartPosLabel = QLabel('startPosition[0-5]:')
        self.nrSrsRes0StartPosEdit = QLineEdit('0')
        self.nrSrsRes0StartPosEdit.setValidator(QIntValidator(0, 5))
        
        self.nrSrsRes0NumSymbsLabel = QLabel('nrofSymbols:')
        self.nrSrsRes0NumSymbsComb = QComboBox()
        self.nrSrsRes0NumSymbsComb.addItems(['n1', 'n2', 'n4'])
        self.nrSrsRes0NumSymbsComb.setCurrentIndex(0)
        
        self.nrSrsRes0RepFactorLabel = QLabel('repetitionFactor:')
        self.nrSrsRes0RepFactorComb = QComboBox()
        self.nrSrsRes0RepFactorComb.addItems(['n1', 'n2', 'n4'])
        self.nrSrsRes0RepFactorComb.setCurrentIndex(0)
        
        self.nrSrsRes0FreqPosLabel = QLabel('freqDomainPosition[0-67]:')
        self.nrSrsRes0FreqPosEdit = QLineEdit('0')
        self.nrSrsRes0FreqPosEdit.setValidator(QIntValidator(0, 67))
        
        self.nrSrsRes0FreqShiftLabel = QLabel('freqDomainShift[0-268]:')
        self.nrSrsRes0FreqShiftEdit = QLineEdit('0')
        self.nrSrsRes0FreqShiftEdit.setValidator(QIntValidator(0, 268))
        
        self.nrSrsRes0FreqHopCSrsLabel = QLabel('c-SRS[0-63]:')
        self.nrSrsRes0FreqHopCSrsEdit = QLineEdit('0')
        self.nrSrsRes0FreqHopCSrsEdit.setValidator(QIntValidator(0, 63))
        
        self.nrSrsRes0FreqHopBSrsLabel = QLabel('b-SRS[0-3]:')
        self.nrSrsRes0FreqHopBSrsEdit = QLineEdit('0')
        self.nrSrsRes0FreqHopBSrsEdit.setValidator(QIntValidator(0, 3))
        
        self.nrSrsRes0FreqHopBHopLabel = QLabel('b-hop[0-3]:')
        self.nrSrsRes0FreqHopBHopEdit = QLineEdit('0')
        self.nrSrsRes0FreqHopBHopEdit.setValidator(QIntValidator(0, 3))
        
        self.nrSrsRes0ResTypeLabel = QLabel('resourceType:')
        self.nrSrsRes0ResTypeComb = QComboBox()
        self.nrSrsRes0ResTypeComb.addItems(['aperiodic', 'semi-persistent', 'periodic'])
        self.nrSrsRes0ResTypeComb.setCurrentIndex(2)
        self.nrSrsRes0ResTypeComb.setEnabled(False)
        
        self.nrSrsRes0PeriodLabel = QLabel('SRS-Periodicity:')
        self.nrSrsRes0PeriodComb = QComboBox()
        self.nrSrsRes0PeriodComb.addItems(['sl1', 'sl2', 'sl4', 'sl5', 'sl8', 'sl10', 'sl16', 'sl20', 'sl32', 'sl40', 'sl64', 'sl80', 'sl160',
                                           'sl320', 'sl640', 'sl1280', 'sl2560'])
        self.nrSrsRes0PeriodComb.setCurrentIndex(3)
        
        self.nrSrsRes0OffsetLabel = QLabel('SRS-Offset[0-4]:')
        self.nrSrsRes0OffsetEdit = QLineEdit('0')
        self.nrSrsRes0OffsetEdit.setValidator(QIntValidator(0, 4))
        
        srsRes0Widget = QWidget()
        srsRes0GridLayout = QGridLayout()
        srsRes0GridLayout.addWidget(self.nrSrsRes0ResourceIdLabel, 0, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0ResourceIdEdit, 0, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0NumAntPortsLabel, 1, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0NumAntPortsComb, 1, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0NumCombLabel, 2, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0NumCombComb, 2, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0CombOffsetLabel, 3, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0CombOffsetEdit, 3, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0StartPosLabel, 4, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0StartPosEdit, 4, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0NumSymbsLabel, 5, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0NumSymbsComb, 5, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0RepFactorLabel, 6, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0RepFactorComb, 6, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqPosLabel, 7, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqPosEdit, 7, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqShiftLabel, 8, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqShiftEdit, 8, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopCSrsLabel, 9, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopCSrsEdit, 9, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopBSrsLabel, 10, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopBSrsEdit, 10, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopBHopLabel, 11, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopBHopEdit, 11, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0ResTypeLabel, 12, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0ResTypeComb, 12, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0PeriodLabel, 13, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0PeriodComb, 13, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0OffsetLabel, 14, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0OffsetEdit, 14, 1)
        srsRes0Layout = QVBoxLayout()
        srsRes0Layout.addLayout(srsRes0GridLayout)
        srsRes0Layout.addStretch()
        srsRes0Widget.setLayout(srsRes0Layout)
        
        srsRes0Scroll = QScrollArea()
        srsRes0Scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        srsRes0Scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        srsRes0Scroll.setWidgetResizable(True)
        srsRes0Scroll.setWidget(srsRes0Widget)
        
        #SRS-Resource item 1
        self.nrSrsRes1ResourceIdLabel = QLabel('srs-ResourceId[0-63]:')
        self.nrSrsRes1ResourceIdEdit = QLineEdit()
        self.nrSrsRes1ResourceIdEdit.setText('1')
        self.nrSrsRes1ResourceIdEdit.setEnabled(False)
        
        self.nrSrsRes1NumAntPortsLabel = QLabel('nrofSRS-Ports:')
        self.nrSrsRes1NumAntPortsComb = QComboBox()
        self.nrSrsRes1NumAntPortsComb.addItems(['port1', 'port2', 'port4'])
        self.nrSrsRes1NumAntPortsComb.setCurrentIndex(0)
        
        self.nrSrsRes1NumCombLabel = QLabel('transmissionComb:')
        self.nrSrsRes1NumCombComb= QComboBox()
        self.nrSrsRes1NumCombComb.addItems(['n2', 'n4'])
        self.nrSrsRes1NumCombComb.setCurrentIndex(0)
        
        self.nrSrsRes1CombOffsetLabel = QLabel('combOffset[0-1]:')
        self.nrSrsRes1CombOffsetEdit = QLineEdit('0')
        self.nrSrsRes1CombOffsetEdit.setValidator(QIntValidator(0, 1))
        
        self.nrSrsRes1StartPosLabel = QLabel('startPosition[0-5]:')
        self.nrSrsRes1StartPosEdit = QLineEdit('0')
        self.nrSrsRes1StartPosEdit.setValidator(QIntValidator(0, 5))
        
        self.nrSrsRes1NumSymbsLabel = QLabel('nrofSymbols:')
        self.nrSrsRes1NumSymbsComb = QComboBox()
        self.nrSrsRes1NumSymbsComb.addItems(['n1', 'n2', 'n4'])
        self.nrSrsRes1NumSymbsComb.setCurrentIndex(0)
        
        self.nrSrsRes1RepFactorLabel = QLabel('repetitionFactor:')
        self.nrSrsRes1RepFactorComb = QComboBox()
        self.nrSrsRes1RepFactorComb.addItems(['n1', 'n2', 'n4'])
        self.nrSrsRes1RepFactorComb.setCurrentIndex(0)
        
        self.nrSrsRes1FreqPosLabel = QLabel('freqDomainPosition[0-67]:')
        self.nrSrsRes1FreqPosEdit = QLineEdit('0')
        self.nrSrsRes1FreqPosEdit.setValidator(QIntValidator(0, 67))
        
        self.nrSrsRes1FreqShiftLabel = QLabel('freqDomainShift[0-268]:')
        self.nrSrsRes1FreqShiftEdit = QLineEdit('0')
        self.nrSrsRes1FreqShiftEdit.setValidator(QIntValidator(0, 268))
        
        self.nrSrsRes1FreqHopCSrsLabel = QLabel('c-SRS[0-63]:')
        self.nrSrsRes1FreqHopCSrsEdit = QLineEdit('0')
        self.nrSrsRes1FreqHopCSrsEdit.setValidator(QIntValidator(0, 63))
        
        self.nrSrsRes1FreqHopBSrsLabel = QLabel('b-SRS[0-3]:')
        self.nrSrsRes1FreqHopBSrsEdit = QLineEdit('0')
        self.nrSrsRes1FreqHopBSrsEdit.setValidator(QIntValidator(0, 3))
        
        self.nrSrsRes1FreqHopBHopLabel = QLabel('b-hop[0-3]:')
        self.nrSrsRes1FreqHopBHopEdit = QLineEdit('0')
        self.nrSrsRes1FreqHopBHopEdit.setValidator(QIntValidator(0, 3))
        
        self.nrSrsRes1ResTypeLabel = QLabel('resourceType:')
        self.nrSrsRes1ResTypeComb = QComboBox()
        self.nrSrsRes1ResTypeComb.addItems(['aperiodic', 'semi-persistent', 'periodic'])
        self.nrSrsRes1ResTypeComb.setCurrentIndex(2)
        self.nrSrsRes1ResTypeComb.setEnabled(False)
        
        self.nrSrsRes1PeriodLabel = QLabel('SRS-Periodicity:')
        self.nrSrsRes1PeriodComb = QComboBox()
        self.nrSrsRes1PeriodComb.addItems(['sl1', 'sl2', 'sl4', 'sl5', 'sl8', 'sl10', 'sl16', 'sl20', 'sl32', 'sl40', 'sl64', 'sl80', 'sl160',
                                           'sl320', 'sl640', 'sl1280', 'sl2560'])
        self.nrSrsRes1PeriodComb.setCurrentIndex(3)
        
        self.nrSrsRes1OffsetLabel = QLabel('SRS-Offset[0-4]:')
        self.nrSrsRes1OffsetEdit = QLineEdit('0')
        self.nrSrsRes1OffsetEdit.setValidator(QIntValidator(0, 4))
        
        srsRes1Widget = QWidget()
        srsRes1GridLayout = QGridLayout()
        srsRes1GridLayout.addWidget(self.nrSrsRes1ResourceIdLabel, 0, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1ResourceIdEdit, 0, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1NumAntPortsLabel, 1, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1NumAntPortsComb, 1, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1NumCombLabel, 2, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1NumCombComb, 2, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1CombOffsetLabel, 3, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1CombOffsetEdit, 3, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1StartPosLabel, 4, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1StartPosEdit, 4, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1NumSymbsLabel, 5, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1NumSymbsComb, 5, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1RepFactorLabel, 6, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1RepFactorComb, 6, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqPosLabel, 7, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqPosEdit, 7, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqShiftLabel, 8, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqShiftEdit, 8, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopCSrsLabel, 9, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopCSrsEdit, 9, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopBSrsLabel, 10, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopBSrsEdit, 10, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopBHopLabel, 11, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopBHopEdit, 11, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1ResTypeLabel, 12, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1ResTypeComb, 12, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1PeriodLabel, 13, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1PeriodComb, 13, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1OffsetLabel, 14, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1OffsetEdit, 14, 1)
        srsRes1Layout = QVBoxLayout()
        srsRes1Layout.addLayout(srsRes1GridLayout)
        srsRes1Layout.addStretch()
        srsRes1Widget.setLayout(srsRes1Layout)
        
        srsRes1Scroll = QScrollArea()
        srsRes1Scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        srsRes1Scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        srsRes1Scroll.setWidgetResizable(True)
        srsRes1Scroll.setWidget(srsRes1Widget)
        
        #SRS-Resource item 2
        self.nrSrsRes2ResourceIdLabel = QLabel('srs-ResourceId[0-63]:')
        self.nrSrsRes2ResourceIdEdit = QLineEdit()
        self.nrSrsRes2ResourceIdEdit.setText('2')
        self.nrSrsRes2ResourceIdEdit.setEnabled(False)
        
        self.nrSrsRes2NumAntPortsLabel = QLabel('nrofSRS-Ports:')
        self.nrSrsRes2NumAntPortsComb = QComboBox()
        self.nrSrsRes2NumAntPortsComb.addItems(['port1', 'port2', 'port4'])
        self.nrSrsRes2NumAntPortsComb.setCurrentIndex(0)
        
        self.nrSrsRes2NumCombLabel = QLabel('transmissionComb:')
        self.nrSrsRes2NumCombComb= QComboBox()
        self.nrSrsRes2NumCombComb.addItems(['n2', 'n4'])
        self.nrSrsRes2NumCombComb.setCurrentIndex(0)
        
        self.nrSrsRes2CombOffsetLabel = QLabel('combOffset[0-1]:')
        self.nrSrsRes2CombOffsetEdit = QLineEdit('0')
        self.nrSrsRes2CombOffsetEdit.setValidator(QIntValidator(0, 1))
        
        self.nrSrsRes2StartPosLabel = QLabel('startPosition[0-5]:')
        self.nrSrsRes2StartPosEdit = QLineEdit('0')
        self.nrSrsRes2StartPosEdit.setValidator(QIntValidator(0, 5))
        
        self.nrSrsRes2NumSymbsLabel = QLabel('nrofSymbols:')
        self.nrSrsRes2NumSymbsComb = QComboBox()
        self.nrSrsRes2NumSymbsComb.addItems(['n1', 'n2', 'n4'])
        self.nrSrsRes2NumSymbsComb.setCurrentIndex(0)
        
        self.nrSrsRes2RepFactorLabel = QLabel('repetitionFactor:')
        self.nrSrsRes2RepFactorComb = QComboBox()
        self.nrSrsRes2RepFactorComb.addItems(['n1', 'n2', 'n4'])
        self.nrSrsRes2RepFactorComb.setCurrentIndex(0)
        
        self.nrSrsRes2FreqPosLabel = QLabel('freqDomainPosition[0-67]:')
        self.nrSrsRes2FreqPosEdit = QLineEdit('0')
        self.nrSrsRes2FreqPosEdit.setValidator(QIntValidator(0, 67))
        
        self.nrSrsRes2FreqShiftLabel = QLabel('freqDomainShift[0-268]:')
        self.nrSrsRes2FreqShiftEdit = QLineEdit('0')
        self.nrSrsRes2FreqShiftEdit.setValidator(QIntValidator(0, 268))
        
        self.nrSrsRes2FreqHopCSrsLabel = QLabel('c-SRS[0-63]:')
        self.nrSrsRes2FreqHopCSrsEdit = QLineEdit('0')
        self.nrSrsRes2FreqHopCSrsEdit.setValidator(QIntValidator(0, 63))
        
        self.nrSrsRes2FreqHopBSrsLabel = QLabel('b-SRS[0-3]:')
        self.nrSrsRes2FreqHopBSrsEdit = QLineEdit('0')
        self.nrSrsRes2FreqHopBSrsEdit.setValidator(QIntValidator(0, 3))
        
        self.nrSrsRes2FreqHopBHopLabel = QLabel('b-hop[0-3]:')
        self.nrSrsRes2FreqHopBHopEdit = QLineEdit('0')
        self.nrSrsRes2FreqHopBHopEdit.setValidator(QIntValidator(0, 3))
        
        self.nrSrsRes2ResTypeLabel = QLabel('resourceType:')
        self.nrSrsRes2ResTypeComb = QComboBox()
        self.nrSrsRes2ResTypeComb.addItems(['aperiodic', 'semi-persistent', 'periodic'])
        self.nrSrsRes2ResTypeComb.setCurrentIndex(2)
        self.nrSrsRes2ResTypeComb.setEnabled(False)
        
        self.nrSrsRes2PeriodLabel = QLabel('SRS-Periodicity:')
        self.nrSrsRes2PeriodComb = QComboBox()
        self.nrSrsRes2PeriodComb.addItems(['sl1', 'sl2', 'sl4', 'sl5', 'sl8', 'sl10', 'sl16', 'sl20', 'sl32', 'sl40', 'sl64', 'sl80', 'sl160',
                                           'sl320', 'sl640', 'sl1280', 'sl2560'])
        self.nrSrsRes2PeriodComb.setCurrentIndex(3)
        
        self.nrSrsRes2OffsetLabel = QLabel('SRS-Offset[0-4]:')
        self.nrSrsRes2OffsetEdit = QLineEdit('0')
        self.nrSrsRes2OffsetEdit.setValidator(QIntValidator(0, 4))
        
        srsRes2Widget = QWidget()
        srsRes2GridLayout = QGridLayout()
        srsRes2GridLayout.addWidget(self.nrSrsRes2ResourceIdLabel, 0, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2ResourceIdEdit, 0, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2NumAntPortsLabel, 1, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2NumAntPortsComb, 1, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2NumCombLabel, 2, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2NumCombComb, 2, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2CombOffsetLabel, 3, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2CombOffsetEdit, 3, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2StartPosLabel, 4, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2StartPosEdit, 4, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2NumSymbsLabel, 5, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2NumSymbsComb, 5, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2RepFactorLabel, 6, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2RepFactorComb, 6, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqPosLabel, 7, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqPosEdit, 7, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqShiftLabel, 8, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqShiftEdit, 8, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopCSrsLabel, 9, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopCSrsEdit, 9, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopBSrsLabel, 10, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopBSrsEdit, 10, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopBHopLabel, 11, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopBHopEdit, 11, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2ResTypeLabel, 12, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2ResTypeComb, 12, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2PeriodLabel, 13, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2PeriodComb, 13, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2OffsetLabel, 14, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2OffsetEdit, 14, 1)
        srsRes2Layout = QVBoxLayout()
        srsRes2Layout.addLayout(srsRes2GridLayout)
        srsRes2Layout.addStretch()
        srsRes2Widget.setLayout(srsRes2Layout)
        
        srsRes2Scroll = QScrollArea()
        srsRes2Scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        srsRes2Scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        srsRes2Scroll.setWidgetResizable(True)
        srsRes2Scroll.setWidget(srsRes2Widget)
        
        #SRS-Resource item 3 
        self.nrSrsRes3ResourceIdLabel = QLabel('srs-ResourceId[0-63]:')
        self.nrSrsRes3ResourceIdEdit = QLineEdit()
        self.nrSrsRes3ResourceIdEdit.setText('3')
        self.nrSrsRes3ResourceIdEdit.setEnabled(False)
        
        self.nrSrsRes3NumAntPortsLabel = QLabel('nrofSRS-Ports:')
        self.nrSrsRes3NumAntPortsComb = QComboBox()
        self.nrSrsRes3NumAntPortsComb.addItems(['port1', 'port2', 'port4'])
        self.nrSrsRes3NumAntPortsComb.setCurrentIndex(0)
        
        self.nrSrsRes3NumCombLabel = QLabel('transmissionComb:')
        self.nrSrsRes3NumCombComb= QComboBox()
        self.nrSrsRes3NumCombComb.addItems(['n2', 'n4'])
        self.nrSrsRes3NumCombComb.setCurrentIndex(0)
        
        self.nrSrsRes3CombOffsetLabel = QLabel('combOffset[0-1]:')
        self.nrSrsRes3CombOffsetEdit = QLineEdit('0')
        self.nrSrsRes3CombOffsetEdit.setValidator(QIntValidator(0, 1))
        
        self.nrSrsRes3StartPosLabel = QLabel('startPosition[0-5]:')
        self.nrSrsRes3StartPosEdit = QLineEdit('0')
        self.nrSrsRes3StartPosEdit.setValidator(QIntValidator(0, 5))
        
        self.nrSrsRes3NumSymbsLabel = QLabel('nrofSymbols:')
        self.nrSrsRes3NumSymbsComb = QComboBox()
        self.nrSrsRes3NumSymbsComb.addItems(['n1', 'n2', 'n4'])
        self.nrSrsRes3NumSymbsComb.setCurrentIndex(0)
        
        self.nrSrsRes3RepFactorLabel = QLabel('repetitionFactor:')
        self.nrSrsRes3RepFactorComb = QComboBox()
        self.nrSrsRes3RepFactorComb.addItems(['n1', 'n2', 'n4'])
        self.nrSrsRes3RepFactorComb.setCurrentIndex(0)
        
        self.nrSrsRes3FreqPosLabel = QLabel('freqDomainPosition[0-67]:')
        self.nrSrsRes3FreqPosEdit = QLineEdit('0')
        self.nrSrsRes3FreqPosEdit.setValidator(QIntValidator(0, 67))
        
        self.nrSrsRes3FreqShiftLabel = QLabel('freqDomainShift[0-268]:')
        self.nrSrsRes3FreqShiftEdit = QLineEdit('0')
        self.nrSrsRes3FreqShiftEdit.setValidator(QIntValidator(0, 268))
        
        self.nrSrsRes3FreqHopCSrsLabel = QLabel('c-SRS[0-63]:')
        self.nrSrsRes3FreqHopCSrsEdit = QLineEdit('0')
        self.nrSrsRes3FreqHopCSrsEdit.setValidator(QIntValidator(0, 63))
        
        self.nrSrsRes3FreqHopBSrsLabel = QLabel('b-SRS[0-3]:')
        self.nrSrsRes3FreqHopBSrsEdit = QLineEdit('0')
        self.nrSrsRes3FreqHopBSrsEdit.setValidator(QIntValidator(0, 3))
        
        self.nrSrsRes3FreqHopBHopLabel = QLabel('b-hop[0-3]:')
        self.nrSrsRes3FreqHopBHopEdit = QLineEdit('0')
        self.nrSrsRes3FreqHopBHopEdit.setValidator(QIntValidator(0, 3))
        
        self.nrSrsRes3ResTypeLabel = QLabel('resourceType:')
        self.nrSrsRes3ResTypeComb = QComboBox()
        self.nrSrsRes3ResTypeComb.addItems(['aperiodic', 'semi-persistent', 'periodic'])
        self.nrSrsRes3ResTypeComb.setCurrentIndex(2)
        self.nrSrsRes3ResTypeComb.setEnabled(False)
        
        self.nrSrsRes3PeriodLabel = QLabel('SRS-Periodicity:')
        self.nrSrsRes3PeriodComb = QComboBox()
        self.nrSrsRes3PeriodComb.addItems(['sl1', 'sl2', 'sl4', 'sl5', 'sl8', 'sl10', 'sl16', 'sl20', 'sl32', 'sl40', 'sl64', 'sl80', 'sl160',
                                           'sl320', 'sl640', 'sl1280', 'sl2560'])
        self.nrSrsRes3PeriodComb.setCurrentIndex(3)
        
        self.nrSrsRes3OffsetLabel = QLabel('SRS-Offset[0-4]:')
        self.nrSrsRes3OffsetEdit = QLineEdit('0')
        self.nrSrsRes3OffsetEdit.setValidator(QIntValidator(0, 4))
        
        srsRes3Widget = QWidget()
        srsRes3GridLayout = QGridLayout()
        srsRes3GridLayout.addWidget(self.nrSrsRes3ResourceIdLabel, 0, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3ResourceIdEdit, 0, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3NumAntPortsLabel, 1, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3NumAntPortsComb, 1, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3NumCombLabel, 2, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3NumCombComb, 2, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3CombOffsetLabel, 3, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3CombOffsetEdit, 3, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3StartPosLabel, 4, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3StartPosEdit, 4, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3NumSymbsLabel, 5, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3NumSymbsComb, 5, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3RepFactorLabel, 6, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3RepFactorComb, 6, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqPosLabel, 7, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqPosEdit, 7, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqShiftLabel, 8, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqShiftEdit, 8, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopCSrsLabel, 9, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopCSrsEdit, 9, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopBSrsLabel, 10, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopBSrsEdit, 10, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopBHopLabel, 11, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopBHopEdit, 11, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3ResTypeLabel, 12, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3ResTypeComb, 12, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3PeriodLabel, 13, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3PeriodComb, 13, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3OffsetLabel, 14, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3OffsetEdit, 14, 1)
        srsRes3Layout = QVBoxLayout()
        srsRes3Layout.addLayout(srsRes3GridLayout)
        srsRes3Layout.addStretch()
        srsRes3Widget.setLayout(srsRes3Layout)
        
        srsRes3Scroll = QScrollArea()
        srsRes3Scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        srsRes3Scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        srsRes3Scroll.setWidgetResizable(True)
        srsRes3Scroll.setWidget(srsRes3Widget)
        
        srsResTabWidget = QTabWidget()
        srsResTabWidget.addTab(srsRes0Scroll, 'SRS resource 0')
        srsResTabWidget.addTab(srsRes1Scroll, 'SRS resource 1')
        srsResTabWidget.addTab(srsRes2Scroll, 'SRS resource 2')
        srsResTabWidget.addTab(srsRes3Scroll, 'SRS resource 3')
        
        #SRS-ResourceSet item 0 for codebook PUSCH
        self.nrSrsResSet0ResourceSetIdLabel = QLabel('srs-ResourceSetId[0-15]:')
        self.nrSrsResSet0ResourceSetIdEdit = QLineEdit()
        self.nrSrsResSet0ResourceSetIdEdit.setText('0')
        self.nrSrsResSet0ResourceSetIdEdit.setEnabled(False)
        
        self.nrSrsResSet0ResourceIdListLabel = QLabel('srs-ResourceIdList:')
        self.nrSrsResSet0ResourceIdListEdit = QLineEdit()
        self.nrSrsResSet0ResourceIdListEdit.setText('0')
        
        self.nrSrsResSet0ResTypeLabel = QLabel('resourceType:')
        self.nrSrsResSet0ResTypeComb = QComboBox()
        self.nrSrsResSet0ResTypeComb.addItems(['aperiodic', 'semi-persistent', 'periodic'])
        self.nrSrsResSet0ResTypeComb.setCurrentIndex(2)
        self.nrSrsResSet0ResTypeComb.setEnabled(False)
        
        self.nrSrsResSet0UsageLabel = QLabel('usage:')
        self.nrSrsResSet0UsageComb = QComboBox()
        self.nrSrsResSet0UsageComb.addItems(['beamManagement', 'codebook', 'nonCodebook', 'antennaSwitching'])
        self.nrSrsResSet0UsageComb.setCurrentIndex(1)
        self.nrSrsResSet0UsageComb.setEnabled(False)
        
        srsResSet0Widget = QWidget()
        srsResSet0GridLayout = QGridLayout()
        srsResSet0GridLayout.addWidget(self.nrSrsResSet0ResourceSetIdLabel, 0, 0)
        srsResSet0GridLayout.addWidget(self.nrSrsResSet0ResourceSetIdEdit, 0, 1)
        srsResSet0GridLayout.addWidget(self.nrSrsResSet0ResourceIdListLabel, 1, 0)
        srsResSet0GridLayout.addWidget(self.nrSrsResSet0ResourceIdListEdit, 1, 1)
        srsResSet0GridLayout.addWidget(self.nrSrsResSet0ResTypeLabel, 2, 0)
        srsResSet0GridLayout.addWidget(self.nrSrsResSet0ResTypeComb, 2, 1)
        srsResSet0GridLayout.addWidget(self.nrSrsResSet0UsageLabel, 3, 0)
        srsResSet0GridLayout.addWidget(self.nrSrsResSet0UsageComb, 3, 1)
        srsResSet0Layout = QVBoxLayout()
        srsResSet0Layout.addLayout(srsResSet0GridLayout)
        srsResSet0Layout.addStretch()
        srsResSet0Widget.setLayout(srsResSet0Layout)
        
        #SRS-ResourceSet item 1 for codebook PUSCH
        self.nrSrsResSet1ResourceSetIdLabel = QLabel('srs-ResourceSetId[0-15]:')
        self.nrSrsResSet1ResourceSetIdEdit = QLineEdit()
        self.nrSrsResSet1ResourceSetIdEdit.setText('1')
        self.nrSrsResSet1ResourceSetIdEdit.setEnabled(False)
        
        self.nrSrsResSet1ResourceIdListLabel = QLabel('srs-ResourceIdList:')
        self.nrSrsResSet1ResourceIdListEdit = QLineEdit()
        self.nrSrsResSet1ResourceIdListEdit.setText('0,1,2,3')
        
        self.nrSrsResSet1ResTypeLabel = QLabel('resourceType:')
        self.nrSrsResSet1ResTypeComb = QComboBox()
        self.nrSrsResSet1ResTypeComb.addItems(['aperiodic', 'semi-persistent', 'periodic'])
        self.nrSrsResSet1ResTypeComb.setCurrentIndex(2)
        self.nrSrsResSet1ResTypeComb.setEnabled(False)
        
        self.nrSrsResSet1UsageLabel = QLabel('usage:')
        self.nrSrsResSet1UsageComb = QComboBox()
        self.nrSrsResSet1UsageComb.addItems(['beamManagement', 'codebook', 'nonCodebook', 'antennaSwitching'])
        self.nrSrsResSet1UsageComb.setCurrentIndex(2)
        self.nrSrsResSet1UsageComb.setEnabled(False)
        
        srsResSet1Widget = QWidget()
        srsResSet1GridLayout = QGridLayout()
        srsResSet1GridLayout.addWidget(self.nrSrsResSet1ResourceSetIdLabel, 0, 0)
        srsResSet1GridLayout.addWidget(self.nrSrsResSet1ResourceSetIdEdit, 0, 1)
        srsResSet1GridLayout.addWidget(self.nrSrsResSet1ResourceIdListLabel, 1, 0)
        srsResSet1GridLayout.addWidget(self.nrSrsResSet1ResourceIdListEdit, 1, 1)
        srsResSet1GridLayout.addWidget(self.nrSrsResSet1ResTypeLabel, 2, 0)
        srsResSet1GridLayout.addWidget(self.nrSrsResSet1ResTypeComb, 2, 1)
        srsResSet1GridLayout.addWidget(self.nrSrsResSet1UsageLabel, 3, 0)
        srsResSet1GridLayout.addWidget(self.nrSrsResSet1UsageComb, 3, 1)
        srsResSet1Layout = QVBoxLayout()
        srsResSet1Layout.addLayout(srsResSet1GridLayout)
        srsResSet1Layout.addStretch()
        srsResSet1Widget.setLayout(srsResSet1Layout)
        
        srsResSetTabWidget = QTabWidget()
        srsResSetTabWidget.addTab(srsResSet0Widget, 'SRS resource set 0')
        srsResSetTabWidget.addTab(srsResSet1Widget, 'SRS resource set 1')
        
        srsWidget = QWidget()
        srsLayout = QVBoxLayout()
        srsLayout.addWidget(srsResTabWidget)
        srsLayout.addWidget(srsResSetTabWidget)
        srsLayout.addStretch()
        srsWidget.setLayout(srsLayout)
        
        #pucch settings
        #PUCCH-FormatConfig for pucch format 1/2/3/4
        self.nrDedPucchFmt134NumSlotsLabel = QLabel('nrofSlots(Format 1/3/4):')
        self.nrDedPucchFmt134NumSlotsComb = QComboBox()
        self.nrDedPucchFmt134NumSlotsComb.addItems(['n1', 'n2', 'n4', 'n8'])
        self.nrDedPucchFmt134NumSlotsComb.setCurrentIndex(0)
        
        self.nrDedPucchFmt134InterSlotFreqHopLabel = QLabel('interslotFrequencyHopping(Format 1/3/4):')
        self.nrDedPucchFmt134InterSlotFreqHopComb = QComboBox()
        self.nrDedPucchFmt134InterSlotFreqHopComb.addItems(['disabled', 'enabled'])
        self.nrDedPucchFmt134InterSlotFreqHopComb.setCurrentIndex(0)
        
        self.nrDedPucchFmt34AddDmrsLabel = QLabel('additionalDMRS(Format 3/4):')
        self.nrDedPucchFmt34AddDmrsComb = QComboBox()
        self.nrDedPucchFmt34AddDmrsComb.addItems(['false', 'true'])
        self.nrDedPucchFmt34AddDmrsComb.setCurrentIndex(1)
        
        self.nrDedPucchFmt234SimulAckCsiLabel = QLabel('simultaneousHARQ-ACK-CSI(Format 2/3/4):')
        self.nrDedPucchFmt234SimulAckCsiComb = QComboBox()
        self.nrDedPucchFmt234SimulAckCsiComb.addItems(['false', 'true'])
        self.nrDedPucchFmt234SimulAckCsiComb.setCurrentIndex(1)
        
        dedPucchFmtCfgWidget = QWidget()
        dedPucchFmtCfgGridLayout = QGridLayout()
        dedPucchFmtCfgGridLayout.addWidget(self.nrDedPucchFmt134NumSlotsLabel, 0, 0)
        dedPucchFmtCfgGridLayout.addWidget(self.nrDedPucchFmt134NumSlotsComb, 0, 1)
        dedPucchFmtCfgGridLayout.addWidget(self.nrDedPucchFmt134InterSlotFreqHopLabel, 1, 0)
        dedPucchFmtCfgGridLayout.addWidget(self.nrDedPucchFmt134InterSlotFreqHopComb, 1, 1)
        dedPucchFmtCfgGridLayout.addWidget(self.nrDedPucchFmt34AddDmrsLabel, 2, 0)
        dedPucchFmtCfgGridLayout.addWidget(self.nrDedPucchFmt34AddDmrsComb, 2, 1)
        dedPucchFmtCfgGridLayout.addWidget(self.nrDedPucchFmt234SimulAckCsiLabel, 3, 0)
        dedPucchFmtCfgGridLayout.addWidget(self.nrDedPucchFmt234SimulAckCsiComb, 3, 1)
        dedPucchFmtCfgLayout = QVBoxLayout()
        dedPucchFmtCfgLayout.addLayout(dedPucchFmtCfgGridLayout)
        dedPucchFmtCfgLayout.addStretch()
        dedPucchFmtCfgWidget.setLayout(dedPucchFmtCfgLayout)
        
        #PUCCH-Resource item 0 for pucch format 0
        self.nrDedPucchRes0ResourceIdLabel = QLabel('pucch-ResourceId[0-55]:')
        self.nrDedPucchRes0ResourceIdEdit = QLineEdit()
        self.nrDedPucchRes0ResourceIdEdit.setText('0')
        self.nrDedPucchRes0ResourceIdEdit.setEnabled(False)
        
        self.nrDedPucchRes0FormatLabel = QLabel('format:')
        self.nrDedPucchRes0FormatComb = QComboBox()
        self.nrDedPucchRes0FormatComb.addItems(['format 0', 'format 1', 'format 2', 'format 3', 'format 4'])
        self.nrDedPucchRes0FormatComb.setCurrentIndex(0)
        self.nrDedPucchRes0FormatComb.setEnabled(False)
        
        self.nrDedPucchRes0ResourceSetIdLabel = QLabel('pucch-ResourceSetId[0-3]:')
        self.nrDedPucchRes0ResourceSetIdEdit = QLineEdit()
        self.nrDedPucchRes0ResourceSetIdEdit.setText('0')
        self.nrDedPucchRes0ResourceSetIdEdit.setEnabled(False)
        
        self.nrDedPucchRes0StartingPrbLabel = QLabel('startingPRB[0-274]:')
        self.nrDedPucchRes0StartingPrbEdit = QLineEdit()
        self.nrDedPucchRes0StartingPrbEdit.setValidator(QIntValidator(0, 274))
        
        self.nrDedPucchRes0IntraSlotFreqHopLabel = QLabel('intraSlotFrequencyHopping:')
        self.nrDedPucchRes0IntraSlotFreqHopComb = QComboBox()
        self.nrDedPucchRes0IntraSlotFreqHopComb.addItems(['disabled', 'enabled'])
        self.nrDedPucchRes0IntraSlotFreqHopComb.setCurrentIndex(0)
        
        self.nrDedPucchRes0SecondHopPrbLabel = QLabel('secondHopPRB[0-274]:')
        self.nrDedPucchRes0SecondHopPrbEdit = QLineEdit()
        self.nrDedPucchRes0SecondHopPrbEdit.setValidator(QIntValidator(0, 274))
        
        self.nrDedPucchRes0NumPrbsLabel = QLabel('nrofPRBs[1]:')
        self.nrDedPucchRes0NumPrbsEdit = QLineEdit('1')
        self.nrDedPucchRes0NumPrbsEdit.setEnabled(False)
        
        self.nrDedPucchRes0StartingSymbLabel = QLabel('startingSymbolIndex[0-13]:')
        self.nrDedPucchRes0StartingSymbEdit = QLineEdit('0')
        self.nrDedPucchRes0StartingSymbEdit.setValidator(QIntValidator(0, 13))
        
        self.nrDedPucchRes0NumSymbsLabel = QLabel('nrofSymbols[1-2]:')
        self.nrDedPucchRes0NumSymbEdit = QLineEdit('1')
        self.nrDedPucchRes0NumSymbEdit.setValidator(QIntValidator(1, 2))
        
        dedPucchRes0Widget = QWidget()
        dedPucchRes0GridLayout = QGridLayout()
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0ResourceIdLabel, 0, 0)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0ResourceIdEdit, 0, 1)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0FormatLabel, 1, 0)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0FormatComb, 1, 1)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0ResourceSetIdLabel, 2, 0)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0ResourceSetIdEdit, 2, 1)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0StartingPrbLabel, 3, 0)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0StartingPrbEdit, 3, 1)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0IntraSlotFreqHopLabel, 4, 0)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0IntraSlotFreqHopComb, 4, 1)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0SecondHopPrbLabel, 5, 0)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0SecondHopPrbEdit, 5, 1)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0NumPrbsLabel, 6, 0)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0NumPrbsEdit, 6, 1)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0StartingSymbLabel, 7, 0)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0StartingSymbEdit, 7, 1)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0NumSymbsLabel, 8, 0)
        dedPucchRes0GridLayout.addWidget(self.nrDedPucchRes0NumSymbEdit, 8, 1)
        dedPucchRes0Layout = QVBoxLayout()
        dedPucchRes0Layout.addLayout(dedPucchRes0GridLayout)
        dedPucchRes0Layout.addStretch()
        dedPucchRes0Widget.setLayout(dedPucchRes0Layout)
        
        #PUCCH-Resource item 1 for pucch format 1
        self.nrDedPucchRes1ResourceIdLabel = QLabel('pucch-ResourceId[0-55]:')
        self.nrDedPucchRes1ResourceIdEdit = QLineEdit()
        self.nrDedPucchRes1ResourceIdEdit.setText('1')
        self.nrDedPucchRes1ResourceIdEdit.setEnabled(False)
        
        self.nrDedPucchRes1FormatLabel = QLabel('format:')
        self.nrDedPucchRes1FormatComb = QComboBox()
        self.nrDedPucchRes1FormatComb.addItems(['format 0', 'format 1', 'format 2', 'format 3', 'format 4'])
        self.nrDedPucchRes1FormatComb.setCurrentIndex(1)
        self.nrDedPucchRes1FormatComb.setEnabled(False)
        
        self.nrDedPucchRes1ResourceSetIdLabel = QLabel('pucch-ResourceSetId[0-3]:')
        self.nrDedPucchRes1ResourceSetIdEdit = QLineEdit()
        self.nrDedPucchRes1ResourceSetIdEdit.setText('0')
        self.nrDedPucchRes1ResourceSetIdEdit.setEnabled(False)
        
        self.nrDedPucchRes1StartingPrbLabel = QLabel('startingPRB[0-274]:')
        self.nrDedPucchRes1StartingPrbEdit = QLineEdit()
        self.nrDedPucchRes1StartingPrbEdit.setValidator(QIntValidator(0, 274))
        
        self.nrDedPucchRes1IntraSlotFreqHopLabel = QLabel('intraSlotFrequencyHopping:')
        self.nrDedPucchRes1IntraSlotFreqHopComb = QComboBox()
        self.nrDedPucchRes1IntraSlotFreqHopComb.addItems(['disabled', 'enabled'])
        self.nrDedPucchRes1IntraSlotFreqHopComb.setCurrentIndex(0)
        
        self.nrDedPucchRes1SecondHopPrbLabel = QLabel('secondHopPRB[0-274]:')
        self.nrDedPucchRes1SecondHopPrbEdit = QLineEdit()
        self.nrDedPucchRes1SecondHopPrbEdit.setValidator(QIntValidator(0, 274))
        
        self.nrDedPucchRes1NumPrbsLabel = QLabel('nrofPRBs[1]:')
        self.nrDedPucchRes1NumPrbsEdit = QLineEdit('1')
        self.nrDedPucchRes1NumPrbsEdit.setEnabled(False)
        
        self.nrDedPucchRes1StartingSymbLabel = QLabel('startingSymbolIndex[0-10]:')
        self.nrDedPucchRes1StartingSymbEdit = QLineEdit('0')
        self.nrDedPucchRes1StartingSymbEdit.setValidator(QIntValidator(0, 10))
        
        self.nrDedPucchRes1NumSymbsLabel = QLabel('nrofSymbols[4-14]:')
        self.nrDedPucchRes1NumSymbEdit = QLineEdit('4')
        self.nrDedPucchRes1NumSymbEdit.setValidator(QIntValidator(4, 14))
        
        dedPucchRes1Widget = QWidget()
        dedPucchRes1GridLayout = QGridLayout()
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1ResourceIdLabel, 0, 0)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1ResourceIdEdit, 0, 1)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1FormatLabel, 1, 0)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1FormatComb, 1, 1)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1ResourceSetIdLabel, 2, 0)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1ResourceSetIdEdit, 2, 1)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1StartingPrbLabel, 3, 0)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1StartingPrbEdit, 3, 1)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1IntraSlotFreqHopLabel, 4, 0)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1IntraSlotFreqHopComb, 4, 1)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1SecondHopPrbLabel, 5, 0)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1SecondHopPrbEdit, 5, 1)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1NumPrbsLabel, 6, 0)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1NumPrbsEdit, 6, 1)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1StartingSymbLabel, 7, 0)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1StartingSymbEdit, 7, 1)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1NumSymbsLabel, 8, 0)
        dedPucchRes1GridLayout.addWidget(self.nrDedPucchRes1NumSymbEdit, 8, 1)
        dedPucchRes1Layout = QVBoxLayout()
        dedPucchRes1Layout.addLayout(dedPucchRes1GridLayout)
        dedPucchRes1Layout.addStretch()
        dedPucchRes1Widget.setLayout(dedPucchRes1Layout)
        
        #PUCCH-Resource item 2 for pucch format 2
        self.nrDedPucchRes2ResourceIdLabel = QLabel('pucch-ResourceId[0-55]:')
        self.nrDedPucchRes2ResourceIdEdit = QLineEdit()
        self.nrDedPucchRes2ResourceIdEdit.setText('2')
        self.nrDedPucchRes2ResourceIdEdit.setEnabled(False)
        
        self.nrDedPucchRes2FormatLabel = QLabel('format:')
        self.nrDedPucchRes2FormatComb = QComboBox()
        self.nrDedPucchRes2FormatComb.addItems(['format 0', 'format 1', 'format 2', 'format 3', 'format 4'])
        self.nrDedPucchRes2FormatComb.setCurrentIndex(2)
        self.nrDedPucchRes2FormatComb.setEnabled(False)
        
        self.nrDedPucchRes2ResourceSetIdLabel = QLabel('pucch-ResourceSetId[0-3]:')
        self.nrDedPucchRes2ResourceSetIdEdit = QLineEdit()
        self.nrDedPucchRes2ResourceSetIdEdit.setText('1')
        self.nrDedPucchRes2ResourceSetIdEdit.setEnabled(False)
        
        self.nrDedPucchRes2StartingPrbLabel = QLabel('startingPRB[0-274]:')
        self.nrDedPucchRes2StartingPrbEdit = QLineEdit()
        self.nrDedPucchRes2StartingPrbEdit.setValidator(QIntValidator(0, 274))
        
        self.nrDedPucchRes2IntraSlotFreqHopLabel = QLabel('intraSlotFrequencyHopping:')
        self.nrDedPucchRes2IntraSlotFreqHopComb = QComboBox()
        self.nrDedPucchRes2IntraSlotFreqHopComb.addItems(['disabled', 'enabled'])
        self.nrDedPucchRes2IntraSlotFreqHopComb.setCurrentIndex(0)
        
        self.nrDedPucchRes2SecondHopPrbLabel = QLabel('secondHopPRB[0-274]:')
        self.nrDedPucchRes2SecondHopPrbEdit = QLineEdit()
        self.nrDedPucchRes2SecondHopPrbEdit.setValidator(QIntValidator(0, 274))
        
        self.nrDedPucchRes2NumPrbsLabel = QLabel('nrofPRBs[1-16]:')
        self.nrDedPucchRes2NumPrbsEdit = QLineEdit('1')
        self.nrDedPucchRes2NumPrbsEdit.setValidator(QIntValidator(1, 16))
        
        self.nrDedPucchRes2StartingSymbLabel = QLabel('startingSymbolIndex[0-13]:')
        self.nrDedPucchRes2StartingSymbEdit = QLineEdit('0')
        self.nrDedPucchRes2StartingSymbEdit.setValidator(QIntValidator(0, 13))
        
        self.nrDedPucchRes2NumSymbsLabel = QLabel('nrofSymbols[1-2]:')
        self.nrDedPucchRes2NumSymbEdit = QLineEdit('1')
        self.nrDedPucchRes2NumSymbEdit.setValidator(QIntValidator(1, 2))
        
        dedPucchRes2Widget = QWidget()
        dedPucchRes2GridLayout = QGridLayout()
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2ResourceIdLabel, 0, 0)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2ResourceIdEdit, 0, 1)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2FormatLabel, 1, 0)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2FormatComb, 1, 1)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2ResourceSetIdLabel, 2, 0)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2ResourceSetIdEdit, 2, 1)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2StartingPrbLabel, 3, 0)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2StartingPrbEdit, 3, 1)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2IntraSlotFreqHopLabel, 4, 0)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2IntraSlotFreqHopComb, 4, 1)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2SecondHopPrbLabel, 5, 0)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2SecondHopPrbEdit, 5, 1)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2NumPrbsLabel, 6, 0)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2NumPrbsEdit, 6, 1)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2StartingSymbLabel, 7, 0)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2StartingSymbEdit, 7, 1)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2NumSymbsLabel, 8, 0)
        dedPucchRes2GridLayout.addWidget(self.nrDedPucchRes2NumSymbEdit, 8, 1)
        dedPucchRes2Layout = QVBoxLayout()
        dedPucchRes2Layout.addLayout(dedPucchRes2GridLayout)
        dedPucchRes2Layout.addStretch()
        dedPucchRes2Widget.setLayout(dedPucchRes2Layout)
        
        #PUCCH-Resource item 3 for pucch format 3
        self.nrDedPucchRes3ResourceIdLabel = QLabel('pucch-ResourceId[0-55]:')
        self.nrDedPucchRes3ResourceIdEdit = QLineEdit()
        self.nrDedPucchRes3ResourceIdEdit.setText('3')
        self.nrDedPucchRes3ResourceIdEdit.setEnabled(False)
        
        self.nrDedPucchRes3FormatLabel = QLabel('format:')
        self.nrDedPucchRes3FormatComb = QComboBox()
        self.nrDedPucchRes3FormatComb.addItems(['format 0', 'format 1', 'format 2', 'format 3', 'format 4'])
        self.nrDedPucchRes3FormatComb.setCurrentIndex(3)
        self.nrDedPucchRes3FormatComb.setEnabled(False)
        
        self.nrDedPucchRes3ResourceSetIdLabel = QLabel('pucch-ResourceSetId[0-3]:')
        self.nrDedPucchRes3ResourceSetIdEdit = QLineEdit()
        self.nrDedPucchRes3ResourceSetIdEdit.setText('1')
        self.nrDedPucchRes3ResourceSetIdEdit.setEnabled(False)
        
        self.nrDedPucchRes3StartingPrbLabel = QLabel('startingPRB[0-274]:')
        self.nrDedPucchRes3StartingPrbEdit = QLineEdit()
        self.nrDedPucchRes3StartingPrbEdit.setValidator(QIntValidator(0, 274))
        
        self.nrDedPucchRes3IntraSlotFreqHopLabel = QLabel('intraSlotFrequencyHopping:')
        self.nrDedPucchRes3IntraSlotFreqHopComb = QComboBox()
        self.nrDedPucchRes3IntraSlotFreqHopComb.addItems(['disabled', 'enabled'])
        self.nrDedPucchRes3IntraSlotFreqHopComb.setCurrentIndex(0)
        
        self.nrDedPucchRes3SecondHopPrbLabel = QLabel('secondHopPRB[0-274]:')
        self.nrDedPucchRes3SecondHopPrbEdit = QLineEdit()
        self.nrDedPucchRes3SecondHopPrbEdit.setValidator(QIntValidator(0, 274))
        
        self.nrDedPucchRes3NumPrbsLabel = QLabel('nrofPRBs[1-16]:')
        self.nrDedPucchRes3NumPrbsEdit = QLineEdit('1')
        self.nrDedPucchRes3NumPrbsEdit.setValidator(QIntValidator(1, 16))
        
        self.nrDedPucchRes3StartingSymbLabel = QLabel('startingSymbolIndex[0-10]:')
        self.nrDedPucchRes3StartingSymbEdit = QLineEdit('0')
        self.nrDedPucchRes3StartingSymbEdit.setValidator(QIntValidator(0, 10))
        
        self.nrDedPucchRes3NumSymbsLabel = QLabel('nrofSymbols[4-14]:')
        self.nrDedPucchRes3NumSymbEdit = QLineEdit('4')
        self.nrDedPucchRes3NumSymbEdit.setValidator(QIntValidator(4, 14))
        
        dedPucchRes3Widget = QWidget()
        dedPucchRes3GridLayout = QGridLayout()
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3ResourceIdLabel, 0, 0)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3ResourceIdEdit, 0, 1)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3FormatLabel, 1, 0)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3FormatComb, 1, 1)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3ResourceSetIdLabel, 2, 0)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3ResourceSetIdEdit, 2, 1)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3StartingPrbLabel, 3, 0)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3StartingPrbEdit, 3, 1)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3IntraSlotFreqHopLabel, 4, 0)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3IntraSlotFreqHopComb, 4, 1)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3SecondHopPrbLabel, 5, 0)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3SecondHopPrbEdit, 5, 1)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3NumPrbsLabel, 6, 0)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3NumPrbsEdit, 6, 1)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3StartingSymbLabel, 7, 0)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3StartingSymbEdit, 7, 1)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3NumSymbsLabel, 8, 0)
        dedPucchRes3GridLayout.addWidget(self.nrDedPucchRes3NumSymbEdit, 8, 1)
        dedPucchRes3Layout = QVBoxLayout()
        dedPucchRes3Layout.addLayout(dedPucchRes3GridLayout)
        dedPucchRes3Layout.addStretch()
        dedPucchRes3Widget.setLayout(dedPucchRes3Layout)
        
        #PUCCH-Resource item 4 for pucch format 4
        self.nrDedPucchRes4ResourceIdLabel = QLabel('pucch-ResourceId[0-55]:')
        self.nrDedPucchRes4ResourceIdEdit = QLineEdit()
        self.nrDedPucchRes4ResourceIdEdit.setText('4')
        self.nrDedPucchRes4ResourceIdEdit.setEnabled(False)
        
        self.nrDedPucchRes4FormatLabel = QLabel('format:')
        self.nrDedPucchRes4FormatComb = QComboBox()
        self.nrDedPucchRes4FormatComb.addItems(['format 0', 'format 1', 'format 2', 'format 3', 'format 4'])
        self.nrDedPucchRes4FormatComb.setCurrentIndex(4)
        self.nrDedPucchRes4FormatComb.setEnabled(False)
        
        self.nrDedPucchRes4ResourceSetIdLabel = QLabel('pucch-ResourceSetId[0-3]:')
        self.nrDedPucchRes4ResourceSetIdEdit = QLineEdit()
        self.nrDedPucchRes4ResourceSetIdEdit.setText('1')
        self.nrDedPucchRes4ResourceSetIdEdit.setEnabled(False)
        
        self.nrDedPucchRes4StartingPrbLabel = QLabel('startingPRB[0-274]:')
        self.nrDedPucchRes4StartingPrbEdit = QLineEdit()
        self.nrDedPucchRes4StartingPrbEdit.setValidator(QIntValidator(0, 274))
        
        self.nrDedPucchRes4IntraSlotFreqHopLabel = QLabel('intraSlotFrequencyHopping:')
        self.nrDedPucchRes4IntraSlotFreqHopComb = QComboBox()
        self.nrDedPucchRes4IntraSlotFreqHopComb.addItems(['disabled', 'enabled'])
        self.nrDedPucchRes4IntraSlotFreqHopComb.setCurrentIndex(0)
        
        self.nrDedPucchRes4SecondHopPrbLabel = QLabel('secondHopPRB[0-274]:')
        self.nrDedPucchRes4SecondHopPrbEdit = QLineEdit()
        self.nrDedPucchRes4SecondHopPrbEdit.setValidator(QIntValidator(0, 274))
        
        self.nrDedPucchRes4NumPrbsLabel = QLabel('nrofPRBs[1]:')
        self.nrDedPucchRes4NumPrbsEdit = QLineEdit('1')
        self.nrDedPucchRes4NumPrbsEdit.setEnabled(False)
        
        self.nrDedPucchRes4StartingSymbLabel = QLabel('startingSymbolIndex[0-10]:')
        self.nrDedPucchRes4StartingSymbEdit = QLineEdit('0')
        self.nrDedPucchRes4StartingSymbEdit.setValidator(QIntValidator(0, 10))
        
        self.nrDedPucchRes4NumSymbsLabel = QLabel('nrofSymbols[4-14]:')
        self.nrDedPucchRes4NumSymbEdit = QLineEdit('4')
        self.nrDedPucchRes4NumSymbEdit.setValidator(QIntValidator(4, 14))
        
        dedPucchRes4Widget = QWidget()
        dedPucchRes4GridLayout = QGridLayout()
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4ResourceIdLabel, 0, 0)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4ResourceIdEdit, 0, 1)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4FormatLabel, 1, 0)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4FormatComb, 1, 1)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4ResourceSetIdLabel, 2, 0)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4ResourceSetIdEdit, 2, 1)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4StartingPrbLabel, 3, 0)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4StartingPrbEdit, 3, 1)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4IntraSlotFreqHopLabel, 4, 0)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4IntraSlotFreqHopComb, 4, 1)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4SecondHopPrbLabel, 5, 0)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4SecondHopPrbEdit, 5, 1)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4NumPrbsLabel, 6, 0)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4NumPrbsEdit, 6, 1)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4StartingSymbLabel, 7, 0)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4StartingSymbEdit, 7, 1)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4NumSymbsLabel, 8, 0)
        dedPucchRes4GridLayout.addWidget(self.nrDedPucchRes4NumSymbEdit, 8, 1)
        dedPucchRes4Layout = QVBoxLayout()
        dedPucchRes4Layout.addLayout(dedPucchRes4GridLayout)
        dedPucchRes4Layout.addStretch()
        dedPucchRes4Widget.setLayout(dedPucchRes4Layout)
        
        #SchedulingRequestResourceConfig item 0 for dynamic SR using pucch format 0
        self.nrDsrRes0SrResourceIdLabel = QLabel('schedulingRequestResourceId[0-7]:')
        self.nrDsrRes0SrResourceIdEdit = QLineEdit()
        self.nrDsrRes0SrResourceIdEdit.setText('0')
        self.nrDsrRes0SrResourceIdEdit.setEnabled(False)
        
        self.nrDsrRes0ResourceIdLabel= QLabel('resource(PUCCH-ResourceId)[0-55]:')
        self.nrDsrRes0ResourceIdEdit = QLineEdit()
        self.nrDsrRes0ResourceIdEdit.setText('0')
        self.nrDsrRes0ResourceIdEdit.setEnabled(False)
        
        self.nrDsrRes0PeriodicityLabel = QLabel('periodicity:')
        self.nrDsrRes0PeriodicityComb = QComboBox()
        self.nrDsrRes0PeriodicityComb.addItems(['sym2', 'sym6or7', 'sl1', 'sl2', 'sl4', 'sl5', 'sl8', 'sl10', 'sl16', 'sl20',
                                                        'sl40', 'sl80', 'sl160', 'sl320', 'sl640'])
        self.nrDsrRes0PeriodicityComb.setCurrentIndex(5)
        
        self.nrDsrRes0OffsetLabel = QLabel('offset(in slots)[0-4]:')
        self.nrDsrRes0OffsetEdit = QLineEdit('0')
        self.nrDsrRes0OffsetEdit.setValidator(QIntValidator(0, 4))
        
        dsrRes0Widget = QWidget()
        dsrRes0GridLayout = QGridLayout()
        dsrRes0GridLayout.addWidget(self.nrDsrRes0SrResourceIdLabel, 0, 0)
        dsrRes0GridLayout.addWidget(self.nrDsrRes0SrResourceIdEdit, 0, 1)
        dsrRes0GridLayout.addWidget(self.nrDsrRes0ResourceIdLabel, 1, 0)
        dsrRes0GridLayout.addWidget(self.nrDsrRes0ResourceIdEdit, 1, 1)
        dsrRes0GridLayout.addWidget(self.nrDsrRes0PeriodicityLabel, 2, 0)
        dsrRes0GridLayout.addWidget(self.nrDsrRes0PeriodicityComb, 2, 1)
        dsrRes0GridLayout.addWidget(self.nrDsrRes0OffsetLabel, 3, 0)
        dsrRes0GridLayout.addWidget(self.nrDsrRes0OffsetEdit, 3, 1)
        dsrRes0Layout = QVBoxLayout()
        dsrRes0Layout.addLayout(dsrRes0GridLayout)
        dsrRes0Layout.addStretch()
        dsrRes0Widget.setLayout(dsrRes0Layout)
        
        #SchedulingRequestResourceConfig item 1 for dynamic SR using pucch format 1
        self.nrDsrRes1SrResourceIdLabel = QLabel('schedulingRequestResourceId[0-7]:')
        self.nrDsrRes1SrResourceIdEdit = QLineEdit()
        self.nrDsrRes1SrResourceIdEdit.setText('1')
        self.nrDsrRes1SrResourceIdEdit.setEnabled(False)
        
        self.nrDsrRes1ResourceIdLabel= QLabel('resource(PUCCH-ResourceId)[0-55]:')
        self.nrDsrRes1ResourceIdEdit = QLineEdit()
        self.nrDsrRes1ResourceIdEdit.setText('1')
        self.nrDsrRes1ResourceIdEdit.setEnabled(False)
        
        self.nrDsrRes1PeriodicityLabel = QLabel('periodicity:')
        self.nrDsrRes1PeriodicityComb = QComboBox()
        self.nrDsrRes1PeriodicityComb.addItems(['sym2', 'sym6or7', 'sl1', 'sl2', 'sl4', 'sl5', 'sl8', 'sl10', 'sl16', 'sl20',
                                                        'sl40', 'sl80', 'sl160', 'sl320', 'sl640'])
        self.nrDsrRes1PeriodicityComb.setCurrentIndex(5)
        
        self.nrDsrRes1OffsetLabel = QLabel('offset(in slots)[0-4]:')
        self.nrDsrRes1OffsetEdit = QLineEdit('0')
        self.nrDsrRes1OffsetEdit.setValidator(QIntValidator(0, 4))
        
        dsrRes1Widget = QWidget()
        dsrRes1GridLayout = QGridLayout()
        dsrRes1GridLayout.addWidget(self.nrDsrRes1SrResourceIdLabel, 0, 0)
        dsrRes1GridLayout.addWidget(self.nrDsrRes1SrResourceIdEdit, 0, 1)
        dsrRes1GridLayout.addWidget(self.nrDsrRes1ResourceIdLabel, 1, 0)
        dsrRes1GridLayout.addWidget(self.nrDsrRes1ResourceIdEdit, 1, 1)
        dsrRes1GridLayout.addWidget(self.nrDsrRes1PeriodicityLabel, 2, 0)
        dsrRes1GridLayout.addWidget(self.nrDsrRes1PeriodicityComb, 2, 1)
        dsrRes1GridLayout.addWidget(self.nrDsrRes1OffsetLabel, 3, 0)
        dsrRes1GridLayout.addWidget(self.nrDsrRes1OffsetEdit, 3, 1)
        dsrRes1Layout = QVBoxLayout()
        dsrRes1Layout.addLayout(dsrRes1GridLayout)
        dsrRes1Layout.addStretch()
        dsrRes1Widget.setLayout(dsrRes1Layout)
        
        dedPucchResTabWidget = QTabWidget()
        dedPucchResTabWidget.addTab(dedPucchFmtCfgWidget, 'PUCCH-FormatConfig')
        dedPucchResTabWidget.addTab(dedPucchRes0Widget, 'PUCCH resource 0')
        dedPucchResTabWidget.addTab(dedPucchRes1Widget, 'PUCCH resource 1')
        dedPucchResTabWidget.addTab(dedPucchRes2Widget, 'PUCCH resource 2')
        dedPucchResTabWidget.addTab(dedPucchRes3Widget, 'PUCCH resource 3')
        dedPucchResTabWidget.addTab(dedPucchRes4Widget, 'PUCCH resource 4')
        
        dsrResTabWidget = QTabWidget()
        dsrResTabWidget.addTab(dsrRes0Widget, 'DSR resource 0')
        dsrResTabWidget.addTab(dsrRes1Widget, 'DSR resource 1')
        
        dedPucchWidget = QWidget()
        dedPucchLayout = QVBoxLayout()
        dedPucchLayout.addWidget(dedPucchResTabWidget)
        dedPucchLayout.addWidget(dsrResTabWidget)
        dedPucchWidget.setLayout(dedPucchLayout)
        
        dedUlBwpTabWidget = QTabWidget()
        dedUlBwpTabWidget.addTab(dedPuschCfgWidget, 'PUSCH-Config')
        dedUlBwpTabWidget.addTab(dmrsDedPuschWidget, 'DM-RS(PUSCH)')
        dedUlBwpTabWidget.addTab(srsWidget, 'SRS')
        dedUlBwpTabWidget.addTab(dedPucchWidget, 'PUCCH-Config')
        
        dedUlBwpWidget = QWidget()
        dedUlBwpLayout = QVBoxLayout()
        dedUlBwpLayout.addWidget(dedUlBwpGrpBox)
        dedUlBwpLayout.addWidget(dedUlBwpTabWidget)
        dedUlBwpLayout.addStretch()
        dedUlBwpWidget.setLayout(dedUlBwpLayout)
        
        bwpCfgTabWidget = QTabWidget()
        bwpCfgTabWidget.addTab(iniDlBwpWidget, 'Initial DL BWP')
        bwpCfgTabWidget.addTab(iniUlBwpWidget, 'Initial UL BWP')
        bwpCfgTabWidget.addTab(dedDlBwpWidget, 'Dedicated DL BWP')
        bwpCfgTabWidget.addTab(dedUlBwpWidget, 'Dedicated UL BWP')

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
        self.coreset0Offset = 0
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
            self.nrSsbKssbEdit.setValidator(QIntValidator(0, 11))
            self.nrSsbNCrbSsbEdit.setText(str(minGuardBand+offset))
        elif key in ('30_15', '30_30'):
            self.nrSsbKssbLabel.setText('k_SSB[0-23]:')
            self.nrSsbKssbEdit.setValidator(QIntValidator(0, 23))
            self.nrSsbNCrbSsbEdit.setText(str(2*(minGuardBand+offset)))
        elif key == '60_240':
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            self.nrSsbKssbEdit.setValidator(QIntValidator(0, 11))
            minGuardBand240k = int(self.nrSsbMinGuardBandScs240kEdit.text())
            self.nrSsbNCrbSsbEdit.setText(str(max(minGuardBand+offset, 4*minGuardBand240k)))
        elif key == '120_120':
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            self.nrSsbKssbEdit.setValidator(QIntValidator(0, 11))
            self.nrSsbNCrbSsbEdit.setText(str(2*(minGuardBand+offset)))
        elif key == '120_240':
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            self.nrSsbKssbEdit.setValidator(QIntValidator(0, 11))
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
        self.flagCoreset0 = self.validateCoreset0()
        if self.flagCoreset0:
            self.updateKSsbAndNCrbSsb(offset=0 if self.coreset0Offset <= 0 else self.coreset0Offset)

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
        self.flagCoreset0 = self.validateCoreset0()
        if self.flagCoreset0:
            self.updateKSsbAndNCrbSsb(offset=0 if self.coreset0Offset <= 0 else self.coreset0Offset)

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
        self.flagCoreset0 = self.validateCoreset0()
        if self.flagCoreset0:
            self.updateKSsbAndNCrbSsb(offset=0 if self.coreset0Offset <= 0 else self.coreset0Offset)
    
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
        if not self.nrMibCoreset0Edit.text():
            return False
        
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
        self.coreset0MultiplexingPat, self.coreset0NumRbs, self.coreset0NumSymbs, self.coreset0OffsetList = val
        if int(self.nrCarrierNumRbEdit.text()) < self.coreset0NumRbs:
            self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid CORESET0 setting: CORESET0 numRBs=%d, while carrier numRBs=%s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.coreset0NumRbs, self.nrCarrierNumRbEdit.text()))
            return False
        
        #(3) if k_ssb is configured, further validate CORESET0
        if self.nrSsbKssbEdit.text():
            kSsb = int(self.nrSsbKssbEdit.text())
            if len(self.coreset0OffsetList) == 2:
                self.coreset0Offset = self.coreset0OffsetList[0] if kSsb == 0 else self.coreset0OffsetList[1] 
            else:
                self.coreset0Offset = self.coreset0OffsetList[0]
                
            '''
            if offset > 0, min bw = max(self.coreset0NumRbs, offset + 20 * scsSsb / scsPdcch), and n_CRB_SSB needs update w.r.t to offset
            if offset <= 0, min bw = self.coreset0NumRbs - offset, and don't have to update n_CRB_SSB
            '''
            if self.coreset0Offset > 0:
                minBw = max(self.coreset0NumRbs, self.coreset0Offset + 20 * int(self.nrSsbScsComb.currentText()[:-3]) / int(self.nrCarrierScsComb.currentText()[:-3]))
            else:
                minBw = self.coreset0NumRbs - self.coreset0Offset
            
            if int(self.nrCarrierNumRbEdit.text()) < minBw:
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid CORESET0 setting: CORESET0 numRBs=%d, offset=%d, minBw = %d, while carrier numRBs=%s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.coreset0NumRbs, self.coreset0Offset, minBw, self.nrCarrierNumRbEdit.text()))
                return False
        
        #when validation passed
        return True
    
    def validateSearchSpaceZero(self):
        self.ngwin.logEdit.append('-->inside validateSearchSpaceZero')
        if not self.nrMibCss0Edit.text():
            return False
        
        if not self.flagCoreset0:
            self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid CORESET0 setting!' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            return False
        
        if self.coreset0MultiplexingPat == '1':
            if self.freqRange == 'FR1':
                return True
        
            if self.freqRange == 'FR2' and int(self.nrMibCss0Edit.text()) in range(14):
                return True
            else:
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid CSS0 setting: searchSpaceZero can be [0, 13] for CORESET0/CSS0 with multiplexing pattern 1 and FR2!' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                return False
        else:   #self.coreset0MultiplexingPat = '2' or '3'
            if int(self.nrMibCss0Edit.text()) == 0:
                return True
            else:
                self.ngwin.logEdit.append('[%s]<font color=red>ERROR</font>: Invalid CSS0 setting: searchSpaceZero can be [0] for CORESET0/CSS0 with multiplexing pattern 2/3!' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                return False
    
    def onMibCoreset0EditEditingFinished(self):
        self.ngwin.logEdit.append('-->inside onMibCoreset0EditEditingFinished')
        #(1) validate CORESET0 and update n_CRB_SSB when necessary
        self.flagCoreset0 = self.validateCoreset0()
        if self.flagCoreset0:
            self.updateKSsbAndNCrbSsb(offset=0 if self.coreset0Offset <= 0 else self.coreset0Offset)
                
    def onSsbKssbEditEditingFinished(self):
        self.ngwin.logEdit.append('-->inside onSsbKssbEditEditingFinished')
        #(1) validate CORESET0 and update n_CRB_SSB when necessary
        self.flagCoreset0 = self.validateCoreset0()
        if self.flagCoreset0:
            self.updateKSsbAndNCrbSsb(offset=0 if self.coreset0Offset <= 0 else self.coreset0Offset)

    def onOkBtnClicked(self):
        self.ngwin.logEdit.append('-->inside onOkBtnClicked')
        #TODO
        self.accept()
