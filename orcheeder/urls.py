# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page
from django.views.generic import RedirectView, TemplateView

from haystack.views import search_view_factory

from orcheeder.forms import OrcheederInlineSearchForm
from orcheeder.sitemaps import sitemaps_dict
from orcheeder.views import home


admin.autodiscover()


urlpatterns = patterns("",
    url(r"^$", home, name="home"),
    url(r"^about/", TemplateView.as_view(template_name="about/about.html"), name="about"),

    url(r"^admin/", include(admin.site.urls)),

    url(r"^account/", include("account.urls")),
    url(r'^news/', include('planet.urls')),
    url(r'^search/$', search_view_factory(
        form_class=OrcheederInlineSearchForm,
    ), name='haystack_search'),
    (r'^robots\.txt$', include('robots.urls')),

    url(r'^orchid/', include('taxon.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^growers/', include('growers.urls')),
    url(r'^orchids-for-sale/', include('growers.urls')),

)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += patterns('',
    #redirects
    url(r'^orchids/species/(?P<slug>.*?)/(?P<species_id>\d+)/$', RedirectView.as_view(url='/orchid/species/%(species_id)s/%(slug)s/')),
    url(r'^orchids/generas/(?P<slug>.*?)/(?P<genus_id>\d+)/$', RedirectView.as_view(url='/orchid/genus/%(genus_id)s/%(slug)s/')),
    url(r'^orchids/species/(?P<slug>.*?)/(?P<species_id>\d+)/tips/$', RedirectView.as_view(url='/orchid/species/%(species_id)s/%(slug)s/tips/')),
    url(r'^orchids/generas/(?P<slug>.*?)/(?P<genus_id>\d+)/tips/$', RedirectView.as_view(url='/orchid/genus/%(genus_id)s/%(slug)s/tips/')),
    url(r'^orchids/species/(?P<slug>.*?)/(?P<species_id>\d+)/posts/$', RedirectView.as_view(url='/orchid/species/%(species_id)s/%(slug)s/news/')),
    url(r'^orchids/generas/(?P<slug>.*?)/(?P<genus_id>\d+)/posts/$', RedirectView.as_view(url='/orchid/genus/%(genus_id)s/%(slug)s/news/')),
    )


# sitemaps
urlpatterns += patterns('',
    url(r'^sitemap.xml$',
        cache_page(172800)(sitemaps_views.index),
        {'sitemaps': sitemaps_dict, 'sitemap_url_name': 'sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(172800)(sitemaps_views.sitemap),
        {'sitemaps': sitemaps_dict}, name='sitemaps'),
)
