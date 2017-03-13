#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.template.context_processors import csrf
from django.shortcuts import redirect,HttpResponse,render_to_response,render
from django.http.response import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.context import RequestContext
from models import UserInfo,DocumentInfo
from forms import DocumentForm
from decorators import is_login_auth
import platform,os
from utils.common  import  Page,page_div,query_page_div
from DocumentSearch import settings
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
            searchos = request.GET.get('searchos',None)
            searchhostname = request.GET.get('searchhostname',None)
            searchsn = request.GET.get('searchsn',None)
            searchpublish = request.GET.get('searchpublish',None)
            searchip = request.GET.get('searchip',None)
            tmpstarttime = request.GET.get('searchstarttime',None)
            tmpendtime = request.GET.get('searchendtime',None)
            Qset = {}
            Qset['searchos'] = searchos
            Qset['searchhostname'] = searchhostname
            Qset['searchsn'] = searchsn
            Qset['searchpublish'] = searchpublish
            Qset['searchip'] = searchip
            Qset['tmpstarttime'] = tmpstarttime
            Qset['tmpendtime'] = tmpendtime

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
            allServer = HostInfo.objects(Q(os__contains=searchos)
                                         &Q(networkinfo__addrlst__contains=searchip)
                                         &Q(hostname__contains=searchhostname)
                                         &Q(ispublish__contains=searchpublish)
                                         &Q(hardwareinfo__SN__contains=searchsn)
                                         &Q(timestamp__gte=searchstarttime)
                                         &Q(timestamp__lte=searchendtime))
            AllCount = allServer.count()
            ret['AllCount'] = AllCount
            PageObj = Page(AllCount,page,6)
            allServerObj = allServer[PageObj.begin:PageObj.end]
            pageurl = 'index'
            querycondition = request.META.get("QUERY_STRING",None)
            pageinfo = query_page_div(page, PageObj.all_page_count,pageurl,querycondition)
            ret['PageInfo'] = pageinfo
            ret['allServerObj'] = allServerObj
            UserInfoObj = UserInfo.objects.get(username=request.session.get('username',None))
            ret['UserInfoObj'] = UserInfoObj
            ret['Qset'] = Qset
            return render_to_response('index.html',ret,context_instance=RequestContext(request))
        #正常主页的分页显示
        else:
            allDoc = DocumentInfo.objects.all()
            AllCount = allDoc.count()
            ret['AllCount'] = AllCount
            PageObj = Page(AllCount,page,6)
            DocumentInfoObj = allDoc[PageObj.begin:PageObj.end]
            pageurl = 'index'
            pageinfo = page_div(page, PageObj.all_page_count,pageurl)
            ret['PageInfo'] = pageinfo
            ret['DocumentInfoObj'] = DocumentInfoObj
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
        if DocumentObj_form.is_valid():
            DocumentObj = DocumentObj_form.save(commit=False)
            #索引状态放置为s即开始所以
            DocumentObj.indexstate = 's'
            DocumentObj.save()

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
        with open(file_name) as f:
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
