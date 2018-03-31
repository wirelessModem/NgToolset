#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngm8015proc.py
Description:
    M8015 analysis tool.
Change History:
    2018-3-29   v0.1    created.    github/zhenggao2
'''

import os

class M8015(object):
    def __init__(self):
        self.periodStartTime = None
        self.iaHoPrepFail = None
        self.iaHoAtt = None
        self.iaHoSucc = None
        self.iaHoFailTime = None
        self.irHoPrepFailOth = None
        self.irHoPrepFailTime = None
        self.irHoPrepFailAc = None
        self.irHoPrepFailQci = None
        self.irHoAtt = None
        self.irHoSucc = None
        self.irHoFailTime = None
        self.mroLateHo = None
        self.mroEarlyType1Ho = None
        self.mroEarlyType2Ho = None
        self.mroPingPongHo = None
        self.ifLbHoAtt = None
        self.ifLbHoSucc = None
        
    def __str__(self):
        _list = [self.periodStartTime, self.iaHoPrepFail, self.iaHoAtt, self.iaHoSucc, self.iaHoFailTime,
                 self.irHoPrepFailOth, self.irHoPrepFailTime, self.irHoPrepFailAc, self.irHoPrepFailQci,
                 self.irHoAtt, self.irHoSucc, self.irHoFailTime,
                 self.mroLateHo, self.mroEarlyType1Ho, self.mroEarlyType2Ho, self.mroPingPongHo,
                 self.ifLbHoAtt, self.ifLbHoSucc]
        return ','.join(_list)
    
    __repr__ = __str__

class Lncel(object):
    def __init__(self):
        self.enbId = None
        self.lcrId = None
        self.eci = None
        self.earfcn = None
        self.pci = None
        self.tac = None
        self.th1 = None
        self.a3Off = None
        self.hysA3off = None
        self.a3RepInt = None
        self.a3Ttt = None
        self.a5Th3 = None
        self.a5Th3a = None
        self.hysA5Th3 = None
        self.a5RepInt = None
        self.a5Ttt = None
        self.a2Th2If = None
        self.hysA2Th2If = None
        self.a2Ttt = None
        self.a1Th2a = None
        self.hysA1Th2a = None
        self.a1Ttt = None
    
    def __str__(self):
        _list = [self.enbId, self.lcrId, self.eci, self.earfcn, self.pci, self.tac, self.th1,
                 self.a3Off, self.hysA3Off, self.a3RepInt, self.a3Ttt,
                 self.a5Th3, self.a5Th3a, self.hysA5Th3, self.a5RepInt, self.a5Ttt,
                 self.a2Th2If, self.hysA2Th2If, self.a2Ttt,
                 self.a1Th2a, self.hysA1Th2a, self.a1Ttt]
        return ','.join(_list)
    
    __repr__ = __str__

class Lnadj(object):
    def __init__(self):
        self.coDn = None
        self.adjEnbId = None
        self.adjEnbIp = None
        self.x2Stat = None
        
    def __str__(self):
        _list = [self.coDn, self.adjEnbId, self.adjEnbIp, self.x2Stat]
        return ','.join(_list)
    
    __repr__ = __str__

class Lnadjl(object):
    def __init__(self):
        self.coDn = None
        self.adjEnbId = None
        self.adjLcrId = None
        self.adjEarfcn = None
        self.adjPci = None
        self.adjTac = None
        
    def __str__(self):
        _list = [self.coDn, self.adjEnbId, self.adjLcrId, self.adjEarfcn, self.adjPci, self.adjTac]
        return ','.join(_list)
    
    __repr__ = __str__
        
class Lnhoif(object):
    def __init__(self):
        self.coDn = None
        self.ifEarfcn = None
        self.ifA3Off = None
        self.ifHysA3off = None
        self.ifA3RepInt = None
        self.ifA3Ttt = None
        self.ifA5Th3 = None
        self.ifA5Th3a = None
        self.ifHysA5Th3 = None
        self.ifA5RepInt = None
        self.ifA5Ttt = None
        self.ifMbw = None
        
    def __str__(self):
        _list = [self.coDn, self.ifEarfcn, self.ifA3Off, self.ifHysA3Off, self.ifA3RepInt, self.ifA3Ttt,
                 self.ifA5Th3, self.ifA5Th3a, self.ifHysA5Th3, self.ifA5RepInt, self.ifA5Ttt, self.ifMbw]
        return ','.join(_list)
    
    __repr__ = __str__
    
class Lnrel(object):
    def __init__(self):
        self.coDn = None
        #self.adjEnbId = None
        #self.adjLcrId = None
        self.cio = None
        self.hoAllowed = None
        self.nrStat = None
        
    def __str__(self):
        _list = [self.coDn, #self.adjEnbId, self.adjLcrId, 
                 self.cio, self.hoAllowed, self.nrStat]
        return ','.join(_list)
    
    __repr__ = __str__
        
class NgM8015Proc(object):
    def __init__(self):
        #connection defined as below:
        #m8015Data.key.lncel_id == lncelData.key
        #m8015Data.key.lncel_id == lnhoifData.key
        #m8015Data.key.lncel_id == lnrelData.key.lncel_id
        #m8015Data.key.lnbts_id == lnadjData.key
        #m8015Data.key.lnbts_id == lnadjlData.key
        self.m8015Data= dict() #[key='m8015.lnbts_id+m8015.lncel_id+m8015.eci_id', val=list of M8015]
        self.lncelData = dict() #[key=lncel.lncel_id, val=Lncel]
        self.lnadjData = dict() #[key=lnadj.lnbts_id, val=Lnadj]
        self.lnadjlData = dict() #[key=lnadjl.lnbts_id, val=Lnadjl]
        self.lnhoifData = dict() #[key=lnhoif.lncel_id, val=Lnhoif]
        self.lnrelData = dict() #[key='lnrel.lncel_id+lnrel.adj_enb_id+lnrel.adj_lcr_id', val=Lnrel]
    
    def loadCsvData(self):
        self.loadLncel()
        self.loadLnadj()
        self.loadLnadjl()
        self.loadLnhoif()
        self.loadLnrel()
        self.loadM8015()
    
    def print(self):
        for key,val in self.lncelData.items():
            print('key=%s,val=%s' % (key, val))
        for key,val in self.lnadjData.items():
            print('key=%s,val=%s' % (key, val))
        for key,val in self.lnadjlData.items():
            print('key=%s,val=%s' % (key, val))
        for key,val in self.lnhoifData.items():
            print('key=%s,val=%s' % (key, val))
        for key,val in self.lnrelData.items():
            print('key=%s,val=%s' % (key, val))
        for key,val in self.m8015Data.items():
            print('key=%s,val=%s' % (key, val))
        
    def loadLncel(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_lncel.csv'), 'r') as f:
            #note: use strip to remove the tailing '/n'
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            print(d)
            
            while True:
                line = f.readline().strip()
                if not line:
                    break
                
                tokens = line.split(',')
                
                t = Lncel()
                t.enbId = tokens[d['ENB_ID']]
                t.lcrId = tokens[d['LCR_ID']]
                t.eci = tokens[d['ECI']]
                t.earfcn = tokens[d['EARFCN']]
                t.pci = tokens[d['PCI']]
                t.tac = tokens[d['TAC']]
                t.th1 = tokens[d['TH1']]
                t.a3Off = tokens[d['A3_OFF']]
                t.hysA3Off = tokens[d['HYS_A3_OFF']]
                t.a3RepInt = tokens[d['A3_REP_INT']]
                t.a3Ttt = tokens[d['A3_TTT']]
                t.a5Th3 = tokens[d['A5_TH3']]
                t.a5Th3a = tokens[d['A5_TH3A']]
                t.hysA5Th3 = tokens[d['HYS_A5_TH3']]
                t.a5RepInt = tokens[d['A5_REP_INT']]
                t.a5Ttt = tokens[d['A5_TTT']]
                t.a2Th2If = tokens[d['A2_TH2_IF']]
                t.hysA2Th2If = tokens[d['HYS_A2_TH2_IF']]
                t.a2Ttt = tokens[d['A2_TTT']]
                t.a1Th2a = tokens[d['A1_TH2A']]
                t.hysA1Th2a = tokens[d['HYS_A1_TH2A']]
                t.a1Ttt = tokens[d['A1_TTT']]
                
                self.lncelData[tokens[d['LNCEL_ID']]] = t 
    
    def loadLnadj(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_lnadj.csv'), 'r') as f:
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            print(d)
            
            while True:
                line = f.readline().strip()
                if not line:
                    break
                
                tokens = line.split(',')
                
                t = Lnadj()
                t.coDn = '/'.join(tokens[d['CO_DN']].split('/')[1:])
                t.adjEnbId = tokens[d['ADJ_ENB_ID']]
                t.adjEnbIp = tokens[d['ADJ_ENB_IP']]
                t.x2Stat = tokens[d['X2_STAT']]
                
                self.lnadjData[tokens[d['LNBTS_ID']]] = t
    
    def loadLnadjl(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_lnadjl.csv'), 'r') as f:
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            print(d)
            
            while True:
                line = f.readline().strip()
                if not line:
                    break
                
                tokens = line.split(',')
                
                t = Lnadjl()
                t.coDn = '/'.join(tokens[d['CO_DN']].split('/')[1:])
                t.adjEnbId = tokens[d['ADJ_ENB_ID']]
                t.adjLcrId = tokens[d['ADJ_LCR_ID']]
                t.adjEarfcn = tokens[d['ADJ_EARFCN']]
                t.adjPci = tokens[d['ADJ_PCI']]
                t.adjTac = tokens[d['ADJ_TAC']]
                
                self.lnadjlData[tokens[d['LNBTS_ID']]] = t
    
    def loadLnhoif(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_lnhoif.csv'), 'r') as f:
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            print(d)
            
            while True:
                line = f.readline().strip()
                if not line:
                    break
                
                tokens = line.split(',')
                
                t = Lnhoif()
                t.coDn = '/'.join(tokens[d['CO_DN']].split('/')[1:])
                t.ifEarfcn = tokens[d['IF_EARFCN']]
                t.ifA3Off = tokens[d['IF_A3_OFF']]
                t.ifHysA3Off = tokens[d['IF_HYS_A3_OFF']]
                t.ifA3RepInt = tokens[d['IF_A3_REP_INT']]
                t.ifA3Ttt = tokens[d['IF_A3_TTT']]
                t.ifA5Th3 = tokens[d['IF_A5_TH3']]
                t.ifA5Th3a = tokens[d['IF_A5_TH3A']]
                t.ifHysA5Th3 = tokens[d['IF_HYS_A5_TH3']]
                t.ifA5RepInt = tokens[d['IF_A5_REP_INT']]
                t.ifA5Ttt = tokens[d['IF_A5_TTT']]
                t.ifMbw = tokens[d['IF_MBW']]
                
                self.lnhoifData[tokens[d['LNCEL_ID']]] = t
    
    def loadLnrel(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_lnrel.csv'), 'r') as f:
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            print(d)
            
            while True:
                line = f.readline().strip()
                if not line:
                    break
                
                tokens = line.split(',')
                
                t = Lnrel()
                t.coDn = '/'.join(tokens[d['CO_DN']].split('/')[1:])
                #t.adjEnbId = tokens[d['ADJ_ENB_ID']]
                #t.adjLcrId = tokens[d['ADJ_LCR_ID']]
                t.cio = tokens[d['CIO']]
                t.hoAllowed = tokens[d['HO_ALLOWED']]
                t.nrStat = tokens[d['NR_STAT']]
                
                self.lnrelData[tokens[d['LNCEL_ID']] + '_' + tokens[d['ADJ_ENB_ID']] + '_' + tokens[d['ADJ_LCR_ID']]] = t
    
    def loadM8015(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_m8015.csv'), 'r') as f:
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            print(d)
            
            while True:
                line = f.readline().strip()
                if not line:
                    break
                
                tokens = line.split(',')
                
                t = M8015()
                t.periodStartTime = tokens[d['PERIOD_START_TIME']]
                t.iaHoPrepFail = tokens[d['INTRA_HO_PREP_FAIL_NB']]
                t.iaHoAtt = tokens[d['INTRA_HO_ATT_NB']]
                t.iaHoSucc = tokens[d['INTRA_HO_SUCC_NB']]
                t.iaHoFailTime = tokens[d['INTRA_HO_FAIL_NB']]
                t.irHoPrepFailOth = tokens[d['INTER_HO_PREP_FAIL_OTH_NB']]
                t.irHoPrepFailTime = tokens[d['INTER_HO_PREP_FAIL_TIME_NB']]
                t.irHoPrepFailAc = tokens[d['INTER_HO_PREP_FAIL_AC_NB']]
                t.irHoPrepFailQci = tokens[d['INTER_HO_PREP_FAIL_QCI_NB']]
                t.irHoAtt = tokens[d['INTER_HO_ATT_NB']]
                t.irHoSucc = tokens[d['INTER_HO_SUCC_NB']]
                t.irHoFailTime = tokens[d['INTER_HO_FAIL_NB']]
                t.mroLateHo = tokens[d['MRO_LATE_HO_NB']]
                t.mroEarlyType1Ho = tokens[d['MRO_EARLY_TYPE1_HO_NB']]
                t.mroEarlyType2Ho = tokens[d['MRO_EARLY_TYPE2_HO_NB']]
                t.mroPingPongHo = tokens[d['MRO_PING_PONG_HO_NB']]
                t.ifLbHoAtt = tokens[d['HO_LB_IF_ATT_NB']]
                t.ifLbHoSucc = tokens[d['HO_LB_IF_SUCC_NB']]
                
                key = tokens[d['LNBTS_ID']] + '_' + tokens[d['LNCEL_ID']] + '_' + tokens[d['ECI_ID']]
                
                if not key in self.m8015Data:
                    self.m8015Data[key] = [t]
                else:
                    self.m8015Data[key].append(t)
