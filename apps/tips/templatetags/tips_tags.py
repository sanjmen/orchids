# -*- coding: utf-8 -*-
"""
"""
from django import template

from tips.models import Tip


register = template.Library()


class TipsNode(template.Node):

    def __init__(self, context_var, obj):
        self.context_var = context_var
        self.obj_var = template.Variable(obj)

    def render(self, context):
        obj = self.obj_var.resolve(context)

        object_list = Tip.objects.filter(name=obj).select_related("author", "name")

        context[self.context_var] = object_list

        return u""


@register.tag
def get_tips_for(parser, token):
    """
    Usage: {% get_tips_for <obj> as <some_var> %}
    """

    bits = token.split_contents()

    if len(bits) != 4:
        message = "'%s' tag requires three arguments" % bits[0]
        raise template.TemplateSyntaxError(message)

    return TipsNode(bits[3], bits[1])
