#!/usr/bin/python3
# -*- encoding: utf-8 -*-

'''
File:
    ngsqlquery.py
Description:
    SQL query utilty using cx_Oracle library .
Change History:
    2018-3-22   v0.1    created.    github/zhenggao2
'''

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import qApp
import cx_Oracle
import os
import re
from ngsqlsubui import NgSqlSubUi

class NgSqlQuery(object):
    def __init__(self, ngwin, args):
        self.ngwin = ngwin
        self.args = args
        self.stat = False
        self.initDb()
    
    def initDb(self):
        confDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
        with open(os.path.join(confDir, self.args['dbConf']), 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                if line.startswith('#') or line.strip() == '':
                    continue
                
                tokens = line.split('=')
                tokens = list(map(lambda x:x.strip(), tokens))
                if len(tokens) == 2:
                    if tokens[0].upper() == 'HOST_NAME':
                        self.dbHost = tokens[1]
                    elif tokens[0].upper() == 'TCP_PORT':
                        self.dbPort = tokens[1]
                    elif tokens[0].upper() == 'DB_NAME':
                        self.dbService = tokens[1]
                    elif tokens[0].upper() == 'USER_NAME':
                        self.dbUserName = tokens[1]
                    elif tokens[0].upper() == 'USER_PASSCODE':
                        self.dbUserPwd = tokens[1]
    
    def exec_(self):
        dsn = cx_Oracle.makedsn(self.dbHost, self.dbPort, service_name=self.dbService)
        
        self.ngwin.logEdit.append('<font color=blue>Connecting to Oracle DB</font>(DSN=%s)' % dsn)
        qApp.processEvents()
        try:
            db = cx_Oracle.connect(self.dbUserName, self.dbUserPwd, dsn)
        except cx_Oracle.DatabaseError as e:
            # cx_Oracle 5.0.4 raises a cx_Oracle.DatabaseError exception
            # with the following attributes and values:
            #  code = 2091
            #  message = 'ORA-02091: transaction rolled back
            #            'ORA-02291: integrity constraint (TEST_DJANGOTEST.SYS
            #               _C00102056) violated - parent key not found'
            self.ngwin.logEdit.append('<font color=red>cx_Oracle.DatabaseError: %s!</font>' % e.args[0].message)
            return
            
        cursor = db.cursor()
        
        sqlDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sql')
        for sqlFn in self.args['sqlQuery']:
            with open(os.path.join(sqlDir, sqlFn), 'r') as f:
                self.ngwin.logEdit.append('<font color=blue>Executing query: %s</font>' % f.name)
                qApp.processEvents()
                
                self.names = []
                self.answers = []
                reSql = re.compile(r"^[a-zA-Z0-9\_\s\>\<\=\(]+\&([a-zA-Z\_]+)[\,\s\'a-zA-Z0-9\)]+$")
                while True:
                    line = f.readline()
                    if not line:
                        break
                    
                    #substitute names if necessary
                    m = reSql.match(line)
                    if m is not None:
                        self.names.extend(m.groups())
                        
                f.seek(0)
                query = f.read()
                if len(self.names) > 0:
                    dlg = NgSqlSubUi(self.ngwin, self.names)
                    if dlg.exec_() == QDialog.Accepted:
                        self.answers = dlg.answers
                        valid = True
                        for an in self.answers:
                            if len(an) == 0:
                                valid = False
                                break
                        if not valid:
                            self.ngwin.logEdit.append('<font color=red>-->Query skipped!</font>')
                            qApp.processEvents()
                            continue
                        
                        if self.ngwin.enableDebug:
                            for name,answer in zip(self.names, self.answers):
                                self.ngwin.logEdit.append('-->Subsitution: %s=%s' % (name, answer))
                            qApp.processEvents()
                            
                        for index,name in enumerate(self.names):
                            query = query.replace('&'+name, "'"+self.answers[index]+"'")
                    else:
                        self.ngwin.logEdit.append('<font color=red>-->Query skipped!</font>')
                        qApp.processEvents()
                        continue
                
                try:
                    cursor.execute(query)
                except cx_Oracle.DatabaseError as e:
                    self.ngwin.logEdit.append('<font color=red>cx_Oracle.DatabaseError: %s!</font>' % e.args[0].message)
                    return
                
                fields = ','.join([a[0] for a in cursor.description])
                #self.ngwin.logEdit.append('Fields: %s' % fields)
                
                #record = cursor.fetchone()
                #self.ngwin.logEdit.append(','.join([str(i) for i in record]))
                records = cursor.fetchall()
                
                outDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
                outFn = sqlFn.replace('.sql', '.csv')
                with open(os.path.join(outDir, outFn), 'w') as of:
                    self.ngwin.logEdit.append('-->Exporting query results to: %s' % of.name)
                    qApp.processEvents()
                    
                    of.write(fields)
                    of.write('\n')
                    for r in records:
                        of.write(','.join([str(token) for token in r]))
                        of.write('\n')
        
        self.stat = True
        self.ngwin.logEdit.append('<font color=blue>Done!</font>')
