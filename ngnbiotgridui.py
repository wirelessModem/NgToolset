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
from PyQt5.QtWidgets import QDialog, QTextEdit, QTabWidget, QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import ngmainwin
from ngltephy import LteResType
from ngltegrid import NgLteGrid
from ngb36utils import time2str36, freq2str36

class NgNbiotGridUi(QDialog):
    def __init__(self, ngwin):
        super().__init__()
        self.ngwin = ngwin
        self.args = dict()
        self.initResGridMapper()
        self.initUi()
    
    def initResGridMapper(self):
        pass
    
    def initUi(self):
        pass
