#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ng_app.py
Description:
    The main routine.
Change History:
    2018-1-19   v0.1    created by github/zhenggao2
'''

import sys
from PyQt5.QtWidgets import QApplication
from ngmainwin import NgMainWin

app = QApplication(sys.argv)
mainWin = NgMainWin()
mainWin.show()
sys.exit(app.exec_())
