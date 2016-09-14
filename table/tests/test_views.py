#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
import json
import django

from django.test import Client, TestCase

if django.VERSION >= (1, 10):
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

from table import Table
from table.columns import Column
from table.models import Person


class TestTable(Table):
    id = Column('id', header='#')
    name = Column('name', header='NAME')
    email = Column('email', header='EMAIL', searchable=False)

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

        Person.objects.create(id=1, name="Tom", email="tom@mail.com")
        Person.objects.create(id=2, name="Jerry", email="jerry@mail.com")

    def test_model_data_source(self):
        response = self.client.get(self.url, self.payload)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        expect_data = {
            "sEcho": "1",
            "iTotalRecords": 2,
            "iTotalDisplayRecords": 2,
            "aaData": [["1", "Tom", "tom@mail.com"], ["2", "Jerry", "jerry@mail.com"]]
        }
        self.assertEqual(data, expect_data)

    def test_queryset_data_source(self):
        pass

    def test_search(self):
        url, payload = self.url, self.payload
        payload.update({"sSearch": "T"})

        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        expect_data = {
            "sEcho": "1",
            "iTotalRecords": 2,
            "iTotalDisplayRecords": 1,
            "aaData": [["1", "Tom", "tom@mail.com"]]
        }
        self.assertEqual(data, expect_data)

    def test_search_fuzzy(self):
        url, payload = self.url, self.payload
        payload.update({"sSearch": "T 2"})

        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        expect_data = {
            "sEcho": "1",
            "iTotalRecords": 2,
            "iTotalDisplayRecords": 0,
            "aaData": []
        }
        self.assertEqual(data, expect_data)

    def test_unsearchable_column(self):
        url, payload = self.url, self.payload
        payload.update({"sSearch": "mail"})

        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        expect_data = {
            "sEcho": "1",
            "iTotalRecords": 2,
            "iTotalDisplayRecords": 0,
            "aaData": []
        }
        self.assertEqual(data, expect_data)

    def test_sort_asc(self):
        url, payload = self.url, self.payload
        payload.update({
            "iSortCol_0": 0,
            "sSortDir_0": "asc",
        })

        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        expect_data = {
            "sEcho": "1",
            "iTotalRecords": 2,
            "iTotalDisplayRecords": 2,
            "aaData": [["1", "Tom", "tom@mail.com"], ["2", "Jerry", "jerry@mail.com"]]
        }
        self.assertEqual(data, expect_data)

    def test_sort_desc(self):
        url, payload = self.url, self.payload
        payload.update({
            "iSortCol_0": 0,
            "sSortDir_0": "desc",
        })

        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        expect_data = {
            "sEcho": "1",
            "iTotalRecords": 2,
            "iTotalDisplayRecords": 2,
            "aaData": [["2", "Jerry", "jerry@mail.com"], ["1", "Tom", "tom@mail.com"]]
        }
        self.assertEqual(data, expect_data)

    def test_paging(self):
        url, payload = self.url, self.payload

        # query 1st page
        payload.update({
            "iDisplayStart": 0,
            "iDisplayLength": 1,
        })
        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expect_data = {
            "sEcho": "1",
            "iTotalRecords": 2,
            "iTotalDisplayRecords": 2,
            "aaData": [["1", "Tom", "tom@mail.com"]]
        }
        self.assertEqual(data, expect_data)

        # query 2nd page
        payload.update({
            "iDisplayStart": 1,
            "iDisplayLength": 1,
        })
        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expect_data.update({
            "aaData": [["2", "Jerry", "jerry@mail.com"]]
        })
        self.assertEqual(data, expect_data)

    def test_paging_disabled(self):
        url, payload = self.url, self.payload
        payload.update({
            "iDisplayStart": 0,
            "iDisplayLength": -1,
        })
        response = self.client.get(url, payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        expect_data = {
            "sEcho": "1",
            "iTotalRecords": 2,
            "iTotalDisplayRecords": 2,
            "aaData": [["1", "Tom", "tom@mail.com"], ["2", "Jerry", "jerry@mail.com"]]
        }
        self.assertEqual(data, expect_data)

    def test_convert_queryset_to_values_list(self):
        pass
