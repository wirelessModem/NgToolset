#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngb36utils.py
Description:
    Implementation of time/frequency encoding in base36.
Change History:
    2018-1-30   v0.1    created.    github/zhenggao2
'''

from numpy import base_repr

def time2str36(hsfn, sfn, subf, symb):
    #HSFN, range 0~1023, two base36 chars
    strHsfn = base_repr(hsfn, base=36)
    #SFN, range 0~1023, two base36 chars
    strSfn = base_repr(sfn, base=36)
    #subframe, range 0~10, one base36 char
    strSubf = base_repr(subf, base=36)
    #symbol, range 0~14, one base36 char
    strSymb = base_repr(symb, base=36)
    
    return '[%s%s%s%s]' % (strHsfn.zfill(2), strSfn.zfill(2), strSubf, strSymb)

def freq2str36(prb, sc):
    #prb, range 0~99, two base36 chars
    strPrb = base_repr(prb, base=36)
    #subcarrier, range 0~47, two base36 chars
    strSc = base_repr(sc, base=36)
    
    return '[%s%s]' % (strPrb.zfill(2), strSc.zfill(2))
 
