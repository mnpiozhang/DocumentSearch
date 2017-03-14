#!/usr/bin/env python
# -*- coding:utf-8 -*-
import platform
from DocumentSearch import settings
import docx
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.converter import TextConverter
from cStringIO import StringIO

def get_file_absolute_path(relative_file):
    sys_type = platform.system()
    if sys_type == 'Windows':
        #windows下使用
        the_file_name = settings.MEDIA_ROOT + '\\' + str(relative_file).replace('/', '\\').decode('utf-8')
    elif sys_type == 'Linux':
        #linux下使用
        the_file_name = settings.MEDIA_ROOT + "/" + str(relative_file).decode('utf-8')
    else:
        #非linux或windows下，如unbantu等皆使用linux的标准
        the_file_name = settings.MEDIA_ROOT + "/" + str(relative_file).decode('utf-8')
    
    return the_file_name

#导入数据到elasticsearch
def sync_es(inputdict,idnum):
    es = Elasticsearch([settings.ES_URL])
    articlemapping = {
                      "mappings" : {
                                    "documentsearch" : {
                                                "_all": {
                                                        "analyzer": "ik_max_word",
                                                        "search_analyzer": "ik_max_word",
                                                        "term_vector": "no",
                                                        "store": "false"
                                                        },
                                                "properties" : {
                                                        "docname" : { 
                                                                    "type" : "string", 
                                                                    "analyzer": "ik_max_word",
                                                                    "search_analyzer": "ik_max_word",
                                                                    "include_in_all": "true",
                                                                    "boost": 8
                                                                    },
                                                        "description" : { 
                                                                    "type" : "string", 
                                                                    "analyzer": "ik_max_word",
                                                                    "search_analyzer": "ik_max_word",
                                                                    "include_in_all": "true",
                                                                    "boost": 8
                                                                    },
                                                        "content" : { 
                                                                    "type" : "string", 
                                                                    "analyzer": "ik_max_word",
                                                                    "search_analyzer": "ik_max_word",
                                                                    "include_in_all": "true",
                                                                    "boost": 8
                                                                    },
                                                                }
                                                 }
                                    }
                      }
    indexName = "documentIndex"
    if not es.indices.exists(indexName):
        es.indices.create(index = indexName, body = articlemapping,ignore = 400)
    return es.index(index=indexName, doc_type="documentsearch", body=inputdict, id=idnum)


def import_txt_content(id,doc_title,doc_description,filepath):
    with open(filepath.decode("utf-8"),'rU') as f:
        f_content = f.read()
    es_import_dict = {}
    es_import_dict['docname'] = doc_title
    es_import_dict['description'] = doc_description
    es_import_dict['content'] = f_content
    return sync_es(es_import_dict,id)

def import_word_content(id,doc_title,doc_description,filepath):
    document = docx.Document(filepath.decode("utf-8"))
    docText = '\n'.join([
                         paragraph.text.encode('utf-8') for paragraph in document.paragraphs
                         ])
    es_import_dict = {}
    es_import_dict['docname'] = doc_title
    es_import_dict['description'] = doc_description
    es_import_dict['content'] = docText
    return sync_es(es_import_dict,id)

def import_pdf_content(id,doc_title,doc_description,filepath):
    try:
        retstr = StringIO()
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        codec = 'utf-8'
        device = TextConverter(rsrcmgr,retstr,codec=codec,laparams=laparams)
        with open(filepath.decode("utf-8"), 'rb') as f:
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.get_pages(f):
                interpreter.process_page(page)
                
        device.close()
        str = retstr.getvalue()
        retstr.close()
    except Exception,e:
        print e
    es_import_dict = {}
    es_import_dict['docname'] = doc_title
    es_import_dict['description'] = doc_description
    es_import_dict['content'] = str
    return sync_es(es_import_dict,id)