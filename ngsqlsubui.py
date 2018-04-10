#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngsqlsubui.py
Description:
    UI for SQL substitution.
Change History:
    2018-3-29   v0.1    created.    github/zhenggao2
'''

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QCheckBox, QPushButton
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout

class NgSqlSubUi(QDialog):
    def __init__(self, ngwin, names):
        super().__init__()
        self.ngwin = ngwin
        self.names = names
        self.initUi()
    
    def onOkBtnClicked(self):
        self.answers = []
        for edit in self.editList:
            self.answers.append(edit.text().strip())
        
        self.accept()
    
    def initUi(self):
        self.labelList = []
        self.editList = []
        for name in self.names:
            label = QLabel(name+':')
            edit = QLineEdit()
            self.labelList.append(label)
            self.editList.append(edit)
        self.applyToAllChkBox = QCheckBox('Apply to all subsequent queries?')
        self.applyToAllChkBox.setChecked(True)
        self.okBtn = QPushButton('OK')
        self.cancelBtn = QPushButton('Cancel')
        self.okBtn.clicked.connect(self.onOkBtnClicked)
        self.cancelBtn.clicked.connect(self.reject)
        
        self.layout1 = QGridLayout()
        for index, name in enumerate(self.names):
            self.layout1.addWidget(self.labelList[index], index, 0)
            self.layout1.addWidget(self.editList[index], index, 1)
            
        self.layout1.addWidget(self.applyToAllChkBox, len(self.names)+1, 0, 1, 2)
            
        self.layout2 = QHBoxLayout()
        self.layout2.addStretch()
        self.layout2.addWidget(self.okBtn)
        self.layout2.addWidget(self.cancelBtn)
    
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)
        
        self.setLayout(self.layout)
        self.setWindowTitle('Substitution')
