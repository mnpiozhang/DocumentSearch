#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response,redirect


def searchtitle(request):
    if request.method == 'POST':
        search = request.POST.get('search',None)
        if search == "":
            ret = {'Search':None,'Hit':0,'Doc':None}
            return render_to_response('search.html',ret,context_instance=RequestContext(request))

        result = search_result(search)
        hitcount = result["hits"]["total"]
        if hitcount == 0:
            ret = {'Search':search,'Hit':0,'Doc':None}
        else:
            #重新定义hitcount避免草稿的数量也统计进去.
            #如果搜索hit为1，但是命中的文章为草稿，则hitcount重置为0，无搜索结果
            hitcount = 0
            DocLst = []
            for i in result["hits"]["hits"]:
                #判断是否为草稿，草稿直接pass
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
        return redirect('/')


