#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ng_mainwin.py
Description:
    NgMainWin definition
Change History:
    2018-1-19   v0.1    created.    github/zhenggao2
'''

from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QTabWidget, QTextEdit, QMessageBox
from PyQt5.QtWidgets import qApp, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase
#-->import plugins
from ngltegridui import NgLteGridUi
from ngnbiotgridui import NgNbiotGridUi

class NgMainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.enableDebug = False
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.logEdit = QTextEdit()
        self.tabWidget.addTab(self.logEdit, 'log')
       
        self.createActions()
        self.createMenus()
       
        self.setCentralWidget(self.tabWidget)
        self.setWindowTitle('NG Toolset')
        self.setWindowFlags(self.windowFlags() or Qt.WindowMinMaxButtonsHint)
        self.setWindowState(self.windowState() or Qt.WindowMaximized)
        self.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)
    
    def onTabCloseRequested(self, index):
        if index == 0:
            return
        widget = self.tabWidget.widget(index)
        self.tabWidget.removeTab(index)
        
    def onAbout(self):
        QMessageBox.information(self, 'About', '<h1>NG Toolset</h1><p>NG toolset is set of useful NPO tools for 4G and 5G.</p>'
                                + '<p>Author: zhengwei.gao@yahoo.com</p>')
        
    def onEnableDebug(self, checked):
        self.enableDebug = checked
        
    def onChkSqlPlugin(self):
        drivers = QSqlDatabase().drivers()
        for e in drivers:
            self.logEdit.append('Found SQL driver: %s' % e)
            
    def onExecLteResGrid(self):
        dlg = NgLteGridUi(self)
        dlg.exec_()
    
    def onExecNbiotResGrid(self):
        dlg = NgNbiotGridUi(self)
        dlg.exec_()
    
    def onExecNrResGrid(self):
        pass
        
    def createActions(self):
        #File Menu
        self.exitAction = QAction('Exit')
        self.exitAction.triggered.connect(self.close)
        
        #LTE menu
        self.lteResGridAction= QAction('LTE Resource Grid')
        self.lteResGridAction.triggered.connect(self.onExecLteResGrid)
        self.nbiotResGridAction= QAction('NB-IoT Resource Grid')
        self.nbiotResGridAction.triggered.connect(self.onExecNbiotResGrid)
        
        #NR menu
        self.nrResGridAction= QAction('NR Resource Grid')
        self.nrResGridAction.triggered.connect(self.onExecNrResGrid)
        
        #Misc menu
        self.chkSqlAction = QAction('Check SQL Plugin')
        self.chkSqlAction.triggered.connect(self.onChkSqlPlugin)
        
        #Options menu
        self.enableDebugAction = QAction('Enable Debug')
        self.enableDebugAction.setCheckable(True)
        self.enableDebugAction.setChecked(False)
        self.enableDebugAction.triggered[bool].connect(self.onEnableDebug)
        
        #Help menu
        self.aboutAction = QAction('About')
        self.aboutAction.triggered.connect(self.onAbout)
        self.aboutQtAction = QAction('About Qt')
        self.aboutQtAction.triggered.connect(qApp.aboutQt)
    
    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu('File')
        self.fileMenu.addAction(self.exitAction)
        
        self.lteMenu = self.menuBar().addMenu('LTE')
        self.lteMenu.addAction(self.lteResGridAction)
        self.lteMenu.addAction(self.nbiotResGridAction)
        
        self.nrMenu = self.menuBar().addMenu('NR')
        self.nrMenu.addAction(self.nrResGridAction)
        
        self.miscMenu = self.menuBar().addMenu('Misc')
        self.miscMenu.addAction(self.chkSqlAction)
        
        self.optionsMenu = self.menuBar().addMenu('Options')
        self.optionsMenu.addAction(self.enableDebugAction)
        
        self.helpMenu = self.menuBar().addMenu('Help')
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.aboutQtAction)
        
