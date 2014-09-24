#!/usr/bin/env python
# coding: utf-8

from django.utils.safestring import mark_safe
from table.columns import Column


class CheckboxColumn(Column):
    def __init__(self, header=None, **kwargs):
        kwargs["field"] = None
        kwargs["safe"] = False
        kwargs["sortable"] = False
        kwargs["searchable"] = False
        super(CheckboxColumn, self).__init__(header=header, **kwargs)

    def render(self, obj):
        return mark_safe('<input type="checkbox">')
