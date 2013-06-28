# -*- coding: UTF-8 -*-
from django.contrib import admin

from tips.models import Tip


class TipAdmin(admin.ModelAdmin):
    list_display = ("author", "name", "text", "source_description", "created_at")
    list_select_related = True
    search_fields = ("author", "name")
    list_filter = ("author", "source_description")
    raw_id_fields = ("name", "author")

admin.site.register(Tip, TipAdmin)
