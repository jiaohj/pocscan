# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
urlpatterns = patterns(
    'pocscan.work.views',
    url(r'^upload/$', 'upload_plug', name='upload'),
)
