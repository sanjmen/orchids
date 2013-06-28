# -*- coding: utf-8 -*-
"""
Several usefull template tags!
"""
from random import shuffle, sample, randint

from django import template
from django.contrib.auth.models import User

from haystack.query import SearchQuerySet

from taxon.models import Genus, Species


register = template.Library()


class LatestSpeciesNode(template.Node):

    def __init__(self, context_var, model):
        self.context_var = context_var
        self.model = model

    def render(self, context):
        object_list = Species.objects.filter(imagen__isnull=False).distinct().order_by("-updated_at")[:12]
        context[self.context_var] = object_list
        return u""


class LatestGenusNode(template.Node):

    def __init__(self, context_var, model):
        self.context_var = context_var
        self.model = model

    def render(self, context):
        object_list = Genus.objects.all().order_by("-updated_at")[:12]
        context[self.context_var] = object_list
        return u""


class LatestNamesNode(template.Node):

    def __init__(self, context_var, model):
        self.context_var = context_var
        self.model = model

    def render(self, context):
        object_list = SearchQuerySet().models(self.model).order_by("-updated_at").load_all()
        context[self.context_var] = object_list
        return u""


class TaxonWithTipsNode(template.Node):

    def __init__(self, context_var, obj):
        self.context_var = context_var
        self.obj_var = template.Variable(obj)

    def render(self, context):
        obj = self.obj_var.resolve(context)

        object_list = Species.objects.filter(tip__isnull=False, imagen__isnull=False).distinct().exclude(pk=obj.pk)[:12]

        context[self.context_var] = object_list

        return u""


TOP_GENUS = (
        (624, "phalaenopsis"),
        (133, "cattleya"),
        (857, "vanda"),
        (228, "cymbidium"),
        (253, "dendrobium"),
        (571, "oncidium"),
        (563, "odontoglossum"),
        (602, "paphiopedilum"),
        (234, "cypripedium"),
        (628, "phragmipedium"),
        (132, "catasetum"),
        (789, "stanhopea"),
        )


class TopGenusNode(template.Node):

    def __init__(self, context_var, model):
        self.context_var = context_var
        self.model = model

    def render(self, context):
        object_list = []
        for g in TOP_GENUS:
            object_list.append(Genus.objects.get(pk=g[0]))

        context[self.context_var] = object_list

        return u""


@register.tag
def get_latest_genus(parser, token):
    """
    Usage: {% get_latest_genus as <some_var> %}
    """

    bits = token.split_contents()

    if len(bits) != 3:
        message = "'%s' tag requires two arguments" % bits[0]
        raise template.TemplateSyntaxError(message)

    return LatestGenusNode(bits[2], Genus)


@register.tag
def get_latest_species(parser, token):
    """
    Usage: {% get_latest_species as <some_var> %}
    """

    bits = token.split_contents()

    if len(bits) != 3:
        message = "'%s' tag requires two arguments" % bits[0]
        raise template.TemplateSyntaxError(message)

    return LatestSpeciesNode(bits[2], Species)


@register.tag
def get_taxones_with_tips_for(parser, token):
    """
    Usage: {% get_taxones_with_tips_for <obj> as <some_var> %}
    """

    bits = token.split_contents()

    if len(bits) != 4:
        message = "'%s' tag requires three arguments" % bits[0]
        raise template.TemplateSyntaxError(message)

    return TaxonWithTipsNode(bits[3], bits[1])


@register.tag
def get_top_genus(parser, token):
    """
    Usage: {% get_top_genus as <some_var> %}
    """
    bits = token.split_contents()

    if len(bits) != 3:
        message = "'%s' tag requires two arguments" % bits[0]
        raise template.TemplateSyntaxError(message)

    return TopGenusNode(bits[2], Genus)


@register.filter(name='randomize_list')
def randomize_list(alist, sample_count=None):
    shuffle(alist)
    if sample_count:
        sample_count = min(len(alist), int(sample_count))
        alist = sample(alist, sample_count)
    return alist


@register.filter(name='get_user')
def get_user(username):
    user = User.objects.get(username=username)
    return user

@register.filter(name='randint')
def get_rrandint(top):
    return randint(0, top)

