#!/usr/bin/env python
# coding: utf-8

from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.generic.list import BaseListView
from table.forms import QueryDataForm
from table.tables import TableDataMap


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        return HttpResponse(self.convert_context_to_json(context),
                            content_type='application/json',
                            **response_kwargs)

    def convert_context_to_json(self, context):
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)


class FeedDataView(JSONResponseMixin, BaseListView):
    def get(self, request, *args, **kwargs):
        self.token = kwargs["token"]
        query_form = QueryDataForm(request.GET)
        if query_form.is_valid():
            self.query_data = query_form.cleaned_data
        else:
            return self.render_to_response({"error": "Query form is invalid."})
        return BaseListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        model = TableDataMap.get_model(self.token)
        if model is None:
            return None
        return model.objects.all()

    def get_search_arguments(self):
        args = ()
        return args

    def get_sort_arguments(self):
        arguments = []
        columns = TableDataMap.get_columns(self.token)
        for key, value in self.query_data.items():
            if not key.startswith("iSortCol"):
                continue
            field = columns[value].field
            dir = self.query_data["sSortDir_" + key.split("_")[1]]
            if dir == "asc":
                arguments.append(field)
            else:
                arguments.append("-" + field)
        return arguments

    def filter_queryset(self, queryset):
        filter_args = self.get_search_arguments()
        sort_args = self.get_sort_arguments()
        queryset = queryset.filter(*filter_args).order_by(*sort_args)
        return queryset
        
    def get_context_data(self, **kwargs):
        sEcho = self.query_data["sEcho"]
        queryset = kwargs.pop("object_list")
        if queryset is not None:
            start = self.query_data["iDisplayStart"]
            length = self.query_data["iDisplayLength"]

            filtered_queryset = self.filter_queryset(queryset)
            paginated_queryset = filtered_queryset[start:start+length]
            context = {
                "sEcho": sEcho,
                "iTotalRecords": queryset.count(),
                "iTotalDisplayRecords": filtered_queryset.count(),
                "aaData": [list(e) for e in paginated_queryset.values_list()],
            }
        else:
            context = {
                "sEcho": sEcho,
                "iTotalRecords": 0,
                "iTotalDisplayRecords": 0,
                "aaData": [],
            }
        return context

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

