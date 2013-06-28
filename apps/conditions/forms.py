# -*- coding: UTF-8 -*-
from django import forms

from conditions.models import Condition


class ConditionForm(forms.ModelForm):

    class Meta:
        model = Condition
        exclude = ("name", "author", )

    def __init__(self, user, name, *args, **kwargs):
        self.user = user
        self.name = name
        super(ConditionForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        condition = super(ConditionForm, self).save(commit=False)
        condition.author = self .user
        condition.name = self.name
        condition.save()
        return condition
