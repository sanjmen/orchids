# -*- coding: utf-8 -*-

from haystack import indexes

from growers.models import Grower, OrchidProduct


class GrowerIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """
    Search Index for growers.Grower
    """
    grower_name = indexes.CharField(model_attr="name")
    text = indexes.CharField(document=True, use_template=True)

    country = indexes.CharField(model_attr="country")
    state = indexes.CharField(model_attr="usstate")
    address = indexes.CharField(model_attr="address")

    tags = indexes.FacetMultiValueField(null=True)

    created_at = indexes.DateTimeField(model_attr="created_at")

    class Meta:
        model = Grower
        fields = ["grower_name", "country", "state", "address", "created_at"]

    def prepare_tags(self, obj):
        return [tag.strip() for tag in obj.tags.split(",")]

    def index_queryset(self, using=None):
        return Grower.objects.all()


class OrchidProductIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """
    Search index for growers.OrchidProduct
    """
    grower = indexes.CharField(model_attr="grower")
    title = indexes.CharField(model_attr="title")
    text = indexes.CharField(document=True, use_template=True)

    price = indexes.CharField(model_attr="price")
    mount = indexes.CharField(model_attr="mount")

    created_at = indexes.DateTimeField(model_attr="created_at")

    class Meta:
        model = OrchidProduct
        fields = ["title", "price", "mount", "created_at"]

    def prepare_grower(self, obj):
        return obj.grower.id

    def index_queryset(self, using=None):
        return OrchidProduct.objects.exclude(publish=False)
