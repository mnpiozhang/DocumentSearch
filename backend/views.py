#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.template.context_processors import csrf
from django.shortcuts import redirect,HttpResponse,render_to_response,render
from django.http.response import StreamingHttpResponse,HttpResponseRedirect,HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from models import UserInfo,DocumentInfo
from forms import DocumentForm
from decorators import is_login_auth
import platform,os
from utils.common  import  Page,page_div,query_page_div,get_doc_page_info,filenameJudge
from DocumentSearch import settings
import datetime
from django.db.models import Q
from tasks import analyze_uploadfile_task
from indexhelper import del_es_doc
import os
# Create your views here.

#登陆
@csrf_exempt
def login(request):
# Create your views here.
    ret = {'status':''}
    if request.method == 'POST':
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        is_not_empty=all([username,password])
        if is_not_empty:
            count = UserInfo.objects.filter(username=username,password=password).count()
            #判断输入用户名密码OK，则跳转到主页面
            if count == 1:
                request.session['username'] = username
                request.session['login_auth'] = True
                #logging.info("user login : {}".format(username))
                return redirect('/backend/index/')
            else:
                ret['status']='password error'
        else:
            ret['status']='can not empty'
    return render_to_response('login.html',ret)


#登出
@is_login_auth
def logout(request):
    #logging.info("user logout : {}".format(request.session['username']))
    del request.session['login_auth']
    del request.session['username']
    return redirect("/backend/login/")


#首页
@is_login_auth
def index(request,page=1):
    ret = {'DocumentInfoObj':None,'UserInfoObj':None,'PageInfo':None,'AllCount':None}
    try:
        page = int(page)
    except Exception:
        page = 1
    if request.method == 'GET':
        #查询页面的分页显示
        if request.GET.get('issearch',None):
            searchindexstate = request.GET.get('searchindexstate',None)
            tmpstarttime = request.GET.get('searchstarttime',None)
            tmpendtime = request.GET.get('searchendtime',None)
            Qset = {}
            Qset['indexstate'] = searchindexstate
            Qset['searchstarttime'] = tmpstarttime
            Qset['searchendtime'] = tmpendtime

            #判断是否输入了开始时间，没输入或输入非法则默认为1970.01.01
            try:
                searchstarttime = datetime.datetime.strptime(tmpstarttime,'%Y-%m-%d')
            except:
                searchstarttime = datetime.datetime(1970, 1, 1)
            #判断是否输入了结束时间或输入非法，没输入或输入非法则默认为现在
            try:
                searchendtime = datetime.datetime.strptime(tmpendtime,'%Y-%m-%d')
            except:
                searchendtime = datetime.datetime.now()
            allDoc = DocumentInfo.objects.filter(
                                                 Q(indexstate__startswith=searchindexstate)
                                                 &Q(timestamp__gte=searchstarttime)
                                                 &Q(timestamp__lte=searchendtime)
                                                 )
            AllCount = allDoc.count()
            ret['AllCount'] = AllCount
            PageObj = Page(AllCount,page,6)
            DocumentInfoObj = allDoc[PageObj.begin:PageObj.end]
            pageurl = 'index'
            querycondition = request.META.get("QUERY_STRING",None)
            pageinfo = query_page_div(page, PageObj.all_page_count,pageurl,querycondition)
            ret['PageInfo'] = pageinfo
            ret['DocumentInfoObj'] = DocumentInfoObj
            UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
            ret['UserInfoObj'] = UserInfoObj
            ret['Qset'] = Qset
            print Qset
            return render_to_response('index.html',ret,context_instance=RequestContext(request))
        #正常主页的分页显示
        else:
            docPage = get_doc_page_info(DocumentInfo,page,'n')
            ret['AllCount'] = docPage['AllCount']
            ret['PageInfo'] = docPage['PageInfo']
            ret['DocumentInfoObj'] = docPage['DocumentInfoObj']
            UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
            ret['UserInfoObj'] = UserInfoObj
            return render_to_response('index.html',ret,context_instance=RequestContext(request))
    else:
        return HttpResponse("this is a web page , please use metod GET")


#提交新文档
@is_login_auth
def submit_doc(request):
    ret = {'UserName':None,'form':None,'UserInfoObj':None}
    ret['UserName'] = request.session.get('username',None)
    #WorkOrderObj = WorkOrder.objects.create()
    UserInfoObj = UserInfo.objects.get(username=ret['UserName'])
    ret['UserInfoObj'] = UserInfoObj
    if request.method == 'POST':
        DocumentObj_form = DocumentForm(request.POST,request.FILES)
        upload_filename = request.FILES['attachment'].name
        #django.core.files.uploadedfile.InMemoryUploadedFile
        fileSuffixObj = filenameJudge(upload_filename)
        file_flag = fileSuffixObj.suffix_judge()
        if DocumentObj_form.is_valid() and file_flag:
            DocumentObj = DocumentObj_form.save(commit=False)
            #索引状态放置为b即开始索引
            DocumentObj.indexstate = 'b'
            DocumentObj.save()
            analyze_uploadfile_task.delay(DocumentObj.id,file_flag)
            ret['status'] = 'save ok'
            
        else:
            ret['status'] = 'save error'
            ret['form'] = DocumentObj_form
            #添加跨站请求伪造的认证
            ret.update(csrf(request))
            return render(request,'submitdoc.html',ret)
            
    DocumentObj_form = DocumentForm()
    ret['form'] = DocumentObj_form
    #添加跨站请求伪造的认证
    ret.update(csrf(request))
    return render_to_response('submitdoc.html',ret)


