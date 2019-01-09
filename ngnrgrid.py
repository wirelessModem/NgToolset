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
#from openpyxl import Workbook
import xlsxwriter
import ngmainwin

class NrResType(Enum):
    NR_RES_PSS = 0
    NR_RES_SSS = 1
    NR_RES_PBCH = 2
    NR_RES_SIB1 = 3
    NR_RES_PDCCH = 4
    NR_RES_PDSCH = 5
    NR_RES_CSI_RS = 6
    NR_RES_MSG2 = 7
    NR_RES_MSG4 = 8
    
    NR_RES_PRACH = 10
    NR_RES_PUCCH = 11
    NR_RES_PUSCH = 12
    NR_RES_SRS = 13
    NR_RES_MSG3 = 14 
    
    NR_RES_DMRS_PBCH = 20
    NR_RES_DMRS_SIB1 = 21
    NR_RES_DMRS_PDCCH = 22 
    NR_RES_DMRS_PDSCH = 23
    NR_RES_DMRS_MSG2 = 24
    NR_RES_DMRS_MSG4 = 25
    
    NR_RES_DMRS_PUCCH = 30 
    NR_RES_DMRS_PUSCH = 31 
    NR_RES_DMRS_MSG3 = 32 
    
    NR_RES_PTRS_PDSCH = 40 
    NR_RES_PTRS_PUSCH = 41 
    
    NR_RES_DTX = 50 
    
    NR_RES_D = 60 
    NR_RES_F = 61 
    NR_RES_U = 62 
    NR_RES_GB = 63
    
    NR_RES_BUTT = 99

