#!/usr/bin/env python
# coding: utf-8

from datetime import date
from django.test import TestCase
from table.columns.calendarcolumn import MonthsColumn

class MonthColumnTest(TestCase):
    def test_cols_count(self):
        col = MonthsColumn(date(2012, 12, 18), date(2013, 07, 01))
        self.assertEqual(col.cols_count, 8)
        col = MonthsColumn(date(2012, 12, 18), date(2012, 12, 19))
        self.assertEqual(col.cols_count, 1)
        col = MonthsColumn(date(2012, 1, 18), date(2012, 12, 19))
        self.assertEqual(col.cols_count, 12)

    def test_cols_names(self):
        col = MonthsColumn(date(2012, 12, 18), date(2012, 12, 19))
        self.assertEqual(col.cols_names, ['December',])
        col = MonthsColumn(date(2012, 12, 18), date(2013, 2, 1))
        self.assertEqual(col.cols_names, ['December', 'January', 'February',])

