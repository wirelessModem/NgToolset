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

        #-->(1) Resource Grid Config Widget
        resGridCfgWidget = QWidget()
        resGridCfgLayout = QVBoxLayout()

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

        self.nrSsbKssbLabel = QLabel('k_SSB:')
        self.nrSsbKssbEdit = QLineEdit()
        self.nrSsbKssbEdit.setPlaceholderText('FR1: 0~23, FR2: 0~11')

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

        #connect signals to slots
        self.nrCarrierBwComb.currentIndexChanged[int].connect(self.onCarrierBwCombCurrentIndexChanged)
        self.nrCarrierScsComb.currentIndexChanged[int].connect(self.onCarrierScsCombCurrentIndexChanged)
        self.nrCarrierBandComb.currentIndexChanged[int].connect(self.onCarrierBandCombCurrentIndexChanged)
        self.nrSsbScsComb.currentIndexChanged[int].connect(self.onSsbScsCombCurrentIndexChanged)
        self.nrCarrierBandComb.setCurrentText('n77')

        gridLayoutResGridCfg = QGridLayout()
        gridLayoutResGridCfg.addWidget(self.nrCarrierBandLabel, 0, 0)
        gridLayoutResGridCfg.addWidget(self.nrCarrierBandComb, 0, 1)
        gridLayoutResGridCfg.addWidget(self.nrCarrierBandInfoLabel, 1, 0, 1, 2)
        gridLayoutResGridCfg.addWidget(carrierGridGrpBox, 2, 0, 1, 2)
        gridLayoutResGridCfg.addWidget(ssbGridGrpBox, 3, 0, 1, 2)

        resGridCfgLayout.addLayout(gridLayoutResGridCfg)
        resGridCfgLayout.addStretch()
        resGridCfgWidget.setLayout(resGridCfgLayout)
        
        #-->(2) SSB Config Widget
        ssbCfgWidget = QWidget()
        ssbCfgLayout = QVBoxLayout()
        
        #---->(2.1) SSB configurations
        self.nrSsbInOneGrpLabel = QLabel('inOneGroup:')
        self.nrSsbInOneGrpEdit = QLineEdit()
        self.nrSsbInOneGrpEdit.setPlaceholderText('11111111')
        
        self.nrSsbGrpPresenceLabel = QLabel('groupPresence:')
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
        
        self.nrSsbPciLabel = QLabel('PCI:')
        self.nrSsbPciEdit = QLineEdit()
        self.nrSsbPciEdit.setPlaceholderText('0~1007')
        
        #---->(2.2) MIB configurations
        self.nrMibSfnLabel = QLabel('SFN:')
        self.nrMibSfnEdit = QLineEdit()
        self.nrMibSfnEdit.setPlaceholderText('0~1023')
        
        self.nrMibDmRsTypeAPosLabel = QLabel('dmrs-TypeA-Position:')
        self.nrMibDmRsTypeAPosComb = QComboBox()
        self.nrMibDmRsTypeAPosComb.addItems(['pos2', 'pos3'])
        self.nrMibDmRsTypeAPosComb.setCurrentIndex(0)
        
        self.nrMibScsCommonLabel = QLabel('subCarrierSpacingCommon:')
        self.nrMibScsCommonComb = QComboBox()
        self.nrMibScsCommonComb.addItems(['15KHz', '30KHz', '60KHz', '120KHz'])
        self.nrMibScsCommonComb.setEnabled(False)
        
        self.nrMibRmsiCoreset0Label = QLabel('coresetZero(PDCCH-ConfigSIB1):')
        self.nrMibRmsiCoreset0Edit = QLineEdit()
        self.nrMibRmsiCoreset0Edit.setPlaceholderText('0~15')
        
        self.nrMibRmsiCss0Label = QLabel('searchSpaceZero(PDCCH-ConfigSIB1):')
        self.nrMibRmsiCss0Edit = QLineEdit()
        self.nrMibRmsiCss0Edit.setPlaceholderText('0~15')
        
        mibGrpBox = QGroupBox()
        mibGrpBox.setTitle('MIB')
        mibGrpBoxLayout = QGridLayout()
        mibGrpBoxLayout.addWidget(self.nrMibSfnLabel, 0, 0)
        mibGrpBoxLayout.addWidget(self.nrMibSfnEdit, 0, 1)
        mibGrpBoxLayout.addWidget(self.nrMibDmRsTypeAPosLabel, 1, 0)
        mibGrpBoxLayout.addWidget(self.nrMibDmRsTypeAPosComb, 1, 1)
        mibGrpBoxLayout.addWidget(self.nrMibScsCommonLabel, 2, 0)
        mibGrpBoxLayout.addWidget(self.nrMibScsCommonComb, 2, 1)
        mibGrpBoxLayout.addWidget(self.nrMibRmsiCoreset0Label, 3, 0)
        mibGrpBoxLayout.addWidget(self.nrMibRmsiCoreset0Edit, 3, 1)
        mibGrpBoxLayout.addWidget(self.nrMibRmsiCss0Label, 4, 0)
        mibGrpBoxLayout.addWidget(self.nrMibRmsiCss0Edit, 4, 1)
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
        
        self.nrTddCfgPat1NumDlSlotsLabel = QLabel('nrofDownlinkSlots:')
        self.nrTddCfgPat1NumDlSlotsEdit = QLineEdit()
        
        self.nrTddCfgPat1NumDlSymbsLabel = QLabel('nrofDownlinkSymbols:')
        self.nrTddCfgPat1NumDlSymbsEdit = QLineEdit()
        
        self.nrTddCfgPat1NumUlSymbsLabel = QLabel('nrofUplinkSymbols:')
        self.nrTddCfgPat1NumUlSymbsEdit = QLineEdit()
        
        self.nrTddCfgPat1NumUlSlotsLabel = QLabel('nrofUplinkSlots:')
        self.nrTddCfgPat1NumUlSlotsEdit = QLineEdit()
        
        self.nrTddCfgPat2PeriodLabel = QLabel('dl-UL-TransmissionPeriodicity:')
        self.nrTddCfgPat2PeriodComb = QComboBox()
        self.nrTddCfgPat2PeriodComb.addItems(['not used', '0.5ms', '0.625ms', '1ms', '1.25ms', '2ms', '2.5ms', '3ms', '4ms', '5ms', '10ms'])
        self.nrTddCfgPat2PeriodComb.setCurrentIndex(0)
        
        self.nrTddCfgPat2NumDlSlotsLabel = QLabel('nrofDownlinkSlots:')
        self.nrTddCfgPat2NumDlSlotsEdit = QLineEdit()
        
        self.nrTddCfgPat2NumDlSymbsLabel = QLabel('nrofDownlinkSymbols:')
        self.nrTddCfgPat2NumDlSymbsEdit = QLineEdit()
        
        self.nrTddCfgPat2NumUlSymbsLabel = QLabel('nrofUplinkSymbols:')
        self.nrTddCfgPat2NumUlSymbsEdit = QLineEdit()
        
        self.nrTddCfgPat2NumUlSlotsLabel = QLabel('nrofUplinkSlots:')
        self.nrTddCfgPat2NumUlSlotsEdit = QLineEdit()
        
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
        
        #-->(3) Coreset/SearchSpace Config Widget
        pdcchCfgWidget = QWidget()
        pdcchCfgLayout = QVBoxLayout()
        
        #---->(3.1) CSS0 configurations
        
        
        

        #-->Tab Widgets
        tabWidget = QTabWidget()
        tabWidget.addTab(resGridCfgWidget, 'Resource Grids')
        tabWidget.addTab(ssbCfgWidget, 'SSB Settings')

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
            ('n1', ('1920 MHz-1980 MHz', '2110 MHz-2170 MHz', 'FDD')),
            ('n2', ('1850 MHz-1910 MHz', '1930 MHz-1990 MHz', 'FDD')),
            ('n3', ('1710 MHz-1785 MHz', '1805 MHz-1880 MHz', 'FDD')),
            ('n5', ('824 MHz-849 MHz', '869 MHz-894 MHz', 'FDD')),
            ('n7', ('2500 MHz-2570 MHz', '2620 MHz-2690 MHz', 'FDD')),
            ('n8', ('880 MHz-915 MHz', '925 MHz-960 MHz', 'FDD')),
            ('n12', ('699 MHz-716 MHz', '729 MHz-746 MHz', 'FDD')),
            ('n20', ('832 MHz-862 MHz', '791 MHz-821 MHz', 'FDD')),
            ('n25', ('1850 MHz-1915 MHz', '1930 MHz-1995 MHz', 'FDD')),
            ('n28', ('703 MHz-748 MHz', '758 MHz-803 MHz', 'FDD')),
            ('n34', ('2010 MHz-2025 MHz', '2010 MHz-2025 MHz', 'TDD')),
            ('n38', ('2570 MHz-2620 MHz', '2570 MHz-2620 MHz', 'TDD')),
            ('n39', ('1880 MHz-1920 MHz', '1880 MHz-1920 MHz', 'TDD')),
            ('n40', ('2300 MHz-2400 MHz', '2300 MHz-2400 MHz', 'TDD')),
            ('n41', ('2496 MHz-2690 MHz', '2496 MHz-2690 MHz', 'TDD')),
            ('n50', ('1432 MHz-1517 MHz', '1432 MHz-1517 MHz', 'TDD')),
            ('n51', ('1427 MHz-1432 MHz', '1427 MHz-1432 MHz', 'TDD')),
            ('n66', ('1710 MHz-1780 MHz', '2110 MHz-2200 MHz', 'FDD')),
            ('n70', ('1695 MHz-1710 MHz', '1995 MHz-2020 MHz', 'FDD')),
            ('n71', ('663 MHz-698 MHz', '617 MHz-652 MHz', 'FDD')),
            ('n74', ('1427 MHz-1470 MHz', '1475 MHz-1518 MHz', 'FDD')),
            ('n75', ('N/A', '1432 MHz-1517 MHz', 'SDL')),
            ('n76', ('N/A', '1427 MHz-1432 MHz', 'SDL')),
            ('n77', ('3300 MHz-4200 MHz', '3300 MHz-4200 MHz', 'TDD')),
            ('n78', ('3300 MHz-3800 MHz', '3300 MHz-3800 MHz', 'TDD')),
            ('n79', ('4400 MHz-5000 MHz', '4400 MHz-5000 MHz', 'TDD')),
            ('n80', ('1710 MHz-1785 MHz', 'N/A', 'SUL')),
            ('n81', ('880 MHz-915 MHz', 'N/A', 'SUL')),
            ('n82', ('832 MHz-862 MHz', 'N/A', 'SUL')),
            ('n83', ('703 MHz-748 MHz', 'N/A', 'SUL')),
            ('n84', ('1920 MHz-1980 MHz', 'N/A', 'SUL')),
            ('n86', ('1710 MHz-1780 MHz', 'N/A', 'SUL')),
            ('n257', ('26500 MHz-29500 MHz', '26500 MHz-29500 MHz', 'TDD')),
            ('n258', ('24250 MHz-27500 MHz', '24250 MHz-27500 MHz', 'TDD')),
            ('n260', ('37000 MHz-40000 MHz', '37000 MHz-40000 MHz', 'TDD')),
            ('n261', ('27500 MHz-28350 MHz', '27500 MHz-28350 MHz', 'TDD')),
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

    def updateKSsbAndNCrbSsb(self):
        #refer to 3GPP 38.211 vf30
        #7.4.3.1	Time-frequency structure of an SS/PBCH block
        '''
        For FR1, k_ssb and n_crb_ssb based on 15k
        For FR2, k_ssb based on carrier_scs, n_crb_ssb based on 60k

        FR1/FR2   carrier_scs   ssb_scs     k_ssb	n_crb_ssb
        -----------------------------------------------------------
        FR1	        15k         15k         0~11	minGuardBand
                    15k         30k         0~11	minGuardBand
                    30k         15k         0~23	2*minGuardBand
                    30k         30k         0~23	2*minGuardBand
        FR2         60k         120k        0~11	minGuardBand
                    60k         240k        0~11	max(minGuardBand,4*minGuardBand240k)
                    120k        120k        0~11	2*minGuardBand
                    120k        240k        0~11	max(2*minGuardBand,4*minGuardBand240k)
        -----------------------------------------------------------
        '''
        key = self.nrCarrierScsComb.currentText()[:-3] + '_' + self.nrSsbScsComb.currentText()[:-3]
        minGuardBand = int(self.nrMinGuardBandEdit.text())
        if key in ('15_15', '15_30', '60_120'):
            self.nrSsbKssbEdit.setPlaceholderText('0~11')
            self.nrSsbNCrbSsbEdit.setText(str(minGuardBand))
        elif key in ('30_15', '30_30'):
            self.nrSsbKssbEdit.setPlaceholderText('0~23')
            self.nrSsbNCrbSsbEdit.setText(str(2*minGuardBand))
        elif key == '60_240':
            self.nrSsbKssbEdit.setPlaceholderText('0~11')
            minGuardBand240k = int(self.nrSsbMinGuardBandScs240kEdit.text())
            self.nrSsbNCrbSsbEdit.setText(str(max(minGuardBand, 4*minGuardBand240k)))
        elif key == '120_120':
            self.nrSsbKssbEdit.setPlaceholderText('0~11')
            self.nrSsbNCrbSsbEdit.setText(str(2*minGuardBand))
        else:   #key == '120_240':
            self.nrSsbKssbEdit.setPlaceholderText('0~11')
            minGuardBand240k = int(self.nrSsbMinGuardBandScs240kEdit.text())
            self.nrSsbNCrbSsbEdit.setText(str(max(2*minGuardBand, 4*minGuardBand240k)))
    
    def onCarrierBandCombCurrentIndexChanged(self, index):
        #self.ngwin.logEdit.append('inside onCarrierBandCombCurrentIndexChanged, index=%d' % index)
        if index < 0:
            return

        #(1) update band info
        ulBand, dlBand, self.duplexMode = self.nrOpBands[self.nrCarrierBandComb.currentText()]
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

    def onCarrierScsCombCurrentIndexChanged(self, index):
        #self.ngwin.logEdit.append('inside onCarrierScsCombCurrentIndexChanged, index=%d' % index)
        if index < 0:
            return

        #(1) update transmission bandwidth
        key = self.nrCarrierBandComb.currentText() + '_' + self.nrCarrierScsComb.currentText()[:-3]
        if not key in self.nrBandScs2BwFr1 and not key in self.nrBandScs2BwFr2:
            return
        if self.freqRange == 'FR1':
            bwSubset = [self.nrBwSetFr1[i] for i in range(len(self.nrBwSetFr1)) if self.nrBandScs2BwFr1[key][i]]
        else:
            bwSubset = [self.nrBwSetFr2[i] for i in range(len(self.nrBwSetFr2)) if self.nrBandScs2BwFr2[key][i]]

        self.nrCarrierBwComb.clear()
        self.nrCarrierBwComb.addItems(bwSubset)
        self.nrCarrierBwComb.setCurrentIndex(0)

    def onCarrierBwCombCurrentIndexChanged(self, index):
        #self.ngwin.logEdit.append('inside onCarrierBwCombCurrentIndexChanged, index=%d' % index)
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
                
        #(4) update k_SSB and n_CRB_SSB
        self.updateKSsbAndNCrbSsb()

    def onSsbScsCombCurrentIndexChanged(self, index):
        #self.ngwin.logEdit.append('inside onSsbScsCombCurrentIndexChanged, index=%d' % index)
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
                                          ' subcarrier spacing is 240KHz!' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
                self.nrSsbMinGuardBandScs240kEdit.setText('NA')
                return
            else:
                self.nrSsbMinGuardBandScs240kEdit.setText(str(self.nrSsbMinGuardBandScs240k[self.nrCarrierBwComb.currentIndex()]))
        else:
            self.nrSsbMinGuardBandScs240kEdit.setText('NA')
        
        #(3) update k_SSB and n_CRB_SSB
        if self.nrMinGuardBandEdit.text():
            self.updateKSsbAndNCrbSsb()

    def onOkBtnClicked(self):
        #TODO
        self.accept()
