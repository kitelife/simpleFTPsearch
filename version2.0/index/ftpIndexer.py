#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import bsddb
import pyinotify
import config

def listDir(rootPath, dbFile):

    db = bsddb.btopen(dbFile,'w')

    for root, dirs, files in os.walk(rootPath):
        #print root
        for directory in dirs:
            if not root.endswith('/'):
                root += '/'
            db[root+directory] = directory
        for fi in files:
            if not root.endswith('/'):
                root += '/'
            db[root+fi] = fi

    db.close()

class processHandler(pyinotify.ProcessEvent):
    def __init__(self, dbFile):
        pathParts = dbFile.split('/')
        self.dbName = pathParts[-1]
        self.dbPath = '/'.join(pathParts[0:-1])

        self.dbenv = bsddb.db.DBEnv()
        self.dbenv.open(self.dbPath, bsddb.db.DB_CREATE | bsddb.db.DB_INIT_MPOOL)
        self.dbConnect = bsddb.db.DB(self.dbenv)
        self.dbConnect.open(self.dbName, bsddb.db.DB_BTREE, bsddb.db.DB_CREATE, 0666)

    def process_IN_CREATE(self, event):

        self.dbConnect.put(event.path + '/' + event.name, event.name)
        self.dbConnect.sync()
        print 'Create ' + event.path + '/' + event.name

    def process_IN_DELETE(self, event):
        if self.dbConnect.exists(event.path + '/' + event.name):
            self.dbConnect.delete(event.path + '/' + event.name)
            self.dbConnect.sync()
        print 'Delete ' + event.path + '/' + event.name

    def process_IN_MOVED_FROM(self, event):
        if self.dbConnect.exists(event.path + '/' + event.name):
            self.dbConnect.delete(event.path + '/' + event.name)
            self.dbConnect.sync()
        print event.name, 'move from', event.path

    def process_IN_MOVED_TO(self, event):

        self.dbConnect.put(event.path + '/' + event.name, event.name)
        self.dbConnect.sync()
        print event.name, 'move to', event.path

if __name__ == '__main__':
    db = 'dbFile.db'
    if len(config.dbFile.split('/')) <= 1:
        dbFile = os.getcwd() + '/' + config.dbFile
    else:
        dbFile = config.dbFile

    if len(sys.argv) > 1:
        if sys.argv[1] == '-i':
            if os.path.exists(dbFile):
                os.remove(dbFile)
            for directory in config.listenDirs:
                listDir(directory, dbFile)

    ph = processHandler(dbFile)
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, default_proc_fun=ph)
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO
    for directory in config.listenDirs:
        wm.add_watch(directory, mask, rec=True, auto_add=True)

    notifier.loop();