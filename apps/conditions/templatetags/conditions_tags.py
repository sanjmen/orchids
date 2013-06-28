# -*- coding: utf-8 -*-
from django import template

from conditions.models import Condition


register = template.Library()


class NaturalConditionsNode(template.Node):

    def __init__(self, context_var, obj):
        self.context_var = context_var
        self.obj_var = template.Variable(obj)

    def render(self, context):
        obj = self.obj_var.resolve(context)

        object_list = Condition.objects.filter(name=obj, natural=True)\
            .select_related("author", "condition_type").order_by("condition_type__code")

        context[self.context_var] = object_list

        return u""


class GrowingConditionsNode(template.Node):

    def __init__(self, context_var, obj):
        self.context_var = context_var
        self.obj_var = template.Variable(obj)

    def render(self, context):
        obj = self.obj_var.resolve(context)

        object_list = Condition.objects.filter(name=obj, natural=False)\
            .select_related("author", "condition_type").order_by("condition_type__code")

        context[self.context_var] = object_list

        return u""


@register.tag
def get_natural_conditions_for(parser, token):
    """
    Usage: {% get_natural_conditions_for <obj> as <some_var> %}
    """

    bits = token.split_contents()

    if len(bits) != 4:
        message = "'%s' tag requires three arguments" % bits[0]
        raise template.TemplateSyntaxError(message)

    return NaturalConditionsNode(bits[3], bits[1])


@register.tag
def get_growing_conditions_for(parser, token):
    """
    Usage: {% get_growing_conditions_for <obj> as <some_var> %}
    """

    bits = token.split_contents()

    if len(bits) != 4:
        message = "'%s' tag requires three arguments" % bits[0]
        raise template.TemplateSyntaxError(message)

    return GrowingConditionsNode(bits[3], bits[1])

