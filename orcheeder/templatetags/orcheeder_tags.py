# -*- coding: utf-8 -*-
from django import template
from django.contrib.sites.models import Site
from django.db import models

from haystack.query import SearchQuerySet
from planet.models import Post


register = template.Library()


@register.filter
def template_fragment(result):
    return "search/results/{content_type}.html".format(content_type=result.content_type())


@register.filter
def get_full_url(obj):
    site = Site.objects.get_current()
    return "http://{domain}{url}".format(url=obj.get_absolute_url(), domain=site.domain)


class MoreLikeThisNode(template.Node):
    def __init__(self, model, varname, for_types=None, limit=None):
        self.model = template.Variable(model)
        self.varname = varname
        self.for_types = for_types
        self.limit = limit

        if not self.limit is None:
            self.limit = int(self.limit)

    def render(self, context):
        try:
            model_instance = self.model.resolve(context)
            sqs = SearchQuerySet()

            if not self.for_types is None:
                intermediate = template.Variable(self.for_types)
                for_types = intermediate.resolve(context).split(',')
                search_models = []

                for model in for_types:
                    model_class = models.get_model(*model.split('.'))

                    if model_class:
                        search_models.append(model_class)

            sqs = sqs.more_like_this(model_instance).models(*search_models).load_all()

            if not self.limit is None:
                sqs = sqs[:self.limit]

            context[self.varname] = sqs

        except:
            pass

        return ''


@register.tag
def orcheeder_more_like_this(parser, token):
    """
    Fetches similar items from the search index to find content that is similar
    to the provided model's content.

    Syntax::

        {% more_like_this model_instance as varname [for app_label.model_name,app_label.model_name,...] [limit n] %}

    Example::

        # Pull a full SearchQuerySet (lazy loaded) of similar content.
        {% more_like_this entry as related_content %}

        # Pull just the top 5 similar pieces of content.
        {% more_like_this entry as related_content limit 5  %}

        # Pull just the top 5 similar entries or comments.
        {% more_like_this entry as related_content for "blog.entry,comments.comment" limit 5  %}
    """
    bits = token.split_contents()

    if not len(bits) in (4, 6, 8):
        raise template.TemplateSyntaxError(u"'%s' tag requires either 3, 5 or 7 arguments." % bits[0])

    model = bits[1]

    if bits[2] != 'as':
        raise template.TemplateSyntaxError(u"'%s' tag's second argument should be 'as'." % bits[0])

    varname = bits[3]
    limit = None
    for_types = None

    if len(bits) == 6:
        if bits[4] != 'limit' and bits[4] != 'for':
            raise template.TemplateSyntaxError(u"'%s' tag's fourth argument should be either 'limit' or 'for'." % bits[0])

        if bits[4] == 'limit':
            limit = bits[5]
        else:
            for_types = bits[5]

    if len(bits) == 8:
        if bits[4] != 'for':
            raise template.TemplateSyntaxError(u"'%s' tag's fourth argument should be 'for'." % bits[0])

        for_types = bits[5]

        if bits[6] != 'limit':
            raise template.TemplateSyntaxError(u"'%s' tag's sixth argument should be 'limit'." % bits[0])

        limit = bits[7]

    return MoreLikeThisNode(model, varname, for_types, limit)


class RelatedPostsForObjectNode(template.Node):

    def __init__(self, context_var, obj):
        self.context_var = context_var
        self.obj_var = template.Variable(obj)

    def render(self, context):
        obj = self.obj_var.resolve(context)

        try:
            obj_ids = [result.id.split(".")[-1] for result in SearchQuerySet()\
                .models(Post).filter(text__icontains=obj.scientific)[:10]]
            object_list = Post.objects.filter(pk__in=obj_ids)
        except:
            object_list = []
        context[self.context_var] = object_list

        return u""


@register.tag
def search_related_posts_for(parser, token):
    """
    Usage: {% search_related_posts_for <obj> as <some_var> %}
    """

    bits = token.split_contents()

    if len(bits) != 4:
        message = "'%s' tag requires three arguments" % bits[0]
        raise template.TemplateSyntaxError(message)

    return RelatedPostsForObjectNode(bits[3], bits[1])
