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

import cx_Oracle
import os

class NgSqlQuery(object):
    def __init__(self, ngwin, args):
        self.ngwin = ngwin
        self.args = args
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
    
    def exec(self):
        dsn = cx_Oracle.makedsn(self.dbHost, self.dbPort, service_name=self.dbService)
        print(dsn)
        db = cx_Oracle.connect(self.dbUserName, self.dbUserPwd, dsn)
        cursor = db.cursor()
        
        sqlDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sql')
        for sqlFn in self.args['sqlQuery']:
            with open(os.path.join(sqlDir, sqlFn), 'r') as f:
                print('executing %s' % f.name)
                query = f.read()
                cursor.execute(query)
                
                fields = ','.join([a[0] for a in cursor.description])
                fields = 'INDEX,' + fields
                print(fields)
                records = cursor.fetchall()
                for i,r in enumerate(records):
                    print('%d: %s' % (i, r))
