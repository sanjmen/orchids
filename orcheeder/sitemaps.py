# -*- coding: utf-8 -*-
from django.contrib.flatpages.models import FlatPage
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from planet.models import Post, Blog, Feed, Author

from taxon.sitemaps import SpeciesSitemap, GenusSitemap, GenusTipSitemap, SpeciesTipSitemap
from growers.models import Grower, OrchidProduct


class FlatPageSitemap(Sitemap):

    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return FlatPage.objects.all()


class BlogSitemap(Sitemap):

    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Blog.objects.values_list("id", "date_created")

    def lastmod(self, obj):
        return obj[1]

    def location(self, obj):
        return reverse("planet.views.blog_detail", kwargs=dict(blog_id=obj[0], ))


class PostSitemap(Sitemap):

    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Post.objects.values_list("id", "date_created")

    def lastmod(self, obj):
        return obj[1]

    def location(self, obj):
        return reverse("planet.views.post_detail", kwargs=dict(post_id=obj[0], ))


class AuthorSitemap(Sitemap):

    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Author.objects.values_list("id")

    def location(self, obj):
        return reverse("planet.views.author_detail", kwargs=dict(author_id=obj[0], ))


class FeedSitemap(Sitemap):

    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Feed.objects.values_list("id", "last_modified")

    def lastmod(self, obj):
        return obj[1]

    def location(self, obj):
        return reverse("planet.views.feed_detail", kwargs=dict(feed_id=obj[0], ))


class GrowerSitemap(Sitemap):

    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return Grower.objects.values_list("slug", "updated_at")

    def lastmod(self, obj):
        return obj[1]

    def location(self, obj):
        return reverse("growers.views.grower_detail", kwargs=dict(slug=obj[0], ))


class OrchidProductSitemap(Sitemap):

    changefreq = "always"
    priority = 0.9

    def items(self):
        return OrchidProduct.objects.filter(publish=True)\

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


sitemaps_dict = {
    "blogs": BlogSitemap(),
    "posts": PostSitemap(),
    "authors": AuthorSitemap(),
    "feeds": FeedSitemap(),
    "species": SpeciesSitemap(),
    "genus": GenusSitemap(),
    "species-tips": SpeciesTipSitemap(),
    "genus-tips": GenusTipSitemap(),
    #"conditions": ConditionSitemap(),
    "pages": FlatPageSitemap(),
    "growers": GrowerSitemap(),
    "products": OrchidProductSitemap(),
}
