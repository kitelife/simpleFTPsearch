#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import bsddb
import config

def search(keyWord):
    db = bsddb.btopen(config.dbFile, 'r')
    countAll = 0
    countResult=0
    for key, value in db.iteritems():
        countAll += 1
        if keyWord.lower() in value.lower():
            countResult += 1
            print value,'--->',key
    db.close()
    print 'All Num:', countAll
    print 'Result Num:',countResult

if __name__ == '__main__':
    search(sys.argv[1])
