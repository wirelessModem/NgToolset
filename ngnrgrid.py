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
        
        #HSFN not exit in NR specs, but used in 5GNR resource grid for convenience
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
            if not self.initTddUlDlConfig():
                return False
            self.initTddGrid(self.hsfn, int(self.args['mib']['sfn']))
        elif self.args['freqBand']['duplexMode'] == 'FDD':
            self.gridNrFddDl[dn] = np.full((self.nrScTot, self.nrSymbPerRfNormCp), NrResType.NR_RES_D.value)
            self.gridNrFddUl[dn] = np.full((self.nrScTot, self.nrSymbPerRfNormCp), NrResType.NR_RES_U.value)
        else:
            return False
        
        return True
        
    def initTddUlDlConfig(self):
        #refer to 3GPP 38.213 vf30
        #11.1	Slot configuration
        self.tddCfgRefScsPeriod = {
            '0.5ms_0' : None,
            '0.5ms_1' : 1,
            '0.5ms_2' : 2,
            '0.5ms_3' : 4,
            '0.625ms_0' : None,
            '0.625ms_1' : None,
            '0.625ms_2' : None,
            '0.625ms_3' : 5,
            '1ms_0' : 1,
            '1ms_1' : 2,
            '1ms_2' : 4,
            '1ms_3' : 8,
            '1.25ms_0' : None,
            '1.25ms_1' : None,
            '1.25ms_2' : 5,
            '1.25ms_3' : 10,
            '2ms_0' : 2,
            '2ms_1' : 4,
            '2ms_2' : 8,
            '2ms_3' : 16,
            '2.5ms_0' : None,
            '2.5ms_1' : 5,
            '2.5ms_2' : 10,
            '2.5ms_3' : 20,
            '3ms_0' : 3,
            '3ms_1' : 6,
            '3ms_2' : 12,
            '3ms_3' : 24,
            '4ms_0' : 4,
            '4ms_1' : 8,
            '4ms_2' : 16,
            '4ms_3' : 32,
            '5ms_0' : 5,
            '5ms_1' : 10,
            '5ms_2' : 20,
            '5ms_3' : 40,
            '10ms_0' : 10,
            '10ms_1' : 20,
            '10ms_2' : 40,
            '10ms_3' : 80,
            }
        #period is x8 of actual value
        self.tddCfgPeriod2Int = {'0.5ms':4, '0.625ms':5, '1ms':8, '1.25ms':10, '2ms':16, '2.5ms':20, '3ms':24, '4ms':32, '5ms':40, '10ms':80}
        
        self.nrTddCfgRefScs = int(self.args['tddCfg']['refScs'][:-3])
        key = '%s_%s' % (self.args['tddCfg']['pat1Period'], self.nrScs2Mu[self.nrTddCfgRefScs])
        if not key in self.tddCfgRefScsPeriod or self.tddCfgRefScsPeriod[key] is None:
            self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring tddCfgRefScsPeriod!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
            return False
        self.pat1NumSlotsPerPeriod = self.tddCfgRefScsPeriod[key]
        self.nrTddCfgPat1NumDlSlots = int(self.args['tddCfg']['pat1NumDlSlots'])
        self.nrTddCfgPat1NumDlSymbs = int(self.args['tddCfg']['pat1NumDlSymbs'])
        self.nrTddCfgPat1NumUlSymbs = int(self.args['tddCfg']['pat1NumUlSymbs'])
        self.nrTddCfgPat1NumUlSlots = int(self.args['tddCfg']['pat1NumUlSlots'])
        
        if self.args['tddCfg']['pat2Period'] != 'not used':
            key = '%s_%s' % (self.args['tddCfg']['pat2Period'], self.nrScs2Mu[self.nrTddCfgRefScs])
            if not key in self.tddCfgRefScsPeriod or self.tddCfgRefScsPeriod[key] is None:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid key(="%s") when referring tddCfgRefScsPeriod!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), key))
                return False
            self.pat2NumSlotsPerPeriod = self.tddCfgRefScsPeriod[key]
            self.nrTddCfgPat2NumDlSlots = int(self.args['tddCfg']['pat2NumDlSlots'])
            self.nrTddCfgPat2NumDlSymbs = int(self.args['tddCfg']['pat2NumDlSymbs'])
            self.nrTddCfgPat2NumUlSymbs = int(self.args['tddCfg']['pat2NumUlSymbs'])
            self.nrTddCfgPat2NumUlSlots = int(self.args['tddCfg']['pat2NumUlSlots'])
            
            period = self.tddCfgPeriod2Int[self.args['tddCfg']['pat1Period']] + self.tddCfgPeriod2Int[self.args['tddCfg']['pat2Period']] 
            if 160 % period != 0:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid TDD-UL-DL-Config periodicity(=%.3fms) with p=%.3fms and p2=%.3fms, which should divide 20ms!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), period/8, self.tddCfgPeriod2Int[self.args['tddCfg']['pat1Period']]/8, self.tddCfgPeriod2Int[self.args['tddCfg']['pat2Period']]/8))
                return False
        else:
            self.pat2NumSlotsPerPeriod = None
            period = self.tddCfgPeriod2Int[self.args['tddCfg']['pat1Period']]
            if 160 % period != 0:
                self.ngwin.logEdit.append('<font color=red><b>[%s]Error</font>: Invalid TDD-UL-DL-Config periodicity(=%.3fms), which should divide 20ms!' % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()), period/8))
                return False
            
        self.periodsPer20ms = 160 // period
        
        pattern = []
        pattern.extend(['D'] * self.nrTddCfgPat1NumDlSlots * self.nrSymbPerSlotNormCp)
        pattern.extend(['D'] * self.nrTddCfgPat1NumDlSymbs)
        pattern.extend(['F'] * ((self.pat1NumSlotsPerPeriod - self.nrTddCfgPat1NumDlSlots - self.nrTddCfgPat1NumUlSlots) * self.nrSymbPerSlotNormCp - self.nrTddCfgPat1NumDlSymbs - self.nrTddCfgPat1NumUlSymbs))
        pattern.extend(['U'] * self.nrTddCfgPat1NumUlSymbs)
        pattern.extend(['U'] * self.nrTddCfgPat1NumUlSlots * self.nrSymbPerSlotNormCp)
        
        if self.pat2NumSlotsPerPeriod is None:
            numSlotsPerPeriod = self.pat1NumSlotsPerPeriod
        else:
            numSlotsPerPeriod = self.pat1NumSlotsPerPeriod + self.pat2NumSlotsPerPeriod
            
            pattern.extend(['D'] * self.nrTddCfgPat2NumDlSlots * self.nrSymbPerSlotNormCp)
            pattern.extend(['D'] * self.nrTddCfgPat2NumDlSymbs)
            pattern.extend(['F'] * ((self.pat2NumSlotsPerPeriod - self.nrTddCfgPat2NumDlSlots - self.nrTddCfgPat2NumUlSlots) * self.nrSymbPerSlotNormCp - self.nrTddCfgPat2NumDlSymbs - self.nrTddCfgPat2NumUlSymbs))
            pattern.extend(['U'] * self.nrTddCfgPat2NumUlSymbs)
            pattern.extend(['U'] * self.nrTddCfgPat2NumUlSlots * self.nrSymbPerSlotNormCp)
        
        pattern = pattern * self.periodsPer20ms
        self.tddPatEvenRf = pattern[:self.nrSlotPerRf[self.nrScs2Mu[self.nrTddCfgRefScs]] * self.nrSymbPerSlotNormCp]
        self.tddPatOddRf = pattern[self.nrSlotPerRf[self.nrScs2Mu[self.nrTddCfgRefScs]] * self.nrSymbPerSlotNormCp:]
        
        self.ngwin.logEdit.append('pattern of even frame:')
        for i in range(len(self.tddPatEvenRf)):
            if (i+1) % self.nrSymbPerSlotNormCp == 0:
                self.ngwin.logEdit.append('-->slot%d: %s' % (i // self.nrSymbPerSlotNormCp, ''.join(self.tddPatEvenRf[i-13:i+1])))
        self.ngwin.logEdit.append('pattern of odd frame:')
        for i in range(len(self.tddPatOddRf)):
            if (i+1) % self.nrSymbPerSlotNormCp == 0:
                self.ngwin.logEdit.append('-->slot%d: %s' % (i // self.nrSymbPerSlotNormCp, ''.join(self.tddPatOddRf[i-13:i+1])))
        
        return True
    
    def initTddGrid(self, hsfn, sfn):
        dn = '%s_%s' % (hsfn, sfn)
        if not dn in self.gridNrTdd:
            #report error
            return
        
        tddCfgMap = {'D':NrResType.NR_RES_D.value, 'F':NrResType.NR_RES_F.value, 'U':NrResType.NR_RES_U.value}
        scale = self.baseScsTd // self.nrTddCfgRefScs
        self.ngwin.logEdit.append('scale=%d where baseScTd=%dKHz and tddCfgRefScs=%dKHz' % (scale, self.baseScsTd, self.nrTddCfgRefScs))
        if sfn % 2 == 0:
            for i in range(len(self.tddPatEvenRf)):
                for j in range(scale):
                    self.gridNrTdd[dn][:,i*scale+j] = tddCfgMap[self.tddPatEvenRf[i]] 
        else:
            for i in range(len(self.tddPatOddRf)):
                for j in range(scale):
                    self.gridNrTdd[dn][:,i*scale+j] = tddCfgMap[self.tddPatOddRf[i]] 
        
        '''
        rows, cols = self.gridNrTdd[dn].shape
        for i in range(rows):
            self.ngwin.logEdit.append(','.join([str(self.gridNrTdd[dn][i,j]) for j in range(cols)]))
        '''
        
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
