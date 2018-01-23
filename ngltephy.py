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

class LtePhy(Enum):
    #frame structure
    LTE_FS_TYPE1 = 0
    LTE_FS_TYPE2 = 1
    #sysmtem bandwidth
    LTE_BW_6 = 0
    LTE_BW_15 = 1
    LTE_BW_25 = 2
    LTE_BW_50 = 3
    LTE_BW_75 = 4
    LTE_BW_100 = 5
    #cyclic prefix
    LTE_CP_NORMAL = 0
    LTE_CP_EXTENDED = 1
    #PHICH duration
    LTE_PHICH_DUR_NORMAL = 0
    LTE_PHICH_DUR_EXTENDED = 1
    #phich resource
    LTE_PHICH_RES_ONE_SIXTH = 0
    LTE_PHICH_RES_HALF = 1
    LTE_PHICH_RES_ONE = 2
    LTE_PHICH_RES_TWO = 3
    #TDD only, subframe assignment
    LTE_TDD_SA0 = 0
    LTE_TDD_SA1 = 1
    LTE_TDD_SA2 = 2
    LTE_TDD_SA3 = 3
    LTE_TDD_SA4 = 4
    LTE_TDD_SA5 = 5
    LTE_TDD_SA6 = 6
    #TDD only, special subframe pattern
    LTE_TDD_SSP0 = 0
    LTE_TDD_SSP1 = 1
    LTE_TDD_SSP2 = 2
    LTE_TDD_SSP3 = 3
    LTE_TDD_SSP4 = 4
    LTE_TDD_SSP5 = 5
    LTE_TDD_SSP6 = 6
    LTE_TDD_SSP7 = 7
    LTE_TDD_SSP8 = 8
    #TDD only, HARQ-ACK feedback mode in uplink
    LTE_TDD_AN_BUNDLING = 0
    LTE_TDD_AN_MULTIPLEXING = 1
    #PRACH pattern
    LTE_PRACH_SFN_EVEN = 0
    LTE_PRACH_SFN_ANY = 1
    #downlink antenna port(s)
    LTE_DL_AP_ONE = 0
    LTE_DL_AP_TWO = 1
    LTE_DL_AP_FOUR = 2
        
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
    
