#!/usr/bin/env python
# coding: utf-8

from datetime import date
from django.test import TestCase
from table.columns.base import Column, BoundColumn, ColumnHeader
from table.columns.sequencecolumn import SequenceColumn
from table.columns.calendarcolumn import DaysColumn, WeeksColumn, MonthsColumn


class BaseColumntestCase(TestCase):
    def test_create_instance(self):
        column = Column("field")

        self.assertEqual(column.field, "field")
        self.assertEqual(column.attrs, {})

        self.assertTrue(column.sortable, True)
        self.assertTrue(column.searchable, True)
        self.assertTrue(column.safe, True)
        self.assertTrue(column.visible, True)
        self.assertTrue(column.space, True)

    def test_column_header(self):
        column = Column("field", "A",header_attrs={"id": "col-id"},
                        header_row_order=1)
        self.assertEqual(column.header.text, "A")
        self.assertEqual(column.header.attrs, 'id="col-id"')
        self.assertEqual(column.header.row_order, 1)

    def test_render(self):
        class Foo():
            def __init__(self, foo):
                self.foo = foo
        f = Foo("bar")
        column = Column("foo")
        self.assertEqual(column.render(f), "bar")


class SequenceColumnTestCase(TestCase):
    def setUp(self):
        self.column = SequenceColumn("foo", headers=["A", "B", "C"])

    def test_create_instance(self):
        self.assertEqual(self.column.headers, ["A", "B", "C"])

    def test_length(self):
        self.assertEqual(len(self.column), 3)

    def test_getitem(self):
        col = self.column[0]
        self.assertEqual(col.field, "foo.0")
        self.assertEqual(col.header.text, "A")

    def test_extend_columns(self):
        columns = []
        columns.extend(self.column)
        self.assertEqual(len(columns), 3)

    def test_get_field(self):
        self.assertEqual(self.column.get_field(0), "foo.0")
        self.assertEqual(self.column.get_field(1), "foo.1")
        self.assertEqual(self.column.get_field(2), "foo.2")

    def test_get_column(self):
        column0 = self.column.get_column(0)
        self.assertEqual(column0.field, "foo.0")
        self.assertEqual(column0.header.text, "A")

    def test_columns_property(self):
        self.assertTrue(isinstance(self.column.columns, list))
        self.assertEqual(len(self.column.columns), 3)
        self.assertEqual(self.column.columns[0].field, "foo.0")
        self.assertEqual(self.column.columns[1].field, "foo.1")
        self.assertEqual(self.column.columns[2].field, "foo.2")


class DaysColumnTestCase(TestCase):
    def setUp(self):
        self.column1 = DaysColumn(None, date(2012, 12, 18), date(2012, 12, 19))
        self.column2 = DaysColumn(None, date(2013, 12, 30), date(2014, 1, 1))

    def test_length(self):
        self.assertEqual(len(self.column1), 2)
        self.assertEqual(len(self.column2), 3)

    def test_headers(self):
        self.assertEqual(self.column1.headers, ['18', '19'])
        self.assertEqual(self.column2.headers, ['30', '31', '01'])


class WeeksColumnTestCase(TestCase):
    def setUp(self):
        self.column1 = WeeksColumn(None, date(2013, 12, 18), date(2013, 12, 19))
        self.column2 = WeeksColumn(None, date(2013, 12, 30), date(2014, 1, 1))

    def test_length(self):
        self.assertEqual(len(self.column1), 2)
        self.assertEqual(len(self.column2), 3)

    def test_columns_names(self):
        self.assertEqual(self.column1.headers, ['Wed', 'Thu'])
        self.assertEqual(self.column2.headers, ['Mon', 'Tue', 'Wed'])


class MonthsColumnTestCase(TestCase):
    def test_columns_count(self):
        col = MonthsColumn(None, date(2012, 12, 18), date(2013, 07, 01))
        self.assertEqual(col.columns_count, 8)
        col = MonthsColumn(None, date(2012, 12, 18), date(2012, 12, 19))
        self.assertEqual(col.columns_count, 1)
        col = MonthsColumn(None, date(2012, 1, 18), date(2012, 12, 19))
        self.assertEqual(col.columns_count, 12)

    def test_columns_names(self):
        col = MonthsColumn(None, date(2012, 12, 18), date(2012, 12, 19))
        self.assertEqual(col.columns_names, ['December',])
        col = MonthsColumn(None, date(2012, 12, 18), date(2013, 2, 1))
        self.assertEqual(col.columns_names, ['December', 'January', 'February',])


