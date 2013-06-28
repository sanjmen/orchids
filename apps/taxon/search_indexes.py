# -*- coding: utf-8 -*-

from haystack import indexes

from taxon.models import Species, Genus, Name


class GenusIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """
    Search Index for taxon.Genus
    """
    name = indexes.CharField()
    text = indexes.CharField(document=True, use_template=True)
    rank = indexes.CharField(model_attr="rank")

    countries = indexes.FacetMultiValueField(null=True)
    tags = indexes.FacetMultiValueField(null=True)

    created_at = indexes.DateTimeField(model_attr="created_at")

    class Meta:
        model = Genus
        fields = ["created_at"]

    def prepare_name(self, obj):
        return obj.get_partial()

    def prepare_rank(self, obj):
        return obj.get_rank_display()

    def prepare_tags(self, obj):
        return [tag.strip() for tag in obj.tags.split(",")]

    def prepare_countries(self, obj):
        return [country.printable_name for country in obj.countries.all()]

    def get_updated_field(self):
        return "updated_at"

    def index_queryset(self, using=None):
        return Genus.objects.all()


class SpeciesIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """
    Search Index for taxon.Species
    """
    name = indexes.CharField()
    text = indexes.CharField(document=True, use_template=True)
    rank = indexes.CharField(model_attr="rank")

    countries = indexes.FacetMultiValueField(null=True)
    tags = indexes.FacetMultiValueField(null=True)

    created_at = indexes.DateTimeField(model_attr="created_at")

    class Meta:
        model = Species
        fields = ["created_at"]

    def prepare_name(self, obj):
        return obj.get_partial()

    def prepare_rank(self, obj):
        return obj.get_rank_display()

    def prepare_tags(self, obj):
        return [tag.strip() for tag in obj.tags.split(",")]

    def prepare_countries(self, obj):
        return [country.printable_name for country in obj.countries.all()]

    def get_updated_field(self):
        return "updated_at"

    def index_queryset(self, using=None):
        return Species.objects.all()


class NameIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """
    Search Index for taxon.Name
    """
    name = indexes.CharField()
    text = indexes.CharField(document=True, use_template=True)
    rank = indexes.CharField(model_attr="rank")

    countries = indexes.FacetMultiValueField(null=True)
    tags = indexes.FacetMultiValueField(null=True)

    created_at = indexes.DateTimeField(model_attr="created_at")

    class Meta:
        model = Name
        fields = ["created_at"]

    def prepare_name(self, obj):
        return obj.get_partial()

    def prepare_rank(self, obj):
        return obj.get_rank_display()

    def prepare_tags(self, obj):
        return [tag.strip() for tag in obj.tags.split(",")]

    def prepare_countries(self, obj):
        return [country.printable_name for country in obj.countries.all()]

    def get_updated_field(self):
        return "updated_at"

    def index_queryset(self, using=None):
        return Name.objects.all()

