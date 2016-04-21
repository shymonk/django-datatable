#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.test import TestCase

from table.utils import Accessor


class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        app_label = 'table'


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Meta:
        app_label = 'table'


class AccessorTestCase(TestCase):

    def test_resolve_manager_instance(self):
        p1 = Publication(title='The Python Journal')
        p1.save()
        a1 = Article(headline='Django lets you build Web apps easily')
        a1.save()
        a1.publications.add(p1)

        self.assertEqual(Accessor('article_set.count').resolve(p1), 1)
