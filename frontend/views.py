#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response,redirect
from django.template.context import RequestContext
from backend.indexhelper import search_result

def search(request):
    ret = {'Search':None,'Hit':0,'Doc':None}
    if request.method == 'POST':
        search = request.POST.get('search',None)
        if search == "":
            return render_to_response('search.html',ret,context_instance=RequestContext(request))

        result = search_result(search)
        hitcount = result["hits"]["total"]
        if hitcount == 0:
            ret = {'Search':search,'Hit':0,'Doc':None}
        else:
            hitcount = 0
            DocLst = []
            for i in result["hits"]["hits"]:
                tmpdict = {}
                tmpdict['id'] = i['_id']
                tmpdict['title'] = i['_source']['docname']
                tmpdict['description'] = i['_source']['description']
                tmpdict['filepath'] = i['_source']['filepath']
                DocLst.append(tmpdict)
                hitcount = hitcount +1
            ret = {'Search':search,'Hit':hitcount,'Doc':DocLst}
        return render_to_response('search.html',ret,context_instance=RequestContext(request))
    else:
        return render_to_response('search.html',ret,context_instance=RequestContext(request))


