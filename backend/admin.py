from django.contrib import admin
from models import UserInfo,UserType,GroupInfo,DocumentType,DocumentInfo
# Register your models here.
admin.site.register(UserType) 
admin.site.register(UserInfo)
admin.site.register(GroupInfo)
admin.site.register(DocumentType)
admin.site.register(DocumentInfo)