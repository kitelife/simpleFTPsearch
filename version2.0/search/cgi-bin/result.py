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

contentTemplate = "<html>%s%s</html>"
headerTemplate = '''<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />%s</head>'''
bodyTemplate = r'''
<body>
    <div class="resultbody">
        <div id="search_form">
            %s
        </div>
        <div id="abstract_part">
            %s
        </div>
        <div id="result_items">
            %s
        </div>
    </div>
</body>
'''

googlewebfonts = "<link href='http://fonts.googleapis.com/css?family=Bitter:400,700,400italic&subset=latin,latin-ext' rel='stylesheet' type='text/css'>"
cssFile = r'''
<link rel="stylesheet" href="../css/bootstrap/bootstrap.min.css" type="text/css">
<link href="../css/style.css" rel="stylesheet" type="text/css">
'''

abstract = ''
items = ''

search_form = r'''
<form action="/cgi-bin/result.py" method="post" id="result_page_search_form">
    <div class="search_form_inner">
    <input name="searchterm" type="text" class="input_search">
    <button type="submit" class="btn btn-primary">搜 索</button>
    </div>
</form>
'''

form = cgi.FieldStorage()
keyWordValue = form.getvalue('searchterm')
if keyWordValue == None:
    abstract = "<div class='abstract'><h3>你的输入不能为空哦...</h3></div>"
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

    abstract = "<div class='abstract'><h3>Result Num: %s</h3></div>" %countResult
    items = "<div class='results'>"

    index = 1
    for key, value in resultDict.iteritems():
        for root_path in cgiConfig.root_list:
            if root_path in key:
                key = key.replace(root_path, "ftp://" + os.environ['SERVER_NAME'])
        items += "<div class='item'><p>%d. %s</p>" %(index, value)
        items += "<p><a href='%s' target='_blank'>%s</a></p></div>" %(key, key)
        index += 1
    items += "</div>"

headString = googlewebfonts + cssFile
header = headerTemplate % (headString)
body = bodyTemplate % (search_form, abstract, items)
content = contentTemplate % (header, body)

print 'Content-Type: text/html;'
print
print content
