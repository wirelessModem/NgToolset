#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngxmlparser.py
Description:
    Xml parser for Nokia scfc/vendor.
Change History:
    2018-2-5   v0.1    created.    github/zhenggao2
'''

from collections import OrderedDict
import xml.etree.ElementTree as ET
import os
import time
import ngmainwin


class NgXmlParser(object):
    def __init__(self, ngwin, inDir, outDir=None):
        self.ngwin = ngwin
        self.inDir = inDir
        if outDir is None:
            self.outDir = self.inDir 
        else:
            self.outDir = outDir
        self.data = OrderedDict()
    
    def start(self):
        ts = time.strftime('%Y%m%d%H%M%S', time.localtime()) 
        for root, dirs, files in os.walk(self.inDir):
            self.xmls = sorted([os.path.join(root, fn) for fn in files if fn.endswith('xml')], key=str.lower) 
            self.isScfc = False
            self.enbId = None
            for fn in self.xmls:
                self.data.clear()
                
                self.parseXml(fn)
                
                with open(os.path.join(self.outDir, 'xml_parsed_%s.dat' % ts), 'a') as f:
                    f.write('#%s\n' % fn)
                    for dn in self.data.keys():
                        f.write('$DN=%s\n' % dn)
                        for par, val in self.data[dn].items():
                            if isinstance(val, list):
                                f.write('%s=(%s)\n' % (par, ','.join(val)))
                            else:
                                f.write('%s=%s\n' % (par, val)) 
    
    def parseXml(self, fn):
        self.ngwin.logEdit.append('Parsing %s' % fn)
        
        bn = os.path.basename(fn).lower()
        if bn.startswith('scfc'):
            self.isScfc = True
        else:
            self.isScfc = False
        
        try:
            root = ET.parse(fn).getroot()
        except Exception as e:
            self.ngwin.logEdit.append("ERROR: fail to parse file: %s!" % fn)
            return
        
        '''
        self.ngwin.logEdit.append(root.tag, root.attrib)
        for child in root:
            self.ngwin.logEdit.append(child.tag, child.attrib)
        '''
        
        #xml with namespace
        xmlns = '{raml21.xsd}'
        cm = root.find(xmlns + 'cmData')
        for mo in cm.findall(xmlns + 'managedObject'):
            dn = mo.get('distName')
            tokens = dn.split('/')
            if self.isScfc and self.enbId is None:
                self.enbId = tokens[0].split('-')[-1]
            elif self.enbId is not None:
                dn = dn.replace('*', self.enbId)
            
            self.data[dn] = OrderedDict()
            for _list in mo.findall(xmlns + 'list'):
                listName = _list.get('name')
                for item in _list.findall(xmlns + 'item'):
                    for p in item.findall(xmlns + 'p'):
                        par = listName + '.' + p.get('name')
                        if par in self.data[dn]:
                            self.data[dn][par].append(p.text)
                        else:
                            self.data[dn][par] = [p.text]
            
            for p in mo.findall(xmlns + 'p'):
                par = p.get('name')
                self.data[dn][par] = p.text
