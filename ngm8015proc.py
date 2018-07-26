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

class M8001(object):
    def __init__(self):
        self.smallMsg1Att = 0
        self.largeMsg1Att = 0
        self.dedMsg1Att = 0
        self.rachMsg2 = 0
        
    def __str__(self):
        _list = [self.smallMsg1Att, self.largeMsg1Att, self.dedMsg1Att, self.rachMsg2]
        _list = list(map(str, _list))
        return ','.join(_list)


class M8007(object):
    def __init__(self):
        self.drbSetupAtt = 0
        self.drbSetupSucc = 0
        self.drbSetupFailTimer = 0

    def __str__(self):
        _list = [self.drbSetupAtt, self.drbSetupSucc, self.drbSetupFailTimer]
        _list = list(map(str, _list))
        return ','.join(_list)

class M8005(object):
    def __init__(self):
        self.avgRssiPucch = 0
        self.avgRssiPusch = 0
        self.avgSinrPucch = 0
        self.avgSinrPusch = 0
        
    def __str__(self):
        _list = [self.avgRssiPucch, self.avgRssiPusch, self.avgSinrPucch, self.avgSinrPusch]
        _list = list(map(str, _list))
        return ','.join(_list)

class M8006(object):
    def __init__(self):
        self.erabSetupAtt = 0
        self.erabSetupSucc = 0
        self.erabSetupFailRrna = 0
        self.erabSetupFailTru = 0
        self.erabSetupFailUel = 0
        self.erabSetupFailRip = 0
        self.erabSetupFailUp = 0
        self.erabSetupFailMob = 0
        self.erabRelQci1Tot = 0
        self.erabRelQci1Ina = 0
        self.erabRelQci1UeLost = 0
        self.erabRelQci1Tru = 0
        self.erabRelQci1Red = 0
        self.erabRelQci1Eugr = 0
        self.erabRelQci1Rrna = 0
        self.erabRelQci1HoFail = 0
        self.erabRelQci1EpcPs = 0
        self.erabRelQci1TnlUnsp = 0
        
    def __str__(self):
        _list = [self.erabSetupAtt, self.erabSetupSucc, self.erabSetupFailRrna, self.erabSetupFailTru, self.erabSetupFailUel, self.erabSetupFailRip,
                 self.erabSetupFailUp, self.erabSetupFailMob,
                 self.erabRelQci1Tot, self.erabRelQci1Ina, self.erabRelQci1UeLost, self.erabRelQci1Tru, self.erabRelQci1Red,
                 self.erabRelQci1Eugr, self.erabRelQci1Rrna, self.erabRelQci1HoFail, self.erabRelQci1EpcPs, self.erabRelQci1TnlUnsp]
        _list = list(map(str, _list))
        return ','.join(_list)

class M8013(object):
    def __init__(self):
        self.rrcMsg3Mos = 0
        self.rrcMsg3Mt = 0
        self.rrcMsg3Mod = 0
        self.rrcMsg3Emg = 0
        self.rrcMsg3HiPrio = 0
        self.rrcMsg3DelTol = 0
        self.rrcMsg5 = 0
        
    def __str__(self):
        _list = [self.rrcMsg3Mos, self.rrcMsg3Mt, self.rrcMsg3Mod, self.rrcMsg3Emg,
                 self.rrcMsg3HiPrio, self.rrcMsg3DelTol, self.rrcMsg5]
        _list = list(map(str, _list))
        return ','.join(_list)
    
class M8051(object):
    def __init__(self):
        self.avgUeRrcConn = 0
        self.maxUeRrcConn = 0
        self.avgUeAct = 0
        self.maxUeAct = 0
        
    def __str__(self):
        _list = [self.avgRssiPucch, self.avgRssiPusch, self.avgSinrPucch, self.avgSinrPusch]
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

