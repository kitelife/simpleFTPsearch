#!/usr/bin/python

#-*- coding: utf-8 -*-

import sys
import os
import time

import operationOnMySQL
import operateLog
#-----------------------------------
host = 'xxxx'
userName = 'xxxx'
passwd = 'xxxx'
dbName = 'dataforftpsearch'
chroot1 = 'xxxx'
chroot2 = 'xxxx'
url = 'ftp://xxxx:xxx'
#-----------------------------------

def listFileInThisDir(directory):

	operateMySQL = operationOnMySQL.MySQLdbOperation(host, userName, passwd,dbName)
	operateMySQL.dropTable('filelist')
	operateMySQL.createTable()

	for root, dirs, files in os.walk(directory):
		for fi in files:
			filePath = root + '/' + fi
			filePath = filePath.replace('//','/')
			fileInfo = os.stat(filePath)
			if chroot1 in filePath:
				filePath = filePath.replace(chroot1,url)
			else:
				filePath = filePath.replace(chroot2,url)
			timeInlist = list(time.localtime(fileInfo.st_ctime)[:6])
			lenOfTimeList = len(timeInlist)
			for index in range(lenOfTimeList):
				timeInlist[index] = str(timeInlist[index])
			fileTime = '-'.join(timeInlist)

			operateMySQL.addData(fi, filePath, fileTime)

	operateMySQL.closeLink()

if __name__ == '__main__':
	
	beginMessage = '***** Begin list FTP directory at : ' + time.ctime() + ' *****\n'
	operateLog.writeLog(beginMessage)

	listFileInThisDir('/var/ftp/')
	
	endMessage = '##### End list FTP directory at: ' + time.ctime() + ' #####\n'
	operateLog.writeLog(endMessage)
