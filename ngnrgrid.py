#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngnrgrid.py
Description:
    Implementation of 5GNR resource grid.
Change History:
    2018-12-28  v0.1    created.    github/zhenggao2
'''

import ngmainwin

class NgNrGrid(object):
    def __init__(self, ngwin, args):
        self.ngwin = ngwin
        self.args = args
        self.init()
    
    def init(self):
        self.ngwin.logEdit.append('---->inside init')
        self.nrSubfPerRf = 10
        self.nrSlotPerSubf = [2 ** mu for mu in range(5)]
        self.nrSlotPerRf = [self.nrSubfPerRf * 2 ** mu for mu in range(5)]
        self.nrSymbPerSlotNormCp = 14
        self.nrSymbPerSlotExtCp = 12
        self.nrScPerPrb = 12
    
    def recvSsb(self):
        self.ngwin.logEdit.append('---->inside recvSsb')
        pass
    
    def monitorPdcch(self):
        pass
    
    def recvSib1(self):
        pass
    
    def sendMsg1(self):
        pass
    
    def recvMsg2(self):
        pass
    
    def sendMsg3(self):
        pass
    
    def recvMsg4(self):
        pass
    
    def sendPucch(self):
        pass
    
    def sendPusch(self):
        pass
    
    def recvPdsch(self):
        pass
    
    def normalOps(self):
        pass
