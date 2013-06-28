# -*- coding: utf-8 -*-
from django.forms import ChoiceField
from django.utils.translation import ugettext_lazy as _
from django.db.models import get_model

from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet


SEARCH_MODEL_CHOICES = (
    ("species", _("Species")),
    ("genus", _("Genus")),
    ("posts", _("Blog Posts")),
    ("growers", _("Growers")),
    ("tips", _("Growing Tips")),
    ("conditions", ("Natural Conditions")),
    ("onsale", _("Orchids on sale")),
)

CHOICE_TO_MODEL_MAP = {
    "species": get_model("taxon", "species"),
    "genus": get_model("taxon", "genus"),
    "posts": get_model("planet", "post"),
    "growers": get_model("growers", "grower"),
    "tips": get_model("conditions", "growingcondition"),
    "conditions": get_model("conditions", "naturalcondition"),
    "onsale": get_model("growers", "orchidproduct")
}


class OrcheederInlineSearchForm(ModelSearchForm):
    """
    """

    def __init__(self, *args, **kwargs):
        super(ModelSearchForm, self).__init__(*args, **kwargs)
        self.fields['models'] = ChoiceField(
            choices=SEARCH_MODEL_CHOICES, required=False, label=_('in'))

    def get_models(self):
        try:
            app_model = self.cleaned_data.get("models")
        except AttributeError:
            return []

        if app_model:
            model = CHOICE_TO_MODEL_MAP[app_model]
            return [model]

        return []

    def search(self):
        try:
            q = self.cleaned_data.get("q")
        except AttributeError:
            q = None

        if not q:
            return SearchQuerySet().models(*self.get_models()).all().load_all()

        return super(OrcheederInlineSearchForm, self).search()
