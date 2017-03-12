from django.contrib import admin
from models import UserInfo,UserType,GroupInfo
# Register your models here.
admin.site.register(UserType) 
admin.site.register(UserInfo)
admin.site.register(GroupInfo)