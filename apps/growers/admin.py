# -*- coding: UTF-8 -*-
from django.contrib import admin

from growers.models import Grower, OrchidProduct

class GrowerAdmin(admin.ModelAdmin):
    pass


def make_published(modeladmin, request, queryset):
    queryset.update(publish=True)
make_published.short_description = "Publish selected products"


def make_unpublished(modeladmin, request, queryset):
    queryset.update(publish=False)
make_unpublished.short_description = "Unpublish selected products"


class OrchidProductAdmin(admin.ModelAdmin):
    list_display = ("title", "grower", "origin", "publish", "created_at")
    search_fields = ("title", "origin")
    list_filter = ("publish", "grower")
    actions = [make_published, make_unpublished]


admin.site.register(Grower, GrowerAdmin)
admin.site.register(OrchidProduct, OrchidProductAdmin)
