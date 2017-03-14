#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.test import TestCase


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