#!/usr/bin/env python
# coding: utf-8

from django.template.loader import get_template
from django.template import Context
from django.utils.safestring import mark_safe


class TableSearchBox(object):
    def __init__(self, placeholder=None):
        self.placeholder = placeholder or 'Search'
        self.dom = ("<'col-sm-3 col-md-3 col-lg-3 col-sm-offset-9 "
                    "col-md-offset-9 col-lg-offset-9'f>")

class TableInfoLabel(object):
    def __init__(self, format=None):
        self.format = format or 'Total _TOTAL_'
        self.dom = "<'col-sm-3 col-md-3 col-lg-3'i>"

class TablePagination(object):
    def __init__(self, first=None, last=None, prev=None, next=None):
        self.first = first or 'First'
        self.last = last or 'Last'
        self.prev = prev or 'Prev'
        self.next = next or 'Next'
        self.dom = ("<'col-sm-6 col-md-6 col-lg-6 col-sm-offset-2 "
                    "col-md-offset-2 col-lg-offset-2'p>")

class TableLengthMenu(object):
    def __init__(self):
        self.dom = "<'col-sm-1 col-md-1 col-lg-1'l>"

class TableExtButton(object):
    def __init__(self, text='', link='', template='table/ext_button.html'):
        self.text = text
        self.link = link
        self.template = template
        self.dom = "<'col-sm-9 col-md-9 col-lg-9 ext-btn'>"

    @property
    def html(self):
        template = get_template(self.template)
        context = Context({'text': self.text, 'link': self.link})
        return mark_safe(template.render(context).strip())
