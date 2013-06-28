# -*- coding: UTF-8 -*-
from django.contrib import admin

from conditions.models import ConditionType, Condition


class ConditionTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("name", )

admin.site.register(ConditionType, ConditionTypeAdmin)


class ConditionAdmin(admin.ModelAdmin):
    list_display = ("condition_type", "author", "name", "text", "natural", "source_description", "created_at")
    list_select_related = True
    search_fields = ("condition_type__name", "author", "name")
    list_filter = ("author", "condition_type", "source_description", "natural")
    raw_id_fields = ("name", )

admin.site.register(Condition, ConditionAdmin)
