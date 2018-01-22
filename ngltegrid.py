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

import numpy as np
import ngmainwin
from ngltephy import LtePhy, LteResType

class NgLteGrid(object):
    def __init__(self, ngwin, args):
        self.scPerPrb = 12
        self.slotPerSubf = 2
        self.subfPerRf = 10
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
        _sspmap_norm = {0 : (3, 10, 1),
                   1 : (9, 4, 1),
                   2 : (10, 3, 1),
                   3 : (11, 2, 1),
                   4 : (12, 1, 1),
                   5 : (3, 9, 2),
                   6 : (9, 3, 2),
                   7 : (10, 2, 2),
                   8 : (11, 1, 2)}
        _sspmap_ext = {0 : (3, 8, 1),
                       1 : (8, 3, 1),
                       2 : (9, 2, 1),
                       3 : (10, 1, 1),
                       4 : (3, 7, 2),
                       5 : (8, 2, 2),
                       6 : (9, 1, 2)}
        if self.cp == LtePhy.LTE_CP_NORMAL.value:
            self.dwpts, self.gp, self.uppts = _sspmap_norm[self.ssp]
        else:
            if self.ssp >= 7:
                self.ngwin.logEdit.append('args error: SSP 7/8 can only be used for normal CP.')
                return
            else:
                self.dwpts, self.gp, self.uppts = _sspmap_ext[self.ssp]
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
        self.rePerSymb = self.prbNum * self.scPerPrb
        self.rePerSlot = self.rePerSymb * self.symbPerSlot
        self.rePerSubf = self.rePerSlot * self.slotPerSubf
        self.rePerRf = self.rePerSubf * self.subfPerRf
        
        _apmap = (1, 2, 4)
        self.apNum = _apmap[self.ap]
        
        self.gridDl = np.zeros((self.apNum, self.rePerRf))
        self.gridDl += LteResType.LTE_RES_PDSCH.value 
        self.gridUl = np.zeros((1, self.rePerRf))
        self.gridUl += LteResType.LTE_RES_PUSCH.value
        if self.ngwin.enableDebug:
            self.ngwin.logEdit.append('NgLteGrid.gridDl info: ndim=%s, shape=%s, dtype=%s' % (str(self.gridDl.ndim), str(self.gridDl.shape), str(self.gridDl.dtype)))
            self.ngwin.logEdit.append('NgLteGrid.gridUl info: ndim=%s, shape=%s, dtype=%s' % (str(self.gridUl.ndim), str(self.gridUl.shape), str(self.gridUl.dtype)))
            
        _tddconf = [{'name' : 'sa0', 'pat' : 'dsuuudsuuu', 'ack' : {2 : (6,), 4 : (4,), 7 : (6,), 9 : (4,)}},
                    {'name' : 'sa1', 'pat' : 'dsuuddsuud', 'ack' : {2 : (7, 6), 3 : (4,), 7 : (7, 6), 8 : (4,)}},
                    {'name' : 'sa2', 'pat' : 'dsudddsudd', 'ack': {2 : (8, 7, 4, 6), 7 : (8, 7, 4, 6)}}, 
                    {'name' : 'sa3', 'pat' : 'dsuuudsddd', 'ack': {2 : (7, 6, 11), 3 : (6, 5), 4: (5, 4)}},
                    {'name' : 'sa4', 'pat' : 'dsuudddddd', 'ack' : {2 : (12, 8, 7, 11), 3 : (6, 5, 4, 7)}},
                    {'name' : 'sa5', 'pat' : 'dsuddddddd', 'ack' : {2 : (13, 12, 9, 8, 7, 5, 4, 11, 6)}},
                    {'name' : 'sa6', 'pat' : 'dsuuudsuud', 'ack' : {2 : (7,), 3 : (7,), 4 : (5,), 7 : (7,), 8 : (7,)}}]
        self.subfPatTdd = _tddconf[self.sa]['pat']
        self.ackIndTdd = _tddconf[self.sa]['ack']
        self.cce = np.zeros(self.subfPerRf)
        self.maxPucch = np.zeros(self.subfPerRf)
        
        if self.fs == LtePhy.LTE_FS_TYPE2.value:
            for isf in range(self.subfPerRf):
                if self.subfPatTdd[isf] == 'u':
                    for iap in range(self.apNum):
                        for ire in range(self.rePerSubf):
                            self.gridDl[iap][isf * self.rePerSubf + ire] = LteResType.LTE_RES_UL.value
                elif self.subfPatTdd[isf] == 's':
                    for iap in range(self.apNum):
                        for isymb in range(self.dwpts, self.symbPerSubf):
                            for ire in range(self.rePerSymb):
                                self.gridDl[iap][isf * self.rePerSubf + isymb * self.rePerSymb + ire] = LteResType.LTE_RES_GP.value if isymb < self.dwpts + self.gp else LteResType.LTE_RES_UL.value
                    for isymb in range(self.dwpts + self.gp):
                        for ire in range(self.rePerSymb):
                            self.gridUl[0][isf * self.rePerSubf + isymb * self.rePerSymb + ire] = LteResType.LTE_RES_DL.value  if isymb < self.dwpts else LteResType.LTE_RES_GP.value
                else:
                    for ire in range(self.rePerSubf):
                        self.gridUl[0][isf * self.rePerSubf + ire] = LteResType.LTE_RES_DL.value
        
        if self.fs == LtePhy.LTE_FS_TYPE1.value:
            self.initPrachFdd()
            self.initSrsFdd()
        else:
            self.initPrachTdd()
            self.initSrsTdd()
        
        self.crsOk= False
        self.pcfichOk= False
        self.phichOk= False
        self.pucchOk = False
        self.prachOk = False
        
        self.isOk = True
        
    def initPrachFdd(self):
        _prachconffdd = [{'id' : 0, 'format' : 0, 'sfn' : 'even', 'subf' : (1,)}, 
                         {'id' : 1, 'format' : 0, 'sfn' : 'even', 'subf' : (4,)},
                         {'id' : 2, 'format' : 0, 'sfn' : 'even', 'subf' : (7,)}, 
                         {'id' : 3, 'format' : 0, 'sfn' : 'any', 'subf' : (1,)}, 
                         {'id' : 4, 'format' : 0, 'sfn' : 'any', 'subf' : (4,)}, 
                         {'id' : 5, 'format' : 0, 'sfn' : 'any', 'subf' : (7,)}, 
                         {'id' : 6, 'format' : 0, 'sfn' : 'any', 'subf' : (1, 6)}, 
                         {'id' : 7, 'format' : 0, 'sfn' : 'any', 'subf' : (2, 7)},
                         {'id' : 8, 'format' : 0, 'sfn' : 'any', 'subf' : (3, 8)}, 
                         {'id' : 9, 'format' : 0, 'sfn' : 'any', 'subf' : (1, 4, 7)}, 
                         {'id' : 10, 'format' : 0, 'sfn' : 'any', 'subf' : (2, 5, 8)}, 
                         {'id' : 11, 'format' : 0, 'sfn' : 'any', 'subf' : (3, 6, 9)}, 
                         {'id' : 12, 'format' : 0, 'sfn' : 'any', 'subf' : (0, 2, 4, 6, 8)}, 
                         {'id' : 13, 'format' : 0, 'sfn' : 'any', 'subf' : (1, 3, 5, 7, 9)}, 
                         {'id' : 14, 'format' : 0, 'sfn' : 'any', 'subf' : (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)}, 
                         {'id' : 15, 'format' : 0, 'sfn' : 'even', 'subf' : (9,)}, 
                         {'id' : 16, 'format' : 1, 'sfn' : 'even', 'subf' : (1,)}, 
                         {'id' : 17, 'format' : 1, 'sfn' : 'even', 'subf' : (4,)}, 
                         {'id' : 18, 'format' : 1, 'sfn' : 'even', 'subf' : (7,)}, 
                         {'id' : 19, 'format' : 1, 'sfn' : 'any', 'subf' : (1,)}, 
                         {'id' : 20, 'format' : 1, 'sfn' : 'any', 'subf' : (4,)}, 
                         {'id' : 21, 'format' : 1, 'sfn' : 'any', 'subf' : (7,)}, 
                         {'id' : 22, 'format' : 1, 'sfn' : 'any', 'subf' : (1, 6)}, 
                         {'id' : 23, 'format' : 1, 'sfn' : 'any', 'subf' : (2, 7)},
                         {'id' : 24, 'format' : 1, 'sfn' : 'any', 'subf' : (3, 8)}, 
                         {'id' : 25, 'format' : 1, 'sfn' : 'any', 'subf' : (1, 4, 7)}, 
                         {'id' : 26, 'format' : 1, 'sfn' : 'any', 'subf' : (2, 5, 8)}, 
                         {'id' : 27, 'format' : 1, 'sfn' : 'any', 'subf' : (3, 6, 9)}, 
                         {'id' : 28, 'format' : 1, 'sfn' : 'any', 'subf' : (0, 2, 4, 6, 8)}, 
                         {'id' : 29, 'format' : 1, 'sfn' : 'any', 'subf' : (1, 3, 5, 7, 9)}, 
                         #invalid config index = 30
                         {'id' : 30, 'format' : -1},
                         {'id' : 31, 'format' : 1, 'sfn' : 'any', 'subf' : (9,)}, 
                         {'id' : 32, 'format' : 2, 'sfn' : 'even', 'subf' : (1,)}, 
                         {'id' : 33, 'format' : 2, 'sfn' : 'even', 'subf' : (4,)}, 
                         {'id' : 34, 'format' : 2, 'sfn' : 'even', 'subf' : (7,)}, 
                         {'id' : 35, 'format' : 2, 'sfn' : 'any', 'subf' : (1,)}, 
                         {'id' : 36, 'format' : 2, 'sfn' : 'any', 'subf' : (4,)}, 
                         {'id' : 37, 'format' : 2, 'sfn' : 'any', 'subf' : (7,)},
                         {'id' : 38, 'format' : 2, 'sfn' : 'any', 'subf' : (1, 6)}, 
                         {'id' : 39, 'format' : 2, 'sfn' : 'any', 'subf' : (2, 7)},
                         {'id' : 40, 'format' : 2, 'sfn' : 'any', 'subf' : (3, 8)}, 
                         {'id' : 41, 'format' : 2, 'sfn' : 'any', 'subf' : (1, 4, 7)}, 
                         {'id' : 42, 'format' : 2, 'sfn' : 'any', 'subf' : (2, 5, 8)}, 
                         {'id' : 43, 'format' : 2, 'sfn' : 'any', 'subf' : (3, 6, 9)}, 
                         {'id' : 44, 'format' : 2, 'sfn' : 'any', 'subf' : (0, 2, 4, 6, 8)}, 
                         {'id' : 45, 'format' : 2, 'sfn' : 'any', 'subf' : (1, 3, 5, 7, 9)}, 
                         #invalid config index = 46 
                         {'id' : 46, 'format' : -1},
                         {'id' : 47, 'format' : 2, 'sfn' : 'any', 'subf' : (9,)}, 
                         {'id' : 48, 'format' : 3, 'sfn' : 'even', 'subf' : (1,)}, 
                         {'id' : 49, 'format' : 3, 'sfn' : 'even', 'subf' : (4,)}, 
                         {'id' : 50, 'format' : 3, 'sfn' : 'even', 'subf' : (7,)}, 
                         {'id' : 51, 'format' : 3, 'sfn' : 'any', 'subf' : (1,)}, 
                         {'id' : 52, 'format' : 3, 'sfn' : 'any', 'subf' : (4,)}, 
                         {'id' : 53, 'format' : 3, 'sfn' : 'any', 'subf' : (7,)},
                         {'id' : 54, 'format' : 3, 'sfn' : 'any', 'subf' : (1, 6)}, 
                         {'id' : 55, 'format' : 3, 'sfn' : 'any', 'subf' : (2, 7)},
                         {'id' : 56, 'format' : 3, 'sfn' : 'any', 'subf' : (3, 8)}, 
                         {'id' : 57, 'format' : 3, 'sfn' : 'any', 'subf' : (1, 4, 7)}, 
                         {'id' : 58, 'format' : 3, 'sfn' : 'any', 'subf' : (2, 5, 8)}, 
                         {'id' : 59, 'format' : 3, 'sfn' : 'any', 'subf' : (3, 6, 9)}, 
                         #invalid config index = 60/61/62
                         {'id' : 60, 'format' : -1},
                         {'id' : 61, 'format' : -1},
                         {'id' : 62, 'format' : -1},
                         {'id' : 63, 'format' : 3, 'sfn' : 'any', 'sfNum' : (9,)}]
        
        if _prachconffdd[self.prachConfInd]['format'] < 0:
            self.ngwin.logEdit.append('args error: invalid PRACH configuration index: %d. PRACH index 30/46/60/61/62 are not supported in FDD.' % self.prachConfInd)
            return False
        self.prachFddFormat = _prachconffdd[self.prachConfInd]['format']
        self.prachFddSfn = _prachconffdd[self.prachConfInd]['sfn']
        self.prachFddSubf = _prachconffdd[self.prachConfInd]['subf']
        return True
    
    def initPrachTdd(self):
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
        
        _prachquadstdd = [[[(0,1,0,2)], [(0,1,0,1)], [(0,1,0,0)], [(0,1,0,2)], [(0,1,0,1)], [(0,1,0,0)], [(0,1,0,2)]],
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
        
        self.prachTddQuad = _prachquadstdd[self.prachConfInd][self.sa]
        if self.prachTddQuad is None:
            self.ngwin.logEdit.append('args error: invalid PRACH configuration index %d for UL/DL configuration %d' % (self.prachConfInd, self.sa))
            return False
        
        return True
        
    def initSrsFdd(self):
        pass
    
    def initSrsTdd(self):
        pass
                    
