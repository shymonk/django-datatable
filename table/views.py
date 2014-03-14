#!/usr/bin/env python
# coding: utf-8

from django.db.models import Q
from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.generic.list import BaseListView
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseBadRequest

from table.forms import QueryDataForm
from table.columns import LinkColumn
from table.tables import TableDataMap
from table.utils import A

class JSONResponseMixin(object):
    """
    A mixin that allows you to easily serialize simple data such as a dict or
    Django models.
    """
    content_type = None
    json_dumps_kwargs = None

    def get_content_type(self):
        if (self.content_type is not None and
            not isinstance(self.content_type,
                           (six.string_types, six.text_type))):
            raise ImproperlyConfigured(
                '{0} is missing a content type. Define {0}.content_type, '
                'or override {0}.get_content_type().'.format(
                    self.__class__.__name__))
        return self.content_type or u"application/json"

    def get_json_dumps_kwargs(self):
        if self.json_dumps_kwargs is None:
            self.json_dumps_kwargs = {}
        self.json_dumps_kwargs.setdefault(u'ensure_ascii', False)
        return self.json_dumps_kwargs

    def render_json_response(self, context_dict, status=200):
        """
        Limited serialization for shipping plain data. Do not use for models
        or other complex or custom objects.
        """
        json_context = json.dumps(
            context_dict,
            cls=DjangoJSONEncoder,
            **self.get_json_dumps_kwargs()).encode(u'utf-8')
        return HttpResponse(json_context,
                            content_type=self.get_content_type(),
                            status=status)

    def render_json_object_response(self, objects, **kwargs):
        """
        Serializes objects using Django's builtin JSON serializer. Additional
        kwargs can be used the same way for django.core.serializers.serialize.
        """
        json_data = serializers.serialize(u"json", objects, **kwargs)
        return HttpResponse(json_data, content_type=self.get_content_type())


class FeedDataView(JSONResponseMixin, BaseListView):
    """
    The view to feed ajax data of table.
    """
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
        """
        Get `Q` object passed to `filter` function.
        """
        search = self.query_data["sSearch"]
        print search
        search_columns = TableDataMap.get_columns(self.token)
        search_fields = [col.field for col in search_columns if col.searchable]
        queries = []
        for field in search_fields:
            key = "__".join(field.split(".") + ["icontains"])
            value = search
            queries.append(Q(**{key: value}))
        return reduce(lambda x, y: x|y, queries)

    def get_sort_arguments(self):
        """
        Get list of arguments passed to `order_by()` function.
        """
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
        order_args = self.get_sort_arguments()
        queryset = queryset.filter(filter_args).order_by(*order_args)
        return queryset

    def convert_queryset_to_values_list(self, queryset):
        values_list = []
        columns = TableDataMap.get_columns(self.token)
        for obj in queryset:
            values_list.append([column.render(obj) for column in columns])
        return values_list
        
    def get_context_data(self, **kwargs):
        sEcho = self.query_data["sEcho"]
        queryset = kwargs.pop("object_list")
        if queryset is not None:
            start = self.query_data["iDisplayStart"]
            length = self.query_data["iDisplayLength"]

            filtered_queryset = self.filter_queryset(queryset)
            paginated_queryset = filtered_queryset[start:start+length]
            values_list = self.convert_queryset_to_values_list(paginated_queryset)
            context = {
                "sEcho": sEcho,
                "iTotalRecords": queryset.count(),
                "iTotalDisplayRecords": filtered_queryset.count(),
                "aaData": [list(e) for e in values_list],
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
        return self.render_json_response(context)

