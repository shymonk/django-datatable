#!/usr/bin/env python
# coding: utf-8

from datetime import date
from django.test import TestCase
from table.columns import MonthsColumn, WeeksColumn, DaysColumn


class MonthsColumnTest(TestCase):
    def test_cols_count(self):
        col = MonthsColumn(None, date(2012, 12, 18), date(2013, 07, 01))
        self.assertEqual(col.cols_count, 8)
        col = MonthsColumn(None, date(2012, 12, 18), date(2012, 12, 19))
        self.assertEqual(col.cols_count, 1)
        col = MonthsColumn(None, date(2012, 1, 18), date(2012, 12, 19))
        self.assertEqual(col.cols_count, 12)

    def test_cols_names(self):
        col = MonthsColumn(None, date(2012, 12, 18), date(2012, 12, 19))
        self.assertEqual(col.cols_names, ['December',])
        col = MonthsColumn(None, date(2012, 12, 18), date(2013, 2, 1))
        self.assertEqual(col.cols_names, ['December', 'January', 'February',])

class DaysColumnTest(TestCase):
    def setUp(self):
        self.col1 = DaysColumn(None, date(2012, 12, 18), date(2012, 12, 19))
        self.col2 = DaysColumn(None, date(2013, 12, 30), date(2014, 1, 1))

    def test_cols_count(self):
        self.assertEqual(self.col1.cols_count, 2)
        self.assertEqual(self.col2.cols_count, 3)

    def test_cols_names(self):
        self.assertEqual(self.col1.cols_names, ['18', '19'])
        self.assertEqual(self.col2.cols_names, ['30', '31', '01'])

class WeeksColumnTest(TestCase):
    def setUp(self):
        self.col1 = WeeksColumn(None, date(2013, 12, 18), date(2013, 12, 19))
        self.col2 = WeeksColumn(None, date(2013, 12, 30), date(2014, 1, 1))

    def test_cols_count(self):
        self.assertEqual(self.col1.cols_count, 2)
        self.assertEqual(self.col2.cols_count, 3)

    def test_cols_names(self):
        self.assertEqual(self.col1.cols_names, ['Wed', 'Thu'])
        self.assertEqual(self.col2.cols_names, ['Mon', 'Tue', 'Wed'])
