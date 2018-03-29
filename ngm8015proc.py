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

class SrcRawData(object):
    def __init__(self):
        self.lnbtsId = None #bts.co_object_instance
        #self.lncel = None
        #self.lnhoif = None
        self.raw = dict() #[key=eci_id, val=DstRawData]

class DstRawData(object):
    def __init__(self):
        self.counters = dict() #[key=period_start_time, value=M8015]
        self.accumulated = None 
        #self.lnadj = None
        #self.lnrel = None

class M8015(object):
    def __init__(self):
        self.iaHoPrepFail = None
        self.iaHoAtt = None
        self.iaHoSucc = None
        self.iaHoFailTime = None
        self.irHoPerpFailOth = None
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

class Lncel(object):
    def __init__(self):
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

class Lnadj(object):
    def __init__(self):
        self.coDn = None
        self.adjEnbId = None
        self.adjEnbIp = None
        self.x2Stat = None

class Lnadjl(object):
    def __init__(self):
        self.coDn = None
        self.adjEnbId = None
        self.adjLcrId = None
        self.adjEarfcn = None
        self.adjPci = None
        self.adjTac = None
        
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
        
class Lnrel(object):
    def __init__(self):
        self.coDn = None
        self.adjEnbId = None
        self.adjLcrId = None
        self.cio = None
        self.hoAllowed = None
        self.nrStat = None
        
class NgM8015Proc(object):
    def __init__(self):
        #connection defined as below:
        #rawData.key == lncelData.key
        #rawData.key == lnhoifData.key
        #rawData.key == lnrelData.key
        #rawData.val.lnbtsId == lnadjData.key
        #rawData.val.lnbtsId == lnadjlData.key
        self.rawData = dict() #[key=m8015.lncel_id, val=SrcRawData]
        self.lncelData = dict() #[key=lncel.lncel_id, val=Lncel]
        self.lnadjData = dict() #[key=lnadj.lnbts_id, val=Lnadj]
        self.lnadjlData = dict() #[key=lnadjl.lnbts_id, val=Lnadjl]
        self.lnhoifData = dict() #[key=lnhoif.lncel_id, val=Lnhoif]
        self.lnrelData = dict() #[key=lnrel.lncel_id, val=Lnrel]
        
