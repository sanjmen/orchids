# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from growers.models import Grower, OrchidProduct


def grower_detail(request, slug):
    grower = get_object_or_404(Grower, slug=slug)

    return render_to_response("growers/grower.html",
            {"grower": grower},
            context_instance=RequestContext(request))


def product_detail(request, slug, product_id):
    product = get_object_or_404(OrchidProduct, pk=product_id)

    if not product.publish:
        raise Http404

    return render_to_response("growers/product.html",
            {"product": product},
            context_instance=RequestContext(request))