class NgNrGrid(object):
    def __init__(self, ngwin, args):
        self.ngwin = ngwin
        self.args = args
        if not self.init():
            return
        #self.exportToExcel()
            
    
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
        self.nrScGb = self.nrScPerPrb * self.nrCarrierMinGuardBand * (self.nrCarrierScs // self.baseScsFd)
        self.nrSymbPerRfNormCp = self.nrSymbPerSlotNormCp * self.nrSlotPerRf[self.nrScs2Mu[self.baseScsTd]]
        
        self.nrDuplexMode = self.args['freqBand']['duplexMode']
        self.nrMibSfn = int(self.args['mib']['sfn'])
        
        self.gridNrTdd = OrderedDict()
        self.gridNrFddDl = OrderedDict()
        self.gridNrFddUl = OrderedDict()
        dn = '%s_%s' % (self.hsfn, self.nrMibSfn)
        if self.nrDuplexMode == 'TDD':
            self.gridNrTdd[dn] = np.full((self.nrScTot, self.nrSymbPerRfNormCp), NrResType.NR_RES_GB.value)
            if not self.initTddUlDlConfig():
                return False
            self.initTddGrid(self.hsfn, self.nrMibSfn)
        elif self.nrDuplexMode == 'FDD':
            self.gridNrFddDl[dn] = np.full((self.nrScTot, self.nrSymbPerRfNormCp), NrResType.NR_RES_D.value)
            self.gridNrFddUl[dn] = np.full((self.nrScTot, self.nrSymbPerRfNormCp), NrResType.NR_RES_U.value)
            #init 'min guard band'
            self.gridNrFddDl[dn][:self.nrScGb, :] = NrResType.NR_RES_GB.value
            self.gridNrFddUl[dn][:self.nrScGb, :] = NrResType.NR_RES_GB.value
        else:
            return False
        
        self.outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
            
        self.nrSsbPeriod = int(self.args['ssbBurst']['period'][:-2])
        self.nrMibHrf = int(self.args['mib']['hrf'])
        self.nrSsbScs = int(self.args['ssbGrid']['scs'][:-3])
        self.nrSsbPattern = self.args['ssbGrid']['pattern']
        self.nrSsbMinGuardBand240k = int(self.args['ssbGrid']['minGuardBand240k']) if self.nrSsbScs == 240 else None
        self.nrSsbKssb = int(self.args['ssbGrid']['kSsb'])
        self.nrSsbNCrbSsb = int(self.args['ssbGrid']['nCrbSsb'])
        self.nrSsbMaxL = int(self.args['ssbBurst']['maxL'])
        self.nrSsbInOneGroup = self.args['ssbBurst']['inOneGroup']
        self.nrSsbGroupPresence = self.args['ssbBurst']['groupPresence'] if self.nrSsbMaxL == 64 else None
        self.nrMibCommonScs = int(self.args['mib']['commonScs'][:-3])
        if self.nrSsbMaxL == 64:
            self.ssbSet = ''
            for group in self.nrSsbGroupPresence:
                if group == '1':
                    self.ssbSet += self.nrSsbInOneGroup
                else:
                    self.ssbSet += '00000000'
        else:
            self.ssbSet = self.nrSsbInOneGroup[:self.nrSsbMaxL]
        
        self.ngwin.logEdit.append('ssbSet="%s"' % self.ssbSet)
        
        if self.nrSsbPattern == 'Case A' and self.nrSsbScs == 15:
            ssb1 = [2, 8]
            ssb2 = 14
            ssb3 = [0, 1] if self.nrSsbMaxL == 4 else [0, 1, 2, 3]
        elif self.nrSsbPattern == 'Case B' and self.nrSsbScs == 30:
            ssb1 = [4, 8, 16, 20]
            ssb2 = 28 
            ssb3 = [0,] if self.nrSsbMaxL == 4 else [0, 1]
        elif self.nrSsbPattern == 'Case C' and self.nrSsbScs == 30:
            ssb1 = [2, 8]
            ssb2 = 14 
            ssb3 = [0, 1] if self.nrSsbMaxL == 4 else [0, 1, 2, 3]
        elif self.nrSsbPattern == 'Case D' and self.nrSsbScs == 120:
            ssb1 = [4, 8, 16, 20]
            ssb2 = 28 
            ssb3 = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18]
        elif self.nrSsbPattern == 'Case E' and self.nrSsbScs == 240:
            ssb1 = [8, 12, 16, 20, 32, 36, 40, 44]
            ssb2 = 56 
            ssb3 = [0, 1, 2, 3, 5, 6, 7, 8]
        else:
            return False
        
        self.ssbFirstSymbSet = []
        for i in ssb1:
            for j in ssb3:
                self.ssbFirstSymbSet.append(i + ssb2 * j)
        self.ssbFirstSymbSet.sort()
        
        ssbFirstSymbSetStr = [] 
        for i in range(len(self.ssbSet)):
            ssbFirstSymbSetStr.append(str(self.ssbFirstSymbSet[i]) if self.ssbSet[i] == '1' else '-')
        self.ngwin.logEdit.append('ssb first symbols: "%s"' % ','.join(ssbFirstSymbSetStr))
                
        
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
                    self.gridNrTdd[dn][self.nrScGb:,i*scale+j] = tddCfgMap[self.tddPatEvenRf[i]] 
        else:
            for i in range(len(self.tddPatOddRf)):
                for j in range(scale):
                    self.gridNrTdd[dn][self.nrScGb:,i*scale+j] = tddCfgMap[self.tddPatOddRf[i]] 
        
        '''
        rows, cols = self.gridNrTdd[dn].shape
        for i in range(rows):
            self.ngwin.logEdit.append(','.join([str(self.gridNrTdd[dn][i,j]) for j in range(cols)]))
        '''
        
    def exportToExcel(self):
        self.ngwin.logEdit.append('---->exporting to excel(engine=xlsxwriter)...')
        verticalHeader = []
        for i in range(self.nrScTot):
            verticalHeader.append('crb%dsc%d' % (i // self.nrScPerPrb, i % self.nrScPerPrb))
        
        horizontalHeader = ['k/l']
        if self.nrDuplexMode == 'TDD':
            for key in self.gridNrTdd.keys():
                hsfn, sfn = key.split('_')
                for i in range(self.nrSymbPerRfNormCp//self.nrSymbPerSlotNormCp):
                    for j in range(self.nrSymbPerSlotNormCp):
                        horizontalHeader.append('sfn%s\nslot%d\nsymb%d' % (sfn, i, j))
        else:
            for key in self.gridNrFddDl.keys():
                hsfn, sfn = key.split('_')
                for i in range(self.nrSymbPerRfNormCp//self.nrSymbPerSlotNormCp):
                    for j in range(self.nrSymbPerSlotNormCp):
                        horizontalHeader.append('sfn%s\nslot%d\nsymb%d' % (sfn, i, j))
        
        workbook = xlsxwriter.Workbook(os.path.join(self.outDir, '5gnr_grid_%s.xlsx' % (time.strftime('%Y%m%d%H%M%S', time.localtime()))))
        fmtHHeader = workbook.add_format({'font_name':'Arial', 'font_size':9, 'bold':True, 'align':'center', 'valign':'vcenter', 'text_wrap':True, 'bg_color':'yellow'})
        fmtVHeader = workbook.add_format({'font_name':'Arial', 'font_size':9, 'bold':True, 'align':'center', 'valign':'vcenter', 'shrink':True, 'bg_color':'yellow'})
        
        #key=NrResType, val=(name, font_color, bg_color)
        resMap = dict()
        resMap[NrResType.NR_RES_PSS.value] = ('PSS', '#000000', '#00FF00')
        resMap[NrResType.NR_RES_SSS.value] = ('PSS', '#000000', '#FFFF00')
        resMap[NrResType.NR_RES_PBCH.value] = ('PBCH', '#000000', '#80FFFF')
        resMap[NrResType.NR_RES_SIB1.value] = ('SIB1', '#0000FF', '#FFFFFF')
        resMap[NrResType.NR_RES_PDCCH.value] = ('PDCCH', '#000000', '#00FFFF')
        resMap[NrResType.NR_RES_PDSCH.value] = ('PDSCH', '#000000', '#FFFFFF')
        resMap[NrResType.NR_RES_CSI_RS.value] = ('CSI-RS', '#000000', '#FF0000')
        resMap[NrResType.NR_RES_MSG2.value] = ('MSG2', '#000000', '#FF00FF')
        resMap[NrResType.NR_RES_MSG4.value] = ('MSG4', '#000000', '#FF00FF')
        
        resMap[NrResType.NR_RES_PRACH.value] = ('CSI-RS', '#000000', '#80FFFF')
        resMap[NrResType.NR_RES_PUCCH.value] = ('PUCCH', '#FFFFFF', '#0000FF')
        resMap[NrResType.NR_RES_PUSCH.value] = ('PUSCH', '#000000', '#FFFFFF')
        resMap[NrResType.NR_RES_SRS.value] = ('PUSCH', '#000000', '#FFFF00')
        resMap[NrResType.NR_RES_MSG3.value] = ('MSG3', '#000000', '#FF00FF')
        
        resMap[NrResType.NR_RES_DMRS_PBCH.value] = ('DMRS', '#000000', '#FF0000')
        resMap[NrResType.NR_RES_DMRS_SIB1.value] = ('DMRS', '#000000', '#FF0000')
        resMap[NrResType.NR_RES_DMRS_PDCCH.value] = ('DMRS', '#000000', '#FF0000')
        resMap[NrResType.NR_RES_DMRS_PDSCH.value] = ('DMRS', '#000000', '#FF0000')
        resMap[NrResType.NR_RES_DMRS_MSG2.value] = ('DMRS', '#000000', '#FF0000')
        resMap[NrResType.NR_RES_DMRS_MSG4.value] = ('DMRS', '#000000', '#FF0000')
        resMap[NrResType.NR_RES_DMRS_PUCCH.value] = ('DMRS', '#000000', '#FF0000')
        resMap[NrResType.NR_RES_DMRS_PUSCH.value] = ('DMRS', '#000000', '#FF0000')
        resMap[NrResType.NR_RES_DMRS_MSG3.value] = ('DMRS', '#000000', '#FF0000')
        
        resMap[NrResType.NR_RES_PTRS_PDSCH.value] = ('PTRS', '#000000', '#FF00FF')
        resMap[NrResType.NR_RES_PTRS_PUSCH.value] = ('PTRS', '#000000', '#FF00FF')
        
        resMap[NrResType.NR_RES_DTX.value] = ('DTX', '#FFFFFF', '#000000')
        
        resMap[NrResType.NR_RES_D.value] = ('D', '#FFFFFF', '#000000')
        resMap[NrResType.NR_RES_F.value] = ('F', '#FFFFFF', '#808080')
        resMap[NrResType.NR_RES_U.value] = ('U', '#FFFFFF', '#000000')
        resMap[NrResType.NR_RES_GB.value] = ('GB', '#808080', '#000000')
        
        formatMap = dict()
        for key, val in resMap.items():
            name, fg, bg = val
            formatMap[key] = workbook.add_format({'font_name':'Arial', 'font_size':9, 'align':'left', 'valign':'vcenter', 'font_color':fg, 'bg_color':bg})
            
        if self.nrDuplexMode == 'TDD':
            sheet1 = workbook.add_worksheet('TDD Grid')
            sheet1.set_zoom(90)
            sheet1.freeze_panes(1, 1)
            
            #write header
            sheet1.write_row(0, 0, horizontalHeader, fmtHHeader)
            sheet1.write_column(1, 0, verticalHeader, fmtVHeader)
            
            count = 0
            for key,val in self.gridNrTdd.items():
                for row in range(val.shape[0]):
                    for col in range(val.shape[1]):
                        name, fg, bg = resMap[val[row, col]]
                        sheet1.write(row+1, col+1+count*val.shape[1], name, formatMap[val[row, col]])
                count += 1
        else:
            sheet1 = workbook.add_worksheet('FDD UL Grid')
            sheet1.set_zoom(90)
            sheet1.freeze_panes(1, 1)
            sheet2 = workbook.add_worksheet('FDD DL Grid')
            sheet2.set_zoom(90)
            sheet2.freeze_panes(1, 1)
            
            #write header
            sheet1.write_row(0, 0, horizontalHeader, fmtHHeader)
            sheet1.write_column(1, 0, verticalHeader, fmtVHeader)
            sheet2.write_row(0, 0, horizontalHeader, fmtHHeader)
            sheet2.write_column(1, 0, verticalHeader, fmtVHeader)
         
            count = 0
            for key,val in self.gridNrFddUl.items():
                for row in range(val.shape[0]):
                    for col in range(val.shape[1]):
                        name, fg, bg = resMap[val[row, col]]
                        sheet1.write(row+1, col+1+count*val.shape[1], name, formatMap[val[row, col]])
                count += 1
            
            count = 0
            for key,val in self.gridNrFddDl.items():
                for row in range(val.shape[0]):
                    for col in range(val.shape[1]):
                        name, fg, bg = resMap[val[row, col]]
                        sheet2.write(row+1, col+1+count*val.shape[1], name, formatMap[val[row, col]])
                count += 1
        
        workbook.close()
    
    def recvSsb(self, hsfn, sfn):
        self.ngwin.logEdit.append('---->inside recvSsb')
        
        if self.nrSsbPeriod >= 10 and self.deltaSfn(self.hsfn, self.nrMibSfn, hsfn, sfn) % (self.nrSsbPeriod // 10) != 0:
            return
        
        ssbHrfSet = [0, 1] if self.nrSsbPeriod < 10 else [self.nrMibHrf]
        
        #TODO SSB frequency domain
        #related to kssb and n_crb_ssb
        
        for hrf in ssbHrfSet:
            for issb in range(len(self.ssbSet)):
                if self.ssbSet[issb] == '0':
                    continue
                #SSB time domain
                ssbFirstSymb = hrf * (self.nrSymbPerRfNormCp // 2) + self.ssbFirstSymbSet[issb] * (self.baseScsTd // self.nrSsbScs)
                
                #TODO update nr grid
                
            pass
        
        pass
    
    def deltaSfn(self, hsfn0, sfn0, hsfn1, sfn1):
        return (1024 * hsfn1 + sfn1) - (1024 * hsfn0 + sfn0)
    
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
