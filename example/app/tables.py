#!/usr/bin/env python
# coding: utf-8

from table import Table, Column


class PersonTable(Table):
    id = Column(index=True, title=u'序号')
    name = Column(attr='name', title=u'姓名')