#文件下载功能
@is_login_auth
def big_file_download(request,attachmentid):
    
    def _file_iterator(file_name, chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
                
    DocumentFileObj = DocumentInfo.objects.get(id=attachmentid)
    #获取系统类别
    sys_type = platform.system()
    
    if sys_type == 'Windows':
        #windows下使用
        the_file_name = str(settings.MEDIA_ROOT) + '\\' + str(DocumentFileObj.attachment).replace('/', '\\').decode('utf-8')
    elif sys_type == 'Linux':
        #linux下使用
        the_file_name = settings.MEDIA_ROOT + "/" + str(DocumentFileObj.attachment).decode('utf-8')
    else:
        #非linux或windows下，如unbantu等皆使用linux的标准
        the_file_name = settings.MEDIA_ROOT + "/" + str(DocumentFileObj.attachment).decode('utf-8')
    
    response = StreamingHttpResponse(_file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    
    if sys_type == 'Windows':
        #windows下使用
        response['Content-Disposition'] = 'attachment;filename=' + the_file_name.encode('gbk').split("\\")[-1]
    elif sys_type == 'Linux':
        #linux下使用
        response['Content-Disposition'] = 'attachment;filename=' + the_file_name.encode('gbk').split("/")[-1]
    else:
        #非linux或windows下，如unbantu等皆使用linux的标准
        response['Content-Disposition'] = 'attachment;filename=' + the_file_name.encode('gbk').split("/")[-1]
    
    return response

#批量删除主机信息
@is_login_auth
def batch_del_doc(request):
    if request.method == 'POST':
        #根据传进来的主机id批量删除数据库对象
        ret = {'DocumentInfoObj':None,'UserInfoObj':None,'PageInfo':None,'AllCount':None}
        will_del_doc = request.POST.getlist("checkboxdel[]",None)
        if will_del_doc:
            for i in will_del_doc:
                DocumentInfoObj = DocumentInfo.objects.get(id=i)
                DocumentInfoObj.delete()
                try:
                    del_es_doc(i)
                except Exception,e:
                    print e
                    print "del this doc id in es error,may be this doc id does not exist "
            ids = ",".join(will_del_doc)
            ret['popover'] = { "id":ids,"info":"已经删除以下编号的文档" }
        else:
            ret['popover'] = { "id":"","info":"没有选中可删除的文档" }
        page = 1
        docPage = get_doc_page_info(DocumentInfo,page,'n')
        ret['AllCount'] = docPage['AllCount']
        ret['PageInfo'] = docPage['PageInfo']
        ret['DocumentInfoObj'] = docPage['DocumentInfoObj']
        UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
        ret['UserInfoObj'] = UserInfoObj
        return render_to_response('index.html',ret,context_instance=RequestContext(request))
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
    
#删除文档信息
@is_login_auth
def del_doc(request,id):
    try:
        try:
            DocumentInfoObj = DocumentInfo.objects.get(id=id)
        except Exception,e:
            print e
            return HttpResponseRedirect('/backend/index')
        DocumentInfoObj.delete()
        try:
            del_es_doc(id)
        except Exception,e:
            print e
            print "del this doc id in es error,may be this doc id does not exist "
        ret = {'DocumentInfoObj':None,'UserInfoObj':None,'PageInfo':None,'AllCount':None}
        page = 1
        docPage = get_doc_page_info(DocumentInfo,page,'n')
        ret['AllCount'] = docPage['AllCount']
        ret['PageInfo'] = docPage['PageInfo']
        ret['DocumentInfoObj'] = docPage['DocumentInfoObj']
        UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
        ret['UserInfoObj'] = UserInfoObj
        ret['popover'] = { "id":id,"info":"已经删除文档" }
        return render_to_response('index.html',ret,context_instance=RequestContext(request))
    except Exception,e:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    
#编辑文档信息
@is_login_auth
def edit(request,id):
    ret = {'UserName':None,'form':None,'status':'','id':None,'UserInfoObj':None}
    DocumentInfoObj = DocumentInfo.objects.get(id=id)
    #print DocumentInfoObj.type
    if request.method == 'POST':
        DocumentInfoObj_form = DocumentForm(data=request.POST,files=request.FILES,instance=DocumentInfoObj)
        #print request.POST
        #print request.FILES['attachment'].name
        #print DocumentInfoObj.attachment
        #print str(DocumentInfoObj.attachment)
        #print DocumentInfoObj_form.attachment
        try:
            fileSuffixObj = filenameJudge(request.FILES['attachment'].name)
        except:
            fileSuffixObj = filenameJudge(os.path.basename(str(DocumentInfoObj.attachment)))
        file_flag = fileSuffixObj.suffix_judge()
        if DocumentInfoObj_form.is_valid() and file_flag:
            DocumentObj = DocumentInfoObj_form.save(commit=False)
            #索引状态放置为b即开始索引
            DocumentObj.indexstate = 'b'
            DocumentObj.save()
            analyze_uploadfile_task.delay(DocumentObj.id,file_flag)
            ret['status'] = '修改成功'
        else:
            ret['status'] = '修改失败'
            ret['form'] = DocumentInfoObj_form
            #添加跨站请求伪造的认证
            ret.update(csrf(request))
            return render(request,'edit.html',ret)
            
    DocumentInfoObj_form = DocumentForm(instance=DocumentInfoObj)
    ret['UserName'] = request.session.get('username',None)
    UserInfoObj = UserInfo.objects.get(username=ret['UserName'])
    ret['UserInfoObj'] = UserInfoObj
    ret['form'] = DocumentInfoObj_form
    ret['id'] = id
    #添加跨站请求伪造的认证
    ret.update(csrf(request))
    return render_to_response('edit.html',ret)