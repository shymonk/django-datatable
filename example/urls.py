#!/usr/bin/env python
# coding: utf-8
from django.conf.urls import patterns, include, url

from .app.views import MyDataView


urlpatterns = patterns('',
    url(r'^$', 'app.views.base', name='base'),
    url(r'^datasource/ajax/$', 'app.views.ajax', name='ajax'),
    url(r'^datasource/ajaxsource/$', 'app.views.ajax_source', name='ajax_source'),
    url(r'^datasource/ajaxsource/api/$', MyDataView.as_view(), name='ajax_source_api'),

    url(r'^column/sequence/$', 'app.views.sequence_column', name='sequence_column'),
    url(r'^column/calendar/$', 'app.views.calendar_column', name='calendar_column'),
    url(r'^column/link/$', 'app.views.link_column', name='link_column'),

    url(r'^user/(\d+)/$', 'app.views.user_profile', name='user_profile'),
    url(r'^table/', include('table.urls')),
)
