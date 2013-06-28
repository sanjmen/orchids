# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from conditions.forms import ConditionForm
from taxon.models import Name


def add_condition(request, name_id):

    name = get_object_or_404(Name, pk=name_id)

    if request.method == "POST":
        form = ConditionForm(data=request.POST, user=request.user, name=name)
        if form.is_valid():
            condition = form.save()
        return HttpResponseRedirect(condition.name.get_absolute_url())
    else:
        if not request.is_ajax():
            raise Http404

        form = ConditionForm(user=request.user, name=name)

    return render_to_response("conditions/add.html",
        {"form": form, "name": name}, context_instance=RequestContext(request))
