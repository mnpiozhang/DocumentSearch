#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.template.context_processors import csrf
from django.shortcuts import redirect,HttpResponse,render_to_response,render
from django.views.decorators.csrf import csrf_exempt
from models import UserInfo,DocumentInfo
from forms import DocumentForm
from decorators import is_login_auth
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
def index(request):
    ret = {'UserName':None,'UserInfoObj':None,'DocumentInfo':None}
    ret['UserName'] = request.session.get('username',None)
    UserInfoObj = UserInfo.objects.get(username=ret['UserName'])
    ret['UserInfoObj'] = UserInfoObj
    DocumentInfoObj = DocumentInfo.objects.all()
    ret['DocumentInfo'] = DocumentInfoObj
    #设置session超时时间
    #request.session.set_expiry(0)
    return render_to_response('index.html',ret)

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
    
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
                
    AttachmentsFileObj = Attachments.objects.get(id=attachmentid)
    #获取系统类别
    sys_type = platform.system()
    
    if sys_type == 'Windows':
        #windows下使用
        the_file_name = str(settings.MEDIA_ROOT) + '\\' + str(AttachmentsFileObj.attachment).replace('/', '\\').decode('utf-8')
    elif sys_type == 'Linux':
        #linux下使用
        the_file_name = settings.MEDIA_ROOT + "/" + str(AttachmentsFileObj.attachment).decode('utf-8')
    else:
        #非linux或windows下，如unbantu等皆使用linux的标准
        the_file_name = settings.MEDIA_ROOT + "/" + str(AttachmentsFileObj.attachment).decode('utf-8')
    
    response = StreamingHttpResponse(file_iterator(the_file_name))
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
