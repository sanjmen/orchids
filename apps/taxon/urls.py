# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('taxon.views',
        url(r'^species/(?P<name_id>\d+)/(?P<slug>.*?)/tips/$', "species_more_tips", name="species_more_tips"),
        url(r'^genus/(?P<name_id>\d+)/(?P<slug>.*?)/tips/$', "genus_more_tips", name="genus_more_tips"),
        url(r'^genus/(?P<name_id>\d+)/(?P<slug>.*?)/news/$', "genus_more_posts", name="genus_more_posts"),
        url(r'^species/(?P<name_id>\d+)/(?P<slug>.*?)/news/$', "species_more_posts", name="species_more_posts"),
        url(r'^species/(?P<species_id>\d+)/(?P<slug>.*?)/$', "species_detail", name="species_detail"),
        url(r'^genus/(?P<genus_id>\d+)/(?P<slug>.*?)/$', "genus_detail", name="genus_detail"),
        url(r'^(?P<synonym_id>\d+)/(?P<slug>.*?)/$', "synonym_detail", name="synonym_detail"),
        )
