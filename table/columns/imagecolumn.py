#!/usr/bin/env python
# coding: utf-8
from django.template import Template, Context

from table.columns import Column
from table.utils import Accessor


class ImageColumn(Column):
    def __init__(self, field=None, image_title=None, *args, **kwargs):
        kwargs["sortable"] = False
        kwargs["searchable"] = False
        self.image_title = image_title
        super(ImageColumn, self).__init__(field=field, *args, **kwargs)

    def render(self, obj):
        path = Accessor(self.field).resolve(obj)
        if isinstance(self.image_title, Accessor):
            title = self.image_title.resolve(self.obj)
        else:
            title = self.image_title
        template = Template('{%% load static %%}<img src="{%% static "%s" %%}"'
                            ' title="%s">' % (path, title))
        return template.render(Context())
