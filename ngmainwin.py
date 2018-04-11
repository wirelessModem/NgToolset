#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngmainwin.py
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
from ngxmlparser import NgXmlParser
from ngsqlquery import NgSqlQuery
from ngm8015proc import NgM8015Proc
import os

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
    
    def onExecXmlParser(self):
        indir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        parser = NgXmlParser(self, indir) 
        parser.start()
    
    def onExecNedsM8015(self):
        args = dict()
        args['dbConf'] = 'dbconfig.txt'
        args['sqlQuery'] = ['neds_lnadj.sql', 'neds_lnadjl.sql', 'neds_lncel.sql', 'neds_lnhoif.sql', 'neds_lnrel.sql',
                            'neds_m8015.sql', 'neds_m8051.sql', 'neds_m8005.sql', 'neds_m8001.sql', 'neds_m8013.sql', 'neds_m8006.sql',]
    
        query = NgSqlQuery(self, args)
        query.exec_()
        
        if query.queryStat:
            proc = NgM8015Proc(self)
            proc.loadCsvData()
            proc.makeEciMap()
            proc.procUserCase01()
            proc.procUserCase02()
            self.logEdit.append('<font color=blue>Done!</font>')
        
    def onExecLteResGrid(self):
        dlg = NgLteGridUi(self)
        dlg.exec_()
    
    def onExecNbiotResGrid(self):
        dlg = NgNbiotGridUi(self)
        dlg.exec_()
    
    def onExecNrResGrid(self):
        QMessageBox.information(self, 'NR Resource Grid', '<p><font color=red><b>Oops, NR resource grid is still under development!</b></font></p>'
                                + '<p>Please visit: <a href="http://www.3gpp.org/ftp/Specs/2018-03/Rel-15/38_series/"> http://www.3gpp.org/ftp/Specs/2018-03/Rel-15/38_series/</a> for latest 5G NSA specifications.</p>')
        
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
        self.xmlParserAction = QAction('SCF/Vendor Parser')
        self.xmlParserAction.triggered.connect(self.onExecXmlParser)
        self.sqlQueryAction = QAction('NEDS (M8015 Analyzer)')
        self.sqlQueryAction.triggered.connect(self.onExecNedsM8015)
        
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
        self.miscMenu.addAction(self.xmlParserAction)
        self.miscMenu.addAction(self.sqlQueryAction)
        
        self.optionsMenu = self.menuBar().addMenu('Options')
        self.optionsMenu.addAction(self.enableDebugAction)
        
        self.helpMenu = self.menuBar().addMenu('Help')
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.aboutQtAction)
        
