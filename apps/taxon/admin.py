# -*- coding: UTF-8 -*-
from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from taxon.models import Source, SourceKey, Authorship, Reference, Name, Imagen

class NameAdmin(admin.ModelAdmin):
    list_display = ('rank', 'scientific', 'genus_hybrid_marker',
        'parent', 'genus_name', 'species_hybrid_marker', 'species_epithet',
            'infraspecific_rank', 'infraspecific_epithet')
    list_select_related = True
    search_fields = ('scientific', 'genus_name', 'species_epithet')
    list_filter = ('rank', 'name_status')


class ImagenAdmin(AdminImageMixin, admin.ModelAdmin):
        pass

admin.site.register(Imagen, ImagenAdmin)
admin.site.register(Name, NameAdmin)
admin.site.register(Source)
admin.site.register(SourceKey)
admin.site.register(Authorship)
admin.site.register(Reference)
