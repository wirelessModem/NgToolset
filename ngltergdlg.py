#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngltergdlg.py
Description:
    UI for LTE resource grid.
Change History:
    2018-1-19   v0.1    created.    github/zhenggao2
'''

from PyQt5.QtWidgets import QDialog, QTextEdit, QTabWidget, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QColor
import ngmainwin
from ngltephy import LteResType

class NgLteResGridDlg(QDialog):
    def __init__(self):
        super().__init__()
        self.params = dict()
        self.initResGridMapper()
        self.initUi()
        
    def onOkBtnClicked(self):
        self.accept()
    
    def initUi(self):
        self.fsLabel = QLabel('Frame Structure:')
        self.fsCombo = QComboBox()
        self.fsCombo.addItem('Type 1(FDD)')
        self.fsCombo.addItem('Type 2(TDD)')
        self.fsCombo.setCurrentIndex(1)
        
        self.bwLabel = QLabel('System Bandwidth:')
        self.bwCombo = QComboBox()
        self.bwCombo.addItem('1.4MHz')
        self.bwCombo.addItem('3MHz')
        self.bwCombo.addItem('5MHz')
        self.bwCombo.addItem('10MHz')
        self.bwCombo.addItem('15MHz')
        self.bwCombo.addItem('20MHz')
        self.bwCombo.setCurrentIndex(5)

        self.cpLabel = QLabel('Cyclic Prefix:')
        self.cpCombo = QComboBox()
        self.cpCombo.addItem('Normal CP')
        self.cpCombo.addItem('Extended CP')
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

        self.layout1 = QGridLayout();
        self.layout1.addWidget(self.fsLabel, 0, 0)
        self.layout1.addWidget(self.fsCombo, 0, 1)
        self.layout1.addWidget(self.bwLabel, 1, 0)
        self.layout1.addWidget(self.bwCombo, 1, 1)
        self.layout1.addWidget(self.cpLabel, 2, 0)
        self.layout1.addWidget(self.cpCombo, 2, 1)
        self.layout1.addWidget(self.apLabel, 3, 0)
        self.layout1.addWidget(self.apCombo, 3, 1)
        self.layout1.addWidget(self.pciLabel, 4, 0)
        self.layout1.addWidget(self.pciEdit, 4, 1)
        self.layout1.addWidget(self.cfiLabel, 5, 0)
        self.layout1.addWidget(self.cfiCombo, 5, 1)
        self.layout1.addWidget(self.cfiSsfLabel, 6, 0)
        self.layout1.addWidget(self.cfiSsfCombo, 6, 1)
        self.layout1.addWidget(self.phichDurLabel, 7, 0)
        self.layout1.addWidget(self.phichDurCombo, 7, 1)
        self.layout1.addWidget(self.phichResLabel, 8, 0)
        self.layout1.addWidget(self.phichResCombo, 8, 1)
        self.layout1.addWidget(self.saLabel, 9, 0)
        self.layout1.addWidget(self.saCombo, 9, 1)
        self.layout1.addWidget(self.sspLabel, 10, 0)
        self.layout1.addWidget(self.sspCombo, 10, 1)
        self.layout1.addWidget(self.dsPucchLabel, 11, 0)
        self.layout1.addWidget(self.dsPucchCombo, 11, 1)
        self.layout1.addWidget(self.nCqiRbLabel, 12, 0)
        self.layout1.addWidget(self.nCqiRbEdit, 12, 1)
        self.layout1.addWidget(self.nCsAnLabel, 13, 0)
        self.layout1.addWidget(self.nCsAnEdit, 13, 1)
        self.layout1.addWidget(self.n1PucchAnLabel, 14, 0)
        self.layout1.addWidget(self.n1PucchAnEdit, 14, 1)
        self.layout1.addWidget(self.tddAckModeLabel, 15, 0)
        self.layout1.addWidget(self.tddAckModeCombo, 15, 1)
        self.layout1.addWidget(self.sfnLabel, 16, 0)
        self.layout1.addWidget(self.sfnEdit, 16, 1)
        self.layout1.addWidget(self.prachConfIndLabel, 17, 0)
        self.layout1.addWidget(self.prachConfIndEdit, 17, 1)
        self.layout1.addWidget(self.prachFreqOffLabel, 18, 0)
        self.layout1.addWidget(self.prachFreqOffEdit, 18, 1)
        self.layout1.addWidget(self.srsSfConfLabel, 19, 0)
        self.layout1.addWidget(self.srsSfConfEdit, 19, 1)

        self.layout2 = QHBoxLayout();
        self.layout2.addStretch()
        self.layout2.addWidget(self.okBtn)
        self.layout2.addWidget(self.cancelBtn)

        self.layout = QVBoxLayout();
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)

        self.setLayout(self.layout)
        self.setWindowTitle('LTE Resource Grid Tool')
    
    def initResGridMapper(self):
        dlMap = dict()
        dlMap[LteResType.LTE_RES_PDSCH] = ('pdsch', QColor(0, 0, 0), QColor(255, 255, 255)) 
        dlMap[LteResType.LTE_RES_PDCCH] = ('pdcch', QColor(0, 0, 0), QColor(0, 255, 255)) 
        dlMap[LteResType.LTE_RES_PHICH] = ('phich', QColor(0, 0, 0), QColor(255, 0, 255)) 
        dlMap[LteResType.LTE_RES_PCFICH] = ('pcfich', QColor(0, 0, 255), QColor(255, 255, 255)) 
        dlMap[LteResType.LTE_RES_PBCH] = ('pbch', QColor(0, 0, 0), QColor(128, 255, 255)) 
        dlMap[LteResType.LTE_RES_PSCH] = ('psch', QColor(0, 0, 0), QColor(0, 255, 0)) 
        dlMap[LteResType.LTE_RES_SSCH] = ('ssch', QColor(0, 0, 0), QColor(255, 255, 0)) 
        dlMap[LteResType.LTE_RES_CRS] = ('crs', QColor(0, 0, 0), QColor(255, 0, 0)) 
        dlMap[LteResType.LTE_RES_DTX] = ('dtx', QColor(255, 255, 255), QColor(0, 0, 0)) 
        dlMap[LteResType.LTE_RES_GP] = ('gp', QColor(255, 255, 255), QColor(0, 0, 0)) 
        dlMap[LteResType.LTE_RES_UL] = ('ul', QColor(255, 255, 255), QColor(0, 0, 0)) 
        
        ulMap = dict()
        ulMap[LteResType.LTE_RES_GP] = ('gp', QColor(0, 0, 0), QColor(0, 255, 0))
        ulMap[LteResType.LTE_RES_DL] = ('dl', QColor(255, 255, 255), QColor(0, 0, 0))
        ulMap[LteResType.LTE_RES_PUSCH] = ('pusch', QColor(0, 0, 0), QColor(255, 255, 255))
        ulMap[LteResType.LTE_RES_PUCCH_AN] = ('an', QColor(0, 0, 0), QColor(0, 255, 255))
        ulMap[LteResType.LTE_RES_PUCCH_MIXED] = ('mixed', QColor(0, 0, 0), QColor(255, 0, 255))
        ulMap[LteResType.LTE_RES_PUCCH_CQI] = ('cqi', QColor(255, 255, 255), QColor(0, 0, 255))
        ulMap[LteResType.LTE_RES_PRACH] = ('prach', QColor(0, 0, 0), QColor(128, 255, 255))
        ulMap[LteResType.LTE_RES_DMRS] = ('dmrs', QColor(0, 0, 0), QColor(255, 0, 0))
        ulMap[LteResType.LTE_RES_SRS] = ('srs', QColor(0, 0, 0), QColor(255, 255, 0))
        
        self.params['dlmap'] = dlMap
        self.params['ulmap'] = ulMap
