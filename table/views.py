#!/usr/bin/env python
# coding: utf-8

from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.generic.list import BaseListView


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
        return BaseListView.get(self, request, *args, **kwargs)

    def get_queryset(context):
        pass

    def get_context_data(self, **kwargs):
        return context

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)



