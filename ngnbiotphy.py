#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngnbiotphy.py
Description:
    NB-ioT L1(PHY layer) definitions.
Change History:
    2018-1-30   v0.1    created.    github/zhenggao2
'''

from enum import Enum
import numpy as np

class NbiotPhy(Enum):
    #nb operation mode
    NBIOT_INBAND_SAME_PCI = 0
    NBIOT_INBAND_DIFF_PCI = 1
    NBIOT_GUARDBAND = 2
    NBIOT_STANDALONE = 3
    
    #nb ul subcarrier spacing
    NBIOT_UL_3DOT75K = 0
    NBIOT_UL_15K = 1

class NbiotResType(Enum):
    #nb downlink
    NBIOT_RES_NPSS = 0
    NBIOT_RES_NSSS = 1
    NBIOT_RES_NRS = 2
    NBIOT_RES_CRS = 3
    NBIOT_RES_NPBCH = 4
    NBIOT_RES_SIB1 = 5
    NBIOT_RES_SIB2 = 6
    NBIOT_RES_SIB3 = 7
    NBIOT_RES_NPDCCH = 8
    NBIOT_RES_NPDSCH_WO_BCCH = 9
    NBIOT_RES_DTX = 10
    NBIOT_RES_NPDSCH_GAP = 11
    NBIOT_RES_NPDCCH_GAP = 12
    
    #nb uplink
    NBIOT_RES_NPRACH = 13
    NBIOT_RES_NPUSCH_FORMAT1 = 14
    NBIOT_RES_NPUSCH_FORMAT2 = 15
    NBIOT_RES_DMRS_NPUSCH = 16
    NBIOT_RES_SRS = 17
    NBIOT_RES_NPRACH_GAP = 18
    NBIOT_RES_NPUSCH_GAP = 19
    
    #nb blank
    NBIOT_RES_BLANK = 20
    
    NBIOT_RES_BUTT = 99

def incSfn(hsfn, sfn, n):
    if n <= 0:
        return (hsfn, sfn)
    
    sfn = sfn + n
    if sfn >= 1024:
        sfn = sfn % 1024
        hsfn = hsfn + 1
        if hsfn >= 1024:
            hsfn = hsfn % 1024
    return (hsfn, sfn)

def incSubf(hsfn, sfn, subf, n):
    if n <= 0:
        return (hsfn, sfn, subf)
    
    subf = subf + n
    if subf >= 10:
        hsfn, sfn = incSfn(hsfn, sfn, subf // 10)
        subf = subf % 10
    
    return (hsfn, sfn, subf)

def incSlot(hsfn, sfn, slot, n, slotPerRf):
    if n <= 0:
        return (hsfn, sfn, slot)
    
    slot = slot + n
    if slot >= slotPerRf:
        hsfn, sfn = incSfn(hsfn, sfn, slot // slotPerRf)
        slot = slot % slotPerRf
        
    return (hsfn, sfn, slot)

def randc(seed, mpn):
    #36.211 7.2	Pseudo-random sequence generation
    nc = 1600
    
    #init x1
    x1 = [0] * 31
    x1[0] = 1
    
    #init x2
    seedStr = np.base_repr(seed, base=2).zfill(31)
    x2=[int(s) for s in seedStr]
    
    #deduce x1 and x2
    for n in range(31, nc+mpn):
        x1.append((x1[n-31+3] + x1[n-31]) % 2)
        x2.append((x2[n-31+3] + x2[n-31+2] + x2[n-31+1] + x2[n-31]) % 2)
    
    c = []
    for n in range(mpn):
        c.append((x1[n+nc] + x2[n+nc]) % 2)
    
    return c
        
    
