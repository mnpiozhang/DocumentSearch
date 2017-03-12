# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentinfo',
            name='attachment',
            field=models.FileField(upload_to=b'%Y/%m/%d', verbose_name='\u9644\u4ef6\u6587\u6863\u6587\u4ef6', blank=True),
        ),
    ]
