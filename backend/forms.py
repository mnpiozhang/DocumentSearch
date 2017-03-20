#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import forms
from models import DocumentInfo
from django.contrib.admin import widgets


class DocumentForm(forms.models.ModelForm):
    attachment = forms.FileField(allow_empty_file=False,error_messages={'required': '请上传文档文件'})
    def __init__(self, *args, **kwargs):
        super(DocumentForm,self).__init__(*args, **kwargs)
        self.fields['type'].choices =  list(self.fields["type"].choices)[1:] 
    class Meta:
        model = DocumentInfo
        fields = ('docname','description','attachment','type')
        widgets = {
                   'docname' : forms.TextInput(attrs={'placeholder':'文档名称必填'}),
                   'description' : forms.Textarea(attrs={'placeholder':'文档简要描述必填','class':'form-control','rows':10}),
                   'type': forms.Select(attrs={'placeholder':'文档类型必填'}),
                   }
        error_messages = {
                          'docname' :{'required':'请输入文档名称'},
                          'description' :{'required':'请简要填写文档描述，并作为第一搜索依据'},
                          'type': {'required':'请选择一个文档类型'},
                          }
