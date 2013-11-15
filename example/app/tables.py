#!/usr/bin/env python
# coding: utf-8

from table.columns import Column, LinkColumn, DatetimeColumn, Link
from table.utils import A
from table import Table
from models import Person


class PersonTable(Table):
    id = Column(field='id', header=u'#', header_attrs={'width': '5%'})
    name = Column(field='name', header=u'姓名') 
    create = DatetimeColumn(field='create', header=u'注册时间')
    action = LinkColumn(header=u'操作', links=[Link(text=u'编辑', viewname='app.views.edit', args=('id',))])

    class Meta:
        model = Person
        ext_button_link = "http://www.baidu.com"
