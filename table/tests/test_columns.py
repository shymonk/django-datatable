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
        self.assertEqual(col.header)

    def test_extend_columns(self):
        pass

    def test_get_column_field(self):
        pass

    def test_get_column(self):
        pass

    def test_columns(self):
        pass


class DaysColumnTest(TestCase):
    def setUp(self):
        self.col1 = DaysColumn(None, date(2012, 12, 18), date(2012, 12, 19))
        self.col2 = DaysColumn(None, date(2013, 12, 30), date(2014, 1, 1))

    def test_columns_count(self):
        self.assertEqual(self.col1.columns_count, 2)
        self.assertEqual(self.col2.columns_count, 3)

    def test_columns_names(self):
        self.assertEqual(self.col1.columns_names, ['18', '19'])
        self.assertEqual(self.col2.columns_names, ['30', '31', '01'])


class MonthsColumnTest(TestCase):
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


class WeeksColumnTest(TestCase):
    def setUp(self):
        self.col1 = WeeksColumn(None, date(2013, 12, 18), date(2013, 12, 19))
        self.col2 = WeeksColumn(None, date(2013, 12, 30), date(2014, 1, 1))

    def test_columns_count(self):
        self.assertEqual(self.col1.columns_count, 2)
        self.assertEqual(self.col2.columns_count, 3)

    def test_columns_names(self):
        self.assertEqual(self.col1.columns_names, ['Wed', 'Thu'])
        self.assertEqual(self.col2.columns_names, ['Mon', 'Tue', 'Wed'])
