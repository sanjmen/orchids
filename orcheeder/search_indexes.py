# -*- coding: utf-8 -*-

from haystack import indexes

from planet.models import Post


class PostIndex(indexes.ModelSearchIndex, indexes.Indexable):
    """
    Search Index for planet.Post
    """
    title = indexes.CharField(model_attr="title")
    text = indexes.CharField(document=True, use_template=True)
    authors = indexes.CharField()
    feed_id = indexes.IntegerField(model_attr="feed__id")
    blog_id = indexes.IntegerField(model_attr="feed__blog__id")

    tags = indexes.FacetMultiValueField(null=True)

    created_at = indexes.DateTimeField(model_attr="date_created")

    class Meta:
        model = Post
        fields = ["title", "tags", "created_at"]

    def get_updated_field(self):
        return "date_modified"

    def prepare_authors(self, obj):
        return " ".join([author.name for author in obj.authors.all()])

    def prepare_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Post.objects.all()
