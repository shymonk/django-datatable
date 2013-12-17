#!/usr/bin/env python
# coding: utf-8

from table.columns import Column, LinkColumn, DatetimeColumn, Link
from table.utils import A
from table import Table
from models import Person


class PersonTable(Table):
    id = Column(field='id', header=u'#', header_attrs={'width': '5%'})
    name = Column(field='name', header=u'NAME') 
    action = LinkColumn(header=u'ACTION', links=[Link(text=u'EDIT', viewname='app.views.edit', args=(A('id'),))])

    class Meta:
        model = Person
        ext_button_template = "button.html"
        # disable_search = True
        # disable_info = True
        # disable_length_menu = True
        # disable_pagination = True
