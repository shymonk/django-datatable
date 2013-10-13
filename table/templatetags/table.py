from django import template

register = template.Library()


@register.tag
def render_table(parser, token):
    pass
