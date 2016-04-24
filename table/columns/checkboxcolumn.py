#!/usr/bin/env python
# coding: utf-8
from django.utils.safestring import mark_safe

from table.columns import Column
from table.utils import Accessor


class CheckboxColumn(Column):
    def __init__(self, field=None, header=None, **kwargs):
        kwargs["safe"] = False
        kwargs["sortable"] = False
        kwargs["searchable"] = False
        super(CheckboxColumn, self).__init__(field=field, header=header, **kwargs)

    def render(self, obj):
        checked = bool(Accessor(self.field).resolve(obj)) if self.field else False
        if checked:
            return mark_safe('<input checked type="checkbox">')
        else:
            return mark_safe('<input type="checkbox">')
