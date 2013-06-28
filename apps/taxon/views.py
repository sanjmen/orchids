# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext

from haystack.query import SearchQuerySet
from conditions.models import Condition
from taxon.models import Name, Species, Imagen
from tips.models import Tip
from planet.models import Post


def get_name(name_id, slug):
    try:
        taxon = Name.objects.select_related("parent").get(pk=name_id)

    except Name.DoesNotExist:
        scientific = " ".join(slug.split('-'))
        taxon = get_object_or_404(Name, scientific=scientific)

    return taxon


def _get_related_posts_for(taxon):
    post_ids = [result.id.split(".")[-1] for
        result in SearchQuerySet().models(Post).filter(text__icontains=taxon.scientific)]
    return Post.objects.filter(pk__in=post_ids)


def species_detail(request, species_id, slug):
    taxon = get_name(species_id, slug)

    if taxon.name_status == 's':
        raise Http404

    if taxon.rank == 'gen.':
        return HttpResponseRedirect(reverse(genus_detail, args=(species_id, slug)))

    if taxon.rank != 'sp.':
        raise Http404

    return render_to_response("taxon/species.html",
            {"taxon": taxon},
            context_instance=RequestContext(request))


def genus_detail(request, genus_id, slug):
    taxon = get_name(genus_id, slug)

    if taxon.rank != 'gen.':
        return HttpResponseRedirect(reverse(species_detail, args=(genus_id, slug)))

    if taxon.name_status == 's':
        raise Http404

    species_list = Species.objects.filter(parent=taxon).order_by("scientific")

    return render_to_response("taxon/genus.html",
            {"taxon": taxon, 'species_list': species_list},
            context_instance=RequestContext(request))


def species_more_tips(request, name_id, slug):
    taxon = get_name(name_id, slug)

    if taxon.rank == 'gen.':
        return HttpResponseRedirect(reverse(genus_more_tips, args=(name_id, slug)))

    if taxon.name_status == 's':
        return Http404

    tip_list = Condition.objects.filter(name=taxon, natural=False) or \
            Condition.objects.filter(name=taxon.parent, natural=False) or \
            Tip.objects.filter(name=taxon)

    if not tip_list:
        tip_list = get_list_or_404(Tip, name=taxon.get_parent)

    has_genus_tips = Condition.objects.filter(name=taxon.parent, natural=False).exists()\
                    or Tip.objects.filter(name=taxon.parent).exists()

    return render_to_response("taxon/more_tips.html", {"taxon": taxon,
        'tip_list': tip_list, 'has_genus_tips': has_genus_tips},
            context_instance=RequestContext(request))


def genus_more_tips(request, name_id, slug):
    taxon = get_name(name_id, slug)

    if taxon.rank != 'gen.':
        return HttpResponseRedirect(reverse(species_more_tips, args=(name_id, slug)))

    if taxon.name_status == 's':
        return Http404

    tip_list = Condition.objects.filter(name=taxon, natural=False)
    if not tip_list:
        tip_list = get_list_or_404(Tip, name=taxon)

    return render_to_response("taxon/more_tips.html",
            {"taxon": taxon, 'tip_list': tip_list},
            context_instance=RequestContext(request))


def species_more_posts(request, name_id, slug):
    taxon = get_name(name_id, slug)

    if taxon.rank == 'gen.':
        return HttpResponseRedirect(reverse(genus_more_posts, args=(name_id, slug)))

    related_post_list = _get_related_posts_for(taxon)

    if not related_post_list:
        raise Http404

    return render_to_response("taxon/more_posts.html",
            {"taxon": taxon, 'related_post_list': related_post_list},
            context_instance=RequestContext(request))


def genus_more_posts(request, name_id, slug):
    taxon = get_name(name_id, slug)

    if taxon.rank != 'gen.':
        return HttpResponseRedirect(reverse(species_more_posts, args=(name_id, slug)))

    related_post_list = _get_related_posts_for(taxon)

    if not related_post_list:
        raise Http404

    return render_to_response("taxon/more_posts.html",
            {"taxon": taxon, 'related_post_list': related_post_list},
            context_instance=RequestContext(request))


def view_image(request, photo_id):
    if not request.is_ajax():
        raise Http404

    photo = get_object_or_404(Imagen, pk=photo_id)

    return render_to_response("taxon/image.html",
            {"photo": photo}, context_instance=RequestContext(request))


def synonym_detail(request, synonym_id, slug):
    taxon = get_name(synonym_id, slug)

    if taxon.name_status is 'a':
        raise Http404

    related_post_list = _get_related_posts_for(taxon)

    return render_to_response("taxon/synonym.html",
            {"taxon": taxon, 'related_post_list': related_post_list},
            context_instance=RequestContext(request))


