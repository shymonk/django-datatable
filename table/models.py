#!/usr/bin/env python
# coding: utf-8
""" Model for test.
"""
from django.db import models


class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
