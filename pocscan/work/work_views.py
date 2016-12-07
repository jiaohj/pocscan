# -*- coding: utf-8 -*-
import json

import os
import signal

import psutil
from django.conf import settings

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import PlugRecord, PocTask
from .utils import jsonify
import uuid
from celery.result import AsyncResult


@csrf_exempt
@jsonify
def upload_plug(request, *args, **kwargs):
    if request.method == 'POST':
        poc_uuid = uuid.uuid4().hex
        filename = request.FILES.get('pocfile')
        file_path = "%s/%s.py" % (settings.MEDIA_ROOT, poc_uuid)
        try:
            fp = open(file_path, 'w')
            fp.write(filename.read())
            fp.close()
        except Exception as e:
            print e, filename.read()
            return dict(status=-1, msg=u"上传文件失败")
        PlugRecord.objects.create(uuid=poc_uuid, plug=file_path)
        return dict(status=0, pocId=poc_uuid)
    return dict(status=-1, msg=u"请求方式错误")


@csrf_exempt
@jsonify
def del_plug(request, *args, **kwargs):
    if request.method == 'POST':
        body = json.loads(request.body)
        poc_id = body.get('pocId')
        try:
            plug = PlugRecord.objects.get(uuid=poc_id)
        except:
            return dict(status=-1, msg=u"插件不存在")
        plug.is_active = False
        plug.save()
        return dict(status=0)
    return dict(status=-1, msg=u"请求方式错误")


@csrf_exempt
@jsonify
def make_task(request):
    """
    purpose: run task
     return child process object instance
    :param request:
    :return:
    """

    if request.method == 'POST':
        body = json.loads(request.body)
        task_id = body.get('taskId')
        uuid = body.get('pocId')
        print uuid, task_id
        try:
            plug = PlugRecord.objects.get(uuid=uuid)
        except:
            return dict(status=-1, msg=u"插件不存在！")
        if PocTask.objects.filter(task_id=task_id, plug__uuid=uuid, status__in=[0]).exists():
            return dict(status=-1, msg=u"任务已存在！")
        result = '{path}/{task}/{name}.txt'.format(path=settings.MEDIA_ROOT, task=task_id, name=uuid)
        task = PocTask.objects.create(task_id=task_id, plug=plug, result=result, status=0, created=timezone.now())
        from .tasks import do_runner_task
        celery_task = do_runner_task.delay(task.id)
        task.start_time = timezone.now()
        task.local_task_id = celery_task.id
        task.save()
        return dict(status=0)
    return dict(status=-1, msg=u"请求方式错误")


@csrf_exempt
@jsonify
def query_task(request, *args, **kwargs):
    if request.method == 'GET':
        body = json.loads(request.body)
        poc_id = body.get('pocId')
        task_id = body.get('taskId')
        if not PlugRecord.objects.filter(uuid=poc_id).exists():
            return dict(status=-1, msg=u"插件不存在")
        if not PocTask.objects.filter(task_id=task_id, plug__uuid=poc_id).exists():
            return dict(status=-1, msg=u"任务不存在")
        log_url = 'http://{host}/media/{task}/{name}.txt'.format(host=request.get_host(), task=task_id, name=poc_id)
        return dict(status=0, result=log_url)
    return dict(status=-1, msg=u"请求方式错误")


@csrf_exempt
@jsonify
def stop_task(request, *args, **kwargs):
    if request.method == 'POST':
        body = json.loads(request.body)
        task_id = body.get('taskId')
        if not PocTask.objects.filter(task_id=task_id, status__in=[0]).exists():
            return dict(status=-1, msg=u"任务已完成")
        task = PocTask.objects.filter(task_id=task_id, status__in=[0]).first()
        task_res = AsyncResult(task.local_task_id)
        if task_res.successful():
            return dict(status=-1, msg=u"任务已完成")
        else:
            pid = task.get_pid()
            if pid != -1:
                # os.kill(pid, signal.SIGINT)
                for p in pid:
                    process = psutil.Process(int(p))
                    process.kill()
            task_res.revoke()
            task.status = 10
            task.save()
            return dict(status=0)
    return dict(status=-1, msg=u"请求方式错误")


@csrf_exempt
@jsonify
def query_status(request, *args, **kwargs):
    if request.method == 'GET':
        body = json.loads(request.body)
        task_ids = body.get('taskIds')
        result = {}
        if isinstance(task_ids, list):
            for task_id in task_ids:
                if not PocTask.objects.filter(task_id=task_id).exists():
                    result[task_id] = ''
                    continue
                task = PocTask.objects.filter(task_id=task_id).first()
                result['task_id'] = task.status
        else:
            return dict(status=-1, msg=u"参数错误！")
        return dict(status=0, data=result)
    return dict(status=-1, msg=u"请求方式错误")
