#!/usr/bin/env python
# coding: utf-8

from django.template.loader import get_template
from django.template import Context
from django.utils.safestring import mark_safe


class TableSearchBox(object):
    def __init__(self, placeholder=None, visible=True):
        self.placeholder = placeholder 
        self.visible = visible
    
    @property
    def dom(self):
        if self.visible:
            return "<'col-sm-3 col-md-3 col-lg-3'f>"
        else:
            return "<'col-sm-3 col-md-3 col-lg-3'>"

class TableInfoLabel(object):
    def __init__(self, format, visible=True):
        self.format = format
        self.visible = visible

    @property
    def dom(self):
        if self.visible:
            return "<'col-sm-3 col-md-3 col-lg-3'i>"
        else:
            return "<'col-sm-3 col-md-3 col-lg-3'>"

class TablePagination(object):
    def __init__(self, first, last, prev, next, visible=True):
        self.first = first
        self.last = last
        self.prev = prev
        self.next = next
        self.visible = visible

    @property
    def dom(self):
        if self.visible:
            return ("<'col-sm-6 col-md-6 col-lg-6 col-sm-offset-2 "
                    "col-md-offset-2 col-lg-offset-2'p>") 
        else:
            return ("<'col-sm-6 col-md-6 col-lg-6 col-sm-offset-2 "
                    "col-md-offset-2 col-lg-offset-2'>")

class TableLengthMenu(object):
    def __init__(self, visible=True):
        self.visible = visible

    @property
    def dom(self):
        if self.visible:
            return "<'col-sm-1 col-md-1 col-lg-1'l>"
        else:
            return "<'col-sm-1 col-md-1 col-lg-1'>"

class TableExtButton(object):
    def __init__(self, template, context=None, visible=True):
        self.template = template
        self.context = context
        self.visible = visible

    @property
    def dom(self):
        return "<'col-sm-9 col-md-9 col-lg-9 ext-btn'>"

    @property
    def html(self):
        template = get_template(self.template)
        context = Context(self.context)
        return mark_safe(template.render(context).strip())
