# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.sitemaps import Sitemap

from taxon.models import Species, Genus


class SpeciesSitemap(Sitemap):

    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return Species.objects.exclude(name_status="s")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("taxon.views.species_detail",
            kwargs=dict(slug=obj.get_slug(), species_id=obj.id, ))


class GenusSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Genus.objects.exclude(name_status="s")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("taxon.views.genus_detail",
            kwargs=dict(slug=obj.get_slug(), genus_id=obj.id, ))


class GenusTipSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Genus.objects.filter(tip__isnull=False)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("taxon.views.genus_more_tips",
            kwargs=dict(slug=obj.get_slug(), name_id=obj.id, ))


class SpeciesTipSitemap(Sitemap):

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Species.objects.filter(tip__isnull=False).distinct()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse("taxon.views.species_more_tips",
            kwargs=dict(slug=obj.get_slug(), name_id=obj.id, ))
