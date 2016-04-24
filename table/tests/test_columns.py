#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from datetime import date

from django.test import TestCase

from table.utils import A
from table.columns.base import Column
from table.columns.linkcolumn import Link, ImageLink
from table.columns.sequencecolumn import SequenceColumn
from table.columns.calendarcolumn import DaysColumn, WeeksColumn, MonthsColumn, CalendarColumn


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
        column = Column("field", "A", header_attrs={"id": "col-id"}, header_row_order=1)
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


class LinkColumnTestCase(TestCase):
    def test_link(self):
        link = Link(text=A("foo"))
        self.assertEqual(link.render({}), "<a ></a>")
        self.assertEqual(link.render({"foo": "bar"}), "<a >bar</a>")

    def test_imagelink(self):
        image_link = ImageLink(image="test.jpg", image_title="foo")
        self.assertEqual(image_link.render({}), '<a ><img src="/static/test.jpg" title="foo"></a>')
        image_link = ImageLink(image="test.jpg", image_title=A("foo"))
        self.assertEqual(image_link.render({"foo": "bar"}), '<a ><img src="/static/test.jpg" title="bar"></a>')


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

    def test_headers(self):
        self.assertEqual(self.column1.headers, ['Wed', 'Thu'])
        self.assertEqual(self.column2.headers, ['Mon', 'Tue', 'Wed'])


class MonthsColumnTestCase(TestCase):
    def test_length(self):
        column1 = MonthsColumn(None, date(2012, 12, 18), date(2013, 07, 01))
        self.assertEqual(len(column1), 8)
        column2 = MonthsColumn(None, date(2012, 12, 18), date(2012, 12, 19))
        self.assertEqual(len(column2), 1)
        column3 = MonthsColumn(None, date(2012, 1, 18), date(2012, 12, 19))
        self.assertEqual(len(column3), 12)

    def test_headers(self):
        column1 = MonthsColumn(None, date(2012, 12, 18), date(2012, 12, 19))
        self.assertEqual(column1.headers, ['December'])
        column2 = MonthsColumn(None, date(2012, 12, 18), date(2013, 2, 1))
        self.assertEqual(column2.headers, ['December', 'January', 'February'])


class CalendarColumnTestCase(TestCase):
    def test_inline_month_columns(self):
        column = CalendarColumn(None, date(2012, 12, 18), date(2013, 03, 01))
        self.assertEqual(len(column), 4 + 74 + 74)
        self.assertEqual(column.months_column.headers, ['December', 'January', 'February', 'March'])
        self.assertEqual(column.months_column[0].header.base_attrs['colspan'], '14')
        self.assertEqual(column.months_column[1].header.base_attrs['colspan'], '31')
        self.assertEqual(column.months_column[2].header.base_attrs['colspan'], '28')
        self.assertEqual(column.months_column[3].header.base_attrs['colspan'], '1')

        column = CalendarColumn(None, date(2014, 5, 4), date(2014, 5, 9))
        self.assertEqual(len(column), 1 + 6 + 6)
        self.assertEqual(column.months_column.headers, ['May'])
        self.assertEqual(column.months_column[0].header.base_attrs['colspan'], '6')
