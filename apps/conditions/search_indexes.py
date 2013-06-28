# -*- coding: utf-8 -*-

from haystack import indexes

from conditions.models import NaturalCondition, GrowingCondition


class NaturalIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """
    Search Index for conditions.NaturalCondition
    """
    name = indexes.CharField(model_attr="name")
    text = indexes.CharField(document=True, use_template=True)
    condition_type = indexes.CharField(model_attr="condition_type")
    source_description = indexes.CharField(model_attr="source_description")

    created_at = indexes.DateTimeField(model_attr="created_at")

    class Meta:
        model = NaturalCondition
        fields = ["condition_type", "source_description", "created_at"]

    def prepare_name(self, obj):
        return obj.name.scientific

    def index_queryset(self, using=None):
        return NaturalCondition.objects.all()


class GrowingIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """
    Search Index for conditions.GrowingCondition
    """
    name = indexes.CharField()
    text = indexes.CharField(document=True, use_template=True)
    condition_type = indexes.CharField(model_attr="condition_type")
    source_description = indexes.CharField(model_attr="source_description")

    created_at = indexes.DateTimeField(model_attr="created_at")

    class Meta:
        model = GrowingCondition
        fields = ["condition_type", "source_description", "created_at"]

    def prepare_name(self, obj):
        return obj.name.scientific

    def index_queryset(self, using=None):
        return GrowingCondition.objects.all()


