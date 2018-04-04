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
import time
from PyQt5.QtWidgets import qApp

class M8015(object):
    def __init__(self):
        self.periodStartTime = 'NA'
        self.iaHoPrepFail = 0
        self.iaHoAtt = 0
        self.iaHoSucc = 0
        self.iaHoFailTime = 0
        self.irHoPrepFailOth = 0
        self.irHoPrepFailTime = 0
        self.irHoPrepFailAc = 0
        self.irHoPrepFailQci = 0
        self.irHoAtt = 0
        self.irHoSucc = 0
        self.irHoFailTime = 0
        self.mroLateHo = 0
        self.mroEarlyType1Ho = 0
        self.mroEarlyType2Ho = 0
        self.mroPingPongHo = 0
        self.ifLbHoAtt = 0
        self.ifLbHoSucc = 0
        
    def __str__(self):
        _list = [self.periodStartTime, self.iaHoPrepFail, self.iaHoAtt, self.iaHoSucc, self.iaHoFailTime,
                 self.irHoPrepFailOth, self.irHoPrepFailTime, self.irHoPrepFailAc, self.irHoPrepFailQci,
                 self.irHoAtt, self.irHoSucc, self.irHoFailTime,
                 self.mroLateHo, self.mroEarlyType1Ho, self.mroEarlyType2Ho, self.mroPingPongHo,
                 self.ifLbHoAtt, self.ifLbHoSucc]
        _list = list(map(str, _list))
        return ','.join(_list)

class Lncel(object):
    def __init__(self):
        self.lnbtsId = None
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

class Lnadj(object):
    def __init__(self):
        self.coDn = None
        self.adjEnbId = None
        self.adjEnbIp = None
        self.x2Stat = None
        
    def __str__(self):
        _list = [self.coDn, self.adjEnbId, self.adjEnbIp, self.x2Stat]
        return ','.join(_list)
    
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

class HoStat(object):
    def __init__(self):
        self.lnbtsId = None
        self.lncelId = None
        self.iaHoPrepFail = 0
        self.iaHoAtt = 0
        self.iaHoSucc = 0
        self.irHoPrepFail = 0
        self.irHoAtt = 0
        self.irHoSucc = 0
        self.mroLateHo = 0
        self.mroEarlyHo = 0
        self.mroPingPongHo = 0
    
    def __str__(self):
        _list = [self.lnbtsId, self.lncelId, self.iaHoPrepFail, self.iaHoAtt, self.iaHoSucc, self.irHoPrepFail, self.irHoAtt, self.irHoSucc]
        _list = list(map(_list, str))
        return ','.join(_list)
        
