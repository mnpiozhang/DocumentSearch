#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import platform
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def attachment_format(value):
    sys_type = platform.system()
    if sys_type == 'Windows':
        #return value.split("\\")[-1]
        return value.split("/")[-1]
    else:
        return value.split("/")[-1]


