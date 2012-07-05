#!/usr/bin/env python
#-*- coding:utf-8 -*-

import cgi
import bsddb
import cgiConfig

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
    headerTemplate = "<head>%s</head>"
    bodyTemplate = "<body>%s%s</body>"

    abstract = "<p><h3>Result Num: %s</h3></p>" %countResult
    items = ""

    index = 1
    for key, value in resultDict.iteritems():
        items += "<p>%d.%s</p>" %(index, value)
        items += "<p><a href='%s' target='_blank'>%s</a></p>" %(key, key)
        index += 1

    header = headerTemplate % ("")
    body = bodyTemplate % (abstract, items)
    content = contentTemplate % (header, body)

print 'Content-Type: text/html'
print
print content