class NgM8015Proc(object):
    def __init__(self, ngwin):
        self.ngwin = ngwin
        
        #connection defined as below:
        #m8015Data.key.lncel_id == lncelData.key
        #m8015Data.key.lncel_id == lnhoifData.key
        #m8015Data.key.lncel_id == lnrelData.key.lncel_id
        #m8015Data.key.lnbts_id == lnadjData.key
        #m8015Data.key.lnbts_id == lnadjlData.key
        self.m8015Data= dict() #[key='m8015.lnbts_id+m8015.lncel_id+m8015.eci_id', val=list of M8015]
        self.m8015AggData= dict() #[key='m8015.lnbts_id+m8015.lncel_id+m8015.eci_id', val=aggregated M8015]
        self.lncelData = dict() #[key=lncel.lncel_id, val=Lncel]
        self.lnadjData = dict() #[key=lnadj.lnbts_id, val=Lnadj]
        self.lnadjlData = dict() #[key=lnadjl.lnbts_id, val=Lnadjl]
        self.lnhoifData = dict() #[key=lnhoif.lncel_id, val=Lnhoif]
        self.lnrelData = dict() #[key='lnrel.lncel_id+lnrel.adj_enb_id+lnrel.adj_lcr_id', val=Lnrel]
        
        self.earfcnMap = dict() #[key=eci, val=earfcn]
        self.pciMap = dict() #[key=eci, val=pci]
        self.tacMap = dict() #[key=eci, val=tac]
        
        self.m8015Earfcnxy = dict() #[key='earfcnx+earfcny', val=HoStat]
        self.m8015Ecixy = dict() #[key='ecix+eciy', val=HoStat]
        self.ngwin.logEdit.append('<font color=blue>M8015 analyzer initialized!</font>')
    
    def loadCsvData(self):
        self.loadLncel()
        self.loadLnadj()
        self.loadLnadjl()
        self.loadLnhoif()
        self.loadLnrel()
        self.loadM8015()
    
    def print_(self):
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
            #print('Loading %s' % f.name)
            self.ngwin.logEdit.append('Loading %s' % f.name)
            qApp.processEvents()
            
            #note: use strip to remove the tailing '/n'
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            #print(d)
            
            while True:
                line = f.readline().strip()
                if not line:
                    break
                
                tokens = line.split(',')
                
                t = Lncel()
                t.lnbtsId = tokens[d['LNBTS_ID']]
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
            #print('Loading %s' % f.name)
            self.ngwin.logEdit.append('Loading %s' % f.name)
            qApp.processEvents()
            
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            #print(d)
            
            while True:
                line = f.readline().strip()
                if not line:
                    break
                
                tokens = line.split(',')
                
                t = Lnadj()
                t.coDn = '/'.join(tokens[d['CO_DN']].split('/')[1:])
                #t.adjEnbId = tokens[d['ADJ_ENB_ID']]
                t.adjEnbIp = tokens[d['ADJ_ENB_IP']]
                t.x2Stat = tokens[d['X2_STAT']]
                
                self.lnadjData[tokens[d['LNBTS_ID']] + '_' + tokens[d['ADJ_ENB_ID']]] = t
    
    def loadLnadjl(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_lnadjl.csv'), 'r') as f:
            #print('Loading %s' % f.name)
            self.ngwin.logEdit.append('Loading %s' % f.name)
            qApp.processEvents()
            
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            #print(d)
            
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
            #print('Loading %s' % f.name)
            self.ngwin.logEdit.append('Loading %s' % f.name)
            qApp.processEvents()
            
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            #print(d)
            
            while True:
                line = f.readline().strip()
                if not line:
                    break
                
                tokens = line.split(',')
                
                t = Lnhoif()
                t.coDn = '/'.join(tokens[d['CO_DN']].split('/')[1:])
                #t.ifEarfcn = tokens[d['IF_EARFCN']]
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
                
                self.lnhoifData[tokens[d['LNCEL_ID']] + '_' + tokens[d['IF_EARFCN']]] = t
    
    def loadLnrel(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_lnrel.csv'), 'r') as f:
            #print('Loading %s' % f.name)
            self.ngwin.logEdit.append('Loading %s' % f.name)
            qApp.processEvents()
            
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            #print(d)
            
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
            #print('Loading %s' % f.name)
            self.ngwin.logEdit.append('Loading %s' % f.name)
            qApp.processEvents()
            
            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            #print(d)
            
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
        
        self.aggM8015()
    
    def aggM8015(self):
        #print('Aggregating M8015')
        self.ngwin.logEdit.append('Aggregating M8015')
        qApp.processEvents()
        
        for key,val in self.m8015Data.items():
            t = M8015()
            for rec in val:
                t.iaHoPrepFail = t.iaHoPrepFail + int(rec.iaHoPrepFail)
                t.iaHoAtt = t.iaHoAtt + int(rec.iaHoAtt)
                t.iaHoSucc = t.iaHoSucc + int(rec.iaHoSucc)
                t.iaHoFailTime = t.iaHoFailTime + int(rec.iaHoFailTime)
                t.irHoPrepFailOth = t.irHoPrepFailOth + int(rec.irHoPrepFailOth)
                t.irHoPrepFailTime = t.irHoPrepFailTime + int(rec.irHoPrepFailTime)
                t.irHoPrepFailAc = t.irHoPrepFailAc + int(rec.irHoPrepFailAc)
                t.irHoPrepFailQci = t.irHoPrepFailQci + int(rec.irHoPrepFailQci)
                t.irHoAtt = t.irHoAtt + int(rec.irHoAtt)
                t.irHoSucc = t.irHoSucc + int(rec.irHoSucc)
                t.irHoFailTime = t.irHoFailTime + int(rec.irHoFailTime)
                t.mroLateHo = t.mroLateHo + int(rec.mroLateHo)
                t.mroEarlyType1Ho = t.mroEarlyType1Ho + int(rec.mroEarlyType1Ho)
                t.mroEarlyType2Ho = t.mroEarlyType2Ho + int(rec.mroEarlyType2Ho)
                t.mroPingPongHo = t.mroPingPongHo + int(rec.mroPingPongHo)
                t.ifLbHoAtt = t.ifLbHoAtt + int(rec.ifLbHoAtt)
                t.ifLbHoSucc = t.ifLbHoSucc + int(rec.ifLbHoSucc)
            
            self.m8015AggData[key] = t
                
        '''
        for key,val in self.m8015AggData.items():
            print('key=%s,val=%s' % (key,val))
        '''
    
    def makeEciMap(self):
        #print('Making per ECI map')
        self.ngwin.logEdit.append('Making per ECI map')
        qApp.processEvents()
        
        for key,val in self.lncelData.items():
            if not val.eci in self.earfcnMap:
                self.earfcnMap[val.eci] = val.earfcn
                self.pciMap[val.eci] = val.pci
                self.tacMap[val.eci] = val.tac
        
        for key,val in self.lnadjlData.items():
            eci = 256*val.adjEnbId+val.adjLcrId
            if not eci in self.earfcnMap:
                self.earfcnMap[eci] = val.adjEarfcn
                self.pciMap[eci] = val.adjPci
                self.tacMap[eci] = val.adjTac
                
    def procUserCase01(self):
        #print('Performing analysis for user case #01: per earfcn hosr')
        self.ngwin.logEdit.append('<font color=blue>Performing analysis for user case #01: per earfcn hosr</font>')
        qApp.processEvents()
        
        #user case#1: EARFCNx -> EARFCNy HOSR analysis
        for key,val in self.m8015AggData.items():
            tokens = key.split('_')
            if len(tokens) == 3:
                lnbtsId = tokens[0]
                lncelId = tokens[1]
                eci = tokens[2]
            else:
                continue
            
            if not lncelId in self.lncelData:
                continue
            
            eciSrc = self.lncelData[lncelId].eci
            
            if eciSrc in self.earfcnMap:
                earfcnSrc = self.earfcnMap[eciSrc]
            else:
                earfcnSrc = 'NA'
                
            if eci in self.earfcnMap:
                earfcnDst = self.earfcnMap[eci]
            else:
                earfcnDst = 'NA'
            
            key = earfcnSrc + '_' + earfcnDst 
            if not key in self.m8015Earfcnxy:
                self.m8015Earfcnxy[key] = HoStat()
            self.m8015Earfcnxy[key].iaHoAtt = self.m8015Earfcnxy[key].iaHoAtt + val.iaHoAtt
            self.m8015Earfcnxy[key].iaHoSucc = self.m8015Earfcnxy[key].iaHoSucc + val.iaHoSucc
            self.m8015Earfcnxy[key].irHoAtt = self.m8015Earfcnxy[key].irHoAtt + val.irHoAtt
            self.m8015Earfcnxy[key].irHoSucc = self.m8015Earfcnxy[key].irHoSucc + val.irHoSucc
        
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'm8015_per_earfcn_%s.csv' % time.strftime('%Y%m%d%H%M%S', time.localtime())), 'w') as f:
            self.ngwin.logEdit.append('-->Exporting results to: %s' % f.name)
            qApp.processEvents()
                    
            header = ['DN', 'IA_HO_ATT', 'IA_HO_SUCC', 'IR_HO_ATT', 'IR_HO_SUCC', 'HO_ATT_TOT', 'HO_SUCC_TOT', 'HOSR2(%)']
            f.write(','.join(header))
            f.write('\n')
            
            #for key,val in self.m8015Earfcnxy.items():
            for key,val in sorted(self.m8015Earfcnxy.items(), key=lambda d : d[0]):
                line = [key, val.iaHoAtt, val.iaHoSucc, val.irHoAtt, val.irHoSucc]
                line.append(val.iaHoAtt + val.irHoAtt)
                line.append(val.iaHoSucc + val.irHoSucc)
                if val.iaHoAtt + val.irHoAtt == 0:
                    line.append('DIV0')
                else:
                    line.append('%.2f' % (100*(val.iaHoSucc+val.irHoSucc)/(val.iaHoAtt+val.irHoAtt)))
                line = list(map(str, line))
                f.write(','.join(line))
                f.write('\n')
        
    def procUserCase02(self):
        #print('Performing analysis for user case #02: hosr top n')
        self.ngwin.logEdit.append('<font color=blue>Performing analysis for user case #02: hosr top n</font>')
        qApp.processEvents()
        
        #user case#2: hosr top n analysis
        for key,val in self.m8015AggData.items():
            tokens = key.split('_')
            if len(tokens) == 3:
                lnbtsId = tokens[0]
                lncelId = tokens[1]
                eci = tokens[2]
            else:
                continue
            
            if not lncelId in self.lncelData:
                continue
            
            eciSrc = self.lncelData[lncelId].eci
            
            key = eciSrc + '_' + eci
            if not key in self.m8015Ecixy:
                self.m8015Ecixy[key] = HoStat()
            self.m8015Ecixy[key].lnbtsId = lnbtsId
            self.m8015Ecixy[key].lncelId = lncelId 
            self.m8015Ecixy[key].iaHoPrepFail = val.iaHoPrepFail
            self.m8015Ecixy[key].iaHoAtt = val.iaHoAtt
            self.m8015Ecixy[key].iaHoSucc = val.iaHoSucc
            self.m8015Ecixy[key].irHoPrepFail = val.irHoPrepFailAc + val.irHoPrepFailOth + val.irHoPrepFailQci + val.irHoPrepFailTime
            self.m8015Ecixy[key].irHoAtt = val.irHoAtt
            self.m8015Ecixy[key].irHoSucc = val.irHoSucc
            self.m8015Ecixy[key].mroLateHo= val.mroLateHo
            self.m8015Ecixy[key].mroEarlyHo= val.mroEarlyType1Ho + val.mroEarlyType2Ho
            self.m8015Ecixy[key].mroPingPongHo= val.mroPingPongHo
            
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'm8015_topn_%s.csv' % time.strftime('%Y%m%d%H%M%S', time.localtime())), 'w') as f:
            self.ngwin.logEdit.append('-->Exporting results to: %s' % f.name)
            qApp.processEvents()
                    
            header = ['DN','SRC_ENB_ID', 'SRC_LCR_ID', 'SRC_EARFCN', 'SRC_PCI', 'SRC_TAC', 'DST_ENB_ID', 'DST_LCR_ID', 'DST_EARFCN', 'DST_PCI', 'DST_TAC']
            header.extend(['IA_HO_PREP_FAIL', 'IA_HO_ATT', 'IA_HO_SUCC', 'IR_HO_PREP_FAIL', 'IR_HO_ATT', 'IR_HO_SUCC', 'HO_ATT_TOT', 'HO_SUCC_TOT', 'HO_PREP_FAIL', 'HO_EXEC_FAIL', 'HOSR2(%)', 'MRO_LATE_HO', 'MRO_EARLY_HO', 'MRO_PPONG_HO'])
            header.extend(['DN_LNADJ', 'X2_STAT'])
            header.extend(['DN_LNREL', 'CIO', 'HO_ALLOWED'])
            header.extend(['IA_A3', 'IA_A5', 'IF_A2', 'IF_A1'])
            header.extend(['DN_LNHOIF', 'IF_A3', 'IF_A5'])
            f.write(','.join(header))
            f.write('\n')
            
            #for key,val in self.m8015Ecixy.items():
            for key,val in sorted(self.m8015Ecixy.items(), key=lambda d : d[1].iaHoPrepFail+d[1].irHoPrepFail+d[1].iaHoAtt+d[1].irHoAtt-d[1].iaHoSucc-d[1].irHoSucc, reverse=True):
                if val.iaHoPrepFail + val.iaHoAtt + val.irHoPrepFail + val.irHoAtt == 0:
                    continue
                
                #src/dst cell info
                line = [key]
                eciSrc, eciDst = key.split('_')
                lcrIdSrc = int(eciSrc) % 256
                lcrIdDst = int(eciDst) % 256
                enbIdSrc = (int(eciSrc) - lcrIdSrc) // 256
                enbIdDst = (int(eciDst) - lcrIdDst) // 256
                
                if eciSrc in self.earfcnMap:
                    earfcnSrc = self.earfcnMap[eciSrc]
                else:
                    earfcnSrc = 'NA'
                    
                if eciDst in self.earfcnMap:
                    earfcnDst = self.earfcnMap[eciDst]
                else:
                    earfcnDst = 'NA'
                
                if eciSrc in self.pciMap:
                    pciSrc = self.pciMap[eciSrc]
                else:
                    pciSrc = 'NA'
                    
                if eciDst in self.pciMap:
                    pciDst = self.pciMap[eciDst]
                else:
                    pciDst = 'NA'
                    
                if eciSrc in self.tacMap:
                    tacSrc = self.tacMap[eciSrc]
                else:
                    tacSrc = 'NA'
                    
                if eciDst in self.tacMap:
                    tacDst = self.tacMap[eciDst]
                else:
                    tacDst = 'NA'
                    
                line.extend([enbIdSrc, lcrIdSrc, earfcnSrc, pciSrc, tacSrc])
                line.extend([enbIdDst, lcrIdDst, earfcnDst, pciDst, tacDst])
                
                #M8015 info
                line.extend([val.iaHoPrepFail, val.iaHoAtt, val.iaHoSucc, val.irHoPrepFail, val.irHoAtt, val.irHoSucc])
                line.append(val.iaHoAtt + val.irHoAtt)
                line.append(val.iaHoSucc + val.irHoSucc)
                line.append(val.iaHoPrepFail + val.irHoPrepFail)
                line.append(val.iaHoAtt + val.irHoAtt - val.iaHoSucc - val.irHoSucc)
                if val.iaHoAtt + val.irHoAtt == 0:
                    line.append('DIV0')
                else:
                    line.append('%.2f' % (100*(val.iaHoSucc+val.irHoSucc)/(val.iaHoAtt+val.irHoAtt)))
                line.extend([val.mroLateHo, val.mroEarlyHo, val.mroPingPongHo])
                
                #LNADJ info
                lnadjKey = val.lnbtsId + '_' + str(enbIdDst)
                if lnadjKey in self.lnadjData:
                    dnLnadj = self.lnadjData[lnadjKey].coDn
                    x2Stat = self.lnadjData[lnadjKey].x2Stat
                else:
                    dnLnadj, x2Stat = ('NA', 'NA')
                line.extend([dnLnadj, x2Stat])
                
                #LNREL info
                lnrelKey = val.lncelId + '_' + str(enbIdDst) + '_' + str(lcrIdDst)
                if lnrelKey in self.lnrelData:
                    dnLnrel = self.lnrelData[lnrelKey].coDn
                    cio = self.lnrelData[lnrelKey].cio
                    hoAllowed = self.lnrelData[lnrelKey].hoAllowed
                else:
                    dnLnrel, cio, hoAllowed = ('NA', 'NA', 'NA')
                line.extend([dnLnrel, cio, hoAllowed])
                
                #LNCEL info
                lncelKey = val.lncelId
                if lncelKey in self.lncelData:
                    iaA3 = self.lncelData[lncelKey].a3Off + '_' + self.lncelData[lncelKey].hysA3Off
                    iaA5 = self.lncelData[lncelKey].a5Th3 + '_' + self.lncelData[lncelKey].a5Th3a + '_' + self.lncelData[lncelKey].hysA5Th3
                    ifA2 = self.lncelData[lncelKey].a2Th2If + '_' + self.lncelData[lncelKey].hysA2Th2If
                    ifA1 = self.lncelData[lncelKey].a1Th2a + '_' + self.lncelData[lncelKey].hysA1Th2a
                else:
                    iaA3, iaA5, ifA2, ifA1 = ('NA', 'NA', 'NA', 'NA')
                line.extend([iaA3, iaA5, ifA2, ifA1])
                    
                #LNHOIF info
                lnhoifKey = val.lncelId + '_' + earfcnDst
                if lnhoifKey in self.lnhoifData:
                    dnLnhoif = self.lnhoifData[lnhoifKey].coDn
                    ifA3 = self.lnhoifData[lnhoifKey].ifA3Off + '_' + self.lnhoifData[lnhoifKey].ifHysA3Off
                    ifA5 = self.lnhoifData[lnhoifKey].ifA5Th3 + '_' + self.lnhoifData[lnhoifKey].ifA5Th3a + '_' + self.lnhoifData[lnhoifKey].ifHysA5Th3
                else:
                    dnLnhoif, ifA3, ifA5 = ('NA', 'NA', 'NA')
                line.extend([dnLnhoif, ifA3, ifA5])
                    
                line = list(map(str, line))
                f.write(','.join(line))
                f.write('\n')
                
    def procUserCase03(self):
        self.ngwin.logEdit.append('<font color=blue>Performing analysis for user case #0l: clean LNADJ/LNREL</font>')
        qApp.processEvents()
        
        #user case#3: clean lnadj/lnrel
        for lncelidx in self.lncelData.keys():
            for lncelidy in self.lncelData.keys():
                if lncelidx == lncelidy:
                    continue
                lnbtsidx = self.lncelData[lncelidx].lnbtsId
                enbx = self.lncelData[lncelidx].enbId
                lcrx = self.lncelData[lncelidy].lcrId
                lnbtsidy = self.lncelData[lncelidy].lnbtsId
                enby = self.lncelData[lncelidy].enbId
                lcry = self.lncelData[lncelidy].lcrId
                
                #x-->y
                m8015xy = lnbtsidx + '_' + lncelidx + '_' + str(256*int(enby)+int(lcry)) 
                lnrelxy = lncelidx + '_' + enby + '_' + lcry
                lnadjxy = lnbtsidx + '_' + enby
                
                #y-->x
                m8015yx = lnbtsidy + '_' + lncelidy + '_' + str(256*int(enbx)+int(lcrx))
                lnrelyx = lncelidy + '_' + enbx + '_' + lcrx
                lnadjyx = lnbtsidy + '_' + enbx
                
                if lnrelxy in self.lnrelData and lnrelyx in self.lnrelData:
                    if checkM8015(m8015xy) and checkM8015(m8015yx):
                        continue
                    else:
                        #possible uni-directional NR
                        pass
                elif not (lnrelxy in self.lnrelData or lnrelyx in self.lnrelData):
                    if enbx == enby or lnadjxy in self.lnadjData or lnadjyx in self.lnadjData:
                        #redundant NR?
                        pass
            
    def checkM8015(self, key):
        if not key in self.m8015AggData:
            return False
        
        val = self.m8015AggData[key]
        numHo = val.iaHoPrepFail + val.iaHoAtt + val.irHoPrepFailAc + val.irHoPrepFailOth + val.irHoPrepFailQci + val.irHoPrepFailTime + val.irHoAtt
        if numHo > 0:
            return True 
        else:
            return False
        
    def procUserCasexx(self):
        pass
