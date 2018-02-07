#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngnbiotgrid.py
Description:
    NgNbiotGrid definition.
Change History:
    2018-1-31   v0.1    created.    github/zhenggao2
'''
from collections import Counter, OrderedDict
import math
import os
import time 
import numpy as np
import ngmainwin
from ngltephy import LtePhy, LteResType
from ngnbiotphy import NbiotPhy, NbiotResType
from ngb36utils import time2str36, freq2str36

class NgNbiotGrid(object):
    def __init__(self, ngwin, args):
        self.scNbDl= 12 
        self.slotPerSubfNbDl = 2
        self.subfPerRfNbDl = 10
        self.slotPerRfNbDl = self.slotPerSubfNbDl * self.subfPerRfNbDl 
        if args['nbUlScSpacing'] == NbiotPhy.NBIOT_UL_3DOT75K.value:
            self.scNbUl = 48
            self.slotPerRfNbUl = 5
        else:
            self.scNbUl = 12
            self.slotPerRfNbUl = 20
        self.symbPerSlotNb = 7
        self.symbPerRfNbUl = self.symbPerSlotNb * self.slotPerRfNbUl
        self.symbPerSubfNbDl = self.symbPerSlotNb * self.slotPerSubfNbDl
        self.symbPerRfNbDl = self.symbPerSubfNbDl * self.subfPerRfNbDl
        self.ngwin = ngwin
        self.args = args
        self.init()
    
    def init(self):
        self.initSib1Mapping()
        
        #determine nb ul prb index
        n = math.ceil(self.args['maxPucchRes'] / 2)
        if self.args['nbInbandPrbIndUl'] == 0:
            self.args['nbInbandPrbIndUl'] = n + 6
        elif not (self.args['nbInbandPrbIndUl'] >= n + 6 and self.args['nbInbandPrbIndUl'] <= self.args['hostLteNumPrb'] - n - 1):
            self.ngwin.logEdit.append("Invalid 'NB Inband PRB Index UL', fallback to use default value!")
            self.args['nbInbandPrbIndUl'] = n + 6
            
        #host lte ul/dl resource grid post-processing
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        for fn in self.args['hostLteGrids']:
            with open(os.path.join(outDir, fn), 'r+') as f:
                if 'LTE_UL_RES_GRID' in fn:
                    nbMark1 = self.args['nbInbandPrbIndUl'] * 12 + 1
                    nbMark2 = (self.args['nbInbandPrbIndUl'] + 1) * 12 + 1
                elif 'LTE_DL_RES_GRID' in fn:
                    nbMark1 = self.args['nbInbandPrbIndDl'] * 12 + 1
                    nbMark2 = (self.args['nbInbandPrbIndDl'] + 1) * 12 + 1
                data = f.read()
                lines = data.split('\n')
                tokens = lines[0].split(',')[1:]
                nbLine = ','.join([str(LteResType.LTE_RES_NB_INBAND.value)] * len(tokens))
                f.seek(0)
                f.write('\n'.join(lines[0:nbMark1]))
                f.write('\n')
                if 'LTE_UL_RES_GRID' in fn:
                    for ire in range(self.scNbUl):
                        f.write(freq2str36(self.args['nbInbandPrbIndUl'], ire) + ',' + nbLine + '\n')
                elif 'LTE_DL_RES_GRID' in fn:
                    for ire in range(self.scNbDl):
                        f.write(freq2str36(self.args['nbInbandPrbIndDl'], ire) + ',' + nbLine + '\n')
                f.write('\n'.join(lines[nbMark2:]))
        
        #data structure for NB mapping
        self.gridNbUl = OrderedDict()  #key='HSFN_SFN', value=ndarray of [#ap, #sc, #symbol]
        self.gridNbDl = OrderedDict()  #key='HSFN_SFN', value=ndarray of [#ap, #sc, #symbol]
        self.gridNbDlTmp = None
        
    def initSib1Mapping(self):
        #from 36.331 5.2.1.2a
        #The SystemInformationBlockType1-NB (SIB1-NB) uses a fixed schedule with a periodicity of 2560 ms.
        #SIB1-NB transmission occurs in subframe #4 of every other frame in 16 continuous frames.
        #The starting frame for the first transmission of the SIB1-NB is derived from the cell PCID and the number of repetitions within the 2560 ms period
        #and repetitions are made, equally spaced, within the 2560 ms period (see TS 36.213 [23]).
        if self.args['npdschSib1NumRep'] == 4:
            self.sib1MapRf = [self.args['npdschSib1StartRf'] + 64 * i + 2 * j for i in range(4) for j in range(8)]
        elif self.args['npdschSib1NumRep'] == 8:
            self.sib1MapRf = [self.args['npdschSib1StartRf'] + 32 * i + 2 * j for i in range(8) for j in range(8)]
        elif self.args['npdschSib1NumRep'] == 16:
            self.sib1MapRf = [self.args['npdschSib1StartRf'] + 16 * i + 2 * j for i in range(16) for j in range(8)]
    
    def fillNpss(self, hsfn, sfn):
        dn = str(hsfn) + '_' + str(sfn)
        if not dn in self.gridNbDl:
            self.ngwin.logEdit.append('Call NgNbiotGrid.fillHostCrs at first to initialize NgNbiotGrid.gridNbDl!')
            return
        
        slots = (5*2, 5*2+1) #subframe 5 of each radio frame
        for iap in range(self.args['nbDlAp']):
            for islot in slots:
                for isymb in range(3, self.symbPerSlotNb): #skip first 3 ofdm symbols which are reserved for PDCCH
                    for isc in range(self.scNbDl-1): #last subcarrier is reserved
                        if self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] == NbiotResType.NBIOT_RES_BLANK.value:
                            self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] = NbiotResType.NBIOT_RES_NPSS.value
    
    def fillNsss(self, hsfn, sfn):
        if sfn % 2 != 0:
            return
        
        dn = str(hsfn) + '_' + str(sfn)
        if not dn in self.gridNbDl:
            self.ngwin.logEdit.append('Call NgNbiotGrid.fillHostCrs at first to initialize NgNbiotGrid.gridNbDl!')
            return
        
        slots = (9*2, 9*2+1) #subframe 9 of even radio frame
        for iap in range(self.args['nbDlAp']):
            for islot in slots:
                for isymb in range(3, self.symbPerSlotNb): #skip first 3 ofdm symbols which are reserved for PDCCH
                    for isc in range(self.scNbDl):
                        if self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] == NbiotResType.NBIOT_RES_BLANK.value:
                            self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] = NbiotResType.NBIOT_RES_NSSS.value
        
    
    def fillNrs(self, hsfn, sfn):
        pass
    
    def fillHostCrs(self, hsfn, sfn):
        dn = str(hsfn) + '_' + str(sfn)
        
        #init gridNbDl and gridNbUl for dn="hsfn_sfn"
        if not dn in self.gridNbDl:
            self.gridNbDl[dn] = np.full((self.args['nbDlAp'], self.scNbDl, self.symbPerRfNbDl), NbiotResType.NBIOT_RES_BLANK.value)
            self.gridNbUl[dn] = np.full((1, self.scNbUl, self.symbPerRfNbUl), NbiotResType.NBIOT_RES_BLANK.value)
        
        _crsPos = [(0, 0, 0),
                   (0, self.symbPerSlotNb-3, 3),
                   (1, 0, 3),
                   (1, self.symbPerSlotNb-3, 0)]
        m = list(range(2))
        vShift = self.args['nbPci'] % 6
        
        for ap, l, v in _crsPos:
            k = list(map(lambda x : 6*x+(v+vShift)%6, m))
            symb = [islot * self.symbPerSlotNb + l for islot in range(self.slotPerRfNbDl)]
            
            for _k in k:
                for _symb in symb:
                    if self.gridNbDl[dn][ap][_k][_symb] == NbiotResType.NBIOT_RES_BLANK.value:
                        self.gridNbDl[dn][ap][_k][_symb] = NbiotResType.NBIOT_RES_CRS.value
            
            for _ap in range(self.args['nbDlAp']):
                if _ap != ap:
                    for _k in k:
                        for _symb in symb:
                            if self.gridNbDl[dn][_ap][_k][_symb] == NbiotResType.NBIOT_RES_BLANK.value:
                                self.gridNbDl[dn][_ap][_k][_symb] = NbiotResType.NBIOT_RES_DTX.value
    
    def fillHostSrs(self, hsfn, sfn):
        pass

    def fillGridNbDlTmp(self):
        if self.gridNbDlTmp is not None:
            return
        
        #from 36.211 10.2.4.4
        #For the purpose of the (NPBCH) mapping, the UE shall assume cell-specific reference signals for antenna ports 0-3 and
        #narrowband reference signals for antenna ports 2000 and 2001 being present irrespective of the actual configuration.
        self.gridNbDlTmp = np.full((4, self.scNbDl, self.symbPerRfNbDl), NbiotResType.NBIOT_RES_BLANK.value)
        
        _crsPos = [(0, 0, 0),
                   (0, self.symbPerSlotNb-3, 3),
                   (1, 0, 3),
                   (1, self.symbPerSlotNb-3, 0),
                   (2, 1, 0),
                   (2, 1, 3),
                   (3, 1, 3),
                   (3, 1, 6)]
        
        _nrsPos = [(0, self.symbPerSlotNb-2, 0),
                   (0, self.symbPerSlotNb-1, 3),
                   (1, self.symbPerSlotNb-2, 3),
                   (1, self.symbPerSlotNb-1, 0)]
        
        m = list(range(2))
        vShift = self.args['nbPci']% 6
        
        #Temporary CRS mapping with 4 antenna ports
        for ap, l, v in _crsPos:
            k = list(map(lambda x : 6*x+(v+vShift)%6, m))
            
            if ap in [0, 1]:
                symb = [islot * self.symbPerSlotNb + l for islot in range(self.slotPerRfNbDl)]
            elif (ap == 2 and v == 0) or (ap == 3 and v == 3):
                symb = [islot * self.symbPerSlotNb + l for islot in range(self.slotPerRfNbDl) if islot % 2 == 0]
            else: #(ap == 2 and v == 3) or (ap == 3 and v == 6)
                symb = [islot * self.symbPerSlotNb + l for islot in range(self.slotPerRfNbDl) if islot % 2 == 1]
            
            for _k in k:
                for _symb in symb:
                    if self.gridNbDlTmp[ap][_k][_symb] == NbiotResType.NBIOT_RES_BLANK.value:
                        self.gridNbDlTmp[ap][_k][_symb] = NbiotResType.NBIOT_RES_CRS.value
            
            for _ap in range(4):
                if _ap != ap:
                    for _k in k:
                        for _symb in symb:
                            if self.gridNbDlTmp[_ap][_k][_symb] == NbiotResType.NBIOT_RES_BLANK.value:
                                self.gridNbDlTmp[_ap][_k][_symb] = NbiotResType.NBIOT_RES_DTX.value
        
        #Temporary NRS mapping with 2 antenna ports
        for ap, l, v in _nrsPos:
            k = list(map(lambda x : 6*x+(v+vShift)%6, m))
            symb = [islot * self.symbPerSlotNb + l for islot in range(self.slotPerRfNbDl)]
            
            for _k in k:
                for _symb in symb:
                    if self.gridNbDlTmp[ap][_k][_symb] == NbiotResType.NBIOT_RES_BLANK.value:
                        self.gridNbDlTmp[ap][_k][_symb] = NbiotResType.NBIOT_RES_NRS.value
            
            for _ap in range(2):
                if _ap != ap:
                    for _k in k:
                        for _symb in symb:
                            if self.gridNbDlTmp[_ap][_k][_symb] == NbiotResType.NBIOT_RES_BLANK.value:
                                self.gridNbDlTmp[_ap][_k][_symb] = NbiotResType.NBIOT_RES_DTX.value
    
    def fillNpbch(self, hsfn, sfn):
        dn = str(hsfn) + '_' + str(sfn)
        if not dn in self.gridNbDl:
            self.ngwin.logEdit.append('Call NgNbiotGrid.fillHostCrs at first to initialize NgNbiotGrid.gridNbDl!')
            return
        
        if self.gridNbDlTmp is None:
            self.fillGridNbDlTmp()
        
        slots = (0, 1) #subframe 0 of each radio frame
        for iap in range(self.args['nbDlAp']):
            for islot in slots:
                for isymb in range(3, self.symbPerSlotNb): #skip first 3 ofdm symbols which are reserved for PDCCH
                    for isc in range(self.scNbDl):
                        if self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] == NbiotResType.NBIOT_RES_BLANK.value and self.gridNbDlTmp[iap][isc][islot*self.symbPerSlotNb+isymb] == NbiotResType.NBIOT_RES_BLANK.value:
                            self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] = NbiotResType.NBIOT_RES_NPBCH.value
    
    def fillNbSib1(self, hsfn, sfn):
        pass
    
    def fillNbSib2(self, hsfn, sfn):
        pass
    
    def fillNbSib3(self, hsfn, sfn):
        pass
    
    def fillNpdcch(self, hsfn, sfn):
        pass
    
    def fillNpdschWoBcch(self, hsfn, sfn):
        pass
    
    def fillNprach(self, hsfn, sfn):
        pass
    
    def fillNpuschFormat1(self, hsfn, sfn):
        pass
    
    def fillNpuschFormat2(self, hsfn, sfn):
        pass
    
    def normalOps(self, hsfn, sfn):
        #NB DL
        self.fillHostCrs(hsfn, sfn)
        self.fillNpss(hsfn, sfn)
        self.fillNsss(hsfn, sfn)
        self.fillNpbch(hsfn, sfn)
        self.fillNbSib1(hsfn, sfn)
        self.fillNrs(hsfn, sfn)
        self.fillNbSib2(hsfn, sfn)
        self.fillNbSib3(hsfn, sfn)
        #NB UL
        self.fillNprach(hsfn, sfn)
    
    def monitorNpdcch(self, hsfn, sfn):
        self.normalOps(hsfn, sfn)
        self.fillNpdcch(hsfn, sfn)
        
    def sendNpuschFormat1(self, hsfn, sfn):
        self.normalOps(hsfn, sfn)
        self.fillNpuschFormat1(hsfn, sfn)
    
    def sendNpuschFormat2(self, hsfn, sfn):
        self.normalOps(hsfn, sfn)
        self.fillNpuschFormat2(hsfn, sfn)
    
    def recvNpdschWoBcch(self, hsfn, sfn):
        self.normalOps(hsfn, sfn)
        self.fillNpdschWoBcch(hsfn, sfn)
