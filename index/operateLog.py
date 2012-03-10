#!/usr/bin/python

#-*- coding: utf-8 -*-
_logs = 'LogForListFTP.txt'

def writeLog(message):
	logFile = open(_logs, 'a')
	logFile.write(message + '\n')
	logFile.close()
