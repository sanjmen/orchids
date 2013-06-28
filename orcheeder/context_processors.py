# -*- coding: utf-8 -*-
from orcheeder.forms import OrcheederInlineSearchForm

def search_form(request):
    form = OrcheederInlineSearchForm()
    return {"search_form": form}
