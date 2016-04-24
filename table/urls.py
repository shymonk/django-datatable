#!/usr/bin/env python
# coding: utf-8
from django.conf.urls import url

from table.views import FeedDataView


urlpatterns = [
    url(r'^ajax/(?P<token>\w{32})/$', FeedDataView.as_view(), name='feed_data'),
]