class Irfim(object):
    def __init__(self):
        self.coDn = None
        self.ifEarfcn = None
        self.ifResPrio = None
        self.ifRxlevMin = None
        self.ifThLow = None
        self.ifThHigh = None
        self.ifMbw = None
        
    def __str__(self):
        _list = [self.coDn, self.ifEarfcn, self.ifResPrio, self.ifRxlevMin, self.ifThLow, self.ifThHigh, self.ifMbw]
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
        
        self.m8001Data= dict() #[key='m8001.lnbts_id+m8001.lncel_id', val=list of M8001]
        self.m8001AggData= dict() #[key='m8001.lnbts_id+m8001.lncel_id', val=aggregated M8001]

        self.m8007Data= dict() #[key='m8007.lnbts_id+m8007.lncel_id', val=list of M8007]
        self.m8007AggData= dict() #[key='m8007.lnbts_id+m8007.lncel_id', val=aggregated M8007]

        self.m8005Data= dict() #[key='m8005.lnbts_id+m8005.lncel_id', val=list of M8005]
        self.m8005AggData= dict() #[key='m8005.lnbts_id+m8005.lncel_id', val=aggregated M8005]
        
        self.m8006Data= dict() #[key='m8006.lnbts_id+m8006.lncel_id', val=list of M8006]
        self.m8006AggData= dict() #[key='m8006.lnbts_id+m8006.lncel_id', val=aggregated M8006]
        
        self.m8013Data= dict() #[key='m8013.lnbts_id+m8013.lncel_id', val=list of M8013]
        self.m8013AggData= dict() #[key='m8013.lnbts_id+m8013.lncel_id', val=aggregated M8013]
        
        self.m8051Data= dict() #[key='m8051.lnbts_id+m8051.lncel_id', val=list of M8051]
        self.m8051AggData= dict() #[key='m8051.lnbts_id+m8051.lncel_id', val=aggregated M8051]
        
        self.lncelData = dict() #[key=lncel.lncel_id, val=Lncel]
        self.lnadjData = dict() #[key=lnadj.lnbts_id, val=Lnadj]
        self.lnadjlData = dict() #[key=lnadjl.lnbts_id, val=Lnadjl]
        self.lnhoifData = dict() #[key=lnhoif.lncel_id+lnhoif.if_earfcn, val=Lnhoif]
        self.irfimData = dict() #[key=irfim.lncel_id+irfim.if_earfcn, val=Irfim]
        self.lnrelData = dict() #[key='lnrel.lncel_id+lnrel.adj_enb_id+lnrel.adj_lcr_id', val=Lnrel]
        self.gridData = [] #optional data for atu grid, enbid+lcrid
        
        self.lnbtsIdLncelIdMap = dict() #[key=ECI, val=lnbts_id+lncel_id]
        self.earfcnMap = dict() #[key=eci, val=earfcn]
        self.pciMap = dict() #[key=eci, val=pci]
        self.tacMap = dict() #[key=eci, val=tac]
        
        self.m8015Earfcnxy = dict() #[key='earfcnx+earfcny', val=HoStat]
        self.m8015Ecixy = dict() #[key='ecix+eciy', val=HoStat]
        
        self.earfcnLnhoif = dict() #[key=enbid+lcrid, val=list of lnhoif earfcn]
        self.earfcnIrfim = dict() #[key=enbid+lcrid, val=list of irfim earfcn]

        self.ngwin.logEdit.append('<font color=blue>M8015 analyzer initialized!</font>')
    
    def loadCsvData(self):
        self.loadLncel()
        self.loadLnadj()
        self.loadLnadjl()
        self.loadLnhoif()
        self.loadIrfim()
        self.loadLnrel()
        self.loadM8015()
        self.loadM8001()
        self.loadM8005()
        self.loadM8006()
        self.loadM8007()
        self.loadM8013()
        self.loadM8051()
        self.loadOpt()
    
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
    
    def loadOpt(self):
        try:
            outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
            with open(os.path.join(outDir, 'grid.csv'), 'r') as f:
                #print('Loading %s' % f.name)
                self.ngwin.logEdit.append('Loading %s' % f.name)
                qApp.processEvents()
                
                line = f.readline().strip()
                tokens = line.split(',')
                d = dict(zip(tokens, range(len(tokens))))
                
                while True:
                    line = f.readline().strip()
                    if not line:
                        break
                    
                    tokens = line.split(',')
                    dn = tokens[d['ENBID']] + '_' + tokens[d['LCRID']]
                    if not dn in self.gridData:
                        self.gridData.append(dn)
                    else:
                        self.ngwin.logEdit.append('-->Duplicate cell found: %s' % dn)
        except Exception as e:
            return
        
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
                t.adjEnbId = tokens[d['ADJ_ENB_ID']]
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
                
                self.lnhoifData[tokens[d['LNCEL_ID']] + '_' + tokens[d['IF_EARFCN']]] = t
    
    def loadIrfim(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_irfim.csv'), 'r') as f:
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
                
                t = Irfim()
                t.coDn = '/'.join(tokens[d['CO_DN']].split('/')[1:])
                t.ifEarfcn = tokens[d['IF_EARFCN']]
                t.ifResPrio = tokens[d['IF_RES_PRIO']]
                t.ifRxlevMin = tokens[d['IF_RXLEV_MIN']]
                t.ifThLow = tokens[d['IF_TH_LOW']]
                t.ifThHigh = tokens[d['IF_TH_HIGH']]
                t.ifMbw = tokens[d['IF_MBW']]
                
                self.irfimData[tokens[d['LNCEL_ID']] + '_' + tokens[d['IF_EARFCN']]] = t
    
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
                t.adjEnbId = tokens[d['ADJ_ENB_ID']]
                t.adjLcrId = tokens[d['ADJ_LCR_ID']]
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
    
    def loadM8001(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_m8001.csv'), 'r') as f:
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
                
                t = M8001()
                t.smallMsg1Att = tokens[d['RACH_STP_ATT_SMALL_MSG']]
                t.largeMsg1Att = tokens[d['RACH_STP_ATT_LARGE_MSG']]
                t.dedMsg1Att = tokens[d['RACH_STP_ATT_DEDICATED']]
                t.rachMsg2 = tokens[d['RACH_STP_COMPLETIONS']]
                
                key = tokens[d['LNBTS_ID']] + '_' + tokens[d['LNCEL_ID']]
                
                if not key in self.m8001Data:
                    self.m8001Data[key] = [t]
                else:
                    self.m8001Data[key].append(t)
        
        self.aggM8001()

    def loadM8007(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_m8007.csv'), 'r') as f:
            # print('Loading %s' % f.name)
            self.ngwin.logEdit.append('Loading %s' % f.name)
            qApp.processEvents()

            line = f.readline().strip()
            tokens = line.split(',')
            d = dict(zip(tokens, range(len(tokens))))
            # print(d)

            while True:
                line = f.readline().strip()
                if not line:
                    break

                tokens = line.split(',')

                t = M8007()
                t.drbSetupAtt= tokens[d['DATA_RB_STP_ATT']]
                t.drbSetupSucc= tokens[d['DATA_RB_STP_SUCC']]
                t.drbSetupFailTimer= tokens[d['DATA_RB_STP_FAIL']]

                key = tokens[d['LNBTS_ID']] + '_' + tokens[d['LNCEL_ID']]

                if not key in self.m8007Data:
                    self.m8007Data[key] = [t]
                else:
                    self.m8007Data[key].append(t)

        self.aggM8007()

    def loadM8005(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_m8005.csv'), 'r') as f:
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
                
                t = M8005()
                t.avgRssiPucch = tokens[d['RSSI_PUCCH_AVG']]
                t.avgRssiPusch = tokens[d['RSSI_PUSCH_AVG']]
                t.avgSinrPucch = tokens[d['SINR_PUCCH_AVG']]
                t.avgSinrPusch = tokens[d['SINR_PUSCH_AVG']]
                
                key = tokens[d['LNBTS_ID']] + '_' + tokens[d['LNCEL_ID']]
                
                if not key in self.m8005Data:
                    self.m8005Data[key] = [t]
                else:
                    self.m8005Data[key].append(t)
        
        self.aggM8005()
    
    def loadM8006(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_m8006.csv'), 'r') as f:
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
                
                t = M8006()
                t.erabSetupAtt = tokens[d['EPS_BEARER_SETUP_ATTEMPTS']]
                t.erabSetupSucc = tokens[d['EPS_BEARER_SETUP_COMPLETIONS']]
                t.erabSetupFailRrna = tokens[d['ERAB_INI_SETUP_FAIL_RNL_RRNA']] + tokens[d['ERAB_ADD_SETUP_FAIL_RNL_RRNA']]
                t.erabSetupFailTru = tokens[d['ERAB_INI_SETUP_FAIL_TNL_TRU']] + tokens[d['ERAB_ADD_SETUP_FAIL_TNL_TRU']]
                t.erabSetupFailUel = tokens[d['ERAB_INI_SETUP_FAIL_RNL_UEL']] + tokens[d['ERAB_ADD_SETUP_FAIL_RNL_UEL']]
                t.erabSetupFailRip = tokens[d['ERAB_INI_SETUP_FAIL_RNL_RIP']] + tokens[d['ERAB_ADD_SETUP_FAIL_RNL_RIP']]
                t.erabSetupFailUp = tokens[d['ERAB_ADD_SETUP_FAIL_UP']]
                t.erabSetupFailMob = tokens[d['ERAB_ADD_SETUP_FAIL_RNL_MOB']]
                t.erabRelQci1Tot = tokens[d['ERAB_REL_ENB_QCI1']]
                t.erabRelQci1Ina = tokens[d['ERAB_REL_ENB_RNL_INA_QCI1']]
                t.erabRelQci1UeLost = tokens[d['ERAB_REL_ENB_RNL_UEL_QCI1']]
                t.erabRelQci1Tru = tokens[d['ERAB_REL_ENB_TNL_TRU_QCI1']]
                t.erabRelQci1Red = tokens[d['ERAB_REL_ENB_RNL_RED_QCI1']]
                t.erabRelQci1Eugr = tokens[d['ERAB_REL_ENB_RNL_EUGR_QCI1']]
                t.erabRelQci1Rrna = tokens[d['ERAB_REL_ENB_RNL_RRNA_QCI1']]
                t.erabRelQci1HoFail = tokens[d['ERAB_REL_HO_FAIL_TIM_QCI1']]
                t.erabRelQci1EpcPs = tokens[d['ERAB_REL_EPC_PATH_SWITCH_QCI1']]
                t.erabRelQci1TnlUnsp = tokens[d['ERAB_REL_ENB_TNL_UNSP_QCI1']]
                
                key = tokens[d['LNBTS_ID']] + '_' + tokens[d['LNCEL_ID']]
                
                if not key in self.m8006Data:
                    self.m8006Data[key] = [t]
                else:
                    self.m8006Data[key].append(t)
        
        self.aggM8006()
    
    def loadM8013(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_m8013.csv'), 'r') as f:
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
                
                t = M8013()
                t.rrcMsg3Mos = tokens[d['SIGN_CONN_ESTAB_ATT_MO_S']]
                t.rrcMsg3Mt = tokens[d['SIGN_CONN_ESTAB_ATT_MT']]
                t.rrcMsg3Mod = tokens[d['SIGN_CONN_ESTAB_ATT_MO_D']]
                t.rrcMsg3Emg = tokens[d['SIGN_CONN_ESTAB_ATT_EMG']]
                t.rrcMsg3HiPrio = tokens[d['SIGN_CONN_ESTAB_ATT_HIPRIO']]
                t.rrcMsg3DelTol = tokens[d['SIGN_CONN_ESTAB_ATT_DEL_TOL']]
                t.rrcMsg5 = tokens[d['SIGN_CONN_ESTAB_COMP']]
                
                key = tokens[d['LNBTS_ID']] + '_' + tokens[d['LNCEL_ID']]
                
                if not key in self.m8013Data:
                    self.m8013Data[key] = [t]
                else:
                    self.m8013Data[key].append(t)
        
        self.aggM8013()
    
    def loadM8051(self):
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'neds_m8051.csv'), 'r') as f:
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
                
                t = M8051()
                t.avgUeRrcConn = tokens[d['RRC_CONNECTED_UE_AVG']]
                t.maxUeRrcConn = tokens[d['RRC_CONNECTED_UE_MAX']]
                t.avgUeAct = tokens[d['CELL_LOAD_ACTIVE_UE_AVG']]
                t.maxUeAct = tokens[d['CELL_LOAD_ACTIVE_UE_MAX']]
                
                key = tokens[d['LNBTS_ID']] + '_' + tokens[d['LNCEL_ID']]
                
                if not key in self.m8051Data:
                    self.m8051Data[key] = [t]
                else:
                    self.m8051Data[key].append(t)
        
        self.aggM8051()
    
    def aggM8001(self):
        self.ngwin.logEdit.append('Aggregating M8001')
        qApp.processEvents()
        
        for key,val in self.m8001Data.items():
            t = M8001()
            for rec in val:
                try:
                    t.smallMsg1Att = t.smallMsg1Att + int(rec.smallMsg1Att)
                    t.largeMsg1Att = t.largeMsg1Att + int(rec.largeMsg1Att)
                    t.dedMsg1Att = t.dedMsg1Att + int(rec.dedMsg1Att)
                    t.rachMsg2 = t.rachMsg2 + int(rec.rachMsg2)
                except Exception as e:
                    #ignore ValueError that may raised by int()
                    continue
            
            self.m8001AggData[key] = t
                
        '''
        for key,val in self.m8001AggData.items():
            print('key=%s,val=%s' % (key,val))
        '''

    def aggM8007(self):
        self.ngwin.logEdit.append('Aggregating M8007')
        qApp.processEvents()

        for key, val in self.m8007Data.items():
            t = M8007()
            for rec in val:
                try:
                    t.drbSetupAtt = t.drbSetupAtt + int(rec.drbSetupAtt)
                    t.drbSetupSucc = t.drbSetupSucc + int(rec.drbSetupSucc)
                    t.drbSetupFailTimer = t.drbSetupFailTimer + int(rec.drbsetupFailTimer)
                except Exception as e:
                    # ignore ValueError that may raised by int()
                    continue

            self.m8007AggData[key] = t

        '''
        for key,val in self.m8007AggData.items():
            print('key=%s,val=%s' % (key,val))
        '''
        
    def aggM8005(self):
        self.ngwin.logEdit.append('Aggregating M8005')
        qApp.processEvents()
        
        for key,val in self.m8005Data.items():
            t = M8005()
            cnt = 0
            for rec in val:
                try:
                    t.avgRssiPucch = t.avgRssiPucch + int(rec.avgRssiPucch)
                    t.avgRssiPusch = t.avgRssiPusch + int(rec.avgRssiPusch)
                    t.avgSinrPucch = t.avgSinrPucch + int(rec.avgSinrPucch)
                    t.avgSinrPusch = t.avgSinrPusch + int(rec.avgSinrPusch)
                    cnt = cnt + 1
                except Exception as e:
                    #ignore ValueError that may raised by int()
                    continue
            
            if cnt > 0:
                t.avgRssiPucch = round(t.avgRssiPucch / cnt, 2)
                t.avgRssiPusch = round(t.avgRssiPusch / cnt, 2)
                t.avgSinrPucch = round(t.avgSinrPucch / cnt, 2)
                t.avgSinrPusch = round(t.avgSinrPusch / cnt, 2)
            else:
                t.avgRssiPucch, t.avgRssiPusch, t.avgSinrPucch, t.avgSinrPusch = ('DIV0', 'DIV0', 'DIV0', 'DIV0')
                
            
            self.m8005AggData[key] = t
                
        '''
        for key,val in self.m8005AggData.items():
            print('key=%s,val=%s' % (key,val))
        '''
    
    def aggM8006(self):
        self.ngwin.logEdit.append('Aggregating M8006')
        qApp.processEvents()
        
        for key,val in self.m8006Data.items():
            t = M8006()
            for rec in val:
                try:
                    t.erabSetupAtt = t.erabSetupAtt + int(rec.erabSetupAtt)
                    t.erabSetupSucc = t.erabSetupSucc + int(rec.erabSetupSucc)
                    t.erabSetupFailRrna = t.erabSetupFailRrna + int(rec.erabSetupFailRrna)
                    t.erabSetupFailTru = t.erabSetupFailTru + int(rec.erabSetupFailTru)
                    t.erabSetupFailUel = t.erabSetupFailUel + int(rec.erabSetupFailUel)
                    t.erabSetupFailRip = t.erabSetupFailRip + int(rec.erabSetupFailRip)
                    t.erabSetupFailUp = t.erabSetupFailUp + int(rec.erabSetupFailUp)
                    t.erabSetupFailMob = t.erabSetupFailMob + int(rec.erabSetupFailMob)
                    t.erabRelQci1Tot = t.erabRelQci1Tot + int(rec.erabRelQci1Tot)
                    t.erabRelQci1Ina = t.erabRelQci1Ina + int(rec.erabRelQci1Ina)
                    t.erabRelQci1UeLost = t.erabRelQci1UeLost + int(rec.erabRelQci1UeLost)
                    t.erabRelQci1Tru = t.erabRelQci1Tru + int(rec.erabRelQci1Tru)
                    t.erabRelQci1Red = t.erabRelQci1Red + int(rec.erabRelQci1Red)
                    t.erabRelQci1Eugr = t.erabRelQci1Eugr + int(rec.erabRelQci1Eugr)
                    t.erabRelQci1Rrna = t.erabRelQci1Rrna + int(rec.erabRelQci1Rrna)
                    t.erabRelQci1HoFail = t.erabRelQci1HoFail + int(rec.erabRelQci1HoFail)
                    t.erabRelQci1EpcPs = t.erabRelQci1EpcPs + int(rec.erabRelQci1EpcPs)
                    t.erabRelQci1TnlUnsp = t.erabRelQci1TnlUnsp + int(rec.erabRelQci1TnlUnsp)
                except Exception as e:
                    #ignore ValueError that may raised by int()
                    continue
            
            self.m8006AggData[key] = t
                
        '''
        for key,val in self.m8006AggData.items():
            print('key=%s,val=%s' % (key,val))
        '''
    
    def aggM8013(self):
        self.ngwin.logEdit.append('Aggregating M8013')
        qApp.processEvents()
        
        for key,val in self.m8013Data.items():
            t = M8013()
            for rec in val:
                try:
                    t.rrcMsg3Mos = t.rrcMsg3Mos + int(rec.rrcMsg3Mos)
                    t.rrcMsg3Mt = t.rrcMsg3Mt + int(rec.rrcMsg3Mt)
                    t.rrcMsg3Mod = t.rrcMsg3Mod + int(rec.rrcMsg3Mod)
                    t.rrcMsg3Emg = t.rrcMsg3Emg + int(rec.rrcMsg3Emg)
                    t.rrcMsg3HiPrio = t.rrcMsg3HiPrio + int(rec.rrcMsg3HiPrio)
                    t.rrcMsg3DelTol = t.rrcMsg3DelTol + int(rec.rrcMsg3DelTol)
                    t.rrcMsg5 = t.rrcMsg5 + int(rec.rrcMsg5)
                except Exception as e:
                    #ignore ValueError that may raised by int()
                    continue
            
            self.m8013AggData[key] = t
                
        '''
        for key,val in self.m8013AggData.items():
            print('key=%s,val=%s' % (key,val))
        '''
    
    def aggM8051(self):
        self.ngwin.logEdit.append('Aggregating M8051')
        qApp.processEvents()
        
        for key,val in self.m8051Data.items():
            t = M8051()
            cnt = 0
            for rec in val:
                try:
                    t.avgUeRrcConn = t.avgUeRrcConn + int(rec.avgUeRrcConn)
                    t.maxUeRrcConn = max(t.maxUeRrcConn, int(rec.maxUeRrcConn))
                    t.avgUeAct = t.avgUeAct + int(rec.avgUeAct)
                    t.maxUeAct = max(t.maxUeAct, int(rec.maxUeAct))
                    cnt = cnt + 1
                except Exception as e:
                    #ignore ValueError that may raised by int()
                    continue
                
            if cnt > 0:
                t.avgUeRrcConn = round(t.avgUeRrcConn / cnt, 2)
                t.avgUeAct = round(t.avgUeAct / cnt, 2)
            else:
                t.avgUeRrcConn, t.avgUeAct = ('DIV0', 'DIV0')
            
            self.m8051AggData[key] = t
                
        '''
        for key,val in self.m8051AggData.items():
            print('key=%s,val=%s' % (key,val))
        '''
    
    def aggM8015(self):
        #print('Aggregating M8015')
        self.ngwin.logEdit.append('Aggregating M8015')
        qApp.processEvents()
        
        for key,val in self.m8015Data.items():
            t = M8015()
            for rec in val:
                try:
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
                except Exception as e:
                    #ignore ValueError that may raised by int()
                    continue
            
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
            self.lnbtsIdLncelIdMap[val.eci] = val.lnbtsId + '_' + key
            
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
        with open(os.path.join(outDir, 'm8015_per_earfcn_%s.csv' % time.strftime('%Y%m%d_%H%M%S', time.localtime())), 'w') as f:
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
        with open(os.path.join(outDir, 'm8015_topn_%s.csv' % time.strftime('%Y%m%d_%H%M%S', time.localtime())), 'w') as f:
            self.ngwin.logEdit.append('-->Exporting results to: %s' % f.name)
            qApp.processEvents()
                    
            header = ['DN','SRC_ENB_ID', 'SRC_LCR_ID', 'SRC_EARFCN', 'SRC_PCI', 'SRC_TAC', 'DST_ENB_ID', 'DST_LCR_ID', 'DST_EARFCN', 'DST_PCI', 'DST_TAC']
            header.extend(['IA_HO_PREP_FAIL', 'IA_HO_ATT', 'IA_HO_SUCC', 'IR_HO_PREP_FAIL', 'IR_HO_ATT', 'IR_HO_SUCC', 'HO_ATT_TOT', 'HO_SUCC_TOT', 'HO_PREP_FAIL', 'HO_EXEC_FAIL', 'HOSR2(%)', 'MRO_LATE_HO', 'MRO_EARLY_HO', 'MRO_PPONG_HO'])
            header.extend(['DN_LNADJ', 'X2_STAT'])
            header.extend(['DN_LNREL', 'CIO', 'HO_ALLOWED'])
            header.extend(['IA_A3', 'IA_A5', 'IF_A2', 'IF_A1'])
            header.extend(['DN_LNHOIF', 'IF_A3', 'IF_A5'])
            header.extend(['SRC_ERAB_REL_UEL_QCI1', 'SRC_ERAB_REL_HOFAIL_QCI1'])
            header.extend(['DST_NUM_MSG1', 'DST_NUM_MSG2', 'DST_RRC_MSG3', 'DST_RRC_MSG5', 'DST_RASR_MSG2', 'DST_RASR_MSG3', 'DST_RRC_SSR'])
            header.extend(['DST_DRB_ATT', 'DST_DRB_SUCC', 'DST_DRB_FAIL_TIM', 'DST_DRB_FAIL_OTH', 'DST_ERAB_ATT', 'DST_ERAB_SUCC',
                           'DST_ERAB_FAIL_RRNA', 'DST_ERAB_FAIL_TRU', 'DST_ERAB_FAIL_UEL', 'DST_ERAB_FAIL_RIP', 'DST_ERAB_FAIL_UP', 'DST_ERAB_FAIL_MOB', 'DST_ERAB_FAIL_OTH'])
            header.extend(['DST_AVG_UE_RRC_CONN', 'DST_MAX_UE_RRC_CONN', 'DST_AVG_UE_ACT', 'DST_MAX_UE_ACT'])
            header.extend(['DST_RSSI_PUCCH', 'DST_SINR_PUCCH', 'DST_RSSI_PUSCH', 'DST_SINR_PUSCH'])
            header.extend(['IS_GRID'])
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
                
                #erab abnormal release(cause=ue_lost or ho_fail) for qci1, source cell only
                m8006Key = val.lnbtsId + '_' + val.lncelId
                if m8006Key in self.m8006AggData:
                    ueLost = self.m8006AggData[m8006Key].erabRelQci1UeLost
                    hoFail = self.m8006AggData[m8006Key].erabRelQci1HoFail
                else:
                    ueLost, hoFail = ('NA', 'NA')
                line.extend([ueLost, hoFail])
                
                msg1, msg2, msg3, msg5, rasrMsg2, rasrMsg3, rrcSsr = ('NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA')
                drbAtt, drbSucc, drbFailTim, drbFailOth = ('NA', 'NA', 'NA', 'NA')
                erabAtt, erabSucc, erabFailRrna, erabFailTru, erabFailUel, erabFailRip, erabFailUp, erabFailMob, erabFailOth = ('NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA')
                avgUeRrc, maxUeRrc, avgUeAct, maxUeAct = ('NA', 'NA', 'NA', 'NA')
                rssiPucch, sinrPucch, rssiPusch, sinrPusch = ('NA', 'NA', 'NA', 'NA')
                if eciDst in self.lnbtsIdLncelIdMap:
                    #msg1/2/3/5 count, target cell only
                    m8001Key = self.lnbtsIdLncelIdMap[eciDst]
                    m8013Key = self.lnbtsIdLncelIdMap[eciDst]
                    if m8001Key in self.m8001AggData and m8013Key in self.m8013AggData:
                        msg1 = self.m8001AggData[m8001Key].smallMsg1Att + self.m8001AggData[m8001Key].largeMsg1Att + self.m8001AggData[m8001Key].dedMsg1Att
                        msg2 = self.m8001AggData[m8001Key].rachMsg2
                        msg3 = self.m8013AggData[m8013Key].rrcMsg3Mos + self.m8013AggData[m8013Key].rrcMsg3Mt + self.m8013AggData[m8013Key].rrcMsg3Mod + self.m8013AggData[m8013Key].rrcMsg3Emg + self.m8013AggData[m8013Key].rrcMsg3HiPrio + self.m8013AggData[m8013Key].rrcMsg3DelTol
                        msg5 = self.m8013AggData[m8013Key].rrcMsg5
                        rasrMsg2 = round(100 * msg2 / msg1, 2) if msg1 > 0 else 'DIV0'
                        rasrMsg3 = round(100 * msg3 / msg1, 2) if msg1 > 0 else 'DIV0'
                        rrcSsr = round(100 * msg5 / msg3, 2) if msg3 > 0 else 'DIV0'

                    #drb/erab setup count, target cell only
                    m8006Key = self.lnbtsIdLncelIdMap[eciDst]
                    m8007Key = self.lnbtsIdLncelIdMap[eciDst]
                    if m8006Key in self.m8006AggData and m8007Key in self.m8006AggData:
                        drbAtt = self.m8007AggData[m8007Key].drbSetupAtt
                        drbSucc = self.m8007AggData[m8007Key].drbSetupSucc
                        drbFailTim = self.m8007AggData[m8007Key].drbSetupFailTimer
                        drbFailOth = drbAtt - drbSucc - drbFailTim
                        erabAtt = self.m8006AggData[m8006Key].erabSetupAtt
                        erabSucc = self.m8006AggData[m8006Key].erabSetupSucc
                        erabFailRrna = self.m8006AggData[m8006Key].erabSetupFailRrna
                        erabFailTru = self.m8006AggData[m8006Key].erabSetupFailTru
                        erabFailUel = self.m8006AggData[m8006Key].erabSetupFailUel
                        erabFailRip = self.m8006AggData[m8006Key].erabSetupFailRip
                        erabFailUp = self.m8006AggData[m8006Key].erabSetupFailUp
                        erabFailMob = self.m8006AggData[m8006Key].erabSetupFailMob
                        erabFailOth = self.m8006AggData[m8006Key].erabSetupFailOth

                    #rrc_connected/active ue count, target cell only
                    m8051Key = self.lnbtsIdLncelIdMap[eciDst]
                    if m8051Key in self.m8051AggData:
                        avgUeRrc = self.m8051AggData[m8051Key].avgUeRrcConn
                        maxUeRrc = self.m8051AggData[m8051Key].maxUeRrcConn
                        avgUeAct = self.m8051AggData[m8051Key].avgUeAct
                        maxUeAct = self.m8051AggData[m8051Key].maxUeAct
                    
                    #pucch/pusch rssi/sinr, target cell only
                    m8005Key = self.lnbtsIdLncelIdMap[eciDst]
                    if m8005Key in self.m8005AggData:
                        rssiPucch = self.m8005AggData[m8005Key].avgRssiPucch
                        sinrPucch = self.m8005AggData[m8005Key].avgSinrPucch
                        rssiPusch = self.m8005AggData[m8005Key].avgRssiPusch
                        sinrPusch = self.m8005AggData[m8005Key].avgSinrPusch
                        
                line.extend([msg1, msg2, msg3, msg5, rasrMsg2, rasrMsg3, rrcSsr])
                line.extend([avgUeRrc, maxUeRrc, avgUeAct, maxUeAct])
                line.extend([rssiPucch, sinrPucch, rssiPusch, sinrPusch])
                
                #for ATU grid info
                gridSrcKey = str(enbIdSrc) + '_' + str(lcrIdSrc)
                gridDstKey = str(enbIdDst) + '_' + str(lcrIdDst)
                if gridSrcKey in self.gridData:
                    isGrid = 'YES'
                else:
                    isGrid = 'NO'
                isGrid = isGrid + '_'
                if gridDstKey in self.gridData:
                    isGrid = isGrid + 'YES'
                else:
                    isGrid = isGrid + 'NO'
                line.extend([isGrid])
                
                line = list(map(str, line))
                f.write(','.join(line))
                f.write('\n')
                
    def procUserCase03(self):
        self.ngwin.logEdit.append('<font color=blue>Performing analysis for user case #03: clean LNADJ/LNREL</font>')
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
            
    def procUserCase04(self):
        self.ngwin.logEdit.append('<font color=blue>Performing analysis for user case #04: lnhoif/irfim configuration analysis</font>')
        qApp.processEvents()
        
        earfcnSet = ['37900', '38098', '38400', '38544', '38950', '39148']
        
        #check LNHOIF
        for key in self.lnhoifData.keys():
            tokens = key.split('_')
            lncelId = tokens[0]
            earfcn = tokens[1]
            
            if earfcn == 'None':
                continue
            
            if lncelId in self.lncelData:
                dn = self.lncelData[lncelId].enbId + '_' + self.lncelData[lncelId].lcrId
                if not dn in self.earfcnLnhoif:
                    self.earfcnLnhoif[dn] = [earfcn]
                else:
                    self.earfcnLnhoif[dn].append(earfcn)
        
        #check IRFIM
        invalidIrfim = ['ENBID,LCRID,EARFCN,IRFIM_DN,IF_EARFCN,IF_RES_PRIO,IF_RXLEV_MIN,IF_TH_LOW,IF_TH_HIGH,IF_MBW']
        for key in self.irfimData.keys():
            tokens = key.split('_')
            lncelId = tokens[0]
            earfcn = tokens[1]
            
            if earfcn == 'None':
                continue
            
            if lncelId in self.lncelData:
                if earfcn == self.lncelData[lncelId].earfcn:
                    #invalid IRFIM founded
                    invalidIrfim.append(','.join([self.lncelData[lncelId].enbId, self.lncelData[lncelId].lcrId, self.lncelData[lncelId].earfcn, str(self.irfimData[key])]))
                    continue
                    
                dn = self.lncelData[lncelId].enbId + '_' + self.lncelData[lncelId].lcrId
                if not dn in self.earfcnIrfim:
                    self.earfcnIrfim[dn] = [earfcn]
                else:
                    self.earfcnIrfim[dn].append(earfcn)
                    
        outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        with open(os.path.join(outDir, 'lnhoif_irfim_check_%s.csv' % time.strftime('%Y%m%d_%H%M%S', time.localtime())), 'w') as f:
            self.ngwin.logEdit.append('-->Exporting results to: %s' % f.name)
            qApp.processEvents()
            
            header = ['ENBID', 'LCRID', 'EARFCN', 'LNHOIF_EARFCN', 'MISSED_LNHOIF_EARFCN', 'IRFIM_EARFCN', 'MISSED_IRFIM_EARFCN']
            f.write(','.join(header))
            f.write('\n')
            
            for key,val in self.lncelData.items():
                dn = val.enbId + '_' + val.lcrId
                if not dn in self.earfcnLnhoif and not dn in self.earfcnLnhoif:
                    continue
                
                line = [val.enbId, val.lcrId, val.earfcn]
                
                if dn in self.earfcnLnhoif:
                    configued = '/'.join(self.earfcnLnhoif[dn])
                    #missed = '/'.join([f for f in earfcnSet if not f in self.earfcnLnhoif[dn] and f != val.earfcn])
                    missed = [f for f in earfcnSet if not f in self.earfcnLnhoif[dn] and f != val.earfcn]
                    #special handling for band 38/41
                    if val.earfcn == '40540':
                        missed.remove('37900')
                    elif val.earfcn == '40738':
                        missed.remove('38098')
                    missed = '/'.join(missed)
                    
                    line.extend([configued, missed])
                else:
                    line.extend(['NA', 'NA'])
                
                if dn in self.earfcnIrfim:
                    configued = '/'.join(self.earfcnIrfim[dn])
                    #missed = '/'.join([f for f in earfcnSet if not f in self.earfcnIrfim[dn] and f != val.earfcn])
                    missed = [f for f in earfcnSet if not f in self.earfcnIrfim[dn] and f != val.earfcn]
                    #special handling for band 38/41
                    if val.earfcn == '40540':
                        missed.remove('37900')
                    elif val.earfcn == '40738':
                        missed.remove('38098')
                    missed = '/'.join(missed)
                    
                    line.extend([configued, missed])
                else:
                    line.extend(['NA', 'NA'])
                
                f.write(','.join(line))
                f.write('\n')
        
        if len(invalidIrfim) > 1:
            with open(os.path.join(outDir, 'irfim_problem_%s.csv' % time.strftime('%Y%m%d_%H%M%S', time.localtime())), 'w') as f:
                self.ngwin.logEdit.append('-->Exporting results to: %s' % f.name)
                qApp.processEvents()
                for val in invalidIrfim:
                    f.write(val)
                    f.write('\n')
                
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
