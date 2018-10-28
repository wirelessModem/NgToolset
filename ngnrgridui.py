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

from collections import OrderedDict
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QGroupBox, QTabWidget
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
        #refer to 3GPP 38.104 vf30
        #Table 5.2-1: NR operating bands in FR1
        #Table 5.2-2: NR operating bands in FR2
        _nrOpBandsVf30 = (
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
            ('n80', ('1710 MHz-1785 MHz', 'N/A', 'SUL ')),
            ('n81', ('880 MHz-915 MHz', 'N/A', 'SUL ')),
            ('n82', ('832 MHz-862 MHz', 'N/A', 'SUL ')),
            ('n83', ('703 MHz-748 MHz', 'N/A', 'SUL')),
            ('n84', ('1920 MHz-1980 MHz', 'N/A', 'SUL')),
            ('n86', ('1710 MHz-1780 MHz', 'N/A', 'SUL')),
            ('n257', ('26500 MHz-29500 MHz', '26500 MHz-29500 MHz', 'TDD')),
            ('n258', ('24250 MHz-27500 MHz', '24250 MHz-27500 MHz', 'TDD')),
            ('n260', ('37000 MHz-40000 MHz', '37000 MHz-40000 MHz', 'TDD')),
            ('n261', ('27500 MHz-28350 MHz', '27500 MHz-28350 MHz', 'TDD')),
            )
        self.nrOpBands = OrderedDict(_nrOpBandsVf30)
        self.nrCarrierBandLabel = QLabel('Operating band:')
        self.nrCarrierBandComb = QComboBox()
        self.nrCarrierBandComb.addItems(list(self.nrOpBands.keys()))

        self.nrCarrierBandInfoLabel = QLabel()

        self.nrCarrierScsLabel = QLabel('Subcarrier spacing:')
        self.nrCarrierScsComb = QComboBox()

        self.nrCarrierBwLabel = QLabel('Transmission bandwidth:')
        self.nrCarrierBwComb = QComboBox()

        self.nrCarrierNumRbLabel = QLabel('N_RB:')
        self.nrCarrierNumRbEdit = QLineEdit()
        #self.nrCarrierNumRbEdit.setFocusPolicy(Qt.NoFocus)

        self.nrCarrierBwComb.currentIndexChanged[int].connect(self.onCarrierBwCombCurrentIndexChanged)
        self.nrCarrierScsComb.currentIndexChanged[int].connect(self.onCarrierScsCombCurrentIndexChanged)
        self.nrCarrierBandComb.currentIndexChanged[int].connect(self.onCarrierBandCombCurrentIndexChanged)
        self.nrCarrierBandComb.setCurrentText('n77')

        layout1 = QGridLayout()
        layout1.addWidget(self.nrCarrierBandLabel, 0, 0)
        layout1.addWidget(self.nrCarrierBandComb, 0, 1)
        layout1.addWidget(self.nrCarrierBandInfoLabel, 1, 0, 1, 2)
        layout1.addWidget(self.nrCarrierScsLabel, 2, 0)
        layout1.addWidget(self.nrCarrierScsComb, 2, 1)
        layout1.addWidget(self.nrCarrierBwLabel, 3, 0)
        layout1.addWidget(self.nrCarrierBwComb, 3, 1)
        layout1.addWidget(self.nrCarrierNumRbLabel, 4, 0)
        layout1.addWidget(self.nrCarrierNumRbEdit, 4, 1)

        layout = QVBoxLayout()
        layout.addLayout(layout1)

        self.setLayout(layout)
        self.setWindowTitle('5GNR Resource Grid')

    def onCarrierBandCombCurrentIndexChanged(self, index):
        #self.ngwin.logEdit.append('inside onCarrierBandCombCurrentIndexChanged, index=%d' % index)

        #update band info
        _ulBand, _dlBand, _mode = self.nrOpBands[self.nrCarrierBandComb.currentText()]
        self.freqRange = 'FR1' if int(self.nrCarrierBandComb.currentText()[1:]) <= 256 else 'FR2'
        if _mode == 'TDD':
            self.nrCarrierBandInfoLabel.setText('<font color=blue>UL/DL: %s, %s, %s</font>' % (_ulBand, _mode, self.freqRange))
        else:
            self.nrCarrierBandInfoLabel.setText('<font color=blue>UL: %s, DL: %s, %s, %s</font>' % (_ulBand, _dlBand, _mode, self.freqRange))

        #update subcarrier spacing
        #_nrScsSet = ('15Khz', '30KHz', '60KHz', '120KHz', '240KHz')
        if self.freqRange == 'FR1':
            _scsSubset = ('15KHz', '30KHz', '60KHz')
        else:
            _scsSubset = ('60KHz', '120KHz')
        self.nrCarrierScsComb.clear()
        self.nrCarrierScsComb.addItems(_scsSubset)
        self.nrCarrierScsComb.setCurrentIndex(0)


    def onCarrierScsCombCurrentIndexChanged(self, index):
        #self.ngwin.logEdit.append('inside onCarrierScsCombCurrentIndexChanged, index=%d' % index)
        if index < 0:
            return

        #refer to 3GPP 38.104 vf30
        #Table 5.3.5-1: BS channel bandwidths and SCS per operating band in FR1
        _nrBandScs2BwFr1 = {
            'n1_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n1_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n1_60' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n2_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n2_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n2_60' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n3_15' : (1,1,1,1,1,1,0,0,0,0,0,0,0),
            'n3_30' : (0,1,1,1,1,1,0,0,0,0,0,0,0),
            'n3_60' : (0,1,1,1,1,1,0,0,0,0,0,0,0),
            'n5_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n5_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n5_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n7_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n7_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n7_60' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n8_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n8_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n8_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n12_15' : (1,1,1,0,0,0,0,0,0,0,0,0,0),
            'n12_30' : (0,1,1,0,0,0,0,0,0,0,0,0,0),
            'n12_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n20_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n20_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n20_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n25_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n25_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n25_60' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n28_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n28_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n28_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n34_15' : (1,0,0,0,0,0,0,0,0,0,0,0,0),
            'n34_30' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n34_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n38_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n38_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n38_60' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n39_15' : (1,1,1,1,1,1,1,0,0,0,0,0,0),
            'n39_30' : (0,1,1,1,1,1,1,0,0,0,0,0,0),
            'n39_60' : (0,1,1,1,1,1,1,0,0,0,0,0,0),
            'n40_15' : (1,1,1,1,1,1,1,1,0,0,0,0,0),
            'n40_30' : (0,1,1,1,1,1,1,1,1,0,1,0,1),
            'n40_60' : (0,1,1,1,1,1,1,1,1,0,1,0,1),
            'n41_15' : (0,1,1,1,0,0,1,1,0,0,0,0,0),
            'n41_30' : (0,1,1,1,0,0,1,1,1,1,1,1,1),
            'n41_60' : (0,1,1,1,0,0,1,1,1,1,1,1,1),
            'n50_15' : (1,1,1,1,0,0,1,1,0,0,0,0,0),
            'n50_30' : (0,1,1,1,0,0,1,1,1,0,1,0,0),
            'n50_60' : (0,1,1,1,0,0,1,1,1,0,1,0,0),
            'n51_15' : (1,0,0,0,0,0,0,0,0,0,0,0,0),
            'n51_30' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n51_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n66_15' : (1,1,1,1,0,0,1,0,0,0,0,0,0),
            'n66_30' : (0,1,1,1,0,0,1,0,0,0,0,0,0),
            'n66_60' : (0,1,1,1,0,0,1,0,0,0,0,0,0),
            'n70_15' : (1,1,1,1,1,0,0,0,0,0,0,0,0),
            'n70_30' : (0,1,1,1,1,0,0,0,0,0,0,0,0),
            'n70_60' : (0,1,1,1,1,0,0,0,0,0,0,0,0),
            'n71_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n71_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n71_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n74_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n74_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n74_60' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n75_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n75_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n75_60' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n76_15' : (1,0,0,0,0,0,0,0,0,0,0,0,0),
            'n76_30' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n76_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n77_15' : (0,1,1,1,0,1,1,1,0,0,0,0,0),
            'n77_30' : (0,1,1,1,0,1,1,1,1,1,1,1,1),
            'n77_60' : (0,1,1,1,0,1,1,1,1,1,1,1,1),
            'n78_15' : (0,1,1,1,0,1,1,1,0,0,0,0,0),
            'n78_30' : (0,1,1,1,0,1,1,1,1,1,1,1,1),
            'n78_60' : (0,1,1,1,0,1,1,1,1,1,1,1,1),
            'n79_15' : (0,0,0,0,0,0,1,1,0,0,0,0,0),
            'n79_30' : (0,0,0,0,0,0,1,1,1,0,1,0,1),
            'n79_60' : (0,0,0,0,0,0,1,1,1,0,1,0,1),
            'n80_15' : (1,1,1,1,1,1,0,0,0,0,0,0,0),
            'n80_30' : (0,1,1,1,1,1,0,0,0,0,0,0,0),
            'n80_60' : (0,1,1,1,1,1,0,0,0,0,0,0,0),
            'n81_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n81_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n81_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n82_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n82_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n82_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n83_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n83_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n83_60' : (0,0,0,0,0,0,0,0,0,0,0,0,0),
            'n84_15' : (1,1,1,1,0,0,0,0,0,0,0,0,0),
            'n84_30' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n84_60' : (0,1,1,1,0,0,0,0,0,0,0,0,0),
            'n86_15' : (1,1,1,1,0,0,1,0,0,0,0,0,0),
            'n86_30' : (0,1,1,1,0,0,1,0,0,0,0,0,0),
            'n86_60' : (0,1,1,1,0,0,1,0,0,0,0,0,0),
        }
        #Table 5.3.5-2: BS channel bandwidths and SCS per operating band in FR2
        _nrBandScs2BwFr2 = {
            'n257_60': (1, 1, 1, 0),
            'n257_120': (1, 1, 1, 1),
            'n258_60': (1, 1, 1, 0),
            'n258_120': (1, 1, 1, 1),
            'n260_60': (1, 1, 1, 0),
            'n260_120': (1, 1, 1, 1),
            'n261_60': (1, 1, 1, 0),
            'n261_120': (1, 1, 1, 1),
        }

        _nrBwSetFr1 = ('5MHz', '10MHz', '15MHz', '20MHz', '25MHz', '30MHz', '40MHz', '50MHz', '60MHz', '70MHz', '80MHz', '90MHz', '100MHz')
        _nrBwSetFr2 = ('50MHz', '100MHz', '200MHz', '400MHz')

        _key = self.nrCarrierBandComb.currentText() + '_' + self.nrCarrierScsComb.currentText()[:-3]
        if not _key in _nrBandScs2BwFr1 and not _key in _nrBandScs2BwFr2:
            return
        if self.freqRange == 'FR1':
            _bwSubset = [_nrBwSetFr1[i] for i in range(len(_nrBwSetFr1)) if _nrBandScs2BwFr1[_key][i]]
        else:
            _bwSubset = [_nrBwSetFr2[i] for i in range(len(_nrBwSetFr2)) if _nrBandScs2BwFr2[_key][i]]

        self.nrCarrierBwComb.clear()
        self.nrCarrierBwComb.addItems(_bwSubset)
        self.nrCarrierBwComb.setCurrentIndex(0)

    def onCarrierBwCombCurrentIndexChanged(self, index):
        #self.ngwin.logEdit.append('inside onCarrierBwCombCurrentIndexChanged, index=%d' % index)
        if index < 0:
            return

        #refer to 3GPP 38.104 vf30
        #Table 5.3.2-1: Transmission bandwidth configuration N_RB for FR1
        _nrNrbFr1 = {
            15: (25, 52, 79, 106, 133, 160, 216, 270, 0, 0, 0, 0, 0),
            30: (11, 24, 38, 51, 65, 78, 106, 133, 162, 189, 217, 245, 273),
            60: (0, 11, 18, 24, 31, 38, 51, 65, 79, 93, 107, 121, 135),
        }
        #Table 5.3.2-2: Transmission bandwidth configuration N_RB for FR2
        _nrNrbFr2 = {
            60: (66, 132, 264, 0),
            120: (32, 66, 132, 264),
        }

        _nrBwSetFr1 = ('5MHz', '10MHz', '15MHz', '20MHz', '25MHz', '30MHz', '40MHz', '50MHz', '60MHz', '70MHz', '80MHz', '90MHz', '100MHz')
        _nrBwSetFr2 = ('50MHz', '100MHz', '200MHz', '400MHz')

        _key = int(self.nrCarrierScsComb.currentText()[:-3])
        if not _key in _nrNrbFr1 and not _key in _nrNrbFr2:
            return

        if self.freqRange == 'FR1':
            self.numRb = _nrNrbFr1[_key][_nrBwSetFr1.index(self.nrCarrierBwComb.currentText())]
        else:
            self.numRb = _nrNrbFr2[_key][_nrBwSetFr2.index(self.nrCarrierBwComb.currentText())]
        self.nrCarrierNumRbEdit.setText(str(self.numRb))
