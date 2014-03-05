#!/usr/bin/env python
# coding: utf-8

from uuid import uuid4
from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from table.views import FeedDataView
from table.forms import QueryDataForm
from table.models import Person
from table.columns import Column
from table import Table


class TestTable(Table):
    id = Column('id', header='#')
    name = Column('name', header='NAME')

    class Meta:
        model = Person
        ajax = True


class FeedDataViewTestCase(TestCase):
    def setUp(self):
        self.table = TestTable()
        self.client = Client()
        self.url = reverse("feed_data", args=(self.table.token,))
        self.payload = {
            "sEcho": "1",
            "iColumns": 2,
            "iDisplayStart": 0,
            "iDisplayLength": 10,
            "sSearch": "",
            "bRegex": False,
            "iSortingCols": 1
        }

        Person.objects.create(id=1, name="Tom")
        Person.objects.create(id=2, name="Jerry")

    def test_api_basic(self):
        response = self.client.get(self.url, self.payload)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        expect_data = {
            "sEcho": "1",
            "iTotalRecords": 2,
            "iTotalDisplayRecords": 2,
            "aaData": [[1, "Tom"], [2, "Jerry"]]
            }
        self.assertEqual(data, expect_data)

    def test_api_search(self):
        self.payload["sSearch"] = "T"

        response = self.client.get(self.url, self.payload)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        expect_data = {
            "sEcho": "1",
            "iTotalRecords": 2,
            "iTotalDisplayRecords": 1,
            "aaData": [[1, "Tom"]]
            }
        self.assertEqual(data, expect_data)
        

    def test_api_sort(self):
        pass
