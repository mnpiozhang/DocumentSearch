#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.test import TestCase

'''
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter
from cStringIO import StringIO
# Create your tests here.

retstr = StringIO()
rsrcmgr = PDFResourceManager()
laparams = LAParams()
codec = 'utf-8'
device = TextConverter(rsrcmgr,retstr,codec=codec,laparams=laparams)
with open('C:\\Users\\lenovo\\Downloads\\ReferenceCard.pdf'.decode("utf-8"), 'rb') as f:
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.get_pages(f):
        interpreter.process_page(page)
        
device.close()
str = retstr.getvalue()
retstr.close()
print str
'''

import json
#s={u'docname': u'\u6697\u5ba4\u9022\u706f', u'content': u'\n192.168.187.143   root\xc3\xdc\xc2\xeb\xa3\xbatysxwg\n\xb6\xcb\xbf\xda 6022\n\n\n192.168.23.62   root    fNFRNmWy6LD3wddeNQprxHMb$qHB\n\n192.168.73.59   6022 logview logview\n\n192.168.50.235  6022  logfiles logfiles#TYsx2012\n\n\n\n182.138.27.204 54077\n182.138.27.205 54077  1.\xcc\xec\xd2\xed\xca\xd3\xd1\xb6\xcd\xf8\xb9\xdc\n\ntysxwg\nTy_wg1q2w3e4r', u'description': u'\u6492\u5730\u65b9'}
#b = json.dumps(s)
#print b
bb = u'\u6492\u5730\u65b9'
#print bb.encode('utf-8')


ss = '\n192.168.187.143   root\xc3\xdc\xc2\xeb\xa3\xbatysxwg\n\xb6\xcb\xbf\xda 6022\n\n\n192.168.23.62   root    fNFRNmWy6LD3wddeNQprxHMb$qHB\n\n192.168.73.59   6022 logview logview\n\n192.168.50.235  6022  logfiles logfiles#TYsx2012\n\n\n\n182.138.27.204 54077\n182.138.27.205 54077  1.\xcc\xec\xd2\xed\xca\xd3\xd1\xb6\xcd\xf8\xb9\xdc\n\ntysxwg\nTy_wg1q2w3e4r'
#print unicode(ss.decode('gbk'))
#print ss.decode('gbk').encode('utf-8')

ccc=u'/home/hu/ds/DocumentSearch/media/2017/03/15/\u8bdd\u5355\u76d1\u63a7.docx'
print ccc.decode("utf-8")