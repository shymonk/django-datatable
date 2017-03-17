#!/usr/bin/env python
# coding: utf-8
from django import template
from django.template import Context


register = template.Library()


class TableNode(template.Node):
    template_name = "table/table.html"

    def __init__(self, table):
        self.table = template.Variable(table)

    def render(self, context):
        table = self.table.resolve(context)
        context = Context({'table': table})
        t = template.loader.get_template(self.template_name)
        return t.render(context)


class SimpleTableNode(TableNode):
    template_name = "table/simple_table.html"


class TableTableNode(TableNode):
    template_name = "table/table_table.html"


class MediaTableNode(TableNode):
    template_name = "table/table_media.html"


class ScriptTableNode(TableNode):
    template_name = "table/table_script.html"


@register.tag
def render_table(parser, token):
    try:
        tag, table = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single arguments' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return TableNode(table)


@register.tag
def render_simple_table(parser, token):
    try:
        tag, table = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single arguments' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return SimpleTableNode(table)


@register.tag
def render_table_table(parser, token):
    try:
        tag, table = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single arguments' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return TableTableNode(table)


@register.tag
def render_media_table(parser, token):
    try:
        tag, table = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single arguments' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return MediaTableNode(table)


@register.tag
def render_script_table(parser, token):
    try:
        tag, table = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single arguments' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return ScriptTableNode(table)