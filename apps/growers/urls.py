# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('growers.views',
        url(r'^(?P<slug>[-\w]+)/$', "grower_detail", name="grower_detail"),
        url(r'^(?P<slug>.*?)/(?P<product_id>\d+)/$', "product_detail", name="product_detail"),
        )

