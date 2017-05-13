#!/usr/bin/env python
# coding: utf-8
from django.template.loader import get_template
from django.template import Context, Template
from django.utils.safestring import mark_safe


class SearchBox(object):
    def __init__(self, visible=True, placeholder=None, label=None):
        self.visible = visible
        self.placeholder = placeholder or "Search"
        self.label = label or "Search:"

    @property
    def dom(self):
        if self.visible:
            return "<'col-sm-3 col-md-3 col-lg-3'f>"
        else:
            return "<'col-sm-3 col-md-3 col-lg-3'>"


class InfoLabel(object):
    def __init__(self, visible=True, format=None, filtered=None, post_fix=None):
        self.visible = visible
        self.format = format or "Total _TOTAL_"
        self.filtered = filtered or '(filtered from _MAX_ total entries)'
        self.post_fix = post_fix or ""

    @property
    def dom(self):
        if self.visible:
            return "<'col-sm-3 col-md-3 col-lg-3'i>"
        else:
            return "<'col-sm-3 col-md-3 col-lg-3'>"


class Pagination(object):
    def __init__(self, visible=True, length=10, first=None,
                 last=None, prev=None, next=None):
        self.visible = visible
        self.length = length
        self.first = first or "First"
        self.last = last or "Last"
        self.prev = prev or "Prev"
        self.next = next or "Next"

    @property
    def dom(self):
        if self.visible:
            return ("<'col-sm-6 col-md-6 col-lg-6 col-sm-offset-2 "
                    "col-md-offset-2 col-lg-offset-2'p>")
        else:
            return ("<'col-sm-6 col-md-6 col-lg-6 col-sm-offset-2 "
                    "col-md-offset-2 col-lg-offset-2'>")


class LengthMenu(object):
    def __init__(self, visible=True, format=None):
        self.visible = visible
        self.format = format or "Show _MENU_ entries"

    @property
    def dom(self):
        if self.visible:
            return "<'col-sm-1 col-md-1 col-lg-1'l>"
        else:
            return "<'col-sm-1 col-md-1 col-lg-1'>"
