from django import template
from django.template import Context


register = template.Library()


class TableNode(template.Node):
    def __init__(self, table):
        self.table = template.Variable(table)

    def render(self, context):
        table = self.table.resolve(context)

        columns = [column.title for column in table.columns]
        objects = []
        if table.opts.model:
            queryset = table.opts.model.objects.all()
        else:
            queryset = table.data
        fields = [col.field for col in table.columns if col.field]
        for obj in queryset:
            objects.append([getattr(obj, field) for field in fields])
        
        context = Context({'name': table.opts.id, 'columns': columns, 'object_list': objects})
        t = template.loader.get_template("table.html")        
        return t.render(context)


@register.tag
def render_table(parser, token):
    try:
        tag, table = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single arguments' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return TableNode(table)
