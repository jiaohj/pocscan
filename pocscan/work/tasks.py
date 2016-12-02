# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf import settings
from django.utils import timezone

import os
from celery import shared_task

from .models import PocTask



@shared_task
def do_runner_task(task_id):
    try:
        task = PocTask.objects.get(pk=task_id)
    except:
        return
    path = '{0}/{1}'.format(settings.MEDIA_ROOT, task.task_id)
    if not os.path.exists(path):
        os.makedirs(path)

    if not os.path.isfile(task.result.url):
        os.mknod(task.result.url)

    cmd = task.get_cmd()
    try:
        os.system(cmd)
    except Exception as e:
        print e
        return
    task.end_time = timezone.now()
    task.status = 1
    task.save()
