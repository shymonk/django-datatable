#!/usr/bin/env python
# coding: utf-8

from django.test import TestCase

from table.widgets import *
from table.tables import Table, TableWidgets


class TableWidgetsTestCase(TestCase):
    """
    Test cases for datatable dom widgets.
    """
    def test_searchbox(self):
        searchbox = SearchBox()
        self.assertEqual(searchbox.dom, "<'col-sm-3 col-md-3 col-lg-3'f>")
        self.assertEqual(searchbox.placeholder, "Search")
        searchbox = SearchBox(visible=False)
        self.assertEqual(searchbox.dom, "<'col-sm-3 col-md-3 col-lg-3'>")

    def test_pagiantion(self):
        pagination = Pagination()
        self.assertEqual(pagination.first, "First")
        self.assertEqual(pagination.last, "Last")
        self.assertEqual(pagination.prev, "Prev")
        self.assertEqual(pagination.next, "Next")
        self.assertEqual(
            pagination.dom,
            "<'col-sm-6 col-md-6 col-lg-6 col-sm-offset-2 col-md-offset-2 col-lg-offset-2'p>"
        )
        pagination = Pagination(visible=False)
        self.assertEqual(
            pagination.dom,
            "<'col-sm-6 col-md-6 col-lg-6 col-sm-offset-2 col-md-offset-2 col-lg-offset-2'>"
        )

    def test_info_label(self):
        label = InfoLabel()
        self.assertEqual(label.dom, "<'col-sm-3 col-md-3 col-lg-3'i>")
        label = InfoLabel(visible=False)
        self.assertEqual(label.dom, "<'col-sm-3 col-md-3 col-lg-3'>")

    def test_length_menu(self):
        menu = LengthMenu()
        self.assertEqual(menu.dom, "<'col-sm-1 col-md-1 col-lg-1'l>")
        menu = LengthMenu(visible=False)
        self.assertEqual(menu.dom, "<'col-sm-1 col-md-1 col-lg-1'>")

    def test_widgets_dom(self):
        class TestTable(Table):
            class Meta:
                search_placeholder = "test"
                info_format = "__TOTAL__"
                pagination_first = "F"
                pagination_last = "L"
                pagination_prev = "P"
                pagination_next = "N"

        table = TestTable([])
        widgets = TableWidgets(table)
        self.assertEqual(widgets.search_box.placeholder, "test")
        self.assertEqual(widgets.info_label.format, "__TOTAL__")
        self.assertEqual(widgets.pagination.first, "F")
        self.assertEqual(widgets.pagination.last, "L")
        self.assertEqual(widgets.pagination.prev, "P")
        self.assertEqual(widgets.pagination.next, "N")
        self.assertEqual(
            widgets.render_dom(),
            "<'row'<'col-sm-9 col-md-9 col-lg-9'>"
            "<'col-sm-3 col-md-3 col-lg-3'f>>"
            "rt"
            "<'row'<'col-sm-3 col-md-3 col-lg-3'i>"
            "<'col-sm-6 col-md-6 col-lg-6 col-sm-offset-2 col-md-offset-2 col-lg-offset-2'p>"
            "<'col-sm-1 col-md-1 col-lg-1'l>>"
        )

    def test_widgets_dom_simple(self):
        class SimpleTable(Table):
            class Meta:
                search = False
                pagination = False
                info = False
                length_menu = False
        table = SimpleTable([])
        widgets = TableWidgets(table)
        self.assertEqual(widgets.render_dom(), "rt")
