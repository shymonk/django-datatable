#!/usr/bin/env python
# coding: utf-8

from django.template.loader import get_template
from django.template import Context
from django.utils.safestring import mark_safe


class TableSearchBox(object):
    def __init__(self, placeholder=None, disable=False):
        self.placeholder = placeholder 
        self.disable = disable
    
    @property
    def dom(self):
        if self.disable:
            return "<'col-sm-3 col-md-3 col-lg-3'>"
        else:
            return "<'col-sm-3 col-md-3 col-lg-3'f>"

class TableInfoLabel(object):
    def __init__(self, format, disable=False):
        self.format = format
        self.disable = disable

    @property
    def dom(self):
        if self.disable:
            return "<'col-sm-3 col-md-3 col-lg-3'>"
        else:
            return "<'col-sm-3 col-md-3 col-lg-3'i>"

class TablePagination(object):
    def __init__(self, first, last, prev, next, disable=False):
        self.first = first
        self.last = last
        self.prev = prev
        self.next = next
        self.disable = disable

    @property
    def dom(self):
        if self.disable:
            return ("<'col-sm-6 col-md-6 col-lg-6 col-sm-offset-2 "
                    "col-md-offset-2 col-lg-offset-2'>") 
        else:
            return ("<'col-sm-6 col-md-6 col-lg-6 col-sm-offset-2 "
                    "col-md-offset-2 col-lg-offset-2'p>")

class TableLengthMenu(object):
    def __init__(self, disable=False):
        self.disable = disable

    @property
    def dom(self):
        if self.disable:
            return "<'col-sm-1 col-md-1 col-lg-1'>"
        else:
            return "<'col-sm-1 col-md-1 col-lg-1'l>"

class TableExtButton(object):
    def __init__(self, text, link, template='table/ext_button.html'):
        self.text = text
        self.link = link
        self.template = template

    @property
    def dom(self):
        return "<'col-sm-9 col-md-9 col-lg-9 ext-btn'>"

    @property
    def html(self):
        template = get_template(self.template)
        context = Context({'text': self.text, 'link': self.link})
        return mark_safe(template.render(context).strip())
