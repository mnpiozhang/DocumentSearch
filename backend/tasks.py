#!/usr/bin/env python
# -*- coding:utf-8 -*-
from celery.decorators import task  
from celery.utils.log import get_task_logger  
from models import DocumentInfo
from indexhelper import get_file_absolute_path,import_txt_content,import_word_content,import_pdf_content
import traceback

logger = get_task_logger(__name__)  
 
@task(name="analyze_uploadfile_task")  
def analyze_uploadfile_task(id,flag):
    try:
        DocumentInfoObj = DocumentInfo.objects.get(id=id)
        DocumentInfoObj.indexstate = 'i'
        DocumentInfoObj.save()
        doc_title = DocumentInfoObj.docname
        doc_type = DocumentInfoObj.type.doctype
        doc_description = DocumentInfoObj.description
        file_absolute_path = get_file_absolute_path(DocumentInfoObj.attachment)
        #判断文件flag
        if flag == 'txt':
            index_result = import_txt_content(id,doc_title,doc_type,doc_description,file_absolute_path)
        elif flag == 'word':
            index_result = import_word_content(id,doc_title,doc_type,doc_description,file_absolute_path)
        elif flag == 'pdf':
            index_result = import_pdf_content(id,doc_title,doc_type,doc_description,file_absolute_path)
        else:
            index_result = None
        if index_result:
            print '索引成功'
            DocumentInfoObj.indexstate = 's'
            DocumentInfoObj.save()
    except Exception,e:
        DocumentInfoObj.indexstate = 'f'
        DocumentInfoObj.save()
        print e
        print '索引失败'
        print traceback.format_exc()


