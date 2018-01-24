#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngltegrid.py
Description:
    NgLteGrid definition.
Change History:
    2018-1-21   v0.1    created.    github/zhenggao2
'''

from collections import Counter
import math
import os
import time 
import numpy as np
import ngmainwin
from ngltephy import LtePhy, LteResType

class NgLteGrid(object):
    def __init__(self, ngwin, args):
        self.scPerPrb = 12
        self.slotPerSubf = 2
        self.subfPerRf = 10
        self.regPerCce = 9
        self.isOk = False
        self.ngwin = ngwin
        self.init(args)
    
    def init(self, args):
        self.fs = args['fs']
        self.bw = args['bw']
        self.cp = args['cp']
        self.ap = args['ap']
        self.pci = args['pci']
        self.cfi = args['cfi']
        self.cfiSsf = args['cfiSsf']
        self.phichDur = args['phichDur']
        self.phichRes = args['phichRes']
        self.sa = args['sa']
        self.ssp = args['ssp']
        _sspNormCp = {0 : (3, 10, 1),
                   1 : (9, 4, 1),
                   2 : (10, 3, 1),
                   3 : (11, 2, 1),
                   4 : (12, 1, 1),
                   5 : (3, 9, 2),
                   6 : (9, 3, 2),
                   7 : (10, 2, 2),
                   8 : (11, 1, 2)}
        _sspExtCp = {0 : (3, 8, 1),
                       1 : (8, 3, 1),
                       2 : (9, 2, 1),
                       3 : (10, 1, 1),
                       4 : (3, 7, 2),
                       5 : (8, 2, 2),
                       6 : (9, 1, 2)}
        if self.cp == LtePhy.LTE_CP_NORMAL.value:
            self.dwpts, self.gp, self.uppts = _sspNormCp[self.ssp]
        else:
            if self.ssp >= 7:
                self.ngwin.logEdit.append('args error: SSP 7/8 can only be used for normal CP.')
                return
            else:
                self.dwpts, self.gp, self.uppts = _sspExtCp[self.ssp]
        self.deltaPucchShift = args['dsPucch']
        self.nCqiRb = args['nCqiRb']
        self.nCsAn = args['nCsAn']
        self.n1PucchAn = args['n1PucchAn']
        self.tddAckMode = args['tddAckMode']
        self.sfn = args['sfn']
        self.prachConfInd = args['prachConfInd']
        self.prachFreqOff = args['prachFreqOff']
        self.srsSubfConf = args['srsSubfConf']
        
        if self.bw == LtePhy.LTE_BW_6.value:
            if not (self.cfi >= 2 and self.cfi <= 4 and self.cfiSsf == 2):
                self.ngwin.logEdit.append('args error: when system bandwidth is 1.4MHz, CFI must be 2~4 in normal DL subframe and must be 2 in DwPTS.')
                return
        else:
            if not(self.cfi >= 1 and self.cfi <= 3 and self.cfiSsf >= 1 and self.cfiSsf <= 2):
                self.ngwin.logEdit.append('args error: when system bandwidth is not 1.4MHz, CFI must be 1~3 in normal DL subframe and must be 1~2 in DwPTS.')
                return
            
        _prbmap = (6, 15, 25, 50, 75, 100)
        self.prbNum = _prbmap[self.bw]
        
        self.symbPerSlot = 7 if self.cp == LtePhy.LTE_CP_NORMAL.value else 6
        self.symbPerSubf = self.symbPerSlot * self.slotPerSubf
        self.symbPerRf = self.symbPerSubf * self.subfPerRf
        self.rePerSymb = self.prbNum * self.scPerPrb
        self.rePerSlot = self.rePerSymb * self.symbPerSlot
        self.rePerSubf = self.rePerSlot * self.slotPerSubf
        self.rePerRf = self.rePerSubf * self.subfPerRf
        
        _apmap = (1, 2, 4)
        self.apNum = _apmap[self.ap]
        
        self.gridDl = np.full((self.apNum, self.rePerSymb, self.symbPerRf), LteResType.LTE_RES_PDSCH.value)
        self.gridUl = np.full((1, self.rePerSymb, self.symbPerRf), LteResType.LTE_RES_PUSCH.value)
        if self.ngwin.enableDebug:
            self.ngwin.logEdit.append('NgLteGrid.gridDl info: ndim=%s, shape=%s, dtype=%s' % (str(self.gridDl.ndim), str(self.gridDl.shape), str(self.gridDl.dtype)))
            self.ngwin.logEdit.append('NgLteGrid.gridUl info: ndim=%s, shape=%s, dtype=%s' % (str(self.gridUl.ndim), str(self.gridUl.shape), str(self.gridUl.dtype)))
            
        _tddConf = [{'name' : 'sa0', 'pat' : 'dsuuudsuuu', 'ack' : {2 : (6,), 4 : (4,), 7 : (6,), 9 : (4,)}},
                    {'name' : 'sa1', 'pat' : 'dsuuddsuud', 'ack' : {2 : (7, 6), 3 : (4,), 7 : (7, 6), 8 : (4,)}},
                    {'name' : 'sa2', 'pat' : 'dsudddsudd', 'ack': {2 : (8, 7, 4, 6), 7 : (8, 7, 4, 6)}}, 
                    {'name' : 'sa3', 'pat' : 'dsuuudsddd', 'ack': {2 : (7, 6, 11), 3 : (6, 5), 4: (5, 4)}},
                    {'name' : 'sa4', 'pat' : 'dsuudddddd', 'ack' : {2 : (12, 8, 7, 11), 3 : (6, 5, 4, 7)}},
                    {'name' : 'sa5', 'pat' : 'dsuddddddd', 'ack' : {2 : (13, 12, 9, 8, 7, 5, 4, 11, 6)}},
                    {'name' : 'sa6', 'pat' : 'dsuuudsuud', 'ack' : {2 : (7,), 3 : (7,), 4 : (5,), 7 : (7,), 8 : (7,)}}]
        self.subfPatTdd = _tddConf[self.sa]['pat']
        self.ackIndTdd = _tddConf[self.sa]['ack']
        self.cce = np.zeros(self.subfPerRf)
        self.maxPucch = np.zeros(self.subfPerRf)
        
        if self.fs == LtePhy.LTE_FS_TYPE2.value:
            for isf in range(self.subfPerRf):
                if self.subfPatTdd[isf] == 'u':
                    for iap in range(self.apNum):
                        for ire in range(self.rePerSymb):
                            self.gridDl[iap][ire][isf*self.symbPerSubf:(isf+1)*self.symbPerSubf] = LteResType.LTE_RES_UL.value
                elif self.subfPatTdd[isf] == 's':
                    for iap in range(self.apNum):
                        for ire in range(self.rePerSymb):
                            self.gridDl[iap][ire][isf*self.symbPerSubf+self.dwpts:isf*self.symbPerSubf+self.dwpts+self.gp] = LteResType.LTE_RES_GP.value
                            self.gridDl[iap][ire][isf*self.symbPerSubf+self.dwpts+self.gp:(isf+1)*self.symbPerSubf] = LteResType.LTE_RES_UL.value
                    for ire in range(self.rePerSymb):
                        self.gridUl[0][ire][isf*self.symbPerSubf:isf*self.symbPerSubf+self.dwpts] = LteResType.LTE_RES_DL.value
                        self.gridUl[0][ire][isf*self.symbPerSubf+self.dwpts:isf*self.symbPerSubf+self.dwpts+self.gp] = LteResType.LTE_RES_GP.value
                else:
                    for ire in range(self.rePerSymb):
                        self.gridUl[0][ire][isf*self.symbPerSubf:(isf+1)*self.symbPerSubf] = LteResType.LTE_RES_DL.value
        
        if self.fs == LtePhy.LTE_FS_TYPE1.value:
            if not self.initPrachFdd():
                self.ngwin.logEdit.append('NgLteGrid::initPrachFdd failed.')
                return
            if not self.initSrsFdd():
                self.ngwin.logEdit.append('NgLteGrid::initSrsFdd failed.')
                return
        else:
            if not self.initPrachTdd():
                self.ngwin.logEdit.append('NgLteGrid::initPrachTdd failed.')
                return
            if not self.initSrsTdd():
                self.ngwin.logEdit.append('NgLteGrid::initSrsTdd failed.')
                return
        
        self.crsOk= False
        self.pcfichOk= False
        self.phichOk= False
        self.pucchOk = False
        self.prachOk = False
        
        self.isOk = True
        
    def initPrachFdd(self):
        #Table 5.7.1-2: Frame structure type 1 random access configuration for preamble formats 0-3
        _prachConfFdd = [{'format' : 0, 'sfn' : 'even', 'subf' : (1,)}, 
                         #1
                         {'format' : 0, 'sfn' : 'even', 'subf' : (4,)},
                         #2
                         {'format' : 0, 'sfn' : 'even', 'subf' : (7,)}, 
                         #3
                         {'format' : 0, 'sfn' : 'any', 'subf' : (1,)}, 
                         #4
                         {'format' : 0, 'sfn' : 'any', 'subf' : (4,)}, 
                         #5
                         {'format' : 0, 'sfn' : 'any', 'subf' : (7,)}, 
                         #6
                         {'format' : 0, 'sfn' : 'any', 'subf' : (1, 6)}, 
                         #7
                         {'format' : 0, 'sfn' : 'any', 'subf' : (2, 7)},
                         #8
                         {'format' : 0, 'sfn' : 'any', 'subf' : (3, 8)}, 
                         #9
                         {'format' : 0, 'sfn' : 'any', 'subf' : (1, 4, 7)}, 
                         #10
                         {'format' : 0, 'sfn' : 'any', 'subf' : (2, 5, 8)}, 
                         #11
                         {'format' : 0, 'sfn' : 'any', 'subf' : (3, 6, 9)}, 
                         #12
                         {'format' : 0, 'sfn' : 'any', 'subf' : (0, 2, 4, 6, 8)}, 
                         #13
                         {'format' : 0, 'sfn' : 'any', 'subf' : (1, 3, 5, 7, 9)}, 
                         #14
                         {'format' : 0, 'sfn' : 'any', 'subf' : (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)}, 
                         #15
                         {'format' : 0, 'sfn' : 'even', 'subf' : (9,)}, 
                         #16
                         {'format' : 1, 'sfn' : 'even', 'subf' : (1,)}, 
                         #17
                         {'format' : 1, 'sfn' : 'even', 'subf' : (4,)}, 
                         #18
                         {'format' : 1, 'sfn' : 'even', 'subf' : (7,)}, 
                         #19
                         {'format' : 1, 'sfn' : 'any', 'subf' : (1,)}, 
                         #20
                         {'format' : 1, 'sfn' : 'any', 'subf' : (4,)}, 
                         #21
                         {'format' : 1, 'sfn' : 'any', 'subf' : (7,)}, 
                         #22
                         {'format' : 1, 'sfn' : 'any', 'subf' : (1, 6)}, 
                         #23
                         {'format' : 1, 'sfn' : 'any', 'subf' : (2, 7)},
                         #24
                         {'format' : 1, 'sfn' : 'any', 'subf' : (3, 8)}, 
                         #25
                         {'format' : 1, 'sfn' : 'any', 'subf' : (1, 4, 7)}, 
                         #26
                         {'format' : 1, 'sfn' : 'any', 'subf' : (2, 5, 8)}, 
                         #27
                         {'format' : 1, 'sfn' : 'any', 'subf' : (3, 6, 9)}, 
                         #28
                         {'format' : 1, 'sfn' : 'any', 'subf' : (0, 2, 4, 6, 8)}, 
                         #29
                         {'format' : 1, 'sfn' : 'any', 'subf' : (1, 3, 5, 7, 9)}, 
                         #30 invalid config index = 30
                         {'format' : -1},
                         #31
                         {'format' : 1, 'sfn' : 'any', 'subf' : (9,)}, 
                         #32
                         {'format' : 2, 'sfn' : 'even', 'subf' : (1,)}, 
                         #33
                         {'format' : 2, 'sfn' : 'even', 'subf' : (4,)}, 
                         #34
                         {'format' : 2, 'sfn' : 'even', 'subf' : (7,)}, 
                         #35
                         {'format' : 2, 'sfn' : 'any', 'subf' : (1,)}, 
                         #36
                         {'format' : 2, 'sfn' : 'any', 'subf' : (4,)}, 
                         #37
                         {'format' : 2, 'sfn' : 'any', 'subf' : (7,)},
                         #38
                         {'format' : 2, 'sfn' : 'any', 'subf' : (1, 6)}, 
                         #39
                         {'format' : 2, 'sfn' : 'any', 'subf' : (2, 7)},
                         #40
                         {'format' : 2, 'sfn' : 'any', 'subf' : (3, 8)}, 
                         #41
                         {'format' : 2, 'sfn' : 'any', 'subf' : (1, 4, 7)}, 
                         #42
                         {'format' : 2, 'sfn' : 'any', 'subf' : (2, 5, 8)}, 
                         #43
                         {'format' : 2, 'sfn' : 'any', 'subf' : (3, 6, 9)}, 
                         #44
                         {'format' : 2, 'sfn' : 'any', 'subf' : (0, 2, 4, 6, 8)}, 
                         #45
                         {'format' : 2, 'sfn' : 'any', 'subf' : (1, 3, 5, 7, 9)}, 
                         #46 invalid config index = 46 
                         {'format' : -1},
                         #47
                         {'format' : 2, 'sfn' : 'any', 'subf' : (9,)}, 
                         #48
                         {'format' : 3, 'sfn' : 'even', 'subf' : (1,)}, 
                         #49
                         {'format' : 3, 'sfn' : 'even', 'subf' : (4,)}, 
                         #50
                         {'format' : 3, 'sfn' : 'even', 'subf' : (7,)}, 
                         #51
                         {'format' : 3, 'sfn' : 'any', 'subf' : (1,)}, 
                         #52
                         {'format' : 3, 'sfn' : 'any', 'subf' : (4,)}, 
                         #53
                         {'format' : 3, 'sfn' : 'any', 'subf' : (7,)},
                         #54
                         {'format' : 3, 'sfn' : 'any', 'subf' : (1, 6)}, 
                         #55
                         {'format' : 3, 'sfn' : 'any', 'subf' : (2, 7)},
                         #56
                         {'format' : 3, 'sfn' : 'any', 'subf' : (3, 8)}, 
                         #57
                         {'format' : 3, 'sfn' : 'any', 'subf' : (1, 4, 7)}, 
                         #58
                         {'format' : 3, 'sfn' : 'any', 'subf' : (2, 5, 8)}, 
                         #59
                         {'format' : 3, 'sfn' : 'any', 'subf' : (3, 6, 9)}, 
                         #60~62 invalid config index = 60/61/62
                         {'format' : -1},
                         {'format' : -1},
                         {'format' : -1},
                         #63
                         {'format' : 3, 'sfn' : 'any', 'sfNum' : (9,)}]
        
        if _prachConfFdd[self.prachConfInd]['format'] < 0:
            self.ngwin.logEdit.append('args error: invalid PRACH configuration index: %d. PRACH index 30/46/60/61/62 are not supported in FDD.' % self.prachConfInd)
            return False
        self.prachFddFormat = _prachConfFdd[self.prachConfInd]['format']
        self.prachFddSfn = _prachConfFdd[self.prachConfInd]['sfn']
        self.prachFddSubf = _prachConfFdd[self.prachConfInd]['subf']
        return True
    
    def initPrachTdd(self):
        #Table 5.7.1-3: Frame structure type 2 random access configurations for preamble formats 0-4.
        if self.prachConfInd in range(20):
            self.prachTddFormat = 0
        elif self.prachConfInd in range(20, 30):
            self.prachTddFormat = 1
        elif self.prachConfInd in range(39, 40):
            self.prachTddFormat = 2
        elif self.prachConfInd in range(40, 48):
            self.prachTddFormat = 3
        elif self.prachConfInd in range(48, 58):
            self.prachTddFormat = 4
        else:
            self.ngwin.logEdit.append('args error: PRACH configuration index 58~63 are not supported for frame structure type 2.')
            return False
        
        #Table 5.7.1-4: Frame structure type 2 random access preamble mapping in time and frequency.
        _prachQuadTdd = [[[(0,1,0,2)], [(0,1,0,1)], [(0,1,0,0)], [(0,1,0,2)], [(0,1,0,1)], [(0,1,0,0)], [(0,1,0,2)]],
                  #1
                  [[(0,2,0,2)], [(0,2,0,1)], [(0,2,0,0)], [(0,2,0,2)], [(0,2,0,1)], [(0,2,0,0)], [(0,2,0,2)]],
                  #2
                  [[(0,1,1,2)], [(0,1,1,1)], [(0,1,1,0)], [(0,1,0,1)], [(0,1,0,0)], None, [(0,1,1,1)]],
                  #3
                  [[(0,0,0,2)], [(0,0,0,1)], [(0,0,0,0)], [(0,0,0,2)], [(0,0,0,1)], [(0,0,0,0)], [(0,0,0,2)]],
                  #4
                  [[(0,0,1,2)], [(0,0,1,1)], [(0,0,1,0)], [(0,0,0,1)], [(0,0,0,0)], None, [(0,0,1,1)]],
                  #5
                  [[(0,0,0,1)], [(0,0,0,0)], None, [(0,0,0,0)], None, None, [(0,0,0,1)]],
                  #6
                  [[(0,0,0,2),(0,0,1,2)], [(0,0,0,1),(0,0,1,1)], [(0,0,0,0),(0,0,1,0)], [(0,0,0,1),(0,0,0,2)], [(0,0,0,0),(0,0,0,1)], [(0,0,0,0),(1,0,0,0)], [(0,0,0,2),(0,0,1,1)]],
                  #7
                  [[(0,0,0,1),(0,0,1,1)], [(0,0,0,0),(0,0,1,0)], None, [(0,0,0,0),(0,0,0,2)], None, None, [(0,0,0,1),(0,0,1,0)]],
                  #8
                  [[(0,0,0,0),(0,0,1,0)], None, None, [(0,0,0,0),(0,0,0,1)], None, None, [(0,0,0,0),(0,0,1,1)]],
                  #9
                  [[(0,0,0,1),(0,0,0,2),(0,0,1,2)], [(0,0,0,0),(0,0,0,1),(0,0,1,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0)], [(0,0,0,0),(0,0,0,1),(0,0,0,2)], [(0,0,0,0),(0,0,0,1),(1,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0)], [(0,0,0,1),(0,0,0,2),(0,0,1,1)]],
                  #10
                  [[(0,0,0,0),(0,0,1,0),(0,0,1,1)], [(0,0,0,1),(0,0,1,0),(0,0,1,1)], [(0,0,0,0),(0,0,1,0),(1,0,1,0)], None, [(0,0,0,0),(0,0,0,1),(1,0,0,0)], None, [(0,0,0,0),(0,0,0,2),(0,0,1,0)]],
                  #11
                  [None, [(0,0,0,0),(0,0,0,1),(0,0,1,0)], None, None, None, None, [(0,0,0,1),(0,0,1,0),(0,0,1,1)]],
                  #12
                  [[(0,0,0,1),(0,0,0,2),(0,0,1,1),(0,0,1,2)], [(0,0,0,0),(0,0,0,1),(0,0,1,0),(0,0,1,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0)], [(0,0,0,0),(0,0,0,1),(0,0,0,2),(1,0,0,2)], [(0,0,0,0),(0,0,0,1),(1,0,0,0),(1,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0)], [(0,0,0,1),(0,0,0,2),(0,0,1,0),(0,0,1,1)]],
                  #13
                  [[(0,0,0,0),(0,0,0,2),(0,0,1,0),(0,0,1,2)], None, None, [(0,0,0,0),(0,0,0,1),(0,0,0,2),(1,0,0,1)], None, None, [(0,0,0,0),(0,0,0,1),(0,0,0,2),(0,0,1,1)]],
                  #14
                  [[(0,0,0,0),(0,0,0,1),(0,0,1,0),(0,0,1,1)], None, None, [(0,0,0,0),(0,0,0,1),(0,0,0,2),(1,0,0,0)], None, None, [(0,0,0,0),(0,0,0,2),(0,0,1,0),(0,0,1,1)]],
                  #15
                  [[(0,0,0,0),(0,0,0,1),(0,0,0,2),(0,0,1,1),(0,0,1,2)], [(0,0,0,0),(0,0,0,1),(0,0,1,0),(0,0,1,1),(1,0,0,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0)], [(0,0,0,0),(0,0,0,1),(0,0,0,2),(1,0,0,1),(1,0,0,2)], [(0,0,0,0),(0,0,0,1),(0,0,0,2),(1,0,0,1),(2,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0)], [(0,0,0,0),(0,0,0,1),(0,0,0,2),(0,0,1,0),(0,0,1,1)]],
                  #16
                  [[(0,0,0,1),(0,0,0,2),(0,0,1,0),(0,0,1,1),(0,0,1,2)], [(0,0,0,0),(0,0,0,1),(0,0,1,0),(0,0,1,1),(1,0,1,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,1,0)], [(0,0,0,0),(0,0,0,1),(0,0,0,2),(1,0,0,0),(1,0,0,2)], [(0,0,0,0),(0,0,0,1),(1,0,0,0),(1,0,0,1),(2,0,0,0)], None, None],
                  #17
                  [[(0,0,0,0),(0,0,0,1),(0,0,0,2),(0,0,1,0),(0,0,1,2)], [(0,0,0,0),(0,0,0,1),(0,0,1,0),(0,0,1,1),(1,0,0,0)], None, [(0,0,0,0),(0,0,0,1),(0,0,0,2),(1,0,0,0),(1,0,0,1)], None, None, None],
                  #18
                  [[(0,0,0,0),(0,0,0,1),(0,0,0,2),(0,0,1,0),(0,0,1,1),(0,0,1,2)], [(0,0,0,0),(0,0,0,1),(0,0,1,0),(0,0,1,1),(1,0,0,1),(1,0,1,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0),(2,0,1,0)], [(0,0,0,0),(0,0,0,1),(0,0,0,2),(1,0,0,0),(1,0,0,1),(1,0,0,2)], [(0,0,0,0),(0,0,0,1),(1,0,0,0),(1,0,0,1),(2,0,0,0),(2,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0),(5,0,0,0)], [(0,0,0,0),(0,0,0,1),(0,0,0,2),(0,0,1,0),(0,0,1,1),(1,0,0,2)]],
                  #19
                  [None, [(0,0,0,0),(0,0,0,1),(0,0,1,0),(0,0,1,1),(1,0,0,0),(1,0,1,0)], None, None, None, None, [(0,0,0,0),(0,0,0,1),(0,0,0,2),(0,0,1,0),(0,0,1,1),(1,0,1,1)]],
                  #20
                  [[(0,1,0,1)], [(0,1,0,0)], None, [(0,1,0,1)], [(0,1,0,0)], None, [(0,1,0,1)]],
                  #21
                  [[(0,2,0,1)], [(0,2,0,0)], None, [(0,2,0,1)], [(0,2,0,0)], None, [(0,2,0,1)]],
                  #22
                  [[(0,1,1,1)], [(0,1,1,0)], None, None, None, None, [(0,1,1,0)]],
                  #23
                  [[(0,0,0,1)], [(0,0,0,0)], None, [(0,0,0,1)], [(0,0,0,0)], None, [(0,0,0,1)]],
                  #24
                  [[(0,0,1,1)], [(0,0,1,0)], None, None, None, None, [(0,0,1,0)]],
                  #25
                  [[(0,0,0,1),(0,0,1,1)], [(0,0,0,0),(0,0,1,0)], None, [(0,0,0,1),(1,0,0,1)], [(0,0,0,0),(1,0,0,0)], None, [(0,0,0,1),(0,0,1,0)]],
                  #26
                  [[(0,0,0,1),(0,0,1,1),(1,0,0,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0)], None, [(0,0,0,1),(1,0,0,1),(2,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0)], None, [(0,0,0,1),(0,0,1,0),(1,0,0,1)]],
                  #27
                  [[(0,0,0,1),(0,0,1,1),(1,0,0,1),(1,0,1,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0)], None, [(0,0,0,1),(1,0,0,1),(2,0,0,1),(3,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0)], None, [(0,0,0,1),(0,0,1,0),(1,0,0,1),(1,0,1,0)]],
                  #28
                  [[(0,0,0,1),(0,0,1,1),(1,0,0,1),(1,0,1,1),(2,0,0,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0)], None, [(0,0,0,1),(1,0,0,1),(2,0,0,1),(3,0,0,1),(4,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0)], None, [(0,0,0,1),(0,0,1,0),(1,0,0,1),(1,0,1,0),(2,0,0,1)]],
                  #29
                  [[(0,0,0,1),(0,0,1,1),(1,0,0,1),(1,0,1,1),(2,0,0,1),(2,0,1,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0),(2,0,1,0)], None, [(0,0,0,1),(1,0,0,1),(2,0,0,1),(3,0,0,1),(4,0,0,1),(5,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0),(5,0,0,0)], None, [(0,0,0,1),(0,0,1,0),(1,0,0,1),(1,0,1,0),(2,0,0,1),(2,0,1,0)]],
                  #30
                  [[(0,1,0,1)], [(0,1,0,0)], None, [(0,1,0,1)], [(0,1,0,0)], None, [(0,1,0,1)]],
                  #31
                  [[(0,2,0,1)], [(0,2,0,0)], None, [(0,2,0,1)], [(0,2,0,0)], None, [(0,2,0,1)]],
                  #32
                  [[(0,1,1,1)], [(0,1,1,0)], None, None, None, None, [(0,1,1,0)]],
                  #33
                  [[(0,0,0,1)], [(0,0,0,0)], None, [(0,0,0,1)], [(0,0,0,0)], None, [(0,0,0,1)]],
                  #34
                  [[(0,0,1,1)], [(0,0,1,0)], None, None, None, None, [(0,0,1,0)]],
                  #35
                  [[(0,0,0,1),(0,0,1,1)], [(0,0,0,0),(0,0,1,0)], None, [(0,0,0,1),(1,0,0,1)], [(0,0,0,0),(1,0,0,0)], None, [(0,0,0,1),(0,0,1,0)]],
                  #36
                  [[(0,0,0,1),(0,0,1,1),(1,0,0,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0)], None, [(0,0,0,1),(1,0,0,1),(2,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0)], None, [(0,0,0,1),(0,0,1,0),(1,0,0,1)]],
                  #37
                  [[(0,0,0,1),(0,0,1,1),(1,0,0,1),(1,0,1,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0)], None, [(0,0,0,1),(1,0,0,1),(2,0,0,1),(3,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0)], None, [(0,0,0,1),(0,0,1,0),(1,0,0,1),(1,0,1,0)]],
                  #38
                  [[(0,0,0,1),(0,0,1,1),(1,0,0,1),(1,0,1,1),(2,0,0,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0)], None, [(0,0,0,1),(1,0,0,1),(2,0,0,1),(3,0,0,1),(4,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0)], None, [(0,0,0,1),(0,0,1,0),(1,0,0,1),(1,0,1,0),(2,0,0,1)]],
                  #39
                  [[(0,0,0,1),(0,0,1,1),(1,0,0,1),(1,0,1,1),(2,0,0,1),(2,0,1,1)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0),(2,0,1,0)], None, [(0,0,0,1),(1,0,0,1),(2,0,0,1),(3,0,0,1),(4,0,0,1),(5,0,0,1)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0),(5,0,0,0)], None, [(0,0,0,1),(0,0,1,0),(1,0,0,1),(1,0,1,0),(2,0,0,1),(2,0,1,0)]],
                  #40
                  [[(0,1,0,0)], None, None, [(0,1,0,0)], None, None, [(0,1,0,0)]],
                  #41
                  [[(0,2,0,0)], None, None, [(0,2,0,0)], None, None, [(0,2,0,0)]],
                  #42
                  [[(0,1,1,0)], None, None, None, None, None, None],
                  #43
                  [[(0,0,0,0)], None, None, [(0,0,0,0)], None, None, [(0,0,0,0)]],
                  #44
                  [[(0,0,1,0)], None, None, None, None, None, None],
                  #45
                  [[(0,0,0,0),(0,0,1,0)], None, None, [(0,0,0,0),(1,0,0,0)], None, None, [(0,0,0,0),(1,0,0,0)]],
                  #46
                  [[(0,0,0,0),(0,0,1,0),(1,0,0,0)], None, None, [(0,0,0,0),(1,0,0,0),(2,0,0,0)], None, None, [(0,0,0,0),(1,0,0,0),(2,0,0,0)]],
                  #47
                  [[(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0)], None, None, [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0)], None, None, [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0)]],
                  #48
                  [[(0,1,0,0)], [(0,1,0,0)], [(0,1,0,0)], [(0,1,0,0)], [(0,1,0,0)], [(0,1,0,0)], [(0,1,0,0)]],
                  #49
                  [[(0,2,0,0)], [(0,2,0,0)], [(0,2,0,0)], [(0,2,0,0)], [(0,2,0,0)], [(0,2,0,0)], [(0,2,0,0)]],
                  #50
                  [[(0,1,1,0)], [(0,1,1,0)], [(0,1,1,0)], None, None, None, [(0,1,1,0)]],
                  #51
                  [[(0,0,0,0)], [(0,0,0,0)], [(0,0,0,0)], [(0,0,0,0)], [(0,0,0,0)], [(0,0,0,0)], [(0,0,0,0)]],
                  #52
                  [[(0,0,1,0)], [(0,0,1,0)], [(0,0,1,0)], None, None, None, [(0,0,1,0)]],
                  #53
                  [[(0,0,0,0),(0,0,1,0)], [(0,0,0,0),(0,0,1,0)], [(0,0,0,0),(0,0,1,0)], [(0,0,0,0),(1,0,0,0)], [(0,0,0,0),(1,0,0,0)], [(0,0,0,0),(1,0,0,0)], [(0,0,0,0),(0,0,1,0)]],
                  #54
                  [[(0,0,0,0),(0,0,1,0),(1,0,0,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0)]],
                  #55
                  [[(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0)]],
                  #56
                  [[(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0)]],
                  #57
                  [[(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0),(2,0,1,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0),(2,0,1,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0),(2,0,1,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0),(5,0,0,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0),(5,0,0,0)], [(0,0,0,0),(1,0,0,0),(2,0,0,0),(3,0,0,0),(4,0,0,0),(5,0,0,0)], [(0,0,0,0),(0,0,1,0),(1,0,0,0),(1,0,1,0),(2,0,0,0),(2,0,1,0)]],
                  #58~63 is not supported
                  [None, None, None, None, None, None, None],
                  [None, None, None, None, None, None, None],
                  [None, None, None, None, None, None, None],
                  [None, None, None, None, None, None, None],
                  [None, None, None, None, None, None, None],
                  [None, None, None, None, None, None, None]
                  ]
        
        self.prachTddQuad = _prachQuadTdd[self.prachConfInd][self.sa]
        if self.prachTddQuad is None:
            self.ngwin.logEdit.append('args error: invalid PRACH configuration index %d for UL/DL configuration %d' % (self.prachConfInd, self.sa))
            return False
        
        return True
        
    def initSrsFdd(self):
        #Table 5.5.3.3-1: Frame structure type 1 sounding reference signal subframe configuration.
        _srsSubfConfFdd = [{'tSfc' : 1, 'deltaSfc' : (0,)},
                       {'tSfc' : 2, 'deltaSfc' : (0,)},
                       {'tSfc' : 2, 'deltaSfc' : (1,)},
                       {'tSfc' : 5, 'deltaSfc' : (0,)},
                       {'tSfc' : 5, 'deltaSfc' : (1,)},
                       {'tSfc' : 5, 'deltaSfc' : (2,)},
                       {'tSfc' : 5, 'deltaSfc' : (3,)},
                       {'tSfc' : 5, 'deltaSfc' : (0,1)},
                       {'tSfc' : 5, 'deltaSfc' : (2,3)},
                       {'tSfc' : 10, 'deltaSfc' : (0,)},
                       {'tSfc' : 10, 'deltaSfc' : (1,)},
                       {'tSfc' : 10, 'deltaSfc' : (2,)},
                       {'tSfc' : 10, 'deltaSfc' : (3,)},
                       {'tSfc' : 10, 'deltaSfc' : (0,1,2,3,4,6,8)},
                       {'tSfc' : 10, 'deltaSfc' : (0,1,2,3,4,5,6,8)},
                       #15 is invalid
                       None
                       ]
        
        if self.srsSubfConf < 0 or self.srsSubfConf > 14:
            self.ngwin.logEdit.append('args error: valid SRS subframe configuration for FDD is [0, 14].')
            return False
        self.tSfc = _srsSubfConfFdd[self.srsSubfConf]['tSfc']
        self.deltaSfc = _srsSubfConfFdd[self.srsSubfConf]['deltaSfc']
        return True
    
    def initSrsTdd(self):
        #Table 5.5.3.3-2: Frame structure type 2 sounding reference signal subframe configuration.
        _srsSubfConfTdd = [{'tSfc' : 5, 'deltaSfc' : (1,)},
                       {'tSfc' : 5, 'deltaSfc' : (1,2)},
                       {'tSfc' : 5, 'deltaSfc' : (1,3)},
                       {'tSfc' : 5, 'deltaSfc' : (1,4)},
                       {'tSfc' : 5, 'deltaSfc' : (1,2,3)},
                       {'tSfc' : 5, 'deltaSfc' : (1,2,4)},
                       {'tSfc' : 5, 'deltaSfc' : (1,3,4)},
                       {'tSfc' : 5, 'deltaSfc' : (1,2,3,4)},
                       {'tSfc' : 10, 'deltaSfc' : (1,2,6)},
                       {'tSfc' : 10, 'deltaSfc' : (1,3,6)},
                       {'tSfc' : 10, 'deltaSfc' : (1,6,7)},
                       {'tSfc' : 10, 'deltaSfc' : (1,2,6,8)},
                       {'tSfc' : 10, 'deltaSfc' : (1,3,6,9)},
                       {'tSfc' : 10, 'deltaSfc' : (1,4,6,7)},
                       #14~15 are invalid
                       None,
                       None
                       ]
        if self.srsSubfConf < 0 or self.srsSubfConf > 13:
            self.ngwin.logEdit.append('args error: valid SRS subframe configuration for TDD is [0, 13].')
            return False
        self.tSfc = _srsSubfConfTdd[self.srsSubfConf]['tSfc']
        self.deltaSfc = _srsSubfConfTdd[self.srsSubfConf]['deltaSfc']
        return True
    
    def fillCrs(self):
        if self.crsOk:
            return
        #6.10.1.2	Mapping to resource elements
        '''
        iap,l,v,k,special case
        0,0,0,6*im+(v+v_shift)%6,no
        0,symbPerSlot-3,3,same,no
        1,0,3,same,no
        1,symbPerSlot-3,0,same,no
        2,1,0,same,no
        2,1,3,same,no
        3,1,3,same,no
        3,1,6,same,no
        '''
        _crsPos = [(0, 0, 0),
                   (0, self.symbPerSlot-3, 3),
                   (1, 0, 3),
                   (1, self.symbPerSlot-3, 0),
                   (2, 1, 0),
                   (2, 1, 3),
                   (3, 1, 3),
                   (3, 1, 6)]
        if self.apNum == 1:
            _crsPos = _crsPos[:2]
        elif self.apNum == 2:
            _crsPos = _crsPos[:4]
            
        m = list(range(2*self.prbNum))
        vShift = self.pci % 6
        
        for ap, l, v in _crsPos:
            k = list(map(lambda x : 6*x+(v+vShift)%6, m))
            
            if ap in [0, 1]:
                symb = [isf*self.symbPerSubf+l for isf in range(self.subfPerRf)] + [isf*self.symbPerSubf+self.symbPerSlot+l for isf in range(self.subfPerRf)]
            elif (ap == 2 and v == 0) or (ap == 3 and v == 3):
                symb = [isf*self.symbPerSubf+l for isf in range(self.subfPerRf)]
            else: #(ap == 2 and v == 3) or (ap == 3 and v == 6)
                symb = [isf*self.symbPerSubf+self.symbPerSlot+l for isf in range(self.subfPerRf)]
            
            for _k in k:
                for _symb in symb:
                    if self.gridDl[ap][_k][_symb] == LteResType.LTE_RES_PDSCH.value:
                        self.gridDl[ap][_k][_symb] = LteResType.LTE_RES_CRS.value
            
            for _ap in range(self.apNum):
                if _ap != ap:
                    for _k in k:
                        for _symb in symb:
                            if self.gridDl[_ap][_k][_symb] == LteResType.LTE_RES_PDSCH.value:
                                self.gridDl[_ap][_k][_symb] = LteResType.LTE_RES_DTX.value
        
        #in case of the first ofdm symbol with one antenna port, CRS is mapped as if two CRS are exist, as specified in 3GPP 36.211 6.2.4.
        if self.apNum == 1:
            ap, l, v = [0, 0, 3]
            k = list(map(lambda x : 6*x+(v+vShift)%6, m))
            symb = [isf*self.symbPerSubf+l for isf in range(self.subfPerRf)]
            for _k in k:
                for _symb in symb:
                    if self.gridDl[ap][_k][_symb] == LteResType.LTE_RES_PDSCH.value:
                        self.gridDl[ap][_k][_symb] = LteResType.LTE_RES_DTX.value
            
        self.crsOk= True
            
    def fillPbch(self):
        if not self.crsOk:
            self.ngwin.logEdit.append('NgLteGrid.fillCrs must be called before NgLteGrid.fillPbch.')
            return
        #BUGFIX: according to 36.211
        #The mapping operation shall assume cell-specific reference signals for antenna ports 0-3 being present irrespective of the actual configuration.
        #The UE shall assume that the resource elements assumed to be reserved for reference signals in the mapping operation above but not used for transmission of reference signal are not available for PDSCH transmission.
        gridDlTmp = np.full((4, self.rePerSymb, self.symbPerRf), LteResType.LTE_RES_PDSCH.value)
        _crsPos = [(0, 0, 0),
                   (0, self.symbPerSlot-3, 3),
                   (1, 0, 3),
                   (1, self.symbPerSlot-3, 0),
                   (2, 1, 0),
                   (2, 1, 3),
                   (3, 1, 3),
                   (3, 1, 6)]
            
        m = list(range(2*self.prbNum))
        vShift = self.pci % 6
        
        for ap, l, v in _crsPos:
            k = list(map(lambda x : 6*x+(v+vShift)%6, m))
            
            if ap in [0, 1]:
                symb = [isf*self.symbPerSubf+l for isf in range(self.subfPerRf)] + [isf*self.symbPerSubf+self.symbPerSlot+l for isf in range(self.subfPerRf)]
            elif (ap == 2 and v == 0) or (ap == 3 and v == 3):
                symb = [isf*self.symbPerSubf+l for isf in range(self.subfPerRf)]
            else: #(ap == 2 and v == 3) or (ap == 3 and v == 6)
                symb = [isf*self.symbPerSubf+self.symbPerSlot+l for isf in range(self.subfPerRf)]
            
            for _k in k:
                for _symb in symb:
                    if gridDlTmp[ap][_k][_symb] == LteResType.LTE_RES_PDSCH.value:
                        gridDlTmp[ap][_k][_symb] = LteResType.LTE_RES_CRS.value
            
            for _ap in range(self.apNum):
                if _ap != ap:
                    for _k in k:
                        for _symb in symb:
                            if gridDlTmp[_ap][_k][_symb] == LteResType.LTE_RES_PDSCH.value:
                                gridDlTmp[_ap][_k][_symb] = LteResType.LTE_RES_DTX.value
        
        reNumPbch = 72
        symbNumPbch = 4
        startRePbch = self.rePerSymb // 2 - 36
        for iap in range(self.apNum):
            for isym in range(symbNumPbch):
                for ire in range(reNumPbch):
                    if gridDlTmp[iap][startRePbch+ire][self.symbPerSlot+isym] != LteResType.LTE_RES_CRS.value and gridDlTmp[iap][startRePbch+ire][self.symbPerSlot+isym] != LteResType.LTE_RES_DTX.value:
                        self.gridDl[iap][startRePbch+ire][self.symbPerSlot+isym] = LteResType.LTE_RES_PBCH.value
                    elif self.gridDl[iap][startRePbch+ire][self.symbPerSlot+isym] == LteResType.LTE_RES_PDSCH.value:
                        self.gridDl[iap][startRePbch+ire][self.symbPerSlot+isym] = LteResType.LTE_RES_DTX.value
    
    def fillSch(self):
        #assume that P-SCH and S-SCH is transmitted on all antenna port
        ns = [i-5 for i in range(72)]
        if self.fs == LtePhy.LTE_FS_TYPE1.value:
            slots = [1, 10]
            for iap in range(self.apNum):
                for slot in slots:
                    for n in ns:
                        k = n - 31 + self.rePerSymb // 2
                        if n <= -1 or n >= 62:
                            self.gridDl[iap][k][slot*self.symbPerSlot+(self.symbPerSlot-1)] = LteResType.LTE_RES_DTX.value
                            self.gridDl[iap][k][slot*self.symbPerSlot+(self.symbPerSlot-2)] = LteResType.LTE_RES_DTX.value
                        else:
                            self.gridDl[iap][k][slot*self.symbPerSlot+(self.symbPerSlot-1)] = LteResType.LTE_RES_PSCH.value
                            self.gridDl[iap][k][slot*self.symbPerSlot+(self.symbPerSlot-2)] = LteResType.LTE_RES_SSCH.value
        else:
            #P-SCH
            sfs = [1, 6]
            for iap in range(self.apNum):
                for sf in sfs:
                    for n in ns:
                        k = n - 31 + self.rePerSymb // 2
                        if n <= -1 or n >= 62:
                            self.gridDl[iap][k][sf*self.symbPerSubf+2] = LteResType.LTE_RES_DTX.value
                        else:
                            self.gridDl[iap][k][sf*self.symbPerSubf+2] = LteResType.LTE_RES_PSCH.value
            
            #S-SCH
            slots = [1, 11]
            for iap in range(self.apNum):
                for slot in slots:
                    for n in ns:
                        k = n - 31 + self.rePerSymb // 2
                        if n <= -1 or n >= 62:
                            self.gridDl[iap][k][slot*self.symbPerSlot+(self.symbPerSlot-1)] = LteResType.LTE_RES_DTX.value
                        else:
                            self.gridDl[iap][k][slot*self.symbPerSlot+(self.symbPerSlot-1)] = LteResType.LTE_RES_SSCH.value
            
    
    def fillPdcch(self):
        if not self.pcfichOk:
            self.fillPcfich()
        if not self.phichOk:
            self.fillPhich()
            
        if self.fs == LtePhy.LTE_FS_TYPE1.value:
            L = [self.cfi] * self.subfPerRf
        else:
            L = [0] * self.subfPerRf
            for isf in range(self.subfPerRf):
                if self.subfPatTdd[isf] == 'd':
                    L[isf] = self.cfi
                elif self.subfPatTdd[isf] == 's':
                    L[isf] = self.cfiSsf
        
        for isf in range(self.subfPerRf):
            if L[isf] == 0:
                continue
            
            reg = []
            for isym in range(L[isf]):
                if isym == 0 or (isym == 1 and self.apNum == 4) or (isym == 3 and self.cp == LtePhy.LTE_CP_EXTENDED.value):
                    numReg = 2  #two REGs
                else:
                    numReg = 3  #three REGs
                sizeReg = self.scPerPrb // numReg
                
                used = [False] * (numReg*self.prbNum)
                for ireg in range(numReg*self.prbNum):
                    for ire in [sizeReg*ireg+i for i in range(sizeReg)]:
                        if self.gridDl[0][ire][isf*self.symbPerSubf+isym] == LteResType.LTE_RES_PCFICH.value or self.gridDl[0][ire][isf*self.symbPerSubf+isym] == LteResType.LTE_RES_PHICH.value:
                            used[ireg] = True
                            break
                reg.append(used)
                
                #assume all REGs remained are allocated to PDCCH
                for iap in range(self.apNum):
                    for ireg in range(numReg*self.prbNum):
                        if used[ireg] == False:
                            for ire in [sizeReg*ireg+i for i in range(sizeReg)]:
                                if self.gridDl[iap][ire][isf*self.symbPerSubf+isym] != LteResType.LTE_RES_CRS.value and self.gridDl[iap][ire][isf*self.symbPerSubf+isym] != LteResType.LTE_RES_DTX.value:
                                    self.gridDl[iap][ire][isf*self.symbPerSubf+isym] = LteResType.LTE_RES_PDCCH.value
            
            #REG can be used for other purpose, such as to calculate maximum available CCE number
            _flatten = [x for used in reg for x in used]
            regNum = Counter(_flatten)[False]
            self.cce[isf] = math.floor(regNum / self.regPerCce)
            
        self.ngwin.logEdit.append('CCE statistics:')
        if self.fs == LtePhy.LTE_FS_TYPE1.value:
            for isf in range(self.subfPerRf):
                self.ngwin.logEdit.append('-->CCE number in subframe %d = %d' % (isf, self.cce[isf]))
        else:
            for isf in [_isf for _isf in range(self.subfPerRf) if self.subfPatTdd[_isf] != 'u']:
                self.ngwin.logEdit.append('-->CCE number in subframe %d = %d' % (isf, self.cce[isf]))
    
    def fillPcfich(self):
        if not self.crsOk:
            self.fillCrs()
        if self.pcfichOk:
            return
        
        regNumPcfich = 4
        rePerReg = 6
        kAvg = (self.scPerPrb // 2) * (self.pci % (2 * self.prbNum))
        for iap in range(self.apNum):
            for ireg in range(regNumPcfich):
                k = kAvg + math.floor(ireg * self.prbNum / 2) * (self.scPerPrb // 2)
                k = k % self.rePerSymb
                for ire in range(rePerReg):
                    #In case of one antenna port, a REG in the 1st symbol of a subframe contains 6 REs, make sure use DTX to replace the unused REs which are virtually reserved for CRS. Please refer to 3GPP 36.211 6.2.4.
                    for isf in range(self.subfPerRf):
                        if self.gridDl[iap][k+ire][isf*self.symbPerSubf] == LteResType.LTE_RES_PDSCH.value:
                            self.gridDl[iap][k+ire][isf*self.symbPerSubf] = LteResType.LTE_RES_PCFICH.value
        
        self.pcfichOk = True
    
    def fillPhich(self):
        if not self.pcfichOk:
            self.fillPcfich()
        if self.phichOk:
            return
        
        if self.phichDur == LtePhy.LTE_PHICH_DUR_NORMAL.value:
            phichDur = [1]*self.subfPerRf
        else:
            phichDur = [3]*self.subfPerRf
            if self.fs == LtePhy.LTE_FS_TYPE2.value:
                phichDur[1] = 2
                phichDur[6] = 2
        
        phichRes = [1/6, 1/2, 1, 2][self.phichRes]
        phichGrpNum = [math.ceil(phichRes*self.prbNum/8) if self.cp == LtePhy.LTE_CP_NORMAL.value else 2*math.ceil(phichRes*self.prbNum/8)]*self.subfPerRf
        if self.fs == LtePhy.LTE_FS_TYPE2.value:
            phichGrpNum = list(map(lambda isf:phichGrpNum[isf] if self.subfPatTdd[isf] != 'u' else 0, list(range(self.subfPerRf))))
            
            #Table 6.9-1: The factor mi for frame structure type 2.
            _phichMi = [(2,1,None,None,None,2,1,None,None,None),
                        (0,1,None,None,1,0,1,None,None,1),
                        (0,0,None,1,0,0,0,None,1,0),
                        (1,0,None,None,None,0,0,0,1,1),
                        (0,0,None,None,0,0,0,0,1,1),
                        (0,0,None,0,0,0,0,0,1,0),
                        (1,1,None,None,None,1,1,None,None,1)]
            mi = _phichMi[self.sa]
            phichGrpNum = list(map(lambda isf:mi[isf]*phichGrpNum[isf] if mi[isf] is not None else phichGrpNum[isf], list(range(self.subfPerRf))))
        
        for isf in range(self.subfPerRf):
            if phichGrpNum[isf] == 0:
                continue
            phichMapUnitNum = phichGrpNum[isf] if self.cp == LtePhy.LTE_CP_NORMAL.value else phichGrpNum[isf]//2
            
            for iap in range(self.apNum):
                cchReg = []
                for isym in range(phichDur[isf]):
                    if isym == 0 or (isym == 1 and self.apNum == 4):
                        numReg = 2
                    elif (isym == 1 and (self.apNum == 1 or self.apNum == 2)) or isym == 2:
                        numReg = 3
                    rePerReg = self.scPerPrb//numReg
                    reg = [True]*(numReg*self.prbNum)
                    for ireg in range(numReg*self.prbNum):
                        for ire in range(rePerReg):
                            if self.gridDl[iap][rePerReg*ireg+ire][isym] == LteResType.LTE_RES_PCFICH.value:
                                reg[ireg] = False
                                break
                    regInd = [ireg for ireg in range(numReg*self.prbNum) if reg[ireg] == True]
                    cchReg.append(regInd)
                    
                for imu in range(phichMapUnitNum):
                    for iquad in range(3):
                        if self.phichDur == LtePhy.LTE_PHICH_DUR_NORMAL.value:
                            timel = 0
                        elif self.phichDur == LtePhy.LTE_PHICH_DUR_EXTENDED.value and self.fs == LtePhy.LTE_FS_TYPE2.value and (isf == 1 or isf == 6):
                            timel = (math.floor(imu / 2) + iquad + 1) % 2
                        else:
                            timel = iquad
                            
                        if self.phichDur == LtePhy.LTE_PHICH_DUR_EXTENDED.value and self.fs == LtePhy.LTE_FS_TYPE2.value and (isf == 1 or isf == 6):
                            nl = len(cchReg[timel])
                            freqk = (math.floor(self.pci * nl / len(cchReg[1])) + imu + math.floor(iquad * nl / 3)) % nl
                        else:
                            nl = len(cchReg[timel])
                            freqk = (math.floor(self.pci * nl / len(cchReg[0])) + imu + math.floor(iquad * nl / 3)) % nl
                        
                        if timel == 0 or (timel == 1 and self.apNum == 4):
                            numReg = 2
                        elif (timel == 1 and (self.apNum == 1 or self.apNum == 2)) or timel == 2:
                            numReg = 3
                        rePerReg = self.scPerPrb//numReg
                        
                        for ire in range(rePerReg):
                            if self.gridDl[iap][rePerReg*cchReg[timel][freqk]+ire][isf*self.symbPerSubf+timel] != LteResType.LTE_RES_CRS.value and self.gridDl[iap][rePerReg*cchReg[timel][freqk]+ire][isf*self.symbPerSubf+timel] != LteResType.LTE_RES_DTX.value:
                                self.gridDl[iap][rePerReg*cchReg[timel][freqk]+ire][isf*self.symbPerSubf+timel] = LteResType.LTE_RES_PHICH.value
                            
        self.phichOk = True
    
    def printDl(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        if not os.path.exists(outDir):
            os.mkdir(outDir)
        for iap in range(self.apNum):
            with open(os.path.join(outDir, 'LTE_DL_RES_GRID_AP'+str(iap)+'_'+time.strftime('%Y%m%d%H%M%S', time.localtime())+'.csv'), 'w') as f:
                line = []
                line.append('k/l')
                line.extend([str(k) for i in range(self.subfPerRf) for j in range(self.slotPerSubf) for k in range(self.symbPerSlot)])
                f.write(','.join(line))
                f.write('\n')
                
                for ire in range(self.rePerSymb):
                    line = []
                    line.append(str(ire))
                    line.extend([str(self.gridDl[iap][ire][isf*self.symbPerSubf+isym]) for isf in range(self.subfPerRf) for isym in range(self.symbPerSubf)])
                    f.write(','.join(line))
                    f.write('\n')
    
    def fillPucch(self):
        pass
    
    def fillPrach(self):
        pass
    
    def fillDmrsForPusch(self):
        pass
    
    def fillSrs(self):
        pass
    
    def printUl(self):
        pass
