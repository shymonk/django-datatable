#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

from django.test import TestCase

from table.tables import Table
from table.columns import Column


class TestTable(Table):
    foo = Column(field='id', header='ID', header_row_order=0)
    bar = Column(field='name', header='NAME', header_row_order=1)


class BaseTableTestCase(TestCase):
    def setUp(self):
        data = [{'id': 1, 'name': 'a'}, {'id': 2, 'name': 'b'}]
        self.table = TestTable(data)

    def test_data_source(self):
        data = [{'id': 1, 'name': 'a'}, {'id': 2, 'name': 'b'}]
        self.assertEqual(self.table.data.list, data)

    def test_rows(self):
        first_row = self.table.rows[0].values()
        second_row = self.table.rows[1].values()
        self.assertEqual(first_row, ['1', 'a'])
        self.assertEqual(second_row, ['2', 'b'])

    def test_header_rows(self):
        first_header_row = [header.text for header in self.table.header_rows[0]]
        second_header_row = [header.text for header in self.table.header_rows[1]]
        self.assertEqual(first_header_row, ['ID'])
        self.assertEqual(second_header_row, ['NAME'])


class TableDataMapTestCase(TestCase):
    def test_register(self):
        pass

    def test_get_data(self):
        pass

    def test_get_columns(self):
        pass


class TableAddonsTestCase(TestCase):
    def test_basic_init(self):
        pass

    def test_render_dom(self):
        pass


class TableOptionsTestCase(TestCase):
    def test_basic_init(self):
        pass


class TableMetaClassTestCase(TestCase):
    def test_create_class_obj(self):
        pass
