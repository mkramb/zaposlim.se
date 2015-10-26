from django import template
from django.conf import settings

register = template.Library()

class StraightIncludeNode(template.Node):
    def __init__(self, template_path):
        self.filepath = '%s/%s' % (settings.TEMPLATE_DIRS[0], template_path)

    def render(self, context):
        fp = open(self.filepath, 'r')
        output = fp.read()
        fp.close()
        return output

@register.tag("straight_include")
def do_straight_include(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("%r tag takes one argument: the location of the file within the template folder" % bits[0])
    path = bits[1][1:-1]

    return StraightIncludeNode(path)

@register.filter
def truncatechars(s, num):
    """
    Truncates a word after a given number of chars
    Argument: Number of chars to truncate after
    """
    length = int(num)
    string = []
    for word in s.split():
        if len(' '.join(string)) > length:
            string.append(word[:length]+'...')
            break
        else:
            string.append(word)
    return u' '.join(string)

@register.filter
def truncate(value, arg):
    """
    Truncates a string after a given number of chars
    Argument: Number of chars to truncate after
    """
    try:
        length = int(arg)
    except ValueError: # invalid literal for int()
        return value # Fail silently.
    if not isinstance(value, basestring):
        value = str(value)
    if (len(value) > length):
        return value[:length] + "..."
    else:
        return value
