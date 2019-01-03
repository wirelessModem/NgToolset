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

import math
import os
import time
from enum import Enum
from collections import OrderedDict
import numpy as np
import ngmainwin

class NrResType(Enum):
    NR_RES_PSS = 0
    NR_RES_SSS = 1
    NR_RES_PBCH = 2
    NR_RES_SIB1 = 3
    NR_RES_PDCCH = 4
    NR_RES_PDSCH = 5
    NR_RES_CSI_RS = 6
    
    NR_RES_PRACH = 10
    NR_RES_PUCCH = 11
    NR_RES_PUSCH = 12
    NR_RES_SRS = 13
    
    NR_RES_DMRS_PBCH = 20
    NR_RES_DMRS_SIB1 = 21
    NR_RES_DMRS_PDCCH = 22 
    NR_RES_DMRS_PDSCH = 23
    
    NR_RES_DMRS_PUCCH = 30 
    NR_RES_DMRS_PUSCH = 31 
    
    NR_RES_PTRS_PDSCH = 40 
    NR_RES_PTRS_PUSCH = 41 
    
    NR_RES_DTX = 50 
    
    NR_RES_D = 60 
    NR_RES_F = 61 
    NR_RES_U = 62 
    
    NR_RES_BUTT = 99

class NgNrGrid(object):
    def __init__(self, ngwin, args):
        self.ngwin = ngwin
        self.args = args
        if not self.init():
            return
            
    
    def init(self):
        self.ngwin.logEdit.append('---->inside init')
        
        #HSFN is not used in NR, but used in 5GNR resource grid for convenience
        self.hsfn = 0
        
        self.nrSubfPerRf = 10
        self.nrSlotPerSubf = [2 ** mu for mu in range(5)]
        self.nrSlotPerRf = [self.nrSubfPerRf * 2 ** mu for mu in range(5)]
        self.nrScs2Mu = {15:0, 30:1, 60:2, 120:3, 240:4}
        self.nrSymbPerSlotNormCp = 14
        self.nrSymbPerSlotExtCp = 12
        self.nrScPerPrb = 12
        
        self.baseScsFd = 15 if self.args['freqBand']['freqRange'] == 'FR1' else 60 
        self.baseScsTd = 60 if self.args['freqBand']['freqRange'] == 'FR1' else 240 
        
        self.nrCarrierScs = int(self.args['carrierGrid']['scs'][:-3])
        self.nrCarrierMinGuardBand = int(self.args['carrierGrid']['minGuardBand'])
        self.nrCarrierNumRbs = int(self.args['carrierGrid']['numRbs'])
        
        self.nrScTot = self.nrScPerPrb * (self.nrCarrierMinGuardBand + self.nrCarrierNumRbs) * (self.nrCarrierScs // self.baseScsFd)
        self.nrSymbPerRfNormCp = self.nrSymbPerSlotNormCp * self.nrSlotPerRf[self.nrScs2Mu[self.baseScsTd]]
        
        self.gridNrTdd = OrderedDict()
        self.gridNrFddDl = OrderedDict()
        self.gridNrFddUl = OrderedDict()
        dn = '%s_%s' % (self.hsfn, self.args['mib']['sfn'])
        if self.args['freqBand']['duplexMode'] == 'TDD':
            self.gridNrTdd[dn] = np.full((self.nrScTot, self.nrSymbPerRfNormCp), NrResType.NR_RES_F.value)
            self.initTddUlDlConfig()
        elif self.args['freqBand']['duplexMode'] == 'FDD':
            self.gridNrFddDl[dn] = np.full((self.nrScTot, self.nrSymbPerRfNormCp), NrResType.NR_RES_D.value)
            self.gridNrFddUl[dn] = np.full((self.nrScTot, self.nrSymbPerRfNormCp), NrResType.NR_RES_U.value)
        else:
            return False
        
        return True
        
    def initTddUlDlConfig(self):
        self.tddCfgRefScsPeriod = {
            'ms0p5_0' : None,
            'ms0p5_1' : 1,
            'ms0p5_2' : 2,
            'ms0p5_3' : 4,
            'ms0p625_0' : None,
            'ms0p625_1' : None,
            'ms0p625_2' : None,
            'ms0p625_3' : 5,
            'ms1_0' : 1,
            'ms1_1' : 2,
            'ms1_2' : 4,
            'ms1_3' : 8,
            'ms1p25_0' : None,
            'ms1p25_1' : None,
            'ms1p25_2' : 5,
            'ms1p25_3' : 10,
            'ms2_0' : 2,
            'ms2_1' : 4,
            'ms2_2' : 8,
            'ms2_3' : 16,
            'ms2p5_0' : None,
            'ms2p5_1' : 5,
            'ms2p5_2' : 10,
            'ms2p5_3' : 20,
            'ms5_0' : 5,
            'ms5_1' : 10,
            'ms5_2' : 20,
            'ms5_3' : 40,
            'ms10_0' : 10,
            'ms10_1' : 20,
            'ms10_2' : 40,
            'ms10_3' : 80,
            }
        self.tddCfgPeriod2Int = {'ms0p5':4, 'ms0p625':5, 'ms1':8, 'ms1p25':10, 'ms2':16, 'ms2p5':20, 'ms5':40, 'ms10':80}
        
        self.nrTddCfgRefScs = int(self.args['tddCfg']['refScs'][:-3])
        key = '%s_%s' % (self.args['tddCfg']['pat1Period'], self.nrScs2Mu[self.nrTddCfgRefScs])
        if not key in self.tddCfgRefScsPeriod or self.tddCfgRefScsPeriod[key] is None:
            #print error
            return False
        self.pat1NumSlots = self.tddCfgRefScsPeriod[key]
        
        if self.args['tddCfg']['pat2Period'] != 'not used':
            key = '%s_%s' % (self.args['tddCfg']['pat2Period'], self.nrScs2Mu[self.nrTddCfgRefScs])
            if not key in self.tddCfgRefScsPeriod or self.tddCfgRefScsPeriod[key] is None:
                #print error
                return False
            self.pat2NumSlots = self.tddCfgRefScsPeriod[key]
            period = self.tddCfgPeriod2Int[self.args['tddCfg']['pat1Period']] + self.tddCfgPeriod2Int[self.args['tddCfg']['pat2Period']] 
            if 160 % period != 0:
                #print error
                return False
            else:
                self.periodsPer20ms = 160 // period
        else:
            self.pat2NumSlots = None
            self.periodsPer20ms = 160 // self.tddCfgPeriod2Int[self.args['tddCfg']['pat1Period']]
        
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
