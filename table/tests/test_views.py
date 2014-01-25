#!/usr/bin/env python
# coding: utf-8

from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from table.views import FeedDataView
from table.forms import QueryDataForm


class FeedDataViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("feed_data")
        self.set_queryset_method()

    def set_queryset_method(self):
        def get_queryset(self):
            object_list = [
                {"name": "A", "age": 18},
                {"name": "B", "age": 35},
                {"name": "C", "age": 70},
            ]
            return object_list
        FeedDataView.get_queryset = get_queryset

    def test_api_basic(self):
        payload = {
            "sEcho": "1",
            "iColumns": 2,
            "iDisplayStart": 0,
            "iDisplayLength": 10,
            "sSearch": "",
            "bRegex": False,
            "iSortingCols": 1
        }
        response = self.client.get(self.url, payload)
        status_code = response.status_code
        data = json.loads(response.content)
        self.assertEqual(status_code, 200)

        expect_data = {
            "sEcho": "1",
            "iTotalRecords": 3,
            "iTotalDisplayRecords": 3,
            "aaData": [["A", 18], ["B", 35], ["C", 70]]
            }
        self.assertEqual(data, expect_data)

    def test_api_search(self):
        pass

    def test_api_sort(self):
        pass

