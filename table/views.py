#!/usr/bin/env python
# coding: utf-8

from django.db.models import Q
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.generic.list import BaseListView
from django.core.serializers.json import DjangoJSONEncoder

from table.forms import QueryDataForm
from table.tables import TableDataMap


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return HttpResponse(
            self.convert_context_to_json(context),
            content_type='application/json',
            **response_kwargs
        )

    def convert_context_to_json(self, context):
        """
        Convert the context dictionary into a JSON object.
        """
        return json.dumps(context, cls=DjangoJSONEncoder)


class FeedDataView(JSONResponseMixin, BaseListView):
    """
    The view to feed ajax data of table.
    """
    def get(self, request, *args, **kwargs):
        self.token = kwargs["token"]
        self.columns = TableDataMap.get_columns(self.token)

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

    def filter_queryset(self, queryset):
        def get_filter_arguments(filter_target):
            """
            Get `Q` object passed to `filter` function.
            """
            queries = []
            fields = [col.field for col in self.columns if col.searchable]
            for field in fields:
                key = "__".join(field.split(".") + ["icontains"])
                value = filter_target
                queries.append(Q(**{key: value}))
            return reduce(lambda x, y: x | y, queries)

        filter_text = self.query_data["sSearch"]
        if filter_text:
            for target in filter_text.split():
                queryset = queryset.filter(get_filter_arguments(target))
        return queryset

    def sort_queryset(self, queryset):
        def get_sort_arguments():
            """
            Get list of arguments passed to `order_by()` function.
            """
            arguments = []
            for key, value in self.query_data.items():
                if not key.startswith("iSortCol_"):
                    continue
                field = self.columns[value].field
                dir = self.query_data["sSortDir_" + key.split("_")[1]]
                if dir == "asc":
                    arguments.append(field)
                else:
                    arguments.append("-" + field)
            return arguments
        order_args = get_sort_arguments()
        if order_args:
            queryset = queryset.order_by(*order_args)
        return queryset

    def convert_queryset_to_values_list(self, queryset):
        return [[col.render(obj) for col in self.columns] for obj in queryset]

    def get_context_data(self, **kwargs):
        sEcho = self.query_data["sEcho"]
        queryset = kwargs.pop("object_list")
        if queryset is not None:
            start = self.query_data["iDisplayStart"]
            length = self.query_data["iDisplayLength"]

            filtered_queryset = self.filter_queryset(queryset)
            sorted_queryset = self.sort_queryset(filtered_queryset)
            paginated_queryset = sorted_queryset[start : start + length]
            values_list = self.convert_queryset_to_values_list(paginated_queryset)
            context = {
                "sEcho": sEcho,
                "iTotalRecords": queryset.count(),
                "iTotalDisplayRecords": filtered_queryset.count(),
                "aaData": values_list,
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
        return self.render_to_json_response(context)
