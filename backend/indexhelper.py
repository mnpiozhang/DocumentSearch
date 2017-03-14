#!/usr/bin/env python
# -*- coding:utf-8 -*-
import platform
from DocumentSearch import settings

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



def import_txt_content(filepath):
    pass

def import_word_content(filepath):
    pass

def import_pdf_content(filepath):
    pass