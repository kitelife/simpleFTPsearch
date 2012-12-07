#!/usr/bin/python
#-*- coding:utf-8 -*-
import cgi
import bsddb
import cgiConfig
import os
import logging

LOG_FILEANME = "search.log"
logging.basicConfig(filename=LOG_FILEANME, level=logging.INFO)
logging.info(os.environ['SERVER_NAME'])

form = cgi.FieldStorage()
keyWordValue = form.getvalue('searchterm')

if keyWordValue == None:
    content = "<h3>你的输入不能为空哦...</h3>"
else:
    db = bsddb.btopen(cgiConfig.dbFile, 'r')
    countAll = 0
    countResult=0
    resultDict = dict()
    for key, value in db.iteritems():
        countAll += 1
        if keyWordValue.lower() in value.lower():
            resultDict[key] = value
            countResult += 1
    db.close()

    contentTemplate = "<html>%s%s</html>"
    headerTemplate = '''<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />%s</head>'''
    bodyTemplate = "<body>%s%s</body>"

    abstract = "<div class='abstract'><h3>Result Num: %s</h3></div>" %countResult
    items = "<div class='results'>"

    index = 1
    for key, value in resultDict.iteritems():
	   for root_path in cgiConfig.root_list:
	       if root_path in key:
		      key = key.replace(root_path, "ftp://" + os.environ['SERVER_NAME'])
        items += "<p>%d.%s</p>" %(index, value)
        items += "<p><a href='%s' target='_blank'>%s</a></p>" %(key, key)
        index += 1
    items += "</div>"
    googlewebfonts = "<link href='http://fonts.googleapis.com/css?family=Bitter:400,700,400italic&subset=latin,latin-ext' rel='stylesheet' type='text/css'>"
    cssFile = "<link href='../css/style.css' rel='stylesheet' type='text/css'>"
    headString = googlewebfonts + cssFile
    header = headerTemplate % (headString)
    body = bodyTemplate % (abstract, items)
    content = contentTemplate % (header, body)

print 'Content-Type: text/html;'
print
print content
