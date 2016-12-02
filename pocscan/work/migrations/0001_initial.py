# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlugRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(max_length=64, verbose_name='uuid')),
                ('plug', models.FileField(default=b'', upload_to=b'plugs/default', verbose_name='\u6587\u4ef6\u8def\u5f84')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
            ],
            options={
                'verbose_name': '\u63d2\u4ef6\u8bb0\u5f55\u8868',
                'verbose_name_plural': '\u63d2\u4ef6\u8bb0\u5f55\u8868',
            },
        ),
        migrations.CreateModel(
            name='PocTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='\u4efb\u52a1\u521b\u5efa\u65f6\u95f4', auto_created=True)),
                ('task_id', models.CharField(max_length=64, verbose_name='\u4efb\u52a1id')),
                ('local_task_id', models.CharField(unique=True, max_length=64, verbose_name='\u672c\u5730\u4efb\u52a1id', db_index=True)),
                ('start_time', models.DateTimeField(null=True, verbose_name='\u4efb\u52a1\u5f00\u59cb\u65f6\u95f4', blank=True)),
                ('end_time', models.DateTimeField(null=True, verbose_name='\u4efb\u52a1\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('status', models.IntegerField(default=0, verbose_name='\u4efb\u52a1\u72b6\u6001', choices=[(b'', '------'), (0, '\u8fd0\u884c\u4e2d'), (1, '\u5df2\u7ed3\u675f')])),
                ('result', models.FileField(default=b'', upload_to=b'plugs/result', verbose_name='\u6587\u4ef6\u8def\u5f84')),
                ('plug', models.ForeignKey(verbose_name='\u63d2\u4ef6', to='work.PlugRecord')),
            ],
            options={
                'verbose_name': '\u4efb\u52a1\u8868',
                'verbose_name_plural': '\u4efb\u52a1\u8868',
            },
        ),
    ]
