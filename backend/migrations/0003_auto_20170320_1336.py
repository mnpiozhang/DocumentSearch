# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_documentinfo_attachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doctype', models.CharField(max_length=50, verbose_name='\u6587\u6863\u7c7b\u578b')),
            ],
        ),
        migrations.AlterField(
            model_name='documentinfo',
            name='indexstate',
            field=models.CharField(default=b's', max_length=1, choices=[(b'b', b'begin index'), (b'i', b'indexing'), (b'f', b'index fail'), (b's', b'index success')]),
        ),
        migrations.AddField(
            model_name='documentinfo',
            name='type',
            field=models.ForeignKey(related_name='doc_type', default=1, verbose_name='\u6587\u6863\u6240\u5c5e\u7c7b\u578b', to='backend.DocumentType'),
            preserve_default=False,
        ),
    ]
