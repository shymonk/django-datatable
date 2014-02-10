#!/usr/bin/env python
# coding: utf-8

from django import forms

"""
int	iDisplayStart	Display start point in the current data set.
int	iDisplayLength	Number of records that the table can display in the current draw. It is expected that the number of records returned will be equal to this number, unless the server has fewer records to return.
int	iColumns	Number of columns being displayed (useful for getting individual column search info)
string	sSearch	Global search field
bool	bRegex	True if the global filter should be treated as a regular expression for advanced filtering, false if not.
bool	bSearchable_(int)	Indicator for if a column is flagged as searchable or not on the client-side
string	sSearch_(int)	Individual column filter
bool	bRegex_(int)	True if the individual column filter should be treated as a regular expression for advanced filtering, false if not
bool	bSortable_(int)	Indicator for if a column is flagged as sortable or not on the client-side
int	iSortingCols	Number of columns to sort on
int	iSortCol_(int)	Column being sorted on (you will need to decode this number for your database)
string	sSortDir_(int)	Direction to be sorted - "desc" or "asc".
string	mDataProp_(int)	The value specified by mDataProp for each column. This can be useful for ensuring that the processing of data is independent from the order of the columns.
string	sEcho	Information for DataTables to use for rendering.
"""

class QueryDataForm(forms.Form):
    """
    Noninteractive form that used to organize query parameters
    of DataTables.
    """
    sEcho = forms.CharField()
    iDisplayStart = forms.IntegerField()
    iDisplayLength = forms.IntegerField()
    iColumns = forms.IntegerField()
    sSearch = forms.CharField(required=False)
    bRegex = forms.BooleanField(required=False)
    iSortingCols = forms.IntegerField()
