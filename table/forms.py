#!/usr/bin/env python
# coding: utf-8
from django import forms


class QueryDataForm(forms.Form):
    """
    Non-interactive form that used to organize query parameters
    of DataTables.
    """
    sEcho = forms.CharField()
    iDisplayStart = forms.IntegerField()
    iDisplayLength = forms.IntegerField()
    iColumns = forms.IntegerField()
    sSearch = forms.CharField(required=False)
    bRegex = forms.BooleanField(required=False)
    iSortingCols = forms.IntegerField(required=False)

    def __init__(self, data=None, *args, **kwargs):
        super(QueryDataForm, self).__init__(data, *args, **kwargs)
        for key in data.keys():
            if key.startswith("iSortCol"):
                self.fields[key] = forms.IntegerField()
            if key.startswith("sSortDir"):
                self.fields[key] = forms.CharField()
