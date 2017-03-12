# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docname', models.CharField(max_length=50, verbose_name='\u6587\u6863\u540d\u79f0')),
                ('description', models.TextField(verbose_name='\u7b80\u5355\u63cf\u8ff0')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='\u65f6\u95f4\u6233')),
                ('modifiedtime', models.DateTimeField(auto_now=True, verbose_name='\u6700\u8fd1\u4fee\u6539\u65f6\u95f4')),
                ('indexstate', models.CharField(default=b's', max_length=1, choices=[(b's', b'start index'), (b'i', b'indexing'), (b'f', b'index fail')])),
            ],
        ),
        migrations.CreateModel(
            name='GroupInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('groupname', models.CharField(max_length=50, verbose_name='\u7ec4\u540d\u79f0')),
                ('groupname_abbreviate', models.CharField(max_length=10, verbose_name='\u7ec4\u540d\u79f0\u7f29\u5199')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50, verbose_name='\u7528\u6237\u540d')),
                ('password', models.CharField(max_length=50, verbose_name='\u5bc6\u7801')),
                ('realname', models.CharField(max_length=20, verbose_name='\u771f\u5b9e\u59d3\u540d')),
                ('telphone', models.CharField(max_length=12, verbose_name='\u7528\u6237\u7535\u8bdd')),
                ('group', models.ForeignKey(related_name='user_group', verbose_name='\u7528\u6237\u5c5e\u7ec4', to='backend.GroupInfo')),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typename', models.CharField(max_length=50, verbose_name='\u7528\u6237\u7c7b\u578b\u540d\u79f0')),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='type',
            field=models.ForeignKey(verbose_name='\u7528\u6237\u7c7b\u578b', to='backend.UserType'),
        ),
    ]
