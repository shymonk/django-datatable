from django import template
from django.template import Context


register = template.Library()


class TableNode(template.Node):
    def __init__(self, table):
        self.table = table

    def render(self, context):
        t = template.loader.get_template("table.html")
        
        rows = [{'num': i, 'person_name': self.table.tbody[i].name}
                for i in range(len(self.table.tbody))]
        context = Context({'id': self.table.name, 'thead': self.table.thead, 'tbody': rows})
        return t.render(context)


@register.tag
def render_table(parser, token):
    try:
        tag, table = token.split_contents()
    except ValueError:
        msg = '%r tag requires a single argument' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return TableNode(table)
