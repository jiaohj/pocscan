# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.


class PlugRecord(models.Model):
    uuid = models.CharField(max_length=64, verbose_name=_(u"uuid"))
    plug = models.FileField(upload_to='plugs/default', default='', verbose_name=_(u"文件路径"))

    class Meta:
        verbose_name = _(u"插件记录表")
        verbose_name_plural = _(u"插件记录表")

    def __str__(self):
        return self.uuid


class PocTask(models.Model):
    STATUS_CHOICES = (
        ('', _(u"------")),
        (0, _(u"运行中")),
        (1, _(u"已暂停")),
        (2, _(u"已结束")),
    )
    plug = models.ForeignKey(PlugRecord, verbose_name=_(u"插件"))
    task_id = models.CharField(max_length=64, verbose_name=_(u"任务id"))
    local_task_id = models.CharField(max_length=64, verbose_name=_(u"本地任务id"), unique=True, db_index=True)
    created = models.DateTimeField(auto_created=True, verbose_name=_(u"任务创建时间"))
    start_time = models.DateTimeField(verbose_name=_(u"任务开始时间"), blank=True, null=True)
    end_time = models.DateTimeField(verbose_name=_(u"任务结束时间"), blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name=_(u"任务状态"))
    result = models.TextField(verbose_name=_(u"任务结果"), blank=True)

    class Meta:
        verbose_name = _(u"任务表")
        verbose_name_plural = _(u"任务表")

    def __str__(self):
        return self.local_task_id
