#!/usr/bin/env python
# coding: utf-8

from table.columns import Column, LinkColumn, DatetimeColumn, Link
from table.utils import A
from table import Table
from models import Person


class PersonTable(Table):
    id = Column(field='id', header=u'#', header_attrs={'width': '5%'})
    name = Column(field='name', header=u'姓名') 
    action = LinkColumn(header=u'操作', links=[Link(text=u'编辑', viewname='app.views.edit', args=(A('id'),))])

    class Meta:
        model = Person
        ext_button_link = "http://www.baidu.com"
        ext_button_text = "Add +"
