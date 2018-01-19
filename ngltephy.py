#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngltephy.py
Description:
    LTE L1(PHY layer) definitions.
Change History:
    2018-1-19   v0.1    created.    github/zhenggao2
'''

from enum import Enum

class LtePhy(object):
    def __init__(self):
        self.bw = (6, 15, 25, 50, 75, 100)
        self.cp = ('normal', 'extended')
        self.phichDur = ('normal', 'extended')
        self.phichRes = ('oneSixth', 'half', 'one', 'two')
        self.fs = ('type1', 'type2')
        self.tddSa = ('sa0', 'sa1', 'sa2', 'sa3', 'sa4', 'sa5', 'sa6')
        self.tddSsp = ('ssp0', 'ssp1', 'ssp2', 'ssp3', 'ssp4', 'ssp5', 'ssp6', 'ssp7', 'ssp8')
        self.tddAckMode = ('bundling', 'multiplexing')
        self.prachSfn = ('even', 'any')
        self.dlAp = (1, 2, 4)
        
class LteResType(Enum):
    #downlink
    LTE_RES_PDSCH = 0
    LTE_RES_PDCCH = 1
    LTE_RES_PHICH = 2
    LTE_RES_PCFICH = 3
    LTE_RES_PBCH = 4
    LTE_RES_PSCH = 5
    LTE_RES_SSCH = 6
    LTE_RES_CRS = 7
    LTE_RES_DTX = 8
    
    #tdd specific
    LTE_RES_GP = 9
    LTE_RES_UL = 10
    LTE_RES_DL = 11
    
    #uplink
    LTE_RES_PUSCH = 12
    LTE_RES_PUCCH_AN = 13
    LTE_RES_PUCCH_MIXED = 14
    LTE_RES_PUCCH_CQI = 15
    LTE_RES_PRACH = 16
    LTE_RES_DMRS = 17
    LTE_RES_SRS = 18

    LTE_RES_BUTT = 99
    
