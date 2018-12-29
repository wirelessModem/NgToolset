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
        self.init()
    
    def init(self):
        self.ngwin.logEdit.append('---->inside init')
        
        self.nrSubfPerRf = 10
        self.nrSlotPerSubf = [2 ** mu for mu in range(5)]
        self.nrSlotPerRf = [self.nrSubfPerRf * 2 ** mu for mu in range(5)]
        self.nrSymbPerSlotNormCp = 14
        self.nrSymbPerSlotExtCp = 12
        self.nrScPerPrb = 12
        
        self.gridNbDl[dn] = np.full((self.args['nbDlAp'], self.scNbDl, self.symbPerRfNbDl), NbiotResType.NR_RES_BLANK.value)
        #self.gridNbUl[dn] = np.full((1, self.scNbUl, self.symbPerRfNbUl), NbiotResType.NR_RES_BLANK.value)
        
        
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
