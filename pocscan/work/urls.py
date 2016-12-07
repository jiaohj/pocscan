# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
urlpatterns = patterns(
    'pocscan.work.views',
    url(r'^upload/$', 'upload_plug', name='upload'),
)

urlpatterns += patterns(
    'pocscan.work.work_views',
    url(r'^upload$', 'upload_plug', name='upload'),
    url(r'^delPoc$', 'del_plug', name='del_plug'),
    url(r'^add$', 'make_task', name='make_task'),
    url(r'^query$', 'query_task', name='query_task'),
    url(r'^stopTask$', 'stop_task', name='stop_task'),
    url(r'^queryTasks$', 'query_status', name='query_status'),
)
