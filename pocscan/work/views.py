# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .utils import jsonify


@csrf_exempt
@jsonify
def upload_plug(request, *args, **kwargs):
    return dict(state=True)



