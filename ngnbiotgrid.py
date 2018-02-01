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
        self.slotPerRfNbDl = 20
        if args['nbUlScSpacing'] == NbiotPhy.NBIOT_UL_3DOT75K.value:
            self.scNbUl = 48
            self.slotPerRfNbUl = 5
        else:
            self.scNbUl = 12
            self.slotPerRfNbUl = 20
        self.symbPerSlotNb = 7
        self.symbPerRfNbUl = self.symbPerSlotNb * self.slotPerRfNbUl
        self.symbPerRfNbDl = self.symbPerSlotNb * self.slotPerRfNbDl
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
        pass
    
    def fillNsss(self, hsfn, sfn):
        pass
    
    def fillNrs(self, hsfn, sfn):
        pass
    
    def fillHostCrs(self, hsfn, sfn):
        pass
    
    def fillNpbch(self, hsfn, sfn):
        pass
    
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
