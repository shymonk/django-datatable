#!/usr/bin/env python
# coding: utf-8

from table import Table, Column


class PersonTable(Table):
    id = Column(index=True, title=u'序号', width='50%')
    name = Column(field='name', title=u'姓名', width='50%')
