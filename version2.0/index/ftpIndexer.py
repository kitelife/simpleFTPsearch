#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import bsddb
import pyinotify
import logging
import config

LOG_FILEANME = "index.log"
logging.basicConfig(filename=LOG_FILEANME, level=logging.INFO)

def list_dir(rootPath, dbFile):

    db = bsddb.btopen(dbFile,'w')

    for root, dirs, files in os.walk(rootPath):
        for directory in dirs:
            if not root.endswith('/'):
                root += '/'
            db[root+directory] = directory
            logging.debug(root+directory)
        for fi in files:
            if not root.endswith('/'):
                root += '/'
            db[root+fi] = fi
            logging.debug(root+fi)
    db.close()

class process_handler(pyinotify.ProcessEvent):
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
        logging.info('Create ' + event.path + '/' + event.name)

    def process_IN_DELETE(self, event):
        if self.dbConnect.exists(event.path + '/' + event.name):
            self.dbConnect.delete(event.path + '/' + event.name)
            self.dbConnect.sync()
        logging.info('Delete ' + event.path + '/' + event.name)

    def process_IN_MOVED_FROM(self, event):
        if self.dbConnect.exists(event.path + '/' + event.name):
            self.dbConnect.delete(event.path + '/' + event.name)
            self.dbConnect.sync()
        logging.info(event.name + ' move from ' + event.path)

    def process_IN_MOVED_TO(self, event):

        self.dbConnect.put(event.path + '/' + event.name, event.name)
        self.dbConnect.sync()
        logging.info(event.name + ' move to ' + event.path)

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
                list_dir(directory, dbFile)

    ph = process_handler(dbFile)
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, default_proc_fun=ph)
    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MOVED_FROM | pyinotify.IN_MOVED_TO
    for directory in config.listenDirs:
        wm.add_watch(directory, mask, rec=True, auto_add=True)
    '''由于内核对文件系统的实时监听功能有文件/目录数目配额的，默认貌似有点小(8192)，
    当需要监听的ftp目录文件比较多时，监听在初始化时就会抛出Error，只要将配额适当改得大些就没问题了。
    type sysctl -n fs.inotify.max_user_watches to read your current limit 
    and type sysctl -n -w fs.inotify.max_user_watches=16384 to modify (increase) it.
    '''
    notifier.loop();
