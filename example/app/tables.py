#!/usr/bin/env python
# coding: utf-8

from table.columns import Column, LinkColumn, Link
from table import Table
from models import Person


class PersonTable(Table):
    id = Column(field='id', header=u'序号', header_attrs={'width': '50%'})
    name = Column(field='name', header=u'姓名', header_attrs={'width': '50%'}, sortable=False)

    class Meta:
        model = Person
        ext_button_link = "http://www.baidu.com"


class LinkColumnTable(Table):
    id = Column(field='id', header=u'序号', header_attrs={'width': '33%'})
    name = Column(field='name', header=u'姓名', header_attrs={'width': '33%'})
    action = LinkColumn(header=u'操作', links=[Link(text=u'编辑', viewname='app.views.edit', args=('id',)),],
                        header_attrs={'width': '33%'})

    class Meta:
        model = Person


