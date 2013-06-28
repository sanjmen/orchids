# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from taxon.models import Genus, Imagen
from planet.models import Blog

def home(request):
    """
        return home page
    """

    images = Imagen.objects.all().order_by('-created_at')[:12]
    blogs = Blog.objects.all().order_by('-date_created')[:16]
    genus = Genus.objects.filter(description__isnull=False).order_by('-updated_at')[:6]

    return render_to_response("homepage.html",
            {"images": images,
                "blogs": blogs, "genus": genus},
            context_instance=RequestContext(request))


