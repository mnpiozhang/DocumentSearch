"""ttt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from views import login,logout,index,submit_doc,big_file_download,batch_del_doc,del_doc,edit

urlpatterns = [
               url(r'^login/', login),
               url(r'^logout/', logout),
               url(r'^index/(\d*)', index),
               url(r'^submit/', submit_doc),
               url(r'^download/(?P<attachmentid>\d+)/$',big_file_download),
               url(r'^batchdel/',batch_del_doc),
               url(r'^del/(?P<id>\w+)/$',del_doc),
               url(r'^edit/(?P<id>\d+)/$',edit),
]
