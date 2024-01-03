#!/usr/bin/env python
# coding: utf-8
# from django.conf.urls import url
from django.urls import re_path

from table.views import FeedDataView

urlpatterns = [
    re_path(r"^ajax/(?P<token>\w{32})/$", FeedDataView.as_view(), name="feed_data"),
]
