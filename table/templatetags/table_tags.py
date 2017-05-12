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
        t = template.loader.get_template(
            table.opts.template_name or self.template_name)
        context = {'table': table}
        return t.render(context)


class SimpleTableNode(TableNode):
    template_name = "table/simple_table.html"


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
