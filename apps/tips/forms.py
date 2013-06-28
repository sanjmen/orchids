# -*- coding: UTF-8 -*-
from django import forms

from tips.models import Tip


class TipForm(forms.ModelForm):

    class Meta:
        model = Tip
        exclude = ("name", "author", )

    def __init__(self, user, name, *args, **kwargs):
        self.user = user
        self.name = name
        super(TipForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        tip = super(TipForm, self).save(commit=False)
        tip.author = self .user
        tip.name = self.name
        tip.save()
        return tip
