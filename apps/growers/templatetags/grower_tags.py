# -*- coding: utf-8 -*-
"""
Several usefull template tags!
"""
from django import template
from django.contrib.auth.models import User

from growers.models import OrchidProduct

register = template.Library()

class RelatedProductsNode(template.Node):

    def __init__(self, context_var, obj):
        self.context_var = context_var
        self.obj_var = template.Variable(obj)

    def render(self, context):
        obj = self.obj_var.resolve(context)

        object_list = OrchidProduct.objects.filter(related_taxon=obj)
        if not object_list:
            object_list = OrchidProduct.objects.filter(related_taxon=obj.parent)

        context[self.context_var] = object_list
        return u""

@register.tag
def get_related_products_for(parser, token):
    """
    Usage: {% get_related_products_for <obj> as <some_var> %}
    """

    bits = token.split_contents()

    if len(bits) != 4:
        message = "'%s' tag requires three arguments" % bits[0]
        raise template.TemplateSyntaxError(message)

    return RelatedProductsNode(bits[3], bits[1])

