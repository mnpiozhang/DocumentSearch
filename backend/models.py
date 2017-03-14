#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.db import models

# Create your models here.

class UserType(models.Model):
    typename= models.CharField(max_length=50,verbose_name = u'用户类型名称')
    def __unicode__(self):
        return self.typename

class GroupInfo(models.Model):
    groupname = models.CharField(max_length=50,verbose_name = u'组名称')
    groupname_abbreviate = models.CharField(max_length=10,verbose_name = u'组名称缩写')
    def __unicode__(self):
        return self.groupname

class UserInfo(models.Model):
    username = models.CharField(max_length=50,verbose_name = u'用户名')
    password = models.CharField(max_length=50,verbose_name = u'密码')
    type = models.ForeignKey('UserType',verbose_name = u'用户类型')
    realname = models.CharField(max_length=20,verbose_name = u'真实姓名')
    group = models.ForeignKey(GroupInfo,related_name='user_group',verbose_name = u'用户属组')
    telphone = models.CharField(max_length=12,verbose_name = u'用户电话')
    def __unicode__(self):
        return self.realname

INDEX_STATUS = (
                  ('b','begin index'),
                  ('i','indexing'),
                  ('f','index fail'),
                  ('s','index success'),
                    )

class DocumentInfo(models.Model):
    docname = models.CharField(max_length=50,verbose_name = u'文档名称')
    description = models.TextField(verbose_name = u'简单描述')
    timestamp = models.DateTimeField(auto_now_add = True,verbose_name = u'时间戳')
    modifiedtime = models.DateTimeField(auto_now = True,verbose_name = u'最近修改时间')
    indexstate = models.CharField(max_length=1, choices=INDEX_STATUS,default='s')
    attachment = models.FileField(upload_to='%Y/%m/%d',blank = True,verbose_name = u'附件文档文件')