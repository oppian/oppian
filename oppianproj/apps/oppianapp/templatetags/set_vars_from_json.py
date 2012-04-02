'''
Created on Oct 1, 2009

@author: stephenhartley

Originally from http://code.djangoproject.com/ticket/1322
'''

from django import template
from django.utils import simplejson as json

register = template.Library()

@register.tag()
def set_vars_from_json(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, json_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not (json_string[0] == json_string[-1] and json_string[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name    
    return SetVariables(json.loads(json_string[1:-1]))

class SetVariables(template.Node):
    def __init__(self, variables):
        self.variables = variables
    def render(self, context):
        for key in self.variables.iterkeys():
            context[key] = self.variables[key]
        return ''


@register.tag()
def set_vars_from_json_block(parser, token):
    nodelist = parser.parse(('end_set_vars_from_json_block',))
    parser.delete_first_token()
    return JsonNode(nodelist)

class JsonNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        try:
            output = self.nodelist.render(context)
            variables = json.loads(output)
            for key in variables.iterkeys():
                context[key] = variables[key]
        except:
            pass
        return ''
