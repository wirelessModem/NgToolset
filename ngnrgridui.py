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
import math
from collections import OrderedDict
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QTabWidget, QWidget, QScrollArea
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QColor, QIntValidator, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp

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

        self.nrCarrierScsLabel = QLabel('subcarrierSpacingg:')
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
        
        #---->(1.3) MIB configurations
        self.nrMibSfnLabel = QLabel('SFN[0-1023]:')
        self.nrMibSfnEdit = QLineEdit('0')
        self.nrMibSfnEdit.setValidator(QIntValidator(0, 1023))
        
        self.nrMibDmRsTypeAPosLabel = QLabel('dmrs-TypeA-Position:')
        self.nrMibDmRsTypeAPosComb = QComboBox()
        self.nrMibDmRsTypeAPosComb.addItems(['pos2', 'pos3'])
        self.nrMibDmRsTypeAPosComb.setCurrentIndex(0)
        
        self.nrMibScsCommonLabel = QLabel('subCarrierSpacingCommon:')
        self.nrMibScsCommonComb = QComboBox()
        
        self.nrMibCoreset0Label = QLabel('coresetZero(PDCCH-ConfigSIB1)[0-15]:')
        self.nrMibCoreset0Edit = QLineEdit('0')
        self.nrMibCoreset0Edit.setValidator(QIntValidator(0, 15))
        
        self.nrMibCoreset0InfoLabel = QLabel()
        
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
        mibGrpBoxLayout.addWidget(self.nrMibCoreset0InfoLabel, 4, 0, 1, 2)
        mibGrpBoxLayout.addWidget(self.nrMibCss0Label, 5, 0)
        mibGrpBoxLayout.addWidget(self.nrMibCss0Edit, 5, 1)
        mibGrpBox.setLayout(mibGrpBoxLayout)
        
        #---->(1.4) SSB burst configurations
        self.nrSsbInOneGrpLabel = QLabel('inOneGroup(ssb-PositionsInBurst):')
        self.nrSsbInOneGrpEdit = QLineEdit()
        self.nrSsbInOneGrpEdit.setValidator(QRegExpValidator(QRegExp('[0-1]{8}')))
        self.nrSsbInOneGrpEdit.setPlaceholderText('11111111')
        
        self.nrSsbGrpPresenceLabel = QLabel('groupPresence(ssb-PositionsInBurst):')
        self.nrSsbGrpPresenceEdit = QLineEdit()
        self.nrSsbGrpPresenceEdit.setValidator(QRegExpValidator(QRegExp('[0-1]{8}')))
        self.nrSsbGrpPresenceEdit.setPlaceholderText('11111111')
        
        self.nrSsbPeriodicityLabel = QLabel('ssb-PeriodicityServingCell:')
        self.nrSsbPeriodicityComb = QComboBox()
        self.nrSsbPeriodicityComb.addItems(['5ms', '10ms', '20ms', '40ms', '80ms', '160ms'])
        #refer to 3GPP 38.213 4.1
        #For initial cell selection, a UE may assume that half frames with SS/PBCH blocks occur with a periodicity of 2 frames.
        self.nrSsbPeriodicityComb.setCurrentIndex(2)    #default to 20ms
        
        ssbBurstGrpBox = QGroupBox()
        ssbBurstGrpBox.setTitle('SSB Burst(ServingCellConfigCommonSIB)')
        ssbBurstGrpBoxLayout = QGridLayout()
        ssbBurstGrpBoxLayout.addWidget(self.nrSsbInOneGrpLabel, 0, 0)
        ssbBurstGrpBoxLayout.addWidget(self.nrSsbInOneGrpEdit, 0, 1)
        ssbBurstGrpBoxLayout.addWidget(self.nrSsbGrpPresenceLabel, 1, 0)
        ssbBurstGrpBoxLayout.addWidget(self.nrSsbGrpPresenceEdit, 1, 1)
        ssbBurstGrpBoxLayout.addWidget(self.nrSsbPeriodicityLabel, 2, 0)
        ssbBurstGrpBoxLayout.addWidget(self.nrSsbPeriodicityComb, 2, 1)
        ssbBurstGrpBox.setLayout(ssbBurstGrpBoxLayout)

        gridLayoutResGridCfg = QGridLayout()
        gridLayoutResGridCfg.addWidget(self.nrCarrierBandLabel, 0, 0)
        gridLayoutResGridCfg.addWidget(self.nrCarrierBandComb, 0, 1)
        gridLayoutResGridCfg.addWidget(self.nrCarrierBandInfoLabel, 1, 0, 1, 2)
        gridLayoutResGridCfg.addWidget(ssbGridGrpBox, 2, 0, 1, 2)
        gridLayoutResGridCfg.addWidget(ssbBurstGrpBox, 3, 0, 1, 2)
        gridLayoutResGridCfg.addWidget(mibGrpBox, 4, 0, 1, 2)
        gridLayoutResGridCfg.addWidget(carrierGridGrpBox, 5, 0, 1, 2)

        gridCfgWidget = QWidget()
        gridCfgLayout = QVBoxLayout()
        gridCfgLayout.addLayout(gridLayoutResGridCfg)
        gridCfgLayout.addStretch()
        gridCfgWidget.setLayout(gridCfgLayout)
        
        #-->(2) Common settings tab
        #---->(2.1) PCI
        self.nrSsbPciLabel = QLabel('PCI[0-1007]:')
        self.nrSsbPciEdit = QLineEdit('0')
        self.nrSsbPciEdit.setValidator(QIntValidator(0, 1007))
        
        self.nrUeAntPortsLabel = QLabel('UE antenna ports:')
        self.nrUeAntPortsComb = QComboBox()
        self.nrUeAntPortsComb.addItems(['1Tx', '2Tx', '4Tx'])
        self.nrUeAntPortsComb.setCurrentIndex(2)
        
        #---->(2.2) TDD UL/DL Configurations
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
        tddCfgGrpBoxLayout.addStretch()
        tddCfgGrpBox.setLayout(tddCfgGrpBoxLayout)
        
        pciLayout = QHBoxLayout()
        pciLayout.addWidget(self.nrSsbPciLabel)
        pciLayout.addWidget(self.nrSsbPciEdit)
        pciLayout.addStretch()
        
        ueApLayout = QHBoxLayout()
        ueApLayout.addWidget(self.nrUeAntPortsLabel)
        ueApLayout.addWidget(self.nrUeAntPortsComb)
        ueApLayout.addStretch()
        
        pciGridLayout = QGridLayout()
        pciGridLayout.addWidget(self.nrSsbPciLabel, 0, 0)
        pciGridLayout.addWidget(self.nrSsbPciEdit, 0, 1)
        pciGridLayout.addWidget(self.nrUeAntPortsLabel, 1, 0)
        pciGridLayout.addWidget(self.nrUeAntPortsComb, 1, 1)
        
        commonCfgWidget = QWidget()
        commonCfgLayout = QVBoxLayout()
        commonCfgLayout.addLayout(pciGridLayout)
        commonCfgLayout.addWidget(tddCfgGrpBox)
        commonCfgLayout.addStretch()
        commonCfgWidget.setLayout(commonCfgLayout)
        
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
        self.nrCoreset1FreqResourcesEdit.setValidator(QRegExpValidator(QRegExp('([0-1]{8},){5}[0-1]{5}')))
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
        self.nrCoreset1RegBundleSizeComb.addItems(['n2', 'n6'])
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
        self.nrUssPeriodicityComb.setCurrentIndex(0)
        
        self.nrUssSlotOffsetLabel = QLabel('monitoringSlotOffset[0]:')
        self.nrUssSlotOffsetEdit = QLineEdit('0')
        
        self.nrUssDurationLabel = QLabel('duration[1]:')
        self.nrUssDurationEdit = QLineEdit('1')
        
        self.nrUssFirstSymbsLabel = QLabel('monitoringSymbolsWithinSlot:')
        self.nrUssFirstSymbsEdit = QLineEdit('1010101,0101010')
        self.nrUssFirstSymbsEdit.setValidator(QRegExpValidator(QRegExp('[0-1]{7},[0-1]{7}')))
        
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
        self.nrDci10Sib1TimeAllocFieldEdit.setValidator(QIntValidator(0, 15))
        
        self.nrDci10Sib1TimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrDci10Sib1TimeAllocMappingTypeComb = QComboBox()
        self.nrDci10Sib1TimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        self.nrDci10Sib1TimeAllocMappingTypeComb.setEnabled(False)
        
        self.nrDci10Sib1TimeAllocK0Label = QLabel('K0:')
        self.nrDci10Sib1TimeAllocK0Edit = QLineEdit()
        self.nrDci10Sib1TimeAllocK0Edit.setEnabled(False)
        
        self.nrDci10Sib1TimeAllocSlivLabel = QLabel('SLIV:')
        self.nrDci10Sib1TimeAllocSlivEdit = QLineEdit()
        self.nrDci10Sib1TimeAllocSlivEdit.setEnabled(False)
        
        self.nrDci10Sib1TimeAllocSLabel = QLabel('S(of SLIV):')
        self.nrDci10Sib1TimeAllocSEdit = QLineEdit()
        self.nrDci10Sib1TimeAllocSEdit.setEnabled(False)
        
        self.nrDci10Sib1TimeAllocLLabel = QLabel('L(of SLIV):')
        self.nrDci10Sib1TimeAllocLEdit = QLineEdit()
        self.nrDci10Sib1TimeAllocLEdit.setEnabled(False)
        
        self.nrDci10Sib1FreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrDci10Sib1FreqAllocTypeComb = QComboBox()
        self.nrDci10Sib1FreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrDci10Sib1FreqAllocTypeComb.setCurrentIndex(1)
        self.nrDci10Sib1FreqAllocTypeComb.setEnabled(False)
        
        self.nrDci10Sib1FreqAllocFieldLabel = QLabel('Freq domain resource assignment:')
        self.nrDci10Sib1FreqAllocFieldEdit = QLineEdit()
        self.nrDci10Sib1FreqAllocFieldEdit.setEnabled(False)
        
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
        self.nrDci10Sib1FreqAllocType1BundleSizeComb.setEnabled(False)
        
        self.nrDci10Sib1Cw0McsLabel = QLabel('Modulation and coding scheme(CW0)[0-9]:')
        self.nrDci10Sib1Cw0McsEdit = QLineEdit()
        self.nrDci10Sib1Cw0McsEdit.setValidator(QIntValidator(0, 9))
        
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
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1Cw0McsLabel, 4, 0)
        dci10Sib1GridLayout.addWidget(self.nrDci10Sib1Cw0McsEdit, 4, 1)
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
        self.nrDci10Msg2TimeAllocFieldEdit.setValidator(QIntValidator(0, 15))
        
        self.nrDci10Msg2TimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrDci10Msg2TimeAllocMappingTypeComb = QComboBox()
        self.nrDci10Msg2TimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        self.nrDci10Msg2TimeAllocMappingTypeComb.setEnabled(False)
        
        self.nrDci10Msg2TimeAllocK0Label = QLabel('K0:')
        self.nrDci10Msg2TimeAllocK0Edit = QLineEdit()
        self.nrDci10Msg2TimeAllocK0Edit.setEnabled(False)
        
        self.nrDci10Msg2TimeAllocSlivLabel = QLabel('SLIV:')
        self.nrDci10Msg2TimeAllocSlivEdit = QLineEdit()
        self.nrDci10Msg2TimeAllocSlivEdit.setEnabled(False)
        
        self.nrDci10Msg2TimeAllocSLabel = QLabel('S(of SLIV):')
        self.nrDci10Msg2TimeAllocSEdit = QLineEdit()
        self.nrDci10Msg2TimeAllocSEdit.setEnabled(False)
        
        self.nrDci10Msg2TimeAllocLLabel = QLabel('L(of SLIV):')
        self.nrDci10Msg2TimeAllocLEdit = QLineEdit()
        self.nrDci10Msg2TimeAllocLEdit.setEnabled(False)
        
        self.nrDci10Msg2FreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrDci10Msg2FreqAllocTypeComb = QComboBox()
        self.nrDci10Msg2FreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrDci10Msg2FreqAllocTypeComb.setCurrentIndex(1)
        self.nrDci10Msg2FreqAllocTypeComb.setEnabled(False)
        
        self.nrDci10Msg2FreqAllocFieldLabel = QLabel('Freq domain resource assignment:')
        self.nrDci10Msg2FreqAllocFieldEdit = QLineEdit()
        self.nrDci10Msg2FreqAllocFieldEdit.setEnabled(False)
        
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
        self.nrDci10Msg2FreqAllocType1BundleSizeComb.setEnabled(False)
        
        self.nrDci10Msg2Cw0McsLabel = QLabel('Modulation and coding scheme(CW0)[0-9]:')
        self.nrDci10Msg2Cw0McsEdit = QLineEdit()
        self.nrDci10Msg2Cw0McsEdit.setValidator(QIntValidator(0, 9))
        
        self.nrDci10Msg2TbScalingLabel = QLabel('TB Scaling[0-2]:')
        self.nrDci10Msg2TbScalingEdit = QLineEdit('0')
        self.nrDci10Msg2TbScalingEdit.setValidator(QIntValidator(0, 2))
        
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
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2Cw0McsLabel, 4, 0)
        dci10Msg2GridLayout.addWidget(self.nrDci10Msg2Cw0McsEdit, 4, 1)
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
        self.nrDci10Msg4TimeAllocFieldEdit.setValidator(QIntValidator(0, 15))
        
        self.nrDci10Msg4TimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrDci10Msg4TimeAllocMappingTypeComb = QComboBox()
        self.nrDci10Msg4TimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        self.nrDci10Msg4TimeAllocMappingTypeComb.setEnabled(False)
        
        self.nrDci10Msg4TimeAllocK0Label = QLabel('K0:')
        self.nrDci10Msg4TimeAllocK0Edit = QLineEdit()
        self.nrDci10Msg4TimeAllocK0Edit.setEnabled(False)
        
        self.nrDci10Msg4TimeAllocSlivLabel = QLabel('SLIV:')
        self.nrDci10Msg4TimeAllocSlivEdit = QLineEdit()
        self.nrDci10Msg4TimeAllocSlivEdit.setEnabled(False)
        
        self.nrDci10Msg4TimeAllocSLabel = QLabel('S(of SLIV):')
        self.nrDci10Msg4TimeAllocSEdit = QLineEdit()
        self.nrDci10Msg4TimeAllocSEdit.setEnabled(False)
        
        self.nrDci10Msg4TimeAllocLLabel = QLabel('L(of SLIV):')
        self.nrDci10Msg4TimeAllocLEdit = QLineEdit()
        self.nrDci10Msg4TimeAllocLEdit.setEnabled(False)
        
        self.nrDci10Msg4FreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrDci10Msg4FreqAllocTypeComb = QComboBox()
        self.nrDci10Msg4FreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrDci10Msg4FreqAllocTypeComb.setCurrentIndex(1)
        self.nrDci10Msg4FreqAllocTypeComb.setEnabled(False)
        
        self.nrDci10Msg4FreqAllocFieldLabel = QLabel('Freq domain resource assignment:')
        self.nrDci10Msg4FreqAllocFieldEdit = QLineEdit()
        self.nrDci10Msg4FreqAllocFieldEdit.setEnabled(False)
        
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
        self.nrDci10Msg4FreqAllocType1BundleSizeComb.setEnabled(False)
        
        self.nrDci10Msg4Cw0McsLabel = QLabel('Modulation and coding scheme(CW0)[0-31]:')
        self.nrDci10Msg4Cw0McsEdit = QLineEdit()
        self.nrDci10Msg4Cw0McsEdit.setValidator(QIntValidator(0, 31))
        
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
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4Cw0McsLabel, 4, 0)
        dci10Msg4GridLayout.addWidget(self.nrDci10Msg4Cw0McsEdit, 4, 1)
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
        self.nrDci11PdschActBwpEdit = QLineEdit('1')
        self.nrDci11PdschActBwpEdit.setEnabled(False)
        
        self.nrDci11PdschIndicatedBwpLabel = QLabel('Bandwidth part indicator[0-1]:')
        self.nrDci11PdschIndicatedBwpEdit = QLineEdit('1')
        self.nrDci11PdschIndicatedBwpEdit.setEnabled(False)
        
        self.nrDci11PdschTimeAllocFieldLabel = QLabel('Time domain resource assignment[0-15,16]:')
        self.nrDci11PdschTimeAllocFieldEdit = QLineEdit('16')
        self.nrDci11PdschTimeAllocFieldEdit.setValidator(QIntValidator(0, 16))
        
        self.nrDci11PdschTimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrDci11PdschTimeAllocMappingTypeComb = QComboBox()
        self.nrDci11PdschTimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        
        self.nrDci11PdschTimeAllocK0Label = QLabel('K0[0-32]:')
        self.nrDci11PdschTimeAllocK0Edit = QLineEdit('0')
        self.nrDci11PdschTimeAllocK0Edit.setValidator(QIntValidator(0, 32))
        
        self.nrDci11PdschTimeAllocSlivLabel = QLabel('SLIV[0-127]:')
        self.nrDci11PdschTimeAllocSlivEdit = QLineEdit('28')
        self.nrDci11PdschTimeAllocSlivEdit.setValidator(QIntValidator(0, 127))
        
        self.nrDci11PdschTimeAllocSLabel = QLabel('S(of SLIV)[0-3]:')
        self.nrDci11PdschTimeAllocSEdit = QLineEdit('0')
        self.nrDci11PdschTimeAllocSEdit.setValidator(QIntValidator(0, 3))
        
        self.nrDci11PdschTimeAllocLLabel = QLabel('L(of SLIV)[3-14]:')
        self.nrDci11PdschTimeAllocLEdit = QLineEdit('3')
        self.nrDci11PdschTimeAllocLEdit.setValidator(QIntValidator(3, 14))
        
        self.nrDci11PdschFreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrDci11PdschFreqAllocTypeComb = QComboBox()
        self.nrDci11PdschFreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrDci11PdschFreqAllocTypeComb.setCurrentIndex(1)
        
        self.nrDci11PdschFreqAllocFieldLabel = QLabel('Freq domain resource assignment:')
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
        self.nrDci11PdschCw1McsEdit.setEnabled(False)
        
        self.nrDci11PdschTbsLabel = QLabel('Transport block size(bits):')
        self.nrDci11PdschTbsEdit = QLineEdit()
        self.nrDci11PdschTbsEdit.setEnabled(False)
        
        self.nrDci11PdschDeltaPriLabel = QLabel('PUCCH resource indicator[0-7]:')
        self.nrDci11PdschDeltaPriEdit = QLineEdit()
        self.nrDci11PdschDeltaPriEdit.setValidator(QIntValidator(0, 7))
        
        self.nrDci11PdschK1Label = QLabel('K1(PDSCH-to-HARQ_feedback timing indicator)[0-7]:')
        self.nrDci11PdschK1Edit = QLineEdit()
        self.nrDci11PdschK1Edit.setValidator(QIntValidator(0, 7))
        
        self.nrDci11PdschAntPortsFieldLabel = QLabel('Antenna port(s)[0-15]:')
        self.nrDci11PdschAntPortsFieldEdit = QLineEdit()
        self.nrDci11PdschAntPortsFieldEdit.setValidator(QIntValidator(0, 15))
        
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
        self.nrDci01PuschActBwpEdit = QLineEdit('1')
        self.nrDci01PuschActBwpEdit.setEnabled(False)
        
        self.nrDci01PuschIndicatedBwpLabel = QLabel('Bandwidth part indicator[0-1]:')
        self.nrDci01PuschIndicatedBwpEdit = QLineEdit('1')
        self.nrDci01PuschIndicatedBwpEdit.setEnabled(False)
        
        self.nrDci01PuschTimeAllocFieldLabel = QLabel('Time domain resource assignment[0-15,16]:')
        self.nrDci01PuschTimeAllocFieldEdit = QLineEdit('16')
        self.nrDci01PuschTimeAllocFieldEdit.setValidator(QIntValidator(0, 16))
        
        self.nrDci01PuschTimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrDci01PuschTimeAllocMappingTypeComb = QComboBox()
        self.nrDci01PuschTimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        
        self.nrDci01PuschTimeAllocK2Label = QLabel('K2[0-32]:')
        self.nrDci01PuschTimeAllocK2Edit = QLineEdit('1')
        self.nrDci01PuschTimeAllocK2Edit.setValidator(QIntValidator(0, 32))
        
        self.nrDci01PuschTimeAllocSlivLabel = QLabel('SLIV[0-127]:')
        self.nrDci01PuschTimeAllocSlivEdit = QLineEdit('27')
        self.nrDci01PuschTimeAllocSlivEdit.setValidator(QIntValidator(0, 127))
        
        self.nrDci01PuschTimeAllocSLabel = QLabel('S(of SLIV)[0]:')
        self.nrDci01PuschTimeAllocSEdit = QLineEdit('0')
        self.nrDci01PuschTimeAllocSEdit.setValidator(QIntValidator(0, 0))
        
        self.nrDci01PuschTimeAllocLLabel = QLabel('L(of SLIV)[4-14]:')
        self.nrDci01PuschTimeAllocLEdit = QLineEdit('14')
        self.nrDci01PuschTimeAllocLEdit.setValidator(QIntValidator(4, 14))
        
        self.nrDci01PuschFreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrDci01PuschFreqAllocTypeComb = QComboBox()
        self.nrDci01PuschFreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrDci01PuschFreqAllocTypeComb.setCurrentIndex(1)
        
        self.nrDci01PuschFreqAllocFreqHopLabel= QLabel('Frequency hopping flag:')
        self.nrDci01PuschFreqAllocFreqHopComb = QComboBox()
        self.nrDci01PuschFreqAllocFreqHopComb.addItems(['disabled', 'intra-slot', 'inter-slot'])
        self.nrDci01PuschFreqAllocFreqHopComb.setCurrentIndex(0)
        
        self.nrDci01PuschFreqAllocFieldLabel = QLabel('Freq domain resource assignment:')
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
        
        self.nrDci01PuschPrecodingLayersFieldLabel = QLabel('Precoding info and num of layers[0-63]:')
        self.nrDci01PuschPrecodingLayersFieldEdit = QLineEdit()
        self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(QIntValidator(0, 63))
        
        self.nrDci01PuschSriFieldLabel = QLabel('SRS resource indicator:')
        self.nrDci01PuschSriFieldEdit = QLineEdit()
        self.nrDci01PuschSriFieldEdit.setEnabled(False)
        
        self.nrDci01PuschAntPortsFieldLabel = QLabel('Antenna port(s)[0-7]:')
        self.nrDci01PuschAntPortsFieldEdit = QLineEdit()
        
        self.nrDci01PuschPtrsDmrsMappingLabel = QLabel('PTRS-DMRS association[0-3]:')
        self.nrDci01PuschPtrsDmrsMappingEdit = QLineEdit()
        self.nrDci01PuschPtrsDmrsMappingEdit.setValidator(QIntValidator(0, 3))
        self.nrDci01PuschPtrsDmrsMappingEdit.setEnabled(False)
        
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
        dci01PuschGridLayout.addWidget(self.nrDci01PuschPrecodingLayersFieldLabel, 8, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschPrecodingLayersFieldEdit, 8, 1)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschSriFieldLabel, 9, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschSriFieldEdit, 9, 1)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschAntPortsFieldLabel, 10, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschAntPortsFieldEdit, 10, 1)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschPtrsDmrsMappingLabel, 11, 0)
        dci01PuschGridLayout.addWidget(self.nrDci01PuschPtrsDmrsMappingEdit, 11, 1)
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
        self.nrMsg3PuschTimeAllocFieldEdit.setValidator(QIntValidator(0, 15))
        
        self.nrMsg3PuschTimeAllocMappingTypeLabel = QLabel('Mapping type:')
        self.nrMsg3PuschTimeAllocMappingTypeComb = QComboBox()
        self.nrMsg3PuschTimeAllocMappingTypeComb.addItems(['Type A', 'Type B'])
        self.nrMsg3PuschTimeAllocMappingTypeComb.setEnabled(False)
        
        self.nrMsg3PuschTimeAllocK2Label = QLabel('K2:')
        self.nrMsg3PuschTimeAllocK2Edit = QLineEdit()
        self.nrMsg3PuschTimeAllocK2Edit.setEnabled(False)
        
        self.nrMsg3PuschTimeAllocDeltaLabel= QLabel('Delta:')
        self.nrMsg3PuschTimeAllocDeltaEdit = QLineEdit()
        self.nrMsg3PuschTimeAllocDeltaEdit.setEnabled(False)
        
        self.nrMsg3PuschTimeAllocSlivLabel = QLabel('SLIV:')
        self.nrMsg3PuschTimeAllocSlivEdit = QLineEdit()
        self.nrMsg3PuschTimeAllocSlivEdit.setEnabled(False)
        
        self.nrMsg3PuschTimeAllocSLabel = QLabel('S(of SLIV):')
        self.nrMsg3PuschTimeAllocSEdit = QLineEdit()
        self.nrMsg3PuschTimeAllocSEdit.setEnabled(False)
        
        self.nrMsg3PuschTimeAllocLLabel = QLabel('L(of SLIV):')
        self.nrMsg3PuschTimeAllocLEdit = QLineEdit()
        self.nrMsg3PuschTimeAllocLEdit.setEnabled(False)
        
        self.nrMsg3PuschFreqAllocTypeLabel = QLabel('resourceAllocation:')
        self.nrMsg3PuschFreqAllocTypeComb = QComboBox()
        self.nrMsg3PuschFreqAllocTypeComb.addItems(['RA Type0', 'RA Type1'])
        self.nrMsg3PuschFreqAllocTypeComb.setCurrentIndex(1)
        self.nrMsg3PuschFreqAllocTypeComb.setEnabled(False)
        
        self.nrMsg3PuschFreqAllocFreqHopLabel= QLabel('Frequency hopping flag:')
        self.nrMsg3PuschFreqAllocFreqHopComb = QComboBox()
        self.nrMsg3PuschFreqAllocFreqHopComb.addItems(['disabled', 'enabled'])
        self.nrMsg3PuschFreqAllocFreqHopComb.setCurrentIndex(0)
        
        self.nrMsg3PuschFreqAllocFieldLabel = QLabel('Freq domain resource assignment:')
        self.nrMsg3PuschFreqAllocFieldEdit = QLineEdit()
        
        self.nrMsg3PuschFreqAllocType1RbStartLabel = QLabel('RB_start(of RIV):')
        self.nrMsg3PuschFreqAllocType1RbStartEdit = QLineEdit()
        
        self.nrMsg3PuschFreqAllocType1LRbsLabel = QLabel('L_RBs(of RIV):')
        self.nrMsg3PuschFreqAllocType1LRbsEdit = QLineEdit()
        
        self.nrMsg3PuschFreqAllocType1SecondHopFreqOffLabel = QLabel('Frequency offset for 2nd hop:')
        self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit = QLineEdit()
        self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit.setEnabled(False)
        
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
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocType1SecondHopFreqOffLabel, 5, 0)
        msg3PuschFreqAllocLayout.addWidget(self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit, 5, 1)
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
        self.nrDmrsSib1DmrsTypeComb.setEnabled(False)
        
        self.nrDmrsSib1AddPosLabel = QLabel('dmrs-additionalPosition:')
        self.nrDmrsSib1AddPosComb = QComboBox()
        self.nrDmrsSib1AddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        self.nrDmrsSib1AddPosComb.setEnabled(False)
        
        self.nrDmrsSib1MaxLengthLabel = QLabel('maxLength:')
        self.nrDmrsSib1MaxLengthComb = QComboBox()
        self.nrDmrsSib1MaxLengthComb.addItems(['len1', 'len2'])
        self.nrDmrsSib1MaxLengthComb.setCurrentIndex(0)
        self.nrDmrsSib1MaxLengthComb.setEnabled(False)
        
        self.nrDmrsSib1DmrsPortsLabel = QLabel('DMRS port(s)[1000+x]:')
        self.nrDmrsSib1DmrsPortsEdit = QLineEdit('0')
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
        self.nrDmrsMsg2DmrsTypeComb.setEnabled(False)
        
        self.nrDmrsMsg2AddPosLabel = QLabel('dmrs-additionalPosition:')
        self.nrDmrsMsg2AddPosComb = QComboBox()
        self.nrDmrsMsg2AddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        self.nrDmrsMsg2AddPosComb.setEnabled(False)
        
        self.nrDmrsMsg2MaxLengthLabel = QLabel('maxLength:')
        self.nrDmrsMsg2MaxLengthComb = QComboBox()
        self.nrDmrsMsg2MaxLengthComb.addItems(['len1', 'len2'])
        self.nrDmrsMsg2MaxLengthComb.setCurrentIndex(0)
        self.nrDmrsMsg2MaxLengthComb.setEnabled(False)
        
        self.nrDmrsMsg2DmrsPortsLabel = QLabel('DMRS port(s)[1000+x]:')
        self.nrDmrsMsg2DmrsPortsEdit = QLineEdit('0')
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
        self.nrDmrsMsg4DmrsTypeComb.setEnabled(False)
        
        self.nrDmrsMsg4AddPosLabel = QLabel('dmrs-additionalPosition:')
        self.nrDmrsMsg4AddPosComb = QComboBox()
        self.nrDmrsMsg4AddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        self.nrDmrsMsg4AddPosComb.setEnabled(False)
        
        self.nrDmrsMsg4MaxLengthLabel = QLabel('maxLength:')
        self.nrDmrsMsg4MaxLengthComb = QComboBox()
        self.nrDmrsMsg4MaxLengthComb.addItems(['len1', 'len2'])
        self.nrDmrsMsg4MaxLengthComb.setCurrentIndex(0)
        self.nrDmrsMsg4MaxLengthComb.setEnabled(False)
        
        self.nrDmrsMsg4DmrsPortsLabel = QLabel('DMRS port(s)[1000+x]:')
        self.nrDmrsMsg4DmrsPortsEdit = QLineEdit('0')
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
        self.nrIniDlBwpGenericBwpIdEdit = QLineEdit('0')
        self.nrIniDlBwpGenericBwpIdEdit.setEnabled(False)
        
        self.nrIniDlBwpGenericScsLabel = QLabel('subcarrierSpacing:')
        self.nrIniDlBwpGenericScsComb = QComboBox()
        self.nrIniDlBwpGenericScsComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        self.nrIniDlBwpGenericScsComb.setEnabled(False)
        
        self.nrIniDlBwpGenericCpLabel = QLabel('cyclicPrefix:')
        self.nrIniDlBwpGenericCpComb = QComboBox()
        self.nrIniDlBwpGenericCpComb.addItems(['normal', 'extended'])
        self.nrIniDlBwpGenericCpComb.setCurrentIndex(0)
        
        self.nrIniDlBwpGenericLocAndBwLabel = QLabel('locationAndBandwidth[0-37949]:')
        self.nrIniDlBwpGenericLocAndBwEdit = QLineEdit('0')
        self.nrIniDlBwpGenericLocAndBwEdit.setValidator(QIntValidator(0, 37949))
        
        self.nrIniDlBwpGenericRbStartLabel = QLabel('RB_start:')
        self.nrIniDlBwpGenericRbStartEdit = QLineEdit('0')
        
        self.nrIniDlBwpGenericLRbsLabel = QLabel('L_RBs:')
        self.nrIniDlBwpGenericLRbsEdit = QLineEdit()
        
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
        self.nrIniUlBwpGenericBwpIdEdit = QLineEdit('0')
        self.nrIniUlBwpGenericBwpIdEdit.setEnabled(False)
        
        self.nrIniUlBwpGenericScsLabel = QLabel('subcarrierSpacing:')
        self.nrIniUlBwpGenericScsComb = QComboBox()
        self.nrIniUlBwpGenericScsComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        self.nrIniUlBwpGenericScsComb.setEnabled(False)
        
        self.nrIniUlBwpGenericCpLabel = QLabel('cyclicPrefix:')
        self.nrIniUlBwpGenericCpComb = QComboBox()
        self.nrIniUlBwpGenericCpComb.addItems(['normal', 'extended'])
        self.nrIniUlBwpGenericCpComb.setCurrentIndex(0)
        
        self.nrIniUlBwpGenericLocAndBwLabel = QLabel('locationAndBandwidth[0-37949]:')
        self.nrIniUlBwpGenericLocAndBwEdit = QLineEdit('0')
        self.nrIniUlBwpGenericLocAndBwEdit.setValidator(QIntValidator(0, 37949))
        
        self.nrIniUlBwpGenericRbStartLabel = QLabel('RB_start:')
        self.nrIniUlBwpGenericRbStartEdit = QLineEdit('0')
        
        self.nrIniUlBwpGenericLRbsLabel = QLabel('L_RBs:')
        self.nrIniUlBwpGenericLRbsEdit = QLineEdit()
        
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
        self.nrRachGenericPrachConfIdEdit = QLineEdit('0')
        self.nrRachGenericPrachConfIdEdit.setValidator(QIntValidator(0, 255))
        
        self.nrRachGenericPrachFmtLabel = QLabel('Preamble format:')
        self.nrRachGenericPrachFmtEdit = QLineEdit()
        self.nrRachGenericPrachFmtEdit.setEnabled(False)
        
        self.nrRachGenericScsLabel = QLabel('msg1-SubcarrierSpacing:')
        self.nrRachGenericScsComb = QComboBox()
        self.nrRachGenericScsComb.addItems(['1.25KHz', '5KHz', '15KHz', '30KHz', '60KHz', '120KHz'])
        
        self.nrRachGenericMsg1FdmLabel = QLabel('msg1-FDM:')
        self.nrRachGenericMsg1FdmComb = QComboBox()
        self.nrRachGenericMsg1FdmComb.addItems(['1', '2', '4', '8'])
        
        self.nrRachGenericMsg1FreqStartLabel = QLabel('msg1-FrequencyStart[0-274]:')
        self.nrRachGenericMsg1FreqStartEdit = QLineEdit('0')
        self.nrRachGenericMsg1FreqStartEdit.setValidator(QIntValidator(0, 274))
        
        rachGenericGrpBox = QGroupBox()
        rachGenericGrpBox.setTitle('RACH-ConfigGeneric')
        rachGenericGrpBoxGridLayout = QGridLayout()
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericPrachConfIdLabel, 0, 0)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericPrachConfIdEdit, 0, 1)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericPrachFmtLabel, 1, 0)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericPrachFmtEdit, 1, 1)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericScsLabel, 2, 0)
        rachGenericGrpBoxGridLayout.addWidget(self.nrRachGenericScsComb, 2, 1)
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
        self.nrRachSsbPerRachOccasionComb.addItems(['oneEighth', 'oneFourth', 'oneHalf', 'one', 'two', 'four', 'eight', 'sixteen'])
        self.nrRachSsbPerRachOccasionComb.setCurrentIndex(0)
        
        self.nrRachCbPreamblesPerSsbLabel = QLabel('CB-PreamblesPerSSB:')
        self.nrRachCbPreamblesPerSsbComb = QComboBox()
        self.nrRachCbPreamblesPerSsbComb.addItems([str(i) for i in self.nrSsbPerRachOccasion2CbPreamblesPerSsb['oneEighth']])
        
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
        prachWidgetGridLayout.addWidget(self.nrRachCbPreamblesPerSsbComb, 3, 1)
        prachWidgetGridLayout.addWidget(self.nrRachMsg3TpLabel, 4, 0)
        prachWidgetGridLayout.addWidget(self.nrRachMsg3TpComb, 4, 1)
        prachWidget.setLayout(prachWidgetGridLayout)
        
        #dmrs for msg3 pusch
        self.nrDmrsMsg3DmrsTypeLabel = QLabel('dmrs-Type:')
        self.nrDmrsMsg3DmrsTypeComb = QComboBox()
        self.nrDmrsMsg3DmrsTypeComb.addItems(['Type 1', 'Type 2'])
        self.nrDmrsMsg3DmrsTypeComb.setCurrentIndex(0)
        self.nrDmrsMsg3DmrsTypeComb.setEnabled(False)
        
        self.nrDmrsMsg3AddPosLabel = QLabel('dmrs-additionalPosition:')
        self.nrDmrsMsg3AddPosComb = QComboBox()
        self.nrDmrsMsg3AddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        self.nrDmrsMsg3AddPosComb.setEnabled(False)
        
        self.nrDmrsMsg3MaxLengthLabel = QLabel('maxLength:')
        self.nrDmrsMsg3MaxLengthComb = QComboBox()
        self.nrDmrsMsg3MaxLengthComb.addItems(['len1', 'len2'])
        self.nrDmrsMsg3MaxLengthComb.setCurrentIndex(0)
        self.nrDmrsMsg3MaxLengthComb.setEnabled(False)
        
        self.nrDmrsMsg3DmrsPortsLabel = QLabel('DMRS port(s)[x]:')
        self.nrDmrsMsg3DmrsPortsEdit = QLineEdit('0')
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
        self.nrPucchSib1IniCsIndexesSetEdit = QLineEdit('(0, 3)')
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
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1PrbOffsetLabel, 4, 0)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1PrbOffsetEdit, 4, 1)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1IniCsIndexesSetLabel, 5, 0)
        pucchSib1WidgetGridLayout.addWidget(self.nrPucchSib1IniCsIndexesSetEdit, 5, 1)
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
        self.nrDedDlBwpGenericBwpIdEdit = QLineEdit('1')
        self.nrDedDlBwpGenericBwpIdEdit.setEnabled(False)
        
        self.nrDedDlBwpGenericScsLabel = QLabel('subcarrierSpacing:')
        self.nrDedDlBwpGenericScsComb = QComboBox()
        self.nrDedDlBwpGenericScsComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        self.nrDedDlBwpGenericScsComb.setEnabled(False)
        
        self.nrDedDlBwpGenericCpLabel = QLabel('cyclicPrefix:')
        self.nrDedDlBwpGenericCpComb = QComboBox()
        self.nrDedDlBwpGenericCpComb.addItems(['normal', 'extended'])
        self.nrDedDlBwpGenericCpComb.setCurrentIndex(0)
        
        self.nrDedDlBwpGenericLocAndBwLabel = QLabel('locationAndBandwidth[0-37949]:')
        self.nrDedDlBwpGenericLocAndBwEdit = QLineEdit('0')
        self.nrDedDlBwpGenericLocAndBwEdit.setValidator(QIntValidator(0, 37949))
        
        self.nrDedDlBwpGenericRbStartLabel = QLabel('RB_start:')
        self.nrDedDlBwpGenericRbStartEdit = QLineEdit('0')
        
        self.nrDedDlBwpGenericLRbsLabel = QLabel('L_RBs:')
        self.nrDedDlBwpGenericLRbsEdit = QLineEdit()
        
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
        self.nrDedPdschCfgRbgSizeEdit = QLineEdit('4')
        
        self.nrDedPdschCfgMcsTableLabel = QLabel('mcs-Table:')
        self.nrDedPdschCfgMcsTableComb = QComboBox()
        self.nrDedPdschCfgMcsTableComb.addItems(['qam64', 'qam256', 'qam64LowSE'])
        self.nrDedPdschCfgMcsTableComb.setCurrentIndex(0)
        
        self.nrDedPdschCfgXOverheadLabel = QLabel('xOverhead:')
        self.nrDedPdschCfgXOverheadComb = QComboBox()
        self.nrDedPdschCfgXOverheadComb.addItems(['xOh0', 'xOh6', 'xOh12', 'xOh18'])
        self.nrDedPdschCfgXOverheadComb.setCurrentIndex(0)
        
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
        dedPdschCfgGridLayout.addWidget(self.nrDedPdschCfgXOverheadLabel, 4, 0)
        dedPdschCfgGridLayout.addWidget(self.nrDedPdschCfgXOverheadComb, 4, 1)
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
        self.nrPtrsPdschSwitchLabel = QLabel('Enable PT-RS:')
        self.nrPtrsPdschSwitchComb = QComboBox()
        self.nrPtrsPdschSwitchComb.addItems(['yes', 'no'])
        self.nrPtrsPdschSwitchComb.setCurrentIndex(1)
        self.nrPtrsPdschSwitchComb.setEnabled(False)
        
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
        self.nrDmrsDedPdschDmrsPortsEdit.setEnabled(False)
        
        self.nrDmrsDedPdschCdmGroupsWoDataLabel = QLabel('CDM group(s) without data:')
        self.nrDmrsDedPdschCdmGroupsWoDataEdit = QLineEdit()
        self.nrDmrsDedPdschCdmGroupsWoDataEdit.setEnabled(False)
        
        self.nrDmrsDedPdschFrontLoadSymbsLabel = QLabel('Number of front-load symbols:')
        self.nrDmrsDedPdschFrontLoadSymbsEdit = QLineEdit()
        self.nrDmrsDedPdschFrontLoadSymbsEdit.setEnabled(False)
        
        ptrsPdschWidget = QGroupBox()
        ptrsPdschWidget.setTitle('PT-RS for PDSCH')
        ptrsPdschWidgetGridLayout = QGridLayout()
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschSwitchLabel, 0, 0)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschSwitchComb, 0, 1)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschTimeDensityLabel, 1, 0)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschTimeDensityComb, 1, 1)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschFreqDensityLabel, 2, 0)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschFreqDensityComb, 2, 1)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschReOffsetLabel, 3, 0)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschReOffsetComb, 3, 1)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschDmrsAntPortLabel, 4, 0)
        ptrsPdschWidgetGridLayout.addWidget(self.nrPtrsPdschDmrsAntPortEdit, 4, 1)
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
        self.nrDedUlBwpGenericBwpIdEdit = QLineEdit('1')
        self.nrDedUlBwpGenericBwpIdEdit.setEnabled(False)
        
        self.nrDedUlBwpGenericScsLabel = QLabel('subcarrierSpacing:')
        self.nrDedUlBwpGenericScsComb = QComboBox()
        self.nrDedUlBwpGenericScsComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        self.nrDedUlBwpGenericScsComb.setEnabled(False)
        
        self.nrDedUlBwpGenericCpLabel = QLabel('cyclicPrefix:')
        self.nrDedUlBwpGenericCpComb = QComboBox()
        self.nrDedUlBwpGenericCpComb.addItems(['normal', 'extended'])
        self.nrDedUlBwpGenericCpComb.setCurrentIndex(0)
        
        self.nrDedUlBwpGenericLocAndBwLabel = QLabel('locationAndBandwidth[0-37949]:')
        self.nrDedUlBwpGenericLocAndBwEdit = QLineEdit('0')
        self.nrDedUlBwpGenericLocAndBwEdit.setValidator(QIntValidator(0, 37949))
        
        self.nrDedUlBwpGenericRbStartLabel = QLabel('RB_start:')
        self.nrDedUlBwpGenericRbStartEdit = QLineEdit('0')
        
        self.nrDedUlBwpGenericLRbsLabel = QLabel('L_RBs:')
        self.nrDedUlBwpGenericLRbsEdit = QLineEdit()
        
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
        self.nrDedPuschCfgCbMaxRankEdit = QLineEdit('4')
        self.nrDedPuschCfgCbMaxRankEdit.setValidator(QIntValidator(1, 4))
        
        #note: Lmax is the number of srs resources transmitted by ue, which is ue capability as defined in 38.306
        self.nrDedPuschCfgNonCbMaxLayersLabel = QLabel('non-CB maxLayers(Lmax)[1-4]:')
        self.nrDedPuschCfgNonCbMaxLayersEdit = QLineEdit('4')
        self.nrDedPuschCfgNonCbMaxLayersEdit.setValidator(QIntValidator(1, 4))
        self.nrDedPuschCfgNonCbMaxLayersEdit.setEnabled(False)
        
        self.nrDedPuschCfgFreqHopOffsetLabel = QLabel('frequencyHoppingOffset[0-274]:')
        self.nrDedPuschCfgFreqHopOffsetEdit = QLineEdit('0')
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
        self.nrDedPuschCfgMcsTableComb.addItems(['qam64', 'qam256', 'qam64LowSE'])
        self.nrDedPuschCfgMcsTableComb.setCurrentIndex(0)
        
        self.nrDedPuschCfgXOverheadLabel = QLabel('xOverhead:')
        self.nrDedPuschCfgXOverheadComb = QComboBox()
        self.nrDedPuschCfgXOverheadComb.addItems(['xOh0', 'xOh6', 'xOh12', 'xOh18'])
        self.nrDedPuschCfgXOverheadComb.setCurrentIndex(0)
        
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
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgXOverheadLabel, 10, 0)
        dedPuschCfgGridLayout.addWidget(self.nrDedPuschCfgXOverheadComb, 10, 1)
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
        
        '''
        self.nrDmrsDedPuschRankLabel = QLabel('Transmission rank:')
        self.nrDmrsDedPuschRankEdit = QLineEdit()
        self.nrDmrsDedPuschRankEdit.setEnabled(False)
        '''
        
        #start ptrs
        self.nrPtrsPuschSwitchLabel = QLabel('Enable PT-RS:')
        self.nrPtrsPuschSwitchComb = QComboBox()
        self.nrPtrsPuschSwitchComb.addItems(['yes', 'no'])
        self.nrPtrsPuschSwitchComb.setCurrentIndex(1)
        self.nrPtrsPuschSwitchComb.setEnabled(False)
        
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
        self.nrDmrsDedPuschDmrsPortsEdit.setEnabled(False)
        
        self.nrDmrsDedPuschCdmGroupsWoDataLabel = QLabel('CDM group(s) without data:')
        self.nrDmrsDedPuschCdmGroupsWoDataEdit = QLineEdit()
        self.nrDmrsDedPuschCdmGroupsWoDataEdit.setEnabled(False)
        
        self.nrDmrsDedPuschFrontLoadSymbsLabel = QLabel('Number of front-load symbols:')
        self.nrDmrsDedPuschFrontLoadSymbsEdit = QLineEdit()
        self.nrDmrsDedPuschFrontLoadSymbsEdit.setEnabled(False)
        
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
        
        ptrsPuschSwitchLayout = QHBoxLayout()
        ptrsPuschSwitchLayout.addWidget(self.nrPtrsPuschSwitchLabel)
        ptrsPuschSwitchLayout.addWidget(self.nrPtrsPuschSwitchComb)
        ptrsPuschSwitchLayout.addStretch()
        
        ptrsPuschGrpBox = QGroupBox()
        ptrsPuschGrpBox.setTitle('PT-RS for PUSCH')
        ptrsPuschGrpBoxLayout = QVBoxLayout()
        ptrsPuschGrpBoxLayout.addLayout(ptrsPuschSwitchLayout)
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
        #dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschRankLabel, 3, 0)
        #dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschRankEdit, 3, 1)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschDmrsPortsLabel, 3, 0)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschDmrsPortsEdit, 3, 1)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschCdmGroupsWoDataLabel, 4, 0)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschCdmGroupsWoDataEdit, 4, 1)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschFrontLoadSymbsLabel, 5, 0)
        dmrsDedPuschGridLayout.addWidget(self.nrDmrsDedPuschFrontLoadSymbsEdit, 5, 1)
        dmrsDedPuschGridLayout.addWidget(ptrsPuschGrpBox, 6, 0, 1, 2)
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
        self.nrSrsRes0NumAntPortsComb.addItems(['port1', 'ports2', 'ports4'])
        self.nrSrsRes0NumAntPortsComb.setCurrentIndex(0)
        
        self.nrSrsRes0NonCbPtrsPortIndLabel = QLabel('ptrs-PortIndex(non-CB):')
        self.nrSrsRes0NonCbPtrsPortIndComb = QComboBox()
        self.nrSrsRes0NonCbPtrsPortIndComb.addItems(['n0', 'n1'])
        self.nrSrsRes0NonCbPtrsPortIndComb.setCurrentIndex(0)
        
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
        srsRes0GridLayout.addWidget(self.nrSrsRes0NonCbPtrsPortIndLabel, 2, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0NonCbPtrsPortIndComb, 2, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0NumCombLabel, 3, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0NumCombComb, 3, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0CombOffsetLabel, 4, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0CombOffsetEdit, 4, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0StartPosLabel, 5, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0StartPosEdit, 5, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0NumSymbsLabel, 6, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0NumSymbsComb, 6, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0RepFactorLabel, 7, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0RepFactorComb, 7, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqPosLabel, 8, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqPosEdit, 8, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqShiftLabel, 9, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqShiftEdit, 9, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopCSrsLabel, 10, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopCSrsEdit, 10, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopBSrsLabel, 11, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopBSrsEdit, 11, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopBHopLabel, 12, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0FreqHopBHopEdit, 12, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0ResTypeLabel, 13, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0ResTypeComb, 13, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0PeriodLabel, 14, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0PeriodComb, 14, 1)
        srsRes0GridLayout.addWidget(self.nrSrsRes0OffsetLabel, 15, 0)
        srsRes0GridLayout.addWidget(self.nrSrsRes0OffsetEdit, 15, 1)
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
        self.nrSrsRes1NumAntPortsComb.addItems(['port1', 'ports2', 'ports4'])
        self.nrSrsRes1NumAntPortsComb.setCurrentIndex(0)
        
        self.nrSrsRes1NonCbPtrsPortIndLabel = QLabel('ptrs-PortIndex(non-CB):')
        self.nrSrsRes1NonCbPtrsPortIndComb = QComboBox()
        self.nrSrsRes1NonCbPtrsPortIndComb.addItems(['n0', 'n1'])
        self.nrSrsRes1NonCbPtrsPortIndComb.setCurrentIndex(0)
        
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
        srsRes1GridLayout.addWidget(self.nrSrsRes1NonCbPtrsPortIndLabel, 2, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1NonCbPtrsPortIndComb, 2, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1NumCombLabel, 3, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1NumCombComb, 3, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1CombOffsetLabel, 4, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1CombOffsetEdit, 4, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1StartPosLabel, 5, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1StartPosEdit, 5, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1NumSymbsLabel, 6, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1NumSymbsComb, 6, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1RepFactorLabel, 7, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1RepFactorComb, 7, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqPosLabel, 8, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqPosEdit, 8, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqShiftLabel, 9, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqShiftEdit, 9, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopCSrsLabel, 10, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopCSrsEdit, 10, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopBSrsLabel, 11, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopBSrsEdit, 11, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopBHopLabel, 12, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1FreqHopBHopEdit, 12, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1ResTypeLabel, 13, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1ResTypeComb, 13, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1PeriodLabel, 14, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1PeriodComb, 14, 1)
        srsRes1GridLayout.addWidget(self.nrSrsRes1OffsetLabel, 15, 0)
        srsRes1GridLayout.addWidget(self.nrSrsRes1OffsetEdit, 15, 1)
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
        self.nrSrsRes2NumAntPortsComb.addItems(['port1', 'ports2', 'ports4'])
        self.nrSrsRes2NumAntPortsComb.setCurrentIndex(0)
        
        self.nrSrsRes2NonCbPtrsPortIndLabel = QLabel('ptrs-PortIndex(non-CB):')
        self.nrSrsRes2NonCbPtrsPortIndComb = QComboBox()
        self.nrSrsRes2NonCbPtrsPortIndComb.addItems(['n0', 'n1'])
        self.nrSrsRes2NonCbPtrsPortIndComb.setCurrentIndex(0)
        
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
        srsRes2GridLayout.addWidget(self.nrSrsRes2NonCbPtrsPortIndLabel, 2, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2NonCbPtrsPortIndComb, 2, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2NumCombLabel, 3, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2NumCombComb, 3, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2CombOffsetLabel, 4, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2CombOffsetEdit, 4, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2StartPosLabel, 5, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2StartPosEdit, 5, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2NumSymbsLabel, 6, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2NumSymbsComb, 6, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2RepFactorLabel, 7, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2RepFactorComb, 7, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqPosLabel, 8, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqPosEdit, 8, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqShiftLabel, 9, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqShiftEdit, 9, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopCSrsLabel, 10, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopCSrsEdit, 10, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopBSrsLabel, 11, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopBSrsEdit, 11, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopBHopLabel, 12, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2FreqHopBHopEdit, 12, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2ResTypeLabel, 13, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2ResTypeComb, 13, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2PeriodLabel, 14, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2PeriodComb, 14, 1)
        srsRes2GridLayout.addWidget(self.nrSrsRes2OffsetLabel, 15, 0)
        srsRes2GridLayout.addWidget(self.nrSrsRes2OffsetEdit, 15, 1)
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
        self.nrSrsRes3NumAntPortsComb.addItems(['port1', 'ports2', 'ports4'])
        self.nrSrsRes3NumAntPortsComb.setCurrentIndex(0)
        
        self.nrSrsRes3NonCbPtrsPortIndLabel = QLabel('ptrs-PortIndex(non-CB):')
        self.nrSrsRes3NonCbPtrsPortIndComb = QComboBox()
        self.nrSrsRes3NonCbPtrsPortIndComb.addItems(['n0', 'n1'])
        self.nrSrsRes3NonCbPtrsPortIndComb.setCurrentIndex(0)
        
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
        srsRes3GridLayout.addWidget(self.nrSrsRes3NonCbPtrsPortIndLabel, 2, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3NonCbPtrsPortIndComb, 2, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3NumCombLabel, 3, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3NumCombComb, 3, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3CombOffsetLabel, 4, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3CombOffsetEdit, 4, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3StartPosLabel, 5, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3StartPosEdit, 5, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3NumSymbsLabel, 6, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3NumSymbsComb, 6, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3RepFactorLabel, 7, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3RepFactorComb, 7, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqPosLabel, 8, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqPosEdit, 8, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqShiftLabel, 9, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqShiftEdit, 9, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopCSrsLabel, 10, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopCSrsEdit, 10, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopBSrsLabel, 11, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopBSrsEdit, 11, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopBHopLabel, 12, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3FreqHopBHopEdit, 12, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3ResTypeLabel, 13, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3ResTypeComb, 13, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3PeriodLabel, 14, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3PeriodComb, 14, 1)
        srsRes3GridLayout.addWidget(self.nrSrsRes3OffsetLabel, 15, 0)
        srsRes3GridLayout.addWidget(self.nrSrsRes3OffsetEdit, 15, 1)
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
        
        self.nrSrsResSet0ResourceIdListLabel = QLabel('srs-ResourceIdList[max=2]:')
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
        
        self.nrSrsResSet1ResourceIdListLabel = QLabel('srs-ResourceIdList[max=4]:')
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
        self.nrCarrierBwComb.currentIndexChanged.connect(self.onCarrierBwCombCurIndChanged)
        self.nrCarrierScsComb.currentIndexChanged.connect(self.onCarrierScsCombCurIndChanged)
        self.nrCarrierBandComb.currentIndexChanged.connect(self.onCarrierBandCombCurIndChanged)
        self.nrSsbScsComb.currentIndexChanged.connect(self.onSsbScsCombCurIndChanged)
        self.nrMibScsCommonComb.currentIndexChanged.connect(self.onMibScsCommonCombCurIndChanged)
        self.nrMibDmRsTypeAPosComb.currentIndexChanged.connect(self.onMibDmrsTypeAPosCombCurIndChanged)
        self.nrMibCoreset0Edit.textChanged.connect(self.onMibCoreset0EditTextChanged)
        self.nrMibCss0Edit.textChanged.connect(self.onMibCss0EditTextChanged)
        self.nrSsbKssbEdit.textChanged.connect(self.onSsbKssbEditTextChanged)
        self.nrTddCfgPat2PeriodComb.currentIndexChanged.connect(self.onTddCfgPat2PeriodCombCurIndChanged)
        self.nrUeAntPortsComb.currentIndexChanged.connect(self.onUeAntPortsCombCurIndChanged)
        self.nrCss0AggLevelComb.currentIndexChanged.connect(self.onCss0AggLevelCombCurIndChanged)
        self.nrCss0NumCandidatesComb.currentIndexChanged.connect(self.onCss0NumCandidatesCombCurIndChanged)
        self.nrRachGenericPrachConfIdEdit.textChanged.connect(self.onPrachConfIndEditTextChanged)
        self.nrDsrRes0PeriodicityComb.currentIndexChanged.connect(self.onDsrRes0PeriodicityCombCurIndChanged)
        self.nrDsrRes1PeriodicityComb.currentIndexChanged.connect(self.onDsrRes1PeriodicityCombCurIndChanged)
        #---->signal-slot for initial dl bwp
        self.nrIniDlBwpGenericLocAndBwEdit.textChanged.connect(self.onIniDlBwpLocAndBwEditTextChanged)
        self.nrIniDlBwpGenericLRbsEdit.textChanged.connect(self.onIniDlBwpLRBsOrRBStartEditTextChanged)
        self.nrIniDlBwpGenericRbStartEdit.textChanged.connect(self.onIniDlBwpLRBsOrRBStartEditTextChanged)
        #---->signal-slot for initial ul bwp
        self.nrIniUlBwpGenericLocAndBwEdit.textChanged.connect(self.onIniUlBwpLocAndBwEditTextChanged)
        self.nrIniUlBwpGenericLRbsEdit.textChanged.connect(self.onIniUlBwpLRBsOrRBStartEditTextChanged)
        self.nrIniUlBwpGenericRbStartEdit.textChanged.connect(self.onIniUlBwpLRBsOrRBStartEditTextChanged)
        #---->signal-slot for dedicated dl bwp
        self.nrDedDlBwpGenericLocAndBwEdit.textChanged.connect(self.onDedDlBwpLocAndBwEditTextChanged)
        self.nrDedDlBwpGenericLRbsEdit.textChanged.connect(self.onDedDlBwpLRBsOrRBStartEditTextChanged)
        self.nrDedDlBwpGenericRbStartEdit.textChanged.connect(self.onDedDlBwpLRBsOrRBStartEditTextChanged)
        #---->signal-slot for dedicated ul bwp
        self.nrDedUlBwpGenericLocAndBwEdit.textChanged.connect(self.onDedUlBwpLocAndBwEditTextChanged)
        self.nrDedUlBwpGenericLRbsEdit.textChanged.connect(self.onDedUlBwpLRBsOrRBStartEditTextChanged)
        self.nrDedUlBwpGenericRbStartEdit.textChanged.connect(self.onDedUlBwpLRBsOrRBStartEditTextChanged)
        
        self.nrCoreset1DurationComb.currentIndexChanged.connect(self.onCoreset1DurationCombCurIndChanged)
        self.nrCoreset1CceRegMapComb.currentIndexChanged.connect(self.onCoreset1CceRegMapCombCurIndChanged)
        self.nrUssPeriodicityComb.currentIndexChanged.connect(self.onUssPeriodicityCombCurIndChanged)
        self.nrUssFirstSymbsEdit.textChanged.connect(self.onUssFirstSymbsEditTextChanged)
        
        #---->signal-slot for dcis
        self.nrDci10Sib1TimeAllocFieldEdit.textChanged.connect(self.onDci10Sib1TimeAllocFieldEditTextChanged)
        self.nrDci10Sib1FreqAllocType1LRbsEdit.textChanged.connect(self.onDci10Sib1Type1LRBsOrRBStartEditTextChanged)
        self.nrDci10Sib1FreqAllocType1RbStartEdit.textChanged.connect(self.onDci10Sib1Type1LRBsOrRBStartEditTextChanged)
        self.nrDci10Sib1Cw0McsEdit.textChanged.connect(self.onDci10Sib1Cw0McsEditTextChanged)
        
        self.nrDci10Msg2TimeAllocFieldEdit.textChanged.connect(self.onDci10Msg2TimeAllocFieldEditTextChanged)
        self.nrDci10Msg2FreqAllocType1LRbsEdit.textChanged.connect(self.onDci10Msg2Type1LRBsOrRBStartEditTextChanged)
        self.nrDci10Msg2FreqAllocType1RbStartEdit.textChanged.connect(self.onDci10Msg2Type1LRBsOrRBStartEditTextChanged)
        self.nrDci10Msg2Cw0McsEdit.textChanged.connect(self.onDci10Msg2Cw0McsEditTextChanged)
        self.nrDci10Msg2TbScalingEdit.textChanged.connect(self.onDci10Msg2TbScalingEditTextChanged)
        
        self.nrDci10Msg4TimeAllocFieldEdit.textChanged.connect(self.onDci10Msg4TimeAllocFieldEditTextChanged)
        self.nrDci10Msg4FreqAllocType1LRbsEdit.textChanged.connect(self.onDci10Msg4Type1LRBsOrRBStartEditTextChanged)
        self.nrDci10Msg4FreqAllocType1RbStartEdit.textChanged.connect(self.onDci10Msg4Type1LRBsOrRBStartEditTextChanged)
        self.nrDci10Msg4Cw0McsEdit.textChanged.connect(self.onDci10Msg4Cw0McsEditTextChanged)
        
        self.nrDci11PdschTimeAllocFieldEdit.textChanged.connect(self.onDci11PdschTimeAllocFieldEditTextChanged)
        self.nrDci11PdschTimeAllocSlivEdit.textChanged.connect(self.onDci11PdschTimeAllocSlivEditTextChanged)
        self.nrDci11PdschTimeAllocSEdit.textChanged.connect(self.onDci11PdschTimeAllocSOrLEditTextChanged)
        self.nrDci11PdschTimeAllocLEdit.textChanged.connect(self.onDci11PdschTimeAllocSOrLEditTextChanged)
        self.nrDci11PdschTimeAllocMappingTypeComb.currentIndexChanged.connect(self.onDci11MappingTypeOrDedDlBwpCpCombCurIndChanged)
        self.nrDci11PdschFreqAllocTypeComb.currentIndexChanged.connect(self.onDci11PdschFreqRaTypeCombCurIndChanged)
        self.nrDci11PdschFreqAllocType1LRbsEdit.textChanged.connect(self.onDci11PdschType1LRBsOrRBStartEditTextChanged)
        self.nrDci11PdschFreqAllocType1RbStartEdit.textChanged.connect(self.onDci11PdschType1LRBsOrRBStartEditTextChanged)
        self.nrDci11PdschFreqAllocFieldEdit.textChanged.connect(self.onDci11PdschFreqAllocFieldEditTextChanged)
        self.nrDci11PdschCw0McsEdit.textChanged.connect(self.onDci11PdschCw0McsOrCw1McsEditTextChanged)
        self.nrDci11PdschCw1McsEdit.textChanged.connect(self.onDci11PdschCw0McsOrCw1McsEditTextChanged)
        self.nrDci11PdschAntPortsFieldEdit.textChanged.connect(self.onDci11PdschAntPortsEditTextChanged)
        
        self.nrMsg3PuschTimeAllocFieldEdit.textChanged.connect(self.onMsg3PuschTimeAllocFieldEditTextChanged)
        self.nrMsg3PuschFreqAllocFieldEdit.textChanged.connect(self.onMsg3PuschFreqAllocFieldEditTextChanged)
        self.nrMsg3PuschFreqAllocType1LRbsEdit.textChanged.connect(self.onMsg3PuschLRBsOrRBStartEditTextChanged)
        self.nrMsg3PuschFreqAllocType1RbStartEdit.textChanged.connect(self.onMsg3PuschLRBsOrRBStartEditTextChanged)
        self.nrMsg3PuschFreqAllocFreqHopComb.currentIndexChanged.connect(self.onMsg3PuschFreqHopCombCurIndChanged)
        self.nrMsg3PuschCw0McsEdit.textChanged.connect(self.onMsg3PuschCw0McsEditTextChanged)
        
        self.nrDci01PuschTimeAllocFieldEdit.textChanged.connect(self.onDci01PuschTimeAllocFieldEditTextChanged)
        self.nrDci01PuschTimeAllocSlivEdit.textChanged.connect(self.onDci01PuschTimeAllocSlivEditTextChanged)
        self.nrDci01PuschTimeAllocSEdit.textChanged.connect(self.onDci01PuschTimeAllocSOrLEditTextChanged)
        self.nrDci01PuschTimeAllocLEdit.textChanged.connect(self.onDci01PuschTimeAllocSOrLEditTextChanged)
        self.nrDci01PuschTimeAllocMappingTypeComb.currentIndexChanged.connect(self.onDci01MappingTypeOrDedUlBwpCpCombCurIndChanged)
        self.nrDci01PuschFreqAllocTypeComb.currentIndexChanged.connect(self.onDci01PuschFreqRaTypeCombCurIndChanged)
        self.nrDci01PuschFreqAllocType1LRbsEdit.textChanged.connect(self.onDci01PuschType1LRBsOrRBStartEditTextChanged)
        self.nrDci01PuschFreqAllocType1RbStartEdit.textChanged.connect(self.onDci01PuschType1LRBsOrRBStartEditTextChanged)
        self.nrDci01PuschFreqAllocFieldEdit.textChanged.connect(self.onDci01PuschFreqAllocFieldEditTextChanged)
        self.nrDci01PuschFreqAllocFreqHopComb.currentIndexChanged.connect(self.onDci01PuschFreqHopCombCurIndChanged)
        self.nrDci01PuschCw0McsEdit.textChanged.connect(self.onDci01PuschCw0McsEditTextChanged)
        self.nrDci01PuschPrecodingLayersFieldEdit.textChanged.connect(self.onDci01PuschPrecodingLayersEditTextChanged)
        self.nrDci01PuschSriFieldEdit.textChanged.connect(self.onDci01PuschSriEditTextChanged)
        self.nrDci01PuschAntPortsFieldEdit.textChanged.connect(self.onDci01PuschAntPortsEditTextChanged)
        self.nrDci01PuschPtrsDmrsMappingEdit.textChanged.connect(self.onDci01PuschPtrsDmrsMappingEditTextChanged)
        
        #---->initial dl bwp
        self.nrIniDlBwpGenericCpComb.currentIndexChanged.connect(self.onIniDlBwpCpCombCurIndChanged)
        #---->dedicated dl bwp
        self.nrDedDlBwpGenericCpComb.currentIndexChanged.connect(self.onDci11MappingTypeOrDedDlBwpCpCombCurIndChanged)
        self.nrDedPdschCfgRbgConfigComb.currentIndexChanged.connect(self.onDedPdschCfgRbgConfigCombCurIndChanged)
        self.nrDedPdschCfgMcsTableComb.currentIndexChanged.connect(self.onDedPdschCfgMcsTableCombCurIndChanged)
        self.nrDedPdschCfgXOverheadComb.currentIndexChanged.connect(self.onDedPdschCfgXOverheadCombCurIndChanged)
        self.nrDmrsDedPdschMaxLengthComb.currentIndexChanged.connect(self.onDmrsDedPdschMaxLengthCombCurIndChanged)
        self.nrDmrsDedPdschMaxLengthComb.currentIndexChanged.connect(self.onDmrsDedPdschDmrsTypeOrMaxLengthCombCurIndChanged)
        self.nrDmrsDedPdschDmrsTypeComb.currentIndexChanged.connect(self.onDmrsDedPdschDmrsTypeOrMaxLengthCombCurIndChanged)
        self.nrDmrsDedPdschAddPosComb.currentIndexChanged.connect(self.onDmrsDedPdschAddPosCombCurIndChanged)
        #---->dedicated ul bwp
        self.nrDedUlBwpGenericCpComb.currentIndexChanged.connect(self.onDci01MappingTypeOrDedUlBwpCpCombCurIndChanged)
        self.nrDedPuschCfgRbgConfigComb.currentIndexChanged.connect(self.onDedPuschCfgRbgConfigCombCurIndChanged)
        self.nrDedPuschCfgTpComb.currentIndexChanged.connect(self.onDedPuschCfgTpCombCurIndChanged)
        self.nrDedPuschCfgTxCfgComb.currentIndexChanged.connect(self.onDedPuschCfgTxCfgCombCurIndChanged)
        self.nrDedPuschCfgCbMaxRankEdit.textChanged.connect(self.onDedPuschCfgCbMaxRankTextChanged)
        self.nrDedPuschCfgCbSubsetComb.currentIndexChanged.connect(self.onDedPuschCfgCbSubsetCombCurIndChanged)
        self.nrDedPuschCfgNonCbMaxLayersEdit.textChanged.connect(self.onDedPuschCfgNonCbMaxLayersTextChanged)
        self.nrDedPuschCfgMcsTableComb.currentIndexChanged.connect(self.onDedPuschCfgMcsTableCombCurIndChanged)
        self.nrDedPuschCfgXOverheadComb.currentIndexChanged.connect(self.onDedPuschCfgXOverheadCombCurIndChanged)
        self.nrDmrsDedPuschMaxLengthComb.currentIndexChanged.connect(self.onDmrsDedPuschMaxLengthCombCurIndChanged)
        self.nrDmrsDedPuschDmrsTypeComb.currentIndexChanged.connect(self.onDmrsDedPuschDmrsTypeCombCurIndChanged)
        self.nrDmrsDedPuschAddPosComb.currentIndexChanged.connect(self.onDmrsDedPuschAddPosCombCurIndChanged)
        self.nrSrsResSet0ResourceIdListEdit.textChanged.connect(self.onSrsResSet0ResourceIdListTextChanged)
        self.nrSrsResSet1ResourceIdListEdit.textChanged.connect(self.onSrsResSet1ResourceIdListTextChanged)
        self.nrPtrsPuschTpGroupPatComb.currentIndexChanged.connect(self.onPtrsPuschTpGroupPatCombCurIndChanged)
        self.nrPtrsPuschMaxNumPortsComb.currentIndexChanged.connect(self.onPtrsPuschMaxNumPortsCombCurIndChanged)
        self.nrSrsRes0NumAntPortsComb.currentIndexChanged.connect(self.onSrsResNumAntPortsCombCurIndChanged)
        self.nrSrsRes1NumAntPortsComb.currentIndexChanged.connect(self.onSrsResNumAntPortsCombCurIndChanged)
        self.nrSrsRes2NumAntPortsComb.currentIndexChanged.connect(self.onSrsResNumAntPortsCombCurIndChanged)
        self.nrSrsRes3NumAntPortsComb.currentIndexChanged.connect(self.onSrsResNumAntPortsCombCurIndChanged)
        self.nrSrsRes0NonCbPtrsPortIndComb.currentIndexChanged.connect(self.onSrsResNonCbPtrsPortIndCombCurIndChanged)
        self.nrSrsRes1NonCbPtrsPortIndComb.currentIndexChanged.connect(self.onSrsResNonCbPtrsPortIndCombCurIndChanged)
        self.nrSrsRes2NonCbPtrsPortIndComb.currentIndexChanged.connect(self.onSrsResNonCbPtrsPortIndCombCurIndChanged)
        self.nrSrsRes3NonCbPtrsPortIndComb.currentIndexChanged.connect(self.onSrsResNonCbPtrsPortIndCombCurIndChanged)
        self.nrSrsRes0NumCombComb.currentIndexChanged.connect(self.onSrsRes0NumCombCombCurIndChanged)
        self.nrSrsRes1NumCombComb.currentIndexChanged.connect(self.onSrsRes1NumCombCombCurIndChanged)
        self.nrSrsRes2NumCombComb.currentIndexChanged.connect(self.onSrsRes2NumCombCombCurIndChanged)
        self.nrSrsRes3NumCombComb.currentIndexChanged.connect(self.onSrsRes3NumCombCombCurIndChanged)
        self.nrSrsRes0PeriodComb.currentIndexChanged.connect(self.onSrsRes0PeriodCombCurIndChanged)
        self.nrSrsRes1PeriodComb.currentIndexChanged.connect(self.onSrsRes1PeriodCombCurIndChanged)
        self.nrSrsRes2PeriodComb.currentIndexChanged.connect(self.onSrsRes2PeriodCombCurIndChanged)
        self.nrSrsRes3PeriodComb.currentIndexChanged.connect(self.onSrsRes3PeriodCombCurIndChanged)
        #---->initial ul bwp
        self.nrRachMsg3TpComb.currentIndexChanged.connect(self.onRachMsg3TpCombCurIndChanged)
        self.nrRachSsbPerRachOccasionComb.currentIndexChanged.connect(self.onRachSsbPerRachOccasionCombCurIndChanged)
        self.nrRachNumRaPreamblesEdit.textChanged.connect(self.onRachNumRaPreamblesTextChanged)
        self.nrPucchSib1PucchResCommonEdit.textChanged.connect(self.onPucchSib1PucchResCommonTextChanged)
        
        #---->I am THE driver!
        self.nrCarrierBandComb.setCurrentText('n77')

        #-->Tab Widgets
        tabWidget = QTabWidget()
        tabWidget.addTab(gridCfgWidget, 'Grid Settings')
        tabWidget.addTab(commonCfgWidget, 'Common Settings')
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
        
        #refer to 3GPP 38.211 vf30
        #Table 6.3.3.1-1: PRACH preamble formats for L_RA=839 and scsRA={1.25k, 5k}
        self.nrScsRaLongPrach = {
            '839_0' : '1.25KHz',
            '839_1' : '1.25KHz',
            '839_2' : '1.25KHz',
            '839_3' : '5KHz',
            }
        
        #Table 6.3.3.2-1: Supported combinations of scsRA and scsPusch, and the corresponding value of kBar  
        self.nrNumRbRaAndKBar = {
            '839_1.25_15' : (6, 7),
            '839_1.25_30' : (3, 1),
            '839_1.25_60' : (2, 133),
            '839_5_15' : (24, 12),
            '839_5_30' : (12, 10),
            '839_5_60' : (6, 7),
            '139_15_15' : (12, 2),
            '139_15_30' : (6, 2),
            '139_15_60' : (3, 2),
            '139_30_15' : (24, 2),
            '139_30_30' : (12, 2),
            '139_30_60' : (6, 2),
            '139_60_60' : (12, 2),
            '139_60_120' : (6, 2),
            '139_120_60' : (24, 2),
            '139_120_120' : (12, 2),
            }
        
        #Table 6.3.3.2-2: Random access configurations for FR1 and paired spectrum/supplementary uplink.
        self.nrRaCfgFr1FddSUl = {
            0 : ('0', 16, (1,), (1,), 0, 0, 0, 0),
            1 : ('0', 16, (1,), (4,), 0, 0, 0, 0),
            2 : ('0', 16, (1,), (7,), 0, 0, 0, 0),
            3 : ('0', 16, (1,), (9,), 0, 0, 0, 0),
            4 : ('0', 8, (1,), (1,), 0, 0, 0, 0),
            5 : ('0', 8, (1,), (4,), 0, 0, 0, 0),
            6 : ('0', 8, (1,), (7,), 0, 0, 0, 0),
            7 : ('0', 8, (1,), (9,), 0, 0, 0, 0),
            8 : ('0', 4, (1,), (1,), 0, 0, 0, 0),
            9 : ('0', 4, (1,), (4,), 0, 0, 0, 0),
            10 : ('0', 4, (1,), (7,), 0, 0, 0, 0),
            11 : ('0', 4, (1,), (9,), 0, 0, 0, 0),
            12 : ('0', 2, (1,), (1,), 0, 0, 0, 0),
            13 : ('0', 2, (1,), (4,), 0, 0, 0, 0),
            14 : ('0', 2, (1,), (7,), 0, 0, 0, 0),
            15 : ('0', 2, (1,), (9,), 0, 0, 0, 0),
            16 : ('0', 1, (0,), (1,), 0, 0, 0, 0),
            17 : ('0', 1, (0,), (4,), 0, 0, 0, 0),
            18 : ('0', 1, (0,), (7,), 0, 0, 0, 0),
            19 : ('0', 1, (0,), (1,6,), 0, 0, 0, 0),
            20 : ('0', 1, (0,), (2,7,), 0, 0, 0, 0),
            21 : ('0', 1, (0,), (3,8,), 0, 0, 0, 0),
            22 : ('0', 1, (0,), (1,4,7,), 0, 0, 0, 0),
            23 : ('0', 1, (0,), (2,5,8,), 0, 0, 0, 0),
            24 : ('0', 1, (0,), (3, 6, 9,), 0, 0, 0, 0),
            25 : ('0', 1, (0,), (0,2,4,6,8,), 0, 0, 0, 0),
            26 : ('0', 1, (0,), (1,3,5,7,9,), 0, 0, 0, 0),
            27 : ('0', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 0, 0, 0),
            28 : ('1', 16, (1,), (1,), 0, 0, 0, 0),
            29 : ('1', 16, (1,), (4,), 0, 0, 0, 0),
            30 : ('1', 16, (1,), (7,), 0, 0, 0, 0),
            31 : ('1', 16, (1,), (9,), 0, 0, 0, 0),
            32 : ('1', 8, (1,), (1,), 0, 0, 0, 0),
            33 : ('1', 8, (1,), (4,), 0, 0, 0, 0),
            34 : ('1', 8, (1,), (7,), 0, 0, 0, 0),
            35 : ('1', 8, (1,), (9,), 0, 0, 0, 0),
            36 : ('1', 4, (1,), (1,), 0, 0, 0, 0),
            37 : ('1', 4, (1,), (4,), 0, 0, 0, 0),
            38 : ('1', 4, (1,), (7,), 0, 0, 0, 0),
            39 : ('1', 4, (1,), (9,), 0, 0, 0, 0),
            40 : ('1', 2, (1,), (1,), 0, 0, 0, 0),
            41 : ('1', 2, (1,), (4,), 0, 0, 0, 0),
            42 : ('1', 2, (1,), (7,), 0, 0, 0, 0),
            43 : ('1', 2, (1,), (9,), 0, 0, 0, 0),
            44 : ('1', 1, (0,), (1,), 0, 0, 0, 0),
            45 : ('1', 1, (0,), (4,), 0, 0, 0, 0),
            46 : ('1', 1, (0,), (7,), 0, 0, 0, 0),
            47 : ('1', 1, (0,), (1,6,), 0, 0, 0, 0),
            48 : ('1', 1, (0,), (2,7,), 0, 0, 0, 0),
            49 : ('1', 1, (0,), (3,8,), 0, 0, 0, 0),
            50 : ('1', 1, (0,), (1,4,7,), 0, 0, 0, 0),
            51 : ('1', 1, (0,), (2,5,8,), 0, 0, 0, 0),
            52 : ('1', 1, (0,), (3,6,9,), 0, 0, 0, 0),
            53 : ('2', 16, (1,), (1,), 0, 0, 0, 0),
            54 : ('2', 8, (1,), (1,), 0, 0, 0, 0),
            55 : ('2', 4, (0,), (1,), 0, 0, 0, 0),
            56 : ('2', 2, (0,), (1,), 0, 0, 0, 0),
            57 : ('2', 2, (0,), (5,), 0, 0, 0, 0),
            58 : ('2', 1, (0,), (1,), 0, 0, 0, 0),
            59 : ('2', 1, (0,), (5,), 0, 0, 0, 0),
            60 : ('3', 16, (1,), (1,), 0, 0, 0, 0),
            61 : ('3', 16, (1,), (4,), 0, 0, 0, 0),
            62 : ('3', 16, (1,), (7,), 0, 0, 0, 0),
            63 : ('3', 16, (1,), (9,), 0, 0, 0, 0),
            64 : ('3', 8, (1,), (1,), 0, 0, 0, 0),
            65 : ('3', 8, (1,), (4,), 0, 0, 0, 0),
            66 : ('3', 8, (1,), (7,), 0, 0, 0, 0),
            67 : ('3', 4, (1,), (1,), 0, 0, 0, 0),
            68 : ('3', 4, (1,), (4,), 0, 0, 0, 0),
            69 : ('3', 4, (1,), (7,), 0, 0, 0, 0),
            70 : ('3', 4, (1,), (9,), 0, 0, 0, 0),
            71 : ('3', 2, (1,), (1,), 0, 0, 0, 0),
            72 : ('3', 2, (1,), (4,), 0, 0, 0, 0),
            73 : ('3', 2, (1,), (7,), 0, 0, 0, 0),
            74 : ('3', 2, (1,), (9,), 0, 0, 0, 0),
            75 : ('3', 1, (0,), (1,), 0, 0, 0, 0),
            76 : ('3', 1, (0,), (4,), 0, 0, 0, 0),
            77 : ('3', 1, (0,), (7,), 0, 0, 0, 0),
            78 : ('3', 1, (0,), (1,6,), 0, 0, 0, 0),
            79 : ('3', 1, (0,), (2,7,), 0, 0, 0, 0),
            80 : ('3', 1, (0,), (3,8,), 0, 0, 0, 0),
            81 : ('3', 1, (0,), (1,4,7,), 0, 0, 0, 0),
            82 : ('3', 1, (0,), (2,5,8,), 0, 0, 0, 0),
            83 : ('3', 1, (0,), (3, 6, 9,), 0, 0, 0, 0),
            84 : ('3', 1, (0,), (0,2,4,6,8,), 0, 0, 0, 0),
            85 : ('3', 1, (0,), (1,3,5,7,9,), 0, 0, 0, 0),
            86 : ('3', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 0, 0, 0),
            87 : ('A1', 16, (0,), (4,9,), 0, 1, 6, 2),
            88 : ('A1', 16, (1,), (4,), 0, 2, 6, 2),
            89 : ('A1', 8, (0,), (4,9,), 0, 1, 6, 2),
            90 : ('A1', 8, (1,), (4,), 0, 2, 6, 2),
            91 : ('A1', 4, (0,), (4,9,), 0, 1, 6, 2),
            92 : ('A1', 4, (1,), (4,9,), 0, 1, 6, 2),
            93 : ('A1', 4, (0,), (4,), 0, 2, 6, 2),
            94 : ('A1', 2, (0,), (4,9,), 0, 1, 6, 2),
            95 : ('A1', 2, (0,), (1,), 0, 2, 6, 2),
            96 : ('A1', 2, (0,), (4,), 0, 2, 6, 2),
            97 : ('A1', 2, (0,), (7,), 0, 2, 6, 2),
            98 : ('A1', 1, (0,), (4,), 0, 1, 6, 2),
            99 : ('A1', 1, (0,), (1,6,), 0, 1, 6, 2),
            100 : ('A1', 1, (0,), (4,9,), 0, 1, 6, 2),
            101 : ('A1', 1, (0,), (1,), 0, 2, 6, 2),
            102 : ('A1', 1, (0,), (7,), 0, 2, 6, 2),
            103 : ('A1', 1, (0,), (2,7,), 0, 2, 6, 2),
            104 : ('A1', 1, (0,), (1,4,7,), 0, 2, 6, 2),
            105 : ('A1', 1, (0,), (0,2,4,6,8,), 0, 2, 6, 2),
            106 : ('A1', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 2, 6, 2),
            107 : ('A1', 1, (0,), (1,3,5,7,9,), 0, 2, 6, 2),
            108 : ('A1/B1', 2, (0,), (4,9,), 0, 1, 7, 2),
            109 : ('A1/B1', 2, (0,), (4,), 0, 2, 7, 2),
            110 : ('A1/B1', 1, (0,), (4,), 0, 1, 7, 2),
            111 : ('A1/B1', 1, (0,), (1,6,), 0, 1, 7, 2),
            112 : ('A1/B1', 1, (0,), (4,9,), 0, 1, 7, 2),
            113 : ('A1/B1', 1, (0,), (1,), 0, 2, 7, 2),
            114 : ('A1/B1', 1, (0,), (7,), 0, 2, 7, 2),
            115 : ('A1/B1', 1, (0,), (1,4,7,), 0, 2, 7, 2),
            116 : ('A1/B1', 1, (0,), (0,2,4,6,8,), 0, 2, 7, 2),
            117 : ('A2', 16, (1,), (2,6,9,), 0, 1, 3, 4),
            118 : ('A2', 16, (1,), (4,), 0, 2, 3, 4),
            119 : ('A2', 8, (1,), (2,6,9,), 0, 1, 3, 4),
            120 : ('A2', 8, (1,), (4,), 0, 2, 3, 4),
            121 : ('A2', 4, (0,), (2,6,9,), 0, 1, 3, 4),
            122 : ('A2', 4, (0,), (4,), 0, 2, 3, 4),
            123 : ('A2', 2, (1,), (2,6,9,), 0, 1, 3, 4),
            124 : ('A2', 2, (0,), (1,), 0, 2, 3, 4),
            125 : ('A2', 2, (0,), (4,), 0, 2, 3, 4),
            126 : ('A2', 2, (0,), (7,), 0, 2, 3, 4),
            127 : ('A2', 1, (0,), (4,), 0, 1, 3, 4),
            128 : ('A2', 1, (0,), (1,6,), 0, 1, 3, 4),
            129 : ('A2', 1, (0,), (4,9,), 0, 1, 3, 4),
            130 : ('A2', 1, (0,), (1,), 0, 2, 3, 4),
            131 : ('A2', 1, (0,), (7,), 0, 2, 3, 4),
            132 : ('A2', 1, (0,), (2,7,), 0, 2, 3, 4),
            133 : ('A2', 1, (0,), (1,4,7,), 0, 2, 3, 4),
            134 : ('A2', 1, (0,), (0,2,4,6,8,), 0, 2, 3, 4),
            135 : ('A2', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 2, 3, 4),
            136 : ('A2', 1, (0,), (1,3,5,7,9,), 0, 2, 3, 4),
            137 : ('A2/B2', 2, (1,), (2,6,9,), 0, 1, 3, 4),
            138 : ('A2/B2', 2, (0,), (4,), 0, 2, 3, 4),
            139 : ('A2/B2', 1, (0,), (4,), 0, 1, 3, 4),
            140 : ('A2/B2', 1, (0,), (1,6,), 0, 1, 3, 4),
            141 : ('A2/B2', 1, (0,), (4,9,), 0, 1, 3, 4),
            142 : ('A2/B2', 1, (0,), (1,), 0, 2, 3, 4),
            143 : ('A2/B2', 1, (0,), (7,), 0, 2, 3, 4),
            144 : ('A2/B2', 1, (0,), (1,4,7,), 0, 2, 3, 4),
            145 : ('A2/B2', 1, (0,), (0,2,4,6,8,), 0, 2, 3, 4),
            146 : ('A2/B2', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 2, 3, 4),
            147 : ('A3', 16, (1,), (4,9,), 0, 1, 2, 6),
            148 : ('A3', 16, (1,), (4,), 0, 2, 2, 6),
            149 : ('A3', 8, (1,), (4,9,), 0, 1, 2, 6),
            150 : ('A3', 8, (1,), (4,), 0, 2, 2, 6),
            151 : ('A3', 4, (0,), (4,9,), 0, 1, 2, 6),
            152 : ('A3', 4, (0,), (4,), 0, 2, 2, 6),
            153 : ('A3', 2, (1,), (2,6,9,), 0, 2, 2, 6),
            154 : ('A3', 2, (0,), (1,), 0, 2, 2, 6),
            155 : ('A3', 2, (0,), (4,), 0, 2, 2, 6),
            156 : ('A3', 2, (0,), (7,), 0, 2, 2, 6),
            157 : ('A3', 1, (0,), (4,), 0, 1, 2, 6),
            158 : ('A3', 1, (0,), (1,6,), 0, 1, 2, 6),
            159 : ('A3', 1, (0,), (4,9,), 0, 1, 2, 6),
            160 : ('A3', 1, (0,), (1,), 0, 2, 2, 6),
            161 : ('A3', 1, (0,), (7,), 0, 2, 2, 6),
            162 : ('A3', 1, (0,), (2,7,), 0, 2, 2, 6),
            163 : ('A3', 1, (0,), (1,4,7,), 0, 2, 2, 6),
            164 : ('A3', 1, (0,), (0,2,4,6,8,), 0, 2, 2, 6),
            165 : ('A3', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 2, 2, 6),
            166 : ('A3', 1, (0,), (1,3,5,7,9,), 0, 2, 2, 6),
            167 : ('A3/B3', 2, (1,), (2,6,9,), 0, 2, 2, 6),
            168 : ('A3/B3', 2, (0,), (4,), 0, 2, 2, 6),
            169 : ('A3/B3', 1, (0,), (4,), 0, 1, 2, 6),
            170 : ('A3/B3', 1, (0,), (1,6,), 0, 1, 2, 6),
            171 : ('A3/B3', 1, (0,), (4,9,), 0, 1, 2, 6),
            172 : ('A3/B3', 1, (0,), (1,), 0, 2, 2, 6),
            173 : ('A3/B3', 1, (0,), (7,), 0, 2, 2, 6),
            174 : ('A3/B3', 1, (0,), (1,4,7,), 0, 2, 2, 6),
            175 : ('A3/B3', 1, (0,), (0,2,4,6,8,), 0, 2, 2, 6),
            176 : ('A3/B3', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 2, 2, 6),
            177 : ('B1', 16, (0,), (4,9,), 0, 1, 7, 2),
            178 : ('B1', 16, (1,), (4,), 0, 2, 7, 2),
            179 : ('B1', 8, (0,), (4,9,), 0, 1, 7, 2),
            180 : ('B1', 8, (1,), (4,), 0, 2, 7, 2),
            181 : ('B1', 4, (0,), (4,9,), 0, 1, 7, 2),
            182 : ('B1', 4, (1,), (4,9,), 0, 1, 7, 2),
            183 : ('B1', 4, (0,), (4,), 0, 2, 7, 2),
            184 : ('B1', 2, (0,), (4,9,), 0, 1, 7, 2),
            185 : ('B1', 2, (0,), (1,), 0, 2, 7, 2),
            186 : ('B1', 2, (0,), (4,), 0, 2, 7, 2),
            187 : ('B1', 2, (0,), (7,), 0, 2, 7, 2),
            188 : ('B1', 1, (0,), (4,), 0, 1, 7, 2),
            189 : ('B1', 1, (0,), (1,6,), 0, 1, 7, 2),
            190 : ('B1', 1, (0,), (4,9,), 0, 1, 7, 2),
            191 : ('B1', 1, (0,), (1,), 0, 2, 7, 2),
            192 : ('B1', 1, (0,), (7,), 0, 2, 7, 2),
            193 : ('B1', 1, (0,), (2,7,), 0, 2, 7, 2),
            194 : ('B1', 1, (0,), (1,4,7,), 0, 2, 7, 2),
            195 : ('B1', 1, (0,), (0,2,4,6,8,), 0, 2, 7, 2),
            196 : ('B1', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 2, 7, 2),
            197 : ('B1', 1, (0,), (1,3,5,7,9,), 0, 2, 7, 2),
            198 : ('B4', 16, (0,), (4,9,), 0, 2, 1, 12),
            199 : ('B4', 16, (1,), (4,), 0, 2, 1, 12),
            200 : ('B4', 8, (0,), (4,9,), 0, 2, 1, 12),
            201 : ('B4', 8, (1,), (4,), 0, 2, 1, 12),
            202 : ('B4', 4, (0,), (4,9,), 0, 2, 1, 12),
            203 : ('B4', 4, (0,), (4,), 0, 2, 1, 12),
            204 : ('B4', 4, (1,), (4,9,), 0, 2, 1, 12),
            205 : ('B4', 2, (0,), (4,9,), 0, 2, 1, 12),
            206 : ('B4', 2, (0,), (1,), 0, 2, 1, 12),
            207 : ('B4', 2, (0,), (4,), 0, 2, 1, 12),
            208 : ('B4', 2, (0,), (7,), 0, 2, 1, 12),
            209 : ('B4', 1, (0,), (1,), 0, 2, 1, 12),
            210 : ('B4', 1, (0,), (4,), 0, 2, 1, 12),
            211 : ('B4', 1, (0,), (7,), 0, 2, 1, 12),
            212 : ('B4', 1, (0,), (1,6,), 0, 2, 1, 12),
            213 : ('B4', 1, (0,), (2,7,), 0, 2, 1, 12),
            214 : ('B4', 1, (0,), (4,9,), 0, 2, 1, 12),
            215 : ('B4', 1, (0,), (1,4,7,), 0, 2, 1, 12),
            216 : ('B4', 1, (0,), (0,2,4,6,8,), 0, 2, 1, 12),
            217 : ('B4', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 2, 1, 12),
            218 : ('B4', 1, (0,), (1,3,5,7,9,), 0, 2, 1, 12),
            219 : ('C0', 8, (1,), (4,), 0, 2, 7, 2),
            220 : ('C0', 4, (1,), (4,9,), 0, 1, 7, 2),
            221 : ('C0', 4, (0,), (4,), 0, 2, 7, 2),
            222 : ('C0', 2, (0,), (4,9,), 0, 1, 7, 2),
            223 : ('C0', 2, (0,), (1,), 0, 2, 7, 2),
            224 : ('C0', 2, (0,), (4,), 0, 2, 7, 2),
            225 : ('C0', 2, (0,), (7,), 0, 2, 7, 2),
            226 : ('C0', 1, (0,), (4,), 0, 1, 7, 2),
            227 : ('C0', 1, (0,), (1,6,), 0, 1, 7, 2),
            228 : ('C0', 1, (0,), (4,9,), 0, 1, 7, 2),
            229 : ('C0', 1, (0,), (1,), 0, 2, 7, 2),
            230 : ('C0', 1, (0,), (7,), 0, 2, 7, 2),
            231 : ('C0', 1, (0,), (2,7,), 0, 2, 7, 2),
            232 : ('C0', 1, (0,), (1,4,7,), 0, 2, 7, 2),
            233 : ('C0', 1, (0,), (0,2,4,6,8,), 0, 2, 7, 2),
            234 : ('C0', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 2, 7, 2),
            235 : ('C0', 1, (0,), (1,3,5,7,9,), 0, 2, 7, 2),
            236 : ('C2', 16, (1,), (4,9,), 0, 1, 2, 6),
            237 : ('C2', 16, (1,), (4,), 0, 2, 2, 6),
            238 : ('C2', 8, (1,), (4,9,), 0, 1, 2, 6),
            239 : ('C2', 8, (1,), (4,), 0, 2, 2, 6),
            240 : ('C2', 4, (0,), (4,9,), 0, 1, 2, 6),
            241 : ('C2', 4, (0,), (4,), 0, 2, 2, 6),
            242 : ('C2', 2, (1,), (2,6,9,), 0, 2, 2, 6),
            243 : ('C2', 2, (0,), (1,), 0, 2, 2, 6),
            244 : ('C2', 2, (0,), (4,), 0, 2, 2, 6),
            245 : ('C2', 2, (0,), (7,), 0, 2, 2, 6),
            246 : ('C2', 1, (0,), (4,), 0, 1, 2, 6),
            247 : ('C2', 1, (0,), (1,6,), 0, 1, 2, 6),
            248 : ('C2', 1, (0,), (4,9,), 0, 1, 2, 6),
            249 : ('C2', 1, (0,), (1,), 0, 2, 2, 6),
            250 : ('C2', 1, (0,), (7,), 0, 2, 2, 6),
            251 : ('C2', 1, (0,), (2,7,), 0, 2, 2, 6),
            252 : ('C2', 1, (0,), (1,4,7,), 0, 2, 2, 6),
            253 : ('C2', 1, (0,), (0,2,4,6,8,), 0, 2, 2, 6),
            254 : ('C2', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 2, 2, 6),
            255 : ('C2', 1, (0,), (1,3,5,7,9,), 0, 2, 2, 6),
            }
        
        #Table 6.3.3.2-3: Random access configurations for FR1 and unpaired spectrum.
        self.nrRaCfgFr1Tdd = {
            0 : ('0', 16, (1,), (9,), 0, 0, 0, 0),
            1 : ('0', 8, (1,), (9,), 0, 0, 0, 0),
            2 : ('0', 4, (1,), (9,), 0, 0, 0, 0),
            3 : ('0', 2, (0,), (9,), 0, 0, 0, 0),
            4 : ('0', 2, (1,), (9,), 0, 0, 0, 0),
            5 : ('0', 2, (0,), (4,), 0, 0, 0, 0),
            6 : ('0', 2, (1,), (4,), 0, 0, 0, 0),
            7 : ('0', 1, (0,), (9,), 0, 0, 0, 0),
            8 : ('0', 1, (0,), (8,), 0, 0, 0, 0),
            9 : ('0', 1, (0,), (7,), 0, 0, 0, 0),
            10 : ('0', 1, (0,), (6,), 0, 0, 0, 0),
            11 : ('0', 1, (0,), (5,), 0, 0, 0, 0),
            12 : ('0', 1, (0,), (4,), 0, 0, 0, 0),
            13 : ('0', 1, (0,), (3,), 0, 0, 0, 0),
            14 : ('0', 1, (0,), (2,), 0, 0, 0, 0),
            15 : ('0', 1, (0,), (1,6,), 0, 0, 0, 0),
            16 : ('0', 1, (0,), (1,6,), 7, 0, 0, 0),
            17 : ('0', 1, (0,), (4,9,), 0, 0, 0, 0),
            18 : ('0', 1, (0,), (3,8,), 0, 0, 0, 0),
            19 : ('0', 1, (0,), (2,7,), 0, 0, 0, 0),
            20 : ('0', 1, (0,), (8,9,), 0, 0, 0, 0),
            21 : ('0', 1, (0,), (4,8,9,), 0, 0, 0, 0),
            22 : ('0', 1, (0,), (3,4,9,), 0, 0, 0, 0),
            23 : ('0', 1, (0,), (7,8,9,), 0, 0, 0, 0),
            24 : ('0', 1, (0,), (3,4,8,9,), 0, 0, 0, 0),
            25 : ('0', 1, (0,), (6,7,8,9,), 0, 0, 0, 0),
            26 : ('0', 1, (0,), (1,4,6,9,), 0, 0, 0, 0),
            27 : ('0', 1, (0,), (1,3,5,7,9,), 0, 0, 0, 0),
            28 : ('1', 16, (1,), (7,), 0, 0, 0, 0),
            29 : ('1', 8, (1,), (7,), 0, 0, 0, 0),
            30 : ('1', 4, (1,), (7,), 0, 0, 0, 0),
            31 : ('1', 2, (0,), (7,), 0, 0, 0, 0),
            32 : ('1', 2, (1,), (7,), 0, 0, 0, 0),
            33 : ('1', 1, (0,), (7,), 0, 0, 0, 0),
            34 : ('2', 16, (1,), (6,), 0, 0, 0, 0),
            35 : ('2', 8, (1,), (6,), 0, 0, 0, 0),
            36 : ('2', 4, (1,), (6,), 0, 0, 0, 0),
            37 : ('2', 2, (0,), (6,), 7, 0, 0, 0),
            38 : ('2', 2, (1,), (6,), 7, 0, 0, 0),
            39 : ('2', 1, (0,), (6,), 7, 0, 0, 0),
            40 : ('3', 16, (1,), (9,), 0, 0, 0, 0),
            41 : ('3', 8, (1,), (9,), 0, 0, 0, 0),
            42 : ('3', 4, (1,), (9,), 0, 0, 0, 0),
            43 : ('3', 2, (0,), (9,), 0, 0, 0, 0),
            44 : ('3', 2, (1,), (9,), 0, 0, 0, 0),
            45 : ('3', 2, (0,), (4,), 0, 0, 0, 0),
            46 : ('3', 2, (1,), (4,), 0, 0, 0, 0),
            47 : ('3', 1, (0,), (9,), 0, 0, 0, 0),
            48 : ('3', 1, (0,), (8,), 0, 0, 0, 0),
            49 : ('3', 1, (0,), (7,), 0, 0, 0, 0),
            50 : ('3', 1, (0,), (6,), 0, 0, 0, 0),
            51 : ('3', 1, (0,), (5,), 0, 0, 0, 0),
            52 : ('3', 1, (0,), (4,), 0, 0, 0, 0),
            53 : ('3', 1, (0,), (3,), 0, 0, 0, 0),
            54 : ('3', 1, (0,), (2,), 0, 0, 0, 0),
            55 : ('3', 1, (0,), (1,6,), 0, 0, 0, 0),
            56 : ('3', 1, (0,), (1,6,), 7, 0, 0, 0),
            57 : ('3', 1, (0,), (4,9,), 0, 0, 0, 0),
            58 : ('3', 1, (0,), (3,8,), 0, 0, 0, 0),
            59 : ('3', 1, (0,), (2,7,), 0, 0, 0, 0),
            60 : ('3', 1, (0,), (8,9,), 0, 0, 0, 0),
            61 : ('3', 1, (0,), (4,8,9,), 0, 0, 0, 0),
            62 : ('3', 1, (0,), (3,4,9,), 0, 0, 0, 0),
            63 : ('3', 1, (0,), (7,8,9,), 0, 0, 0, 0),
            64 : ('3', 1, (0,), (3,4,8,9,), 0, 0, 0, 0),
            65 : ('3', 1, (0,), (1,4,6,9,), 0, 0, 0, 0),
            66 : ('3', 1, (0,), (1,3,5,7,9,), 0, 0, 0, 0),
            67 : ('A1', 16, (1,), (9,), 0, 2, 6, 2),
            68 : ('A1', 8, (1,), (9,), 0, 2, 6, 2),
            69 : ('A1', 4, (1,), (9,), 0, 1, 6, 2),
            70 : ('A1', 2, (1,), (9,), 0, 1, 6, 2),
            71 : ('A1', 2, (1,), (4,9,), 7, 1, 3, 2),
            72 : ('A1', 2, (1,), (7,9,), 7, 1, 3, 2),
            73 : ('A1', 2, (1,), (7,9,), 0, 1, 6, 2),
            74 : ('A1', 2, (1,), (8,9,), 0, 2, 6, 2),
            75 : ('A1', 2, (1,), (4,9,), 0, 2, 6, 2),
            76 : ('A1', 2, (1,), (2,3,4,7,8,9,), 0, 1, 6, 2),
            77 : ('A1', 1, (0,), (9,), 0, 2, 6, 2),
            78 : ('A1', 1, (0,), (9,), 7, 1, 3, 2),
            79 : ('A1', 1, (0,), (9,), 0, 1, 6, 2),
            80 : ('A1', 1, (0,), (8,9,), 0, 2, 6, 2),
            81 : ('A1', 1, (0,), (4,9,), 0, 1, 6, 2),
            82 : ('A1', 1, (0,), (7,9,), 7, 1, 3, 2),
            83 : ('A1', 1, (0,), (3,4,8,9,), 0, 1, 6, 2),
            84 : ('A1', 1, (0,), (3,4,8,9,), 0, 2, 6, 2),
            85 : ('A1', 1, (0,), (1,3,5,7,9,), 0, 1, 6, 2),
            86 : ('A1', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 7, 1, 3, 2),
            87 : ('A2', 16, (1,), (9,), 0, 2, 3, 4),
            88 : ('A2', 8, (1,), (9,), 0, 2, 3, 4),
            89 : ('A2', 4, (1,), (9,), 0, 1, 3, 4),
            90 : ('A2', 2, (1,), (7,9,), 0, 1, 3, 4),
            91 : ('A2', 2, (1,), (8,9,), 0, 2, 3, 4),
            92 : ('A2', 2, (1,), (7,9,), 9, 1, 1, 4),
            93 : ('A2', 2, (1,), (4,9,), 9, 1, 1, 4),
            94 : ('A2', 2, (1,), (4,9,), 0, 2, 3, 4),
            95 : ('A2', 2, (1,), (2,3,4,7,8,9,), 0, 1, 3, 4),
            96 : ('A2', 1, (0,), (2,), 0, 1, 3, 4),
            97 : ('A2', 1, (0,), (7,), 0, 1, 3, 4),
            98 : ('A2', 2, (1,), (9,), 0, 1, 3, 4),
            99 : ('A2', 1, (0,), (9,), 0, 2, 3, 4),
            100 : ('A2', 1, (0,), (9,), 9, 1, 1, 4),
            101 : ('A2', 1, (0,), (9,), 0, 1, 3, 4),
            102 : ('A2', 1, (0,), (2,7,), 0, 1, 3, 4),
            103 : ('A2', 1, (0,), (8,9,), 0, 2, 3, 4),
            104 : ('A2', 1, (0,), (4,9,), 0, 1, 3, 4),
            105 : ('A2', 1, (0,), (7,9,), 9, 1, 1, 4),
            106 : ('A2', 1, (0,), (3,4,8,9,), 0, 1, 3, 4),
            107 : ('A2', 1, (0,), (3,4,8,9,), 0, 2, 3, 4),
            108 : ('A2', 1, (0,), (1,3,5,7,9,), 0, 1, 3, 4),
            109 : ('A2', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 9, 1, 1, 4),
            110 : ('A3', 16, (1,), (9,), 0, 2, 2, 6),
            111 : ('A3', 8, (1,), (9,), 0, 2, 2, 6),
            112 : ('A3', 4, (1,), (9,), 0, 1, 2, 6),
            113 : ('A3', 2, (1,), (4,9,), 7, 1, 1, 6),
            114 : ('A3', 2, (1,), (7,9,), 7, 1, 1, 6),
            115 : ('A3', 2, (1,), (7,9,), 0, 1, 2, 6),
            116 : ('A3', 2, (1,), (4,9,), 0, 2, 2, 6),
            117 : ('A3', 2, (1,), (8,9,), 0, 2, 2, 6),
            118 : ('A3', 2, (1,), (2,3,4,7,8,9,), 0, 1, 2, 6),
            119 : ('A3', 1, (0,), (2,), 0, 1, 2, 6),
            120 : ('A3', 1, (0,), (7,), 0, 1, 2, 6),
            121 : ('A3', 2, (1,), (9,), 0, 1, 2, 6),
            122 : ('A3', 1, (0,), (9,), 0, 2, 2, 6),
            123 : ('A3', 1, (0,), (9,), 7, 1, 1, 6),
            124 : ('A3', 1, (0,), (9,), 0, 1, 2, 6),
            125 : ('A3', 1, (0,), (2,7,), 0, 1, 2, 6),
            126 : ('A3', 1, (0,), (8,9,), 0, 2, 2, 6),
            127 : ('A3', 1, (0,), (4,9,), 0, 1, 2, 6),
            128 : ('A3', 1, (0,), (7,9,), 7, 1, 1, 6),
            129 : ('A3', 1, (0,), (3,4,8,9,), 0, 1, 2, 6),
            130 : ('A3', 1, (0,), (3,4,8,9,), 0, 2, 2, 6),
            131 : ('A3', 1, (0,), (1,3,5,7,9,), 0, 1, 2, 6),
            132 : ('A3', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 7, 1, 1, 6),
            133 : ('B1', 4, (1,), (9,), 2, 1, 6, 2),
            134 : ('B1', 2, (1,), (9,), 2, 1, 6, 2),
            135 : ('B1', 2, (1,), (7,9,), 2, 1, 6, 2),
            136 : ('B1', 2, (1,), (4,9,), 8, 1, 3, 2),
            137 : ('B1', 2, (1,), (4,9,), 2, 2, 6, 2),
            138 : ('B1', 1, (0,), (9,), 2, 2, 6, 2),
            139 : ('B1', 1, (0,), (9,), 8, 1, 3, 2),
            140 : ('B1', 1, (0,), (9,), 2, 1, 6, 2),
            141 : ('B1', 1, (0,), (8,9,), 2, 2, 6, 2),
            142 : ('B1', 1, (0,), (4,9,), 2, 1, 6, 2),
            143 : ('B1', 1, (0,), (7,9,), 8, 1, 3, 2),
            144 : ('B1', 1, (0,), (1,3,5,7,9,), 2, 1, 6, 2),
            145 : ('B4', 16, (1,), (9,), 0, 2, 1, 12),
            146 : ('B4', 8, (1,), (9,), 0, 2, 1, 12),
            147 : ('B4', 4, (1,), (9,), 2, 1, 1, 12),
            148 : ('B4', 2, (1,), (9,), 0, 1, 1, 12),
            149 : ('B4', 2, (1,), (9,), 2, 1, 1, 12),
            150 : ('B4', 2, (1,), (7,9,), 2, 1, 1, 12),
            151 : ('B4', 2, (1,), (4,9,), 2, 1, 1, 12),
            152 : ('B4', 2, (1,), (4,9,), 0, 2, 1, 12),
            153 : ('B4', 2, (1,), (8,9,), 0, 2, 1, 12),
            154 : ('B4', 2, (1,), (2,3,4,7,8,9,), 0, 1, 1, 12),
            155 : ('B4', 1, (0,), (1,), 0, 1, 1, 12),
            156 : ('B4', 1, (0,), (2,), 0, 1, 1, 12),
            157 : ('B4', 1, (0,), (4,), 0, 1, 1, 12),
            158 : ('B4', 1, (0,), (7,), 0, 1, 1, 12),
            159 : ('B4', 1, (0,), (9,), 0, 1, 1, 12),
            160 : ('B4', 1, (0,), (9,), 2, 1, 1, 12),
            161 : ('B4', 1, (0,), (9,), 0, 2, 1, 12),
            162 : ('B4', 1, (0,), (4,9,), 2, 1, 1, 12),
            163 : ('B4', 1, (0,), (7,9,), 2, 1, 1, 12),
            164 : ('B4', 1, (0,), (8,9,), 0, 2, 1, 12),
            165 : ('B4', 1, (0,), (3,4,8,9,), 2, 1, 1, 12),
            166 : ('B4', 1, (0,), (1,3,5,7,9,), 2, 1, 1, 12),
            167 : ('B4', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 0, 2, 1, 12),
            168 : ('B4', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 2, 1, 1, 12),
            169 : ('C0', 16, (1,), (9,), 2, 2, 6, 2),
            170 : ('C0', 8, (1,), (9,), 2, 2, 6, 2),
            171 : ('C0', 4, (1,), (9,), 2, 1, 6, 2),
            172 : ('C0', 2, (1,), (9,), 2, 1, 6, 2),
            173 : ('C0', 2, (1,), (8,9,), 2, 2, 6, 2),
            174 : ('C0', 2, (1,), (7,9,), 2, 1, 6, 2),
            175 : ('C0', 2, (1,), (7,9,), 8, 1, 3, 2),
            176 : ('C0', 2, (1,), (4,9,), 8, 1, 3, 2),
            177 : ('C0', 2, (1,), (4,9,), 2, 2, 6, 2),
            178 : ('C0', 2, (1,), (2,3,4,7,8,9,), 2, 1, 6, 2),
            179 : ('C0', 1, (0,), (9,), 2, 2, 6, 2),
            180 : ('C0', 1, (0,), (9,), 8, 1, 3, 2),
            181 : ('C0', 1, (0,), (9,), 2, 1, 6, 2),
            182 : ('C0', 1, (0,), (8,9,), 2, 2, 6, 2),
            183 : ('C0', 1, (0,), (4,9,), 2, 1, 6, 2),
            184 : ('C0', 1, (0,), (7,9,), 8, 1, 3, 2),
            185 : ('C0', 1, (0,), (3,4,8,9,), 2, 1, 6, 2),
            186 : ('C0', 1, (0,), (3,4,8,9,), 2, 2, 6, 2),
            187 : ('C0', 1, (0,), (1,3,5,7,9,), 2, 1, 6, 2),
            188 : ('C0', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 8, 1, 3, 2),
            189 : ('C2', 16, (1,), (9,), 2, 2, 2, 6),
            190 : ('C2', 8, (1,), (9,), 2, 2, 2, 6),
            191 : ('C2', 4, (1,), (9,), 2, 1, 2, 6),
            192 : ('C2', 2, (1,), (9,), 2, 1, 2, 6),
            193 : ('C2', 2, (1,), (8,9,), 2, 2, 2, 6),
            194 : ('C2', 2, (1,), (7,9,), 2, 1, 2, 6),
            195 : ('C2', 2, (1,), (7,9,), 8, 1, 1, 6),
            196 : ('C2', 2, (1,), (4,9,), 8, 1, 1, 6),
            197 : ('C2', 2, (1,), (4,9,), 2, 2, 2, 6),
            198 : ('C2', 2, (1,), (2,3,4,7,8,9,), 2, 1, 2, 6),
            199 : ('C2', 8, (1,), (9,), 8, 2, 1, 6),
            200 : ('C2', 4, (1,), (9,), 8, 1, 1, 6),
            201 : ('C2', 1, (0,), (9,), 2, 2, 2, 6),
            202 : ('C2', 1, (0,), (9,), 8, 1, 1, 6),
            203 : ('C2', 1, (0,), (9,), 2, 1, 2, 6),
            204 : ('C2', 1, (0,), (8,9,), 2, 2, 2, 6),
            205 : ('C2', 1, (0,), (4,9,), 2, 1, 2, 6),
            206 : ('C2', 1, (0,), (7,9,), 8, 1, 1, 6),
            207 : ('C2', 1, (0,), (3,4,8,9,), 2, 1, 2, 6),
            208 : ('C2', 1, (0,), (3,4,8,9,), 2, 2, 2, 6),
            209 : ('C2', 1, (0,), (1,3,5,7,9,), 2, 1, 2, 6),
            210 : ('C2', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 8, 1, 1, 6),
            211 : ('A1/B1', 2, (1,), (9,), 2, 1, 6, 2),
            212 : ('A1/B1', 2, (1,), (4,9,), 8, 1, 3, 2),
            213 : ('A1/B1', 2, (1,), (7,9,), 8, 1, 3, 2),
            214 : ('A1/B1', 2, (1,), (7,9,), 2, 1, 6, 2),
            215 : ('A1/B1', 2, (1,), (4,9,), 2, 2, 6, 2),
            216 : ('A1/B1', 2, (1,), (8,9,), 2, 2, 6, 2),
            217 : ('A1/B1', 1, (0,), (9,), 2, 2, 6, 2),
            218 : ('A1/B1', 1, (0,), (9,), 8, 1, 3, 2),
            219 : ('A1/B1', 1, (0,), (9,), 2, 1, 6, 2),
            220 : ('A1/B1', 1, (0,), (8,9,), 2, 2, 6, 2),
            221 : ('A1/B1', 1, (0,), (4,9,), 2, 1, 6, 2),
            222 : ('A1/B1', 1, (0,), (7,9,), 8, 1, 3, 2),
            223 : ('A1/B1', 1, (0,), (3,4,8,9,), 2, 2, 6, 2),
            224 : ('A1/B1', 1, (0,), (1,3,5,7,9,), 2, 1, 6, 2),
            225 : ('A1/B1', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 8, 1, 3, 2),
            226 : ('A2/B2', 2, (1,), (9,), 0, 1, 3, 4),
            227 : ('A2/B2', 2, (1,), (4,9,), 6, 1, 2, 4),
            228 : ('A2/B2', 2, (1,), (7,9,), 6, 1, 2, 4),
            229 : ('A2/B2', 2, (1,), (4,9,), 0, 2, 3, 4),
            230 : ('A2/B2', 2, (1,), (8,9,), 0, 2, 3, 4),
            231 : ('A2/B2', 1, (0,), (9,), 0, 2, 3, 4),
            232 : ('A2/B2', 1, (0,), (9,), 6, 1, 2, 4),
            233 : ('A2/B2', 1, (0,), (9,), 0, 1, 3, 4),
            234 : ('A2/B2', 1, (0,), (8,9,), 0, 2, 3, 4),
            235 : ('A2/B2', 1, (0,), (4,9,), 0, 1, 3, 4),
            236 : ('A2/B2', 1, (0,), (7,9,), 6, 1, 2, 4),
            237 : ('A2/B2', 1, (0,), (3,4,8,9,), 0, 1, 3, 4),
            238 : ('A2/B2', 1, (0,), (3,4,8,9,), 0, 2, 3, 4),
            239 : ('A2/B2', 1, (0,), (1,3,5,7,9,), 0, 1, 3, 4),
            240 : ('A2/B2', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 6, 1, 2, 4),
            241 : ('A3/B3', 2, (1,), (9,), 0, 1, 2, 6),
            242 : ('A3/B3', 2, (1,), (4,9,), 2, 1, 2, 6),
            243 : ('A3/B3', 2, (1,), (7,9,), 0, 1, 2, 6),
            244 : ('A3/B3', 2, (1,), (7,9,), 2, 1, 2, 6),
            245 : ('A3/B3', 2, (1,), (4,9,), 0, 2, 2, 6),
            246 : ('A3/B3', 2, (1,), (8,9,), 0, 2, 2, 6),
            247 : ('A3/B3', 1, (0,), (9,), 0, 2, 2, 6),
            248 : ('A3/B3', 1, (0,), (9,), 2, 1, 2, 6),
            249 : ('A3/B3', 1, (0,), (9,), 0, 1, 2, 6),
            250 : ('A3/B3', 1, (0,), (8,9,), 0, 2, 2, 6),
            251 : ('A3/B3', 1, (0,), (4,9,), 0, 1, 2, 6),
            252 : ('A3/B3', 1, (0,), (7,9,), 2, 1, 2, 6),
            253 : ('A3/B3', 1, (0,), (3,4,8,9,), 0, 2, 2, 6),
            254 : ('A3/B3', 1, (0,), (1,3,5,7,9,), 0, 1, 2, 6),
            255 : ('A3/B3', 1, (0,), (0,1,2,3,4,5,6,7,8,9,), 2, 1, 2, 6),
            }
        
        #Table 6.3.3.2-4: Random access configurations for FR2 and unpaired spectrum.
        self.nrRaCfgFr2Tdd = {
            0 : ('A1', 16, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 6, 2),
            1 : ('A1', 16, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 6, 2),
            2 : ('A1', 8, (1,2,), (9,19,29,39,), 0, 2, 6, 2),
            3 : ('A1', 8, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 6, 2),
            4 : ('A1', 8, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 6, 2),
            5 : ('A1', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 6, 2),
            6 : ('A1', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 6, 2),
            7 : ('A1', 4, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 6, 2),
            8 : ('A1', 2, (1,), (7,15,23,31,39,), 0, 2, 6, 2),
            9 : ('A1', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 6, 2),
            10 : ('A1', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 6, 2),
            11 : ('A1', 2, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 6, 2),
            12 : ('A1', 1, (0,), (19,39,), 7, 1, 3, 2),
            13 : ('A1', 1, (0,), (3,5,7,), 0, 1, 6, 2),
            14 : ('A1', 1, (0,), (24,29,34,39,), 7, 1, 3, 2),
            15 : ('A1', 1, (0,), (9,19,29,39,), 7, 2, 3, 2),
            16 : ('A1', 1, (0,), (17,19,37,39,), 0, 1, 6, 2),
            17 : ('A1', 1, (0,), (9,19,29,39,), 0, 2, 6, 2),
            18 : ('A1', 1, (0,), (4,9,14,19,24,29,34,39,), 0, 1, 6, 2),
            19 : ('A1', 1, (0,), (4,9,14,19,24,29,34,39,), 7, 1, 3, 2),
            20 : ('A1', 1, (0,), (3,5,7,9,11,13,), 7, 1, 3, 2),
            21 : ('A1', 1, (0,), (23,27,31,35,39,), 7, 1, 3, 2),
            22 : ('A1', 1, (0,), (7,15,23,31,39,), 0, 1, 6, 2),
            23 : ('A1', 1, (0,), (23,27,31,35,39,), 0, 1, 6, 2),
            24 : ('A1', 1, (0,), (13,14,15, 29,30,31,37,38,39,), 7, 2, 3, 2),
            25 : ('A1', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 7, 1, 3, 2),
            26 : ('A1', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 6, 2),
            27 : ('A1', 1, (0,), tuple(range(1,40,2)), 0, 1, 6, 2),
            28 : ('A1', 1, (0,), tuple(range(40)), 7, 1, 3, 2),
            29 : ('A2', 16, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 3, 4),
            30 : ('A2', 16, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 3, 4),
            31 : ('A2', 8, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 3, 4),
            32 : ('A2', 8, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 3, 4),
            33 : ('A2', 8, (1,2,), (9,19,29,39,), 0, 2, 3, 4),
            34 : ('A2', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 3, 4),
            35 : ('A2', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 3, 4),
            36 : ('A2', 4, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 3, 4),
            37 : ('A2', 2, (1,), (7,15,23,31,39,), 0, 2, 3, 4),
            38 : ('A2', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 3, 4),
            39 : ('A2', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 3, 4),
            40 : ('A2', 2, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 3, 4),
            41 : ('A2', 1, (0,), (19,39,), 5, 1, 2, 4),
            42 : ('A2', 1, (0,), (3,5,7,), 0, 1, 3, 4),
            43 : ('A2', 1, (0,), (24,29,34,39,), 5, 1, 2, 4),
            44 : ('A2', 1, (0,), (9,19,29,39,), 5, 2, 2, 4),
            45 : ('A2', 1, (0,), (17,19,37,39,), 0, 1, 3, 4),
            46 : ('A2', 1, (0,), (9, 19, 29, 39,), 0, 2, 3, 4),
            47 : ('A2', 1, (0,), (7,15,23,31,39,), 0, 1, 3, 4),
            48 : ('A2', 1, (0,), (23,27,31,35,39,), 5, 1, 2, 4),
            49 : ('A2', 1, (0,), (23,27,31,35,39,), 0, 1, 3, 4),
            50 : ('A2', 1, (0,), (3,5,7,9,11,13,), 5, 1, 2, 4),
            51 : ('A2', 1, (0,), (3,5,7,9,11,13,), 0, 1, 3, 4),
            52 : ('A2', 1, (0,), (4,9,14,19,24,29,34,39,), 5, 1, 2, 4),
            53 : ('A2', 1, (0,), (4,9,14,19,24,29,34,39,), 0, 1, 3, 4),
            54 : ('A2', 1, (0,), (13,14,15, 29,30,31,37,38,39,), 5, 2, 2, 4),
            55 : ('A2', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 5, 1, 2, 4),
            56 : ('A2', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 3, 4),
            57 : ('A2', 1, (0,), tuple(range(1,40,2)), 0, 1, 3, 4),
            58 : ('A2', 1, (0,), tuple(range(40)), 5, 1, 2, 4),
            59 : ('A3', 16, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 2, 6),
            60 : ('A3', 16, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 2, 6),
            61 : ('A3', 8, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 2, 6),
            62 : ('A3', 8, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 2, 6),
            63 : ('A3', 8, (1,2,), (9,19,29,39,), 0, 2, 2, 6),
            64 : ('A3', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 2, 6),
            65 : ('A3', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 2, 6),
            66 : ('A3', 4, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 2, 6),
            67 : ('A3', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 2, 6),
            68 : ('A3', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 2, 6),
            69 : ('A3', 2, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 2, 6),
            70 : ('A3', 1, (0,), (19,39,), 7, 1, 1, 6),
            71 : ('A3', 1, (0,), (3,5,7,), 0, 1, 2, 6),
            72 : ('A3', 1, (0,), (9,11,13,), 2, 1, 2, 6),
            73 : ('A3', 1, (0,), (24,29,34,39,), 7, 1, 1, 6),
            74 : ('A3', 1, (0,), (9,19,29,39,), 7, 2, 1, 6),
            75 : ('A3', 1, (0,), (17,19,37,39,), 0, 1, 2, 6),
            76 : ('A3', 1, (0,), (9,19,29,39,), 0, 2, 2, 6),
            77 : ('A3', 1, (0,), (7,15,23,31,39,), 0, 1, 2, 6),
            78 : ('A3', 1, (0,), (23,27,31,35,39,), 7, 1, 1, 6),
            79 : ('A3', 1, (0,), (23,27,31,35,39,), 0, 1, 2, 6),
            80 : ('A3', 1, (0,), (3,5,7,9,11,13,), 0, 1, 2, 6),
            81 : ('A3', 1, (0,), (3,5,7,9,11,13,), 7, 1, 1, 6),
            82 : ('A3', 1, (0,), (4,9,14,19,24,29,34,39,), 0, 1, 2, 6),
            83 : ('A3', 1, (0,), (4,9,14,19,24,29,34,39,), 7, 1, 1, 6),
            84 : ('A3', 1, (0,), (13,14,15, 29,30,31,37,38,39,), 7, 2, 1, 6),
            85 : ('A3', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 7, 1, 1, 6),
            86 : ('A3', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 2, 6),
            87 : ('A3', 1, (0,), tuple(range(1,40,2)), 0, 1, 2, 6),
            88 : ('A3', 1, (0,), tuple(range(40)), 7, 1, 1, 6),
            89 : ('B1', 16, (1,), (4,9,14,19,24,29,34,39,), 2, 2, 6, 2),
            90 : ('B1', 8, (1,), (4,9,14,19,24,29,34,39,), 2, 2, 6, 2),
            91 : ('B1', 8, (1,2,), (9,19,29,39,), 2, 2, 6, 2),
            92 : ('B1', 4, (1,), (4,9,14,19,24,29,34,39,), 2, 2, 6, 2),
            93 : ('B1', 2, (1,), (4,9,14,19,24,29,34,39,), 2, 2, 6, 2),
            94 : ('B1', 2, (1,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 6, 2),
            95 : ('B1', 1, (0,), (19,39,), 8, 1, 3, 2),
            96 : ('B1', 1, (0,), (3,5,7,), 2, 1, 6, 2),
            97 : ('B1', 1, (0,), (24,29,34,39,), 8, 1, 3, 2),
            98 : ('B1', 1, (0,), (9,19,29,39,), 8, 2, 3, 2),
            99 : ('B1', 1, (0,), (17,19,37,39,), 2, 1, 6, 2),
            100 : ('B1', 1, (0,), (9,19,29,39,), 2, 2, 6, 2),
            101 : ('B1', 1, (0,), (7,15,23,31,39,), 2, 1, 6, 2),
            102 : ('B1', 1, (0,), (23,27,31,35,39,), 8, 1, 3, 2),
            103 : ('B1', 1, (0,), (23,27,31,35,39,), 2, 1, 6, 2),
            104 : ('B1', 1, (0,), (3,5,7,9,11,13,), 8, 1, 3, 2),
            105 : ('B1', 1, (0,), (4,9,14,19,24,29,34,39,), 8, 1, 3, 2),
            106 : ('B1', 1, (0,), (4,9,14,19,24,29,34,39,), 2, 1, 6, 2),
            107 : ('B1', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 8, 1, 3, 2),
            108 : ('B1', 1, (0,), (13,14,15, 29,30,31,37,38,39,), 8, 2, 3, 2),
            109 : ('B1', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 6, 2),
            110 : ('B1', 1, (0,), tuple(range(1,40,2)), 2, 1, 6, 2),
            111 : ('B1', 1, (0,), tuple(range(40)), 8, 1, 3, 2),
            112 : ('B4', 16, (1,2,), (4,9,14,19,24,29,34,39,), 0, 2, 1, 12),
            113 : ('B4', 16, (1,2,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 1, 12),
            114 : ('B4', 8, (1,2,), (4,9,14,19,24,29,34,39,), 0, 2, 1, 12),
            115 : ('B4', 8, (1,2,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 1, 12),
            116 : ('B4', 8, (1,2,), (9,19,29,39,), 0, 2, 1, 12),
            117 : ('B4', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 1, 12),
            118 : ('B4', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 1, 12),
            119 : ('B4', 4, (1,2,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 1, 12),
            120 : ('B4', 2, (1,), (7,15,23,31,39,), 2, 2, 1, 12),
            121 : ('B4', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 1, 12),
            122 : ('B4', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 1, 12),
            123 : ('B4', 2, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 1, 12),
            124 : ('B4', 1, (0,), (19, 39,), 2, 2, 1, 12),
            125 : ('B4', 1, (0,), (17, 19, 37, 39,), 0, 1, 1, 12),
            126 : ('B4', 1, (0,), (24,29,34,39,), 2, 1, 1, 12),
            127 : ('B4', 1, (0,), (9,19,29,39,), 2, 2, 1, 12),
            128 : ('B4', 1, (0,), (9,19,29,39,), 0, 2, 1, 12),
            129 : ('B4', 1, (0,), (7,15,23,31,39,), 0, 1, 1, 12),
            130 : ('B4', 1, (0,), (7,15,23,31,39,), 0, 2, 1, 12),
            131 : ('B4', 1, (0,), (23,27,31,35,39,), 0, 1, 1, 12),
            132 : ('B4', 1, (0,), (23,27,31,35,39,), 2, 2, 1, 12),
            133 : ('B4', 1, (0,), (9,11,13,15,17,19,), 0, 1, 1, 12),
            134 : ('B4', 1, (0,), (3,5,7,9,11,13,), 2, 1, 1, 12),
            135 : ('B4', 1, (0,), (4,9,14,19,24,29,34,39,), 0, 1, 1, 12),
            136 : ('B4', 1, (0,), (4,9,14,19,24,29,34,39,), 2, 2, 1, 12),
            137 : ('B4', 1, (0,), (13,14,15, 29,30,31,37,38,39,), 2, 2, 1, 12),
            138 : ('B4', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 1, 12),
            139 : ('B4', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 1, 12),
            140 : ('B4', 1, (0,), tuple(range(3,26,2)), 2, 1, 1, 12),
            141 : ('B4', 1, (0,), tuple(range(3,26,2)), 0, 2, 1, 12),
            142 : ('B4', 1, (0,), tuple(range(1,40,2)), 0, 1, 1, 12),
            143 : ('B4', 1, (0,), tuple(range(40)), 2, 1, 1, 12),
            144 : ('C0', 16, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 7, 2),
            145 : ('C0', 16, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 7, 2),
            146 : ('C0', 8, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 7, 2),
            147 : ('C0', 8, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 7, 2),
            148 : ('C0', 8, (1,2,), (9,19,29,39,), 0, 2, 7, 2),
            149 : ('C0', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 7, 2),
            150 : ('C0', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 7, 2),
            151 : ('C0', 4, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 7, 2),
            152 : ('C0', 2, (1,), (7,15,23,31,39,), 0, 2, 7, 2),
            153 : ('C0', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 7, 2),
            154 : ('C0', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 7, 2),
            155 : ('C0', 2, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 7, 2),
            156 : ('C0', 1, (0,), (19,39,), 8, 1, 3, 2),
            157 : ('C0', 1, (0,), (3,5,7,), 0, 1, 7, 2),
            158 : ('C0', 1, (0,), (24,29,34,39,), 8, 1, 3, 2),
            159 : ('C0', 1, (0,), (9,19,29,39,), 8, 2, 3, 2),
            160 : ('C0', 1, (0,), (17,19,37,39,), 0, 1, 7, 2),
            161 : ('C0', 1, (0,), (9,19,29,39,), 0, 2, 7, 2),
            162 : ('C0', 1, (0,), (23,27,31,35,39,), 8, 1, 3, 2),
            163 : ('C0', 1, (0,), (7,15,23,31,39,), 0, 1, 7, 2),
            164 : ('C0', 1, (0,), (23,27,31,35,39,), 0, 1, 7, 2),
            165 : ('C0', 1, (0,), (3,5,7,9,11,13,), 8, 1, 3, 2),
            166 : ('C0', 1, (0,), (4,9,14,19,24,29,34,39,), 8, 1, 3, 2),
            167 : ('C0', 1, (0,), (4,9,14,19,24,29,34,39,), 0, 1, 7, 2),
            168 : ('C0', 1, (0,), (13,14,15, 29,30,31,37,38,39,), 8, 2, 3, 2),
            169 : ('C0', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 8, 1, 3, 2),
            170 : ('C0', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 7, 2),
            171 : ('C0', 1, (0,), tuple(range(1,40,2)), 0, 1, 7, 2),
            172 : ('C0', 1, (0,), tuple(range(40)), 8, 1, 3, 2),
            173 : ('C2', 16, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 2, 6),
            174 : ('C2', 16, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 2, 6),
            175 : ('C2', 8, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 2, 6),
            176 : ('C2', 8, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 2, 6),
            177 : ('C2', 8, (1,2,), (9,19,29,39,), 0, 2, 2, 6),
            178 : ('C2', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 2, 6),
            179 : ('C2', 4, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 2, 6),
            180 : ('C2', 4, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 2, 6),
            181 : ('C2', 2, (1,), (7,15,23,31,39,), 2, 2, 2, 6),
            182 : ('C2', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 1, 2, 6),
            183 : ('C2', 2, (1,), (4,9,14,19,24,29,34,39,), 0, 2, 2, 6),
            184 : ('C2', 2, (1,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 2, 6),
            185 : ('C2', 1, (0,), (19,39,), 2, 1, 2, 6),
            186 : ('C2', 1, (0,), (3,5,7,), 0, 1, 2, 6),
            187 : ('C2', 1, (0,), (24,29,34,39,), 7, 1, 1, 6),
            188 : ('C2', 1, (0,), (9,19,29,39,), 7, 2, 1, 6),
            189 : ('C2', 1, (0,), (17,19,37,39,), 0, 1, 2, 6),
            190 : ('C2', 1, (0,), (9,19,29,39,), 2, 2, 2, 6),
            191 : ('C2', 1, (0,), (7,15,23,31,39,), 2, 1, 2, 6),
            192 : ('C2', 1, (0,), (3,5,7,9,11,13,), 7, 1, 1, 6),
            193 : ('C2', 1, (0,), (23,27,31,35,39,), 7, 2, 1, 6),
            194 : ('C2', 1, (0,), (23,27,31,35,39,), 0, 1, 2, 6),
            195 : ('C2', 1, (0,), (4,9,14,19,24,29,34,39,), 7, 2, 1, 6),
            196 : ('C2', 1, (0,), (4,9,14,19,24,29,34,39,), 2, 1, 2, 6),
            197 : ('C2', 1, (0,), (13,14,15, 29,30,31,37,38,39,), 7, 2, 1, 6),
            198 : ('C2', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 7, 1, 1, 6),
            199 : ('C2', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 0, 1, 2, 6),
            200 : ('C2', 1, (0,), tuple(range(1,40,2)), 0, 1, 2, 6),
            201 : ('C2', 1, (0,), tuple(range(40)), 7, 1, 1, 6),
            202 : ('A1/B1', 16, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 6, 2),
            203 : ('A1/B1', 16, (1,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 6, 2),
            204 : ('A1/B1', 8, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 6, 2),
            205 : ('A1/B1', 8, (1,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 6, 2),
            206 : ('A1/B1', 4, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 6, 2),
            207 : ('A1/B1', 4, (1,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 6, 2),
            208 : ('A1/B1', 2, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 6, 2),
            209 : ('A1/B1', 1, (0,), (19,39,), 8, 1, 3, 2),
            210 : ('A1/B1', 1, (0,), (9,19,29,39,), 8, 1, 3, 2),
            211 : ('A1/B1', 1, (0,), (17,19,37,39,), 2, 1, 6, 2),
            212 : ('A1/B1', 1, (0,), (9,19,29,39,), 2, 2, 6, 2),
            213 : ('A1/B1', 1, (0,), (23,27,31,35,39,), 8, 1, 3, 2),
            214 : ('A1/B1', 1, (0,), (7,15,23,31,39,), 2, 1, 6, 2),
            215 : ('A1/B1', 1, (0,), (23,27,31,35,39,), 2, 1, 6, 2),
            216 : ('A1/B1', 1, (0,), (4,9,14,19,24,29,34,39,), 8, 1, 3, 2),
            217 : ('A1/B1', 1, (0,), (4,9,14,19,24,29,34,39,), 2, 1, 6, 2),
            218 : ('A1/B1', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 6, 2),
            219 : ('A1/B1', 1, (0,), tuple(range(1,40,2)), 2, 1, 6, 2),
            220 : ('A2/B2', 16, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 3, 4),
            221 : ('A2/B2', 16, (1,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 3, 4),
            222 : ('A2/B2', 8, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 3, 4),
            223 : ('A2/B2', 8, (1,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 3, 4),
            224 : ('A2/B2', 4, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 3, 4),
            225 : ('A2/B2', 4, (1,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 3, 4),
            226 : ('A2/B2', 2, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 3, 4),
            227 : ('A2/B2', 1, (0,), (19,39,), 6, 1, 2, 4),
            228 : ('A2/B2', 1, (0,), (9,19,29,39,), 6, 1, 2, 4),
            229 : ('A2/B2', 1, (0,), (17,19,37,39,), 2, 1, 3, 4),
            230 : ('A2/B2', 1, (0,), (9,19,29,39,), 2, 2, 3, 4),
            231 : ('A2/B2', 1, (0,), (23,27,31,35,39,), 6, 1, 2, 4),
            232 : ('A2/B2', 1, (0,), (7,15,23,31,39,), 2, 1, 3, 4),
            233 : ('A2/B2', 1, (0,), (23,27,31,35,39,), 2, 1, 3, 4),
            234 : ('A2/B2', 1, (0,), (4,9,14,19,24,29,34,39,), 6, 1, 2, 4),
            235 : ('A2/B2', 1, (0,), (4,9,14,19,24,29,34,39,), 2, 1, 3, 4),
            236 : ('A2/B2', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 3, 4),
            237 : ('A2/B2', 1, (0,), tuple(range(1,40,2)), 2, 1, 3, 4),
            238 : ('A3/B3', 16, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 2, 6),
            239 : ('A3/B3', 16, (1,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 2, 6),
            240 : ('A3/B3', 8, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 2, 6),
            241 : ('A3/B3', 8, (1,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 2, 6),
            242 : ('A3/B3', 4, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 2, 6),
            243 : ('A3/B3', 4, (1,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 2, 6),
            244 : ('A3/B3', 2, (1,), (4,9,14,19,24,29,34,39,), 2, 1, 2, 6),
            245 : ('A3/B3', 1, (0,), (19,39,), 2, 1, 2, 6),
            246 : ('A3/B3', 1, (0,), (9,19,29,39,), 2, 1, 2, 6),
            247 : ('A3/B3', 1, (0,), (17,19,37,39,), 2, 1, 2, 6),
            248 : ('A3/B3', 1, (0,), (9,19,29,39,), 2, 2, 2, 6),
            249 : ('A3/B3', 1, (0,), (7,15,23,31,39,), 2, 1, 2, 6),
            250 : ('A3/B3', 1, (0,), (23,27,31,35,39,), 2, 1, 2, 6),
            251 : ('A3/B3', 1, (0,), (23,27,31,35,39,), 2, 2, 2, 6),
            252 : ('A3/B3', 1, (0,), (4,9,14,19,24,29,34,39,), 2, 1, 2, 6),
            253 : ('A3/B3', 1, (0,), (4,9,14,19,24,29,34,39,), 2, 2, 2, 6),
            254 : ('A3/B3', 1, (0,), (3,7,11,15,19,23,27,31,35,39,), 2, 1, 2, 6),
            255 : ('A3/B3', 1, (0,), tuple(range(1,40,2)), 2, 1, 2, 6),
            }
        
        #refer to 3GPP 38.214 vf30
        #Table 5.1.2.1.1-2: Default PDSCH time domain resource allocation A for normal CP
        self.nrPdschTimeAllocDefANormCp = {
            '1_2' : ('Type A', 0, 2, 12),
            '1_3' : ('Type A', 0, 3, 11),
            '2_2' : ('Type A', 0, 2, 10),
            '2_3' : ('Type A', 0, 3, 9),
            '3_2' : ('Type A', 0, 2, 9),
            '3_3' : ('Type A', 0, 3, 8),
            '4_2' : ('Type A', 0, 2, 7),
            '4_3' : ('Type A', 0, 3, 6),
            '5_2' : ('Type A', 0, 2, 5),
            '5_3' : ('Type A', 0, 3, 4),
            '6_2' : ('Type B', 0, 9, 4),
            '6_3' : ('Type B', 0, 10, 4),
            '7_2' : ('Type B', 0, 4, 4),
            '7_3' : ('Type B', 0, 6, 4),
            '8_2' : ('Type B', 0, 5, 7),
            '9_2' : ('Type B', 0, 5, 2),
            '10_2' : ('Type B', 0, 9, 2),
            '11_2' : ('Type B', 0, 12, 2),
            '12_2' : ('Type A', 0, 1, 13),
            '13_2' : ('Type A', 0, 1, 6),
            '14_2' : ('Type A', 0, 2, 4),
            '15_2' : ('Type B', 0, 4, 7),
            '16_2' : ('Type B', 0, 8, 4),
            '8_3' : ('Type B', 0, 5, 7),
            '9_3' : ('Type B', 0, 5, 2),
            '10_3' : ('Type B', 0, 9, 2),
            '11_3' : ('Type B', 0, 12, 2),
            '12_3' : ('Type A', 0, 1, 13),
            '13_3' : ('Type A', 0, 1, 6),
            '14_3' : ('Type A', 0, 2, 4),
            '15_3' : ('Type B', 0, 4, 7),
            '16_3' : ('Type B', 0, 8, 4),
            }
        
        #Table 5.1.2.1.1-3: Default PDSCH time domain resource allocation A for extended CP
        self.nrPdschTimeAllocDefAExtCp = {
            '1_2' : ('Type A', 0, 2, 6),
            '1_3' : ('Type A', 0, 3, 5),
            '2_2' : ('Type A', 0, 2, 10),
            '1_3' : ('Type A', 0, 3, 9),
            '3_2' : ('Type A', 0, 2, 9),
            '3_3' : ('Type A', 0, 3, 8),
            '4_2' : ('Type A', 0, 2, 7),
            '4_3' : ('Type A', 0, 3, 6),
            '5_2' : ('Type A', 0, 2, 5),
            '5_3' : ('Type A', 0, 3, 4),
            '6_2' : ('Type B', 0, 6, 4),
            '6_3' : ('Type B', 0, 8, 2),
            '7_2' : ('Type B', 0, 4, 4),
            '7_3' : ('Type B', 0, 6, 4),
            '8_2' : ('Type B', 0, 5, 6),
            '9_2' : ('Type B', 0, 5, 2),
            '10_2' : ('Type B', 0, 9, 2),
            '11_2' : ('Type B', 0, 10, 2),
            '12_2' : ('Type A', 0, 1, 11),
            '13_2' : ('Type A', 0, 1, 6),
            '14_2' : ('Type A', 0, 2, 4),
            '15_2' : ('Type B', 0, 4, 6),
            '16_2' : ('Type B', 0, 8, 4),
            '8_3' : ('Type B', 0, 5, 6),
            '9_3' : ('Type B', 0, 5, 2),
            '10_3' : ('Type B', 0, 9, 2),
            '11_3' : ('Type B', 0, 10, 2),
            '12_3' : ('Type A', 0, 1, 11),
            '13_3' : ('Type A', 0, 1, 6),
            '14_3' : ('Type A', 0, 2, 4),
            '15_3' : ('Type B', 0, 4, 6),
            '16_3' : ('Type B', 0, 8, 4),
            }
        
        #Table 5.1.2.1.1-4: Default PDSCH time domain resource allocation B
        self.nrPdschTimeAllocDefB = {
            '1_2' : ('Type B', 0, 2, 2),
            '2_2' : ('Type B', 0, 4, 2),
            '3_2' : ('Type B', 0, 6, 2),
            '4_2' : ('Type B', 0, 8, 2),
            '5_2' : ('Type B', 0, 10, 2),
            '6_2' : ('Type B', 1, 2, 2),
            '7_2' : ('Type B', 1, 4, 2),
            '8_2' : ('Type B', 0, 2, 4),
            '9_2' : ('Type B', 0, 4, 4),
            '10_2' : ('Type B', 0, 6, 4),
            '11_2' : ('Type B', 0, 8, 4),
            '12_2' : ('Type B', 0, 10, 4),
            '13_2' : ('Type B', 0, 2, 7),
            '14_2' : ('Type A', 0, 2, 12),
            '14_3' : ('Type A', 0, 3, 11),
            '15_2' : ('Type B', 1, 2, 4),
            '1_3' : ('Type B', 0, 2, 2),
            '2_3' : ('Type B', 0, 4, 2),
            '3_3' : ('Type B', 0, 6, 2),
            '4_3' : ('Type B', 0, 8, 2),
            '5_3' : ('Type B', 0, 10, 2),
            '6_3' : ('Type B', 1, 2, 2),
            '7_3' : ('Type B', 1, 4, 2),
            '8_3' : ('Type B', 0, 2, 4),
            '9_3' : ('Type B', 0, 4, 4),
            '10_3' : ('Type B', 0, 6, 4),
            '11_3' : ('Type B', 0, 8, 4),
            '12_3' : ('Type B', 0, 10, 4),
            '13_3' : ('Type B', 0, 2, 7),
            '15_3' : ('Type B', 1, 2, 4),
            }
        #Note 1: If the PDSCH was scheduled with SI-RNTI in PDCCH Type0 common search space, the UE may assume that this PDSCH resource allocation is not applied
        self.nrPdschTimeAllocDefBNote1Set = [12, 13, 14]
        
        #Table 5.1.2.1.1-5: Default PDSCH time domain resource allocation C
        self.nrPdschTimeAllocDefC = {
            '1_2' : ('Type B', 0, 2, 2),
            '2_2' : ('Type B', 0, 4, 2),
            '3_2' : ('Type B', 0, 6, 2),
            '4_2' : ('Type B', 0, 8, 2),
            '5_2' : ('Type B', 0, 10, 2),
            '8_2' : ('Type B', 0, 2, 4),
            '9_2' : ('Type B', 0, 4, 4),
            '10_2' : ('Type B', 0, 6, 4),
            '11_2' : ('Type B', 0, 8, 4),
            '12_2' : ('Type B', 0, 10, 4),
            '13_2' : ('Type B', 0, 2, 7),
            '14_2' : ('Type A', 0, 2, 12),
            '14_3' : ('Type A', 0, 3, 11),
            '15_2' : ('Type A', 0, 0, 6),
            '16_2' : ('Type A', 0, 2, 6),
            '1_3' : ('Type B', 0, 2, 2),
            '2_3' : ('Type B', 0, 4, 2),
            '3_3' : ('Type B', 0, 6, 2),
            '4_3' : ('Type B', 0, 8, 2),
            '5_3' : ('Type B', 0, 10, 2),
            '8_3' : ('Type B', 0, 2, 4),
            '9_3' : ('Type B', 0, 4, 4),
            '10_3' : ('Type B', 0, 6, 4),
            '11_3' : ('Type B', 0, 8, 4),
            '12_3' : ('Type B', 0, 10, 4),
            '13_3' : ('Type B', 0, 2, 7),
            '15_3' : ('Type A', 0, 0, 6),
            '16_3' : ('Type A', 0, 2, 6),
            }
        #Note 1: The UE may assume that this PDSCH resource allocation is not used, if the PDSCH was scheduled with SI-RNTI in PDCCH Type0 common search space
        self.nrPdschTimeAllocDefCNote1Set = [1, 13, 14, 15, 16]
        
        #refer to 3GPP 38.214 vf30
        #Table 6.1.2.1.1-2: Default PUSCH time domain resource allocation A for normal CP
        self.nrPuschTimeAllocDefANormCp = {
            1 : ('Type A',0,0,14),
            2 : ('Type A',0,0,12),
            3 : ('Type A',0,0,10),
            4 : ('Type B',0,2,10),
            5 : ('Type B',0,4,10),
            6 : ('Type B',0,4,8),
            7 : ('Type B',0,4,6),
            8 : ('Type A',1,0,14),
            9 : ('Type A',1,0,12),
            10 : ('Type A',1,0,10),
            11 : ('Type A',2,0,14),
            12 : ('Type A',2,0,12),
            13 : ('Type A',2,0,10),
            14 : ('Type B',0,8,6),
            15 : ('Type A',3,0,14),
            16 : ('Type A',3,0,10),
            }
        
        #Table 6.1.2.1.1-3: Default PUSCH time domain resource allocation A for extended CP
        self.nrPuschTimeAllocDefAExtCp = {
            1 : ('Type A',0,0,8),
            2 : ('Type A',0,0,12),
            3 : ('Type A',0,0,10),
            4 : ('Type B',0,2,10),
            5 : ('Type B',0,4,4),
            6 : ('Type B',0,4,8),
            7 : ('Type B',0,4,6),
            8 : ('Type A',1,0,8),
            9 : ('Type A',1,0,12),
            10 : ('Type A',1,0,10),
            11 : ('Type A',2,0,6),
            12 : ('Type A',2,0,12),
            13 : ('Type A',2,0,10),
            14 : ('Type B',0,8,4),
            15 : ('Type A',3,0,8),
            16 : ('Type A',3,0,10),
            }
        
        #Table 6.1.2.1.1-4: Definition of value j
        self.nrPuschTimeAllocK2j = { '15KHz':1, '30KHz':1, '60KHz':2, '120KHz':3 }
        
        #Table 6.1.2.1.1-5: Definition of value Δ
        self.nrPuschTimeAllocMsg3K2Delta = { '15KHz':2, '30KHz':3, '60KHz':4, '120KHz':6 }
        
        #refer to 3GPP 38.214 vf30
        #Table 5.1.3.1-1: MCS index table 1 for PDSCH
        self.nrPdschMcsTabQam64 = {
            0 : (2,120),
            1 : (2,157),
            2 : (2,193),
            3 : (2,251),
            4 : (2,308),
            5 : (2,379),
            6 : (2,449),
            7 : (2,526),
            8 : (2,602),
            9 : (2,679),
            10 : (4,340),
            11 : (4,378),
            12 : (4,434),
            13 : (4,490),
            14 : (4,553),
            15 : (4,616),
            16 : (4,658),
            17 : (6,438),
            18 : (6,466),
            19 : (6,517),
            20 : (6,567),
            21 : (6,616),
            22 : (6,666),
            23 : (6,719),
            24 : (6,772),
            25 : (6,822),
            26 : (6,873),
            27 : (6,910),
            28 : (6,948),
            29 : None,
            30 : None,
            31 : None,
            }
        
        #Table 5.1.3.1-2: MCS index table 2 for PDSCH
        self.nrPdschMcsTabQam256 = {
            0 : (2,120),
            1 : (2,193),
            2 : (2,308),
            3 : (2,449),
            4 : (2,602),
            5 : (4,378),
            6 : (4,434),
            7 : (4,490),
            8 : (4,553),
            9 : (4,616),
            10 : (4,658),
            11 : (6,466),
            12 : (6,517),
            13 : (6,567),
            14 : (6,616),
            15 : (6,666),
            16 : (6,719),
            17 : (6,772),
            18 : (6,822),
            19 : (6,873),
            20 : (8,682.5),
            21 : (8,711),
            22 : (8,754),
            23 : (8,797),
            24 : (8,841),
            25 : (8,885),
            26 : (8,916.5),
            27 : (8,948),
            28 : None,
            29 : None,
            30 : None,
            31 : None,
            }
        
        #Table 5.1.3.1-3: MCS index table 3 for PDSCH
        self.nrPdschMcsTabQam64LowSE = {
            0 : (2,30),
            1 : (2,40),
            2 : (2,50),
            3 : (2,64),
            4 : (2,78),
            5 : (2,99),
            6 : (2,120),
            7 : (2,157),
            8 : (2,193),
            9 : (2,251),
            10 : (2,308),
            11 : (2,379),
            12 : (2,449),
            13 : (2,526),
            14 : (2,602),
            15 : (4,340),
            16 : (4,378),
            17 : (4,434),
            18 : (4,490),
            19 : (4,553),
            20 : (4,616),
            21 : (6,438),
            22 : (6,466),
            23 : (6,517),
            24 : (6,567),
            25 : (6,616),
            26 : (6,666),
            27 : (6,719),
            28 : (6,772),
            29 : None,
            30 : None,
            31 : None,
            }

        #Table 5.1.3.2-1: TBS for N_info <= 3824
        self.nrTbsTabLessThan3824 = [24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 208, 224, 240, 256, 272, 288, 304, 320, 336, 352, 368, 384, 408, 432, 456, 480, 504, 528, 552, 576, 608, 640, 672, 704, 736, 768, 808, 848, 888, 928, 984, 1032, 1064, 1128, 1160, 1192, 1224, 1256, 1288, 1320, 1352, 1416, 1480, 1544, 1608, 1672, 1736, 1800, 1864, 1928, 2024, 2088, 2152, 2216, 2280, 2408, 2472, 2536, 2600, 2664, 2728, 2792, 2856, 2976, 3104, 3240, 3368, 3496, 3624, 3752, 3824,]
        
        #Table 6.1.4.1-1: MCS index table for PUSCH with transform precoding and 64QAM
        self.nrPuschTpMcsTabQam64 = {
            0 : (2,120),
            1 : (2,157),
            2 : (2,193),
            3 : (2,251),
            4 : (2,308),
            5 : (2,379),
            6 : (2,449),
            7 : (2,526),
            8 : (2,602),
            9 : (2,679),
            10 : (4,340),
            11 : (4,378),
            12 : (4,434),
            13 : (4,490),
            14 : (4,553),
            15 : (4,616),
            16 : (4,658),
            17 : (6,466),
            18 : (6,517),
            19 : (6,567),
            20 : (6,616),
            21 : (6,666),
            22 : (6,719),
            23 : (6,772),
            24 : (6,822),
            25 : (6,873),
            26 : (6,910),
            27 : (6,948),
            28 : None,
            29 : None,
            30 : None,
            31 : None,
            }
        
        #Table 6.1.4.1-2: MCS index table 2 for PUSCH with transform precoding and 64QAM
        self.nrPuschTpMcsTabQam64LowSE = {
            0 : (2,30),
            1 : (2,40),
            2 : (2,50),
            3 : (2,64),
            4 : (2,78),
            5 : (2,99),
            6 : (2,120),
            7 : (2,157),
            8 : (2,193),
            9 : (2,251),
            10 : (2,308),
            11 : (2,379),
            12 : (2,449),
            13 : (2,526),
            14 : (2,602),
            15 : (2,679),
            16 : (4,378),
            17 : (4,434),
            18 : (4,490),
            19 : (4,553),
            20 : (4,616),
            21 : (4,658),
            22 : (4,699),
            23 : (4,772),
            24 : (6,567),
            25 : (6,616),
            26 : (6,666),
            27 : (6,772),
            28 : None,
            29 : None,
            30 : None,
            31 : None,
            }
            
        #refer to 3GPP 38.212 vf30
        #Table 7.3.1.2.2-1: Antenna port(s) (1000 + DMRS port), dmrs-Type=1, maxLength=1
        self.nrDci11AntPortsDmrsType1MaxLen1OneCw = {
            0 : (1,(0,),1),
            1 : (1,(1,),1),
            2 : (1,(0,1,),1),
            3 : (2,(0,),1),
            4 : (2,(1,),1),
            5 : (2,(2,),1),
            6 : (2,(3,),1),
            7 : (2,(0,1,),1),
            8 : (2,(2,3,),1),
            9 : (2,(0,1,2,),1),
            10 : (2,(0,1,2,3,),1),
            11 : (2,(0,2,),1),
            12 : None,
            13 : None,
            14 : None,
            15 : None,
            }
        self.nrDci11AntPortsDmrsType1MaxLen1OneCwValid = '0-11'
        
        #Table 7.3.1.2.2-2: Antenna port(s) (1000 + DMRS port), dmrs-Type=1, maxLength=2
        self.nrDci11AntPortsDmrsType1MaxLen2OneCw = {
            0 : (1,(0,),1),
            1 : (1,(1,),1),
            2 : (1,(0,1,),1),
            3 : (2,(0,),1),
            4 : (2,(1,),1),
            5 : (2,(2,),1),
            6 : (2,(3,),1),
            7 : (2,(0,1,),1),
            8 : (2,(2,3,),1),
            9 : (2,(0,1,2,),1),
            10 : (2,(0,1,2,3,),1),
            11 : (2,(0,2,),1),
            12 : (2,(0,),2),
            13 : (2,(1,),2),
            14 : (2,(2,),2),
            15 : (2,(3,),2),
            16 : (2,(4,),2),
            17 : (2,(5,),2),
            18 : (2,(6,),2),
            19 : (2,(7,),2),
            20 : (2,(0,1,),2),
            21 : (2,(2,3,),2),
            22 : (2,(4,5,),2),
            23 : (2,(6,7,),2),
            24 : (2,(0,4,),2),
            25 : (2,(2,6,),2),
            26 : (2,(0,1,4,),2),
            27 : (2,(2,3,6,),2),
            28 : (2,(0,1,4,5,),2),
            29 : (2,(2,3,6,7,),2),
            30 : (2,(0,2,4,6,),2),
            31 : None,
            }
        self.nrDci11AntPortsDmrsType1MaxLen2OneCwValid = '0-30'
        
        self.nrDci11AntPortsDmrsType1MaxLen2TwoCws = {
            0 : (2,(0,1,2,3,4,),2),
            1 : (2,(0,1,2,3,4,6,),2),
            2 : (2,(0,1,2,3,4,5,6,),2),
            3 : (2,(0,1,2,3,4,5,6,7,),2),
            4 : None,
            5 : None,
            6 : None,
            7 : None,
            8 : None,
            9 : None,
            10 : None,
            11 : None,
            12 : None,
            13 : None,
            14 : None,
            15 : None,
            16 : None,
            17 : None,
            18 : None,
            19 : None,
            20 : None,
            21 : None,
            22 : None,
            23 : None,
            24 : None,
            25 : None,
            26 : None,
            27 : None,
            28 : None,
            29 : None,
            30 : None,
            31 : None,
            }
        self.nrDci11AntPortsDmrsType1MaxLen2TwoCwsValid = '0-3'
        
        #Table 7.3.1.2.2-3: Antenna port(s) (1000 + DMRS port), dmrs-Type=2, maxLength=1
        self.nrDci11AntPortsDmrsType2MaxLen1OneCw = {
            0 : (1,(0,),1),
            1 : (1,(1,),1),
            2 : (1,(0,1,),1),
            3 : (2,(0,),1),
            4 : (2,(1,),1),
            5 : (2,(2,),1),
            6 : (2,(3,),1),
            7 : (2,(0,1,),1),
            8 : (2,(2,3,),1),
            9 : (2,(0,1,2,),1),
            10 : (2,(0,1,2,3,),1),
            11 : (3,(0,),1),
            12 : (3,(1,),1),
            13 : (3,(2,),1),
            14 : (3,(3,),1),
            15 : (3,(4,),1),
            16 : (3,(5,),1),
            17 : (3,(0,1,),1),
            18 : (3,(2,3,),1),
            19 : (3,(4,5,),1),
            20 : (3,(0,1,2,),1),
            21 : (3,(3,4,5,),1),
            22 : (3,(0,1,2,3,),1),
            23 : (2,(0,2,),1),
            24 : None,
            25 : None,
            26 : None,
            27 : None,
            28 : None,
            29 : None,
            30 : None,
            31 : None,
            }
        self.nrDci11AntPortsDmrsType2MaxLen1OneCwValid = '0-23'
        
        self.nrDci11AntPortsDmrsType2MaxLen1TwoCws = {
            0 : (3,(0,1,2,3,4,),1),
            1 : (3,(0,1,2,3,4,5,),1),
            2 : None,
            3 : None,
            4 : None,
            5 : None,
            6 : None,
            7 : None,
            8 : None,
            9 : None,
            10 : None,
            11 : None,
            12 : None,
            13 : None,
            14 : None,
            15 : None,
            16 : None,
            17 : None,
            18 : None,
            19 : None,
            20 : None,
            21 : None,
            22 : None,
            23 : None,
            24 : None,
            25 : None,
            26 : None,
            27 : None,
            28 : None,
            29 : None,
            30 : None,
            31 : None,
            }
        self.nrDci11AntPortsDmrsType2MaxLen1TwoCwsValid = '0-1'
        
        #Table 7.3.1.2.2-4: Antenna port(s) (1000 + DMRS port), dmrs-Type=2, maxLength=2
        self.nrDci11AntPortsDmrsType2MaxLen2OneCw = {
            0 : (1,(0,),1),
            1 : (1,(1,),1),
            2 : (1,(0,1,),1),
            3 : (2,(0,),1),
            4 : (2,(1,),1),
            5 : (2,(2,),1),
            6 : (2,(3,),1),
            7 : (2,(0,1,),1),
            8 : (2,(2,3,),1),
            9 : (2,(0,1,2,),1),
            10 : (2,(0,1,2,3,),1),
            11 : (3,(0,),1),
            12 : (3,(1,),1),
            13 : (3,(2,),1),
            14 : (3,(3,),1),
            15 : (3,(4,),1),
            16 : (3,(5,),1),
            17 : (3,(0,1,),1),
            18 : (3,(2,3,),1),
            19 : (3,(4,5,),1),
            20 : (3,(0,1,2,),1),
            21 : (3,(3,4,5,),1),
            22 : (3,(0,1,2,3,),1),
            23 : (2,(0,2,),1),
            24 : (3,(0,),2),
            25 : (3,(1,),2),
            26 : (3,(2,),2),
            27 : (3,(3,),2),
            28 : (3,(4,),2),
            29 : (3,(5,),2),
            30 : (3,(6,),2),
            31 : (3,(7,),2),
            32 : (3,(8,),2),
            33 : (3,(9,),2),
            34 : (3,(10,),2),
            35 : (3,(11,),2),
            36 : (3,(0,1,),2),
            37 : (3,(2,3,),2),
            38 : (3,(4,5,),2),
            39 : (3,(6,7,),2),
            40 : (3,(8,9,),2),
            41 : (3,(10,11,),2),
            42 : (3,(0,1,6,),2),
            43 : (3,(2,3,8,),2),
            44 : (3,(4,5,10,),2),
            45 : (3,(0,1,6,7,),2),
            46 : (3,(2,3,8,9,),2),
            47 : (3,(4,5,10,11,),2),
            48 : (1,(0,),2),
            49 : (1,(1,),2),
            50 : (1,(6,),2),
            51 : (1,(7,),2),
            52 : (1,(0,1,),2),
            53 : (1,(6,7,),2),
            54 : (2,(0,1,),2),
            55 : (2,(2,3,),2),
            56 : (2,(6,7,),2),
            57 : (2,(8,9,),2),
            58 : None,
            59 : None,
            60 : None,
            61 : None,
            62 : None,
            63 : None,
            }
        self.nrDci11AntPortsDmrsType2MaxLen2OneCwValid = '0-57'
        
        self.nrDci11AntPortsDmrsType2MaxLen2TwoCws = {
            0 : (3,(0,1,2,3,4,),1),
            1 : (3,(0,1,2,3,4,5,),1),
            2 : (2,(0,1,2,3,6,),2),
            3 : (2,(0,1,2,3,6,8,),2),
            4 : (2,(0,1,2,3,6,7,8,),2),
            5 : (2,(0,1,2,3,6,7,8,9,),2),
            6 : None,
            7 : None,
            8 : None,
            9 : None,
            10 : None,
            11 : None,
            12 : None,
            13 : None,
            14 : None,
            15 : None,
            16 : None,
            17 : None,
            18 : None,
            19 : None,
            20 : None,
            21 : None,
            22 : None,
            23 : None,
            24 : None,
            25 : None,
            26 : None,
            27 : None,
            28 : None,
            29 : None,
            30 : None,
            31 : None,
            32 : None,
            33 : None,
            34 : None,
            35 : None,
            36 : None,
            37 : None,
            38 : None,
            39 : None,
            40 : None,
            41 : None,
            42 : None,
            43 : None,
            44 : None,
            45 : None,
            46 : None,
            47 : None,
            48 : None,
            49 : None,
            50 : None,
            51 : None,
            52 : None,
            53 : None,
            54 : None,
            55 : None,
            56 : None,
            57 : None,
            58 : None,
            59 : None,
            60 : None,
            61 : None,
            62 : None,
            63 : None,
            }
        self.nrDci11AntPortsDmrsType2MaxLen2TwoCwsValid = '0-5'
        
        #refer to 3GPP 38.211 vf30
        #Table 7.4.1.1.2-1: Parameters for PDSCH DM-RS configuration type 1.
        #Table 6.4.1.1.3-1: Parameters for PUSCH DM-RS configuration type 1.
        self.nrDmrsSchCfgType1 = {
            0 : (0,0),
            1 : (0,0),
            2 : (1,1),
            3 : (1,1),
            4 : (0,0),
            5 : (0,0),
            6 : (1,1),
            7 : (1,1),
            }
        
        #Table 7.4.1.1.2-2: Parameters for PDSCH DM-RS configuration type 2.
        #Table 6.4.1.1.3-2: Parameters for PUSCH DM-RS configuration type 2.
        self.nrDmrsSchCfgType2 = {
            0 : (0,0),
            1 : (0,0),
            2 : (1,2),
            3 : (1,2),
            4 : (2,4),
            5 : (2,4),
            6 : (0,0),
            7 : (0,0),
            8 : (1,2),
            9 : (1,2),
            10 : (2,4),
            11 : (2,4),
            }
        
        #Table 7.4.1.1.2-3: PDSCH DM-RS positions l- for single-symbol DM-RS.
        self.nrDmrsPdschPosOneSymb = {
            '2_Type A_pos0' : None, '2_Type A_pos1' : None, '2_Type A_pos2' : None, '2_Type A_pos3' : None,
            '3_Type A_pos0' : (0,), '3_Type A_pos1' : (0,), '3_Type A_pos2' : (0,), '3_Type A_pos3' : (0,),
            '4_Type A_pos0' : (0,), '4_Type A_pos1' : (0,), '4_Type A_pos2' : (0,), '4_Type A_pos3' : (0,),
            '5_Type A_pos0' : (0,), '5_Type A_pos1' : (0,), '5_Type A_pos2' : (0,), '5_Type A_pos3' : (0,),
            '6_Type A_pos0' : (0,), '6_Type A_pos1' : (0,), '6_Type A_pos2' : (0,), '6_Type A_pos3' : (0,),
            '7_Type A_pos0' : (0,), '7_Type A_pos1' : (0,), '7_Type A_pos2' : (0,), '7_Type A_pos3' : (0,),
            '8_Type A_pos0' : (0,), '8_Type A_pos1' : (0, 7,), '8_Type A_pos2' : (0, 7,), '8_Type A_pos3' : (0, 7,),
            '9_Type A_pos0' : (0,), '9_Type A_pos1' : (0, 7,), '9_Type A_pos2' : (0, 7,), '9_Type A_pos3' : (0, 7,),
            '10_Type A_pos0' : (0,), '10_Type A_pos1' : (0, 9,), '10_Type A_pos2' : (0, 6, 9,), '10_Type A_pos3' : (0, 6, 9,),
            '11_Type A_pos0' : (0,), '11_Type A_pos1' : (0, 9,), '11_Type A_pos2' : (0, 6, 9,), '11_Type A_pos3' : (0, 6, 9,),
            '12_Type A_pos0' : (0,), '12_Type A_pos1' : (0, 9,), '12_Type A_pos2' : (0, 6, 9,), '12_Type A_pos3' : (0, 5, 8, 11,),
            '13_Type A_pos0' : (0,), '13_Type A_pos1' : (0, 11,), '13_Type A_pos2' : (0, 7, 11,), '13_Type A_pos3' : (0, 5, 8, 11,),
            '14_Type A_pos0' : (0,), '14_Type A_pos1' : (0, 11,), '14_Type A_pos2' : (0, 7, 11,), '14_Type A_pos3' : (0, 5, 8, 11,),
            '2_Type B_pos0' : (0,), '2_Type B_pos1' : (0,), '2_Type B_pos2' : None, '2_Type B_pos3' : None,
            '3_Type B_pos0' : None, '3_Type B_pos1' : None, '3_Type B_pos2' : None, '3_Type B_pos3' : None,
            '4_Type B_pos0' : (0,), '4_Type B_pos1' : (0,), '4_Type B_pos2' : None, '4_Type B_pos3' : None,
            '5_Type B_pos0' : None, '5_Type B_pos1' : None, '5_Type B_pos2' : None, '5_Type B_pos3' : None,
            '6_Type B_pos0' : (0,), '6_Type B_pos1' : (0, 4,), '6_Type B_pos2' : None, '6_Type B_pos3' : None,
            '7_Type B_pos0' : (0,), '7_Type B_pos1' : (0, 4,), '7_Type B_pos2' : None, '7_Type B_pos3' : None,
            '8_Type B_pos0' : None, '8_Type B_pos1' : None, '8_Type B_pos2' : None, '8_Type B_pos3' : None,
            '9_Type B_pos0' : None, '9_Type B_pos1' : None, '9_Type B_pos2' : None, '9_Type B_pos3' : None,
            '10_Type B_pos0' : None, '10_Type B_pos1' : None, '10_Type B_pos2' : None, '10_Type B_pos3' : None,
            '11_Type B_pos0' : None, '11_Type B_pos1' : None, '11_Type B_pos2' : None, '11_Type B_pos3' : None,
            '12_Type B_pos0' : None, '12_Type B_pos1' : None, '12_Type B_pos2' : None, '12_Type B_pos3' : None,
            '13_Type B_pos0' : None, '13_Type B_pos1' : None, '13_Type B_pos2' : None, '13_Type B_pos3' : None,
            '14_Type B_pos0' : None, '14_Type B_pos1' : None, '14_Type B_pos2' : None, '14_Type B_pos3' : None,
            }
        
        #Table 7.4.1.1.2-4: PDSCH DM-RS positions l- for double-symbol DM-RS.
        self.nrDmrsPdschPosTwoSymbs = {
            '2_Type A_pos0' : None, '2_Type A_pos1' : None,  
            '3_Type A_pos0' : None, '3_Type A_pos1' : None,  
            '4_Type A_pos0' : (0,), '4_Type A_pos1' : (0,),  
            '5_Type A_pos0' : (0,), '5_Type A_pos1' : (0,),  
            '6_Type A_pos0' : (0,), '6_Type A_pos1' : (0,),  
            '7_Type A_pos0' : (0,), '7_Type A_pos1' : (0,),  
            '8_Type A_pos0' : (0,), '8_Type A_pos1' : (0,),  
            '9_Type A_pos0' : (0,), '9_Type A_pos1' : (0,),  
            '10_Type A_pos0' : (0,), '10_Type A_pos1' : (0, 8,),  
            '11_Type A_pos0' : (0,), '11_Type A_pos1' : (0, 8,),  
            '12_Type A_pos0' : (0,), '12_Type A_pos1' : (0, 8,),  
            '13_Type A_pos0' : (0,), '13_Type A_pos1' : (0, 10,),  
            '14_Type A_pos0' : (0,), '14_Type A_pos1' : (0, 10,),  
            '2_Type B_pos0' : None, '2_Type B_pos1' : None,  
            '3_Type B_pos0' : None, '3_Type B_pos1' : None,  
            '4_Type B_pos0' : None, '4_Type B_pos1' : None,  
            '5_Type B_pos0' : None, '5_Type B_pos1' : None,  
            '6_Type B_pos0' : (0,), '6_Type B_pos1' : (0,),  
            '7_Type B_pos0' : (0,), '7_Type B_pos1' : (0,),  
            '8_Type B_pos0' : None, '8_Type B_pos1' : None,  
            '9_Type B_pos0' : None, '9_Type B_pos1' : None,  
            '10_Type B_pos0' : None, '10_Type B_pos1' : None,  
            '11_Type B_pos0' : None, '11_Type B_pos1' : None,  
            '12_Type B_pos0' : None, '12_Type B_pos1' : None,  
            '13_Type B_pos0' : None, '13_Type B_pos1' : None,  
            '14_Type B_pos0' : None, '14_Type B_pos1' : None,  
            }
        
        #Table 6.4.1.1.3-3: PUSCH DM-RS positions l- within a slot for single-symbol DM-RS and intra-slot frequency hopping disabled.
        self.nrDmrsPuschPosOneSymbWoIntraSlotFh = {
            '1_Type A_pos0' : None, '1_Type A_pos1' : None, '1_Type A_pos2' : None, '1_Type A_pos3' : None,
            '2_Type A_pos0' : None, '2_Type A_pos1' : None, '2_Type A_pos2' : None, '2_Type A_pos3' : None,
            '3_Type A_pos0' : None, '3_Type A_pos1' : None, '3_Type A_pos2' : None, '3_Type A_pos3' : None,
            '4_Type A_pos0' : (0,), '4_Type A_pos1' : (0,), '4_Type A_pos2' : (0,), '4_Type A_pos3' : (0,),
            '5_Type A_pos0' : (0,), '5_Type A_pos1' : (0,), '5_Type A_pos2' : (0,), '5_Type A_pos3' : (0,),
            '6_Type A_pos0' : (0,), '6_Type A_pos1' : (0,), '6_Type A_pos2' : (0,), '6_Type A_pos3' : (0,),
            '7_Type A_pos0' : (0,), '7_Type A_pos1' : (0,), '7_Type A_pos2' : (0,), '7_Type A_pos3' : (0,),
            '8_Type A_pos0' : (0,), '8_Type A_pos1' : (0, 7,), '8_Type A_pos2' : (0, 7,), '8_Type A_pos3' : (0, 7,),
            '9_Type A_pos0' : (0,), '9_Type A_pos1' : (0, 7,), '9_Type A_pos2' : (0, 7,), '9_Type A_pos3' : (0, 7,),
            '10_Type A_pos0' : (0,), '10_Type A_pos1' : (0, 9,), '10_Type A_pos2' : (0, 6, 9,), '10_Type A_pos3' : (0, 6, 9,),
            '11_Type A_pos0' : (0,), '11_Type A_pos1' : (0, 9,), '11_Type A_pos2' : (0, 6, 9,), '11_Type A_pos3' : (0, 6, 9,),
            '12_Type A_pos0' : (0,), '12_Type A_pos1' : (0, 9,), '12_Type A_pos2' : (0, 6, 9,), '12_Type A_pos3' : (0, 5, 8, 11,),
            '13_Type A_pos0' : (0,), '13_Type A_pos1' : (0, 11,), '13_Type A_pos2' : (0, 7, 11,), '13_Type A_pos3' : (0, 5, 8, 11,),
            '14_Type A_pos0' : (0,), '14_Type A_pos1' : (0, 11,), '14_Type A_pos2' : (0, 7, 11,), '14_Type A_pos3' : (0, 5, 8, 11,),
            '1_Type B_pos0' : (0,), '1_Type B_pos1' : (0,), '1_Type B_pos2' : (0,), '1_Type B_pos3' : (0,),
            '2_Type B_pos0' : (0,), '2_Type B_pos1' : (0,), '2_Type B_pos2' : (0,), '2_Type B_pos3' : (0,),
            '3_Type B_pos0' : (0,), '3_Type B_pos1' : (0,), '3_Type B_pos2' : (0,), '3_Type B_pos3' : (0,),
            '4_Type B_pos0' : (0,), '4_Type B_pos1' : (0,), '4_Type B_pos2' : (0,), '4_Type B_pos3' : (0,),
            '5_Type B_pos0' : (0,), '5_Type B_pos1' : (0, 4,), '5_Type B_pos2' : (0, 4,), '5_Type B_pos3' : (0, 4,),
            '6_Type B_pos0' : (0,), '6_Type B_pos1' : (0, 4,), '6_Type B_pos2' : (0, 4,), '6_Type B_pos3' : (0, 4,),
            '7_Type B_pos0' : (0,), '7_Type B_pos1' : (0, 4,), '7_Type B_pos2' : (0, 4,), '7_Type B_pos3' : (0, 4,),
            '8_Type B_pos0' : (0,), '8_Type B_pos1' : (0, 6,), '8_Type B_pos2' : (0, 3, 6,), '8_Type B_pos3' : (0, 3, 6,),
            '9_Type B_pos0' : (0,), '9_Type B_pos1' : (0, 6,), '9_Type B_pos2' : (0, 3, 6,), '9_Type B_pos3' : (0, 3, 6,),
            '10_Type B_pos0' : (0,), '10_Type B_pos1' : (0, 8,), '10_Type B_pos2' : (0, 4, 8,), '10_Type B_pos3' : (0, 3, 6, 9,),
            '11_Type B_pos0' : (0,), '11_Type B_pos1' : (0, 8,), '11_Type B_pos2' : (0, 4, 8,), '11_Type B_pos3' : (0, 3, 6, 9,),
            '12_Type B_pos0' : (0,), '12_Type B_pos1' : (0, 10,), '12_Type B_pos2' : (0, 5, 10,), '12_Type B_pos3' : (0, 3, 6, 9,),
            '13_Type B_pos0' : (0,), '13_Type B_pos1' : (0, 10,), '13_Type B_pos2' : (0, 5, 10,), '13_Type B_pos3' : (0, 3, 6, 9,),
            '14_Type B_pos0' : (0,), '14_Type B_pos1' : (0, 10,), '14_Type B_pos2' : (0, 5, 10,), '14_Type B_pos3' : (0, 3, 6, 9,),
            }
        
        #Table 6.4.1.1.3-4: PUSCH DM-RS positions l- within a slot for double-symbol DM-RS and intra-slot frequency hopping disabled.
        self.nrDmrsPuschPosTwoSymbsWoIntraSlotFh = {
            '1_Type A_pos0' : None, '1_Type A_pos1' : None,  
            '2_Type A_pos0' : None, '2_Type A_pos1' : None,  
            '3_Type A_pos0' : None, '3_Type A_pos1' : None,  
            '4_Type A_pos0' : (0,), '4_Type A_pos1' : (0,),  
            '5_Type A_pos0' : (0,), '5_Type A_pos1' : (0,),  
            '6_Type A_pos0' : (0,), '6_Type A_pos1' : (0,),  
            '7_Type A_pos0' : (0,), '7_Type A_pos1' : (0,),  
            '8_Type A_pos0' : (0,), '8_Type A_pos1' : (0,),  
            '9_Type A_pos0' : (0,), '9_Type A_pos1' : (0,),  
            '10_Type A_pos0' : (0,), '10_Type A_pos1' : (0, 8,),  
            '11_Type A_pos0' : (0,), '11_Type A_pos1' : (0, 8,),  
            '12_Type A_pos0' : (0,), '12_Type A_pos1' : (0, 8,),  
            '13_Type A_pos0' : (0,), '13_Type A_pos1' : (0, 10,),  
            '14_Type A_pos0' : (0,), '14_Type A_pos1' : (0, 10,),  
            '1_Type B_pos0' : None, '1_Type B_pos1' : None,  
            '2_Type B_pos0' : None, '2_Type B_pos1' : None,  
            '3_Type B_pos0' : None, '3_Type B_pos1' : None,  
            '4_Type B_pos0' : None, '4_Type B_pos1' : None,  
            '5_Type B_pos0' : (0,), '5_Type B_pos1' : (0,),  
            '6_Type B_pos0' : (0,), '6_Type B_pos1' : (0,),  
            '7_Type B_pos0' : (0,), '7_Type B_pos1' : (0,),  
            '8_Type B_pos0' : (0,), '8_Type B_pos1' : (0, 5,),  
            '9_Type B_pos0' : (0,), '9_Type B_pos1' : (0, 5,),  
            '10_Type B_pos0' : (0,), '10_Type B_pos1' : (0, 7,),  
            '11_Type B_pos0' : (0,), '11_Type B_pos1' : (0, 7,),  
            '12_Type B_pos0' : (0,), '12_Type B_pos1' : (0, 9,),  
            '13_Type B_pos0' : (0,), '13_Type B_pos1' : (0, 9,),  
            '14_Type B_pos0' : (0,), '14_Type B_pos1' : (0, 9,),  
            }
        
        #Table 6.4.1.1.3-6: PUSCH DM-RS positions l- within a slot for single-symbol DM-RS and intra-slot frequency hopping enabled. 
        self.nrDmrsPuschPosOneSymbWithIntraSlotFh = {
            '1_Type A_2_pos0_1st' : None,
            '2_Type A_2_pos0_1st' : None,
            '3_Type A_2_pos0_1st' : None,
            '4_Type A_2_pos0_1st' : (2,),
            '5_Type A_2_pos0_1st' : (2,),
            '6_Type A_2_pos0_1st' : (2,),
            '7_Type A_2_pos0_1st' : (2,),
            '1_Type A_2_pos0_2nd' : None,
            '2_Type A_2_pos0_2nd' : None,
            '3_Type A_2_pos0_2nd' : None,
            '4_Type A_2_pos0_2nd' : (0,),
            '5_Type A_2_pos0_2nd' : (0,),
            '6_Type A_2_pos0_2nd' : (0,),
            '7_Type A_2_pos0_2nd' : (0,),
            '1_Type A_2_pos1_1st' : None,
            '2_Type A_2_pos1_1st' : None,
            '3_Type A_2_pos1_1st' : None,
            '4_Type A_2_pos1_1st' : (2,),
            '5_Type A_2_pos1_1st' : (2,),
            '6_Type A_2_pos1_1st' : (2,),
            '7_Type A_2_pos1_1st' : (2, 6,),
            '1_Type A_2_pos1_2nd' : None,
            '2_Type A_2_pos1_2nd' : None,
            '3_Type A_2_pos1_2nd' : None,
            '4_Type A_2_pos1_2nd' : (0,),
            '5_Type A_2_pos1_2nd' : (0, 4,),
            '6_Type A_2_pos1_2nd' : (0, 4,),
            '7_Type A_2_pos1_2nd' : (0, 4,),
            '1_Type A_3_pos0_1st' : None,
            '2_Type A_3_pos0_1st' : None,
            '3_Type A_3_pos0_1st' : None,
            '4_Type A_3_pos0_1st' : (3,),
            '5_Type A_3_pos0_1st' : (3,),
            '6_Type A_3_pos0_1st' : (3,),
            '7_Type A_3_pos0_1st' : (3,),
            '1_Type A_3_pos0_2nd' : None,
            '2_Type A_3_pos0_2nd' : None,
            '3_Type A_3_pos0_2nd' : None,
            '4_Type A_3_pos0_2nd' : (0,),
            '5_Type A_3_pos0_2nd' : (0,),
            '6_Type A_3_pos0_2nd' : (0,),
            '7_Type A_3_pos0_2nd' : (0,),
            '1_Type A_3_pos1_1st' : None,
            '2_Type A_3_pos1_1st' : None,
            '3_Type A_3_pos1_1st' : None,
            '4_Type A_3_pos1_1st' : (3,),
            '5_Type A_3_pos1_1st' : (3,),
            '6_Type A_3_pos1_1st' : (3,),
            '7_Type A_3_pos1_1st' : (3,),
            '1_Type A_3_pos1_2nd' : None,
            '2_Type A_3_pos1_2nd' : None,
            '3_Type A_3_pos1_2nd' : None,
            '4_Type A_3_pos1_2nd' : (0,),
            '5_Type A_3_pos1_2nd' : (0, 4,),
            '6_Type A_3_pos1_2nd' : (0, 4,),
            '7_Type A_3_pos1_2nd' : (0, 4,),
            '1_Type B_0_pos0_1st' : (0,),
            '2_Type B_0_pos0_1st' : (0,),
            '3_Type B_0_pos0_1st' : (0,),
            '4_Type B_0_pos0_1st' : (0,),
            '5_Type B_0_pos0_1st' : (0,),
            '6_Type B_0_pos0_1st' : (0,),
            '7_Type B_0_pos0_1st' : (0,),
            '1_Type B_0_pos0_2nd' : (0,),
            '2_Type B_0_pos0_2nd' : (0,),
            '3_Type B_0_pos0_2nd' : (0,),
            '4_Type B_0_pos0_2nd' : (0,),
            '5_Type B_0_pos0_2nd' : (0,),
            '6_Type B_0_pos0_2nd' : (0,),
            '7_Type B_0_pos0_2nd' : (0,),
            '1_Type B_0_pos1_1st' : (0,),
            '2_Type B_0_pos1_1st' : (0,),
            '3_Type B_0_pos1_1st' : (0,),
            '4_Type B_0_pos1_1st' : (0,),
            '5_Type B_0_pos1_1st' : (0, 4,),
            '6_Type B_0_pos1_1st' : (0, 4,),
            '7_Type B_0_pos1_1st' : (0, 4,),
            '1_Type B_0_pos1_2nd' : (0,),
            '2_Type B_0_pos1_2nd' : (0,),
            '3_Type B_0_pos1_2nd' : (0,),
            '4_Type B_0_pos1_2nd' : (0,),
            '5_Type B_0_pos1_2nd' : (0, 4,),
            '6_Type B_0_pos1_2nd' : (0, 4,),
            '7_Type B_0_pos1_2nd' : (0, 4,),
            }
        
        #refer to 3GPP 38.212 vf30
        #note: 1st part of key: 0=fullyAndPartialAndNonCoherent, 1=partialAndNonCoherent, 2=nonCoherent
        #Table 7.3.1.1.2-2: Precoding information and number of layers, for 4 antenna ports, if transform precoder is disabled and maxRank = 2 or 3 or 4
        self.nrDci01TpmiAp4Tp0MaxRank234 = {
            '0_0' : (1,0),
            '0_1' : (1,1),
            '0_2' : (1,2),
            '0_3' : (1,3),
            '0_4' : (2,0),
            '0_5' : (2,1),
            '0_6' : (2,2),
            '0_7' : (2,3),
            '0_8' : (2,4),
            '0_9' : (2,5),
            '0_10' : (3,0),
            '0_11' : (4,0),
            '0_12' : (1,4),
            '0_13' : (1,5),
            '0_14' : (1,6),
            '0_15' : (1,7),
            '0_16' : (1,8),
            '0_17' : (1,9),
            '0_18' : (1,10),
            '0_19' : (1,11),
            '0_20' : (2,6),
            '0_21' : (2,7),
            '0_22' : (2,8),
            '0_23' : (2,9),
            '0_24' : (2,10),
            '0_25' : (2,11),
            '0_26' : (2,12),
            '0_27' : (2,13),
            '0_28' : (3,1),
            '0_29' : (3,2),
            '0_30' : (4,1),
            '0_31' : (4,2),
            '0_32' : (1,12),
            '0_33' : (1,13),
            '0_34' : (1,14),
            '0_35' : (1,15),
            '0_36' : (1,16),
            '0_37' : (1,17),
            '0_38' : (1,18),
            '0_39' : (1,19),
            '0_40' : (1,20),
            '0_41' : (1,21),
            '0_42' : (1,22),
            '0_43' : (1,23),
            '0_44' : (1,24),
            '0_45' : (1,25),
            '0_46' : (1,26),
            '0_47' : (1,27),
            '0_48' : (2,14),
            '0_49' : (2,15),
            '0_50' : (2,16),
            '0_51' : (2,17),
            '0_52' : (2,18),
            '0_53' : (2,19),
            '0_54' : (2,20),
            '0_55' : (2,21),
            '0_56' : (3,3),
            '0_57' : (3,4),
            '0_58' : (3,5),
            '0_59' : (3,6),
            '0_60' : (4,3),
            '0_61' : (4,4),
            '0_62' : None,
            '0_63' : None,
            '1_0' : (1,0),
            '1_1' : (1,1),
            '1_2' : (1,2),
            '1_3' : (1,3),
            '1_4' : (2,0),
            '1_5' : (2,1),
            '1_6' : (2,2),
            '1_7' : (2,3),
            '1_8' : (2,4),
            '1_9' : (2,5),
            '1_10' : (3,0),
            '1_11' : (4,0),
            '1_12' : (1,4),
            '1_13' : (1,5),
            '1_14' : (1,6),
            '1_15' : (1,7),
            '1_16' : (1,8),
            '1_17' : (1,9),
            '1_18' : (1,10),
            '1_19' : (1,11),
            '1_20' : (2,6),
            '1_21' : (2,7),
            '1_22' : (2,8),
            '1_23' : (2,9),
            '1_24' : (2,10),
            '1_25' : (2,11),
            '1_26' : (2,12),
            '1_27' : (2,13),
            '1_28' : (3,1),
            '1_29' : (3,2),
            '1_30' : (4,1),
            '1_31' : (4,2),
            '2_0' : (1,0),
            '2_1' : (1,1),
            '2_2' : (1,2),
            '2_3' : (1,3),
            '2_4' : (2,0),
            '2_5' : (2,1),
            '2_6' : (2,2),
            '2_7' : (2,3),
            '2_8' : (2,4),
            '2_9' : (2,5),
            '2_10' : (3,0),
            '2_11' : (4,0),
            '2_12' : None,
            '2_13' : None,
            '2_14' : None,
            }
        
        #Table 7.3.1.1.2-3: Precoding information and number of layers for 4 antenna ports, if transform precoder is enabled, or if transform precoder is disabled and maxRank = 1
        self.nrDci01TpmiAp4Tp1OrTp0MaxRank1 = {
            '0_0' : (1,0),
            '0_1' : (1,1),
            '0_2' : (1,2),
            '0_3' : (1,3),
            '0_4' : (1,4),
            '0_5' : (1,5),
            '0_6' : (1,6),
            '0_7' : (1,7),
            '0_8' : (1,8),
            '0_9' : (1,9),
            '0_10' : (1,10),
            '0_11' : (1,11),
            '0_12' : (1,12),
            '0_13' : (1,13),
            '0_14' : (1,14),
            '0_15' : (1,15),
            '0_16' : (1,16),
            '0_17' : (1,17),
            '0_18' : (1,18),
            '0_19' : (1,19),
            '0_20' : (1,20),
            '0_21' : (1,21),
            '0_22' : (1,22),
            '0_23' : (1,23),
            '0_24' : (1,24),
            '0_25' : (1,25),
            '0_26' : (1,26),
            '0_27' : (1,27),
            '0_28' : None,
            '0_29' : None,
            '0_30' : None,
            '0_31' : None,
            '1_0' : (1,0),
            '1_1' : (1,1),
            '1_2' : (1,2),
            '1_3' : (1,3),
            '1_4' : (1,4),
            '1_5' : (1,5),
            '1_6' : (1,6),
            '1_7' : (1,7),
            '1_8' : (1,8),
            '1_9' : (1,9),
            '1_10' : (1,10),
            '1_11' : (1,11),
            '1_12' : None,
            '1_13' : None,
            '1_14' : None,
            '1_15' : None,
            '2_0' : (1,0),
            '2_1' : (1,1),
            '2_2' : (1,2),
            '2_3' : (1,3),
            }
        
        #Table 7.3.1.1.2-4: Precoding information and number of layers, for 2 antenna ports, if transform precoder is disabled and maxRank = 2
        self.nrDci01TpmiAp2Tp0MaxRank2 = {
            '0_0' : (1,0),
            '0_1' : (1,1),
            '0_2' : (2,0),
            '0_3' : (1,2),
            '0_4' : (1,3),
            '0_5' : (1,4),
            '0_6' : (1,5),
            '0_7' : (2,1),
            '0_8' : (2,2),
            '0_9' : None,
            '0_10' : None,
            '0_11' : None,
            '0_12' : None,
            '0_13' : None,
            '0_14' : None,
            '0_15' : None,
            '2_0' : (1,0),
            '2_1' : (1,1),
            '2_2' : (2,0),
            '2_3' : None,
            }
        
        #Table 7.3.1.1.2-5: Precoding information and number of layers, for 2 antenna ports, if transform precoder is enabled, or if transform precoder is disabled and maxRank = 1
        self.nrDci01TpmiAp2Tp1OrTp0MaxRank1 = {
            '0_0' : (1,0),
            '0_1' : (1,1),
            '0_2' : (1,2),
            '0_3' : (1,3),
            '0_4' : (1,4),
            '0_5' : (1,5),
            '0_6' : None,
            '0_7' : None,
            '2_0' : (1,0),
            '2_1' : (1,1),
            }
        
        #refer to 3GPP 38.212 vf30
        #Table 7.3.1.1.2-28: SRI indication for non-codebook based PUSCH transmission, Lmax=1
        #Table 7.3.1.1.2-29: SRI indication for non-codebook based PUSCH transmission, Lmax=2
        #Table 7.3.1.1.2-30: SRI indication for non-codebook based PUSCH transmission, Lmax=3
        #Table 7.3.1.1.2-31: SRI indication for non-codebook based PUSCH transmission, Lmax=4
        self.nrDci01NonCbSri = {
            #Lmax=1
            '1_2_0' : (0,),
            '1_2_1' : (1,),
            '1_3_0' : (0,),
            '1_3_1' : (1,),
            '1_3_2' : (2,),
            '1_3_3' : None,
            '1_4_0' : (0,),
            '1_4_1' : (1,),
            '1_4_2' : (2,),
            '1_4_3' : (3,),
            #Lmax=2
            '2_2_0' : (0,),
            '2_2_1' : (1,),
            '2_2_2' : (0,1,),
            '2_2_3' : None,
            '2_3_0' : (0,),
            '2_3_1' : (1,),
            '2_3_2' : (2,),
            '2_3_3' : (0,1,),
            '2_3_4' : (0,2,),
            '2_3_5' : (1,2,),
            '2_3_6' : None,
            '2_3_7' : None,
            '2_4_0' : (0,),
            '2_4_1' : (1,),
            '2_4_2' : (2,),
            '2_4_3' : (3,),
            '2_4_4' : (0,1,),
            '2_4_5' : (0,2,),
            '2_4_6' : (0,3,),
            '2_4_7' : (1,2,),
            '2_4_8' : (1,3,),
            '2_4_9' : (2,3,),
            '2_4_10' : None,
            '2_4_11' : None,
            '2_4_12' : None,
            '2_4_13' : None,
            '2_4_14' : None,
            '2_4_15' : None,
            #Lmax=3
            '3_2_0' : (0,),
            '3_2_1' : (1,),
            '3_2_2' : (0,1,),
            '3_2_3' : None,
            '3_3_0' : (0,),
            '3_3_1' : (1,),
            '3_3_2' : (2,),
            '3_3_3' : (0,1,),
            '3_3_4' : (0,2,),
            '3_3_5' : (1,2,),
            '3_3_6' : (0,1,2,),
            '3_3_7' : None,
            '3_4_0' : (0,),
            '3_4_1' : (1,),
            '3_4_2' : (2,),
            '3_4_3' : (3,),
            '3_4_4' : (0,1,),
            '3_4_5' : (0,2,),
            '3_4_6' : (0,3,),
            '3_4_7' : (1,2,),
            '3_4_8' : (1,3,),
            '3_4_9' : (2,3,),
            '3_4_10' : (0,1,2,),
            '3_4_11' : (0,1,3,),
            '3_4_12' : (0,2,3,),
            '3_4_13' : (1,2,3,),
            '3_4_14' : None,
            '3_4_15' : None,
            #Lmax=4
            '4_2_0' : (0,),
            '4_2_1' : (1,),
            '4_2_2' : (0,1,),
            '4_2_3' : None,
            '4_3_0' : (0,),
            '4_3_1' : (1,),
            '4_3_2' : (2,),
            '4_3_3' : (0,1,),
            '4_3_4' : (0,2,),
            '4_3_5' : (1,2,),
            '4_3_6' : (0,1,2,),
            '4_3_7' : None,
            '4_4_0' : (0,),
            '4_4_1' : (1,),
            '4_4_2' : (2,),
            '4_4_3' : (3,),
            '4_4_4' : (0,1,),
            '4_4_5' : (0,2,),
            '4_4_6' : (0,3,),
            '4_4_7' : (1,2,),
            '4_4_8' : (1,3,),
            '4_4_9' : (2,3,),
            '4_4_10' : (0,1,2,),
            '4_4_11' : (0,1,3,),
            '4_4_12' : (0,2,3,),
            '4_4_13' : (1,2,3,),
            '4_4_14' : (0,1,2,3,),
            '4_4_15' : None,
            }
        
        #refer to 3GPP 38.212 vf30
        self.nrDci01AntPorts = {
            #Table 7.3.1.1.2-6: Antenna port(s), transform precoder is enabled, dmrs-Type=1, maxLength=1
            #Table 7.3.1.1.2-7: Antenna port(s), transform precoder is enabled, dmrs-Type=1, maxLength=2
            '1_1_1_1_0' : (2,(0,),1),
            '1_1_1_1_1' : (2,(1,),1),
            '1_1_1_1_2' : (2,(2,),1),
            '1_1_1_1_3' : (2,(3,),1),
            '1_1_2_1_0' : (2,(0,),1),
            '1_1_2_1_1' : (2,(1,),1),
            '1_1_2_1_2' : (2,(2,),1),
            '1_1_2_1_3' : (2,(3,),1),
            '1_1_2_1_4' : (2,(0,),2),
            '1_1_2_1_5' : (2,(1,),2),
            '1_1_2_1_6' : (2,(2,),2),
            '1_1_2_1_7' : (2,(3,),2),
            '1_1_2_1_8' : (2,(4,),2),
            '1_1_2_1_9' : (2,(5,),2),
            '1_1_2_1_10' : (2,(6,),2),
            '1_1_2_1_11' : (2,(7,),2),
            '1_1_2_1_12' : None,
            '1_1_2_1_13' : None,
            '1_1_2_1_14' : None,
            '1_1_2_1_15' : None,
            #Table 7.3.1.1.2-8: Antenna port(s), transform precoder is disabled, dmrs-Type=1, maxLength=1, rank = 1
            #Table 7.3.1.1.2-9: Antenna port(s), transform precoder is disabled, dmrs-Type=1, maxLength=1, rank = 2
            #Table 7.3.1.1.2-10: Antenna port(s), transform precoder is disabled, dmrs-Type=1, maxLength=1, rank = 3
            #Table 7.3.1.1.2-11: Antenna port(s), transform precoder is disabled, dmrs-Type=1, maxLength=1, rank = 4
            '0_1_1_1_0' : (1,(0,),1),
            '0_1_1_1_1' : (1,(1,),1),
            '0_1_1_1_2' : (2,(0,),1),
            '0_1_1_1_3' : (2,(1,),1),
            '0_1_1_1_4' : (2,(2,),1),
            '0_1_1_1_5' : (2,(3,),1),
            '0_1_1_1_6' : None,
            '0_1_1_1_7' : None,
            '0_1_1_2_0' : (1,(0,1,),1),
            '0_1_1_2_1' : (2,(0,1,),1),
            '0_1_1_2_2' : (2,(2,3,),1),
            '0_1_1_2_3' : (2,(0,2,),1),
            '0_1_1_2_4' : None,
            '0_1_1_2_5' : None,
            '0_1_1_2_6' : None,
            '0_1_1_2_7' : None,
            '0_1_1_3_0' : (2,(0,1,2,),1),
            '0_1_1_3_1' : None,
            '0_1_1_3_2' : None,
            '0_1_1_3_3' : None,
            '0_1_1_3_4' : None,
            '0_1_1_3_5' : None,
            '0_1_1_3_6' : None,
            '0_1_1_3_7' : None,
            '0_1_1_4_0' : (2,(0,1,2,3,),1),
            '0_1_1_4_1' : None,
            '0_1_1_4_2' : None,
            '0_1_1_4_3' : None,
            '0_1_1_4_4' : None,
            '0_1_1_4_5' : None,
            '0_1_1_4_6' : None,
            '0_1_1_4_7' : None,
            #Table 7.3.1.1.2-12: Antenna port(s), transform precoder is disabled, dmrs-Type=1, maxLength=2, rank = 1
            #Table 7.3.1.1.2-13: Antenna port(s), transform precoder is disabled, dmrs-Type=1, maxLength=2, rank = 2
            #Table 7.3.1.1.2-14: Antenna port(s), transform precoder is disabled, dmrs-Type=1, maxLength=2, rank = 3
            #Table 7.3.1.1.2-15: Antenna port(s), transform precoder is disabled, dmrs-Type=1, maxLength=2, rank = 4
            '0_1_2_1_0' : (1,(0,),1),
            '0_1_2_1_1' : (1,(1,),1),
            '0_1_2_1_2' : (2,(0,),1),
            '0_1_2_1_3' : (2,(1,),1),
            '0_1_2_1_4' : (2,(2,),1),
            '0_1_2_1_5' : (2,(3,),1),
            '0_1_2_1_6' : (2,(0,),2),
            '0_1_2_1_7' : (2,(1,),2),
            '0_1_2_1_8' : (2,(2,),2),
            '0_1_2_1_9' : (2,(3,),2),
            '0_1_2_1_10' : (2,(4,),2),
            '0_1_2_1_11' : (2,(5,),2),
            '0_1_2_1_12' : (2,(6,),2),
            '0_1_2_1_13' : (2,(7,),2),
            '0_1_2_1_14' : None,
            '0_1_2_1_15' : None,
            '0_1_2_2_0' : (1,(0,1,),1),
            '0_1_2_2_1' : (2,(0,1,),1),
            '0_1_2_2_2' : (2,(2,3,),1),
            '0_1_2_2_3' : (2,(0,2,),1),
            '0_1_2_2_4' : (2,(0,1,),2),
            '0_1_2_2_5' : (2,(2,3,),2),
            '0_1_2_2_6' : (2,(4,5,),2),
            '0_1_2_2_7' : (2,(6,7,),2),
            '0_1_2_2_8' : (2,(0,4,),2),
            '0_1_2_2_9' : (2,(2,6,),2),
            '0_1_2_2_10' : None,
            '0_1_2_2_11' : None,
            '0_1_2_2_12' : None,
            '0_1_2_2_13' : None,
            '0_1_2_2_14' : None,
            '0_1_2_2_15' : None,
            '0_1_2_3_0' : (2,(0,1,2,),1),
            '0_1_2_3_1' : (2,(0,1,4,),2),
            '0_1_2_3_2' : (2,(2,3,6,),2),
            '0_1_2_3_3' : None,
            '0_1_2_3_4' : None,
            '0_1_2_3_5' : None,
            '0_1_2_3_6' : None,
            '0_1_2_3_7' : None,
            '0_1_2_3_8' : None,
            '0_1_2_3_9' : None,
            '0_1_2_3_10' : None,
            '0_1_2_3_11' : None,
            '0_1_2_3_12' : None,
            '0_1_2_3_13' : None,
            '0_1_2_3_14' : None,
            '0_1_2_3_15' : None,
            '0_1_2_4_0' : (2,(0,1,2,3,),1),
            '0_1_2_4_1' : (2,(0,1,4,5,),2),
            '0_1_2_4_2' : (2,(2,3,6,7,),2),
            '0_1_2_4_3' : (2,(0,2,4,6,),2),
            '0_1_2_4_4' : None,
            '0_1_2_4_5' : None,
            '0_1_2_4_6' : None,
            '0_1_2_4_7' : None,
            '0_1_2_4_8' : None,
            '0_1_2_4_9' : None,
            '0_1_2_4_10' : None,
            '0_1_2_4_11' : None,
            '0_1_2_4_12' : None,
            '0_1_2_4_13' : None,
            '0_1_2_4_14' : None,
            '0_1_2_4_15' : None,
            #Table 7.3.1.1.2-16: Antenna port(s), transform precoder is disabled, dmrs-Type=2, maxLength=1, rank=1
            #Table 7.3.1.1.2-17: Antenna port(s), transform precoder is disabled, dmrs-Type=2, maxLength=1, rank=2
            #Table 7.3.1.1.2-18: Antenna port(s), transform precoder is disabled, dmrs-Type=2, maxLength=1, rank=3
            #Table 7.3.1.1.2-19: Antenna port(s), transform precoder is disabled, dmrs-Type=2, maxLength=1, rank=4
            '0_2_1_1_0' : (1,(0,),1),
            '0_2_1_1_1' : (1,(1,),1),
            '0_2_1_1_2' : (2,(0,),1),
            '0_2_1_1_3' : (2,(1,),1),
            '0_2_1_1_4' : (2,(2,),1),
            '0_2_1_1_5' : (2,(3,),1),
            '0_2_1_1_6' : (3,(0,),1),
            '0_2_1_1_7' : (3,(1,),1),
            '0_2_1_1_8' : (3,(2,),1),
            '0_2_1_1_9' : (3,(3,),1),
            '0_2_1_1_10' : (3,(4,),1),
            '0_2_1_1_11' : (3,(5,),1),
            '0_2_1_1_12' : None,
            '0_2_1_1_13' : None,
            '0_2_1_1_14' : None,
            '0_2_1_1_15' : None,
            '0_2_1_2_0' : (1,(0,1,),1),
            '0_2_1_2_1' : (2,(0,1,),1),
            '0_2_1_2_2' : (2,(2,3,),1),
            '0_2_1_2_3' : (3,(0,1,),1),
            '0_2_1_2_4' : (3,(2,3,),1),
            '0_2_1_2_5' : (3,(4,5,),1),
            '0_2_1_2_6' : (2,(0,2,),1),
            '0_2_1_2_7' : None,
            '0_2_1_2_8' : None,
            '0_2_1_2_9' : None,
            '0_2_1_2_10' : None,
            '0_2_1_2_11' : None,
            '0_2_1_2_12' : None,
            '0_2_1_2_13' : None,
            '0_2_1_2_14' : None,
            '0_2_1_2_15' : None,
            '0_2_1_3_0' : (2,(0,1,2,),1),
            '0_2_1_3_1' : (3,(0,1,2,),1),
            '0_2_1_3_2' : (3,(3,4,5,),1),
            '0_2_1_3_3' : None,
            '0_2_1_3_4' : None,
            '0_2_1_3_5' : None,
            '0_2_1_3_6' : None,
            '0_2_1_3_7' : None,
            '0_2_1_3_8' : None,
            '0_2_1_3_9' : None,
            '0_2_1_3_10' : None,
            '0_2_1_3_11' : None,
            '0_2_1_3_12' : None,
            '0_2_1_3_13' : None,
            '0_2_1_3_14' : None,
            '0_2_1_3_15' : None,
            '0_2_1_4_0' : (2,(0,1,2,3,),1),
            '0_2_1_4_1' : (3,(0,1,2,3,),1),
            '0_2_1_4_2' : None,
            '0_2_1_4_3' : None,
            '0_2_1_4_4' : None,
            '0_2_1_4_5' : None,
            '0_2_1_4_6' : None,
            '0_2_1_4_7' : None,
            '0_2_1_4_8' : None,
            '0_2_1_4_9' : None,
            '0_2_1_4_10' : None,
            '0_2_1_4_11' : None,
            '0_2_1_4_12' : None,
            '0_2_1_4_13' : None,
            '0_2_1_4_14' : None,
            '0_2_1_4_15' : None,
            #Table 7.3.1.1.2-20: Antenna port(s), transform precoder is disabled, dmrs-Type=2, maxLength=2, rank=1
            #Table 7.3.1.1.2-21: Antenna port(s), transform precoder is disabled, dmrs-Type=2, maxLength=2, rank=2
            #Table 7.3.1.1.2-22: Antenna port(s), transform precoder is disabled, dmrs-Type=2, maxLength=2, rank=3
            #Table 7.3.1.1.2-23: Antenna port(s), transform precoder is disabled, dmrs-Type=2, maxLength=2, rank=4
            '0_2_2_1_0' : (1,(0,),1),
            '0_2_2_1_1' : (1,(1,),1),
            '0_2_2_1_2' : (2,(0,),1),
            '0_2_2_1_3' : (2,(1,),1),
            '0_2_2_1_4' : (2,(2,),1),
            '0_2_2_1_5' : (2,(3,),1),
            '0_2_2_1_6' : (3,(0,),1),
            '0_2_2_1_7' : (3,(1,),1),
            '0_2_2_1_8' : (3,(2,),1),
            '0_2_2_1_9' : (3,(3,),1),
            '0_2_2_1_10' : (3,(4,),1),
            '0_2_2_1_11' : (3,(5,),1),
            '0_2_2_1_12' : (3,(0,),2),
            '0_2_2_1_13' : (3,(1,),2),
            '0_2_2_1_14' : (3,(2,),2),
            '0_2_2_1_15' : (3,(3,),2),
            '0_2_2_1_16' : (3,(4,),2),
            '0_2_2_1_17' : (3,(5,),2),
            '0_2_2_1_18' : (3,(6,),2),
            '0_2_2_1_19' : (3,(7,),2),
            '0_2_2_1_20' : (3,(8,),2),
            '0_2_2_1_21' : (3,(9,),2),
            '0_2_2_1_22' : (3,(10,),2),
            '0_2_2_1_23' : (3,(11,),2),
            '0_2_2_1_24' : (1,(0,),2),
            '0_2_2_1_25' : (1,(1,),2),
            '0_2_2_1_26' : (1,(6,),2),
            '0_2_2_1_27' : (1,(7,),2),
            '0_2_2_1_28' : None,
            '0_2_2_1_29' : None,
            '0_2_2_1_30' : None,
            '0_2_2_1_31' : None,
            '0_2_2_2_0' : (1,(0,1,),1),
            '0_2_2_2_1' : (2,(0,1,),1),
            '0_2_2_2_2' : (2,(2,3,),1),
            '0_2_2_2_3' : (3,(0,1,),1),
            '0_2_2_2_4' : (3,(2,3,),1),
            '0_2_2_2_5' : (3,(4,5,),1),
            '0_2_2_2_6' : (2,(0,2,),1),
            '0_2_2_2_7' : (3,(0,1,),2),
            '0_2_2_2_8' : (3,(2,3,),2),
            '0_2_2_2_9' : (3,(4,5,),2),
            '0_2_2_2_10' : (3,(6,7,),2),
            '0_2_2_2_11' : (3,(8,9,),2),
            '0_2_2_2_12' : (3,(10,11,),2),
            '0_2_2_2_13' : (1,(0,1,),2),
            '0_2_2_2_14' : (1,(6,7,),2),
            '0_2_2_2_15' : (2,(0,1,),2),
            '0_2_2_2_16' : (2,(2,3,),2),
            '0_2_2_2_17' : (2,(6,7,),2),
            '0_2_2_2_18' : (2,(8,9,),2),
            '0_2_2_2_19' : None,
            '0_2_2_2_20' : None,
            '0_2_2_2_21' : None,
            '0_2_2_2_22' : None,
            '0_2_2_2_23' : None,
            '0_2_2_2_24' : None,
            '0_2_2_2_25' : None,
            '0_2_2_2_26' : None,
            '0_2_2_2_27' : None,
            '0_2_2_2_28' : None,
            '0_2_2_2_29' : None,
            '0_2_2_2_30' : None,
            '0_2_2_2_31' : None,
            '0_2_2_3_0' : (2,(0,1,2,),1),
            '0_2_2_3_1' : (3,(0,1,2,),1),
            '0_2_2_3_2' : (3,(3,4,5,),1),
            '0_2_2_3_3' : (3,(0,1,6,),2),
            '0_2_2_3_4' : (3,(2,3,8,),2),
            '0_2_2_3_5' : (3,(4,5,10,),2),
            '0_2_2_3_6' : None,
            '0_2_2_3_7' : None,
            '0_2_2_3_8' : None,
            '0_2_2_3_9' : None,
            '0_2_2_3_10' : None,
            '0_2_2_3_11' : None,
            '0_2_2_3_12' : None,
            '0_2_2_3_13' : None,
            '0_2_2_3_14' : None,
            '0_2_2_3_15' : None,
            '0_2_2_3_16' : None,
            '0_2_2_3_17' : None,
            '0_2_2_3_18' : None,
            '0_2_2_3_19' : None,
            '0_2_2_3_20' : None,
            '0_2_2_3_21' : None,
            '0_2_2_3_22' : None,
            '0_2_2_3_23' : None,
            '0_2_2_3_24' : None,
            '0_2_2_3_25' : None,
            '0_2_2_3_26' : None,
            '0_2_2_3_27' : None,
            '0_2_2_3_28' : None,
            '0_2_2_3_29' : None,
            '0_2_2_3_30' : None,
            '0_2_2_3_31' : None,
            '0_2_2_4_0' : (2,(0,1,2,3,),1),
            '0_2_2_4_1' : (3,(0,1,2,3,),1),
            '0_2_2_4_2' : (3,(0,1,6,7,),2),
            '0_2_2_4_3' : (3,(2,3,8,9,),2),
            '0_2_2_4_4' : (3,(4,5,10,11,),2),
            '0_2_2_4_5' : None,
            '0_2_2_4_6' : None,
            '0_2_2_4_7' : None,
            '0_2_2_4_8' : None,
            '0_2_2_4_9' : None,
            '0_2_2_4_10' : None,
            '0_2_2_4_11' : None,
            '0_2_2_4_12' : None,
            '0_2_2_4_13' : None,
            '0_2_2_4_14' : None,
            '0_2_2_4_15' : None,
            '0_2_2_4_16' : None,
            '0_2_2_4_17' : None,
            '0_2_2_4_18' : None,
            '0_2_2_4_19' : None,
            '0_2_2_4_20' : None,
            '0_2_2_4_21' : None,
            '0_2_2_4_22' : None,
            '0_2_2_4_23' : None,
            '0_2_2_4_24' : None,
            '0_2_2_4_25' : None,
            '0_2_2_4_26' : None,
            '0_2_2_4_27' : None,
            '0_2_2_4_28' : None,
            '0_2_2_4_29' : None,
            '0_2_2_4_30' : None,
            '0_2_2_4_31' : None,
            }
        
        #refer to 3GPP 38.331 vf30
        #ssb-perRACH-OccasionAndCB-PreamblesPerSSB of RACH-ConfigCommon
        self.nrSsbPerRachOccasion2Float = {
            'oneEighth' : 0.125,
            'oneFourth' : 0.25,
            'oneHalf' : 0.5,
            'one' : 1,
            'two' : 2,
            'four' : 4,
            'eight' : 8,
            'sixteen' : 16,
            }
        self.nrSsbPerRachOccasion2CbPreamblesPerSsb = {
            'oneEighth' : (4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64),
            'oneFourth' : (4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64),
            'oneHalf' : (4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64),
            'one' : (4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64),
            'two' : (4,8,12,16,20,24,28,32),
            'four' : (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16),
            'eight' : (1,2,3,4,5,6,7,8),
            'sixteen' : (1,2,3,4),
            }
        
        #refer to 3GPP 38.213 vf30
        #Table 9.2.1-1: PUCCH resource sets before dedicated PUCCH resource configuration
        self.nrCommonPucchResSets = {
            0 : (0,12,2,0,(0, 3)),
            1 : (0,12,2,0,(0, 4, 8)),
            2 : (0,12,2,3,(0, 4, 8)),
            3 : (1,10,4,0,(0, 6)),
            4 : (1,10,4,0,(0, 3, 6, 9)),
            5 : (1,10,4,2,(0, 3, 6, 9)),
            6 : (1,10,4,4,(0, 3, 6, 9)),
            7 : (1,4,10,0,(0, 6)),
            8 : (1,4,10,0,(0, 3, 6, 9)),
            9 : (1,4,10,2,(0, 3, 6, 9)),
            10 : (1,4,10,4,(0, 3, 6, 9)),
            11 : (1,0,14,0,(0, 6)),
            12 : (1,0,14,0,(0, 3, 6, 9)),
            13 : (1,0,14,2,(0, 3, 6, 9)),
            14 : (1,0,14,4,(0, 3, 6, 9)),
            #Note: for pucch resource index 15, 'PRB offset' is floor(N_BWP_size/4)
            15 : (1,0,14,None,(0, 3, 6, 9)),
            }
        
        #offset of CORESET0 w.r.t. SSB
        self.coreset0Offset = 0
        #minimum channel bandwidth
        self.minChBw = 0
        
        #initialize SLIV look-up tables 
        self.initPdschSliv()
        self.initPuschSliv()
        '''
        self.ngwin.logEdit.append('contents of self.nrPdschToSliv:')
        for key,val in self.nrPdschToSliv.items():
            prefix, S, L = key.split('_')
            self.ngwin.logEdit.append('%s,%s,%s,%s'%(prefix,S,L,val))
        self.ngwin.logEdit.append('contents of self.nrPuschToSliv:')
        for key,val in self.nrPuschToSliv.items():
            prefix, S, L = key.split('_')
            self.ngwin.logEdit.append('%s,%s,%s,%s'%(prefix,S,L,val))
        '''
        
        #valid PUSCH PRB allocations when transforming precoding is enabled
        self.lrbsMsg3PuschTp = []
        self.lrbsDedPuschTp = []
        
        #constants
        self.numScPerPrb = 12
            
        
    def validateScsPerBandFr1(self):
        self.ngwin.logEdit.append('-->inside validateScsPerBandFr1')
        
        self.nrScsPerBandFr1 = dict()
        for key,val in self.nrBandScs2BwFr1.items():
            if val.count(1) == 0:
                continue
            band, scs = key.split('_')
            #refer to 38.331 vf30
            #MIB - subCarrierSpacingCommon: Subcarrier spacing for SIB1, Msg.2/4 for initial access and broadcast SI-messages. If the UE acquires this MIB on a carrier frequency <6GHz, the value scs15or60 corresponds to 15 Khz and the value scs30or120 corresponds to 30 kHz. If the UE acquires this MIB on a carrier frequency >6GHz, the value scs15or60 corresponds to 60 Khz and the value scs30or120 corresponds to 120 kHz.
            #BWP - subcarrierSpacing: For the initial DL BWP this field has the same value as the field subCarrierSpacingCommon in MIB of the same serving cell.
            #if scs == '60':
            #    continue
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
        #(a) offset in scsCommon
        #(b) and offset >= 0;
        if not self.nrMinGuardBandEdit.text():
            return
        
        #refer to 3GPP 38.211 vf30
        #7.4.3.1	Time-frequency structure of an SS/PBCH block
        '''
        For FR1, k_ssb and n_crb_ssb based on 15k
        For FR2, k_ssb based on common scs, n_crb_ssb based on 60k

        FR1/FR2   common_scs   ssb_scs     k_ssb	n_crb_ssb
        -----------------------------------------------------------
        FR1	        15k         15k         0~11	minGuardBand*scsCarrier/15+offset
                    15k         30k         0~11	minGuardBand*scsCarrier/15+offset
                    30k         15k         0~23	minGuardBand*scsCarrier/15+2*offset
                    30k         30k         0~23	minGuardBand*scsCarrier/15+2*offset
        FR2         60k         120k        0~11	minGuardBand*scsCarrier/60+offset
                    60k         240k        0~11	max(minGuardBand*scsCarrier/60+offset,4*minGuardBand240k)
                    120k        120k        0~11	minGuardBand*scsCarrier/60+2*offset
                    120k        240k        0~11	max(minGuardBand*scsCarrier/60+2*offset,4*minGuardBand240k)
        -----------------------------------------------------------
        '''
        self.ngwin.logEdit.append('-->inside updateKSsbAndNCrbSsb')
        
        #minGuardBand in carrier scs
        minGuardBand = int(self.nrMinGuardBandEdit.text())
        scsCarrier = int(self.nrCarrierScsComb.currentText()[:-3])
        
        #key = self.nrCarrierScsComb.currentText()[:-3] + '_' + self.nrSsbScsComb.currentText()[:-3]
        key = self.nrMibScsCommonComb.currentText()[:-3] + '_' + self.nrSsbScsComb.currentText()[:-3]
        if key in ('15_15', '15_30'):
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            self.nrSsbKssbEdit.setValidator(QIntValidator(0, 11))
            self.nrSsbNCrbSsbEdit.setText(str(minGuardBand*scsCarrier//15+offset))
        elif key in ('30_15', '30_30'):
            self.nrSsbKssbLabel.setText('k_SSB[0-23]:')
            self.nrSsbKssbEdit.setValidator(QIntValidator(0, 23))
            self.nrSsbNCrbSsbEdit.setText(str(minGuardBand*scsCarrier//15+2*offset))
        elif key == '60_120':
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            self.nrSsbKssbEdit.setValidator(QIntValidator(0, 11))
            self.nrSsbNCrbSsbEdit.setText(str(minGuardBand*scsCarrier//60+offset))
        elif key == '60_240':
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            self.nrSsbKssbEdit.setValidator(QIntValidator(0, 11))
            minGuardBand240k = int(self.nrSsbMinGuardBandScs240kEdit.text())
            self.nrSsbNCrbSsbEdit.setText(str(max(minGuardBand*scsCarrier//60+offset, 4*minGuardBand240k)))
        elif key == '120_120':
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            self.nrSsbKssbEdit.setValidator(QIntValidator(0, 11))
            self.nrSsbNCrbSsbEdit.setText(str(minGuardBand*scsCarrier//60+2*offset))
        elif key == '120_240':
            self.nrSsbKssbLabel.setText('k_SSB[0-11]:')
            self.nrSsbKssbEdit.setValidator(QIntValidator(0, 11))
            minGuardBand240k = int(self.nrSsbMinGuardBandScs240kEdit.text())
            self.nrSsbNCrbSsbEdit.setText(str(max(minGuardBand*scsCarrier//60+2*offset, 4*minGuardBand240k)))
        else:
            pass
    
    def updateRachConfig(self):
        self.ngwin.logEdit.append('-->inside updateRachConfig')
        
        if self.freqRange == 'FR1' and self.duplexMode == 'FDD':
            self.raFormat, self.raX, self.raY, self.raSubfNumFr1SlotNumFr2, self.raStartingSymb, self.raNumSlotsPerSubfFr1Per60KSlotFr2, self.raNumOccasionsPerSlot, self.raDuration = self.nrRaCfgFr1FddSUl[int(self.nrRachGenericPrachConfIdEdit.text())]
        elif self.freqRange == 'FR1' and self.duplexMode == 'TDD':
            self.raFormat, self.raX, self.raY, self.raSubfNumFr1SlotNumFr2, self.raStartingSymb, self.raNumSlotsPerSubfFr1Per60KSlotFr2, self.raNumOccasionsPerSlot, self.raDuration = self.nrRaCfgFr1Tdd[int(self.nrRachGenericPrachConfIdEdit.text())]
        else:   #self.freqRange == 'FR2'
            self.raFormat, self.raX, self.raY, self.raSubfNumFr1SlotNumFr2, self.raStartingSymb, self.raNumSlotsPerSubfFr1Per60KSlotFr2, self.raNumOccasionsPerSlot, self.raDuration = self.nrRaCfgFr2Tdd[int(self.nrRachGenericPrachConfIdEdit.text())]
            
        self.nrRachGenericPrachFmtEdit.setText(self.raFormat)
        if self.raFormat in ('0', '1', '2', '3'):
            raScsSubset = [self.nrScsRaLongPrach['839_'+self.raFormat]]
        else:
            raScsSubset = ('15KHz', '30KHz') if self.freqRange == 'FR1' else ('60KHz', '120KHz')
        self.nrRachGenericScsComb.clear()
        self.nrRachGenericScsComb.addItems(raScsSubset)
        self.nrRachGenericScsComb.setCurrentIndex(0)
    
    def updateCoreset1FreqRes(self):
        if not self.nrDedDlBwpGenericRbStartEdit.text() or not self.nrDedDlBwpGenericLRbsEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside updateCoreset1FreqRes')
        bwpStart = int(self.nrDedDlBwpGenericRbStartEdit.text())
        bwpSize = int(self.nrDedDlBwpGenericLRbsEdit.text())
        #refer to 3GPP 38.213 10.1
        #...the first common RB of the first group of 6 PRBs has index 6*ceil(N_BWP_start/6). 
        firstPrbFirstGrp = 6 * math.ceil(bwpStart / 6)
        numNonOverlapGrps = math.floor((bwpSize - (firstPrbFirstGrp - bwpStart)) / 6)
        text = ''
        for i in range(45):
            if i < numNonOverlapGrps:
                text = text + '1'
            else:
                text = text + '0'
                
            if i > 0 and (i+1) % 8 == 0:
                text = text + ','
        
        self.nrCoreset1FreqResourcesLabel.setText('frequencyDomainResources[%d]:' % numNonOverlapGrps)
        self.nrCoreset1FreqResourcesEdit.setText(text)
        
    
    def onCarrierBandCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onCarrierBandCombCurIndChanged, index=%d' % index)

        #(1) update band info
        ulBand, dlBand, self.duplexMode, self.maxL = self.nrOpBands[self.nrCarrierBandComb.currentText()]
        self.freqRange = 'FR1' if int(self.nrCarrierBandComb.currentText()[1:]) <= 256 else 'FR2'
        if self.duplexMode == 'TDD':
            self.nrCarrierBandInfoLabel.setText('<font color=blue>UL/DL: %s, %s, %s</font>' % (ulBand, self.duplexMode, self.freqRange))
        else:
            self.nrCarrierBandInfoLabel.setText('<font color=blue>UL: %s, DL: %s, %s, %s</font>' % (ulBand, dlBand, self.duplexMode, self.freqRange))

        if self.duplexMode in ('SUL', 'SDL'):
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: SUL/SDL bands (3GPP 38.104 vf30, SDL: n75/n76, SUL: n80/n81/n82/n83/n84/n86)'
                                      ' are not supported!' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            return

        #(2) update ssb scs 
        ssbScsSubset = [v[0] for v in self.nrSsbRasters[self.nrCarrierBandComb.currentText()]]
        self.nrSsbScsComb.clear()
        self.nrSsbScsComb.addItems(ssbScsSubset)
        self.nrSsbScsComb.setCurrentIndex(0)
        
        #(3) update common scs
        if self.freqRange == 'FR1':
            commonScsSubset = ('15KHz', '30KHz')
        else:
            commonScsSubset = ('60KHz', '120KHz')
        self.nrMibScsCommonComb.clear()
        self.nrMibScsCommonComb.addItems(commonScsSubset)
        self.nrMibScsCommonComb.setCurrentIndex(0)

        #(4) update carrier scs
        if self.freqRange == 'FR1':
            carrierScsSubset = self.nrScsPerBandFr1[self.nrCarrierBandComb.currentText()]
        else:
            carrierScsSubset = ('60KHz', '120KHz')
        self.nrCarrierScsComb.clear()
        self.nrCarrierScsComb.addItems(carrierScsSubset)
        self.nrCarrierScsComb.setCurrentIndex(0)
        
        #(5) update ssb-positions-in-burst
        if self.maxL in (4, 8):
            self.nrSsbInOneGrpEdit.setText('11110000' if self.maxL == 4 else '11111111')
            self.nrSsbGrpPresenceEdit.setText('NA')
            self.nrSsbGrpPresenceEdit.setEnabled(False)
        else:
            self.nrSsbInOneGrpEdit.setText('11111111')
            self.nrSsbGrpPresenceEdit.setText('11111111')
            self.nrSsbGrpPresenceEdit.setEnabled(True)
        
        #(6) update rach config 
        self.updateRachConfig()

    def onCarrierScsCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onCarrierScsCombCurIndChanged, index=%d' % index)
        
        #(1) update refScs; update u_PDCCH/u_PDSCH/u_PUSCH in DCI 1_1/0_1 and msg3 PUSCH; update scs of initial ul bwp, dedicated ul/dl bwp
        #self.nrMibScsCommonComb.setCurrentText(self.nrCarrierScsComb.currentText())
        self.nrTddCfgRefScsComb.setCurrentText(self.nrCarrierScsComb.currentText())
        #self.nrIniDlBwpGenericScsComb.setCurrentText(self.nrCarrierScsComb.currentText())
        self.nrIniUlBwpGenericScsComb.setCurrentText(self.nrCarrierScsComb.currentText())
        self.nrDedDlBwpGenericScsComb.setCurrentText(self.nrCarrierScsComb.currentText())
        self.nrDedUlBwpGenericScsComb.setCurrentText(self.nrCarrierScsComb.currentText())
        u = {'15KHz':0, '30KHz':1, '60KHz':2, '120KHz':3, '240KHz':4}[self.nrCarrierScsComb.currentText()]
        #self.nrDci10Sib1MuPdcchEdit.setText(str(u))
        #self.nrDci10Sib1MuPdschEdit.setText(str(u))
        #self.nrDci10Msg2MuPdcchEdit.setText(str(u))
        #self.nrDci10Msg2MuPdschEdit.setText(str(u))
        #self.nrDci10Msg4MuPdcchEdit.setText(str(u))
        #self.nrDci10Msg4MuPdschEdit.setText(str(u))
        self.nrDci11PdschMuPdcchEdit.setText(str(u))
        self.nrDci11PdschMuPdschEdit.setText(str(u))
        self.nrMsg3PuschMuPuschEdit.setText(str(u))
        self.nrMsg3PuschTimeAllocDeltaEdit.setText(str(self.nrPuschTimeAllocMsg3K2Delta[self.nrIniUlBwpGenericScsComb.currentText()]))
        self.nrDci01PuschMuPdcchEdit.setText(str(u))
        self.nrDci01PuschMuPuschEdit.setText(str(u))

        #(2) update transmission bandwidth
        carrierScs = int(self.nrCarrierScsComb.currentText()[:-3])
        commonScs = int(self.nrMibScsCommonComb.currentText()[:-3])
        if commonScs < carrierScs: 
            key = self.nrCarrierBandComb.currentText() + '_' + self.nrMibScsCommonComb.currentText()[:-3]
        else:
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
        '''
        self.flagCoreset0 = self.validateCoreset0()
        if self.flagCoreset0:
            self.updateKSsbAndNCrbSsb(offset=0 if self.coreset0Offset <= 0 else self.coreset0Offset)
            self.flagCss0 = self.validateCss0()
        '''
        
        #(4) update SR periodicity and offset
        srPeriodSet = {
            '15KHz': ('sym2', 'sym6or7', 'sl1', 'sl2', 'sl4', 'sl5', 'sl8', 'sl10', 'sl16', 'sl20', 'sl40', 'sl80'),
            '30KHz': ('sym2', 'sym6or7', 'sl1', 'sl2', 'sl4', 'sl8', 'sl10', 'sl16', 'sl20', 'sl40', 'sl80', 'sl160'),
            '60KHz': ('sym2', 'sym6or7', 'sl1', 'sl2', 'sl4', 'sl8', 'sl16', 'sl20', 'sl40', 'sl80', 'sl160', 'sl320'),
            '120KHz': ('sym2', 'sym6or7', 'sl1', 'sl2', 'sl4', 'sl8', 'sl16', 'sl40', 'sl80', 'sl160', 'sl320', 'sl640'),
            }
        self.nrDsrRes0PeriodicityComb.clear()
        self.nrDsrRes0PeriodicityComb.addItems(srPeriodSet[self.nrCarrierScsComb.currentText()])
        self.nrDsrRes0PeriodicityComb.setCurrentIndex(0)
        self.nrDsrRes0OffsetLabel.setText('offset(in slots)[0]:')
        self.nrDsrRes0OffsetEdit.setText('0')
        self.nrDsrRes0OffsetEdit.setValidator(QIntValidator(0, 0))
        
        self.nrDsrRes1PeriodicityComb.clear()
        self.nrDsrRes1PeriodicityComb.addItems(srPeriodSet[self.nrCarrierScsComb.currentText()])
        self.nrDsrRes1PeriodicityComb.setCurrentIndex(0)
        self.nrDsrRes1OffsetLabel.setText('offset(in slots)[0]:')
        self.nrDsrRes1OffsetEdit.setText('0')
        self.nrDsrRes1OffsetEdit.setValidator(QIntValidator(0, 0))
        
        #(5) validate 'uss first symbols' edit
        self.validateUssFirstSymbs()
    
    def onMibScsCommonCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onMibScsCommonCombCurIndChanged, index=%d' % index)
        
        #(1) update scs for initial dl bwp; update u_pdcch/u_pdsch for sib1/msg2/msg4 
        self.nrIniDlBwpGenericScsComb.setCurrentText(self.nrMibScsCommonComb.currentText())
        u = {'15KHz':0, '30KHz':1, '60KHz':2, '120KHz':3, '240KHz':4}[self.nrMibScsCommonComb.currentText()]
        self.nrDci10Sib1MuPdcchEdit.setText(str(u))
        self.nrDci10Sib1MuPdschEdit.setText(str(u))
        self.nrDci10Msg2MuPdcchEdit.setText(str(u))
        self.nrDci10Msg2MuPdschEdit.setText(str(u))
        self.nrDci10Msg4MuPdcchEdit.setText(str(u))
        self.nrDci10Msg4MuPdschEdit.setText(str(u))
        
        #(2) either update 'carrier bandwidth' or validate coreset0 and update k_ssb and n_crb_ssb
        if self.nrCarrierScsComb.currentText():
            carrierScs = int(self.nrCarrierScsComb.currentText()[:-3])
            commonScs = int(self.nrMibScsCommonComb.currentText()[:-3])
            if commonScs < carrierScs: 
                key = self.nrCarrierBandComb.currentText() + '_' + self.nrMibScsCommonComb.currentText()[:-3]
            else:
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
        else:
            self.flagCoreset0 = self.validateCoreset0()
            if self.flagCoreset0:
                self.updateKSsbAndNCrbSsb(offset=0 if self.coreset0Offset <= 0 else self.coreset0Offset)
                self.flagCss0 = self.validateCss0()

    def onCarrierBwCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onCarrierBwCombCurIndChanged, index=%d' % index)

        #(1) update N_RB w.r.t carrierScs and carrierBw; update N_RB for initial dl bwp w.r.t. commonScs and carrierBw
        carrierScs = int(self.nrCarrierScsComb.currentText()[:-3])
        commonScs = int(self.nrMibScsCommonComb.currentText()[:-3])
        #FIXME two IFs as below is not necessary?
        '''
        if not carrierScs in self.nrNrbFr1 and not carrierScs in self.nrNrbFr2:
            return
        if not commonScs in self.nrNrbFr1 and not commonScs in self.nrNrbFr2:
            return
        '''

        if self.freqRange == 'FR1':
            numRbCarrierScs = self.nrNrbFr1[carrierScs][self.nrBwSetFr1.index(self.nrCarrierBwComb.currentText())]
            numRbCommonScs = self.nrNrbFr1[commonScs][self.nrBwSetFr1.index(self.nrCarrierBwComb.currentText())]
        else:
            numRbCarrierScs = self.nrNrbFr2[carrierScs][self.nrBwSetFr2.index(self.nrCarrierBwComb.currentText())]
            numRbCommonScs = self.nrNrbFr2[commonScs][self.nrBwSetFr2.index(self.nrCarrierBwComb.currentText())]
        self.nrCarrierNumRbEdit.setText(str(numRbCarrierScs))

        #(2) update minGuardBand w.r.t carrierScs and carrierBw
        if self.freqRange == 'FR1':
            minGuardBand = self.nrMinGuardBandFr1[carrierScs][self.nrBwSetFr1.index(self.nrCarrierBwComb.currentText())]
        else:
            minGuardBand = self.nrMinGuardBandFr2[carrierScs][self.nrBwSetFr2.index(self.nrCarrierBwComb.currentText())]
        self.nrMinGuardBandEdit.setText(str(minGuardBand))

        #(3) update minGuardBandScs240k w.r.t. ssbScs and carrierBw
        if self.freqRange == 'FR2' and self.nrSsbScsComb.currentText() == '240KHz':
            carrierBw = int(self.nrCarrierBwComb.currentText()[:-3])
            if carrierBw < 100:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Minimum transmission bandwidth is 100MHz when SSB'
                                          ' subcarrier spacing is 240KHz!' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                self.nrSsbMinGuardBandScs240kEdit.setText('NA')
            else:
                self.nrSsbMinGuardBandScs240kEdit.setText(str(self.nrSsbMinGuardBandScs240k[self.nrCarrierBwComb.currentIndex()]))
                
        #(4) validate CORESET0 and update n_CRB_SSB when necessary
        self.flagCoreset0 = self.validateCoreset0()
        if self.flagCoreset0:
            self.updateKSsbAndNCrbSsb(offset=0 if self.coreset0Offset <= 0 else self.coreset0Offset)
            self.flagCss0 = self.validateCss0()
        
        #(5) update 'L_RBs' and 'RB_start' labels for initial dl bwp tab
        #FIXME L_RBs can't be 1, in which case the 'frequency domain assignment' field in DCIs is 0bits.
        self.nrIniDlBwpGenericRbStartLabel.setText('RB_start[0-%d]:' % (numRbCommonScs -1))
        self.nrIniDlBwpGenericLRbsLabel.setText('L_RBs[2-%d]:' % numRbCommonScs)
        self.nrIniDlBwpGenericRbStartEdit.setText('0')
        self.nrIniDlBwpGenericLRbsEdit.setText(str(numRbCommonScs))
        self.nrIniDlBwpGenericRbStartEdit.setValidator(QIntValidator(0, numRbCommonScs-1))
        self.nrIniDlBwpGenericLRbsEdit.setValidator(QIntValidator(2, numRbCommonScs))
        
        #(6) update 'L_RBs' and 'RB_start' labels for initial ul bwp and dedicated ul/dl bwp tab
        self.nrIniUlBwpGenericRbStartLabel.setText('RB_start[0-%d]:' % (numRbCarrierScs -1))
        self.nrIniUlBwpGenericLRbsLabel.setText('L_RBs[2-%d]:' % numRbCarrierScs)
        self.nrIniUlBwpGenericRbStartEdit.setText('0')
        self.nrIniUlBwpGenericLRbsEdit.setText(str(numRbCarrierScs))
        self.nrIniUlBwpGenericRbStartEdit.setValidator(QIntValidator(0, numRbCarrierScs-1))
        self.nrIniUlBwpGenericLRbsEdit.setValidator(QIntValidator(2, numRbCarrierScs))
        self.nrDedDlBwpGenericRbStartLabel.setText('RB_start[0-%d]:' % (numRbCarrierScs -1))
        self.nrDedDlBwpGenericLRbsLabel.setText('L_RBs[2-%d]:' % numRbCarrierScs)
        self.nrDedDlBwpGenericRbStartEdit.setText('0')
        self.nrDedDlBwpGenericLRbsEdit.setText(str(numRbCarrierScs))
        self.nrDedDlBwpGenericRbStartEdit.setValidator(QIntValidator(0, numRbCarrierScs-1))
        self.nrDedDlBwpGenericLRbsEdit.setValidator(QIntValidator(2, numRbCarrierScs))
        self.nrDedUlBwpGenericRbStartLabel.setText('RB_start[0-%d]:' % (numRbCarrierScs -1))
        self.nrDedUlBwpGenericLRbsLabel.setText('L_RBs[2-%d]:' % numRbCarrierScs)
        self.nrDedUlBwpGenericRbStartEdit.setText('0')
        self.nrDedUlBwpGenericLRbsEdit.setText(str(numRbCarrierScs))
        self.nrDedUlBwpGenericRbStartEdit.setValidator(QIntValidator(0, numRbCarrierScs-1))
        self.nrDedUlBwpGenericLRbsEdit.setValidator(QIntValidator(2, numRbCarrierScs))

    def onSsbScsCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onSsbScsCombCurIndChanged, index=%d' % index)
        
        #(1) update SSB pattern
        ssbScs, ssbPat, ssbGscn = self.nrSsbRasters[self.nrCarrierBandComb.currentText()][self.nrSsbScsComb.currentIndex()]
        self.nrSsbPatternEdit.setText(ssbPat)

        #(2) update minGuardBandScs240k
        if ssbScs == '240KHz':
            carrierBw = int(self.nrCarrierBwComb.currentText()[:-3])
            if carrierBw < 100:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Minimum transmission bandwidth is 100MHz when SSB'
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
            self.flagCss0 = self.validateCss0()
    
    def onUssPeriodicityCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onUssPeriodicityCombCurIndChanged, index=%d' % index)
        
        period = int(self.nrUssPeriodicityComb.currentText()[2:])
        self.nrUssSlotOffsetEdit.clear()
        self.nrUssDurationEdit.clear()
        if period > 1:
            self.nrUssSlotOffsetLabel.setText('monitoringSlotOffset[0-%d]:' % (period-1))
            self.nrUssSlotOffsetEdit.setValidator(QIntValidator(0, period-1))
        else:
            self.nrUssSlotOffsetLabel.setText('monitoringSlotOffset[0]:')
            self.nrUssSlotOffsetEdit.setValidator(QIntValidator(0, 0))
                
        self.nrUssSlotOffsetEdit.setText('0')
        
        if period in (1, 2):
            self.nrUssDurationLabel.setText('duration[1]:')
            self.nrUssDurationEdit.setText('1')
            self.nrUssDurationEdit.setValidator(QIntValidator(1, 1))
        else:
            self.nrUssDurationLabel.setText('duration[1-%d]:' % (period-1))
            self.nrUssDurationEdit.setText(str(period-1))
            self.nrUssDurationEdit.setValidator(QIntValidator(1, period-1))
            
    def validateCoreset0(self):
        if not self.nrMibCoreset0Edit.text():
            return False
        
        ssbScsSubset = [v[0] for v in self.nrSsbRasters[self.nrCarrierBandComb.currentText()]]
        if self.freqRange == 'FR1':
            commonScsSubset = ('15KHz', '30KHz')
        else:
            commonScsSubset = ('60KHz', '120KHz')
        #avoid error when changing 'operating band' from FR1 to FR2
        if not (self.nrSsbScsComb.currentText() in ssbScsSubset and self.nrMibScsCommonComb.currentText() in commonScsSubset):
            return False
        
        self.ngwin.logEdit.append('-->inside validateCoreset0')
        
        self.nrMibCoreset0InfoLabel.setText('<font color=blue>CORESET0: invalid</font>')
        
        #(1) validate coresetZero
        key = self.nrSsbScsComb.currentText()[:-3] + '_' + self.nrMibScsCommonComb.currentText()[:-3] + '_' + self.nrMibCoreset0Edit.text()
        if self.freqRange == 'FR1' and self.minChBw in (5, 10):
            if not key in self.nrCoreset0Fr1MinChBw5m10m.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrCoreset0Fr1MinChBw5m10m!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return False 
            
            if self.nrCoreset0Fr1MinChBw5m10m[key] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid value of coresetZero(=%s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrMibCoreset0Edit.text()))
                return False
            
            val = self.nrCoreset0Fr1MinChBw5m10m[key]
        elif self.freqRange == 'FR1' and self.minChBw == 40:
            if not key in self.nrCoreset0Fr1MinChBw40m.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrCoreset0Fr1MinChBw40m!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return False
            
            if self.nrCoreset0Fr1MinChBw40m[key] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid value of coresetZero(=%s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrMibCoreset0Edit.text()))
                return False
            
            val = self.nrCoreset0Fr1MinChBw40m[key]
        elif self.freqRange == 'FR2':
            if not key in self.nrCoreset0Fr2.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrCoreset0Fr2!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return False
            
            if self.nrCoreset0Fr2[key] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid value of coresetZero(=%s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrMibCoreset0Edit.text()))
                return False
            
            val = self.nrCoreset0Fr2[key]
        else:
            return False
            
        #(2) validate CORESET0 bw against carrier bandwidth
        commonScs = int(self.nrMibScsCommonComb.currentText()[:-3])
        if self.freqRange == 'FR1':
            numRbCommonScs = self.nrNrbFr1[commonScs][self.nrBwSetFr1.index(self.nrCarrierBwComb.currentText())]
        else:
            numRbCommonScs = self.nrNrbFr2[commonScs][self.nrBwSetFr2.index(self.nrCarrierBwComb.currentText())]
            
        self.coreset0MultiplexingPat, self.coreset0NumRbs, self.coreset0NumSymbs, self.coreset0OffsetList = val
        #if int(self.nrCarrierNumRbEdit.text()) < self.coreset0NumRbs:
        if numRbCommonScs < self.coreset0NumRbs:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid CORESET0 setting: CORESET0 numRBs=%d, while numRBs(common scs)=%s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.coreset0NumRbs, numRbCommonScs))
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
                #minBw = max(self.coreset0NumRbs, self.coreset0Offset + 20 * int(self.nrSsbScsComb.currentText()[:-3]) / int(self.nrCarrierScsComb.currentText()[:-3]))
                minBw = max(self.coreset0NumRbs, self.coreset0Offset + 20 * int(self.nrSsbScsComb.currentText()[:-3]) / commonScs)
            else:
                minBw = self.coreset0NumRbs - self.coreset0Offset
            
            #if int(self.nrCarrierNumRbEdit.text()) < minBw:
            if numRbCommonScs < minBw:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid CORESET0 setting: CORESET0 numRBs=%d, offset=%d, minBw = %d, while numRBs(common scs)=%s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.coreset0NumRbs, self.coreset0Offset, minBw, numRbCommonScs))
                return False
        
        #(4) validate self.coreset0NumSymbs against 'dmrs-pointA-Position'
        if self.coreset0NumSymbs == 3 and int(self.nrMibDmRsTypeAPosComb.currentText()[3:]) != 3:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: CORESET numSymbs = 3 is only supported when dmrs-TypeA-Position = 3!' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
            return False
        
        #print CORESET0 info
        #self.ngwin.logEdit.append('<font color=blue><b>[%s]Info</font>: CORESET0 setting: multiplexingPattern = %d, numRBs=%d, numSymbs=%d, offset=%d.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.coreset0MultiplexingPat, self.coreset0NumRbs, self.coreset0NumSymbs, self.coreset0Offset))
        
        self.nrMibCoreset0InfoLabel.setText('<font color=blue>CORESET0: multiplexingPattern=%d, numRBs=%d, numSymbs=%d, offset=%d.</font>' % (self.coreset0MultiplexingPat, self.coreset0NumRbs, self.coreset0NumSymbs, self.coreset0Offset))
        
        #update 'frequency domain assignment' bitwidth for SIB1/Msg2/Msg4 w.r.t CORESET0 bandwidth
        self.bitwidthCoreset0 = math.ceil(math.log2(self.coreset0NumRbs * (self.coreset0NumRbs + 1) / 2))
        
        self.nrDci10Sib1FreqAllocFieldLabel.setText('Freq domain resource assignment[%dbits]:' % self.bitwidthCoreset0)
        self.nrDci10Sib1FreqAllocFieldEdit.setValidator(QRegExpValidator(QRegExp('[0-1]{%d}' % self.bitwidthCoreset0)))
        self.nrDci10Sib1FreqAllocType1RbStartLabel.setText('RB_start(of RIV)[0-%d]:' % (self.coreset0NumRbs - 1))
        self.nrDci10Sib1FreqAllocType1RbStartEdit.setValidator(QIntValidator(0, self.coreset0NumRbs-1))
        self.nrDci10Sib1FreqAllocType1LRbsLabel.setText('L_RBs(of RIV)[2-%d]:' % self.coreset0NumRbs)
        self.nrDci10Sib1FreqAllocType1LRbsEdit.setValidator(QIntValidator(2, self.coreset0NumRbs))
        self.nrDci10Sib1FreqAllocType1RbStartEdit.setText('0')
        self.nrDci10Sib1FreqAllocType1LRbsEdit.setText(str(self.coreset0NumRbs))
        self.nrDci10Sib1FreqAllocFieldEdit.setText('{:0{width}b}'.format(self.makeRiv(self.coreset0NumRbs, 0, self.coreset0NumRbs), width=self.bitwidthCoreset0))
        
        self.nrDci10Msg2FreqAllocFieldLabel.setText('Freq domain resource assignment[%dbits]:' % self.bitwidthCoreset0)
        self.nrDci10Msg2FreqAllocFieldEdit.setValidator(QRegExpValidator(QRegExp('[0-1]{%d}' % self.bitwidthCoreset0)))
        self.nrDci10Msg2FreqAllocType1RbStartLabel.setText('RB_start(of RIV)[0-%d]:' % (self.coreset0NumRbs - 1))
        self.nrDci10Msg2FreqAllocType1RbStartEdit.setValidator(QIntValidator(0, self.coreset0NumRbs-1))
        self.nrDci10Msg2FreqAllocType1LRbsLabel.setText('L_RBs(of RIV)[2-%d]:' % self.coreset0NumRbs)
        self.nrDci10Msg2FreqAllocType1LRbsEdit.setValidator(QIntValidator(2, self.coreset0NumRbs))
        self.nrDci10Msg2FreqAllocType1RbStartEdit.setText('0')
        self.nrDci10Msg2FreqAllocType1LRbsEdit.setText(str(self.coreset0NumRbs))
        self.nrDci10Msg2FreqAllocFieldEdit.setText('{:0{width}b}'.format(self.makeRiv(self.coreset0NumRbs, 0, self.coreset0NumRbs), width=self.bitwidthCoreset0))
        
        self.nrDci10Msg4FreqAllocFieldLabel.setText('Freq domain resource assignment[%dbits]:' % self.bitwidthCoreset0)
        self.nrDci10Msg4FreqAllocFieldEdit.setValidator(QRegExpValidator(QRegExp('[0-1]{%d}' % self.bitwidthCoreset0)))
        self.nrDci10Msg4FreqAllocType1RbStartLabel.setText('RB_start(of RIV)[0-%d]:' % (self.coreset0NumRbs - 1))
        self.nrDci10Msg4FreqAllocType1RbStartEdit.setValidator(QIntValidator(0, self.coreset0NumRbs-1))
        self.nrDci10Msg4FreqAllocType1LRbsLabel.setText('L_RBs(of RIV)[2-%d]:' % self.coreset0NumRbs)
        self.nrDci10Msg4FreqAllocType1LRbsEdit.setValidator(QIntValidator(2, self.coreset0NumRbs))
        self.nrDci10Msg4FreqAllocType1RbStartEdit.setText('0')
        self.nrDci10Msg4FreqAllocType1LRbsEdit.setText(str(self.coreset0NumRbs))
        self.nrDci10Msg4FreqAllocFieldEdit.setText('{:0{width}b}'.format(self.makeRiv(self.coreset0NumRbs, 0, self.coreset0NumRbs), width=self.bitwidthCoreset0))
            
        #when validation passed
        return True
    
    def validateCss0(self):
        if not self.nrMibCss0Edit.text() or not self.flagCoreset0:
            return False
        
        self.ngwin.logEdit.append('-->inside validateCss0')
        
        if self.coreset0MultiplexingPat == 1:
            if self.freqRange == 'FR1':
                return True
        
            if self.freqRange == 'FR2' and int(self.nrMibCss0Edit.text()) in range(14):
                return True
            else:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid CSS0 setting: searchSpaceZero can be [0, 13] for CORESET0/CSS0 with multiplexing pattern 1 and FR2!' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                return False
        else:   #self.coreset0MultiplexingPat = 2/3
            if int(self.nrMibCss0Edit.text()) == 0:
                return True
            else:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid CSS0 setting: searchSpaceZero can be [0] for CORESET0/CSS0 with multiplexing pattern %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.coreset0MultiplexingPat))
                return False
    
    def onMibCoreset0EditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onMibCoreset0EditTextChanged')
        self.flagCoreset0 = self.validateCoreset0()
        if self.flagCoreset0:
            self.updateKSsbAndNCrbSsb(offset=0 if self.coreset0Offset <= 0 else self.coreset0Offset)
            self.flagCss0 = self.validateCss0()
            
    def onMibCss0EditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onMibCss0EditTextChanged')
        self.flagCss0 = self.validateCss0()
                
    def onSsbKssbEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onSsbKssbEditTextChanged')
        self.flagCoreset0 = self.validateCoreset0()
        if self.flagCoreset0:
            self.updateKSsbAndNCrbSsb(offset=0 if self.coreset0Offset <= 0 else self.coreset0Offset)
            
    def onMibDmrsTypeAPosCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onMibDmrsTypeAPosCombCurIndChanged, index=%d' % index)
        #validate coreset0 duration
        self.flagCoreset0 = self.validateCoreset0()
        
        #validate coreset1 duration
        coreset1Duration = int(self.nrCoreset1DurationComb.currentText())
        if coreset1Duration == 3 and int(self.nrMibDmRsTypeAPosComb.currentText()[3:]) != 3:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid setting: coreset1Duration = %s but dmrs-TypeA-Position = "%s"! Reset coreset1Duration to "2".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrCoreset1DurationComb.currentText(), self.nrMibDmRsTypeAPosComb.currentText()))
            self.nrCoreset1DurationComb.setCurrentText('2')
        
        #validate 'time domain resource assignment' of dci
        self.validateDci10Sib1TimeAllocField()
        self.validateDci10Msg2TimeAllocField()
        self.validateDci10Msg4TimeAllocField()
        if self.nrDci11PdschTimeAllocFieldEdit.text():
            timeAllocFieldDci11 = int(self.nrDci11PdschTimeAllocFieldEdit.text())
            if timeAllocFieldDci11 in range(16):
                self.validateDci11PdschTimeAllocField()
            else:
                if self.nrDci11PdschTimeAllocMappingTypeComb.currentText() == 'Type A' and self.nrDci11PdschTimeAllocSEdit.text() and int(self.nrDci11PdschTimeAllocSEdit.text()) == 3 and self.nrMibDmRsTypeAPosComb.currentText() != 'pos3':
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid setting: S of SLIV = %s but dmrs-TypeA-Position = "%s" when PDSCH mapping type is "Type A"!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrDci11PdschTimeAllocSEdit.text(), self.nrMibDmRsTypeAPosComb.currentText()))
                    self.nrDci11PdschTimeAllocSEdit.clear()
        
        #validate 'dmrs-AdditionalPosition' of dmrs for pdsch
        if self.nrDmrsDedPdschAddPosComb.currentText() == 'pos3' and self.nrMibDmRsTypeAPosComb.currentText() != 'pos2':
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: The case dmrs-AdditionalPosition equals to "pos3" is only supported when dmrs-TypeA-Position is equal to "pos2"! Reset dmrs-AdditionalPosition to "pos0".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            self.nrDmrsDedPdschAddPosComb.setCurrentText('pos0')
            return
        
    def onUeAntPortsCombCurIndChanged(self, index):
        if index < 0:
            pass
        
        self.ngwin.logEdit.append('-->inside onUeAntPortsCombCurIndChanged, index=%d' % index)
        self.updateDedPuschCfgLabel()
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
            self.updateDci01PrecodingLayersFieldLabel()
    
    def updateDedPuschCfgLabel(self):
        self.ngwin.logEdit.append('-->inside updateDedPuschCfgLabel') 
        
        numUeAp = int(self.nrUeAntPortsComb.currentText()[:-2])
        tp = self.nrDedPuschCfgTpComb.currentText()
        if numUeAp == 1:
            self.nrDedPuschCfgCbMaxRankLabel.setText('CB maxRank[1]:')
            self.nrDedPuschCfgCbMaxRankEdit.setText('1')
            self.nrDedPuschCfgCbMaxRankEdit.setValidator(QIntValidator(1, 1))
            self.nrDedPuschCfgNonCbMaxLayersLabel.setText('non-CB maxLayers(Lmax)[1]:')
            self.nrDedPuschCfgNonCbMaxLayersEdit.setText('1')
            self.nrDedPuschCfgNonCbMaxLayersEdit.setValidator(QIntValidator(1, 1))
            
            self.nrDedPuschCfgCbSubsetComb.setEnabled(False)
            self.nrDci01PuschPrecodingLayersFieldEdit.clear()
            self.nrDci01PuschPrecodingLayersFieldEdit.setEnabled(False)
        else:
            if tp == 'disabled':
                self.nrDedPuschCfgCbMaxRankLabel.setText('CB maxRank[1-%s]:' % numUeAp)
                self.nrDedPuschCfgCbMaxRankEdit.setText(str(numUeAp))
                self.nrDedPuschCfgCbMaxRankEdit.setValidator(QIntValidator(1, numUeAp))
                self.nrDedPuschCfgNonCbMaxLayersLabel.setText('non-CB maxLayers(Lmax)[1-%s]:' % numUeAp)
                self.nrDedPuschCfgNonCbMaxLayersEdit.setText(str(numUeAp))
                self.nrDedPuschCfgNonCbMaxLayersEdit.setValidator(QIntValidator(1, numUeAp))
            else:
                self.nrDedPuschCfgCbMaxRankLabel.setText('CB maxRank[1]:')
                self.nrDedPuschCfgCbMaxRankEdit.setText('1')
                self.nrDedPuschCfgCbMaxRankEdit.setValidator(QIntValidator(1, 1))
                self.nrDedPuschCfgNonCbMaxLayersLabel.setText('non-CB maxLayers(Lmax)[1]:')
                self.nrDedPuschCfgNonCbMaxLayersEdit.setText('1')
                self.nrDedPuschCfgNonCbMaxLayersEdit.setValidator(QIntValidator(1, 1))
                
            if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
                self.nrDedPuschCfgCbSubsetComb.setEnabled(True)
                if numUeAp == 2:
                    self.nrDedPuschCfgCbSubsetComb.clear()
                    self.nrDedPuschCfgCbSubsetComb.addItems(['fullyAndPartialAndNonCoherent', 'nonCoherent'])
                else:
                    self.nrDedPuschCfgCbSubsetComb.clear()
                    self.nrDedPuschCfgCbSubsetComb.addItems(['fullyAndPartialAndNonCoherent', 'partialAndNonCoherent', 'nonCoherent'])
                self.nrDci01PuschPrecodingLayersFieldEdit.setEnabled(True)
            else:
                self.nrDedPuschCfgCbSubsetComb.setEnabled(False)
                self.nrDci01PuschPrecodingLayersFieldEdit.setEnabled(False)
        
    def onTddCfgPat2PeriodCombCurIndChanged(self, index):
        if index < 0:
            pass
        
        self.ngwin.logEdit.append('-->inside onTddCfgPat2PeriodCombCurIndChanged, index=%d' % index)
        if index == 0:
            self.nrTddCfgPat2NumDlSlotsEdit.clear()
            self.nrTddCfgPat2NumDlSymbsEdit.clear()
            self.nrTddCfgPat2NumUlSymbsEdit.clear()
            self.nrTddCfgPat2NumUlSlotsEdit.clear()
        else:
            self.nrTddCfgPat2NumDlSlotsEdit.setText('3')
            self.nrTddCfgPat2NumDlSymbsEdit.setText('10')
            self.nrTddCfgPat2NumUlSymbsEdit.setText('2')
            self.nrTddCfgPat2NumUlSlotsEdit.setText('1')
    
    def onCss0AggLevelCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onCss0AggLevelCombCurIndChanged, index=%d' % index)
        self.nrCss0NumCandidatesComb.setCurrentText('n%d' % (16 // int(self.nrCss0AggLevelComb.currentText())))
        
    def onCss0NumCandidatesCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onCss0NumCandidatesCombCurIndChanged, index=%d' % index)
        maxNumCandidates = 16 // int(self.nrCss0AggLevelComb.currentText())
        if int(self.nrCss0NumCandidatesComb.currentText()[1:]) > maxNumCandidates:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Max number of PDCCH candidates of AL=%s for CSS0 is %d!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrCss0AggLevelComb.currentText(), maxNumCandidates))
            self.nrCss0AggLevelComb.setCurrentText('n%d' % maxNumCandidates)
    
    def onPrachConfIndEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onPrachConfIndEditTextChanged')
        self.updateRachConfig()
    
    def onDsrRes0PeriodicityCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDsrRes0PeriodicityCombCurIndChanged, index=%d' % index)
        if self.nrDsrRes0PeriodicityComb.currentText() in ('sym2', 'sym6or7', 'sl1'):
            self.nrDsrRes0OffsetLabel.setText('Offset(in slots)[0]:')
            self.nrDsrRes0OffsetEdit.setText('0')
            self.nrDsrRes0OffsetEdit.setValidator(QIntValidator(0, 0))
        else:
            period = int(self.nrDsrRes0PeriodicityComb.currentText()[2:])
            self.nrDsrRes0OffsetLabel.setText('Offset(in slots)[0-%d]:' % (period-1))
            self.nrDsrRes0OffsetEdit.setText('0')
            self.nrDsrRes0OffsetEdit.setValidator(QIntValidator(0, period-1))
            
    def onDsrRes1PeriodicityCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDsrRes1PeriodicityCombCurIndChanged, index=%d' % index)
        if self.nrDsrRes1PeriodicityComb.currentText() in ('sym2', 'sym6or7', 'sl1'):
            self.nrDsrRes1OffsetLabel.setText('Offset(in slots)[0]:')
            self.nrDsrRes1OffsetEdit.setText('0')
            self.nrDsrRes1OffsetEdit.setValidator(QIntValidator(0, 0))
        else:
            period = int(self.nrDsrRes1PeriodicityComb.currentText()[2:])
            self.nrDsrRes1OffsetLabel.setText('Offset(in slots)[0-%d]:' % (period-1))
            self.nrDsrRes1OffsetEdit.setText('0')
            self.nrDsrRes1OffsetEdit.setValidator(QIntValidator(0, period-1))
    
    def onIniDlBwpLocAndBwEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onIniDlBwpLocAndBwEditTextChanged')
        riv = int(self.nrIniDlBwpGenericLocAndBwEdit.text())
        L_RBs, RB_start= self.parseRiv(riv, 275)
        if L_RBs is not None and RB_start is not None: 
            commonScs = int(self.nrMibScsCommonComb.currentText()[:-3])
            if self.freqRange == 'FR1':
                numRbCommonScs = self.nrNrbFr1[commonScs][self.nrBwSetFr1.index(self.nrCarrierBwComb.currentText())]
            else:
                numRbCommonScs = self.nrNrbFr2[commonScs][self.nrBwSetFr2.index(self.nrCarrierBwComb.currentText())]
            #numRbCarrierScs = int(self.nrCarrierNumRbEdit.text())
            #FIXME
            #initial dl bwp need to check against coreset0 bw
            if L_RBs < 1 or L_RBs > (numRbCommonScs - RB_start):
                self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: RIV = %s, L_RBs = %s, RB_start = %s with bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), riv, L_RBs, RB_start, numRbCommonScs))
                self.nrIniDlBwpGenericLRbsEdit.clear()
                self.nrIniDlBwpGenericRbStartEdit.clear()
                return
            
            self.nrIniDlBwpGenericLRbsEdit.setText(str(L_RBs))
            self.nrIniDlBwpGenericRbStartEdit.setText(str(RB_start))
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %d!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), riv)) 
            self.nrIniDlBwpGenericLRbsEdit.clear()
            self.nrIniDlBwpGenericRbStartEdit.clear()
            
    
    def onIniDlBwpLRBsOrRBStartEditTextChanged(self, text):
        if not self.nrIniDlBwpGenericLRbsEdit.text() or not self.nrIniDlBwpGenericRbStartEdit.text():
            return
        
        if int(self.nrIniDlBwpGenericLRbsEdit.text()) <= 1:
            self.nrIniDlBwpGenericLocAndBwEdit.clear()
            return
        
        self.ngwin.logEdit.append('-->inside onIniDlBwpLRBsOrRBStartEditTextChanged')
        L_RBs = int(self.nrIniDlBwpGenericLRbsEdit.text())
        RB_start = int(self.nrIniDlBwpGenericRbStartEdit.text())
        commonScs = int(self.nrMibScsCommonComb.currentText()[:-3])
        if self.freqRange == 'FR1':
            numRbCommonScs = self.nrNrbFr1[commonScs][self.nrBwSetFr1.index(self.nrCarrierBwComb.currentText())]
        else:
            numRbCommonScs = self.nrNrbFr2[commonScs][self.nrBwSetFr2.index(self.nrCarrierBwComb.currentText())]
        #numRbCarrierScs = int(self.nrCarrierNumRbEdit.text())
        if L_RBs < 1 or L_RBs > (numRbCommonScs - RB_start):
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: L_RBs = %s, RB_start = %s with bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), L_RBs, RB_start, numRbCommonScs))
            self.nrIniDlBwpGenericLocAndBwEdit.clear()
            return
        
        riv = self.makeRiv(L_RBs, RB_start, 275)
        if riv is not None and riv in range(37950):
            self.nrIniDlBwpGenericLocAndBwEdit.setText(str(riv))
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %s(with L_RBs = %s, RB_start = %s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if riv is None else str(riv), L_RBs, RB_start))
            self.nrIniDlBwpGenericLocAndBwEdit.clear()
            
    def onIniDlBwpCpCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onIniDlBwpCpCombCurIndChanged, index=%d' % index)
        self.validateDci10Msg2TimeAllocField()
        self.validateDci10Msg4TimeAllocField()
    
    def onIniUlBwpLocAndBwEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onIniUlBwpLocAndBwEditTextChanged')
        riv = int(self.nrIniUlBwpGenericLocAndBwEdit.text())
        L_RBs, RB_start= self.parseRiv(riv, 275)
        if L_RBs is not None and RB_start is not None: 
            numRbCarrierScs = int(self.nrCarrierNumRbEdit.text())
            if L_RBs < 1 or L_RBs > (numRbCarrierScs - RB_start):
                self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: RIV = %s, L_RBs = %s, RB_start = %s with carrier bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), riv, L_RBs, RB_start, numRbCarrierScs))
                self.nrIniUlBwpGenericLRbsEdit.clear()
                self.nrIniUlBwpGenericRbStartEdit.clear()
                return
            
            self.nrIniUlBwpGenericLRbsEdit.setText(str(L_RBs))
            self.nrIniUlBwpGenericRbStartEdit.setText(str(RB_start))
            self.updateIniUlBwpInfo()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %d!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), riv)) 
            self.nrIniUlBwpGenericLRbsEdit.clear()
            self.nrIniUlBwpGenericRbStartEdit.clear()
    
    def onIniUlBwpLRBsOrRBStartEditTextChanged(self, text):
        if not self.nrIniUlBwpGenericLRbsEdit.text() or not self.nrIniUlBwpGenericRbStartEdit.text():
            return
        
        if int(self.nrIniUlBwpGenericLRbsEdit.text()) <= 1:
            self.nrIniUlBwpGenericLocAndBwEdit.clear()
            return
        
        self.ngwin.logEdit.append('-->inside onIniUlBwpLRBsOrRBStartEditTextChanged')
        L_RBs = int(self.nrIniUlBwpGenericLRbsEdit.text())
        RB_start = int(self.nrIniUlBwpGenericRbStartEdit.text())
        numRbCarrierScs = int(self.nrCarrierNumRbEdit.text())
        if L_RBs < 1 or L_RBs > (numRbCarrierScs - RB_start):
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: L_RBs = %s, RB_start = %s with carrier bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), L_RBs, RB_start, numRbCarrierScs))
            self.nrIniUlBwpGenericLocAndBwEdit.clear()
            return
        
        riv = self.makeRiv(L_RBs, RB_start, 275)
        if riv is not None and riv in range(37950):
            self.nrIniUlBwpGenericLocAndBwEdit.setText(str(riv))
            #set 'prb offset' of pucch-sib1 for msg4 harq feedback
            if self.nrPucchSib1PucchResCommonEdit.text() and int(self.nrPucchSib1PucchResCommonEdit.text()) == 15:
                self.nrPucchSib1PrbOffsetEdit.setText(str(math.floor(L_RBs / 4)))
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %s(with L_RBs = %s, RB_start = %s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if riv is None else str(riv), L_RBs, RB_start))
            self.nrIniUlBwpGenericLocAndBwEdit.clear()
    
    def onDedDlBwpLocAndBwEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onDedDlBwpLocAndBwEditTextChanged')
        riv = int(self.nrDedDlBwpGenericLocAndBwEdit.text())
        L_RBs, RB_start= self.parseRiv(riv, 275)
        if L_RBs is not None and RB_start is not None: 
            numRbCarrierScs = int(self.nrCarrierNumRbEdit.text())
            if L_RBs < 1 or L_RBs > (numRbCarrierScs - RB_start):
                self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: RIV = %s, L_RBs = %s, RB_start = %s with carrier bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), riv, L_RBs, RB_start, numRbCarrierScs))
                self.nrDedDlBwpGenericLRbsEdit.clear()
                self.nrDedDlBwpGenericRbStartEdit.clear()
                return
            
            self.nrDedDlBwpGenericLRbsEdit.setText(str(L_RBs))
            self.nrDedDlBwpGenericRbStartEdit.setText(str(RB_start))
            self.updateCoreset1FreqRes()
            self.updateDedDlBwpInfo()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %d!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), riv)) 
            self.nrDedDlBwpGenericLRbsEdit.clear()
            self.nrDedDlBwpGenericRbStartEdit.clear()
            
    
    def onDedDlBwpLRBsOrRBStartEditTextChanged(self, text):
        if not self.nrDedDlBwpGenericLRbsEdit.text() or not self.nrDedDlBwpGenericRbStartEdit.text():
            return
        
        if int(self.nrDedDlBwpGenericLRbsEdit.text()) <= 1:
            self.nrDedDlBwpGenericLocAndBwEdit.clear()
            return
        
        self.ngwin.logEdit.append('-->inside onDedDlBwpLRBsOrRBStartEditTextChanged')
        L_RBs = int(self.nrDedDlBwpGenericLRbsEdit.text())
        RB_start = int(self.nrDedDlBwpGenericRbStartEdit.text())
        numRbCarrierScs = int(self.nrCarrierNumRbEdit.text())
        if L_RBs < 1 or L_RBs > (numRbCarrierScs - RB_start):
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: L_RBs = %s, RB_start = %s with carrier bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), L_RBs, RB_start, numRbCarrierScs))
            self.nrDedDlBwpGenericLocAndBwEdit.clear()
            return
        
        riv = self.makeRiv(L_RBs, RB_start, 275)
        if riv is not None and riv in range(37950):
            self.nrDedDlBwpGenericLocAndBwEdit.setText(str(riv))
            self.updateCoreset1FreqRes()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %s(with L_RBs = %s, RB_start = %s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if riv is None else str(riv), L_RBs, RB_start))
            self.nrDedDlBwpGenericLocAndBwEdit.clear()
    
    def onDedUlBwpLocAndBwEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onDedUlBwpLocAndBwEditTextChanged')
        riv = int(self.nrDedUlBwpGenericLocAndBwEdit.text())
        L_RBs, RB_start= self.parseRiv(riv, 275)
        if L_RBs is not None and RB_start is not None: 
            numRbCarrierScs = int(self.nrCarrierNumRbEdit.text())
            if L_RBs < 1 or L_RBs > (numRbCarrierScs - RB_start):
                self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: RIV = %s, L_RBs = %s, RB_start = %s with carrier bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), riv, L_RBs, RB_start, numRbCarrierScs))
                self.nrDedUlBwpGenericLRbsEdit.clear()
                self.nrIniUlBwpGenericRbStartEdit.clear()
                return
            
            self.nrDedUlBwpGenericLRbsEdit.setText(str(L_RBs))
            self.nrDedUlBwpGenericRbStartEdit.setText(str(RB_start))
            self.updateDedUlBwpInfo()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %d!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), riv)) 
            self.nrDedUlBwpGenericLRbsEdit.clear()
            self.nrDedUlBwpGenericRbStartEdit.clear()
            
    
    def onDedUlBwpLRBsOrRBStartEditTextChanged(self, text):
        if not self.nrDedUlBwpGenericLRbsEdit.text() or not self.nrDedUlBwpGenericRbStartEdit.text():
            return
        
        if int(self.nrDedUlBwpGenericLRbsEdit.text()) <= 1:
            self.nrDedUlBwpGenericLocAndBwEdit.clear()
            return
        
        self.ngwin.logEdit.append('-->inside onDedUlBwpLRBsOrRBStartEditTextChanged')
        L_RBs = int(self.nrDedUlBwpGenericLRbsEdit.text())
        RB_start = int(self.nrDedUlBwpGenericRbStartEdit.text())
        numRbCarrierScs = int(self.nrCarrierNumRbEdit.text())
        if L_RBs < 1 or L_RBs > (numRbCarrierScs - RB_start):
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: L_RBs = %s, RB_start = %s with carrier bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), L_RBs, RB_start, numRbCarrierScs))
            self.nrDedUlBwpGenericLocAndBwEdit.clear()
            return
        
        riv = self.makeRiv(L_RBs, RB_start, 275)
        if riv is not None and riv in range(37950):
            self.nrDedUlBwpGenericLocAndBwEdit.setText(str(riv))
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %s(with L_RBs = %s, RB_start = %s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if riv is None else str(riv), L_RBs, RB_start))
            self.nrDedUlBwpGenericLocAndBwEdit.clear()
            
    def onCoreset1DurationCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onCoreset1DurationCombCurIndChanged, index=%d' % index)
        coreset1Duration = int(self.nrCoreset1DurationComb.currentText())
        
        #validate coreset1 duration against dmrs-TypeA-Position in MIB
        if coreset1Duration == 3 and int(self.nrMibDmRsTypeAPosComb.currentText()[3:]) != 3:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid setting: coreset1Duration = %s but dmrs-TypeA-Position = "%s"! Reset coreset1Duration to 1.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrCoreset1DurationComb.currentText(), self.nrMibDmRsTypeAPosComb.currentText()))
            self.nrCoreset1DurationComb.setCurrentIndex(0)
            return
        
        #set values of reg-BundleSize for interleaved CCE-to-REG mapping
        if self.nrCoreset1CceRegMapComb.currentText() == 'interleaved':
            if coreset1Duration == 1:
                self.nrCoreset1RegBundleSizeComb.clear()
                self.nrCoreset1RegBundleSizeComb.addItems(['n2', 'n6'])
                self.nrCoreset1RegBundleSizeComb.setCurrentIndex(0)
            else:
                self.nrCoreset1RegBundleSizeComb.clear()
                self.nrCoreset1RegBundleSizeComb.addItems(['n%d' % coreset1Duration, 'n6'])
                self.nrCoreset1RegBundleSizeComb.setCurrentIndex(0)
        
        #set 'uss first symbols' edit
        tmpList = ['0']*14
        defSymbOff = 2 if coreset1Duration in (1, 2) else coreset1Duration
        for i in range(0, 14, defSymbOff):
            if i + coreset1Duration <= 14:
                tmpList[i] = '1'
                
        tmpList.insert(7, ',')
        self.nrUssFirstSymbsEdit.setText(''.join(tmpList))
        
                
    def onCoreset1CceRegMapCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onCoreset1CceRegMapCombCurIndChanged, index=%d' % index)
        if self.nrCoreset1CceRegMapComb.currentText() == 'nonInterleaved':
            self.nrCoreset1RegBundleSizeComb.setEnabled(False)
            self.nrCoreset1InterleaverSizeComb.setEnabled(False)
            self.nrCoreset1ShiftIndexEdit.setEnabled(False)
        else:
            self.nrCoreset1RegBundleSizeComb.setEnabled(True)
            self.nrCoreset1InterleaverSizeComb.setEnabled(True)
            self.nrCoreset1ShiftIndexEdit.setEnabled(True)
            coreset1Duration = int(self.nrCoreset1DurationComb.currentText())
            if coreset1Duration == 1:
                self.nrCoreset1RegBundleSizeComb.clear()
                self.nrCoreset1RegBundleSizeComb.addItems(['n2', 'n6'])
                self.nrCoreset1RegBundleSizeComb.setCurrentIndex(0)
            else:
                self.nrCoreset1RegBundleSizeComb.clear()
                self.nrCoreset1RegBundleSizeComb.addItems(['n%d' % coreset1Duration, 'n6'])
                self.nrCoreset1RegBundleSizeComb.setCurrentIndex(0)
                
    def onUssFirstSymbsEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onUssFirstSymbsEditTextChanged')
        self.validateUssFirstSymbs()
    
    def validateUssFirstSymbs(self):
        if len(self.nrUssFirstSymbsEdit.text()) != 15:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Length of monitoringSymbolsWithinSlot for USS with CORESET1 must be 14.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            return
        
        self.ngwin.logEdit.append('-->inside validateUssFirstSymbs')
        
        text = self.nrUssFirstSymbsEdit.text()[:7] + self.nrUssFirstSymbsEdit.text()[-7:]
        #refer to 3GPP 38.213 10.1
        #If the higher layer parameter monitoringSymbolsWithinSlot indicates to a UE to monitor PDCCH in a subset of up to three consecutive symbols that are same in every slot where the UE monitors PDCCH for all search space sets, the UE does not expect to be configured with a PDCCH subcarrier spacing other than 15 kHz if the subset includes at least one symbol after the third symbol.
        subText = text[2:]
        if subText.find('111') >= 0 or subText.find('11') >= 0:
            if int(self.nrDedDlBwpGenericScsComb.currentText()[:-3]) != 15:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid setting of monitoringSymbolsWithinSlot for USS with CORESET1.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                self.ngwin.logEdit.append('If the higher layer parameter monitoringSymbolsWithinSlot indicates to a UE to monitor PDCCH in a subset of up to three' 
                    'consecutive symbols that are same in every slot where the UE monitors PDCCH for all search space sets, the UE does not expect to be configured with a'
                    'PDCCH subcarrier spacing other than 15 kHz if the subset includes at least one symbol after the third symbol.')
                return
        
        #A UE does not expect to be provided a first symbol and a number of consecutive symbols for a control resource set that results to a PDCCH candidate mapping to symbols of different slots.
        coreset1Duration = int(self.nrCoreset1DurationComb.currentText())
        oneList = [i for i in range(len(text)) if text[i] == '1']
        for i in oneList:
            if i + coreset1Duration > 14:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid setting of monitoringSymbolsWithinSlot for USS with CORESET1.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                self.ngwin.logEdit.append('A UE does not expect to be provided a first symbol and a number of consecutive symbols for a control resource set that results'
                    'to a PDCCH candidate mapping to symbols of different slots.')
                return
                    
        #A UE does not expect any two PDCCH monitoring occasions, for a same search space set or for different search space sets, in a same control resource set to be separated by a non-zero number of symbols that is smaller than the control resource set duration.
        for i in range(len(oneList)-1):
            if oneList[i+1] - oneList[i] < coreset1Duration:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid setting of monitoringSymbolsWithinSlot for USS with CORESET1.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                self.ngwin.logEdit.append('A UE does not expect any two PDCCH monitoring occasions, for a same search space set or for different search space sets, in a'
                    'same control resource set to be separated by a non-zero number of symbols that is smaller than the control resource set duration.')
                return
    
    def onDci10Sib1TimeAllocFieldEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onDci10Sib1TimeAllocFieldEditTextChanged')
        self.validateDci10Sib1TimeAllocField()
        
    def onDci10Msg2TimeAllocFieldEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onDci10Msg2TimeAllocFieldEditTextChanged')
        self.validateDci10Msg2TimeAllocField()
        
    def onDci10Msg4TimeAllocFieldEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onDci10Msg4TimeAllocFieldEditTextChanged')
        self.validateDci10Msg4TimeAllocField()
    
    def onDci11PdschTimeAllocFieldEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onDci11PdschTimeAllocFieldEditTextChanged')
        self.validateDci11PdschTimeAllocField()
    
    def onMsg3PuschTimeAllocFieldEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onMsg3PuschTimeAllocFieldEditTextChanged')
        self.validateMsg3PuschTimeAllocField()
    
    def onDci01PuschTimeAllocFieldEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschTimeAllocFieldEditTextChanged')
        self.validateDci01PuschTimeAllocField()
    
    def validateDci10Sib1TimeAllocField(self):
        if not self.nrDci10Sib1TimeAllocFieldEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside validateDci10Sib1TimeAllocField')
        row = int(self.nrDci10Sib1TimeAllocFieldEdit.text()) + 1
        key = '%s_%s' % (row, self.nrMibDmRsTypeAPosComb.currentText()[3:])
        if self.coreset0MultiplexingPat == 1:
            if not key in self.nrPdschTimeAllocDefANormCp.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPdschTimeAllocDefANormCp.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                self.nrDci10Sib1TimeAllocFieldEdit.clear()
                return
            
            val = self.nrPdschTimeAllocDefANormCp[key]
        elif self.coreset0MultiplexingPat == 2:
            if row in self.nrPdschTimeAllocDefBNote1Set:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Row %s is not used for SIB1(SI-RNTI with CSS Type0).' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), row))
                self.nrDci10Sib1TimeAllocFieldEdit.clear()
                return
            
            if not key in self.nrPdschTimeAllocDefB.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPdschTimeAllocDefB.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                self.nrDci10Sib1TimeAllocFieldEdit.clear()
                return
            
            val = self.nrPdschTimeAllocDefB[key]
        else: #self.coreset0MultiplexingPat == 3
            if row in self.nrPdschTimeAllocDefCNote1Set:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Row %s is not used for SIB1(SI-RNTI with CSS Type0).' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), row))
                self.nrDci10Sib1TimeAllocFieldEdit.clear()
                return
            
            if not key in self.nrPdschTimeAllocDefC.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPdschTimeAllocDefC.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                self.nrDci10Sib1TimeAllocFieldEdit.clear()
                return
            
            val = self.nrPdschTimeAllocDefC[key]
        
        mappingType, k0, s, l = val
        self.nrDci10Sib1TimeAllocMappingTypeComb.setCurrentText(mappingType)
        self.nrDci10Sib1TimeAllocK0Edit.setText(str(k0))
        self.nrDci10Sib1TimeAllocSlivEdit.setText(str(self.toSliv(s, l, sch='pdsch', type=mappingType, cp='normal')))
        self.nrDci10Sib1TimeAllocSEdit.setText(str(s))
        self.nrDci10Sib1TimeAllocLEdit.setText(str(l))
        
        #set 'number of cdm group(s) without data' of dmrs for sib1
        if l == 2:
            self.nrDmrsSib1CdmGroupsWoDataEdit.setText('1')
        else:
            self.nrDmrsSib1CdmGroupsWoDataEdit.setText('2')
            
        #set 'dmrs-additionalPosition' of dmrs for sib1
        if mappingType == 'Type A':
            self.nrDmrsSib1AddPosComb.setCurrentText('pos2')
        else:
            if l == 7:#always normal cp for sib1
                self.nrDmrsSib1AddPosComb.setCurrentText('pos1')
            else:
                self.nrDmrsSib1AddPosComb.setCurrentText('pos0')
        
        #update tbs
        self.updateDci10Sib1Tbs()
        
    def updateDci10Sib1Tbs(self):
        self.ngwin.logEdit.append('-->inside updateDci10Sib1Tbs')
        if not self.nrDci10Sib1TimeAllocFieldEdit.text() or not self.nrDci10Sib1TimeAllocLEdit.text() or not self.nrDci10Sib1TimeAllocSEdit.text() or not self.nrDci10Sib1TimeAllocSlivEdit.text():
            return
        
        if not self.nrDci10Sib1FreqAllocType1LRbsEdit.text() or not self.nrDci10Sib1FreqAllocType1RbStartEdit.text() or not self.nrDci10Sib1FreqAllocFieldEdit.text():
            return
        
        if not self.nrDci10Sib1Cw0McsEdit.text():
            return
        
        td = int(self.nrDci10Sib1TimeAllocLEdit.text())
        fd = int(self.nrDci10Sib1FreqAllocType1LRbsEdit.text())
        mcs = int(self.nrDci10Sib1Cw0McsEdit.text())
            
        #calculate dmrs overhead
        key = '%s_%s_%s' % (td, self.nrDci10Sib1TimeAllocMappingTypeComb.currentText(), self.nrDmrsSib1AddPosComb.currentText())
        if not key in self.nrDmrsPdschPosOneSymb.keys() or self.nrDmrsPdschPosOneSymb[key] is None:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDmrsPdschPosOneSymb!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
            return
        val = self.nrDmrsPdschPosOneSymb[key]
        
        #refer to 3GPP 38.211 vf30
        #For PDSCH mapping type A, duration of 3 and 4 symbols in Tables 7.4.1.1.2-3 and 7.4.1.1.2-4 respectively is only applicable when dmrs-TypeA-Position is equal to 'pos2'.
        if self.nrDci10Sib1TimeAllocMappingTypeComb.currentText() == 'Type A' and td in (3, 4) and self.nrMibDmRsTypeAPosComb.currentText() != 'pos2':
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: For PDSCH mapping type A, duration of 3 and 4 symbols in Tables 7.4.1.1.2-3 and 7.4.1.1.2-4 respectively is only applicable when dmrs-TypeA-Position is equal to "pos2".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            return
        
        #FIXME For PDSCH mapping type B, when PDSCH allocation collides with CORESET/SearchSpace
        
        dmrsOh = (2 * int(self.nrDmrsSib1CdmGroupsWoDataEdit.text())) * len(val)
        self.ngwin.logEdit.append('SIB1 DMRS overhead: cdmGroupsWoData=%s, key="%s", val=%s' % (self.nrDmrsSib1CdmGroupsWoDataEdit.text(), key, val))
        
        tbs = self.getTbs(sch='pdsch', tp=0, rnti='si-rnti', tab='qam64', td=td, fd=fd, mcs=mcs, layer=1, dmrs=dmrsOh, xoh=0, scale=1)
        self.nrDci10Sib1TbsEdit.setText(str(tbs) if tbs is not None else '')
    
    def validateDci10Msg2TimeAllocField(self):
        if not self.nrDci10Msg2TimeAllocFieldEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside validateDci10Msg2TimeAllocField')
        row = int(self.nrDci10Msg2TimeAllocFieldEdit.text()) + 1
        key = '%s_%s' % (row, self.nrMibDmRsTypeAPosComb.currentText()[3:])
        if self.nrIniDlBwpGenericCpComb.currentText() == 'normal':
            if not key in self.nrPdschTimeAllocDefANormCp.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPdschTimeAllocDefANormCp.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                self.nrDci10Msg2TimeAllocFieldEdit.clear()
                return
            
            val = self.nrPdschTimeAllocDefANormCp[key]
        else: #self.nrIniDlBwpGenericCpComb.currentText() == 'extended':
            if not key in self.nrPdschTimeAllocDefAExtCp.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPdschTimeAllocDefAExtCp.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                self.nrDci10Msg2TimeAllocFieldEdit.clear()
                return
            
            val = self.nrPdschTimeAllocDefAExtCp[key]
            
        mappingType, k0, s, l = val
        self.nrDci10Msg2TimeAllocMappingTypeComb.setCurrentText(mappingType)
        self.nrDci10Msg2TimeAllocK0Edit.setText(str(k0))
        self.nrDci10Msg2TimeAllocSlivEdit.setText(str(self.toSliv(s, l, sch='pdsch', type=mappingType, cp=self.nrIniDlBwpGenericCpComb.currentText())))
        self.nrDci10Msg2TimeAllocSEdit.setText(str(s))
        self.nrDci10Msg2TimeAllocLEdit.setText(str(l))
        
        #set 'number of cdm group(s) without data' of dmrs for msg2 
        if l == 2:
            self.nrDmrsMsg2CdmGroupsWoDataEdit.setText('1')
        else:
            self.nrDmrsMsg2CdmGroupsWoDataEdit.setText('2')
            
        #set 'dmrs-additionalPosition' of dmrs for msg2 
        if mappingType == 'Type A':
            self.nrDmrsMsg2AddPosComb.setCurrentText('pos2')
        else:
            if (l == 7 and self.nrIniDlBwpGenericCpComb.currentText() == 'normal') or (l == 6 and self.nrIniDlBwpGenericCpComb.currentText() == 'extended'):
                self.nrDmrsMsg2AddPosComb.setCurrentText('pos1')
            else:
                self.nrDmrsMsg2AddPosComb.setCurrentText('pos0')
        
        #update tbs
        self.updateDci10Msg2Tbs()
    
    def updateDci10Msg2Tbs(self):
        self.ngwin.logEdit.append('-->inside updateDci10Msg2Tbs')
        if not self.nrDci10Msg2TimeAllocFieldEdit.text() or not self.nrDci10Msg2TimeAllocLEdit.text() or not self.nrDci10Msg2TimeAllocSEdit.text() or not self.nrDci10Msg2TimeAllocSlivEdit.text():
            return
        
        if not self.nrDci10Msg2FreqAllocType1LRbsEdit.text() or not self.nrDci10Msg2FreqAllocType1RbStartEdit.text() or not self.nrDci10Msg2FreqAllocFieldEdit.text():
            return
        
        if not self.nrDci10Msg2Cw0McsEdit.text():
            return
        
        if not self.nrDci10Msg2TbScalingEdit.text():
            return
        
        td = int(self.nrDci10Msg2TimeAllocLEdit.text())
        fd = int(self.nrDci10Msg2FreqAllocType1LRbsEdit.text())
        mcs = int(self.nrDci10Msg2Cw0McsEdit.text())
        #refer to 3GPP 38.214 vf30
        #Table 5.1.3.2-2: Scaling factor of Ninfo for P-RNTI and RA-RNTI
        scale = {'0':1, '1':0.5, '2':0.25}[self.nrDci10Msg2TbScalingEdit.text()]
            
        #calculate dmrs overhead
        key = '%s_%s_%s' % (td, self.nrDci10Msg2TimeAllocMappingTypeComb.currentText(), self.nrDmrsMsg2AddPosComb.currentText())
        if not key in self.nrDmrsPdschPosOneSymb.keys() or self.nrDmrsPdschPosOneSymb[key] is None:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDmrsPdschPosOneSymb!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
            return
        val = self.nrDmrsPdschPosOneSymb[key]
        
        #refer to 3GPP 38.211 vf30
        #For PDSCH mapping type A, duration of 3 and 4 symbols in Tables 7.4.1.1.2-3 and 7.4.1.1.2-4 respectively is only applicable when dmrs-TypeA-Position is equal to 'pos2'.
        if self.nrDci10Msg2TimeAllocMappingTypeComb.currentText() == 'Type A' and td in (3, 4) and self.nrMibDmRsTypeAPosComb.currentText() != 'pos2':
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: For PDSCH mapping type A, duration of 3 and 4 symbols in Tables 7.4.1.1.2-3 and 7.4.1.1.2-4 respectively is only applicable when dmrs-TypeA-Position is equal to "pos2".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            return
        
        #FIXME For PDSCH mapping type B, when PDSCH allocation collides with CORESET/SearchSpace
        
        dmrsOh = (2 * int(self.nrDmrsMsg2CdmGroupsWoDataEdit.text())) * len(val)
        self.ngwin.logEdit.append('Msg2 DMRS overhead: cdmGroupsWoData=%s, key="%s", val=%s' % (self.nrDmrsMsg2CdmGroupsWoDataEdit.text(), key, val))
        
        tbs = self.getTbs(sch='pdsch', tp=0, rnti='ra-rnti', tab='qam64', td=td, fd=fd, mcs=mcs, layer=1, dmrs=dmrsOh, xoh=0, scale=scale)
        self.nrDci10Msg2TbsEdit.setText(str(tbs) if tbs is not None else '')
        
    def validateDci10Msg4TimeAllocField(self):
        if not self.nrDci10Msg4TimeAllocFieldEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside validateDci10Msg4TimeAllocField')
        row = int(self.nrDci10Msg4TimeAllocFieldEdit.text()) + 1
        key = '%s_%s' % (row, self.nrMibDmRsTypeAPosComb.currentText()[3:])
        if self.nrIniDlBwpGenericCpComb.currentText() == 'normal':
            if not key in self.nrPdschTimeAllocDefANormCp.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPdschTimeAllocDefANormCp.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                self.nrDci10Msg4TimeAllocFieldEdit.clear()
                return
            
            val = self.nrPdschTimeAllocDefANormCp[key]
        else: #self.nrIniDlBwpGenericCpComb.currentText() == 'extended':
            if not key in self.nrPdschTimeAllocDefAExtCp.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPdschTimeAllocDefAExtCp.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                self.nrDci10Msg4TimeAllocFieldEdit.clear()
                return
            
            val = self.nrPdschTimeAllocDefAExtCp[key]
        
        mappingType, k0, s, l = val
        self.nrDci10Msg4TimeAllocMappingTypeComb.setCurrentText(mappingType)
        self.nrDci10Msg4TimeAllocK0Edit.setText(str(k0))
        self.nrDci10Msg4TimeAllocSlivEdit.setText(str(self.toSliv(s, l, sch='pdsch', type=mappingType, cp=self.nrIniDlBwpGenericCpComb.currentText())))
        self.nrDci10Msg4TimeAllocSEdit.setText(str(s))
        self.nrDci10Msg4TimeAllocLEdit.setText(str(l))
        
        #set 'number of cdm group(s) without data' of dmrs for msg4 
        if l == 2:
            self.nrDmrsMsg4CdmGroupsWoDataEdit.setText('1')
        else:
            self.nrDmrsMsg4CdmGroupsWoDataEdit.setText('2')
            
        #set 'dmrs-additionalPosition' of dmrs for msg4 
        if mappingType == 'Type A':
            self.nrDmrsMsg4AddPosComb.setCurrentText('pos2')
        else:
            if (l == 7 and self.nrIniDlBwpGenericCpComb.currentText() == 'normal') or (l == 6 and self.nrIniDlBwpGenericCpComb.currentText() == 'extended'):
                self.nrDmrsMsg4AddPosComb.setCurrentText('pos1')
            else:
                self.nrDmrsMsg4AddPosComb.setCurrentText('pos0')
        
        #update tbs
        self.updateDci10Msg4Tbs()
    
    def updateDci10Msg4Tbs(self):
        self.ngwin.logEdit.append('-->inside updateDci10Msg4Tbs')
        if not self.nrDci10Msg4TimeAllocFieldEdit.text() or not self.nrDci10Msg4TimeAllocLEdit.text() or not self.nrDci10Msg4TimeAllocSEdit.text() or not self.nrDci10Msg4TimeAllocSlivEdit.text():
            return
        
        if not self.nrDci10Msg4FreqAllocType1LRbsEdit.text() or not self.nrDci10Msg4FreqAllocType1RbStartEdit.text() or not self.nrDci10Msg4FreqAllocFieldEdit.text():
            return
        
        if not self.nrDci10Msg4Cw0McsEdit.text():
            return
        
        td = int(self.nrDci10Msg4TimeAllocLEdit.text())
        fd = int(self.nrDci10Msg4FreqAllocType1LRbsEdit.text())
        mcs = int(self.nrDci10Msg4Cw0McsEdit.text())
            
        #calculate dmrs overhead
        key = '%s_%s_%s' % (td, self.nrDci10Msg4TimeAllocMappingTypeComb.currentText(), self.nrDmrsMsg4AddPosComb.currentText())
        if not key in self.nrDmrsPdschPosOneSymb.keys() or self.nrDmrsPdschPosOneSymb[key] is None:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDmrsPdschPosOneSymb!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
            return
        val = self.nrDmrsPdschPosOneSymb[key]
        
        #refer to 3GPP 38.211 vf30
        #For PDSCH mapping type A, duration of 3 and 4 symbols in Tables 7.4.1.1.2-3 and 7.4.1.1.2-4 respectively is only applicable when dmrs-TypeA-Position is equal to 'pos2'.
        if self.nrDci10Msg4TimeAllocMappingTypeComb.currentText() == 'Type A' and td in (3, 4) and self.nrMibDmRsTypeAPosComb.currentText() != 'pos2':
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: For PDSCH mapping type A, duration of 3 and 4 symbols in Tables 7.4.1.1.2-3 and 7.4.1.1.2-4 respectively is only applicable when dmrs-TypeA-Position is equal to "pos2".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            return
        
        #FIXME For PDSCH mapping type B, when PDSCH allocation collides with CORESET/SearchSpace
        
        dmrsOh = (2 * int(self.nrDmrsMsg4CdmGroupsWoDataEdit.text())) * len(val)
        self.ngwin.logEdit.append('Msg4 DMRS overhead: cdmGroupsWoData=%s, key="%s", val=%s' % (self.nrDmrsMsg4CdmGroupsWoDataEdit.text(), key, val))
        
        tbs = self.getTbs(sch='pdsch', tp=0, rnti='tc-rnti', tab='qam64', td=td, fd=fd, mcs=mcs, layer=1, dmrs=dmrsOh, xoh=0, scale=1)
        self.nrDci10Msg4TbsEdit.setText(str(tbs) if tbs is not None else '')
    
    def validateDci11PdschTimeAllocField(self):
        if not self.nrDci11PdschTimeAllocFieldEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside validateDci11PdschTimeAllocField')
        row = int(self.nrDci11PdschTimeAllocFieldEdit.text()) + 1
        if row in range(1, 17):
            #use default time-domain allocation schemes
            key = '%s_%s' % (row, self.nrMibDmRsTypeAPosComb.currentText()[3:])
            if self.nrDedDlBwpGenericCpComb.currentText() == 'normal':
                if not key in self.nrPdschTimeAllocDefANormCp.keys():
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPdschTimeAllocDefANormCp.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    self.nrDci11PdschTimeAllocFieldEdit.clear()
                    return
                
                val = self.nrPdschTimeAllocDefANormCp[key]
            else: #self.nrDedDlBwpGenericCpComb.currentText() == 'extended':
                if not key in self.nrPdschTimeAllocDefAExtCp.keys():
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPdschTimeAllocDefAExtCp.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    self.nrDci11PdschTimeAllocFieldEdit.clear()
                    return
                
                val = self.nrPdschTimeAllocDefAExtCp[key]
            
            self.nrDci11PdschTimeAllocMappingTypeComb.setEnabled(False)
            self.nrDci11PdschTimeAllocK0Edit.setEnabled(False)
            self.nrDci11PdschTimeAllocSlivEdit.setEnabled(False)
            self.nrDci11PdschTimeAllocSEdit.setEnabled(False)
            self.nrDci11PdschTimeAllocLEdit.setEnabled(False)
            
            mappingType, k0, s, l = val
            self.nrDci11PdschTimeAllocMappingTypeComb.setCurrentText(mappingType)
            self.nrDci11PdschTimeAllocK0Edit.setText(str(k0))
            self.nrDci11PdschTimeAllocSlivEdit.setText(str(self.toSliv(s, l, sch='pdsch', type=mappingType, cp=self.nrDedDlBwpGenericCpComb.currentText())))
            self.nrDci11PdschTimeAllocSEdit.setText(str(s))
            self.nrDci11PdschTimeAllocLEdit.setText(str(l))
        else:
            #use user-defined time-domain allocation scheme
            self.nrDci11PdschTimeAllocMappingTypeComb.setEnabled(True)
            self.nrDci11PdschTimeAllocK0Edit.setEnabled(True)
            self.nrDci11PdschTimeAllocSlivEdit.setEnabled(True)
            self.nrDci11PdschTimeAllocSEdit.setEnabled(True)
            self.nrDci11PdschTimeAllocLEdit.setEnabled(True)
    
    def validateMsg3PuschTimeAllocField(self):
        if not self.nrMsg3PuschTimeAllocFieldEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside validateMsg3PuschTimeAllocField')
        key = int(self.nrMsg3PuschTimeAllocFieldEdit.text()) + 1
        if self.nrIniUlBwpGenericCpComb.currentText() == 'normal':
            if not key in self.nrPuschTimeAllocDefANormCp.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPuschTimeAllocDefANormCp.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                self.nrMsg3PuschTimeAllocFieldEdit.clear()
                return
            
            val = self.nrPuschTimeAllocDefANormCp[key]
        else: #self.nrIniUlBwpGenericCpComb.currentText() == 'extended':
            if not key in self.nrPuschTimeAllocDefAExtCp.keys():
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPuschTimeAllocDefAExtCp.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                self.nrMsg3PuschTimeAllocFieldEdit.clear()
                return
            
            val = self.nrPuschTimeAllocDefAExtCp[key]
        
        mappingType, k2, s, l = val
        self.nrMsg3PuschTimeAllocMappingTypeComb.setCurrentText(mappingType)
        self.nrMsg3PuschTimeAllocK2Edit.setText(str(k2+self.nrPuschTimeAllocK2j[self.nrIniUlBwpGenericScsComb.currentText()]))
        self.nrMsg3PuschTimeAllocSlivEdit.setText(str(self.toSliv(s, l, sch='pusch', type=mappingType, cp=self.nrIniUlBwpGenericCpComb.currentText())))
        self.nrMsg3PuschTimeAllocSEdit.setText(str(s))
        self.nrMsg3PuschTimeAllocLEdit.setText(str(l))
        
        #set 'number of cdm group(s) without data' of dmrs for msg3
        if l <= 2 and self.nrRachMsg3TpComb.currentText() == 'disabled':
            self.nrDmrsMsg3CdmGroupsWoDataEdit.setText('1')
        else:
            self.nrDmrsMsg3CdmGroupsWoDataEdit.setText('2')
        
        #update tbs
        self.updateMsg3PuschTbs()
    
    def updateMsg3PuschTbs(self):
        self.ngwin.logEdit.append('-->inside updateMsg3PuschTbs')
        
        if not self.nrMsg3PuschTimeAllocFieldEdit.text() or not self.nrMsg3PuschTimeAllocLEdit.text() or not self.nrMsg3PuschTimeAllocSEdit.text() or not self.nrMsg3PuschTimeAllocSlivEdit.text():
            return
        
        #update 'cdm groups without data' of dmrs for msg3 pusch
        td = int(self.nrMsg3PuschTimeAllocLEdit.text())
        if td <= 2 and self.nrRachMsg3TpComb.currentText() == 'disabled':
            cdmGroups = 1
        else:
            cdmGroups = 2
        self.nrDmrsMsg3CdmGroupsWoDataEdit.setText(str(cdmGroups))
        
        #set tbs by calling getTbs
        if self.nrMsg3PuschFreqAllocTypeComb.currentText() == 'RA Type1' and (not self.nrMsg3PuschFreqAllocType1LRbsEdit.text() or not self.nrMsg3PuschFreqAllocType1RbStartEdit.text() or not self.nrMsg3PuschFreqAllocFieldEdit.text()):
            return
        
        fd = int(self.nrMsg3PuschFreqAllocType1LRbsEdit.text())
        
        if not self.nrMsg3PuschCw0McsEdit.text():
            return
            
        #calculate dmrs overhead
        mappingType = self.nrMsg3PuschTimeAllocMappingTypeComb.currentText()
        freqHop = self.nrMsg3PuschFreqAllocFreqHopComb.currentText()
        #refer to 3GPP 38.214 vf30 6.2.2
        '''
        When transmitted PUSCH is not scheduled by PDCCH format 0_1 with CRC scrambled by C-RNTI, CS-RNTI or MCS-RNTI,... 
        If frequency hopping is disabled:
            -	The UE shall assume dmrs-AdditionalPosition equals to 'pos2' and up to two additional DM-RS can be transmitted according to PUSCH duration, or
        If frequency hopping is enabled:
            -	The UE shall assume dmrs-AdditionalPosition equals to 'pos1' and up to one additional DM-RS can be transmitted according to PUSCH duration.
        '''
        if freqHop == 'enabled':
            #refer to 3GPP 38.211 vf30 6.4.1.1.3
            #if the higher-layer parameter dmrs-AdditionalPosition is not set to 'pos0' and intra-slot frequency hopping is enabled according to clause 7.3.1.1.2 in [4, TS 38.212] and by higher layer, Tables 6.4.1.1.3-6 shall be used assuming dmrs-AdditionalPosition is equal to 'pos1' for each hop.
            #refer to 3GPP 38.214 vf30 6.3
            #In case of intra-slot frequency hopping is configured, the number of symbols in the first hop is given by floor(N_PUSCH_symb/2) , the number of symbols in the second hop is given by N_PUSCH_symb - floor(N_PUSCH_symb/2) , where N_PUSCH_symb is the length of the PUSCH transmission in OFDM symbols in one slot.
            key1 = '%s_%s_%s_%s_1st' % (math.floor(td / 2), mappingType, self.nrMibDmRsTypeAPosComb.currentText()[3:] if mappingType == 'Type A' else '0', 'pos1' if self.nrDmrsMsg3AddPosComb.currentText() != 'pos0' else 'pos0')
            key2 = '%s_%s_%s_%s_2nd' % (td - math.floor(td / 2), mappingType, self.nrMibDmRsTypeAPosComb.currentText()[3:] if mappingType == 'Type A' else '0', 'pos1' if self.nrDmrsMsg3AddPosComb.currentText() != 'pos0' else 'pos0')
            if not key1 in self.nrDmrsPuschPosOneSymbWithIntraSlotFh or not key2 in self.nrDmrsPuschPosOneSymbWithIntraSlotFh or self.nrDmrsPuschPosOneSymbWithIntraSlotFh[key1] is None or self.nrDmrsPuschPosOneSymbWithIntraSlotFh[key2] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(key_1stHop="%s", key_2ndHop="%s") when referring nrDmrsPuschPosOneSymbWithIntraSlotFh!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key1, key2))
                return
            val1 = self.nrDmrsPuschPosOneSymbWithIntraSlotFh[key1]
            val2 = self.nrDmrsPuschPosOneSymbWithIntraSlotFh[key2]
        else:
            key = '%s_%s_%s' % (td, self.nrMsg3PuschTimeAllocMappingTypeComb.currentText(), self.nrDmrsMsg3AddPosComb.currentText())
            if not key in self.nrDmrsPuschPosOneSymbWoIntraSlotFh.keys() or self.nrDmrsPuschPosOneSymbWoIntraSlotFh[key] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDmrsPuschPosOneSymbWoIntraSlotFh!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return
            val = self.nrDmrsPuschPosOneSymbWoIntraSlotFh[key]
        
        #refer to 3GPP 38.211 vf30
        #For PUSCH mapping type A, duration of 4 symbols in Table 6.4.1.1.3-4 is only applicable when dmrs-TypeA-Position is equal to 'pos2'.
        if self.nrMsg3PuschTimeAllocMappingTypeComb.currentText() == 'Type A' and td == 4 and self.nrMibDmRsTypeAPosComb.currentText() != 'pos2':
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: For PUSCH mapping type A, duration of 4 symbols in Table 6.4.1.1.3-4 is only applicable when dmrs-TypeA-Position is equal to "pos2".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            return
        
        if freqHop == 'enabled':
            dmrsOh = (2 * cdmGroups) * (len(val1) + len(val2))
            self.ngwin.logEdit.append('Msg3 PUSCH(RAR UL Grant) DMRS overhead: cdmGroupsWoData=%d, key1="%s", val1=%s, key2="%s", val2=%s' % (cdmGroups, key1, val1, key2, val2))
        else:
            dmrsOh = (2 * cdmGroups) * len(val)
            self.ngwin.logEdit.append('Msg3 PUSCH(RAR UL Grant) DMRS overhead: cdmGroupsWoData=%d, key="%s", val=%s' % (cdmGroups, key, val))
        
        tp = 1 if self.nrRachMsg3TpComb.currentText() == 'enabled' else 0
        mcsCw0 = int(self.nrMsg3PuschCw0McsEdit.text())
        
        tbs = self.getTbs(sch='pusch', tp=tp, rnti='msg3', tab='qam64', td=td, fd=fd, mcs=mcsCw0, layer=1, dmrs=dmrsOh, xoh=0, scale=1)
        self.nrMsg3PuschTbsEdit.setText(str(tbs) if tbs is not None else '')
    
    def validateDci01PuschTimeAllocField(self):
        if not self.nrDci01PuschTimeAllocFieldEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside validateDci01PuschTimeAllocField')
        key = int(self.nrDci01PuschTimeAllocFieldEdit.text()) + 1
        if key in range(1, 17):
            #use default time-domain allocation schemes
            if self.nrDedUlBwpGenericCpComb.currentText() == 'normal':
                if not key in self.nrPuschTimeAllocDefANormCp.keys():
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPuschTimeAllocDefANormCp.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    self.nrDci01PuschTimeAllocFieldEdit.clear()
                    return
                
                val = self.nrPuschTimeAllocDefANormCp[key]
            else: #self.nrDedUlBwpGenericCpComb.currentText() == 'extended':
                if not key in self.nrPuschTimeAllocDefAExtCp.keys():
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrPuschTimeAllocDefAExtCp.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    self.nrDci01PuschTimeAllocFieldEdit.clear()
                    return
                
                val = self.nrPuschTimeAllocDefAExtCp[key]
            
            self.nrDci01PuschTimeAllocMappingTypeComb.setEnabled(False)
            self.nrDci01PuschTimeAllocK2Edit.setEnabled(False)
            self.nrDci01PuschTimeAllocSlivEdit.setEnabled(False)
            self.nrDci01PuschTimeAllocSEdit.setEnabled(False)
            self.nrDci01PuschTimeAllocLEdit.setEnabled(False)
            
            mappingType, k2, s, l = val
            self.nrDci01PuschTimeAllocMappingTypeComb.setCurrentText(mappingType)
            self.nrDci01PuschTimeAllocK2Edit.setText(str(k2+self.nrPuschTimeAllocK2j[self.nrDedUlBwpGenericScsComb.currentText()]))
            self.nrDci01PuschTimeAllocSlivEdit.setText(str(self.toSliv(s, l, sch='pusch', type=mappingType, cp=self.nrDedUlBwpGenericCpComb.currentText())))
            self.nrDci01PuschTimeAllocSEdit.setText(str(s))
            self.nrDci01PuschTimeAllocLEdit.setText(str(l))
        else:
            #use user-defined time-domain allocation scheme
            self.nrDci01PuschTimeAllocMappingTypeComb.setEnabled(True)
            self.nrDci01PuschTimeAllocK2Edit.setEnabled(True)
            self.nrDci01PuschTimeAllocSlivEdit.setEnabled(True)
            self.nrDci01PuschTimeAllocSEdit.setEnabled(True)
            self.nrDci01PuschTimeAllocLEdit.setEnabled(True)
            
    def onDci11PdschTimeAllocSlivEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onDci11PdschTimeAllocSlivEditTextChanged')
        sliv = int(self.nrDci11PdschTimeAllocSlivEdit.text())
        S,L = self.fromSliv(sliv, sch='pdsch', type=self.nrDci11PdschTimeAllocMappingTypeComb.currentText(), cp=self.nrDedDlBwpGenericCpComb.currentText())
        if S is not None and L is not None:
            self.nrDci11PdschTimeAllocSEdit.setText(str(S))
            self.nrDci11PdschTimeAllocLEdit.setText(str(L))
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid SLIV(=%s) and prefix info: type="%s", cp="%s".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), sliv, self.nrDci11PdschTimeAllocMappingTypeComb.currentText(), self.nrDedDlBwpGenericCpComb.currentText()))
            self.nrDci11PdschTimeAllocSEdit.clear()
            self.nrDci11PdschTimeAllocLEdit.clear()
    
    def onDci11PdschTimeAllocSOrLEditTextChanged(self, text):
        if not self.nrDci11PdschTimeAllocSEdit.text() or not self.nrDci11PdschTimeAllocLEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci11PdschTimeAllocSOrLEditTextChanged')
        S = int(self.nrDci11PdschTimeAllocSEdit.text())
        
        #validate S against 'dmrs-TypeA-Position' when mappingType is 'Type A'
        if self.nrDci11PdschTimeAllocMappingTypeComb.currentText() == 'Type A' and S == 3 and self.nrMibDmRsTypeAPosComb.currentText() != 'pos3':
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid setting: S of SLIV = %s but dmrs-TypeA-Position = "%s" when PDSCH mapping type is "Type A"!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), self.nrDci11PdschTimeAllocSEdit.text(), self.nrMibDmRsTypeAPosComb.currentText()))
            self.nrDci11PdschTimeAllocSEdit.clear()
            return
                    
        L = int(self.nrDci11PdschTimeAllocLEdit.text())
        sliv = self.toSliv(S, L, sch='pdsch', type=self.nrDci11PdschTimeAllocMappingTypeComb.currentText(), cp=self.nrDedDlBwpGenericCpComb.currentText())
        if sliv is not None:
            self.nrDci11PdschTimeAllocSlivEdit.setText(str(sliv))
            #update 'tbs' by calling getTbs when necessary
            self.validatePdschAntPorts()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid S/L combination(S=%s, L=%s) and prefix info: type="%s", cp="%s".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), S, L, self.nrDci11PdschTimeAllocMappingTypeComb.currentText(), self.nrDedDlBwpGenericCpComb.currentText()))
            self.nrDci11PdschTimeAllocSlivEdit.clear()
    
    def onDci11MappingTypeOrDedDlBwpCpCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDci11MappingTypeOrDedDlBwpCpCombCurIndChanged, index=%d' % index)
        
        mappingType = self.nrDci11PdschTimeAllocMappingTypeComb.currentText()
        cp = self.nrDedDlBwpGenericCpComb.currentText()
        
        if mappingType == 'Type A':
            if cp == 'normal':
                self.nrDci11PdschTimeAllocSLabel.setText('S(of SLIV)[0-3]:')
                self.nrDci11PdschTimeAllocSEdit.setValidator(QIntValidator(0, 3))
                self.nrDci11PdschTimeAllocLLabel.setText('L(of SLIV)[3-14]:')
                self.nrDci11PdschTimeAllocLEdit.setValidator(QIntValidator(3, 14))
            elif cp == 'extended':
                self.nrDci11PdschTimeAllocSLabel.setText('S(of SLIV)[0-3]:')
                self.nrDci11PdschTimeAllocSEdit.setValidator(QIntValidator(0, 3))
                self.nrDci11PdschTimeAllocLLabel.setText('L(of SLIV)[3-12]:')
                self.nrDci11PdschTimeAllocLEdit.setValidator(QIntValidator(3, 12))
            else:
                return
        elif mappingType == 'Type B':
            if cp == 'normal':
                self.nrDci11PdschTimeAllocSLabel.setText('S(of SLIV)[0-12]:')
                self.nrDci11PdschTimeAllocSEdit.setValidator(QIntValidator(0, 12))
                self.nrDci11PdschTimeAllocLLabel.setText('L(of SLIV)[2,4,7]:')
                self.nrDci11PdschTimeAllocLEdit.setValidator(QIntValidator(2, 7))
            elif cp == 'extended':
                self.nrDci11PdschTimeAllocSLabel.setText('S(of SLIV)[0-10]:')
                self.nrDci11PdschTimeAllocSEdit.setValidator(QIntValidator(0, 10))
                self.nrDci11PdschTimeAllocLLabel.setText('L(of SLIV)[2,4,6]:')
                self.nrDci11PdschTimeAllocLEdit.setValidator(QIntValidator(2, 6))
            else:
                return
        else:
            return
        
        self.nrDci11PdschTimeAllocSlivEdit.clear()
        self.nrDci11PdschTimeAllocSEdit.clear()
        self.nrDci11PdschTimeAllocLEdit.clear()
        
    def onDci01PuschTimeAllocSlivEditTextChanged(self, text):
        if not text:
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschTimeAllocSlivEditTextChanged')
        sliv = int(self.nrDci01PuschTimeAllocSlivEdit.text())
        S,L = self.fromSliv(sliv, sch='pusch', type=self.nrDci01PuschTimeAllocMappingTypeComb.currentText(), cp=self.nrDedUlBwpGenericCpComb.currentText())
        if S is not None and L is not None:
            self.nrDci01PuschTimeAllocSEdit.setText(str(S))
            self.nrDci01PuschTimeAllocLEdit.setText(str(L))
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid SLIV(=%s) and prefix info: type="%s", cp="%s".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), sliv, self.nrDci01PuschTimeAllocMappingTypeComb.currentText(), self.nrDedUlBwpGenericCpComb.currentText()))
            self.nrDci01PuschTimeAllocSEdit.clear()
            self.nrDci01PuschTimeAllocLEdit.clear()
    
    def onDci01PuschTimeAllocSOrLEditTextChanged(self, text):
        if not self.nrDci01PuschTimeAllocSEdit.text() or not self.nrDci01PuschTimeAllocLEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschTimeAllocSOrLEditTextChanged')
        S = int(self.nrDci01PuschTimeAllocSEdit.text())
        L = int(self.nrDci01PuschTimeAllocLEdit.text())
        sliv = self.toSliv(S, L, sch='pusch', type=self.nrDci01PuschTimeAllocMappingTypeComb.currentText(), cp=self.nrDedUlBwpGenericCpComb.currentText())
        if sliv is not None:
            self.nrDci01PuschTimeAllocSlivEdit.setText(str(sliv))
            #update 'tbs' by calling getTbs when necessary
            self.validatePuschAntPorts()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid S/L combination(S=%s, L=%s) and prefix info: type="%s", cp="%s".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), S, L, self.nrDci01PuschTimeAllocMappingTypeComb.currentText(), self.nrDedUlBwpGenericCpComb.currentText()))
            self.nrDci01PuschTimeAllocSlivEdit.clear()
    
    def onDci01MappingTypeOrDedUlBwpCpCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDci01MappingTypeOrDedUlBwpCpCombCurIndChanged, index=%d' % index)
        
        mappingType = self.nrDci01PuschTimeAllocMappingTypeComb.currentText()
        cp = self.nrDedUlBwpGenericCpComb.currentText()
        
        if mappingType == 'Type A':
            if cp == 'normal':
                self.nrDci01PuschTimeAllocSLabel.setText('S(of SLIV)[0]:')
                self.nrDci01PuschTimeAllocSEdit.setValidator(QIntValidator(0, 0))
                self.nrDci01PuschTimeAllocLLabel.setText('L(of SLIV)[4-14]:')
                self.nrDci01PuschTimeAllocLEdit.setValidator(QIntValidator(4, 14))
            elif cp == 'extended':
                self.nrDci01PuschTimeAllocSLabel.setText('S(of SLIV)[0]:')
                self.nrDci01PuschTimeAllocSEdit.setValidator(QIntValidator(0, 0))
                self.nrDci01PuschTimeAllocLLabel.setText('L(of SLIV)[4-12]:')
                self.nrDci01PuschTimeAllocLEdit.setValidator(QIntValidator(4, 12))
            else:
                return
        elif mappingType == 'Type B':
            if cp == 'normal':
                self.nrDci01PuschTimeAllocSLabel.setText('S(of SLIV)[0-13]:')
                self.nrDci01PuschTimeAllocSEdit.setValidator(QIntValidator(0, 13))
                self.nrDci01PuschTimeAllocLLabel.setText('L(of SLIV)[1-14]:')
                self.nrDci01PuschTimeAllocLEdit.setValidator(QIntValidator(1, 14))
            elif cp == 'extended':
                self.nrDci01PuschTimeAllocSLabel.setText('S(of SLIV)[0-12]:')
                self.nrDci01PuschTimeAllocSEdit.setValidator(QIntValidator(0, 12))
                self.nrDci01PuschTimeAllocLLabel.setText('L(of SLIV)[1-12]:')
                self.nrDci01PuschTimeAllocLEdit.setValidator(QIntValidator(1, 12))
            else:
                return
        else:
            return
        
        self.nrDci01PuschTimeAllocSlivEdit.clear()
        self.nrDci01PuschTimeAllocSEdit.clear()
        self.nrDci01PuschTimeAllocLEdit.clear()
    
    def onDci10Sib1Type1LRBsOrRBStartEditTextChanged(self, text):
        if not self.nrDci10Sib1FreqAllocType1LRbsEdit.text() or not self.nrDci10Sib1FreqAllocType1RbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci10Sib1Type1LRBsOrRBStartEditTextChanged')
        L_RBs = int(self.nrDci10Sib1FreqAllocType1LRbsEdit.text())
        RB_start = int(self.nrDci10Sib1FreqAllocType1RbStartEdit.text())
        if L_RBs < 1 or L_RBs > (self.coreset0NumRbs - RB_start):
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: L_RBs = %s, RB_start = %s with CORESET0 bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), L_RBs, RB_start, self.coreset0NumRbs))
            self.nrDci10Sib1FreqAllocFieldEdit.clear()
            return
        
        riv = self.makeRiv(L_RBs, RB_start, self.coreset0NumRbs)
        if riv is not None:
            self.nrDci10Sib1FreqAllocFieldEdit.setText('{:0{width}b}'.format(riv, width=self.bitwidthCoreset0))
            #update tbs
            self.updateDci10Sib1Tbs()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %s(with L_RBs = %s, RB_start = %s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if riv is None else str(riv), L_RBs, RB_start))
            self.nrDci10Sib1FreqAllocFieldEdit.clear()
        
    def onDci10Msg2Type1LRBsOrRBStartEditTextChanged(self, text):
        if not self.nrDci10Msg2FreqAllocType1LRbsEdit.text() or not self.nrDci10Msg2FreqAllocType1RbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci10Msg2Type1LRBsOrRBStartEditTextChanged')
        L_RBs = int(self.nrDci10Msg2FreqAllocType1LRbsEdit.text())
        RB_start = int(self.nrDci10Msg2FreqAllocType1RbStartEdit.text())
        if L_RBs < 1 or L_RBs > (self.coreset0NumRbs - RB_start):
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: L_RBs = %s, RB_start = %s with CORESET0 bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), L_RBs, RB_start, self.coreset0NumRbs))
            self.nrDci10Msg2FreqAllocFieldEdit.clear()
            return
        
        riv = self.makeRiv(L_RBs, RB_start, self.coreset0NumRbs)
        if riv is not None:
            self.nrDci10Msg2FreqAllocFieldEdit.setText('{:0{width}b}'.format(riv, width=self.bitwidthCoreset0))
            #update tbs
            self.updateDci10Msg2Tbs()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %s(with L_RBs = %s, RB_start = %s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if riv is None else str(riv), L_RBs, RB_start))
            self.nrDci10Msg2FreqAllocFieldEdit.clear()
    
    def onDci10Msg4Type1LRBsOrRBStartEditTextChanged(self, text):
        if not self.nrDci10Msg4FreqAllocType1LRbsEdit.text() or not self.nrDci10Msg4FreqAllocType1RbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci10Msg4Type1LRBsOrRBStartEditTextChanged')
        L_RBs = int(self.nrDci10Msg4FreqAllocType1LRbsEdit.text())
        RB_start = int(self.nrDci10Msg4FreqAllocType1RbStartEdit.text())
        if L_RBs < 1 or L_RBs > (self.coreset0NumRbs - RB_start):
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: L_RBs = %s, RB_start = %s with CORESET0 bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), L_RBs, RB_start, self.coreset0NumRbs))
            self.nrDci10Msg4FreqAllocFieldEdit.clear()
            return
        
        riv = self.makeRiv(L_RBs, RB_start, self.coreset0NumRbs)
        if riv is not None:
            self.nrDci10Msg4FreqAllocFieldEdit.setText('{:0{width}b}'.format(riv, width=self.bitwidthCoreset0))
            #update tbs
            self.updateDci10Msg4Tbs()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %s(with L_RBs = %s, RB_start = %s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if riv is None else str(riv), L_RBs, RB_start))
            self.nrDci10Msg4FreqAllocFieldEdit.clear()
    
    def onDedPdschCfgRbgConfigCombCurIndChanged(self, index):
        if index < 0:
            return
        
        if not self.nrDedDlBwpGenericLocAndBwEdit.text() or not self.nrDedDlBwpGenericLRbsEdit.text() or not self.nrDedDlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDedPdschCfgRbgConfigCombCurIndChanged, index=%d' % index)
        bwpSize = int(self.nrDedDlBwpGenericLRbsEdit.text())
        P = self.getNomRbgSizeP(bwpSize, sch='pdsch', config=self.nrDedPdschCfgRbgConfigComb.currentText())
        if P is None:
            self.ngwin.logEdit.append('Error: The nominal RBG size P is None!')
            return
        
        self.nrDedPdschCfgRbgSizeEdit.setText(str(P))
        if self.nrDci11PdschFreqAllocTypeComb.currentText() == 'RA Type0':
            self.updateDedDlBwpInfo()
            
    def onDmrsDedPdschMaxLengthCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDmrsDedPdschMaxLengthCombCurIndChanged, index=%d' % index)
        if self.nrDmrsDedPdschMaxLengthComb.currentText() == 'len1':
            self.nrDmrsDedPdschAddPosComb.clear()
            self.nrDmrsDedPdschAddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        else:
            self.nrDmrsDedPdschAddPosComb.clear()
            self.nrDmrsDedPdschAddPosComb.addItems(['pos0', 'pos1'])
    
    def onDmrsDedPdschDmrsTypeOrMaxLengthCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDmrsDedPdschDmrsTypeOrMaxLengthCombCurIndChanged, index=%d' % index)
        dmrsType = self.nrDmrsDedPdschDmrsTypeComb.currentText()
        maxLength = self.nrDmrsDedPdschMaxLengthComb.currentText()
        
        if dmrsType == 'Type 1' and maxLength == 'len1':
            self.nrDci11PdschAntPortsFieldLabel.setText('Antenna port(s)[0-15]:')
            self.nrDci11PdschAntPortsFieldEdit.setValidator(QIntValidator(0, 15))
            self.nrDci11PdschCw1McsEdit.clear()
            self.nrDci11PdschCw1McsEdit.setEnabled(False)
        elif (dmrsType == 'Type 1' and maxLength == 'len2') or (dmrsType == 'Type 2' and maxLength == 'len1'):
            self.nrDci11PdschAntPortsFieldLabel.setText('Antenna port(s)[0-31]:')
            self.nrDci11PdschAntPortsFieldEdit.setValidator(QIntValidator(0, 31))
            self.nrDci11PdschCw1McsEdit.setEnabled(True)
        else:#dmrsType == 'Type 2' and maxLength == 'len2'
            self.nrDci11PdschAntPortsFieldLabel.setText('Antenna port(s)[0-63]:')
            self.nrDci11PdschAntPortsFieldEdit.setValidator(QIntValidator(0, 63))
            self.nrDci11PdschCw1McsEdit.setEnabled(True)
        
        self.validatePdschCw0McsCw1Mcs()
        
    def onDci10Sib1Cw0McsEditTextChanged(self, text):
        if not self.nrDci10Sib1Cw0McsEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci10Sib1Cw0McsEditTextChanged')
        #update tbs
        self.updateDci10Sib1Tbs()
        
    def onDci10Msg2Cw0McsEditTextChanged(self, text):
        if not self.nrDci10Msg2Cw0McsEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci10Msg2Cw0McsEditTextChanged')
        #update tbs
        self.updateDci10Msg2Tbs()
        
    def onDci10Msg2TbScalingEditTextChanged(self, text):
        if not self.nrDci10Msg2TbScalingEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci10Msg2TbScalingEditTextChanged')
        #update tbs
        self.updateDci10Msg2Tbs()
        
    def onDci10Msg4Cw0McsEditTextChanged(self, text):
        if not self.nrDci10Msg4Cw0McsEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci10Msg4Cw0McsEditTextChanged')
        #update tbs
        self.updateDci10Msg4Tbs()
    
    def onMsg3PuschCw0McsEditTextChanged(self, text):
        if not self.nrMsg3PuschCw0McsEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onMsg3PuschCw0McsEditTextChanged')
        #update tbs
        self.updateMsg3PuschTbs()
    
    def onDci11PdschCw0McsOrCw1McsEditTextChanged(self, text):
        if not self.nrDci11PdschCw0McsEdit.text() and not self.nrDci11PdschCw1McsEdit.text():
            self.nrDci11PdschAntPortsFieldEdit.clear()
            return
        
        self.ngwin.logEdit.append('-->inside onDci11PdschCw0McsOrCw1McsEditTextChanged')
        self.validatePdschCw0McsCw1Mcs()
    
    def validatePdschCw0McsCw1Mcs(self):
        self.ngwin.logEdit.append('-->inside validatePdschCw0McsCw1Mcs')
        if not self.nrDci11PdschCw0McsEdit.text() and not self.nrDci11PdschCw1McsEdit.text():
            self.nrDci11PdschAntPortsFieldEdit.clear()
            return
        
        if not self.nrDci11PdschCw0McsEdit.text() and self.nrDci11PdschCw1McsEdit.text():
            self.ngwin.logEdit.append('<font color=yellow><b>[%s]Warning</font>: Only MCS(CW0) can be set in case of one codeword transmission for PDSCH!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            self.nrDci11PdschCw1McsEdit.clear()
            self.nrDci11PdschAntPortsFieldEdit.clear()
            return
        
        dmrsType = self.nrDmrsDedPdschDmrsTypeComb.currentText()
        maxLength = self.nrDmrsDedPdschMaxLengthComb.currentText()
        numCw = 0
        mcsSet = []
        if self.nrDci11PdschCw0McsEdit.text():
            numCw = numCw + 1
            mcsSet.append(int(self.nrDci11PdschCw0McsEdit.text()))
        else:
            mcsSet.append(None)
            
        if self.nrDci11PdschCw1McsEdit.text():
            numCw = numCw + 1
            mcsSet.append(int(self.nrDci11PdschCw1McsEdit.text()))
        else:
            mcsSet.append(None)
        
        if dmrsType == 'Type 1' and maxLength == 'len1' and numCw == 1:
            self.nrDci11PdschAntPortsFieldLabel.setText('Antenna port(s)[%s]:' % self.nrDci11AntPortsDmrsType1MaxLen1OneCwValid)
        elif dmrsType == 'Type 1' and maxLength == 'len2' and numCw == 1:
            self.nrDci11PdschAntPortsFieldLabel.setText('Antenna port(s)[%s]:' % self.nrDci11AntPortsDmrsType1MaxLen2OneCwValid)
        elif dmrsType == 'Type 1' and maxLength == 'len2' and numCw == 2:
            self.nrDci11PdschAntPortsFieldLabel.setText('Antenna port(s)[%s]:' % self.nrDci11AntPortsDmrsType1MaxLen2TwoCwsValid)
        elif dmrsType == 'Type 2' and maxLength == 'len1' and numCw == 1:
            self.nrDci11PdschAntPortsFieldLabel.setText('Antenna port(s)[%s]:' % self.nrDci11AntPortsDmrsType2MaxLen1OneCwValid)
        elif dmrsType == 'Type 2' and maxLength == 'len1' and numCw == 2:
            self.nrDci11PdschAntPortsFieldLabel.setText('Antenna port(s)[%s]:' % self.nrDci11AntPortsDmrsType2MaxLen1TwoCwsValid)
        elif dmrsType == 'Type 2' and maxLength == 'len2' and numCw == 1:
            self.nrDci11PdschAntPortsFieldLabel.setText('Antenna port(s)[%s]:' % self.nrDci11AntPortsDmrsType2MaxLen2OneCwValid)
        elif dmrsType == 'Type 2' and maxLength == 'len2' and numCw == 2:
            self.nrDci11PdschAntPortsFieldLabel.setText('Antenna port(s)[%s]:' % self.nrDci11AntPortsDmrsType2MaxLen2TwoCwsValid)
        else:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid combination of dmrs-Type(="%s"), maxLength(="%s") and numCw(=%s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), dmrsType, maxLength, numCw))
            return
        
        mcsTable = self.nrDedPdschCfgMcsTableComb.currentText()
        if mcsTable == 'qam256':
            if (mcsSet[0] is not None and mcsSet[0] > 27) or (mcsSet[1] is not None and mcsSet[1] > 27): 
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: MCS(CW0/CW1) should be 0-27 when "mcs-Table" of PDSCH-Config is "%s"!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), mcsTable))
                return
        else:#mcsTable == 'qam64LowSE' or mcsTable == 'qam64'
            if (mcsSet[0] is not None and mcsSet[0] > 28) or (mcsSet[1] is not None and mcsSet[1] > 28): 
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: MCS(CW0/CW1) should be 0-28 when "mcs-Table" of PDSCH-Config is "%s"!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), mcsTable))
                return
        
        if self.nrDci11PdschAntPortsFieldEdit.text():
            self.validatePdschAntPorts()
            
    def onDci11PdschAntPortsEditTextChanged(self, text):
        if not self.nrDci11PdschAntPortsFieldEdit.text():
            self.nrDmrsDedPdschCdmGroupsWoDataEdit.clear()
            self.nrDmrsDedPdschDmrsPortsEdit.clear()
            self.nrDmrsDedPdschFrontLoadSymbsEdit.clear()
            self.nrPtrsPdschDmrsAntPortEdit.clear()
            return
        
        self.ngwin.logEdit.append('-->inside onDci11PdschAntPortsEditTextChanged')
        if not self.nrDci11PdschCw0McsEdit.text() and not self.nrDci11PdschCw1McsEdit.text():
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: MCS(CW0) and/or MCS(CW1) must be set before configuring "Antenna port(s)"!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            self.nrDci11PdschAntPortsFieldEdit.clear()
            return
        
        self.validatePdschAntPorts()
        
    def validatePdschAntPorts(self):
        if not self.nrDci11PdschAntPortsFieldEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside validatePdschAntPorts')
        dmrsType = self.nrDmrsDedPdschDmrsTypeComb.currentText()
        maxLength = self.nrDmrsDedPdschMaxLengthComb.currentText()
        mcsSet = []
        if self.nrDci11PdschCw0McsEdit.text():
            mcsSet.append(int(self.nrDci11PdschCw0McsEdit.text()))
            
        if self.nrDci11PdschCw1McsEdit.text():
            mcsSet.append(int(self.nrDci11PdschCw1McsEdit.text()))
        
        if dmrsType == 'Type 1' and maxLength == 'len1' and len(mcsSet) == 1:
            minVal, maxVal = self.nrDci11AntPortsDmrsType1MaxLen1OneCwValid.split('-')
        elif dmrsType == 'Type 1' and maxLength == 'len2' and len(mcsSet) == 1:
            minVal, maxVal = self.nrDci11AntPortsDmrsType1MaxLen2OneCwValid.split('-')
        elif dmrsType == 'Type 1' and maxLength == 'len2' and len(mcsSet) == 2:
            minVal, maxVal = self.nrDci11AntPortsDmrsType1MaxLen2TwoCwsValid.split('-')
        elif dmrsType == 'Type 2' and maxLength == 'len1' and len(mcsSet) == 1:
            minVal, maxVal = self.nrDci11AntPortsDmrsType2MaxLen1OneCwValid.split('-')
        elif dmrsType == 'Type 2' and maxLength == 'len1' and len(mcsSet) == 2:
            minVal, maxVal = self.nrDci11AntPortsDmrsType2MaxLen1TwoCwsValid.split('-')
        elif dmrsType == 'Type 2' and maxLength == 'len2' and len(mcsSet) == 1:
            minVal, maxVal = self.nrDci11AntPortsDmrsType2MaxLen2OneCwValid.split('-')
        elif dmrsType == 'Type 2' and maxLength == 'len2' and len(mcsSet) == 2:
            minVal, maxVal = self.nrDci11AntPortsDmrsType2MaxLen2TwoCwsValid.split('-')
        else:
            return
        
        ap = int(self.nrDci11PdschAntPortsFieldEdit.text())
        if ap < int(minVal) or ap > int(maxVal):
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid "Antenna port(s)"(=%s), which must be %s-%s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), ap, minVal, maxVal))
            self.nrDci11PdschAntPortsFieldEdit.clear()
            return
        
        #set dmrs for pdsch
        if dmrsType == 'Type 1' and maxLength == 'len1' and len(mcsSet) == 1:
            cdmGroups, dmrsPorts, numDmrsSymbs = self.nrDci11AntPortsDmrsType1MaxLen1OneCw[ap]
        elif dmrsType == 'Type 1' and maxLength == 'len2' and len(mcsSet) == 1:
            cdmGroups, dmrsPorts, numDmrsSymbs = self.nrDci11AntPortsDmrsType1MaxLen2OneCw[ap]
        elif dmrsType == 'Type 1' and maxLength == 'len2' and len(mcsSet) == 2:
            cdmGroups, dmrsPorts, numDmrsSymbs = self.nrDci11AntPortsDmrsType1MaxLen2TwoCws[ap]
        elif dmrsType == 'Type 2' and maxLength == 'len1' and len(mcsSet) == 1:
            cdmGroups, dmrsPorts, numDmrsSymbs = self.nrDci11AntPortsDmrsType2MaxLen1OneCw[ap]
        elif dmrsType == 'Type 2' and maxLength == 'len1' and len(mcsSet) == 2:
            cdmGroups, dmrsPorts, numDmrsSymbs = self.nrDci11AntPortsDmrsType2MaxLen1TwoCws[ap]
        elif dmrsType == 'Type 2' and maxLength == 'len2' and len(mcsSet) == 1:
            cdmGroups, dmrsPorts, numDmrsSymbs = self.nrDci11AntPortsDmrsType2MaxLen2OneCw[ap]
        elif dmrsType == 'Type 2' and maxLength == 'len2' and len(mcsSet) == 2:
            cdmGroups, dmrsPorts, numDmrsSymbs = self.nrDci11AntPortsDmrsType2MaxLen2TwoCws[ap]
        else:
            return
        
        self.nrDmrsDedPdschCdmGroupsWoDataEdit.setText(str(cdmGroups))
        self.nrDmrsDedPdschDmrsPortsEdit.setText(','.join([str(i) for i in dmrsPorts]))
        self.nrDmrsDedPdschFrontLoadSymbsEdit.setText(str(numDmrsSymbs))
        
        #check and set ptrs for pdsch 
        #refer to 3GPP 38.214 vf30 5.1.6.2
        '''
        If a UE receiving PDSCH is configured with the higher layer parameter PTRS-DownlinkConfig, the UE may assume that the following configurations are not occurring simultaneously for the received PDSCH:
            -	any DM-RS ports among 1004-1007 or 1006-1011 for DM-RS configurations type 1 and type 2, respectively are scheduled for the UE and the other UE(s) sharing the DM-RS REs on the same CDM group(s), and
            -	PT-RS is transmitted to the UE.
        '''
        dmrsApSetNoPtrs = list(range(4, 8)) if dmrsType == 'Type 1' else list(range(6, 12))
        noPtrs = False
        for i in dmrsPorts:
            if i in dmrsApSetNoPtrs:
                noPtrs = True
                break
        
        if noPtrs:
            self.nrPtrsPdschSwitchComb.setCurrentText('no')
            self.nrPtrsPdschSwitchComb.setEnabled(False)
            self.nrPtrsPdschDmrsAntPortEdit.clear()
        else:
            self.nrPtrsPdschSwitchComb.setEnabled(True)
            if len(mcsSet) == 1:
                self.nrPtrsPdschDmrsAntPortEdit.setText(str(dmrsPorts[0]))
            elif len(mcsSet) == 2:
                numAntPortsCw0 = math.floor(len(dmrsPorts) / 2)
                if mcsSet[0] >= mcsSet[1]:
                    self.nrPtrsPdschDmrsAntPortEdit.setText(str(dmrsPorts[0]))
                else:
                    self.nrPtrsPdschDmrsAntPortEdit.setText(str(dmrsPorts[numAntPortsCw0]))
            else:
                return
        
        #set tbs by calling getTbs
        if not self.nrDci11PdschTimeAllocFieldEdit.text() or not self.nrDci11PdschTimeAllocLEdit.text() or not self.nrDci11PdschTimeAllocSEdit.text() or not self.nrDci11PdschTimeAllocSlivEdit.text():
            return
        
        if self.nrDci11PdschFreqAllocTypeComb.currentText() == 'RA Type1' and (not self.nrDci11PdschFreqAllocType1LRbsEdit.text() or not self.nrDci11PdschFreqAllocType1RbStartEdit.text() or not self.nrDci11PdschFreqAllocFieldEdit.text()):
            return
        
        if self.nrDci11PdschFreqAllocTypeComb.currentText() == 'RA Type0' and (not self.nrDci11PdschFreqAllocFieldEdit.text() or len(self.nrDci11PdschFreqAllocFieldEdit.text()) != self.bitwidthType0Pdsch or int(self.nrDci11PdschFreqAllocFieldEdit.text(), 2) == 0):
            return
        
        td = int(self.nrDci11PdschTimeAllocLEdit.text())
        if self.nrDci11PdschFreqAllocTypeComb.currentText() == 'RA Type1':
            fd = int(self.nrDci11PdschFreqAllocType1LRbsEdit.text())
        else:
            fd = sum([self.rbgsType0Pdsch[i] for i in range(self.bitwidthType0Pdsch) if self.nrDci11PdschFreqAllocFieldEdit.text()[i] == '1'])
            
        #calculate dmrs overhead
        key = '%s_%s_%s' % (td, self.nrDci11PdschTimeAllocMappingTypeComb.currentText(), self.nrDmrsDedPdschAddPosComb.currentText())
        if numDmrsSymbs == 1:
            if not key in self.nrDmrsPdschPosOneSymb.keys() or self.nrDmrsPdschPosOneSymb[key] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDmrsPdschPosOneSymb!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return
            val = self.nrDmrsPdschPosOneSymb[key]
        else:
            if not key in self.nrDmrsPdschPosTwoSymbs.keys() or self.nrDmrsPdschPosTwoSymbs[key] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDmrsPdschPosTwoSymbs!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return
            val = self.nrDmrsPdschPosOneSymb[key]
        
        #refer to 3GPP 38.211 vf30
        #For PDSCH mapping type A, duration of 3 and 4 symbols in Tables 7.4.1.1.2-3 and 7.4.1.1.2-4 respectively is only applicable when dmrs-TypeA-Position is equal to 'pos2'.
        if self.nrDci11PdschTimeAllocMappingTypeComb.currentText() == 'Type A' and td in (3, 4) and self.nrMibDmRsTypeAPosComb.currentText() != 'pos2':
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: For PDSCH mapping type A, duration of 3 and 4 symbols in Tables 7.4.1.1.2-3 and 7.4.1.1.2-4 respectively is only applicable when dmrs-TypeA-Position is equal to "pos2".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            return
        
        #FIXME For PDSCH mapping type B, when PDSCH allocation collides with CORESET/SearchSpace
        #For PDSCH mapping type B, if the PDSCH duration is 2 or 4 OFDM symbols, only single-symbol DM-RS is supported.
        if self.nrDci11PdschTimeAllocMappingTypeComb.currentText() == 'Type B' and td in (2, 4) and numDmrsSymbs != 1:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: For PDSCH mapping type B, if the PDSCH duration is 2 or 4 OFDM symbols, only single-symbol DM-RS is supported.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            return
        
        dmrsOh = (2 * cdmGroups) * len(val)
        self.ngwin.logEdit.append('PDSCH(DCI 1_1) DMRS overhead: cdmGroupsWoData=%d, key="%s", val=%s' % (cdmGroups, key, val))
        
        tbs = []
        if len(mcsSet) == 1:
            tbs.append(self.getTbs(sch='pdsch', tp=0, rnti='c-rnti', tab=self.nrDedPdschCfgMcsTableComb.currentText(), td=td, fd=fd, mcs=mcsSet[0], layer=len(dmrsPorts), dmrs=dmrsOh, xoh=int(self.nrDedPdschCfgXOverheadComb.currentText()[3:]), scale=1))
        elif len(mcsSet) == 2:
            numAntPortsCw0 = math.floor(len(dmrsPorts) / 2)
            tbs.append(self.getTbs(sch='pdsch', tp=0, rnti='c-rnti', tab=self.nrDedPdschCfgMcsTableComb.currentText(), td=td, fd=fd, mcs=mcsSet[0], layer=numAntPortsCw0, dmrs=dmrsOh, xoh=int(self.nrDedPdschCfgXOverheadComb.currentText()[3:]), scale=1))
            tbs.append(self.getTbs(sch='pdsch', tp=0, rnti='c-rnti', tab=self.nrDedPdschCfgMcsTableComb.currentText(), td=td, fd=fd, mcs=mcsSet[1], layer=len(dmrsPorts)-numAntPortsCw0, dmrs=dmrsOh, xoh=int(self.nrDedPdschCfgXOverheadComb.currentText()[3:]), scale=1))
        else:
            return
        
        self.nrDci11PdschTbsEdit.setText(','.join([str(i) for i in tbs if i is not None]))
        
    def onDmrsDedPuschDmrsTypeCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDmrsDedPuschDmrsTypeCombCurIndChanged, index=%d' % index)
        self.updateDci01AntPortsFieldLabel()
        
        if self.nrDci01PuschAntPortsFieldEdit.text():
            self.validatePuschAntPorts()
        
    def onDmrsDedPuschMaxLengthCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDmrsDedPuschMaxLengthCombCurIndChanged, index=%d' % index)
        if self.nrDmrsDedPuschMaxLengthComb.currentText() == 'len1':
            self.nrDmrsDedPuschAddPosComb.clear()
            self.nrDmrsDedPuschAddPosComb.addItems(['pos0', 'pos1', 'pos2', 'pos3'])
        else:
            self.nrDmrsDedPuschAddPosComb.clear()
            self.nrDmrsDedPuschAddPosComb.addItems(['pos0', 'pos1'])
            
        self.updateDci01AntPortsFieldLabel()
        
        if self.nrDci01PuschAntPortsFieldEdit.text():
            self.validatePuschAntPorts()
    
    def onDmrsDedPuschAddPosCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDmrsDedPuschAddPosCombCurIndChanged, index=%d' % index)
        #refer to 3GPP 38.211 vf30 6.4.1.1.3
        #For PUSCH mapping type A, the case dmrs-AdditionalPosition equal to 'pos3' is only supported when dmrs-TypeA-Position is equal to 'pos2'.
        if self.nrDci01PuschTimeAllocMappingTypeComb.currentText() == 'Type A' and self.nrDmrsDedPuschAddPosComb.currentText() == 'pos3' and self.nrMibDmRsTypeAPosComb.currentText() != 'pos2':
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: For PUSCH mapping type A, the case dmrs-AdditionalPosition equal to "pos3" is only supported when dmrs-TypeA-Position is equal to "pos2". Reset dmrs-additionalPosition to "pos0".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            self.nrDmrsDedPuschAddPosComb.setCurrentText('pos0')
            return
        
        if self.nrDci01PuschAntPortsFieldEdit.text():
            self.validatePuschAntPorts()
            
    def onDmrsDedPdschAddPosCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDmrsDedPdschAddPosCombCurIndChanged, index=%d' % index)
        #refer to 3GPP 38.211 vf30 7.4.1.1.2
        #The case dmrs-AdditionalPosition equals to 'pos3' is only supported when dmrs-TypeA-Position is equal to 'pos2'.
        if self.nrDmrsDedPdschAddPosComb.currentText() == 'pos3' and self.nrMibDmRsTypeAPosComb.currentText() != 'pos2':
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: For PDSCH, the case dmrs-AdditionalPosition equals to "pos3" is only supported when dmrs-TypeA-Position is equal to "pos2"! Reset dmrs-AdditionalPosition to "pos0".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            self.nrDmrsDedPdschAddPosComb.setCurrentText('pos0')
            return
        
        if self.nrDci11PdschAntPortsFieldEdit.text():
            self.validatePdschAntPorts()
        
    def onDci11PdschFreqRaTypeCombCurIndChanged(self, index):
        if index < 0:
            return
        
        if not self.nrDedDlBwpGenericLocAndBwEdit.text() or not self.nrDedDlBwpGenericLRbsEdit.text() or not self.nrDedDlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci11PdschFreqRaTypeCombCurIndChanged, index=%d' % index)
        self.updateDedDlBwpInfo()
        
    def updateDedDlBwpInfo(self):
        if not self.nrDedDlBwpGenericLocAndBwEdit.text() or not self.nrDedDlBwpGenericLRbsEdit.text() or not self.nrDedDlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside updateDedDlBwpInfo')
        bwpSize = int(self.nrDedDlBwpGenericLRbsEdit.text())
        bwpStart = int(self.nrDedDlBwpGenericRbStartEdit.text())
        
        #update nominal rbg size P
        P = self.getNomRbgSizeP(bwpSize, sch='pdsch', config=self.nrDedPdschCfgRbgConfigComb.currentText())
        if P is None:
            self.ngwin.logEdit.append('Error: The nominal RBG size P is None!')
            return
        
        self.nrDedPdschCfgRbgSizeEdit.setText(str(P))
        
        if self.nrDci11PdschFreqAllocTypeComb.currentText() == 'RA Type0':
            self.bitwidthType0Pdsch = math.ceil((bwpSize + (bwpStart % P)) / P)
            self.rbgsType0Pdsch = [0]*self.bitwidthType0Pdsch
            for i in range(self.bitwidthType0Pdsch):
                if i == 0:
                    self.rbgsType0Pdsch[i] = P - bwpStart % P
                elif self.bitwidthType0Pdsch > 1 and i == self.bitwidthType0Pdsch - 1:
                    self.rbgsType0Pdsch[i] = (bwpStart+bwpSize) % P if (bwpStart+bwpSize) % P > 0 else P
                else:
                    self.rbgsType0Pdsch[i] = P
                    
            #set 'freq domain assignment' of dci11
            self.nrDci11PdschFreqAllocFieldLabel.setText('Freq domain resource assignment[%dbits]:' % self.bitwidthType0Pdsch)
            self.nrDci11PdschFreqAllocFieldEdit.setValidator(QRegExpValidator(QRegExp('[0-1]{%d}' % self.bitwidthType0Pdsch)))
            self.nrDci11PdschFreqAllocFieldEdit.setText('1'*self.bitwidthType0Pdsch)
            self.nrDci11PdschFreqAllocFieldEdit.setEnabled(True)
            self.nrDci11PdschFreqAllocType1LRbsEdit.setEnabled(False)
            self.nrDci11PdschFreqAllocType1RbStartEdit.setEnabled(False)
            self.nrDci11PdschFreqAllocType1LRbsEdit.clear()
            self.nrDci11PdschFreqAllocType1RbStartEdit.clear()
        else:
            self.bitwidthType1Pdsch = math.ceil(math.log2(bwpSize * (bwpSize + 1) / 2))
            #set 'freq domain assignment' of dci11
            self.nrDci11PdschFreqAllocFieldLabel.setText('Freq domain resource assignment[%dbits]:' % self.bitwidthType1Pdsch)
            self.nrDci11PdschFreqAllocFieldEdit.setValidator(QRegExpValidator(QRegExp('[0-1]{%d}' % self.bitwidthType1Pdsch)))
            self.nrDci11PdschFreqAllocType1RbStartLabel.setText('RB_start(of RIV)[0-%d]:' % (bwpSize-1))
            self.nrDci11PdschFreqAllocType1RbStartEdit.setValidator(QIntValidator(0, bwpSize-1))
            self.nrDci11PdschFreqAllocType1LRbsLabel.setText('L_RBs(of RIV)[2-%d]:' % bwpSize)
            self.nrDci11PdschFreqAllocType1LRbsEdit.setValidator(QIntValidator(2, bwpSize))
            self.nrDci11PdschFreqAllocType1RbStartEdit.setText('0')
            self.nrDci11PdschFreqAllocType1LRbsEdit.setText(str(bwpSize))
            self.nrDci11PdschFreqAllocFieldEdit.setText('{:0{width}b}'.format(self.makeRiv(bwpSize, 0, bwpSize), width=self.bitwidthType1Pdsch))
            self.nrDci11PdschFreqAllocFieldEdit.setEnabled(False)
            self.nrDci11PdschFreqAllocType1LRbsEdit.setEnabled(True)
            self.nrDci11PdschFreqAllocType1RbStartEdit.setEnabled(True)
    
    def getNomRbgSizeP(self, bwpSize, sch='pdsch', config='config1'):
        #refer to 3GPP 38.214 vf30
        #Table 5.1.2.2.1-1: Nominal RBG size P
        #Table 6.1.2.2.1-1: Nominal RBG size P
        if sch == 'pdsch' or sch == 'pusch':
            if bwpSize >= 1 and bwpSize <= 36:
                return 2 if config == 'config1' else 4
            elif bwpSize >= 37 and bwpSize <= 72:
                return 4 if config == 'config1' else 8
            elif bwpSize >= 73 and bwpSize <= 144:
                return 8 if config == 'config1' else 16
            elif bwpSize >= 145 and bwpSize <= 275:
                return 16
            else:
                return None
        else:
            return None
    
    def onDci11PdschType1LRBsOrRBStartEditTextChanged(self, text):
        if not self.nrDci11PdschFreqAllocType1LRbsEdit.text() or not self.nrDci11PdschFreqAllocType1RbStartEdit.text():
            return
        
        if not self.nrDedDlBwpGenericLocAndBwEdit.text() or not self.nrDedDlBwpGenericLRbsEdit.text() or not self.nrDedDlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci11PdschType1LRBsOrRBStartEditTextChanged')
        L_RBs = int(self.nrDci11PdschFreqAllocType1LRbsEdit.text())
        RB_start = int(self.nrDci11PdschFreqAllocType1RbStartEdit.text())
        bwpSize = int(self.nrDedDlBwpGenericLRbsEdit.text())
        if L_RBs < 1 or L_RBs > (bwpSize - RB_start):
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: L_RBs = %s, RB_start = %s with BWP bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), L_RBs, RB_start, bwpSize))
            self.nrDci11PdschFreqAllocFieldEdit.clear()
            return
        
        riv = self.makeRiv(L_RBs, RB_start, bwpSize)
        if riv is not None:
            self.nrDci11PdschFreqAllocFieldEdit.setText('{:0{width}b}'.format(riv, width=self.bitwidthType1Pdsch))
            #update 'tbs' by calling getTbs when necessary
            self.validatePdschAntPorts()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %s(with L_RBs = %s, RB_start = %s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if riv is None else str(riv), L_RBs, RB_start))
            self.nrDci11PdschFreqAllocFieldEdit.clear()
            
    def onDci11PdschFreqAllocFieldEditTextChanged(self, text):
        if not self.nrDci11PdschFreqAllocFieldEdit.text() or self.nrDci11PdschFreqAllocTypeComb.currentText() == 'RA Type1':
            return
        
        self.ngwin.logEdit.append('-->inside onDci11PdschFreqAllocFieldEditTextChanged')
        if len(self.nrDci11PdschFreqAllocFieldEdit.text()) != self.bitwidthType0Pdsch or int(self.nrDci11PdschFreqAllocFieldEdit.text(), 2) == 0:
            return
        else:
            #update 'tbs' by calling getTbs when necessary
            self.validatePdschAntPorts()
            
    def updateIniUlBwpInfo(self):
        if not self.nrIniUlBwpGenericLocAndBwEdit.text() or not self.nrIniUlBwpGenericLRbsEdit.text() or not self.nrIniUlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside updateIniUlBwpInfo')
        bwpSize = int(self.nrIniUlBwpGenericLRbsEdit.text())
        bwpStart = int(self.nrIniUlBwpGenericRbStartEdit.text())
        
        if self.nrRachMsg3TpComb.currentText() == 'enabled':
            self.updateLRBsMsg3PuschTp()
        
        self.bitwidthType1IniUlBwp = math.ceil(math.log2(bwpSize * (bwpSize + 1) / 2))
        self.bitwidthType1Msg3Pusch = max(14, self.bitwidthType1IniUlBwp)
        
        #set 'freq domain assignment' of msg3 pusch 
        self.nrMsg3PuschFreqAllocFieldLabel.setText('Freq domain resource assignment[%dLSBs]:' % self.bitwidthType1IniUlBwp)
        self.nrMsg3PuschFreqAllocFieldEdit.setValidator(QRegExpValidator(QRegExp('[0-1]{%d}' % self.bitwidthType1Msg3Pusch)))
        self.nrMsg3PuschFreqAllocType1RbStartLabel.setText('RB_start(of RIV)[0-%d]:' % (bwpSize-1))
        self.nrMsg3PuschFreqAllocType1RbStartEdit.setValidator(QIntValidator(0, bwpSize-1))
        self.nrMsg3PuschFreqAllocType1LRbsLabel.setText('L_RBs(of RIV)[2-%d]:' % bwpSize)
        self.nrMsg3PuschFreqAllocType1LRbsEdit.setValidator(QIntValidator(2, bwpSize))
        
        self.nrMsg3PuschFreqAllocType1RbStartEdit.setText('0')
        if self.nrRachMsg3TpComb.currentText() == 'enabled':
            if self.bitwidthType1IniUlBwp <= 14:
                self.nrMsg3PuschFreqAllocType1LRbsEdit.setText(str(self.lrbsMsg3PuschTp[-1]))
                self.nrMsg3PuschFreqAllocFieldEdit.setText('{:0{width}b}'.format(self.makeRiv(self.lrbsMsg3PuschTp[-1], 0, bwpSize), width=self.bitwidthType1Msg3Pusch))
            else:
                for i in range(1, len(self.lrbsMsg3PuschTp)+1):
                    lrbs = self.lrbsMsg3PuschTp[-i]
                    bits = '{:0{width}b}'.format(self.makeRiv(lrbs, 0, bwpSize), width=self.bitwidthType1Msg3Pusch)
                    if self.nrMsg3PuschFreqAllocFreqHopComb.currentText() == 'enabled':
                        subBits = bits[2:2+self.bitwidthType1IniUlBwp-14]
                    else:
                        subBits = bits[0:self.bitwidthType1IniUlBwp-14]
                    if int(subBits, 2) == 0:
                        self.nrMsg3PuschFreqAllocType1LRbsEdit.setText(str(lrbs))
                        self.nrMsg3PuschFreqAllocFieldEdit.setText(bits)
                        break
        else:
            if self.bitwidthType1IniUlBwp <= 14:
                self.nrMsg3PuschFreqAllocType1LRbsEdit.setText(str(bwpSize))
                self.nrMsg3PuschFreqAllocFieldEdit.setText('{:0{width}b}'.format(self.makeRiv(bwpSize, 0, bwpSize), width=self.bitwidthType1Msg3Pusch))
            else:
                for lrbs in range(bwpSize, 0, -1):
                    bits = '{:0{width}b}'.format(self.makeRiv(lrbs, 0, bwpSize), width=self.bitwidthType1Msg3Pusch)
                    if self.nrMsg3PuschFreqAllocFreqHopComb.currentText() == 'enabled':
                        subBits = bits[2:2+self.bitwidthType1IniUlBwp-14]
                    else:
                        subBits = bits[0:self.bitwidthType1IniUlBwp-14]
                    if int(subBits, 2) == 0:
                        self.nrMsg3PuschFreqAllocType1LRbsEdit.setText(str(lrbs))
                        self.nrMsg3PuschFreqAllocFieldEdit.setText(bits)
                        break
                    
        if self.bitwidthType1IniUlBwp >= 14 or self.nrMsg3PuschFreqAllocFreqHopComb.currentText() == 'disabled':
            self.nrMsg3PuschFreqAllocFieldEdit.setEnabled(False)
        else:
            self.nrMsg3PuschFreqAllocFieldEdit.setEnabled(True)
        self.nrMsg3PuschFreqAllocType1LRbsEdit.setEnabled(True)
        self.nrMsg3PuschFreqAllocType1RbStartEdit.setEnabled(True)
        
        if self.nrMsg3PuschFreqAllocFreqHopComb.currentText() == 'enabled':
            self.updateMsg3Pusch2ndHopFreqOff()
    
    def onMsg3PuschLRBsOrRBStartEditTextChanged(self, text):
        if not self.nrMsg3PuschFreqAllocType1LRbsEdit.text() or not self.nrMsg3PuschFreqAllocType1RbStartEdit.text():
            return
        
        if not self.nrIniUlBwpGenericLocAndBwEdit.text() or not self.nrIniUlBwpGenericLRbsEdit.text() or not self.nrIniUlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onMsg3PuschLRBsOrRBStartEditTextChanged')
        L_RBs = int(self.nrMsg3PuschFreqAllocType1LRbsEdit.text())
        RB_start = int(self.nrMsg3PuschFreqAllocType1RbStartEdit.text())
        bwpSize = int(self.nrIniUlBwpGenericLRbsEdit.text())
        
        if L_RBs < 1 or L_RBs > (bwpSize - RB_start):
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: L_RBs = %s, RB_start = %s with BWP bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), L_RBs, RB_start, bwpSize))
            self.nrMsg3PuschFreqAllocFieldEdit.clear()
            return
        
        if self.nrRachMsg3TpComb.currentText() == 'enabled' and not L_RBs in self.lrbsMsg3PuschTp:
            valLessThan, valLargeThan = self.findNearest(self.lrbsMsg3PuschTp, L_RBs)
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: L_RBs must be 2^x*3^y*5^z, where x/y/z>=0. Nearest values are:[%s, %s].' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if valLessThan is None else valLessThan, 'None' if valLargeThan is None else valLargeThan))
            self.nrMsg3PuschFreqAllocFieldEdit.clear()
            return
        
        riv = self.makeRiv(L_RBs, RB_start, bwpSize)
        if riv is not None:
            bits = '{:0{width}b}'.format(riv, width=self.bitwidthType1Msg3Pusch)
            self.nrMsg3PuschFreqAllocFieldEdit.setText(bits)
            
            #validate 'bits' if bitwidthType1IniUlBwp > 14bits
            if self.bitwidthType1IniUlBwp > 14:
                if self.nrMsg3PuschFreqAllocFreqHopComb.currentText() == 'enabled':
                    subBits = bits[2:2+self.bitwidthType1IniUlBwp-14]
                else:
                    subBits = bits[0:self.bitwidthType1IniUlBwp-14]
                    
                if int(subBits, 2) != 0:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Inserted bits(="%s") must be all zeros! Please refer to 3GPP 38.213 vf30 Section 8.2 for details.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), subBits))
                    return
            
            #update tbs
            self.updateMsg3PuschTbs()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %s(with L_RBs = %s, RB_start = %s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if riv is None else str(riv), L_RBs, RB_start))
            self.nrMsg3PuschFreqAllocFieldEdit.clear()

    def onMsg3PuschFreqAllocFieldEditTextChanged(self, text):
        if not self.nrMsg3PuschFreqAllocFieldEdit.text():
            return
        
        if not self.nrIniUlBwpGenericLocAndBwEdit.text() or not self.nrIniUlBwpGenericLRbsEdit.text() or not self.nrIniUlBwpGenericRbStartEdit.text():
            return
        
        if self.bitwidthType1IniUlBwp >= 14:
            #self.ngwin.logEdit.append('Error: The "Freq domain resource assignment" field shall be disabled when self.bitwidthType1IniUlBwp >= 14!')
            return
        
        if len(self.nrMsg3PuschFreqAllocFieldEdit.text()) != self.bitwidthType1Msg3Pusch:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: The "Freq domain resource assignment" field is %d bits, which should be %d bits!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), len(self.nrMsg3PuschFreqAllocFieldEdit.text()), self.bitwidthType1Msg3Pusch))
            return
        
        self.ngwin.logEdit.append('-->inside onMsg3PuschFreqAllocFieldEditTextChanged')
        riv = int(self.nrMsg3PuschFreqAllocFieldEdit.text()[14-self.bitwidthType1IniUlBwp:], 2)
        L_RBs = int(self.nrMsg3PuschFreqAllocType1LRbsEdit.text())
        RB_start = int(self.nrMsg3PuschFreqAllocType1RbStartEdit.text())
        bwpSize = int(self.nrIniUlBwpGenericLRbsEdit.text())
        
        riv2 = self.makeRiv(L_RBs, RB_start, bwpSize)
        if riv != riv2:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Only the [%d] MSBs can be changed! Please refer to 3GPP 38.213 vf30 Section 8.2 for details. Reset to default value.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), min(2, 14-self.bitwidthType1IniUlBwp)))
            self.nrMsg3PuschFreqAllocFieldEdit.setText('{:0{width}b}'.format(riv2, width=self.bitwidthType1Msg3Pusch))
            return
        
        if self.nrMsg3PuschFreqAllocFreqHopComb.currentText() == 'enabled' and bwpSize >= 50 and self.nrMsg3PuschFreqAllocFieldEdit.text()[:2] == '11':
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: UL frequency hop bits "11" is reserved when N_BWP_size >= 50! Please refer to 3GPP 38.213 vf30 Section 8.2 for details. Reset to default value.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            self.nrMsg3PuschFreqAllocFieldEdit.setText('{:0{width}b}'.format(riv2, width=self.bitwidthType1Msg3Pusch))
            return
        
        if self.nrMsg3PuschFreqAllocFreqHopComb.currentText() == 'enabled':
            self.updateMsg3Pusch2ndHopFreqOff()
            
    def findNearest(self, arr, val):
        valLargeThan = None
        valLessThan = None
        
        for i in range(len(arr)):
            if arr[i] > val:
                valLargeThan = arr[i]
                break
            
        for i in range(1, len(arr)+1):
            if arr[-i] < val:
                valLessThan = arr[-i]
                break
        
        return (valLessThan, valLargeThan)
    
    def onMsg3PuschFreqHopCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onMsg3PuschFreqHopCombCurIndChanged, index=%d' % index)
        if self.bitwidthType1IniUlBwp < 14 and self.nrMsg3PuschFreqAllocFreqHopComb.currentText() == 'enabled':
            self.nrMsg3PuschFreqAllocFieldEdit.setEnabled(True)
        else:
            self.nrMsg3PuschFreqAllocFieldEdit.setEnabled(False)
        
        self.updateMsg3Pusch2ndHopFreqOff()
        
        #set 'dmrs-additionalPosition' of dmrs for msg3
        if self.nrMsg3PuschFreqAllocFreqHopComb.currentText() == 'disabled':
            self.nrDmrsMsg3AddPosComb.setCurrentText('pos2')
        else:
            self.nrDmrsMsg3AddPosComb.setCurrentText('pos1')
        
        #update tbs
        self.updateMsg3PuschTbs()
            
    def updateMsg3Pusch2ndHopFreqOff(self):
        if not self.nrMsg3PuschFreqAllocFieldEdit.text():
            self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit.clear()
            return
        if not self.nrIniUlBwpGenericLocAndBwEdit.text() or not self.nrIniUlBwpGenericLRbsEdit.text() or not self.nrIniUlBwpGenericRbStartEdit.text():
            self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit.clear()
            return
        
        self.ngwin.logEdit.append('-->inside updateMsg3Pusch2ndHopFreqOff')
        bwpSize = int(self.nrIniUlBwpGenericLRbsEdit.text())
        if self.nrMsg3PuschFreqAllocFreqHopComb.currentText() == 'enabled':
            nUlHop = 1 if bwpSize < 50 else 2
            freqHopBits = self.nrMsg3PuschFreqAllocFieldEdit.text()[:nUlHop]
            if nUlHop == 1 and freqHopBits == '0':
                self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit.setText(str(math.floor(bwpSize / 2)))
            elif nUlHop == 1 and freqHopBits == '1':
                self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit.setText(str(math.floor(bwpSize / 4)))
            elif nUlHop == 2 and freqHopBits == '00':
                self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit.setText(str(math.floor(bwpSize / 2)))
            elif nUlHop == 2 and freqHopBits == '01':
                self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit.setText(str(math.floor(bwpSize / 4)))
            elif nUlHop == 2 and freqHopBits == '10':
                self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit.setText(str(-1 * math.floor(bwpSize / 4)))
            else:#nUlHop == 2 and freqHopBits == '11'
                #'11' is reversed!
                self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit.clear()
        else:
            self.nrMsg3PuschFreqAllocType1SecondHopFreqOffEdit.clear()
                
                
    def onRachMsg3TpCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onRachMsg3TpCombCurIndChanged, index=%d' % index)
        if self.nrRachMsg3TpComb.currentText() == 'enabled':
            #self.updateLRBsMsg3PuschTp()
            self.updateIniUlBwpInfo()
            
        #update tbs
        self.updateMsg3PuschTbs()
        
    def updateLRBsMsg3PuschTp(self):
        if not self.nrIniUlBwpGenericLocAndBwEdit.text() or not self.nrIniUlBwpGenericLRbsEdit.text() or not self.nrIniUlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside updateLRBsMsg3PuschTp')
        bwpSize = int(self.nrIniUlBwpGenericLRbsEdit.text())
        
        self.lrbsMsg3PuschTp = []
        for x in range(math.ceil(math.log(bwpSize, 2))):
            for y in range(math.ceil(math.log(bwpSize, 3))):
                for z in range(math.ceil(math.log(bwpSize, 5))):
                    lrbs = 2 ** x * 3 ** y * 5 ** z
                    if lrbs <= bwpSize:
                        self.lrbsMsg3PuschTp.append(lrbs)
                    else:
                        break
        #sort in ascending order
        self.lrbsMsg3PuschTp.sort()
        '''
        for i in self.lrbsMsg3PuschTp:
            self.ngwin.logEdit.append('%d' % i)
        '''
        
    def updateLRBsDedPuschTp(self):
        if not self.nrDedUlBwpGenericLocAndBwEdit.text() or not self.nrDedUlBwpGenericLRbsEdit.text() or not self.nrDedUlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside updateLRBsDedPuschTp')
        bwpSize = int(self.nrDedUlBwpGenericLRbsEdit.text())
        
        self.lrbsDedPuschTp = []
        for x in range(math.ceil(math.log(bwpSize, 2))):
            for y in range(math.ceil(math.log(bwpSize, 3))):
                for z in range(math.ceil(math.log(bwpSize, 5))):
                    lrbs = 2 ** x * 3 ** y * 5 ** z
                    if lrbs <= bwpSize:
                        self.lrbsDedPuschTp.append(lrbs)
                    else:
                        break
        #sort in ascending order
        self.lrbsDedPuschTp.sort()
        '''
        for i in self.lrbsDedPuschTp:
            self.ngwin.logEdit.append('%d' % i)
        '''
        
    def onDci01PuschFreqRaTypeCombCurIndChanged(self, index):
        if index < 0:
            return
        
        if not self.nrDedUlBwpGenericLocAndBwEdit.text() or not self.nrDedUlBwpGenericLRbsEdit.text() or not self.nrDedUlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschFreqRaTypeCombCurIndChanged, index=%d' % index)
        if self.nrDci01PuschFreqAllocTypeComb.currentText() == 'RA Type0' and self.nrDedPuschCfgTpComb.currentText() == 'enabled':
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Transform precoding of PUSCH can only be enabled for resource allocation Type 1!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            return
        
        self.updateDedUlBwpInfo()
        
    def updateDedUlBwpInfo(self):
        if not self.nrDedUlBwpGenericLocAndBwEdit.text() or not self.nrDedUlBwpGenericLRbsEdit.text() or not self.nrDedUlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside updateDedUlBwpInfo')
        bwpSize = int(self.nrDedUlBwpGenericLRbsEdit.text())
        bwpStart = int(self.nrDedUlBwpGenericRbStartEdit.text())
        
        #update nominal rbg size P
        P = self.getNomRbgSizeP(bwpSize, sch='pusch', config=self.nrDedPuschCfgRbgConfigComb.currentText())
        if P is None:
            self.ngwin.logEdit.append('Error: The nominal RBG size P is None!')
            return
        
        self.nrDedPuschCfgRbgSizeEdit.setText(str(P))
        
        if self.nrDci01PuschFreqAllocTypeComb.currentText() == 'RA Type0':
            self.bitwidthType0Pusch = math.ceil((bwpSize + (bwpStart % P)) / P)
            self.rbgsType0Pusch = [0]*self.bitwidthType0Pusch
            for i in range(self.bitwidthType0Pusch):
                if i == 0:
                    self.rbgsType0Pusch[i] = P - bwpStart % P
                elif self.bitwidthType0Pusch > 1 and i == self.bitwidthType0Pusch - 1:
                    self.rbgsType0Pusch[i] = (bwpStart+bwpSize) % P if (bwpStart+bwpSize) % P > 0 else P
                else:
                    self.rbgsType0Pusch[i] = P
                    
            #set 'freq domain assignment' of dci01
            self.nrDci01PuschFreqAllocFieldLabel.setText('Freq domain resource assignment[%dbits]:' % self.bitwidthType0Pusch)
            self.nrDci01PuschFreqAllocFieldEdit.setValidator(QRegExpValidator(QRegExp('[0-1]{%d}' % self.bitwidthType0Pusch)))
            self.nrDci01PuschFreqAllocFieldEdit.setText('1'*self.bitwidthType0Pusch)
            self.nrDci01PuschFreqAllocFieldEdit.setEnabled(True)
            self.nrDci01PuschFreqAllocType1LRbsEdit.setEnabled(False)
            self.nrDci01PuschFreqAllocType1RbStartEdit.setEnabled(False)
            self.nrDci01PuschFreqAllocType1LRbsEdit.clear()
            self.nrDci01PuschFreqAllocType1RbStartEdit.clear()
        else:
            if self.nrDedPuschCfgTpComb.currentText() == 'enabled':
                self.updateLRBsDedPuschTp()
        
            self.bitwidthType1DedUlBwp = math.ceil(math.log2(bwpSize * (bwpSize + 1) / 2))
            
            #set 'freq domain assignment' of dci01 
            self.nrDci01PuschFreqAllocFieldLabel.setText('Freq domain resource assignment[%dLSBs]:' % self.bitwidthType1DedUlBwp)
            self.nrDci01PuschFreqAllocFieldEdit.setValidator(QRegExpValidator(QRegExp('[0-1]{%d}' % self.bitwidthType1DedUlBwp)))
            self.nrDci01PuschFreqAllocType1RbStartLabel.setText('RB_start(of RIV)[0-%d]:' % (bwpSize-1))
            self.nrDci01PuschFreqAllocType1RbStartEdit.setValidator(QIntValidator(0, bwpSize-1))
            self.nrDci01PuschFreqAllocType1LRbsLabel.setText('L_RBs(of RIV)[2-%d]:' % bwpSize)
            self.nrDci01PuschFreqAllocType1LRbsEdit.setValidator(QIntValidator(2, bwpSize))
            
            self.nrDci01PuschFreqAllocType1RbStartEdit.setText('0')
            #refer to 3GPP 38.314 vf30 section 6.3
            nUlHop = 1 if bwpSize < 50 else 2
            if self.nrDedPuschCfgTpComb.currentText() == 'enabled':
                for i in range(1, len(self.lrbsDedPuschTp)+1):
                    lrbs = self.lrbsDedPuschTp[-i]
                    bits = '{:0{width}b}'.format(self.makeRiv(lrbs, 0, bwpSize), width=self.bitwidthType1DedUlBwp)
                    if self.nrDci01PuschFreqAllocFreqHopComb.currentText() != 'disabled':
                        subBits = bits[:nUlHop]
                        if int(subBits, 2) == 0:
                            self.nrDci01PuschFreqAllocType1LRbsEdit.setText(str(lrbs))
                            self.nrDci01PuschFreqAllocFieldEdit.setText(bits)
                            break
                    else:
                        self.nrDci01PuschFreqAllocType1LRbsEdit.setText(str(lrbs))
                        self.nrDci01PuschFreqAllocFieldEdit.setText(bits)
                        break
            else:
                for lrbs in range(bwpSize, 0, -1):
                    bits = '{:0{width}b}'.format(self.makeRiv(lrbs, 0, bwpSize), width=self.bitwidthType1DedUlBwp)
                    if self.nrDci01PuschFreqAllocFreqHopComb.currentText() != 'disabled':
                        subBits = bits[:nUlHop]
                        if int(subBits, 2) == 0:
                            self.nrDci01PuschFreqAllocType1LRbsEdit.setText(str(lrbs))
                            self.nrDci01PuschFreqAllocFieldEdit.setText(bits)
                            break
                    else:
                        self.nrDci01PuschFreqAllocType1LRbsEdit.setText(str(lrbs))
                        self.nrDci01PuschFreqAllocFieldEdit.setText(bits)
                        break
                        
            if self.nrDci01PuschFreqAllocFreqHopComb.currentText() == 'disabled':
                self.nrDci01PuschFreqAllocFieldEdit.setEnabled(False)
            else:
                #for simplicity, N_UL_hop bit(s) are fixed to '0' or '00', that's, 'frequencyHoppingOffset(List)' in PUSCH-Config is explicitly configured in 'dedicated ul bwp'
                self.nrMsg3PuschFreqAllocFieldEdit.setEnabled(False)
            self.nrDci01PuschFreqAllocType1LRbsEdit.setEnabled(True)
            self.nrDci01PuschFreqAllocType1RbStartEdit.setEnabled(True)

    def onDci01PuschType1LRBsOrRBStartEditTextChanged(self, text):
        if not self.nrDci01PuschFreqAllocType1LRbsEdit.text() or not self.nrDci01PuschFreqAllocType1RbStartEdit.text():
            return
        
        if not self.nrDedUlBwpGenericLocAndBwEdit.text() or not self.nrDedUlBwpGenericLRbsEdit.text() or not self.nrDedUlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschType1LRBsOrRBStartEditTextChanged')
        L_RBs = int(self.nrDci01PuschFreqAllocType1LRbsEdit.text())
        RB_start = int(self.nrDci01PuschFreqAllocType1RbStartEdit.text())
        bwpSize = int(self.nrDedUlBwpGenericLRbsEdit.text())
        if L_RBs < 1 or L_RBs > (bwpSize - RB_start):
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid setting: L_RBs = %s, RB_start = %s with BWP bandwidth = %s!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), L_RBs, RB_start, bwpSize))
            self.nrDci01PuschFreqAllocFieldEdit.clear()
            return
        
        if self.nrDedPuschCfgTpComb.currentText() == 'enabled' and not L_RBs in self.lrbsDedPuschTp:
            valLessThan, valLargeThan = self.findNearest(self.lrbsDedPuschTp, L_RBs)
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: L_RBs must be 2^x*3^y*5^z, where x/y/z>=0. Nearest values are:[%s, %s].' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if valLessThan is None else valLessThan, 'None' if valLargeThan is None else valLargeThan))
            self.nrDci01PuschFreqAllocFieldEdit.clear()
            return
        
        riv = self.makeRiv(L_RBs, RB_start, bwpSize)
        if riv is not None:
            bits = '{:0{width}b}'.format(riv, width=self.bitwidthType1Pdsch)
            if self.nrDci01PuschFreqAllocFreqHopComb.currentText() != 'disabled':
                nUlHop = 1 if bwpSize < 50 else 2
                if int(bits[:nUlHop], 2) == 0:
                    self.nrDci01PuschFreqAllocFieldEdit.setText(bits)
                    #update 'tbs' by calling getTbs when necessary
                    self.validatePuschAntPorts()
                else:
                    self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: The %d MSB of "Freq domain resouce assignment" field(="%s") must be all zero when frequency hopping is enabled!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), nUlHop, bits))
                    self.nrDci01PuschFreqAllocFieldEdit.clear()
            else:
                self.nrDci01PuschFreqAllocFieldEdit.setText(bits)
                #update 'tbs' by calling getTbs when necessary
                self.validatePuschAntPorts()
        else:
            self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: Invalid RIV = %s(with L_RBs = %s, RB_start = %s)!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), 'None' if riv is None else str(riv), L_RBs, RB_start))
            self.nrDci01PuschFreqAllocFieldEdit.clear()
    
    def onDci01PuschFreqAllocFieldEditTextChanged(self, text):
        if not self.nrDci01PuschFreqAllocFieldEdit.text() or self.nrDci01PuschFreqAllocTypeComb.currentText() == 'RA Type1':
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschFreqAllocFieldEditTextChanged')
        if len(self.nrDci01PuschFreqAllocFieldEdit.text()) != self.bitwidthType0Pusch or int(self.nrDci01PuschFreqAllocFieldEdit.text(), 2) == 0:
            return
        else:
            #update 'tbs' by calling getTbs when necessary
            self.validatePuschAntPorts()
            
    def onDci01PuschFreqHopCombCurIndChanged(self, index):
        if index < 0:
            return
        
        if not self.nrDedUlBwpGenericLocAndBwEdit.text() or not self.nrDedUlBwpGenericLRbsEdit.text() or not self.nrDedUlBwpGenericRbStartEdit.text():
            return
        
        if not self.nrDci01PuschFreqAllocFieldEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschFreqHopCombCurIndChanged, index=%d' % index)
        if self.nrDci01PuschFreqAllocFreqHopComb.currentText() != 'disabled':
            bwpSize = int(self.nrDedUlBwpGenericLRbsEdit.text())
            nUlHop = 1 if bwpSize < 50 else 2
            if int(self.nrDci01PuschFreqAllocFieldEdit.text()[:nUlHop], 2) != 0:
                #FIXME It's better not put constraints of 'The N_UL_HOP MSBs must be all zeros', which limits the RB_start + L_RBs combinations
                self.ngwin.logEdit.append('<font color=purple><b>[%s]Warning</font>: The %d MSB of "Freq domain resource assignment" field(="%s") must be all zero when frequency hopping is enabled!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), nUlHop, self.nrDci01PuschFreqAllocFieldEdit.text()))
                return
        
        if self.nrDci01PuschAntPortsFieldEdit.text():
            self.validatePuschAntPorts()
                
    def onDci01PuschCw0McsEditTextChanged(self, text):
        if not self.nrDci01PuschCw0McsEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschCw0McsEditTextChanged')
        self.validatePuschCw0Mcs()
    
    def validatePuschCw0Mcs(self):
        self.ngwin.logEdit.append('-->inside validatePuschCw0Mcs')
        if not self.nrDci01PuschCw0McsEdit.text():
            self.nrDci01PuschAntPortsFieldEdit.clear()
            return
        
        mcsCw0 = int(self.nrDci01PuschCw0McsEdit.text())
        mcsTable = self.nrDedPuschCfgMcsTableComb.currentText()
        if mcsTable == 'qam256':
            if mcsCw0 > 27:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: MCS(CW0) should be 0-27 when "mcs-Table" of PUSCH-Config is "%s"!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), mcsTable))
                return
        else: 
            if mcsCw0 > 28:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: MCS(CW0) should be 0-28 when "mcs-Table" of PUSCH-Config is "%s"!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), mcsTable))
                return
        
        if self.nrDci01PuschAntPortsFieldEdit.text():
            self.validatePuschAntPorts()
            
    def onDci01PuschPrecodingLayersEditTextChanged(self, text):
        if not self.nrDci01PuschPrecodingLayersFieldEdit.text():
            return
        if self.nrDedPuschCfgTxCfgComb.currentText() != 'codebook':
            return
        if not self.nrDedPuschCfgCbMaxRankEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschPrecodingLayersEditTextChanged')
        numUeAp = int(self.nrUeAntPortsComb.currentText()[:-2])
        tp = self.nrDedPuschCfgTpComb.currentText()
        maxRank = int(self.nrDedPuschCfgCbMaxRankEdit.text())
        cbSubset = self.nrDedPuschCfgCbSubsetComb.currentText()
        precoding = int(self.nrDci01PuschPrecodingLayersFieldEdit.text())
        key = '%s_%s' % ({'fullyAndPartialAndNonCoherent':0, 'partialAndNonCoherent':1, 'nonCoherent':2}[cbSubset], precoding) 
        if numUeAp == 4 and tp == 'disabled' and maxRank in (2,3,4):
            if not key in self.nrDci01TpmiAp4Tp0MaxRank234 or self.nrDci01TpmiAp4Tp0MaxRank234[key] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDci01TpmiAp4Tp0MaxRank234.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return
            else:
                val = self.nrDci01TpmiAp4Tp0MaxRank234[key]
        elif numUeAp == 4 and (tp == 'enabled' or (tp == 'disabled' and maxRank == 1)):
            if not key in self.nrDci01TpmiAp4Tp1OrTp0MaxRank1 or self.nrDci01TpmiAp4Tp1OrTp0MaxRank1[key] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDci01TpmiAp4Tp1OrTp0MaxRank1.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return
            else:
                val = self.nrDci01TpmiAp4Tp1OrTp0MaxRank1[key]
        elif numUeAp == 2 and tp == 'disabled' and maxRank == 2:
            if not key in self.nrDci01TpmiAp2Tp0MaxRank2 or self.nrDci01TpmiAp2Tp0MaxRank2[key] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDci01TpmiAp2Tp0MaxRank2.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return
            else:
                val = self.nrDci01TpmiAp2Tp0MaxRank2[key]
        elif numUeAp == 2 and (tp == 'enabled' or (tp == 'disabled' and maxRank == 1)):
            if not key in self.nrDci01TpmiAp2Tp1OrTp0MaxRank1 or self.nrDci01TpmiAp2Tp1OrTp0MaxRank1[key] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDci01TpmiAp2Tp1OrTp0MaxRank1.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return
            else:
                val = self.nrDci01TpmiAp2Tp1OrTp0MaxRank1[key]
        else:
            pass
        
        rank, tpmi = val
        self.ngwin.logEdit.append('TRI/TPMI(DCI 0_1) info: rank=%s, tpmi=%s (key="%s",val=%s)' % (rank, tpmi, key, val)) 
        
        if self.nrDci01PuschAntPortsFieldEdit.text():
            self.validatePuschAntPorts()
    
    def onDci01PuschSriEditTextChanged(self, text):
        if not self.nrDci01PuschSriFieldEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschSriEditTextChanged')
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'nonCodebook':
            if not self.nrDedPuschCfgNonCbMaxLayersEdit.text() or not self.nrSrsResSet1ResourceIdListEdit.text():
                return
            
            Lmax = int(self.nrDedPuschCfgNonCbMaxLayersEdit.text())
            
            try:
                srsSet1 = [int(i) for i in self.nrSrsResSet1ResourceIdListEdit.text().split(',') if len(i) > 0]
            except Exception as e:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Exception raised when parsing srs-resourceSet1: %s.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), e))
                return
            
            Nsrs = len(srsSet1)
            if Nsrs > 1:
                sri = int(self.nrDci01PuschSriFieldEdit.text())
                key = '%d_%d_%d' % (Lmax, Nsrs, sri)
                if not key in self.nrDci01NonCbSri or self.nrDci01NonCbSri[key] is None:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDci01NonCbSri.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    return
                else:
                    val = self.nrDci01NonCbSri[key]
            
            self.ngwin.logEdit.append('SRI(DCI 0_1) info: rank=%s (key="%s",val=%s)' % (len(val) if Nsrs > 1 else 1, key, val))
            
            if self.nrDci01PuschAntPortsFieldEdit.text():
                self.validatePuschAntPorts()
    
    def onDci01PuschAntPortsEditTextChanged(self, text):
        if not self.nrDci01PuschAntPortsFieldEdit.text():
            self.nrDmrsDedPuschCdmGroupsWoDataEdit.clear()
            self.nrDmrsDedPuschDmrsPortsEdit.clear()
            self.nrDmrsDedPuschFrontLoadSymbsEdit.clear()
            self.nrPtrsPuschDmrsAntPortsEdit.clear()
            self.nrPtrsPuschTpDmrsAntPortsEdit.clear()
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschAntPortsEditTextChanged')
        self.validatePuschAntPorts()
    
    def onDci01PuschPtrsDmrsMappingEditTextChanged(self, text):
        if not self.nrDci01PuschPtrsDmrsMappingEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDci01PuschPtrsDmrsMappingEditTextChanged')
        self.updatePtrsPusch()
        
    def onDedPuschCfgRbgConfigCombCurIndChanged(self, index):
        if index < 0:
            return
        
        if not self.nrDedUlBwpGenericLocAndBwEdit.text() or not self.nrDedUlBwpGenericLRbsEdit.text() or not self.nrDedUlBwpGenericRbStartEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDedPuschCfgRbgConfigCombCurIndChanged, index=%d' % index)
        bwpSize = int(self.nrDedUlBwpGenericLRbsEdit.text())
        P = self.getNomRbgSizeP(bwpSize, sch='pusch', config=self.nrDedPuschCfgRbgConfigComb.currentText())
        if P is None:
            self.ngwin.logEdit.append('Error: The nominal RBG size P is None!')
            return
        
        self.nrDedPuschCfgRbgSizeEdit.setText(str(P))
        if self.nrDci01PuschFreqAllocTypeComb.currentText() == 'RA Type0':
            self.updateDedUlBwpInfo()
    
    def onDedPuschCfgTpCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDedPuschCfgTpCombCurIndChanged, index=%d' % index)
        if self.nrDedPuschCfgTpComb.currentText() == 'enabled':
            if self.nrDci01PuschFreqAllocTypeComb.currentText() == 'RA Type0':
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Transform precoding of PUSCH can only be enabled for resource allocation Type 1!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                return
            
            #self.updateLRBsDedPuschTp()
            self.updateDedUlBwpInfo()
            
            #only DMRS configuration type 1 is supported when tp is enabled
            self.nrDmrsDedPuschDmrsTypeComb.setCurrentText('Type 1')
            self.nrDmrsDedPuschDmrsTypeComb.setEnabled(False)
        else:
            self.nrDmrsDedPuschDmrsTypeComb.setEnabled(True)
        
        #update 'CB maxRank' and 'non-CB maxLayers'
        self.updateDedPuschCfgLabel()
        
        #update 'precoding info and num of layers' label
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
            self.updateDci01PrecodingLayersFieldLabel()
        
        #update 'antenna port(s)' label
        self.updateDci01AntPortsFieldLabel()
        
        if self.nrDci01PuschAntPortsFieldEdit.text():
            self.validatePuschAntPorts()
            
    def onDedPuschCfgTxCfgCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDedPuschCfgTxCfgCombCurIndChanged, index=%d' % index)
        numUeAp = int(self.nrUeAntPortsComb.currentText()[:-2])
        if numUeAp == 1:
            pass
        else:
            if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
                self.nrDedPuschCfgCbSubsetComb.setEnabled(True)
                if numUeAp == 2:
                    self.nrDedPuschCfgCbSubsetComb.clear()
                    self.nrDedPuschCfgCbSubsetComb.addItems(['fullyAndPartialAndNonCoherent', 'nonCoherent'])
                else:
                    self.nrDedPuschCfgCbSubsetComb.clear()
                    self.nrDedPuschCfgCbSubsetComb.addItems(['fullyAndPartialAndNonCoherent', 'partialAndNonCoherent', 'nonCoherent'])
                self.nrDci01PuschPrecodingLayersFieldEdit.setEnabled(True)
            else:
                self.nrDedPuschCfgCbSubsetComb.setEnabled(False)
                self.nrDci01PuschPrecodingLayersFieldEdit.setEnabled(False)
        
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
            self.nrDedPuschCfgCbMaxRankEdit.setEnabled(True)
            self.nrDedPuschCfgNonCbMaxLayersEdit.setEnabled(False)
        else:
            self.nrDedPuschCfgCbMaxRankEdit.setEnabled(False)
            self.nrDedPuschCfgNonCbMaxLayersEdit.setEnabled(True)
            
        #update 'precoding info and num of layers' label
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
            self.updateDci01PrecodingLayersFieldLabel()
            
        #update 'srs resource indicator' label
        self.updateDci01SriFieldLabel()
        
        if self.nrDci01PuschAntPortsFieldEdit.text():
            self.validatePuschAntPorts()
        
    def onDedPuschCfgCbMaxRankTextChanged(self):
        if not self.nrDedPuschCfgCbMaxRankEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDedPuschCfgCbMaxRankTextChanged')
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
            self.updateDci01PrecodingLayersFieldLabel()
            if self.nrDci01PuschAntPortsFieldEdit.text():
                self.validatePuschAntPorts()
            
    def onDedPuschCfgCbSubsetCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDedPdschCfgCbSubsetCombCurIndChanged, index=%d' % index)
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
            self.updateDci01PrecodingLayersFieldLabel()
            if self.nrDci01PuschAntPortsFieldEdit.text():
                self.validatePuschAntPorts()
            
    def onDedPuschCfgNonCbMaxLayersTextChanged(self):
        if not self.nrDedPuschCfgNonCbMaxLayersEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onDedPuschCfgNonCbMaxLayersTextChanged')
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'nonCodebook':
            self.updateDci01SriFieldLabel()
            if self.nrDci01PuschAntPortsFieldEdit.text():
                self.validatePuschAntPorts()
            
    def onSrsResSet1ResourceIdListTextChanged(self):
        if not self.nrSrsRes1ResourceIdEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onSrsResSet1ResourceIdListTextChanged')
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'nonCodebook':
            self.updateDci01SriFieldLabel()
            if self.nrDci01PuschAntPortsFieldEdit.text():
                self.validatePuschAntPorts()
            
    def onSrsResSet0ResourceIdListTextChanged(self):
        if not self.nrSrsRes0ResourceIdEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside onSrsResSet0ResourceIdListTextChanged')
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
            self.updateDci01SriFieldLabel()
    
    def onDedPuschCfgMcsTableCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDedPuschCfgMcsTableCombCurIndChanged, index=%d' % index)
        #update 'tbs' by calling getTbs when necessary
        self.validatePuschCw0Mcs()
        
    def onDedPuschCfgXOverheadCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDedPuschCfgXOverheadCombCurIndChanged, index=%d' % index)
        #update 'tbs' by calling getTbs when necessary
        self.validatePuschAntPorts()
        
    def onDedPdschCfgMcsTableCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDedPdschCfgMcsTableCombCurIndChanged, index=%d' % index)
        #update 'tbs' by calling getTbs when necessary
        self.validatePdschCw0McsCw1Mcs()
        
    def onDedPdschCfgXOverheadCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onDedPdschCfgXOverheadCombCurIndChanged, index=%d' % index)
        #update 'tbs' by calling getTbs when necessary
        self.validatePdschAntPorts()
    
    def updateDci01PrecodingLayersFieldLabel(self):
        self.ngwin.logEdit.append('-->inside updateDci01PrecodingLayersFieldLabel') 
        
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
            if not self.nrDedPuschCfgCbMaxRankEdit.text():
                self.nrDci01PuschPrecodingLayersFieldLabel.setText('Precoding info and num of layers:')
                self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(0)
                return
            numUeAp = int(self.nrUeAntPortsComb.currentText()[:-2])
            tp = self.nrDedPuschCfgTpComb.currentText()
            maxRank = int(self.nrDedPuschCfgCbMaxRankEdit.text()) 
            cbSubset = self.nrDedPuschCfgCbSubsetComb.currentText()
            #refer to 3GPP 38.212 vf30
            #Table 7.3.1.1.2-2: Precoding information and number of layers, for 4 antenna ports, if transform precoder is disabled and maxRank = 2 or 3 or 4
            #Table 7.3.1.1.2-3: Precoding information and number of layers for 4 antenna ports, if transform precoder is enabled, or if transform precoder is disabled and maxRank = 1
            #Table 7.3.1.1.2-4: Precoding information and number of layers, for 2 antenna ports, if transform precoder is disabled and maxRank = 2
            #Table 7.3.1.1.2-5: Precoding information and number of layers, for 2 antenna ports, if transform precoder is enabled, or if transform precoder is disabled and maxRank = 1
            if numUeAp == 4 and tp == 'disabled' and maxRank in (2,3,4):
                if cbSubset == 'fullyAndPartialAndNonCoherent':
                    self.nrDci01PuschPrecodingLayersFieldLabel.setText('Precoding info and num of layers[0-63]:')
                    self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(QIntValidator(0, 63))
                elif cbSubset == 'partialAndNonCoherent':
                    self.nrDci01PuschPrecodingLayersFieldLabel.setText('Precoding info and num of layers[0-31]:')
                    self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(QIntValidator(0, 31))
                else:
                    self.nrDci01PuschPrecodingLayersFieldLabel.setText('Precoding info and num of layers[0-15]:')
                    self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(QIntValidator(0, 15))
            elif numUeAp == 4 and (tp == 'enabled' or (tp == 'disabled' and maxRank == 1)):
                if cbSubset == 'fullyAndPartialAndNonCoherent':
                    self.nrDci01PuschPrecodingLayersFieldLabel.setText('Precoding info and num of layers[0-31]:')
                    self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(QIntValidator(0, 31))
                elif cbSubset == 'partialAndNonCoherent':
                    self.nrDci01PuschPrecodingLayersFieldLabel.setText('Precoding info and num of layers[0-15]:')
                    self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(QIntValidator(0, 15))
                else:
                    self.nrDci01PuschPrecodingLayersFieldLabel.setText('Precoding info and num of layers[0-3]:')
                    self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(QIntValidator(0, 3))
            elif numUeAp == 2 and tp == 'disabled' and maxRank == 2:
                if cbSubset == 'fullyAndPartialAndNonCoherent':
                    self.nrDci01PuschPrecodingLayersFieldLabel.setText('Precoding info and num of layers[0-15]:')
                    self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(QIntValidator(0, 15))
                elif cbSubset == 'nonCoherent':
                    self.nrDci01PuschPrecodingLayersFieldLabel.setText('Precoding info and num of layers[0-3]:')
                    self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(QIntValidator(0, 3))
                else:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Codebook subset "partialAndNonCoherent" is not supported for two antenna ports.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                    return
            elif numUeAp == 2 and (tp == 'enabled' or (tp == 'disabled' and maxRank == 1)):
                if cbSubset == 'fullyAndPartialAndNonCoherent':
                    self.nrDci01PuschPrecodingLayersFieldLabel.setText('Precoding info and num of layers[0-7]')
                    self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(QIntValidator(0, 7))
                elif cbSubset == 'nonCoherent':
                    self.nrDci01PuschPrecodingLayersFieldLabel.setText('Precoding info and num of layers[0-1]')
                    self.nrDci01PuschPrecodingLayersFieldEdit.setValidator(QIntValidator(0, 1))
                else:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Codebook subset "partialAndNonCoherent" is not supported for two antenna ports.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                    return
            else:
                pass
    
    def updateDci01SriFieldLabel(self):
        self.ngwin.logEdit.append('-->inside updateDci01SriFieldLabel') 
        
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'nonCodebook':
            if not self.nrDedPuschCfgNonCbMaxLayersEdit.text() or not self.nrSrsResSet1ResourceIdListEdit.text():
                self.nrDci01PuschSriFieldLabel.setText('SRS resource indicator:')
                self.nrDci01PuschSriFieldEdit.setValidator(0)
                return
            
            Lmax = int(self.nrDedPuschCfgNonCbMaxLayersEdit.text())
            
            try:
                srsSet1 = [int(i) for i in self.nrSrsResSet1ResourceIdListEdit.text().split(',') if len(i) > 0]
            except Exception as e:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Exception raised when parsing srs-resourceSet1: %s.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), e))
                return
            
            Nsrs = len(srsSet1)
            if Nsrs == 0 or sum([1 for i in srsSet1 if i in range(4)]) != Nsrs:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: srs-ResourceIdList of srsSet1 should be a comma-separated string which contains valid srs-ResourceId[0-3], for example, "0,1,2,3".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                return
            
            if Nsrs > 4:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: The maximum number of SRS resources that can be configured for non-codebook based uplink transmission is 4.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                return
            
            if ((0 in srsSet1 and self.nrSrsRes0NumAntPortsComb.currentText() != 'port1')
                or (1 in srsSet1 and self.nrSrsRes1NumAntPortsComb.currentText() != 'port1')
                or (2 in srsSet1 and self.nrSrsRes2NumAntPortsComb.currentText() != 'port1')
                or (3 in srsSet1 and self.nrSrsRes3NumAntPortsComb.currentText() != 'port1')):
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Only one SRS port can be configured for each SRS resource of the SRS resource set configured with usage set to "nonCodebook".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                return
            
            if Nsrs == 1:
                self.nrDci01PuschSriFieldLabel.setText('SRS resource indicator:')
                self.nrDci01PuschSriFieldEdit.clear()
                self.nrDci01PuschSriFieldEdit.setEnabled(False)
            else:
                self.nrDci01PuschSriFieldEdit.setEnabled(True)
                #refer to 3GPP 38.212 vf30
                #Table 7.3.1.1.2-28: SRI indication for non-codebook based PUSCH transmission, Lmax=1
                #Table 7.3.1.1.2-29: SRI indication for non-codebook based PUSCH transmission, Lmax=2
                #Table 7.3.1.1.2-30: SRI indication for non-codebook based PUSCH transmission, Lmax=3
                #Table 7.3.1.1.2-31: SRI indication for non-codebook based PUSCH transmission, Lmax=4
                nonCbSriRange = {
                    '1_2' : (0,1),
                    '1_3' : (0,3),
                    '1_4' : (0,3),
                    '2_2' : (0,3),
                    '2_3' : (0,7),
                    '2_4' : (0,15),
                    '3_2' : (0,3),
                    '3_3' : (0,7),
                    '3_4' : (0,15),
                    '4_2' : (0,3),
                    '4_3' : (0,7),
                    '4_4' : (0,15),
                    }
                key = '%s_%s' % (Lmax, Nsrs)
                minSri, maxSri = nonCbSriRange[key]
                self.nrDci01PuschSriFieldLabel.setText('SRS resource indicator[%d-%d]:' % (minSri, maxSri))
                self.nrDci01PuschSriFieldEdit.setValidator(QIntValidator(minSri, maxSri))
        else:
            if not self.nrSrsResSet0ResourceIdListEdit.text():
                self.nrDci01PuschSriFieldLabel.setText('SRS resource indicator:')
                self.nrDci01PuschSriFieldEdit.setValidator(0)
                return
            
            try:
                srsSet0 = [int(i) for i in self.nrSrsResSet0ResourceIdListEdit.text().split(',') if len(i) > 0]
            except Exception as e:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Exception raised when parsing srs-resourceSet0: %s.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), e))
                return
            
            Nsrs = len(srsSet0)
            if Nsrs == 0 or sum([1 for i in srsSet0 if i in range(4)]) != Nsrs:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: srs-ResourceIdList of srsSet0 should be a comma-separated string which contains valid srs-ResourceId[0-3], for example, "0,1,2,3".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                return
            
            if Nsrs > 2:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: The maximum number of SRS resources that can be configured for codebook based uplink transmission is 2.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                return
            
            if Nsrs == 1:
                self.nrDci01PuschSriFieldLabel.setText('SRS resource indicator:')
                self.nrDci01PuschSriFieldEdit.clear()
                self.nrDci01PuschSriFieldEdit.setEnabled(False)
            else:
                #refer to 3GPP 38.214 vf30 6.1.1.1
                #When multiple SRS resources are configured by SRS-ResourceSet with usage set to 'codebook', the UE shall expect that higher layer parameters nrofSRS-Ports in SRS-Resource in SRS-ResourceSet shall be configured with the same value for all these SRS resources.
                srsApSet = {0:self.nrSrsRes0NumAntPortsComb.currentText(), 1:self.nrSrsRes1NumAntPortsComb.currentText(), 2:self.nrSrsRes2NumAntPortsComb.currentText(), 3:self.nrSrsRes3NumAntPortsComb.currentText()}
                
                if srsApSet[srsSet0[0]] != srsApSet[srsSet0[1]]:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Parameter nrOfSRS-Ports must be the same when multiple SRS resources are configured for codebook based uplink transmission.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                    return
                
                self.nrDci01PuschSriFieldLabel.setText('SRS resource indicator[0-1]:')
                self.nrDci01PuschSriFieldEdit.setValidator(QIntValidator(0, 1))
                self.nrDci01PuschSriFieldEdit.setEnabled(True)
    
    def updateDci01AntPortsFieldLabel(self):
        self.ngwin.logEdit.append('-->inside updateDci01AntPortsFieldLabel') 
        
        tp = self.nrDedPuschCfgTpComb.currentText()
        dmrsType = self.nrDmrsDedPuschDmrsTypeComb.currentText()
        maxLen = self.nrDmrsDedPuschMaxLengthComb.currentText()
        if tp == 'enabled' and dmrsType == 'Type 1' and maxLen == 'len1':#rank=1
            self.nrDci01PuschAntPortsFieldLabel.setText('Antenna port(s)[0-3]:')
            self.nrDci01PuschAntPortsFieldEdit.setValidator(QIntValidator(0, 3))
        elif tp == 'enabled' and dmrsType == 'Type 1' and maxLen == 'len2':#rank=1
            self.nrDci01PuschAntPortsFieldLabel.setText('Antenna port(s)[0-15]:')
            self.nrDci01PuschAntPortsFieldEdit.setValidator(QIntValidator(0, 15))
        elif tp == 'disabled' and dmrsType == 'Type 1' and maxLen == 'len1':#rank=1/2/3/4
            self.nrDci01PuschAntPortsFieldLabel.setText('Antenna port(s)[0-7]:')
            self.nrDci01PuschAntPortsFieldEdit.setValidator(QIntValidator(0, 7))
        elif tp == 'disabled' and dmrsType == 'Type 1' and maxLen == 'len2':#rank=1/2/3/4
            self.nrDci01PuschAntPortsFieldLabel.setText('Antenna port(s)[0-15]:')
            self.nrDci01PuschAntPortsFieldEdit.setValidator(QIntValidator(0, 15))
        elif tp == 'disabled' and dmrsType == 'Type 2' and maxLen == 'len1':#rank=1/2/3/4
            self.nrDci01PuschAntPortsFieldLabel.setText('Antenna port(s)[0-15]:')
            self.nrDci01PuschAntPortsFieldEdit.setValidator(QIntValidator(0, 15))
        elif tp == 'disabled' and dmrsType == 'Type 2' and maxLen == 'len2':#rank=1/2/3/4
            self.nrDci01PuschAntPortsFieldLabel.setText('Antenna port(s)[0-31]:')
            self.nrDci01PuschAntPortsFieldEdit.setValidator(QIntValidator(0, 31))
        else:
            pass
    
    def validatePuschAntPorts(self):
        if not self.nrDci01PuschAntPortsFieldEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside validatePuschAntPorts')
        
        #determine rank
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
            if not self.nrDedPuschCfgCbMaxRankEdit.text() or not self.nrDci01PuschPrecodingLayersFieldEdit.text() or not self.nrSrsResSet0ResourceIdListEdit.text():
                return
            numUeAp = int(self.nrUeAntPortsComb.currentText()[:-2])
            tp = self.nrDedPuschCfgTpComb.currentText()
            maxRank = int(self.nrDedPuschCfgCbMaxRankEdit.text()) 
            cbSubset = self.nrDedPuschCfgCbSubsetComb.currentText()
            precoding = int(self.nrDci01PuschPrecodingLayersFieldEdit.text())
            key = '%s_%s' % ({'fullyAndPartialAndNonCoherent':0, 'partialAndNonCoherent':1, 'nonCoherent':2}[cbSubset], precoding) 
            if numUeAp == 4 and tp == 'disabled' and maxRank in (2,3,4):
                if key in self.nrDci01TpmiAp4Tp0MaxRank234 and self.nrDci01TpmiAp4Tp0MaxRank234[key] is not None:
                    rank, tpmi = self.nrDci01TpmiAp4Tp0MaxRank234[key]
                else:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDci01TpmiAp4Tp0MaxRank234.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    return
            elif numUeAp == 4 and (tp == 'enabled' or (tp == 'disabled' and maxRank == 1)):
                if key in self.nrDci01TpmiAp4Tp1OrTp0MaxRank1 and self.nrDci01TpmiAp4Tp1OrTp0MaxRank1[key] is not None:
                    rank, tpmi = self.nrDci01TpmiAp4Tp1OrTp0MaxRank1[key]
                else:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDci01TpmiAp4Tp1OrTp0MaxRank1.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    return
            elif numUeAp == 2 and tp == 'disabled' and maxRank == 2:
                if key in self.nrDci01TpmiAp2Tp0MaxRank2 and self.nrDci01TpmiAp2Tp0MaxRank2[key] is not None:
                    rank, tpmi = self.nrDci01TpmiAp2Tp0MaxRank2[key]
                else:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDci01TpmiAp2Tp0MaxRank2.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    return
            elif numUeAp == 2 and (tp == 'enabled' or (tp == 'disabled' and maxRank == 1)):
                if key in self.nrDci01TpmiAp2Tp1OrTp0MaxRank1 and self.nrDci01TpmiAp2Tp1OrTp0MaxRank1[key] is not None:
                    rank, tpmi = self.nrDci01TpmiAp2Tp1OrTp0MaxRank1[key]
                else:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDci01TpmiAp2Tp1OrTp0MaxRank1.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    return
            else:
                rank = 1
            
            #refer to 3GPP 38.214 vf30 6.1.1.1
            #The transmission precoder is selected from the uplink codebook that has a number of antenna ports equal to higher layer parameter nrofSRS-Ports in SRS-Config, as defined in Subclause 6.3.1.5 of [4, TS 38.211]. 
            firstResSrsSet0 = int(self.nrSrsResSet0ResourceIdListEdit.text().split(',')[0])
            if firstResSrsSet0 == 0:
                numSrsPorts = int(self.nrSrsRes0NumAntPortsComb.currentText()[-1])
            elif firstResSrsSet0 == 1:
                numSrsPorts = int(self.nrSrsRes1NumAntPortsComb.currentText()[-1])
            elif firstResSrsSet0 == 2:
                numSrsPorts = int(self.nrSrsRes2NumAntPortsComb.currentText()[-1])
            elif firstResSrsSet0 == 3:
                numSrsPorts = int(self.nrSrsRes3NumAntPortsComb.currentText()[-1])
            else:
                pass
            if rank > numSrsPorts:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: TRI = %s while nrofSRS-Ports of the configured SRS resource(s) is "%s" for CB based PUSCH.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), rank, '%s%d' % ('ports' if numSrsPorts > 1 else 'port', numSrsPorts)))
                return
        else:
            if not self.nrDedPuschCfgNonCbMaxLayersEdit.text() or not self.nrSrsResSet1ResourceIdListEdit.text() or not self.nrDci01PuschSriFieldEdit.text():
                return
            
            Lmax = int(self.nrDedPuschCfgNonCbMaxLayersEdit.text())
            
            try:
                srsSet1 = [int(i) for i in self.nrSrsResSet1ResourceIdListEdit.text().split(',') if len(i) > 0]
            except Exception as e:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Exception raised: %s.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), e))
                return
            Nsrs = len(srsSet1)
            
            sri = int(self.nrDci01PuschSriFieldEdit.text())
            
            key = '%s_%s_%s' % (Lmax, Nsrs, sri)
            self.dci01NonCbSrsList = None
            if Nsrs == 1:
                rank = 1
                self.dci01NonCbSrsList = [srsSet1[0]]
            else:
                if key in self.nrDci01NonCbSri and self.nrDci01NonCbSri[key] is not None:
                    rank = len(self.nrDci01NonCbSri[key])
                    self.dci01NonCbSrsList = self.nrDci01NonCbSri[key]
                else:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDci01NonCbSri.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    return
                
        #set dmrs for pusch
        tp = self.nrDedPuschCfgTpComb.currentText()
        dmrsType = self.nrDmrsDedPuschDmrsTypeComb.currentText()
        maxLen = self.nrDmrsDedPuschMaxLengthComb.currentText()
        key = '%d_%s_%s_%d_%s' % (1 if tp == 'enabled' else 0, dmrsType[-1], maxLen[-1], rank, self.nrDci01PuschAntPortsFieldEdit.text())
        if not key in self.nrDci01AntPorts or self.nrDci01AntPorts[key] is None:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDci01AntPorts.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
            return
        
        cdmGroups, dmrsPorts, numDmrsSymbs = self.nrDci01AntPorts[key]
        
        self.nrDmrsDedPuschCdmGroupsWoDataEdit.setText(str(cdmGroups))
        self.nrDmrsDedPuschDmrsPortsEdit.setText(','.join([str(i) for i in dmrsPorts]))
        self.nrDmrsDedPuschFrontLoadSymbsEdit.setText(str(numDmrsSymbs))
        
        #check and set ptrs for pusch
        #refer to 3GPP 38.214 vf30 6.2.2
        '''
        If a UE transmitting PUSCH is configured with the higher layer parameter phaseTrackingRS in DMRS-UplinkConfig, the UE may assume that the following configurations are not occurring simultaneously for the transmitted PUSCH
            -	any DM-RS ports among 4-7 or 6-11 for DM-RS configurations type 1 and type 2, respectively are scheduled for the UE and PT-RS is transmitted from the UE.
        '''
        dmrsApSetNoPtrs = list(range(4, 8)) if dmrsType == 'Type 1' else list(range(6, 12))
        noPtrs = False
        for i in dmrsPorts:
            if i in dmrsApSetNoPtrs:
                noPtrs = True
                break
        
        if noPtrs:
            self.nrPtrsPuschSwitchComb.setCurrentText('no')
            self.nrPtrsPuschSwitchComb.setEnabled(False)
            self.nrPtrsPuschDmrsAntPortsEdit.clear()
            self.nrPtrsPuschTpDmrsAntPortsEdit.clear()
            self.nrDci01PuschPtrsDmrsMappingEdit.setEnabled(False)
            self.nrDci01PuschPtrsDmrsMappingEdit.clear()
        else:
            self.nrPtrsPuschSwitchComb.setEnabled(True)
            if rank > 1:
                self.nrDci01PuschPtrsDmrsMappingEdit.setEnabled(True)
                self.nrPtrsPuschDmrsAntPortsEdit.clear()
                self.nrPtrsPuschTpDmrsAntPortsEdit.clear()
            else:
                self.nrDci01PuschPtrsDmrsMappingEdit.setEnabled(False)
                self.nrDci01PuschPtrsDmrsMappingEdit.clear()
                if tp == 'enabled':
                    self.nrPtrsPuschTpDmrsAntPortsEdit.setText(str(dmrsPorts[0]))
                    self.nrPtrsPuschDmrsAntPortsEdit.clear()
                else:
                    self.nrPtrsPuschDmrsAntPortsEdit.setText(str(dmrsPorts[0]))
                    self.nrPtrsPuschTpDmrsAntPortsEdit.clear()
            
            self.updatePtrsPusch()
        
        #set tbs by calling getTbs
        if not self.nrDci01PuschTimeAllocFieldEdit.text() or not self.nrDci01PuschTimeAllocLEdit.text() or not self.nrDci01PuschTimeAllocSEdit.text() or not self.nrDci01PuschTimeAllocSlivEdit.text():
            return
        
        if self.nrDci01PuschFreqAllocTypeComb.currentText() == 'RA Type1' and (not self.nrDci01PuschFreqAllocType1LRbsEdit.text() or not self.nrDci01PuschFreqAllocType1RbStartEdit.text() or not self.nrDci01PuschFreqAllocFieldEdit.text()):
            return
        
        if self.nrDci01PuschFreqAllocTypeComb.currentText() == 'RA Type0' and (not self.nrDci01PuschFreqAllocFieldEdit.text() or len(self.nrDci01PuschFreqAllocFieldEdit.text()) != self.bitwidthType0Pusch or int(self.nrDci01PuschFreqAllocFieldEdit.text(), 2) == 0):
            return
        
        if not self.nrDci01PuschCw0McsEdit.text():
            return
        
        td = int(self.nrDci01PuschTimeAllocLEdit.text())
        if self.nrDci01PuschFreqAllocTypeComb.currentText() == 'RA Type1':
            fd = int(self.nrDci01PuschFreqAllocType1LRbsEdit.text())
        else:
            fd = sum([self.rbgsType0Pusch[i] for i in range(self.bitwidthType0Pusch) if self.nrDci01PuschFreqAllocFieldEdit.text()[i] == '1'])
            
        #calculate dmrs overhead
        mappingType = self.nrDci01PuschTimeAllocMappingTypeComb.currentText()
        freqHop = self.nrDci01PuschFreqAllocFreqHopComb.currentText()
        if freqHop == 'intra-slot':
            #refer to 3GPP 38.211 vf30 6.4.1.1.3
            #if the higher-layer parameter dmrs-AdditionalPosition is not set to 'pos0' and intra-slot frequency hopping is enabled according to clause 7.3.1.1.2 in [4, TS 38.212] and by higher layer, Tables 6.4.1.1.3-6 shall be used assuming dmrs-AdditionalPosition is equal to 'pos1' for each hop.
            #refer to 3GPP 38.214 vf30 6.3
            #In case of intra-slot frequency hopping is configured, the number of symbols in the first hop is given by floor(N_PUSCH_symb/2) , the number of symbols in the second hop is given by N_PUSCH_symb - floor(N_PUSCH_symb/2) , where N_PUSCH_symb is the length of the PUSCH transmission in OFDM symbols in one slot.
            key1 = '%s_%s_%s_%s_1st' % (math.floor(td / 2), mappingType, self.nrMibDmRsTypeAPosComb.currentText()[3:] if mappingType == 'Type A' else '0', 'pos1' if self.nrDmrsDedPuschAddPosComb.currentText() != 'pos0' else 'pos0')
            key2 = '%s_%s_%s_%s_2nd' % (td - math.floor(td / 2), mappingType, self.nrMibDmRsTypeAPosComb.currentText()[3:] if mappingType == 'Type A' else '0', 'pos1' if self.nrDmrsDedPuschAddPosComb.currentText() != 'pos0' else 'pos0')
            if numDmrsSymbs == 1:
                if not key1 in self.nrDmrsPuschPosOneSymbWithIntraSlotFh or not key2 in self.nrDmrsPuschPosOneSymbWithIntraSlotFh or self.nrDmrsPuschPosOneSymbWithIntraSlotFh[key1] is None or self.nrDmrsPuschPosOneSymbWithIntraSlotFh[key2] is None:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(key_1stHop="%s", key_2ndHop="%s") when referring nrDmrsPuschPosOneSymbWithIntraSlotFh!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key1, key2))
                    return
                val1 = self.nrDmrsPuschPosOneSymbWithIntraSlotFh[key1]
                val2 = self.nrDmrsPuschPosOneSymbWithIntraSlotFh[key2]
            else:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Only single-symbol front-load DM-RS for PUSCH is supported when intra-slot frequency hopping is enabled!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                return
        else:
            key = '%s_%s_%s' % (td, self.nrDci01PuschTimeAllocMappingTypeComb.currentText(), self.nrDmrsDedPuschAddPosComb.currentText())
            if numDmrsSymbs == 1:
                if not key in self.nrDmrsPuschPosOneSymbWoIntraSlotFh.keys() or self.nrDmrsPuschPosOneSymbWoIntraSlotFh[key] is None:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDmrsPuschPosOneSymbWoIntraSlotFh!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    return
                val = self.nrDmrsPuschPosOneSymbWoIntraSlotFh[key]
            else:
                if not key in self.nrDmrsPuschPosTwoSymbsWoIntraSlotFh.keys() or self.nrDmrsPuschPosTwoSymbsWoIntraSlotFh[key] is None:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring nrDmrsPuschPosTwoSymbsWoIntraSlotFh!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                    return
                val = self.nrDmrsPuschPosTwoSymbsWoIntraSlotFh[key]
        
        #refer to 3GPP 38.211 vf30
        #For PUSCH mapping type A, duration of 4 symbols in Table 6.4.1.1.3-4 is only applicable when dmrs-TypeA-Position is equal to 'pos2'.
        if self.nrDci01PuschTimeAllocMappingTypeComb.currentText() == 'Type A' and td == 4 and self.nrMibDmRsTypeAPosComb.currentText() != 'pos2':
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: For PUSCH mapping type A, duration of 4 symbols in Table 6.4.1.1.3-4 is only applicable when dmrs-TypeA-Position is equal to "pos2".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            return
        
        if freqHop == 'intra-slot':
            dmrsOh = (2 * cdmGroups) * (len(val1) + len(val2))
            self.ngwin.logEdit.append('PUSCH(DCI 0_1) DMRS overhead: cdmGroupsWoData=%d, key1="%s", val1=%s, key2="%s", val2=%s' % (cdmGroups, key1, val1, key2, val2))
        else:
            dmrsOh = (2 * cdmGroups) * len(val)
            self.ngwin.logEdit.append('PUSCH(DCI 0_1) DMRS overhead: cdmGroupsWoData=%d, key="%s", val=%s' % (cdmGroups, key, val))
        
        tp = 1 if self.nrDedPuschCfgTpComb.currentText() == 'enabled' else 0
        mcsCw0 = int(self.nrDci01PuschCw0McsEdit.text())
        
        tbs = self.getTbs(sch='pusch', tp=tp, rnti='c-rnti', tab=self.nrDedPuschCfgMcsTableComb.currentText(), td=td, fd=fd, mcs=mcsCw0, layer=len(dmrsPorts), dmrs=dmrsOh, xoh=int(self.nrDedPuschCfgXOverheadComb.currentText()[3:]), scale=1)
        
        self.nrDci01PuschTbsEdit.setText(str(tbs) if tbs is not None else '')
        
    def onPtrsPuschTpGroupPatCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onPtrsPuschTpGroupPatCombCurIndChanged, index=%d' % index)
        grpPatterns = {'pattern 0':(2,2), 'pattern 1':(2,4), 'pattern 2':(4,2), 'pattern 3':(4,4), 'pattern 4':(8,4)}
        pattern = grpPatterns[self.nrPtrsPuschTpGroupPatComb.currentText()]
        self.nrPtrsPuschTpNumGroupsEdit.setText(str(pattern[0]))
        self.nrPtrsPuschTpSamplesPerGroupEdit.setText(str(pattern[1]))
        
    def onPtrsPuschMaxNumPortsCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onPtrsPuschMaxNumPortsCombCurIndChanged, index=%d' % index)
        self.updatePtrsPusch()
        
    def updatePtrsPusch(self): 
        if self.nrDedPuschCfgTpComb.currentText() == 'enabled':
            return
        
        if not self.nrDci01PuschPtrsDmrsMappingEdit.isEnabled() or not self.nrDci01PuschPtrsDmrsMappingEdit.text():
            return
        
        if not self.nrDmrsDedPuschDmrsPortsEdit.text():
            return
        
        self.ngwin.logEdit.append('-->inside updatePtrsPusch')
        dmrsPorts = [int(s) for s in self.nrDmrsDedPuschDmrsPortsEdit.text().split(',')]
        ptrsDmrsMap = int(self.nrDci01PuschPtrsDmrsMappingEdit.text())
        maxPtrsPorts = int(self.nrPtrsPuschMaxNumPortsComb.currentText()[-1])
        if maxPtrsPorts == 1:
            if ptrsDmrsMap in range(len(dmrsPorts)):
                self.nrPtrsPuschDmrsAntPortsEdit.setText(str(dmrsPorts[ptrsDmrsMap]))
            else:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Valid "PTRS-DMRS association" field of DCI 0_1 is %s for PTRS port 0.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '[0]' if len(dmrsPorts) == 1 else '[0-%d]' % (len(dmrsPorts)-1)))
                self.nrDci01PuschPtrsDmrsMappingEdit.clear()
                return
        else:
            ptrsPortDict = {0:[], 1:[]}
            if self.nrDedPuschCfgTxCfgComb.currentText() == 'nonCodebook':
                if self.dci01NonCbSrsList is not None:
                    for i in self.dci01NonCbSrsList:
                        if i == 0:
                            ptrsPortDict[int(self.nrSrsRes0NonCbPtrsPortIndComb.currentText()[-1])].append(dmrsPorts[self.dci01NonCbSrsList.index(i)])
                        elif i == 1:
                            ptrsPortDict[int(self.nrSrsRes1NonCbPtrsPortIndComb.currentText()[-1])].append(dmrsPorts[self.dci01NonCbSrsList.index(i)])
                        elif i == 2:
                            ptrsPortDict[int(self.nrSrsRes2NonCbPtrsPortIndComb.currentText()[-1])].append(dmrsPorts[self.dci01NonCbSrsList.index(i)])
                        elif i == 3:
                            ptrsPortDict[int(self.nrSrsRes3NonCbPtrsPortIndComb.currentText()[-1])].append(dmrsPorts[self.dci01NonCbSrsList.index(i)])
                        else:
                            pass
            else:
                for i in dmrsPorts:
                    if i in (0, 2):
                        ptrsPortDict[0].append(i)
                    elif i in (1, 3):
                        ptrsPortDict[1].append(i)
                    else:
                        pass
            
            if len(ptrsPortDict[0]) >= 1 and len(ptrsPortDict[1]) == 0:
                #PTRS port 0
                if ptrsDmrsMap in range(len(dmrsPorts)):
                    self.nrPtrsPuschDmrsAntPortsEdit.setText(str(dmrsPorts[ptrsDmrsMap]))
                else:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Valid "PTRS-DMRS association" field of DCI 0_1 is %s for PTRS port 0.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), '[0]' if len(dmrsPorts) == 1 else '[0-%d]' % (len(dmrsPorts)-1)))
                    self.nrDci01PuschPtrsDmrsMappingEdit.clear()
                    return
            elif len(ptrsPortDict[0]) >= 1 and len(ptrsPortDict[1]) >= 1:
                #PTRS port 0 and port 1
                if len(ptrsPortDict[0]) == 1 and len(ptrsPortDict[1]) == 1:
                    validPtrsDmrsMap = [0]
                elif len(ptrsPortDict[0]) == 1 and len(ptrsPortDict[1]) == 2:
                    validPtrsDmrsMap = [0, 1]
                elif len(ptrsPortDict[0]) == 2 and len(ptrsPortDict[1]) == 1:
                    validPtrsDmrsMap = [0, 2]
                elif len(ptrsPortDict[0]) == 2 and len(ptrsPortDict[1]) == 2:
                    validPtrsDmrsMap = [0, 1, 2, 3]
                else:
                    pass
                
                if ptrsDmrsMap in validPtrsDmrsMap:
                    bits = '{:02b}'.format(ptrsDmrsMap)
                    associatedDmrsPorts = []
                    for i in range(2):
                        associatedDmrsPorts.append(ptrsPortDict[i][0] if bits[i] == '0' else ptrsPortDict[i][1])
                        
                    self.nrPtrsPuschDmrsAntPortsEdit.setText(','.join([str(i) for i in associatedDmrsPorts]))
                else:
                    self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Valid "PTRS-DMRS association" field of DCI 0_1 is %s for PTRS port 0/1.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), validPtrsDmrsMap))
                    return
            else:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid PTRS port settings with maxNrofPorts of PTRS-UplinkConfig is "n2".' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                return
    
    def onRachSsbPerRachOccasionCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onRachSsbPerRachOccasionCombCurIndChanged, index=%d' % index)
        #refer to 3GPP 38.331 vf30
        '''
        totalNumberOfRA-Preambles
        Total number of preambles used for contention based and contention free random access in the RACH resources defined in RACH-ConfigCommon, excluding preambles used for other purposes (e.g. for SI request). If the field is absent, the all 64 preambles are available for RA. The setting should be consistent with the setting of ssb-perRACH-OccasionAndCB-PreamblesPerSSB, i.e. it should be a multiple of the number of SSBs per RACH occasion.
        '''
        if self.nrRachNumRaPreamblesEdit.text():
            ssbPerRachOccasion = max(1, self.nrSsbPerRachOccasion2Float[self.nrRachSsbPerRachOccasionComb.currentText()])
            numRaPreambles = int(self.nrRachNumRaPreamblesEdit.text())
            if numRaPreambles % ssbPerRachOccasion != 0:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Total number of RA preambles should be a multiple of the number of SSBs per RACH occasion.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                self.nrRachSsbPerRachOccasionComb.setCurrentIndex(-1)
                self.nrRachCbPreamblesPerSsbComb.setCurrentIndex(-1)
                return
        cbPreamblesPerSsbSet =  self.nrSsbPerRachOccasion2CbPreamblesPerSsb[self.nrRachSsbPerRachOccasionComb.currentText()]
        self.nrRachCbPreamblesPerSsbComb.clear()
        self.nrRachCbPreamblesPerSsbComb.addItems([str(i) for i in cbPreamblesPerSsbSet])
    
    def onRachNumRaPreamblesTextChanged(self):
        if not self.nrRachNumRaPreamblesEdit.text() or self.nrRachSsbPerRachOccasionComb.currentIndex() < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onRachNumRaPreamblesTextChanged')
        #refer to 3GPP 38.331 vf30
        '''
        totalNumberOfRA-Preambles
        Total number of preambles used for contention based and contention free random access in the RACH resources defined in RACH-ConfigCommon, excluding preambles used for other purposes (e.g. for SI request). If the field is absent, the all 64 preambles are available for RA. The setting should be consistent with the setting of ssb-perRACH-OccasionAndCB-PreamblesPerSSB, i.e. it should be a multiple of the number of SSBs per RACH occasion.
        '''
        ssbPerRachOccasion = max(1, self.nrSsbPerRachOccasion2Float[self.nrRachSsbPerRachOccasionComb.currentText()])
        numRaPreambles = int(self.nrRachNumRaPreamblesEdit.text())
        if numRaPreambles % ssbPerRachOccasion != 0:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Total number of RA preambles should be a multiple of the number of SSBs per RACH occasion.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            self.nrRachSsbPerRachOccasionComb.setCurrentIndex(-1)
            self.nrRachCbPreamblesPerSsbComb.setCurrentIndex(-1)
            return
        
    def onPucchSib1PucchResCommonTextChanged(self):
        if not self.nrPucchSib1PucchResCommonEdit.text():
            self.nrPucchSib1PucchFmtComb.setCurrentIndex(-1)
            self.nrPucchSib1StartingSymbEdit.clear()
            self.nrPucchSib1NumSymbsEdit.clear()
            self.nrPucchSib1PrbOffsetEdit.clear()
            self.nrPucchSib1IniCsIndexesSetEdit.clear()
            return
        
        self.ngwin.logEdit.append('-->inside onPucchSib1PucchResCommonTextChanged')
        pucchResInd = int(self.nrPucchSib1PucchResCommonEdit.text())
        pucchFmt, firstSymb, numSymbs, prbOffset, initialCsSet = self.nrCommonPucchResSets[pucchResInd]
        if pucchResInd == 15:
            if self.nrIniUlBwpGenericLocAndBwEdit.text() and self.nrIniUlBwpGenericLRbsEdit.text() and self.nrIniUlBwpGenericRbStartEdit.text():
                prbOffset = math.floor(int(self.nrIniUlBwpGenericLRbsEdit.text()) / 4)
            else:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Initial UL BWP must be configured properly when pucch-ResourceCommon(SIB1)=15.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
                self.nrPucchSib1PucchResCommonEdit.clear()
                return
        
        self.nrPucchSib1PucchFmtComb.setCurrentText('format %d' % pucchFmt)
        self.nrPucchSib1StartingSymbEdit.setText(str(firstSymb))
        self.nrPucchSib1NumSymbsEdit.setText(str(numSymbs))
        self.nrPucchSib1PrbOffsetEdit.setText(str(prbOffset))
        self.nrPucchSib1IniCsIndexesSetEdit.setText(str(initialCsSet))
        
    def onSrsResNumAntPortsCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onSrsResNumAntPortsCombCurIndChanged, index=%d' % index)
        self.updateDci01SriFieldLabel()
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'codebook':
            self.validatePuschAntPorts()
            
    def onSrsResNonCbPtrsPortIndCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onSrsResNonCbPtrsPortIndCombCurIndChanged, index=%d' % index)
        if self.nrDedPuschCfgTxCfgComb.currentText() == 'nonCodebook':
            self.updatePtrsPusch()
            
    def onSrsRes0NumCombCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onSrsRes0NumCombCombCurIndChanged, index=%d' % index)
        numComb = int(self.nrSrsRes0NumCombComb.currentText()[-1])
        self.nrSrsRes0CombOffsetLabel.setText('combOffset[0-%d]:' % (numComb - 1))
        self.nrSrsRes0CombOffsetEdit.setText('0')
    
    def onSrsRes1NumCombCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onSrsRes1NumCombCombCurIndChanged, index=%d' % index)
        numComb = int(self.nrSrsRes1NumCombComb.currentText()[-1])
        self.nrSrsRes1CombOffsetLabel.setText('combOffset[0-%d]:' % (numComb - 1))
        self.nrSrsRes1CombOffsetEdit.setText('0')
        
    def onSrsRes2NumCombCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onSrsRes2NumCombCombCurIndChanged, index=%d' % index)
        numComb = int(self.nrSrsRes2NumCombComb.currentText()[-1])
        self.nrSrsRes2CombOffsetLabel.setText('combOffset[0-%d]:' % (numComb - 1))
        self.nrSrsRes2CombOffsetEdit.setText('0')
        
    def onSrsRes3NumCombCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onSrsRes3NumCombCombCurIndChanged, index=%d' % index)
        numComb = int(self.nrSrsRes3NumCombComb.currentText()[-1])
        self.nrSrsRes3CombOffsetLabel.setText('combOffset[0-%d]:' % (numComb - 1))
        self.nrSrsRes3CombOffsetEdit.setText('0')
    
    def onSrsRes0PeriodCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onSrsRes0PeriodCombCurIndChanged, index=%d' % index)
        period = int(self.nrSrsRes0PeriodComb.currentText()[2:])
        if period == 1:
            self.nrSrsRes0OffsetLabel.setText('SRS-Offset[0]:')
        else:
            self.nrSrsRes0OffsetLabel.setText('SRS-Offset[0-%d]:' % (period - 1))
        self.nrSrsRes0OffsetEdit.setText('0')
    
    def onSrsRes1PeriodCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onSrsRes1PeriodCombCurIndChanged, index=%d' % index)
        period = int(self.nrSrsRes1PeriodComb.currentText()[2:])
        if period == 1:
            self.nrSrsRes1OffsetLabel.setText('SRS-Offset[0]:')
        else:
            self.nrSrsRes1OffsetLabel.setText('SRS-Offset[0-%d]:' % (period - 1))
        self.nrSrsRes1OffsetEdit.setText('0')
        
    def onSrsRes2PeriodCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onSrsRes2PeriodCombCurIndChanged, index=%d' % index)
        period = int(self.nrSrsRes2PeriodComb.currentText()[2:])
        if period == 1:
            self.nrSrsRes2OffsetLabel.setText('SRS-Offset[0]:')
        else:
            self.nrSrsRes2OffsetLabel.setText('SRS-Offset[0-%d]:' % (period - 1))
        self.nrSrsRes2OffsetEdit.setText('0')
        
    def onSrsRes3PeriodCombCurIndChanged(self, index):
        if index < 0:
            return
        
        self.ngwin.logEdit.append('-->inside onSrsRes3PeriodCombCurIndChanged, index=%d' % index)
        period = int(self.nrSrsRes3PeriodComb.currentText()[2:])
        if period == 1:
            self.nrSrsRes3OffsetLabel.setText('SRS-Offset[0]:')
        else:
            self.nrSrsRes3OffsetLabel.setText('SRS-Offset[0-%d]:' % (period - 1))
        self.nrSrsRes3OffsetEdit.setText('0')
            
    def getTbs(self, sch='pdsch', tp=0, rnti='c-rnti', tab='qam64', td=1, fd=1, mcs=0, layer=1, dmrs=0, xoh=0, scale=1):
        self.ngwin.logEdit.append('---->inside getTbs: sch="%s", tp=%d, rnti="%s", tab="%s", td=%d, fd=%d, mcs=%d, layer=%d, dmrs=%d, xoh=%d, scale=%.2f' % (sch, tp, rnti, tab, td, fd, mcs, layer, dmrs, xoh, scale)) 
        
        if rnti not in ('c-rnti', 'si-rnti', 'ra-rnti', 'tc-rnti', 'msg3'):
            return None
        
        if tab not in ('qam256', 'qam64', 'qam64LowSE'):
            return None
        
        #reset xoh to 0 for PDSCH when rnti='SI-RNTI', 'RA-RNTI' and for Msg3 PUSCH
        #FIXME what's the case for rnti='TC-RNTI'(msg4)?
        if rnti in ('si-rnti', 'ra-rnti', 'tc-rnti', 'msg3'):
            xoh = 0
        
        #reset scale to 1 for PDSCH when rnti is not 'RA-RNTI' and for PUSCH
        if rnti != 'ra-rnti':
            scale = 1
        
        #refer to 3GPP 38.214 vf30
        #5.1.3	Modulation order, target code rate, redundancy version and transport block size determination
        #6.1.4	Modulation order, redundancy version and transport block size determination
        
        #1st step: get Qm and R(x1024)
        if sch == 'pdsch' or (sch == 'pusch' and tp == 0):
            if rnti == 'c-rnti' and tab == 'qam256':
                val = self.nrPdschMcsTabQam256[mcs]
                if val is None:
                    return None
            elif rnti == 'c-rnti' and tab == 'qam64LowSE':
                val = self.nrPdschMcsTabQam64LowSE[mcs]
                if val is None:
                    return None
            else:
                val = self.nrPdschMcsTabQam64[mcs]
                if val is None:
                    return None
            pass
        elif sch == 'pusch' and tp == 1:
            if rnti == 'c-rnti' and tab == 'qam256':
                val = self.nrPdschMcsTabQam256[mcs]
                if val is None:
                    return None
            elif rnti == 'c-rnti' and tab == 'qam64LowSE':
                val = self.nrPuschTpMcsTabQam64LowSE[mcs]
                if val is None:
                    return None
            else:
                val = self.nrPuschTpMcsTabQam64[mcs]
                if val is None:
                    return None
        else:
            return None
        
        Qm, R = val
        #FIXME what's the case for rnti='TC-RNTI'(msg4)?
        if rnti in ('si-rnti', 'ra-rnti', 'tc-rnti') and Qm > 2:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: The UE is not expected to decode a PDSCH scheduled with P-RNTI, RA-RNTI, SI-RNTI and Qm > 2! (FIXME)Assume the same rule applies to PDSCH scheduled with TC-RNTI.' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            return None
        
        #2nd step: get N_RE
        N_RE = self.numScPerPrb * td - dmrs - xoh
        N_RE = min(156, N_RE) * fd
        
        #3rd step: get N_info
        N_info = math.ceil(scale * N_RE * R * Qm * layer / 1024)
        if N_info <= 3824:
            #4th step: get TBS
            n = max(3, math.floor(math.log2(N_info)) - 6)
            N_info = max(24, 2 ** n * math.floor(N_info / 2 ** n))
            
            tbs = None
            for i in self.nrTbsTabLessThan3824:
                if i >= N_info:
                    tbs = i
                    break
        else:
            #5th step: get TBS
            n = math.floor(math.log2(N_info - 24)) - 5
            N_info = max(3840, 2 ** n * math.ceil((N_info - 24) / 2 ** n))
            if R <= 256:
                C = math.ceil((N_info + 24) / 3816)
                tbs = 8 * C * math.ceil((N_info + 24) / (8 * C)) - 24
            else:
                if N_info > 8424:
                    C = math.ceil((N_info + 24) / 8424)
                    tbs = 8 * C * math.ceil((N_info + 24) / (8 * C)) - 24
                else:
                    tbs = 8 * math.ceil((N_info + 24) / 8 ) - 24
        
        if rnti == 'si-rnti' and tbs is not None and tbs > 2976:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: The UE is not expected to receive a PDSCH assigned by a PDCCH with CRC scrambled by SI-RNTI with a TBS exceeding 2976 bits!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
            return None
        
        return tbs

    def onOkBtnClicked(self):
        self.ngwin.logEdit.append('-->inside onOkBtnClicked')
        #TODO
        self.accept()
    
    def parseRiv(self, riv, N_BWP_size):
        div = riv // N_BWP_size
        rem = riv % N_BWP_size
        
        L_RBs = [div + 1, N_BWP_size + 1 - div]
        RB_start = [rem, N_BWP_size - 1 - rem]
        #self.ngwin.logEdit.append('Info: RIV = %d, L_RBs = [%d,%d], RB_start = [%d,%d], N_BWP_size = %d.' % (riv, L_RBs[0], L_RBs[1], RB_start[0], RB_start[1], N_BWP_size))
        if L_RBs[0] >= 1 and L_RBs[0] <= (N_BWP_size - RB_start[0]) and L_RBs[0] <= math.floor(N_BWP_size / 2):
            return (L_RBs[0], RB_start[0])
        elif L_RBs[1] >= 1 and L_RBs[1] <= (N_BWP_size - RB_start[1]) and L_RBs[1] > math.floor(N_BWP_size / 2):
            return (L_RBs[1], RB_start[1])
        else:
            #invalid RIV
            return (None, None)
    
    def makeRiv(self, L_RBs, RB_start, N_BWP_size):
        if L_RBs < 1 or L_RBs > (N_BWP_size - RB_start):
            #self.ngwin.logEdit.append('Error: L_RBs = %d, RB_start = %d, N_BWP_size = %d.' % (L_RBs, RB_start, N_BWP_size))
            return None 
        
        if (L_RBs - 1) <= math.floor(N_BWP_size / 2):
            riv = N_BWP_size * (L_RBs - 1) + RB_start
        else:
            riv = N_BWP_size * (N_BWP_size - L_RBs + 1) + (N_BWP_size - 1 - RB_start)
        
        return riv
    
    def makeSliv(self, S, L):
        if L <= 0 or L > 14 - S:
            return None
        
        if (L - 1) <= 7:
            sliv = 14 * (L - 1) + S
        else:
            sliv = 14 * (14 - L + 1) + (14 - 1 - S)
        
        return sliv
    
    def initPdschSliv(self):
        #prefix
        #'00': mapping type A + normal cp
        #'01': mapping type A + extended cp
        #'10': mapping type B + normal cp
        #'11': mapping type B + extended cp
        
        self.nrPdschToSliv = dict()
        self.nrPdschFromSliv = dict()
        
        #case1: prefix='00'
        prefix = '00'
        for S in range(4):
            for L in range(3, 15):
                if S+L in range(3, 15):
                    sliv = self.makeSliv(S, L)
                    if sliv is not None:
                        keyToSliv = '%s_%s_%s' % (prefix, S, L)
                        self.nrPdschToSliv[keyToSliv] = sliv
                        keyFromSliv = '%s_%s' % (prefix, sliv)
                        self.nrPdschFromSliv[keyFromSliv] = (S, L)
        
        #case2: prefix='01'
        prefix = '01'
        for S in range(4):
            for L in range(3, 13):
                if S+L in range(3, 13):
                    sliv = self.makeSliv(S, L)
                    if sliv is not None:
                        keyToSliv = '%s_%s_%s' % (prefix, S, L)
                        self.nrPdschToSliv[keyToSliv] = sliv
                        keyFromSliv = '%s_%s' % (prefix, sliv)
                        self.nrPdschFromSliv[keyFromSliv] = (S, L)
        
        #case3: prefix='10'
        prefix = '10'
        for S in range(13):
            for L in (2,4,7):
                if S+L in range(2, 15):
                    sliv = self.makeSliv(S, L)
                    if sliv is not None:
                        keyToSliv = '%s_%s_%s' % (prefix, S, L)
                        self.nrPdschToSliv[keyToSliv] = sliv
                        keyFromSliv = '%s_%s' % (prefix, sliv)
                        self.nrPdschFromSliv[keyFromSliv] = (S, L)
        
        #case4: prefix='11'
        prefix = '11'
        for S in range(11):
            for L in (2,4,6):
                if S+L in range(2, 13):
                    sliv = self.makeSliv(S, L)
                    if sliv is not None:
                        keyToSliv = '%s_%s_%s' % (prefix, S, L)
                        self.nrPdschToSliv[keyToSliv] = sliv
                        keyFromSliv = '%s_%s' % (prefix, sliv)
                        self.nrPdschFromSliv[keyFromSliv] = (S, L)
                    
    
    def initPuschSliv(self):
        #prefix
        #'00': mapping type A + normal cp
        #'01': mapping type A + extended cp
        #'10': mapping type B + normal cp
        #'11': mapping type B + extended cp
        
        self.nrPuschToSliv = dict()
        self.nrPuschFromSliv = dict()
        
        #case1: prefix='00'
        prefix = '00'
        for S in (0,):
            for L in range(4, 15):
                if S+L in range(4, 15):
                    sliv = self.makeSliv(S, L)
                    if sliv is not None:
                        keyToSliv = '%s_%s_%s' % (prefix, S, L)
                        self.nrPuschToSliv[keyToSliv] = sliv
                        keyFromSliv = '%s_%s' % (prefix, sliv)
                        self.nrPuschFromSliv[keyFromSliv] = (S, L)
        
        #case2: prefix='01'
        prefix = '01'
        for S in (0,):
            for L in range(4, 13):
                if S+L in range(4, 13):
                    sliv = self.makeSliv(S, L)
                    if sliv is not None:
                        keyToSliv = '%s_%s_%s' % (prefix, S, L)
                        self.nrPuschToSliv[keyToSliv] = sliv
                        keyFromSliv = '%s_%s' % (prefix, sliv)
                        self.nrPuschFromSliv[keyFromSliv] = (S, L)
        
        #case3: prefix='10'
        prefix = '10'
        for S in range(14):
            for L in range(1, 15):
                if S+L in range(1, 15):
                    sliv = self.makeSliv(S, L)
                    if sliv is not None:
                        keyToSliv = '%s_%s_%s' % (prefix, S, L)
                        self.nrPuschToSliv[keyToSliv] = sliv
                        keyFromSliv = '%s_%s' % (prefix, sliv)
                        self.nrPuschFromSliv[keyFromSliv] = (S, L)
        
        #case4: prefix='11'
        prefix = '11'
        for S in range(13):
            for L in range(1, 13):
                if S+L in range(1, 13):
                    sliv = self.makeSliv(S, L)
                    if sliv is not None:
                        keyToSliv = '%s_%s_%s' % (prefix, S, L)
                        self.nrPuschToSliv[keyToSliv] = sliv
                        keyFromSliv = '%s_%s' % (prefix, sliv)
                        self.nrPuschFromSliv[keyFromSliv] = (S, L)
    
    def toSliv(self, S, L, sch='pdsch', type='Type A', cp='normal'):
        if type == 'Type A':
            if cp == 'normal':
                prefix = '00'
            elif cp == 'extended':
                prefix = '01'
            else:
                return None
        elif type == 'Type B':
            if cp == 'normal':
                prefix = '10'
            elif cp == 'extended':
                prefix = '11'
            else:
                return None
        else:
            return None
                
        key = '%s_%s_%s' % (prefix, S, L)
        if sch == 'pdsch':
            if not key in self.nrPdschToSliv.keys():
                return None
            else:
                sliv = self.nrPdschToSliv[key]
        elif sch == 'pusch':
            if not key in self.nrPuschToSliv.keys():
                return None
            else:
                sliv = self.nrPuschToSliv[key]
        else:
            return None
        
        return sliv
    
    def fromSliv(self, sliv, sch='pdsch', type='Type A', cp='normal'):
        if type == 'Type A':
            if cp == 'normal':
                prefix = '00'
            elif cp == 'extended':
                prefix = '01'
            else:
                return (None, None)
        elif type == 'Type B':
            if cp == 'normal':
                prefix = '10'
            elif cp == 'extended':
                prefix = '11'
            else:
                return (None, None)
        else:
            return (None, None)
                
        key = '%s_%s' % (prefix, sliv)
        if sch == 'pdsch':
            if not key in self.nrPdschFromSliv.keys():
                return (None, None)
            else:
                S, L = self.nrPdschFromSliv[key]
        elif sch == 'pusch':
            if not key in self.nrPuschFromSliv.keys():
                return (None, None)
            else:
                S, L = self.nrPuschFromSliv[key]
        else:
            return (None, None)
        
        return (S, L) 
