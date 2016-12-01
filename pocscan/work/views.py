# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .utils import jsonify
import time
import uuid
import json


@csrf_exempt
@jsonify
def upload_plug(request, *args, **kwargs):
    current_time=time.strftime("%Y%m%d%H%M%S")
    random=uuid._random_getnode()
    unique_ident=current_time+str(random)    #uuid
    filename=str(request.FILES['pocfile'])   #poc filename
    file_path='/tmp/'                        #file store path
    fp=open("%s%s"%(file_path,unique_ident),'w') #{uuid}.py 
    fp.write(filename.read())
    fp.close()
    PlugRecord.objects.create(uuid=unique_ident)

    
    return HttpResponse(json.dumps({"filename":filename,"uuid":unique_ident}),content_type='application/json')


def get_poc_path(uuid): 
    path=PlugRecord.objects.get(uuid=uuid)
    poc_file_path=path+"/"+uuid+".py"
    return path


def make_task(request):
    '''
     purpose: run task
     return child process object instance
    
    '''
    task_id=request.POST['taskid']
    poc_file_path = get_poc_path(uuid)
    task_start_time= time.strftime("%Y-%m-%d %H:%m:%s")
    child_process=subprocess.Popen(["python","{0}".format(poc_file_path)],stdout=subprocess.PIPE)
    pid=child_process.pid
    PocTask.objects.create(task_id=task_id,local_task_id=pid)
    #s.wait() 
    return child_process

def suspend_task(request):
    '''
    return task status
    '''	
    task_id=request.POST['uuid']
    task_id=request.POST['task_id']
    result=PocTask.objects.get(task_id=task_id)
    pid=result.local_task_id
    process = psutil.Process(pid)
    process.suspend()
    task_status=process.status()
    return task_status   


def resume_task(pid):
    '''
    return task status
    '''
    process = psutil.Process(pid)
    process.resume()
    task_status=process.status()
    return task_status
