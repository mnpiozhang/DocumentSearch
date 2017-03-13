#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from models import DocumentInfo
from django.contrib.admin import widgets


class DocumentForm(forms.models.ModelForm):
    
    class Meta:
        model = DocumentInfo
        fields = ('docname','description','attachment')
        widgets = {
                   'docname' : forms.TextInput(attrs={'placeholder':'文档名称必填'}),
                   'description' : forms.Textarea(attrs={'placeholder':'文档简要描述必填','class':'form-control','rows':10}),
                   }
        error_messages = {
                          'docname' :{'required':'请输入文档名称'},
                          'attachment' :{'required':'请上传文档文件'},
                          'description' :{'required':'请简要填写文档描述，并作为第一搜索依据'}
                          }
