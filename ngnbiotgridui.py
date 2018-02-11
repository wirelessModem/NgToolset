#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngnbiotgridui.py
Description:
    UI for NB-IoT resource grid.
Change History:
    2018-1-30   v0.1    created.    github/zhenggao2
'''

import os
import math
from PyQt5.QtWidgets import QDialog, QTextEdit, QTabWidget, QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QWidget, QGroupBox, QMessageBox
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import ngmainwin
from ngltephy import LteResType
from ngltegrid import NgLteGrid
from ngb36utils import time2str36, freq2str36
from ngnbiotphy import NbiotPhy, NbiotResType, incSfn
from ngnbiotgrid import NgNbiotGrid

class NgNbiotGridUi(QDialog):
    def __init__(self, ngwin):
        super().__init__()
        self.ngwin = ngwin
        self.argsLte = dict()
        self.argsNbiot = dict()
        self.initResGridMapper()
        self.initUi()
    
    def initResGridMapper(self):
        self.dlMap = dict()
        self.dlMap[LteResType.LTE_RES_PDSCH.value] = ('PDSCH', QColor(0, 0, 0), QColor(255, 255, 255)) 
        self.dlMap[LteResType.LTE_RES_PDCCH.value] = ('PDCCH', QColor(0, 0, 0), QColor(0, 255, 255)) 
        self.dlMap[LteResType.LTE_RES_PHICH.value] = ('PHICH', QColor(0, 0, 0), QColor(255, 0, 255)) 
        self.dlMap[LteResType.LTE_RES_PCFICH.value] = ('PCFICH', QColor(0, 0, 255), QColor(255, 255, 255)) 
        self.dlMap[LteResType.LTE_RES_PBCH.value] = ('PBCH', QColor(0, 0, 0), QColor(128, 255, 255)) 
        self.dlMap[LteResType.LTE_RES_PSCH.value] = ('PSCH', QColor(0, 0, 0), QColor(0, 255, 0)) 
        self.dlMap[LteResType.LTE_RES_SSCH.value] = ('SSCH', QColor(0, 0, 0), QColor(255, 255, 0)) 
        self.dlMap[LteResType.LTE_RES_CRS.value] = ('CRS', QColor(0, 0, 0), QColor(255, 0, 0)) 
        self.dlMap[LteResType.LTE_RES_DTX.value] = ('DTX', QColor(255, 255, 255), QColor(0, 0, 0)) 
        self.dlMap[LteResType.LTE_RES_GP.value] = ('GP', QColor(255, 255, 255), QColor(0, 0, 0)) 
        self.dlMap[LteResType.LTE_RES_UL.value] = ('UL', QColor(255, 255, 255), QColor(0, 0, 0)) 
        self.dlMap[LteResType.LTE_RES_NB_INBAND.value] = ('NB DL', QColor(128, 128, 128), QColor(0, 0, 0)) 
        
        self.ulMap = dict()
        self.ulMap[LteResType.LTE_RES_GP.value] = ('GP', QColor(0, 0, 0), QColor(0, 255, 0))
        self.ulMap[LteResType.LTE_RES_DL.value] = ('DL', QColor(255, 255, 255), QColor(0, 0, 0))
        self.ulMap[LteResType.LTE_RES_PUSCH.value] = ('PUSCH', QColor(0, 0, 0), QColor(255, 255, 255))
        self.ulMap[LteResType.LTE_RES_PUCCH_AN.value] = ('AN', QColor(0, 0, 0), QColor(0, 255, 255))
        self.ulMap[LteResType.LTE_RES_PUCCH_MIXED.value] = ('MIXED', QColor(0, 0, 0), QColor(255, 0, 255))
        self.ulMap[LteResType.LTE_RES_PUCCH_CQI.value] = ('CQI', QColor(255, 255, 255), QColor(0, 0, 255))
        self.ulMap[LteResType.LTE_RES_PRACH.value] = ('PRACH', QColor(0, 0, 0), QColor(128, 255, 255))
        self.ulMap[LteResType.LTE_RES_DMRS.value] = ('DMRS', QColor(0, 0, 0), QColor(255, 0, 0))
        self.ulMap[LteResType.LTE_RES_SRS.value] = ('SRS', QColor(0, 0, 0), QColor(255, 255, 0))
        self.ulMap[LteResType.LTE_RES_NB_INBAND.value] = ('NB UL', QColor(128, 128, 128), QColor(0, 0, 0))
    
    def initUi(self):
        self.fsLabel = QLabel('Frame Structure:')
        self.fsCombo = QComboBox()
        self.fsCombo.addItem('Type 1(FDD)')
        self.fsCombo.addItem('Type 2(TDD)')
        self.fsCombo.currentIndexChanged[int].connect(self.onFsComboCurrentIndexChanged)
        self.fsCombo.setCurrentIndex(0)

        self.bwLabel = QLabel('System Bandwidth:')
        self.bwCombo = QComboBox()
        self.bwCombo.addItem('1.4MHz')
        self.bwCombo.addItem('3MHz')
        self.bwCombo.addItem('5MHz')
        self.bwCombo.addItem('10MHz')
        self.bwCombo.addItem('15MHz')
        self.bwCombo.addItem('20MHz')
        self.bwCombo.setCurrentIndex(2)

        self.cpLabel = QLabel('Cyclic Prefix:')
        self.cpCombo = QComboBox()
        self.cpCombo.addItem('Normal CP')
        self.cpCombo.addItem('Extended CP')
        self.cpCombo.currentIndexChanged[int].connect(self.onCpComboCurrentIndexChanged)
        self.cpCombo.setCurrentIndex(0)

        self.apLabel = QLabel('Downlink Antenna Port(s):')
        self.apCombo = QComboBox()
        self.apCombo.addItem('One Antenna Port')
        self.apCombo.addItem('Two Antenna Ports')
        self.apCombo.addItem('Four Antenna Ports')
        self.apCombo.setCurrentIndex(1)

        self.pciLabel = QLabel('Physical Cell Identity:')
        self.pciEdit = QLineEdit()
        self.pciEdit.setText('0')

        self.cfiLabel = QLabel('CFI(Normal Downlink Subframe):')
        self.cfiCombo = QComboBox()
        self.cfiCombo.addItem('1')
        self.cfiCombo.addItem('2')
        self.cfiCombo.addItem('3')
        self.cfiCombo.addItem('4')
        self.cfiCombo.setCurrentIndex(2)

        self.cfiSsfLabel = QLabel('CFI(Special Subframe, TDD):')
        self.cfiSsfCombo = QComboBox()
        self.cfiSsfCombo.addItem('1')
        self.cfiSsfCombo.addItem('2')
        self.cfiSsfCombo.setCurrentIndex(1)
        self.cfiSsfCombo.setEnabled(False) #TDD specific parameters is disabled by default!

        self.phichDurLabel = QLabel('PHICH Duration:')
        self.phichDurCombo = QComboBox()
        self.phichDurCombo.addItem('Normal')
        self.phichDurCombo.addItem('Extended')
        self.phichDurCombo.setCurrentIndex(0)

        self.phichResLabel = QLabel('PHICH Resource:')
        self.phichResCombo = QComboBox()
        self.phichResCombo.addItem('OneSixth')
        self.phichResCombo.addItem('Half')
        self.phichResCombo.addItem('One')
        self.phichResCombo.addItem('Two')
        self.phichResCombo.setCurrentIndex(0)

        self.saLabel = QLabel('Subframe Assignment(TDD):')
        self.saCombo = QComboBox()
        self.saCombo.addItem('SA0')
        self.saCombo.addItem('SA1')
        self.saCombo.addItem('SA2')
        self.saCombo.addItem('SA3')
        self.saCombo.addItem('SA4')
        self.saCombo.addItem('SA5')
        self.saCombo.addItem('SA6')
        self.saCombo.setCurrentIndex(2)
        self.saCombo.setEnabled(False) #TDD specific parameters is disabled by default!

        self.sspLabel = QLabel('Special Subframe Pattern(TDD):')
        self.sspCombo = QComboBox()
        self.sspCombo.addItem('SSP0')
        self.sspCombo.addItem('SSP1')
        self.sspCombo.addItem('SSP2')
        self.sspCombo.addItem('SSP3')
        self.sspCombo.addItem('SSP4')
        self.sspCombo.addItem('SSP5')
        self.sspCombo.addItem('SSP6')
        self.sspCombo.addItem('SSP7(Normal CP)')
        self.sspCombo.addItem('SSP8(Normal CP)')
        self.sspCombo.setCurrentIndex(7)
        self.sspCombo.setEnabled(False) #TDD specific parameters is disabled by default!

        self.dsPucchLabel = QLabel('Delta PUCCH Shift:')
        self.dsPucchCombo = QComboBox()
        self.dsPucchCombo.addItem('DS1')
        self.dsPucchCombo.addItem('DS2')
        self.dsPucchCombo.addItem('DS3')
        self.dsPucchCombo.setCurrentIndex(0)

        self.nCqiRbLabel = QLabel('nRB-CQI:')
        self.nCqiRbEdit = QLineEdit()
        self.nCqiRbEdit.setText('2')

        self.nCsAnLabel = QLabel('nCS-AN:')
        self.nCsAnEdit = QLineEdit()
        self.nCsAnEdit.setText('0')

        self.n1PucchAnLabel = QLabel('n1PUCCH-AN：')
        self.n1PucchAnEdit = QLineEdit()
        self.n1PucchAnEdit.setText('36')

        self.tddAckModeLabel = QLabel('ACK/NACK Feedback Mode(TDD):')
        self.tddAckModeCombo = QComboBox()
        self.tddAckModeCombo.addItem('ACK/NACK Bundling')
        self.tddAckModeCombo.addItem('ACK/NACK Multiplexing')
        self.tddAckModeCombo.setCurrentIndex(0)
        self.tddAckModeCombo.setEnabled(False) #TDD specific parameters is disabled by default!

        self.sfnLabel = QLabel('System Frame Number(SFN):')
        self.sfnEdit = QLineEdit()
        self.sfnEdit.setText('0')

        self.prachConfIndLabel = QLabel('PRACH Configuration Index:')
        self.prachConfIndEdit = QLineEdit()
        self.prachConfIndEdit.setText('3')

        self.prachFreqOffLabel = QLabel('PRACH Frequency Offset:')
        self.prachFreqOffEdit = QLineEdit()
        self.prachFreqOffEdit.setText('0')

        self.srsSfConfLabel = QLabel('srs-SubframeConfig:')
        self.srsSfConfEdit = QLineEdit()
        self.srsSfConfEdit.setText('0')

        self.okBtn = QPushButton('OK')
        self.cancelBtn = QPushButton('Cancel')
        self.okBtn.clicked.connect(self.onOkBtnClicked)
        self.cancelBtn.clicked.connect(self.reject)

        layout1 = QGridLayout()
        layout1.addWidget(self.fsLabel, 0, 0)
        layout1.addWidget(self.fsCombo, 0, 1)
        layout1.addWidget(self.bwLabel, 1, 0)
        layout1.addWidget(self.bwCombo, 1, 1)
        layout1.addWidget(self.cpLabel, 2, 0)
        layout1.addWidget(self.cpCombo, 2, 1)
        layout1.addWidget(self.apLabel, 3, 0)
        layout1.addWidget(self.apCombo, 3, 1)
        layout1.addWidget(self.pciLabel, 4, 0)
        layout1.addWidget(self.pciEdit, 4, 1)
        layout1.addWidget(self.cfiLabel, 5, 0)
        layout1.addWidget(self.cfiCombo, 5, 1)
        layout1.addWidget(self.cfiSsfLabel, 6, 0)
        layout1.addWidget(self.cfiSsfCombo, 6, 1)
        layout1.addWidget(self.phichDurLabel, 7, 0)
        layout1.addWidget(self.phichDurCombo, 7, 1)
        layout1.addWidget(self.phichResLabel, 8, 0)
        layout1.addWidget(self.phichResCombo, 8, 1)
        layout1.addWidget(self.saLabel, 9, 0)
        layout1.addWidget(self.saCombo, 9, 1)
        layout1.addWidget(self.sspLabel, 10, 0)
        layout1.addWidget(self.sspCombo, 10, 1)
        layout1.addWidget(self.dsPucchLabel, 11, 0)
        layout1.addWidget(self.dsPucchCombo, 11, 1)
        layout1.addWidget(self.nCqiRbLabel, 12, 0)
        layout1.addWidget(self.nCqiRbEdit, 12, 1)
        layout1.addWidget(self.nCsAnLabel, 13, 0)
        layout1.addWidget(self.nCsAnEdit, 13, 1)
        layout1.addWidget(self.n1PucchAnLabel, 14, 0)
        layout1.addWidget(self.n1PucchAnEdit, 14, 1)
        layout1.addWidget(self.tddAckModeLabel, 15, 0)
        layout1.addWidget(self.tddAckModeCombo, 15, 1)
        layout1.addWidget(self.sfnLabel, 16, 0)
        layout1.addWidget(self.sfnEdit, 16, 1)
        layout1.addWidget(self.prachConfIndLabel, 17, 0)
        layout1.addWidget(self.prachConfIndEdit, 17, 1)
        layout1.addWidget(self.prachFreqOffLabel, 18, 0)
        layout1.addWidget(self.prachFreqOffEdit, 18, 1)
        layout1.addWidget(self.srsSfConfLabel, 19, 0)
        layout1.addWidget(self.srsSfConfEdit, 19, 1)

        hostLteConfig = QWidget()
        layoutHostLte = QVBoxLayout()
        layoutHostLte.addLayout(layout1)
        layoutHostLte.addStretch()
        hostLteConfig.setLayout(layoutHostLte)

        self.nbOpModelabel = QLabel('NB Operation Mode:')
        self.nbOpModeCombo = QComboBox()
        self.nbOpModeCombo.addItem('Inband-SamePCI')
        self.nbOpModeCombo.addItem('Inband-DifferentPCI')
        self.nbOpModeCombo.addItem('Guardband')
        self.nbOpModeCombo.addItem('Standalone')
        self.nbOpModeCombo.setCurrentIndex(0)

        self.nbApLabel = QLabel('NB Downlink Antenna Port(s):')
        self.nbApCombo = QComboBox()
        self.nbApCombo.addItem('One Antenna Port')
        self.nbApCombo.addItem('Two Antenna Ports')
        self.nbApCombo.setCurrentIndex(1)

        self.nbPciLabel = QLabel('NB Physical Cell Identity:')
        self.nbPciEdit = QLineEdit()
        self.nbPciEdit.setText('0')

        self.nbInBandPrbIdxUlLabel = QLabel('NB Inband PRB Index UL:')
        self.nbInBandPrbIdxUlEdit = QLineEdit()
        self.nbInBandPrbIdxUlEdit.setText('0')

        self.nbInBandPrbIdxDlLabel = QLabel('NB Inband PRB Index DL:')
        self.nbInBandPrbIdxDlCombo = QComboBox()
        self.nbInBandPrbIdxDlCombo.addItem('2')
        self.nbInBandPrbIdxDlCombo.addItem('7')
        self.nbInBandPrbIdxDlCombo.addItem('17')
        self.nbInBandPrbIdxDlCombo.addItem('22')
        self.nbInBandPrbIdxDlCombo.setCurrentIndex(0)

        #auto fill nbInBandPrbIdxDlCombo when bwCombo is changed!
        self.bwCombo.currentIndexChanged[int].connect(self.onBwComboCurrentIndexChanged)

        self.nbHsfnLabel = QLabel('NB Hyper SFN:')
        self.nbHsfnEdit = QLineEdit()
        self.nbHsfnEdit.setText('0')

        self.nbSfnLabel = QLabel('NB System Frame Number:')
        self.nbSfnEdit = QLineEdit()
        self.nbSfnEdit.setText('0')

        layout3 = QGridLayout()
        layout3.addWidget(self.nbOpModelabel, 0, 0)
        layout3.addWidget(self.nbOpModeCombo, 0, 1)
        layout3.addWidget(self.nbApLabel, 1, 0)
        layout3.addWidget(self.nbApCombo, 1, 1)
        layout3.addWidget(self.nbPciLabel, 2, 0)
        layout3.addWidget(self.nbPciEdit, 2, 1)
        layout3.addWidget(self.nbInBandPrbIdxUlLabel, 3, 0)
        layout3.addWidget(self.nbInBandPrbIdxUlEdit, 3, 1)
        layout3.addWidget(self.nbInBandPrbIdxDlLabel, 4, 0)
        layout3.addWidget(self.nbInBandPrbIdxDlCombo, 4, 1)
        layout3.addWidget(self.nbHsfnLabel, 5, 0)
        layout3.addWidget(self.nbHsfnEdit, 5, 1)
        layout3.addWidget(self.nbSfnLabel, 6, 0)
        layout3.addWidget(self.nbSfnEdit, 6, 1)
        
        nbIotCommonConfig = QWidget()
        layoutNbCommon = QVBoxLayout()
        layoutNbCommon.addLayout(layout3)
        layoutNbCommon.addStretch()
        nbIotCommonConfig.setLayout(layoutNbCommon)

        self.nbUlScSpacingLabel = QLabel('NB UL Subcarrier Spacing:')
        self.nbUlScSpacingCombo = QComboBox()
        self.nbUlScSpacingCombo.addItem('3.75KHz')
        self.nbUlScSpacingCombo.addItem('15KHz')
        self.nbUlScSpacingCombo.setCurrentIndex(1)

        self.nbNpuschAllSymLabel = QLabel('npusch-AllSymbols-r13:')
        self.nbNpuschAllSymCombo = QComboBox()
        self.nbNpuschAllSymCombo.addItem('True')
        self.nbNpuschAllSymCombo.addItem('False')
        self.nbNpuschAllSymCombo.setCurrentIndex(0)

        self.nbDciN0ScIndLabel = QLabel('Subcarrier Indication(DCI N0):')
        self.nbDciN0ScIndEdit = QLineEdit()
        self.nbDciN0ScIndEdit.setText('0')

        self.nbDciN0ScIndHintLabel = QLabel('<font color=\"blue\">Hint: Value range of Isc is: 0~47 for 3.75KHz, 0~18 for 15KHz!</font>')

        self.nbDciN0RuIndLabel = QLabel('Resource Assignment(DCI N0):')
        self.nbDciN0RuIndCombo = QComboBox()
        for i in range(8):
            self.nbDciN0RuIndCombo.addItem('%d' % i)
        self.nbDciN0RuIndCombo.setCurrentIndex(0)

        self.nbDciN0RepIndLabel = QLabel('Repetition Number(DCI N0):')
        self.nbDciN0RepIndCombo = QComboBox()
        for i in range(8):
            self.nbDciN0RepIndCombo.addItem('%d' % i)
        self.nbDciN0RepIndCombo.setCurrentIndex(0)

        self.nbDciN0DelayIndLabel = QLabel('Scheduling Delay(DCI N0):')
        self.nbDciN0DelayIndCombo = QComboBox()
        for i in range(4):
            self.nbDciN0DelayIndCombo.addItem('%d' % i)
        self.nbDciN0DelayIndCombo.setCurrentIndex(0)

        self.nbNumAnRepLabel = QLabel('ACK-NACK-NumRepetitions-NB-r13:')
        self.nbNumAnRepCombo = QComboBox()
        self.nbNumAnRepCombo.addItem('r1')
        self.nbNumAnRepCombo.addItem('r2')
        self.nbNumAnRepCombo.addItem('r4')
        self.nbNumAnRepCombo.addItem('r8')
        self.nbNumAnRepCombo.addItem('r16')
        self.nbNumAnRepCombo.addItem('r32')
        self.nbNumAnRepCombo.addItem('r64')
        self.nbNumAnRepCombo.addItem('r128')
        self.nbNumAnRepCombo.setCurrentIndex(0)

        self.nbDciN1AnIndLabel = QLabel('HARQ-ACK Resource(DCI N1):')
        self.nbDciN1AnIndCombo = QComboBox()
        for i in range(16):
            self.nbDciN1AnIndCombo.addItem('%d' % i)
        self.nbDciN1AnIndCombo.setCurrentIndex(0)

        self.nbNprachPeriodLabel = QLabel('nprach-Periodicity-r13:')
        self.nbNprachPeriodCombo = QComboBox()
        self.nbNprachPeriodCombo.addItem('ms40')
        self.nbNprachPeriodCombo.addItem('ms80')
        self.nbNprachPeriodCombo.addItem('ms160')
        self.nbNprachPeriodCombo.addItem('ms240')
        self.nbNprachPeriodCombo.addItem('ms320')
        self.nbNprachPeriodCombo.addItem('ms640')
        self.nbNprachPeriodCombo.addItem('ms1280')
        self.nbNprachPeriodCombo.addItem('ms2560')
        self.nbNprachPeriodCombo.setCurrentIndex(0)

        self.nbNprachStartTimeLabel = QLabel('nprach-StartTime-r13:')
        self.nbNprachStartTimeCombo = QComboBox()
        self.nbNprachStartTimeCombo.addItem('ms8')
        self.nbNprachStartTimeCombo.addItem('ms16')
        self.nbNprachStartTimeCombo.addItem('ms32')
        self.nbNprachStartTimeCombo.addItem('ms64')
        self.nbNprachStartTimeCombo.addItem('ms128')
        self.nbNprachStartTimeCombo.addItem('ms256')
        self.nbNprachStartTimeCombo.addItem('ms512')
        self.nbNprachStartTimeCombo.addItem('ms1024')
        self.nbNprachStartTimeCombo.setCurrentIndex(0)

        self.nbNprachRepLabel = QLabel('numRepetitionsPerPreambleAttempt-r13:')
        self.nbNprachRepCombo = QComboBox()
        self.nbNprachRepCombo.addItem('n1')
        self.nbNprachRepCombo.addItem('n2')
        self.nbNprachRepCombo.addItem('n4')
        self.nbNprachRepCombo.addItem('n8')
        self.nbNprachRepCombo.addItem('n16')
        self.nbNprachRepCombo.addItem('n32')
        self.nbNprachRepCombo.addItem('n64')
        self.nbNprachRepCombo.addItem('n128')
        self.nbNprachRepCombo.setCurrentIndex(0)

        self.nbNprachNumScLabel = QLabel('nprach-NumSubcarriers-r13:')
        self.nbNprachNumScCombo = QComboBox()
        self.nbNprachNumScCombo.addItem('n12')
        self.nbNprachNumScCombo.addItem('n24')
        self.nbNprachNumScCombo.addItem('n36')
        self.nbNprachNumScCombo.addItem('n48')
        self.nbNprachNumScCombo.setCurrentIndex(0)

        self.nbNprachScOffLabel = QLabel('nprach-SubcarrierOffset-r13:')
        self.nbNprachScOffCombo = QComboBox()
        self.nbNprachScOffCombo.addItem('n0')
        self.nbNprachScOffCombo.addItem('n12')
        self.nbNprachScOffCombo.addItem('n24')
        self.nbNprachScOffCombo.addItem('n36')
        self.nbNprachScOffCombo.addItem('n2')
        self.nbNprachScOffCombo.addItem('n18')
        self.nbNprachScOffCombo.addItem('n34')
        self.nbNprachScOffCombo.setCurrentIndex(0)

        layout4 = QGridLayout()
        layout4.addWidget(self.nbUlScSpacingLabel, 0, 0)
        layout4.addWidget(self.nbUlScSpacingCombo, 0, 1)
        layout4.addWidget(self.nbNpuschAllSymLabel, 1, 0)
        layout4.addWidget(self.nbNpuschAllSymCombo, 1, 1)

        npuschF1CfgGrpBox = QGroupBox()
        npuschF1CfgGrpBox.setTitle('NPUSCH Format 1')
        layout5 = QGridLayout()
        layout5.addWidget(self.nbDciN0ScIndLabel, 1, 0)
        layout5.addWidget(self.nbDciN0ScIndEdit, 1, 1)
        layout5.addWidget(self.nbDciN0ScIndHintLabel, 2, 0, 1, 2)
        layout5.addWidget(self.nbDciN0RuIndLabel, 3, 0)
        layout5.addWidget(self.nbDciN0RuIndCombo, 3, 1)
        layout5.addWidget(self.nbDciN0RepIndLabel, 4, 0)
        layout5.addWidget(self.nbDciN0RepIndCombo, 4, 1)
        layout5.addWidget(self.nbDciN0DelayIndLabel, 5, 0)
        layout5.addWidget(self.nbDciN0DelayIndCombo, 5, 1)
        npuschF1CfgGrpBox.setLayout(layout5)

        npuschF2CfgGrpBox = QGroupBox()
        npuschF2CfgGrpBox.setTitle('NPUSCH Format 2')
        layout6 = QGridLayout()
        layout6.addWidget(self.nbNumAnRepLabel, 1, 0)
        layout6.addWidget(self.nbNumAnRepCombo, 1, 1)
        layout6.addWidget(self.nbDciN1AnIndLabel, 2, 0)
        layout6.addWidget(self.nbDciN1AnIndCombo, 2, 1)
        npuschF2CfgGrpBox.setLayout(layout6)

        nprachCfgGrpBox = QGroupBox()
        nprachCfgGrpBox.setTitle('NPRACH')
        layout7 = QGridLayout()
        layout7.addWidget(self.nbNprachPeriodLabel, 0, 0)
        layout7.addWidget(self.nbNprachPeriodCombo, 0, 1)
        layout7.addWidget(self.nbNprachStartTimeLabel, 1, 0)
        layout7.addWidget(self.nbNprachStartTimeCombo, 1, 1)
        layout7.addWidget(self.nbNprachRepLabel, 2, 0)
        layout7.addWidget(self.nbNprachRepCombo, 2, 1)
        layout7.addWidget(self.nbNprachNumScLabel, 3, 0)
        layout7.addWidget(self.nbNprachNumScCombo, 3, 1)
        layout7.addWidget(self.nbNprachScOffLabel, 4, 0)
        layout7.addWidget(self.nbNprachScOffCombo, 4, 1)
        nprachCfgGrpBox.setLayout(layout7)

        layout4.addWidget(npuschF1CfgGrpBox, 2, 0, 1, 2)
        layout4.addWidget(npuschF2CfgGrpBox, 3, 0, 1, 2)
        layout4.addWidget(nprachCfgGrpBox, 4, 0, 1, 2)
        nbIotUlConfig = QWidget()
        layoutNbUl = QVBoxLayout()
        layoutNbUl.addLayout(layout4)
        layoutNbUl.addStretch()
        nbIotUlConfig.setLayout(layoutNbUl)    

        self.nbDlBitmapLabel = QLabel('DL-Bitmap-NB-r13:')
        self.nbDlBitmapEdit = QLineEdit()
        self.nbDlBitmapEdit.setText('11111,11111')

        self.nbDciN1SfAssignLabel = QLabel('Resource Assignment(DCI N1):')
        self.nbDciN1SfAssignCombo = QComboBox()
        for i in range(8):
            self.nbDciN1SfAssignCombo.addItem('%d' % i)
        self.nbDciN1SfAssignCombo.setCurrentIndex(0)

        self.nbDciN1RepLabel = QLabel('Repetition Number(DCI N1):')
        self.nbDciN1RepCombo = QComboBox()
        for i in range(16):
            self.nbDciN1RepCombo.addItem('%d' % i)
        self.nbDciN1RepCombo.setCurrentIndex(0)

        self.nbDciN1DelayLabel = QLabel('Scheduling Delay(DCI N1):')
        self.nbDciN1DelayCombo = QComboBox()
        for i in range(8):
            self.nbDciN1DelayCombo.addItem('%d' % i)
        self.nbDciN1DelayCombo.setCurrentIndex(0)

        self.nbDlGapThreshLabel = QLabel('dl-GapThreshold-r13:')
        self.nbDlGapThreshCombo = QComboBox()
        self.nbDlGapThreshCombo.addItem('n32')
        self.nbDlGapThreshCombo.addItem('n64')
        self.nbDlGapThreshCombo.addItem('n128')
        self.nbDlGapThreshCombo.addItem('n256')
        self.nbDlGapThreshCombo.setCurrentIndex(0)

        self.nbDlGapPeriodLabel = QLabel('dl-GapPeriodicity-r13:')
        self.nbDlGapPeriodCombo = QComboBox()
        self.nbDlGapPeriodCombo.addItem('sf64')
        self.nbDlGapPeriodCombo.addItem('sf128')
        self.nbDlGapPeriodCombo.addItem('sf256')
        self.nbDlGapPeriodCombo.addItem('sf512')
        self.nbDlGapPeriodCombo.setCurrentIndex(0)

        self.nbDlGapDurCoeffLabel = QLabel('dl-GapDurationCoeff-r13:')
        self.nbDlGapDurCoeffCombo = QComboBox()
        self.nbDlGapDurCoeffCombo.addItem('oneEighth')
        self.nbDlGapDurCoeffCombo.addItem('oneFourth')
        self.nbDlGapDurCoeffCombo.addItem('threeEighth')
        self.nbDlGapDurCoeffCombo.addItem('oneHalf')
        self.nbDlGapDurCoeffCombo.setCurrentIndex(0)

        self.nbSchedInfoSib1Label = QLabel('schedulingInfoSIB1-r13:')
        self.nbSchedInfoSib1Combo = QComboBox()
        for i in range(12):
            self.nbSchedInfoSib1Combo.addItem('%d' % i)
        self.nbSchedInfoSib1Combo.setCurrentIndex(0)

        self.nbSiWinLengthLabel = QLabel('si-WindowLength-r13:')
        self.nbSiWinLengthCombo = QComboBox()
        self.nbSiWinLengthCombo.addItem('ms160')
        self.nbSiWinLengthCombo.addItem('ms320')
        self.nbSiWinLengthCombo.addItem('ms480')
        self.nbSiWinLengthCombo.addItem('ms640')
        self.nbSiWinLengthCombo.addItem('ms960')
        self.nbSiWinLengthCombo.addItem('ms1280')
        self.nbSiWinLengthCombo.addItem('ms1600')
        self.nbSiWinLengthCombo.setCurrentIndex(0)

        self.nbSiFrameOffLabel = QLabel('si-RadioFrameOffset-r13:')
        self.nbSiFrameOffCombo = QComboBox()
        for i in range(16):
            self.nbSiFrameOffCombo.addItem('%d' % i)
        self.nbSiFrameOffCombo.setCurrentIndex(0)

        self.nbSib2PeriodLabel = QLabel('si-Periodicity-r13(SIB2-NB):')
        self.nbSib2PeriodCombo = QComboBox()
        self.nbSib2PeriodCombo.addItem('rf64')
        self.nbSib2PeriodCombo.addItem('rf128')
        self.nbSib2PeriodCombo.addItem('rf256')
        self.nbSib2PeriodCombo.addItem('rf512')
        self.nbSib2PeriodCombo.addItem('rf1024')
        self.nbSib2PeriodCombo.addItem('rf2048')
        self.nbSib2PeriodCombo.addItem('rf4096')
        self.nbSib2PeriodCombo.setCurrentIndex(0)

        self.nbSib2RepPatLabel = QLabel('si-RepetitionPattern-r13(SIB2-NB):')
        self.nbSib2RepPatCombo = QComboBox()
        self.nbSib2RepPatCombo.addItem('every2ndRF')
        self.nbSib2RepPatCombo.addItem('every4thRF')
        self.nbSib2RepPatCombo.addItem('every8thRF')
        self.nbSib2RepPatCombo.addItem('every16thRF')
        self.nbSib2RepPatCombo.setCurrentIndex(0)

        self.nbSib2TbsLabel = QLabel('si-TB-r13(SIB2-NB):')
        self.nbSib2TbsCombo = QComboBox()
        self.nbSib2TbsCombo.addItem('b56')
        self.nbSib2TbsCombo.addItem('b120')
        self.nbSib2TbsCombo.addItem('b208')
        self.nbSib2TbsCombo.addItem('b256')
        self.nbSib2TbsCombo.addItem('b328')
        self.nbSib2TbsCombo.addItem('b440')
        self.nbSib2TbsCombo.addItem('b552')
        self.nbSib2TbsCombo.addItem('b680')
        self.nbSib2TbsCombo.setCurrentIndex(0)

        self.nbSib3PeriodLabel = QLabel('si-Periodicity-r13(SIB3-NB):')
        self.nbSib3PeriodCombo = QComboBox()
        self.nbSib3PeriodCombo.addItem('rf64')
        self.nbSib3PeriodCombo.addItem('rf128')
        self.nbSib3PeriodCombo.addItem('rf256')
        self.nbSib3PeriodCombo.addItem('rf512')
        self.nbSib3PeriodCombo.addItem('rf1024')
        self.nbSib3PeriodCombo.addItem('rf2048')
        self.nbSib3PeriodCombo.addItem('rf4096')
        self.nbSib3PeriodCombo.setCurrentIndex(0)

        self.nbSib3RepPatLabel = QLabel('si-RepetitionPattern-r13(SIB3-NB):')
        self.nbSib3RepPatCombo = QComboBox()
        self.nbSib3RepPatCombo.addItem('every2ndRF')
        self.nbSib3RepPatCombo.addItem('every4thRF')
        self.nbSib3RepPatCombo.addItem('every8thRF')
        self.nbSib3RepPatCombo.addItem('every16thRF')
        self.nbSib3RepPatCombo.setCurrentIndex(0)

        self.nbSib3TbsLabel = QLabel('si-TB-r13(SIB3-NB):')
        self.nbSib3TbsCombo = QComboBox()
        self.nbSib3TbsCombo.addItem('b56')
        self.nbSib3TbsCombo.addItem('b120')
        self.nbSib3TbsCombo.addItem('b208')
        self.nbSib3TbsCombo.addItem('b256')
        self.nbSib3TbsCombo.addItem('b328')
        self.nbSib3TbsCombo.addItem('b440')
        self.nbSib3TbsCombo.addItem('b552')
        self.nbSib3TbsCombo.addItem('b680')
        self.nbSib3TbsCombo.setCurrentIndex(0)

        self.nbDciN0N1SfRepLabel = QLabel('DCI Subframe Repetition Number(DCI N0/N1):')
        self.nbDciN0N1SfRepCombo = QComboBox()
        self.nbDciN0N1SfRepCombo.addItem('0')
        self.nbDciN0N1SfRepCombo.addItem('1')
        self.nbDciN0N1SfRepCombo.addItem('2')
        self.nbDciN0N1SfRepCombo.addItem('3')
        self.nbDciN0N1SfRepCombo.setCurrentIndex(0)

        self.nbNpdcchUssRepLabel = QLabel('npdcch-NumRepetitions-r13:')
        self.nbNpdcchUssRepCombo = QComboBox()
        self.nbNpdcchUssRepCombo.addItem('r1')
        self.nbNpdcchUssRepCombo.addItem('r2')
        self.nbNpdcchUssRepCombo.addItem('r4')
        self.nbNpdcchUssRepCombo.addItem('r8')
        self.nbNpdcchUssRepCombo.addItem('r16')
        self.nbNpdcchUssRepCombo.addItem('r32')
        self.nbNpdcchUssRepCombo.addItem('r64')
        self.nbNpdcchUssRepCombo.addItem('r128')
        self.nbNpdcchUssRepCombo.addItem('r256')
        self.nbNpdcchUssRepCombo.addItem('r512')
        self.nbNpdcchUssRepCombo.addItem('r1024')
        self.nbNpdcchUssRepCombo.addItem('r2048')
        self.nbNpdcchUssRepCombo.setCurrentIndex(0)

        self.nbNpdcchUssStartSfLabel = QLabel('npdcch-StartSF-USS-r13:')
        self.nbNpdcchUssStartSfCombo = QComboBox()
        self.nbNpdcchUssStartSfCombo.addItem('v1dot5')
        self.nbNpdcchUssStartSfCombo.addItem('v2')
        self.nbNpdcchUssStartSfCombo.addItem('v4')
        self.nbNpdcchUssStartSfCombo.addItem('v8')
        self.nbNpdcchUssStartSfCombo.addItem('v16')
        self.nbNpdcchUssStartSfCombo.addItem('v32')
        self.nbNpdcchUssStartSfCombo.addItem('v48')
        self.nbNpdcchUssStartSfCombo.addItem('v64')
        self.nbNpdcchUssStartSfCombo.setCurrentIndex(2)

        self.nbNpdcchUssOffLabel = QLabel('npdcch-Offset-USS-r13:')
        self.nbNpdcchUssOffCombo = QComboBox()
        self.nbNpdcchUssOffCombo.addItem('zero')
        self.nbNpdcchUssOffCombo.addItem('oneEighth')
        self.nbNpdcchUssOffCombo.addItem('oneFourth')
        self.nbNpdcchUssOffCombo.addItem('threeEighth')
        self.nbNpdcchUssOffCombo.setCurrentIndex(0)

        layout8 = QGridLayout()
        layout8.addWidget(self.nbDlBitmapLabel, 0, 0)
        layout8.addWidget(self.nbDlBitmapEdit, 0, 1)

        npdschWoBcchDciN1CfgGrpBox = QGroupBox()
        npdschWoBcchDciN1CfgGrpBox.setTitle('NPDSCH w/o BCCH by DCI N1')
        layout9 = QGridLayout()
        layout9.addWidget(self.nbDciN1SfAssignLabel, 0, 0)
        layout9.addWidget(self.nbDciN1SfAssignCombo, 0, 1)
        layout9.addWidget(self.nbDciN1RepLabel, 1, 0)
        layout9.addWidget(self.nbDciN1RepCombo, 1, 1)
        layout9.addWidget(self.nbDciN1DelayLabel, 2, 0)
        layout9.addWidget(self.nbDciN1DelayCombo, 2, 1)
        npdschWoBcchDciN1CfgGrpBox.setLayout(layout9)

        nbDlGapCfgGrpBox = QGroupBox()
        nbDlGapCfgGrpBox.setTitle('NB DL Gap')
        layout10 = QGridLayout()
        layout10.addWidget(self.nbDlGapThreshLabel, 0, 0)
        layout10.addWidget(self.nbDlGapThreshCombo, 0, 1)
        layout10.addWidget(self.nbDlGapPeriodLabel, 1, 0)
        layout10.addWidget(self.nbDlGapPeriodCombo, 1, 1)
        layout10.addWidget(self.nbDlGapDurCoeffLabel, 2, 0)
        layout10.addWidget(self.nbDlGapDurCoeffCombo, 2, 1)
        nbDlGapCfgGrpBox.setLayout(layout10)

        sib23TabWidget = QTabWidget()
        sib2Widget = QWidget()
        layout13 = QGridLayout()
        layout13.addWidget(self.nbSib2PeriodLabel, 0, 0)
        layout13.addWidget(self.nbSib2PeriodCombo, 0, 1)
        layout13.addWidget(self.nbSib2RepPatLabel, 1, 0)
        layout13.addWidget(self.nbSib2RepPatCombo, 1, 1)
        layout13.addWidget(self.nbSib2TbsLabel, 2, 0)
        layout13.addWidget(self.nbSib2TbsCombo, 2, 1)
        sib2Widget.setLayout(layout13)
        sib3Widget = QWidget()
        layout14 = QGridLayout()
        layout14.addWidget(self.nbSib3PeriodLabel, 0, 0)
        layout14.addWidget(self.nbSib3PeriodCombo, 0, 1)
        layout14.addWidget(self.nbSib3RepPatLabel, 1, 0)
        layout14.addWidget(self.nbSib3RepPatCombo, 1, 1)
        layout14.addWidget(self.nbSib3TbsLabel, 2, 0)
        layout14.addWidget(self.nbSib3TbsCombo, 2, 1)
        sib3Widget.setLayout(layout14)
        sib23TabWidget.addTab(sib2Widget, 'SIB2-NB')
        sib23TabWidget.addTab(sib3Widget, 'SIB3-NB')

        nbSiCfgGrpBox = QGroupBox()
        nbSiCfgGrpBox.setTitle('NB SI Scheduling List')
        layout11 = QGridLayout()
        layout11.addWidget(self.nbSiWinLengthLabel, 0, 0)
        layout11.addWidget(self.nbSiWinLengthCombo, 0, 1)
        layout11.addWidget(self.nbSiFrameOffLabel, 1, 0)
        layout11.addWidget(self.nbSiFrameOffCombo, 1, 1)
        layout11.addWidget(sib23TabWidget, 2, 0, 1, 2)
        nbSiCfgGrpBox.setLayout(layout11)

        npdcchUssCfgGrpBox = QGroupBox()
        npdcchUssCfgGrpBox.setTitle('NPDCCH USS')
        layout12 = QGridLayout()
        layout12.addWidget(self.nbDciN0N1SfRepLabel, 0, 0)
        layout12.addWidget(self.nbDciN0N1SfRepCombo, 0, 1)
        layout12.addWidget(self.nbNpdcchUssRepLabel, 1, 0)
        layout12.addWidget(self.nbNpdcchUssRepCombo, 1, 1)
        layout12.addWidget(self.nbNpdcchUssStartSfLabel, 2, 0)
        layout12.addWidget(self.nbNpdcchUssStartSfCombo, 2, 1)
        layout12.addWidget(self.nbNpdcchUssOffLabel, 3, 0)
        layout12.addWidget(self.nbNpdcchUssOffCombo, 3, 1)
        npdcchUssCfgGrpBox.setLayout(layout12)

        layout8.addWidget(npdschWoBcchDciN1CfgGrpBox, 1, 0, 1, 2)
        layout8.addWidget(nbDlGapCfgGrpBox, 2, 0, 1, 2)
        layout8.addWidget(self.nbSchedInfoSib1Label, 3, 0)
        layout8.addWidget(self.nbSchedInfoSib1Combo, 3, 1)
        layout8.addWidget(nbSiCfgGrpBox, 4, 0, 1, 2)
        layout8.addWidget(npdcchUssCfgGrpBox, 5, 0, 1, 2)

        nbIotDlConfig = QWidget()
        layoutNbDl = QVBoxLayout()
        layoutNbDl.addLayout(layout8)
        layoutNbDl.addStretch()
        nbIotDlConfig.setLayout(layoutNbDl)

        tabWidget = QTabWidget()
        tabWidget.addTab(hostLteConfig, 'Host LTE')
        tabWidget.addTab(nbIotCommonConfig, 'NB-IoT Common')
        tabWidget.addTab(nbIotUlConfig, 'NB-IoT UL')
        tabWidget.addTab(nbIotDlConfig, 'NB-IoT DL')

        layout2 = QHBoxLayout()
        layout2.addStretch()
        layout2.addWidget(self.okBtn)
        layout2.addWidget(self.cancelBtn)

        layout = QVBoxLayout()
        layout.addWidget(tabWidget)
        layout.addLayout(layout2)

        self.setLayout(layout)
        self.setWindowTitle('NB-IoT Resource Grid Tool')
        
    def onFsComboCurrentIndexChanged(self, index):
        if index != 0:
            QMessageBox.warning(self, 'Host LTE Cell Config', 'Only FDD is supported for NB-IoT!')
            self.fsCombo.setCurrentIndex(0)
    
    def onCpComboCurrentIndexChanged(self, index):
        if index != 0:
            QMessageBox.warning(self, 'Host LTE Cell Config', 'Only normal CP is supported for NB-IoT!')
            self.cpCombo.setCurrentIndex(0)
    
    def onOkBtnClicked(self):
        #step 1: prepare NgLteGrid
        self.prepLteGrid()
        
        #step 2: call NgLteGrid
        lteGrid = NgLteGrid(self.ngwin, self.argsLte)
        if lteGrid.isOk:
            lteGrid.fillCrs()
            lteGrid.fillPbch()
            lteGrid.fillSch()
            
            #36.211 10.2.5.5 NPDCCH mapping
            #- they are not overlapping with resource elements used for PBCH, PSS, SSS, or CRS as defined in clause 6 (if any),
            #note the use of ndarray.copy()!
            self.argsNbiot['hostLteGridDl'] = lteGrid.gridDl.copy()
            
            lteGrid.fillPdcch()
            lteGrid.printDl()
            
            lteGrid.fillPucch()
            lteGrid.fillPrach()
            lteGrid.fillDmrsForPusch()
            lteGrid.fillSrs()
            lteGrid.printUl()
        else:
            self.accept()
            return
        
        self.argsNbiot['maxPucchRes'] = max(lteGrid.maxPucchRes)
            
        #step 3: prepare NgNbiotGrid
        self.prepNbiotGrid()
        
        #step 4: call NgNbiotGrid
        nbGrid = NgNbiotGrid(self.ngwin, self.argsNbiot)
        nrf = 0
        hsfn = self.argsNbiot['nbHsfn']
        sfn = self.argsNbiot['nbSfn']
        while True: 
            #npdcch check?
            T = int(nbGrid.ussRmax * nbGrid.args['npdcchUssStartSf'])
            k0 = None
            for i in range(nbGrid.subfPerRfNbDl):
                if (sfn * nbGrid.subfPerRfNbDl + i) % T == math.floor(nbGrid.args['npdcchUssOff'] * T):
                    k0 = i
                    break
            
            if nbGrid.recvingNpdcch or (k0 is not None and not nbGrid.recvingNpdsch and not nbGrid.sendingNpusch):
                nbGrid.monitorNpdcch(hsfn, sfn)
                hsfn, sfn = incSfn(hsfn, sfn, 1)
                #hsfn, sfn, subf = nbGrid.monitorNpdcch(hsfn, sfn)
            else:
                nbGrid.normalOps(hsfn, sfn)
                hsfn, sfn = incSfn(hsfn, sfn, 1)
            
            nrf = nrf + 1
            if nrf > 256:
                break
        
        #step 5: parse LTE grid and NB-IoT grid
        self.parseLteNbiotGrid()
        
        self.accept()
        
    def onBwComboCurrentIndexChanged(self, index):
        if index == 0:
            QMessageBox.warning(self, 'Host LTE Cell Config', '1.4MHz system bandwidth is not supported for NB-IoT!')
            self.bwCombo.setCurrentIndex(2)
        else:
            _dlPrbInd = [None,
                         (2, 12),
                         (2, 7, 17, 22),
                         (4, 9, 14, 19, 30, 35, 40, 45),
                         (2, 7, 12, 17, 22, 27, 32, 42, 47, 52, 57, 62, 67, 72),
                         (4, 9, 14, 19, 24, 29, 34, 39, 44, 55, 60, 65, 70, 75, 80, 85, 90, 95)]
            self.nbInBandPrbIdxDlCombo.clear()
            for i in _dlPrbInd[index]:
                self.nbInBandPrbIdxDlCombo.addItem(str(i))
            self.nbInBandPrbIdxDlCombo.setCurrentIndex(0)
            
    def prepLteGrid(self):
        self.argsLte['fs'] = self.fsCombo.currentIndex()
        self.argsLte['bw'] = self.bwCombo.currentIndex()
        self.argsLte['cp'] = self.cpCombo.currentIndex()
        self.argsLte['ap'] = self.apCombo.currentIndex()
        self.argsLte['pci'] = int(self.pciEdit.text())
        self.argsLte['cfi'] = int(self.cfiCombo.currentText())
        self.argsLte['cfiSsf'] = int(self.cfiSsfCombo.currentText())
        self.argsLte['phichDur'] = self.phichDurCombo.currentIndex()
        self.argsLte['phichRes'] = self.phichResCombo.currentIndex()
        self.argsLte['sa'] = self.saCombo.currentIndex()
        self.argsLte['ssp'] = self.sspCombo.currentIndex()
        self.argsLte['dsPucch'] = int(self.dsPucchCombo.currentText()[-1])
        self.argsLte['nCqiRb'] = int(self.nCqiRbEdit.text())
        self.argsLte['nCsAn'] = int(self.nCsAnEdit.text())
        self.argsLte['n1PucchAn'] = int(self.n1PucchAnEdit.text())
        self.argsLte['tddAckMode'] = self.tddAckModeCombo.currentIndex()
        self.argsLte['sfn'] = int(self.sfnEdit.text())
        self.argsLte['prachConfInd'] = int(self.prachConfIndEdit.text())
        self.argsLte['prachFreqOff'] = int(self.prachFreqOffEdit.text())
        if self.argsLte['prachFreqOff'] != 0:
            self.ngwin.logEdit.append('PRACH frequency offset must be 0!')
            self.accept()
            return
        self.argsLte['srsSubfConf'] = int(self.srsSfConfEdit.text())
        
        if self.ngwin.enableDebug:
            self.ngwin.logEdit.append('contents of NgNbiotGridUI.argsLte:')
            for key, value in self.argsLte.items():
                self.ngwin.logEdit.append('-->key=%s, value=%s' % (key, str(value)))
    
    def prepNbiotGrid(self):
        #-->host lte part
        files = []
        files.append('LTE_UL_RES_GRID.csv')
        apNum = (1, 2, 4)[self.argsLte['ap']]
        for i in range(apNum):
            files.append('LTE_DL_RES_GRID_AP%d.csv' % i)
        self.argsNbiot['hostLteGrids'] = files
        self.argsNbiot['hostLtePrbNum'] = (6, 15, 25, 50, 75, 100)[self.argsLte['bw']]
        self.argsNbiot['hostLteApNum'] = apNum
        self.argsNbiot['hostLtePci'] = self.argsLte['pci']
        self.argsNbiot['hostLteCfi'] = self.argsLte['cfi']
        self.argsNbiot['hostLteSrsSubfConf'] = self.argsLte['srsSubfConf']
        
        #-->nb common part
        self.argsNbiot['nbOpMode'] = self.nbOpModeCombo.currentIndex()
        if self.argsNbiot['nbOpMode'] > 1:
            self.ngwin.logEdit.append('Only inband NB-IoT is supported!')
            self.accept()
            return
        self.argsNbiot['nbDlAp'] = 1 if self.nbApCombo.currentIndex() == 0 else 2
        if self.argsNbiot['hostLteApNum'] != self.argsNbiot['nbDlAp']:
            self.ngwin.logEdit.append('#AP of NB cell must be the same as #AP of host LTE cell for inband deployment!')
            self.accept()
            return
        self.argsNbiot['nbPci'] = int(self.nbPciEdit.text())
        if self.argsNbiot['nbPci'] < 0 or self.argsNbiot['nbPci'] > 503:
            self.ngwin.logEdit.append('Invalid NB PCI! Valid range is [0, 503].')
            self.accept()
            return
        elif self.argsNbiot['nbOpMode'] == NbiotPhy.NBIOT_INBAND_SAME_PCI.value and self.argsNbiot['hostLtePci'] != self.argsNbiot['nbPci']:
            self.ngwin.logEdit.append('PCI of host LTE and NB is different for inband-samePCI deployment!')
            self.accept()
            return
        elif self.argsNbiot['nbOpMode'] == NbiotPhy.NBIOT_INBAND_DIFF_PCI.value and self.argsNbiot['hostLtePci'] == self.argsNbiot['nbPci']:
            self.ngwin.logEdit.append('PCI of host LTE and NB is the same for inband-differentPCI deployment!')
            self.accept()
            return
        self.argsNbiot['nbInbandPrbIndUl'] = int(self.nbInBandPrbIdxUlEdit.text())
        if self.argsNbiot['nbInbandPrbIndUl'] != 0:
            self.ngwin.logEdit.append('NB Inband PRB Index UL must be 0!')
            self.accept()
            return
        self.argsNbiot['nbInbandPrbIndDl'] = int(self.nbInBandPrbIdxDlCombo.currentText())
        self.argsNbiot['nbHsfn'] = int(self.nbHsfnEdit.text())
        if self.argsNbiot['nbHsfn'] < 0 or self.argsNbiot['nbHsfn'] > 1023:
            self.ngwin.logEdit.append('Invalid NB HSFN! Valid range is: [0, 1023].')
            self.accept()
            return
        self.argsNbiot['nbSfn'] = int(self.nbSfnEdit.text())
        if self.argsNbiot['nbSfn'] < 0 or self.argsNbiot['nbSfn'] > 1023:
            self.ngwin.logEdit.append('Invalid NB SFN! Valid range is: [0, 1023].')
            self.accept()
            return
        #-->nb ul part
        self.argsNbiot['nbUlScSpacing'] = self.nbUlScSpacingCombo.currentIndex()
        self.argsNbiot['npuschAllSymbols'] = True if self.nbNpuschAllSymCombo.currentIndex() == 0 else False
        self.argsNbiot['npuschFormat1Scs'] = []
        _val = int(self.nbDciN0ScIndEdit.text())
        if self.argsNbiot['nbUlScSpacing'] == NbiotPhy.NBIOT_UL_3DOT75K.value and _val >= 0 and _val <= 47:
            self.argsNbiot['npuschFormat1Scs'].append(_val)
        elif self.argsNbiot['nbUlScSpacing'] == NbiotPhy.NBIOT_UL_15K.value and _val >= 0 and _val <= 18:
            if _val >= 0 and _val <= 11:
                self.argsNbiot['npuschFormat1Scs'].append(_val)
            elif _val >= 12 and _val <= 15:
                for nsc in range(3):
                    self.argsNbiot['npuschFormat1Scs'].append(3*(_val-12)+nsc) 
            elif _val >= 16 and _val <= 17:
                for nsc in range(6):
                    self.argsNbiot['npuschFormat1Scs'].append(6*(_val-16)+nsc)
            else:
                 for nsc in range(12):
                    self.argsNbiot['npuschFormat1Scs'].append(nsc)
        else:
            self.ngwin.logEdit.append('Subcarrier Indication(DCI N0) is not valid! Value range is: [0, 47] for 3.75KHz and [0, 18] for 15KHz.')
            self.accept()
            return
        self.argsNbiot['npuschFormat1NumRu'] = (1, 2, 3, 4, 5, 6, 8, 10)[self.nbDciN0RuIndCombo.currentIndex()]
        self.argsNbiot['npuschFormat1NumRep'] = (1, 2, 4, 8, 16, 32, 64, 128)[self.nbDciN0RepIndCombo.currentIndex()]
        self.argsNbiot['npuschFormat1K0'] = (8, 16, 32, 64)[self.nbDciN0DelayIndCombo.currentIndex()]
        #self.argsNbiot['npuschFormat2NumRep'] = int(self.nbDciN1AnIndCombo.currentText()[1:])
        self.argsNbiot['npuschFormat2NumRep'] = int(self.nbNumAnRepCombo.currentText()[1:])
        _npuschF2Conf = [[(38, 13), (39, 13), (40, 13), (41, 13), (42, 13), (43, 13), (44, 13), (45, 13),
                      (38, 21), (39, 21), (40, 21), (41, 21), (42, 21), (43, 21), (44, 21), (45, 21)],
                     [(0, 13), (1, 13), (2, 13), (3, 13), (0, 15), (1, 15), (2, 15), (3, 15),
                      (0, 17), (1, 17), (2, 17), (3, 17), (0, 18), (1, 18), (2, 18), (3, 18)]]
        self.argsNbiot['npuschFormat2Sc'], self.argsNbiot['npuschFormat2K0'] = _npuschF2Conf[self.argsNbiot['nbUlScSpacing']][self.nbDciN1AnIndCombo.currentIndex()]
        self.argsNbiot['nprachPeriod'] = int(self.nbNprachPeriodCombo.currentText()[2:])
        self.argsNbiot['nprachStartTime'] = int(self.nbNprachStartTimeCombo.currentText()[2:])
        self.argsNbiot['nprachRepPerAtt'] = int(self.nbNprachRepCombo.currentText()[1:])
        self.argsNbiot['nprachNumSc'] = int(self.nbNprachNumScCombo.currentText()[1:])
        self.argsNbiot['nprachScOff'] = int(self.nbNprachScOffCombo.currentText()[1:])
        
        #-->nb dl part
        self.argsNbiot['nbDlBitmap'] = self.nbDlBitmapEdit.text().strip().replace(',', '')
        try:
            _val = int(self.argsNbiot['nbDlBitmap'], base=2)
        except ValueError as e:
            self.ngwin.logEdit.append('Invalid NB DL bitmap: %s' % self.argsNbiot['nbDlBitmap'])
            self.accept()
            return
        if len(self.argsNbiot['nbDlBitmap']) != 10 and len(self.argsNbiot['nbDlBitmap']) != 40:
            self.ngwin.logEdit.append('Invalid size of NB DL bitmap, which must be either 10bits or 40bits!')
            self.accept()
            return
        self.argsNbiot['npdschNoBcchDciN1NumSf'] = (1, 2, 3, 4, 5, 6, 8, 10)[self.nbDciN1SfAssignCombo.currentIndex()]
        self.argsNbiot['npdschNoBcchDciN1NumRep'] = (1, 2, 4, 8, 16, 32, 64, 128, 192, 256, 384, 512, 768, 1024, 1536, 2048)[self.nbDciN1RepCombo.currentIndex()]
        rMax = int(self.nbNpdcchUssRepCombo.currentText()[1:])
        self.argsNbiot['npdschNoBcchDciN1K0'] = (0, 4, 8, 12, 16, 32, 64, 128)[self.nbDciN1DelayCombo.currentIndex()] if rMax < 128 else (0, 16, 32, 64, 128, 256, 512, 1024)[self.nbDciN1DelayCombo.currentIndex()]
        self.argsNbiot['nbDlGapThresh'] = int(self.nbDlGapThreshCombo.currentText()[1:])
        self.argsNbiot['nbDlGapPeriod'] = int(self.nbDlGapPeriodCombo.currentText()[2:])
        self.argsNbiot['nbDlGapDurCoeff'] = (1/8, 1/4, 3/8, 1/2)[self.nbDlGapDurCoeffCombo.currentIndex()]
        self.argsNbiot['npdschSib1NumRep'] = (4, 8, 16, 4, 8, 16, 4, 8, 16, 4, 8, 16)[self.nbSchedInfoSib1Combo.currentIndex()]
        if self.argsNbiot['npdschSib1NumRep'] == 4:
            self.argsNbiot['npdschSib1StartRf'] = 16 * (self.argsNbiot['nbPci'] % 4)
        elif self.argsNbiot['npdschSib1NumRep'] == 8:
            self.argsNbiot['npdschSib1StartRf'] = 16 * (self.argsNbiot['nbPci'] % 2)
        elif self.argsNbiot['npdschSib1NumRep'] == 16:
            self.argsNbiot['npdschSib1StartRf'] = 1 * (self.argsNbiot['nbPci'] % 2)
        self.argsNbiot['nbSiWinLen'] = int(self.nbSiWinLengthCombo.currentText()[2:])
        self.argsNbiot['nbSiRfOff'] = int(self.nbSiFrameOffCombo.currentText())
        self.argsNbiot['nbSib2Period'] = int(self.nbSib2PeriodCombo.currentText()[2:])
        self.argsNbiot['nbSib2RepPattern'] = (2, 4, 8, 16)[self.nbSib2RepPatCombo.currentIndex()]
        self.argsNbiot['nbSib2Tbs'] = int(self.nbSib2TbsCombo.currentText()[1:])
        self.argsNbiot['nbSib3Period'] = int(self.nbSib3PeriodCombo.currentText()[2:])
        self.argsNbiot['nbSib3RepPattern'] = (2, 4, 8, 16)[self.nbSib3RepPatCombo.currentIndex()]
        self.argsNbiot['nbSib3Tbs'] = int(self.nbSib3TbsCombo.currentText()[1:])
        self.argsNbiot['nbDciN0N1SfRep'] = int(self.nbDciN0N1SfRepCombo.currentText())
        self.argsNbiot['npdcchUssNumRep'] = int(self.nbNpdcchUssRepCombo.currentText()[1:])
        if (self.argsNbiot['npdcchUssNumRep'] == 1 and self.argsNbiot['nbDciN0N1SfRep'] > 0) or (self.argsNbiot['npdcchUssNumRep'] == 2 and self.argsNbiot['nbDciN0N1SfRep'] > 1) or (self.argsNbiot['npdcchUssNumRep'] == 4 and self.argsNbiot['nbDciN0N1SfRep'] > 2):
            self.ngwin.logEdit.append('For NPDCCH USS, DCI N0/N1 subframe repetition number is: [0] when npdcch-NumRepetition = 1, [0,1] when npdcch-NumRepetition = 2, and [0,1,2] when npdcch-NumRepetition = 4!')
            self.accept()
            return
        self.argsNbiot['npdcchUssStartSf'] = (1.5, 2, 4, 8, 16, 32, 48, 64)[self.nbNpdcchUssStartSfCombo.currentIndex()]
        if self.argsNbiot['npdcchUssNumRep'] * self.argsNbiot['npdcchUssStartSf'] < 4:
            self.ngwin.logEdit.append('T >= 4 where T = R_max * G as specified in 36.213 16.6!')
            self.accept()
            return
        self.argsNbiot['npdcchUssOff'] = (0, 1/8, 1/4, 3/8)[self.nbNpdcchUssOffCombo.currentIndex()]
        
        if self.ngwin.enableDebug:
            self.ngwin.logEdit.append('contents of NgNbiotGridUI.argsNbiot:')
            for key, value in self.argsNbiot.items():
                self.ngwin.logEdit.append('-->key=%s, value=%s' % (key, str(value)))
                         
    def parseLteNbiotGrid(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        
        #parse LTE grid
        scPerPrb = 12
        prbNum = (6, 15, 25, 50, 75, 100)[self.argsLte['bw']]
        for fn in self.argsNbiot['hostLteGrids']:
            with open(os.path.join(outDir, fn), 'r') as f:
                line = f.readline()
                colLabels = line.split(',')[1:]
                rowLabels = []
                numRows = prbNum * scPerPrb
                numCols = len(colLabels)
                
                tab = QTableWidget()
                tab.setRowCount(numRows)
                tab.setColumnCount(numCols)
                tab.setHorizontalHeaderLabels(colLabels)
                #tab.setVerticalHeaderLabels(rowLabels)
                tab.horizontalHeader().setDefaultSectionSize(8 * self.fontMetrics().width('X'))
                tab.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
                
                ire = 0
                while True:
                    line = f.readline()
                    if not line:
                        break
                    
                    tokens = line.split(',')
                    rowLabels.append(tokens[0])
                    for isym in range(numCols):
                        item = QTableWidgetItem()
                        imap = int(tokens[isym+1])
                        if 'UL_RES_GRID' in fn:
                            _str, _fg, _bg = self.ulMap[imap]
                        else:
                            _str, _fg, _bg = self.dlMap[imap]
                        item.setText(_str)
                        item.setForeground(_fg)
                        item.setBackground(_bg)
                        item.setTextAlignment(Qt.AlignCenter)
                        item.setFlags(item.flags() & (~Qt.ItemIsEditable));
                        tab.setItem(ire, isym, item);
                    ire = ire + 1
                
                tab.setVerticalHeaderLabels(rowLabels)
                self.ngwin.tabWidget.addTab(tab, fn)
