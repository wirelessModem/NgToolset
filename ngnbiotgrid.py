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
from ngnbiotphy import NbiotPhy, NbiotResType, incSfn, incSubf, randc
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
            self.slotDurNbUl = 2
        else:
            self.scNbUl = 12
            self.slotPerRfNbUl = 20
            self.slotDurNbUl = 0.5
        self.symbPerSlotNb = 7
        self.symbPerRfNbUl = self.symbPerSlotNb * self.slotPerRfNbUl
        self.symbPerSubfNbDl = self.symbPerSlotNb * self.slotPerSubfNbDl
        self.symbPerRfNbDl = self.symbPerSubfNbDl * self.subfPerRfNbDl
        self.ngwin = ngwin
        self.args = args
        self.init()
    
    def init(self):
        self.initSib1Mapping()
        self.initGridNbDlTmp()
        
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
        self.npdschWoBcchMap = OrderedDict()  #key='HSFN_SFN', value=[list of dl subframes for NPDSCH mapping]
        self.npuschFmt1Map = OrderedDict()  #key='HSFN_SFN', value=[list of dl subframes for NPUSCH format 1 mapping]
        self.npuschFmt2Map = OrderedDict()  #key='HSFN_SFN', value=[list of dl subframes for NPUSCH format 2 mapping]
        
        #data structure for SIB2/SIB3 mapping
        self.sib2Map = OrderedDict()   #key='hsfn_sfn', value=[list of dl subframes for sib2 mapping]
        self.sib3Map = OrderedDict()   #key='hsfn_sfn', value=[list of dl subframes for sib3 mapping]
        
        #data structure for NPDCCH USS mapping
        self.npdcchUssMap = OrderedDict()   #key='hsfn_sfn', value=[list of dl subframes for the first uss candidate]
        
        self.ussRmax = self.args['npdcchUssNumRep']
        #Table 16.6-1: NPDCCH UE- specific search space candidates
        _ussCand = {1 : [(1, 1, 'ncce0')], #(1, 1, 'ncce1'), (1, 2, 'ncce01') not supported!
                    2 : [(1, 1, 'ncce0'), (2, 2, 'ncce01')], #(1, 1, 'ncce1') not supported!
                    4 : [(1, 2, 'ncce01'), (2, 2, 'ncce01'), (4, 2, 'ncce01')],
                    8 : [(self.ussRmax // 8, 2, 'ncce01'), (self.ussRmax // 4, 2, 'ncce01'), (self.ussRmax // 2, 2, 'ncce01'), (self.ussRmax, 2, 'ncce01')]}
        self.ussR, self.ussAggLev, ncce = _ussCand[self.ussRmax][self.args['nbDciN0N1SfRep']] if self.ussRmax < 8 else _ussCand[8][self.args['nbDciN0N1SfRep']]
        
        #data struture for NPRACH mapping
        self.nprachMap = [] #list of OrderedDict, where key='hsfn_sfn', value=[[symbols for group0], [group1], [group2], [group3]] or None for nprach gap
        self.scNbRa = 12
        self.initNprachFreqLoc()
        self.ngwin.logEdit.append('NPRACH frequency locations (nInit=%d):' % self.nInit)
        for i in range(self.args['nprachRepPerAtt']):
            self.ngwin.logEdit.append('-->NPRACH repetion #%d: [%s]' % (i, ','.join([str(self.nScRa[grp]) for grp in range(4*i, 4*(i+1))])))
        self.sendingNprach = False
        
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
    
    def validateNrsSubf(self, sfn, subf):
        #from 36.211 10.2.6
        #When UE receives higher-layer parameter operationModeInfo indicating inband-SamePCI or inband-DifferentPCI,
        #- Before the UE obtains SystemInformationBlockType1-NB, the UE may assume narrowband reference signals are transmitted in subframes #0, #4 and in subframes #9 not containing NSSS.
        #- After the UE obtains SystemInformationBlockType1-NB, the UE may assume narrowband reference signals are transmitted in subframes #0, #4, subframes #9 not containing NSSS, and in NB-IoT downlink subframes and shall not expect narrowband reference signals in other downlink subframes.
        if subf == 0 or subf == 4 or (sfn % 2 == 1 and subf == 9) or self.validateNbDlSubf(sfn, subf):
            return True
        else:
            return False
    
    def fillNrs(self, hsfn, sfn):
        dn = str(hsfn) + '_' + str(sfn)
        if not dn in self.gridNbDl:
            self.ngwin.logEdit.append('Call NgNbiotGrid.fillHostCrs at first to initialize NgNbiotGrid.gridNbDl!')
            return
        
        _nrsPos = [(0, self.symbPerSlotNb-2, 0),
                   (0, self.symbPerSlotNb-1, 3),
                   (1, self.symbPerSlotNb-2, 3),
                   (1, self.symbPerSlotNb-1, 0)]
        if self.args['nbDlAp'] == 1:
            _nrsPos = _nrsPos[:2]
        
        m = list(range(2))
        vShift = self.args['nbPci'] % 6
        
        for ap, l, v in _nrsPos:
            k = list(map(lambda x : 6*x+(v+vShift)%6, m))
            symb = [islot * self.symbPerSlotNb + l for islot in range(self.slotPerRfNbDl) if self.validateNrsSubf(sfn, math.floor(islot/2))]
            
            for _k in k:
                for _symb in symb:
                    if self.gridNbDlTmp[ap][_k][_symb] == NbiotResType.NBIOT_RES_BLANK.value:
                        self.gridNbDlTmp[ap][_k][_symb] = NbiotResType.NBIOT_RES_NRS.value
            
            for _ap in range(self.args['nbDlAp']):
                if _ap != ap:
                    for _k in k:
                        for _symb in symb:
                            if self.gridNbDlTmp[_ap][_k][_symb] == NbiotResType.NBIOT_RES_BLANK.value:
                                self.gridNbDlTmp[_ap][_k][_symb] = NbiotResType.NBIOT_RES_DTX.value
        
    
    def fillHostCrs(self, hsfn, sfn):
        dn = str(hsfn) + '_' + str(sfn)
        
        #init gridNbDl and gridNbUl for dn="hsfn_sfn"
        if not dn in self.gridNbDl:
            self.gridNbDl[dn] = np.full((self.args['nbDlAp'], self.scNbDl, self.symbPerRfNbDl), NbiotResType.NBIOT_RES_BLANK.value)
            #self.gridNbUl[dn] = np.full((1, self.scNbUl, self.symbPerRfNbUl), NbiotResType.NBIOT_RES_BLANK.value)
            #for NPRACH mapping, set shape to (1, 48, self.symbPerRfNbUl)
            self.gridNbUl[dn] = np.full((1, 48, self.symbPerRfNbUl), NbiotResType.NBIOT_RES_BLANK.value)
        
        _crsPos = [(0, 0, 0),
                   (0, self.symbPerSlotNb-3, 3),
                   (1, 0, 3),
                   (1, self.symbPerSlotNb-3, 0)]
        if self.args['nbDlAp'] == 1:
            _crsPos = _crsPos[:2]
            
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

    def initGridNbDlTmp(self):
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
        vShift = self.args['nbPci'] % 6
        
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
        
        slots = (0, 1) #subframe 0 of each radio frame
        for iap in range(self.args['nbDlAp']):
            for islot in slots:
                for isymb in range(3, self.symbPerSlotNb): #skip first 3 ofdm symbols which are reserved for PDCCH
                    for isc in range(self.scNbDl):
                        if self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] == NbiotResType.NBIOT_RES_BLANK.value and self.gridNbDlTmp[iap][isc][islot*self.symbPerSlotNb+isymb] == NbiotResType.NBIOT_RES_BLANK.value:
                            self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] = NbiotResType.NBIOT_RES_NPBCH.value
    
    def fillNbSib1(self, hsfn, sfn):
        if not sfn % 256 in self.sib1MapRf:
            return
        
        dn = str(hsfn) + '_' + str(sfn)
        if not dn in self.gridNbDl:
            self.ngwin.logEdit.append('Call NgNbiotGrid.fillHostCrs at first to initialize NgNbiotGrid.gridNbDl!')
            return
        
        #from 36.211 10.2.3.4
        #the index l in the first slot in a subframe fulfills l >= l_Data_Start where l_Data_Start is given by clause 16.4.1.4 of 3GPP TS 36.213 [4].
        #from 36.213 16.4.1.4
        #- if subframe k is a subframe used for receiving SIB1-NB
        #   - l_Data_Start = 3 the value of the higher layer parameter operationModeInfo is set to ’00’ or ‘01’
        #   - l_Data_Start = 0 otherwise
        #- else...
        slots = (2*4, 2*4+1) #subframe 4 of valid radio frame
        for iap in range(self.args['nbDlAp']):
            for islot in slots:
                for isymb in range(3 if islot % 2 == 0 else 0, self.symbPerSlotNb):
                    for isc in range(self.scNbDl):
                        if self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] == NbiotResType.NBIOT_RES_BLANK.value:
                            self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] = NbiotResType.NBIOT_RES_SIB1.value
    
    def validateNbDlSubf(self, sfn, subf):
        #from 36.213 16.4
        #A NB-IoT UE shall assume a subframe as a NB-IoT DL subframe if
        #-	the UE determines that the subframe does not contain NPSS/NSSS/NPBCH/NB-SIB1 transmission, and
        #-	the subframe is configured as NB-IoT DL subframe after the UE has obtained SystemInformationBlockType1-NB.
        valid = True
        if subf == 5:   #NPSS
            valid = False
        if sfn % 2 == 0 and subf == 9:  #NSSS
            valid = False
        if subf == 0:   #NPBCH
            valid = False
        if sfn in self.sib1MapRf and subf == 4: #NB-SIB1
            valid = False
        if self.args['nbDlBitmap'][(sfn*self.subfPerRfNbDl+subf)%len(self.args['nbDlBitmap'])] == 0:    #DL bitmap
            valid = False
            
        return valid
    
    def resetSib2Mapping(self, hsfn, sfn):
        self.sib2Map.clear()
        siWinLen = self.args['nbSiWinLen'] // 10
        sib2RepPat = self.args['nbSib2RepPattern']
        sib2SubfPerRep = 8 if self.args['nbSib2Tbs'] > 120 else 2
        
        #valid starting radio frames for each SI repetition
        sib2FirstRf = [str(hsfn)+'_'+str(sfn)]
        while True:
            if (len(sib2FirstRf)+1)*sib2RepPat > siWinLen:
                break
            
            hsfn, sfn = incSfn(hsfn, sfn, sib2RepPat)
            sib2FirstRf.append(str(hsfn)+'_'+str(sfn))
        
        #valid dl subframes for each SI repetition
        for _rf in sib2FirstRf:
            tokens = _rf.split('_')
            _hsfn = int(tokens[0])
            _sfn = int(tokens[1])
            for i in range(sib2RepPat):
                _hsfn, _sfn = incSfn(_hsfn, _sfn, i)
                for _subf in range(self.subfPerRfNbDl):
                    if self.validateNbDlSubf(_sfn, _subf):
                        key = str(_hsfn)+'_'+str(_sfn)
                        if key in self.sib2Map:
                            self.sib2Map[key].append(_subf)
                        else:
                            self.sib2Map[key] = [_subf]
                        if len(self.sib2Map[key]) == sib2SubfPerRep:
                            break
    
    def resetSib3Mapping(self, hsfn, sfn):
        self.sib3Map.clear()
        siWinLen = self.args['nbSiWinLen'] // 10
        sib3RepPat = self.args['nbSib3RepPattern']
        sib3SubfPerRep = 8 if self.args['nbSib3Tbs'] > 120 else 2
        
        #valid starting radio frames for each SI repetition
        sib3FirstRf = [str(hsfn)+'_'+str(sfn)]
        while True:
            if (len(sib3FirstRf)+1)*sib3RepPat > siWinLen:
                break
            
            hsfn, sfn = incSfn(hsfn, sfn, sib3RepPat)
            sib3FirstRf.append(str(hsfn)+'_'+str(sfn))
        
        #valid dl subframes for each SI repetition
        for _rf in sib3FirstRf:
            tokens = _rf.split('_')
            _hsfn = int(tokens[0])
            _sfn = int(tokens[1])
            for i in range(sib3RepPat):
                _hsfn, _sfn = incSfn(_hsfn, _sfn, i)
                for _subf in range(self.subfPerRfNbDl):
                    if self.validateNbDlSubf(_sfn, _subf):
                        key = str(_hsfn)+'_'+str(_sfn)
                        if key in self.sib3Map:
                            self.sib3Map[key].append(_subf)
                        else:
                            self.sib3Map[key] = [_subf]
                        if len(self.sib3Map[key]) == sib3SubfPerRep:
                            break
    
    def fillNbSib2(self, hsfn, sfn):
        dn = str(hsfn) + '_' + str(sfn)
        if not dn in self.gridNbDl:
            self.ngwin.logEdit.append('Call NgNbiotGrid.fillHostCrs at first to initialize NgNbiotGrid.gridNbDl!')
            return
        
        #from 36.331 5.2.1.2a
        #The SI messages are transmitted within periodically occurring time domain windows (referred to as SI-windows) using scheduling information provided in SystemInformationBlockType1-NB. Each SI message is associated with a SI-window and the SI-windows of different SI messages do not overlap. That is, within one SI-window only the corresponding SI is transmitted. The length of the SI-window is common for all SI messages, and is configurable.
        #
        #Within the SI-window, the corresponding SI message can be transmitted a number of times over 2 or 8 consecutive NB-IoT downlink subframes depending on TBS. The UE acquires the detailed time/frequency domain scheduling information and other information, e.g. used transport format for the SI messages from schedulingInfoList field in SystemInformationBlockType1-NB. The UE is not required to accumulate several SI messages in parallel but may need to accumulate a SI message across multiple SI windows, depending on coverage condition.
        #
        #SI starting frame: (hsfn*1024+sfn) mod si_period = (n-1)*si_winLen/10 + si_offset
        n = 1   #ascending order in NB-SIB1 schedulingInfoList
        if (hsfn*1024+sfn)%self.args['nbSib2Period'] == (n-1)*self.args['nbSiWinLen']//10+self.args['nbSiRfOff']:
            self.resetSib2Mapping(hsfn, sfn)
        
        key = str(hsfn)+'_'+str(sfn)
        if not key in self.sib2Map:
            return
        
        #from 36.211 10.2.3.4
        #the index l in the first slot in a subframe fulfills l >= l_Data_Start where l_Data_Start is given by clause 16.4.1.4 of 3GPP TS 36.213 [4].
        #from 36.213 16.4.1.4
        #- if subframe k is a subframe used for receiving SIB1-NB
        #   - l_Data_Start = 3 the value of the higher layer parameter operationModeInfo is set to ’00’ or ‘01’
        #   - l_Data_Start = 0 otherwise
        #- else
        #   - l_Data_Start is given by the higher layer parameter eutraControlRegionSize if the value of the higher layer parameter eutraControlRegionSize is present
        #   - l_Data_Start = 0 otherwise
        slots = []
        for subf in self.sib2Map[key]:
            slots.extend([2*subf, 2*subf+1])
            
        for iap in range(self.args['nbDlAp']):
            for islot in slots:
                for isymb in range(self.args['hostLteCfi'] if islot % 2 == 0 else 0, self.symbPerSlotNb):
                    for isc in range(self.scNbDl):
                        if self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] == NbiotResType.NBIOT_RES_BLANK.value:
                            self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] = NbiotResType.NBIOT_RES_SIB2.value
    
    def fillNbSib3(self, hsfn, sfn):
        dn = str(hsfn) + '_' + str(sfn)
        if not dn in self.gridNbDl:
            self.ngwin.logEdit.append('Call NgNbiotGrid.fillHostCrs at first to initialize NgNbiotGrid.gridNbDl!')
            return
        
        #SI starting frame: (hsfn*1024+sfn) mod si_period = (n-1)*si_winLen/10 + si_offset
        n = 2   #ascending order in NB-SIB1 schedulingInfoList
        if (hsfn*1024+sfn)%self.args['nbSib2Period'] == (n-1)*self.args['nbSiWinLen']//10+self.args['nbSiRfOff']:
            self.resetSib3Mapping(hsfn, sfn)
        
        key = str(hsfn)+'_'+str(sfn)
        if not key in self.sib3Map:
            return
        
        slots = []
        for subf in self.sib3Map[key]:
            slots.extend([2*subf, 2*subf+1])
            
        for iap in range(self.args['nbDlAp']):
            for islot in slots:
                #from 36.211 10.2.3.4 and 36.213 16.4.1.4
                for isymb in range(self.args['hostLteCfi'] if islot % 2 == 0 else 0, self.symbPerSlotNb):
                    for isc in range(self.scNbDl):
                        if self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] == NbiotResType.NBIOT_RES_BLANK.value:
                            self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] = NbiotResType.NBIOT_RES_SIB3.value
    
    def resetNpdcchUssMap(self, hsfn, sfn, k0, b):
        self.npdcchUssMap.clear()
        
        #find starting subframe k
        key = str(hsfn) + '_' + str(sfn)
        for subf in range(k0, self.subfPerRfNbDl):
            if self.validateNbDlSubf(sfn, subf):
                if not ((key in self.sib2Map and subf in self.sib2Map[key]) or (key in self.sib3Map and subf in self.sib3Map[key])):
                    b = b - 1
                    if b <= 0:  #found starting subframe k=kb
                        self.npdcchUssMap[key] = [subf]
                        break
        while b > 0:
            hsfn, sfn = incSfn(hsfn, sfn, 1)
            key = str(hsfn) + '_' + str(sfn)
            for subf in range(self.subfPerRfNbDl):
                if self.validateNbDlSubf(sfn, subf):
                    if not ((key in self.sib2Map and subf in self.sib2Map[key]) or (key in self.sib3Map and subf in self.sib3Map[key])):
                        b = b - 1
                        if b <= 0:  #found starting subframe k=kb
                            self.npdcchUssMap[key] = [subf]
                            break
        
        #init uss candidate which repeated in a set of R consecutive NB-IoT downlink subframes
        R = self.ussR - 1
        if R == 0:
            return
        for subf in range(self.npdcchUssMap[key][0]+1, self.subfPerRfNbDl):
            if self.validateNbDlSubf(sfn, subf):
                if not ((key in self.sib2Map and subf in self.sib2Map[key]) or (key in self.sib3Map and subf in self.sib3Map[key])):
                    R = R - 1
                    self.npdcchUssMap[key].append(subf)
                    if R == 0:
                        break
                    
        while R > 0:
            hsfn, sfn = incSfn(hsfn, sfn, 1)
            key = str(hsfn) + '_' + str(sfn)
            for subf in range(self.subfPerRfNbDl):
                if self.validateNbDlSubf(sfn, subf):
                    if not ((key in self.sib2Map and subf in self.sib2Map[key]) or (key in self.sib3Map and subf in self.sib3Map[key])):
                        R = R - 1
                        if key in self.npdcchUssMap:
                            self.npdcchUssMap[key].append(subf)
                        else:
                            self.npdcchUssMap[key] = [subf]
                        if R == 0:
                            break
    
    def fillNpdcchUss(self, hsfn, sfn):
        dn = str(hsfn) + '_' + str(sfn)
        if not dn in self.gridNbDl:
            self.ngwin.logEdit.append('Call NgNbiotGrid.fillHostCrs at first to initialize NgNbiotGrid.gridNbDl!')
            return
        
        key = str(hsfn) + '_' + str(sfn)
        if not key in self.npdcchUssMap:
            return
        
        self.ngwin.logEdit.append('recving NPDCCH @ [HSFN=%d,SFN=%d]' % (hsfn, sfn))
        
        slots = []
        for subf in self.npdcchUssMap[key]:
            slots.extend([2*subf, 2*subf+1])
        
        #from 36.211 10.2.5.5
        #...which meet all of the following criteria: 
        #- they are part of the NCCE(s) assigned for the NPDCCH transmission, and
        #- they are not used for transmission of NPBCH, NPSS, or NSSS , and
        #- they are assumed by the UE not to be used for NRS, and
        #- they are not overlapping with resource elements used for PBCH, PSS, SSS, or CRS as defined in clause 6 (if any), and
        #- the index l in the first slot in a subframe fulfills l >= l_NPDCCH_start where l_NPDCCH_start is given by clause 16.6.1 of 3GPP TS 36.213 [4].
        for iap in range(self.args['nbDlAp']):
            for islot in slots:
                #l = CFI of host LTE in the first slot if a subframe
                for isymb in range(self.args['hostLteCfi'] if islot % 2 == 0 else 0, self.symbPerSlotNb):
                    #for simplicity, always use NCCE0 when AL==1
                    for isc in range(self.scNbDl // 2 if self.ussAggLev == 1 else self.scNbDl):
                        if self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] == NbiotResType.NBIOT_RES_BLANK.value and self.args['hostLteGridDlNpdcch'][iap][self.args['nbInbandPrbIndDl'] * 12 + isc][islot*self.symbPerSlotNb+isymb] == LteResType.LTE_RES_PDSCH.value:
                            self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] = NbiotResType.NBIOT_RES_NPDCCH.value
        
        #TODO: NPDCCH Gap to be implemented!
    
    def resetNpdschWoBcchMap(self, hsfn, sfn, subf):
        self.npdschWoBcchMap.clear()
        
        #36.213 16.4.1
        #A UE shall upon detection on a given serving cell of a NPDCCH with DCI format N1, N2 ending in subframe n intended for the UE, decode, starting in n+5 DL subframe, the corresponding NPDSCH transmission in N consecutive NB-IoT DL subframe(s) ni with i = 0, 1, …, N-1 according to the NPDCCH information
        hsfn, sfn, subf = incSubf(hsfn, sfn, subf, 5)
        
        N = self.args['npdschNoBcchDciN1NumSf'] * self.args['npdschNoBcchDciN1NumRep']
        k0 = self.args['npdschNoBcchDciN1K0']
        
        #skip k0 NB-IoT DL subframes (scheduling delay)
        markSubf = 0
        for _subf in range(subf, self.subfPerRfNbDl):
            if self.validateNbDlSubf(sfn, _subf):
                k0 = k0 - 1
                if k0 <= 0:
                    markSubf = _subf
                    break
                
        while k0 > 0:
            hsfn, sfn = incSfn(hsfn, sfn, 1)
            for _subf in range(self.subfPerRfNbDl):
                if self.validateNbDlSubf(sfn, _subf):
                    k0 = k0 - 1
                    if k0 <= 0:
                        markSubf = _subf
                        break
        
        #find NPDSCH NB-IoT DL subframes n[0..N-1]
        key = str(hsfn) + '_' + str(sfn)
        for _subf in range(markSubf+1, self.subfPerRfNbDl):
            if self.validateNbDlSubf(sfn, _subf):
                if not ((key in self.sib2Map and _subf in self.sib2Map[key]) or (key in self.sib3Map and _subf in self.sib3Map[key])):
                    N = N - 1
                    if key in self.npdschWoBcchMap:
                        self.npdschWoBcchMap[key].append(_subf)
                    else:
                        self.npdschWoBcchMap[key] = [_subf]
                    if N == 0:
                        break
                    
        while N > 0:
            hsfn, sfn = incSfn(hsfn, sfn, 1)
            key = str(hsfn) + '_' + str(sfn)
            for _subf in range(self.subfPerRfNbDl):
                if self.validateNbDlSubf(sfn, _subf):
                    if not ((key in self.sib2Map and _subf in self.sib2Map[key]) or (key in self.sib3Map and _subf in self.sib3Map[key])):
                        N = N - 1
                        if key in self.npdschWoBcchMap:
                            self.npdschWoBcchMap[key].append(_subf)
                        else:
                            self.npdschWoBcchMap[key] = [_subf]
                        if N == 0:
                            break
    
    def fillNpdschWoBcch(self, hsfn, sfn):
        dn = str(hsfn) + '_' + str(sfn)
        if not dn in self.gridNbDl:
            self.ngwin.logEdit.append('Call NgNbiotGrid.fillHostCrs at first to initialize NgNbiotGrid.gridNbDl!')
            return
        
        key = str(hsfn) + '_' + str(sfn)
        if not key in self.npdschWoBcchMap:
            return
        
        self.ngwin.logEdit.append('recving NPDSCH w/o BCCH @ [HSFN=%d,SFN=%d]' % (hsfn, sfn))
        
        slots = []
        for subf in self.npdschWoBcchMap[key]:
            slots.extend([2*subf, 2*subf+1])
        
        #from 36.211 10.2.5.5
        #...which meet all of the following criteria in the current subframe:
        #- the subframe is not used for transmission of NPBCH, NPSS, or NSSS, and
        #- they are assumed by the UE not to be used for NRS, and
        #- they are not overlapping with resource elements used for CRS as defined in clause 6 (if any), and
        #- the index l in the first slot in a subframe fulfills l >= l_Data_Start  where l_Data_Start is given by clause 16.4.1.4 of 3GPP TS 36.213 [4].
        for iap in range(self.args['nbDlAp']):
            for islot in slots:
                #l = CFI of host LTE in the first slot if a subframe
                for isymb in range(self.args['hostLteCfi'] if islot % 2 == 0 else 0, self.symbPerSlotNb):
                    for isc in range(self.scNbDl):
                        if self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] == NbiotResType.NBIOT_RES_BLANK.value and self.args['hostLteGridDlNpdsch'][iap][self.args['nbInbandPrbIndDl'] * 12 + isc][islot*self.symbPerSlotNb+isymb] == LteResType.LTE_RES_PDSCH.value:
                            self.gridNbDl[dn][iap][isc][islot*self.symbPerSlotNb+isymb] = NbiotResType.NBIOT_RES_NPDSCH_WO_BCCH.value
        
        #TODO: NPDSCH Gap to be implemented!
        
    def initNprachFreqLoc(self):
        self.nInit = np.random.randint(0, self.args['nprachNumSc'])
        nStart = self.args['nprachScOff'] + math.floor(self.nInit / self.scNbRa) * self.scNbRa
        self.nScRa = [self.nInit % self.scNbRa]
        
        c = randc(self.args['nbPci'], 10*self.args['nprachRepPerAtt'])
        f = []
        for t in range(self.args['nprachRepPerAtt']):
            nset = list(range(10*t+1, 10*(t+1)))
            ft = sum([c[n] * 2**(n-(10*t+1)) for n in nset]) % (self.scNbRa - 1) + 1
            if t > 0:
                ft = ft + f[t - 1]
            f.append(ft % self.scNbRa)
        
        for i in range(1, 4 * self.args['nprachRepPerAtt']):
            if i % 4 == 0 and i > 0:
                self.nScRa.append((self.nScRa[0] + f[i // 4]) % self.scNbRa)
            elif i % 4 in [1, 3] and self.nScRa[i-1] % 2 == 0:
                self.nScRa.append(self.nScRa[i-1] + 1)
            elif i % 4 in [1, 3] and self.nScRa[i-1] % 2 == 1:
                self.nScRa.append(self.nScRa[i-1] - 1)
            elif i % 4 == 2 and self.nScRa[i-1] < 6:
                self.nScRa.append(self.nScRa[i-1] + 6)
            elif i % 4 == 2 and self.nScRa[i-1] >= 6:
                self.nScRa.append(self.nScRa[i-1] - 6)
        
        self.nScRa = [nStart + n for n in self.nScRa]
    
    def resetNprachMapping(self, hsfn, sfn):
        self.nprachMap.clear()
        self.nprachMap = [OrderedDict() for i in range(self.args['nprachRepPerAtt'])]
        
        hsfn, sfn, subf = incSubf(hsfn, sfn, 0, self.args['nprachStartTime'])
        
        if self.args['nbUlScSpacing'] == NbiotPhy.NBIOT_UL_3DOT75K.value:
            slotNprachPreamb = 3
            symbNprachPreamb = (5, 5, 5, 6)
            if subf / self.slotDurNbUl > self.slotPerRfNbUl - 1:
                hsfn, sfn = incSfn(hsfn, sfn)
                slot = 0
            else:
                slot = math.floor(subf / self.slotDurNbUl)
        else:
            slotNprachPreamb = 12
            symbNprachPreamb= (21, 21, 21, 21)
            slot = math.floor(subf / self.slotDurNbUl)
        
        rep = 0
        while rep < self.args['nprachRepPerAtt']:
            if rep > 0 and rep % 64 == 0:   #after 64 nprach preambles, a 40ms gap is inserted
                for i in range(4):
                    hsfn, sfn = incSfn(hsfn, sfn, 1)
                    key = str(hsfn) + '_' + str(sfn)
                    if not key in self.nprachMap[rep]:
                        self.nprachMap[rep][key] = None
                        
            hsfn, sfn, slot, _list = self.findNextNSlots(hsfn, sfn, slot, slotNprachPreamb)
            
            '''
            self.ngwin.logEdit.append('content of findNextNSlots._list (rep=%d):' % rep)
            self.ngwin.logEdit.append('%s' % ','.join(_list))
            '''
                
            symbGrps = [_list[:sum(symbNprachPreamb[:1])],
                        _list[sum(symbNprachPreamb[:1]):sum(symbNprachPreamb[:2])],
                        _list[sum(symbNprachPreamb[:2]):sum(symbNprachPreamb[:3])],
                        _list[sum(symbNprachPreamb[:3]):sum(symbNprachPreamb[:4])]]
            
            for i, grp in enumerate(symbGrps):
                for symb in grp:
                    tokens = symb.split('|')
                    key = tokens[0]
                    isymb = int(tokens[1])
                    if not key in self.nprachMap[rep] or self.nprachMap[rep][key] is None:
                        self.nprachMap[rep][key] = [None, None, None, None]
                        self.nprachMap[rep][key][i] = [isymb]
                    elif self.nprachMap[rep][key][i] is None:
                        self.nprachMap[rep][key][i] = [isymb]
                    else:
                        self.nprachMap[rep][key][i].append(isymb)
                        
            self.ngwin.logEdit.append('NPRACH mapping(rep=%d):' % rep)
            for key, val in self.nprachMap[rep].items():
                self.ngwin.logEdit.append('-->rep=%d,key=%s,val=%s' % (rep, key, val))
            
            rep = rep + 1
    
    def findNextNSlots(self, hsfn, sfn, slot, n):
        _list = []
        while n > 0:
            if slot < self.slotPerRfNbUl:
                #format = 'hsfn_sfn|symbol'
                _list.extend([str(hsfn)+'_'+str(sfn)+'|'+str(slot*self.symbPerSlotNb+i) for i in range(self.symbPerSlotNb)])
                n = n - 1
                slot = slot + 1
                
            if slot == self.slotPerRfNbUl:
                hsfn, sfn = incSfn(hsfn, sfn, 1)
                slot = 0
        
        return [hsfn, sfn, slot, _list]
        
    def fillNprach(self, hsfn, sfn):
        if sfn % (self.args['nprachPeriod'] // 10) == 0 and not self.sendingNprach:
            self.resetNprachMapping(hsfn, sfn)
        
        key = str(hsfn) + '_' + str(sfn)
        
        for rep in range(self.args['nprachRepPerAtt']):
            if not key in self.nprachMap[rep]:
                continue
            
            if key in self.nprachMap[rep] and self.nprachMap[rep][key] is None:   #NPRACH gap
                continue
            
            #set or clear sendingNprach flag
            if not self.sendingNprach:
                self.sendingNprach = True
            if self.sendingNprach and rep == self.args['nprachRepPerAtt']-1 and list(self.nprachMap[rep].keys())[-1] == key:
                self.sendingNprach = False
            
    def fillNpuschFormat1(self, hsfn, sfn):
        pass
    
    def fillNpuschFormat2(self, hsfn, sfn):
        pass
    
    def normalOps(self, hsfn, sfn):
        self.ngwin.logEdit.append('normalOps @ [HSFN=%d,SFN=%d]' % (hsfn, sfn))
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
        #self.ngwin.logEdit.append('monitorNpdcch @ [HSFN=%d,SFN=%d]' % (hsfn, sfn))
        
        while True:
            #from 36.213 16.6
            #The locations of starting subframe k are given by k=k_b where k_b is the bth consecutive NB-IoT DL subframe from subframe k0,
            #excluding subframes used for transmission of SI messages, and b=u*R , and u=0,1,...,R_max/R-1, and where:
            #-subframe k0 is a subframe satisfying the condition: (10*nf + floor(ns/2)) mod T = floor(a_offset * T)
            #-where T = R_max * G, T >= 4
            T = int(self.ussRmax * self.args['npdcchUssStartSf'])
            k0 = None
            for i in range(self.subfPerRfNbDl):
                if (sfn * self.subfPerRfNbDl + i) % T == math.floor(self.args['npdcchUssOff'] * T):
                    k0 = i
                    break
                
            if k0 is not None:
                u = list(range(self.ussRmax // self.ussR))
                b = u[0] * self.ussR    #for simplicity, always use the first candidate
                
                self.ngwin.logEdit.append('call resetNpdcchUssMap with T=%d, R=%d, k0=%d, b=%d @ [HSFN=%d,SFN=%d]' % (T, self.ussR, k0, b, hsfn, sfn))
                
                self.resetNpdcchUssMap(hsfn, sfn, k0, b)
                
                for key,val in self.npdcchUssMap.items():
                    self.ngwin.logEdit.append('key=%s,val=%s' % (key, val))
                    
                break
            else:
                self.normalOps(hsfn, sfn)
                hsfn, sfn = incSfn(hsfn, sfn, 1)
        
        self.normalOps(hsfn, sfn)
        self.fillNpdcchUss(hsfn, sfn)
        
        #proceed to receive NPDCCH
        allKeys = list(self.npdcchUssMap.keys())
        key = str(hsfn) + '_' + str(sfn)
        if key in allKeys:
            current = key
            last = allKeys[-1] if len(allKeys) > 1 else None
        else:
            current = key
            last = allKeys[-1]
        if last is not None:
            while True:
                hsfn, sfn = incSfn(hsfn, sfn, 1)
                self.normalOps(hsfn, sfn)
                self.fillNpdcchUss(hsfn, sfn)
                
                current = str(hsfn) + '_' + str(sfn)
                if current == last:
                    break
        
        #make return tuple
        retHsfn, retSfn = allKeys[-1].split('_')
        retSubf = self.npdcchUssMap[allKeys[-1]][-1]
        return (int(retHsfn), int(retSfn), retSubf)
        
    def sendNpuschFormat1(self, hsfn, sfn, subf):
        self.normalOps(hsfn, sfn)
        self.fillNpuschFormat1(hsfn, sfn)
        
        #make return tuple
        retHsfn, retSfn = ('0', '0')
        retSubf = 0
        return (int(retHsfn), int(retSfn), retSubf)
    
    def sendNpuschFormat2(self, hsfn, sfn, subf):
        self.normalOps(hsfn, sfn)
        self.fillNpuschFormat2(hsfn, sfn)
        
        #make return tuple
        retHsfn, retSfn = ('0', '0')
        retSubf = 0
        return (int(retHsfn), int(retSfn), retSubf)
    
    def recvNpdschWoBcch(self, hsfn, sfn, subf):
        self.ngwin.logEdit.append('call resetNpdschWoBcchMap with N=%d, k0=%d @ [HSFN=%d,SFN=%d,SUBF=%d]' % (self.args['npdschNoBcchDciN1NumSf']*self.args['npdschNoBcchDciN1NumRep'], self.args['npdschNoBcchDciN1K0'], hsfn, sfn, subf))
        
        self.resetNpdschWoBcchMap(hsfn, sfn, subf)
        
        for key,val in self.npdschWoBcchMap.items():
            self.ngwin.logEdit.append('key=%s,val=%s' % (key, val))
        
        #note there is no need to call normalOps again!
        #self.normalOps(hsfn, sfn)
        self.fillNpdschWoBcch(hsfn, sfn)
        
        #proceed to receive NPDSCH
        allKeys = list(self.npdschWoBcchMap.keys())
        key = str(hsfn) + '_' + str(sfn)
        if key in allKeys:
            current = key
            last = allKeys[-1] if len(allKeys) > 1 else None
        else:
            current = key
            last = allKeys[-1]
        if last is not None:
            while True:
                hsfn, sfn = incSfn(hsfn, sfn, 1)
                self.normalOps(hsfn, sfn)
                self.fillNpdschWoBcch(hsfn, sfn)
                
                current = str(hsfn) + '_' + str(sfn)
                if current == last:
                    break
        
        #make return tuple
        retHsfn, retSfn = allKeys[-1].split('_')
        retSubf = self.npdschWoBcchMap[allKeys[-1]][-1]
        return (int(retHsfn), int(retSfn), retSubf)
