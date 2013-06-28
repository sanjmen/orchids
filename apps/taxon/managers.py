# -*- coding: utf-8 -*-
from django.db import models


class GenusManager(models.Manager):
    def get_query_set(self):
        return super(GenusManager, self).get_query_set().filter(rank="gen.")


class SpecieManager(models.Manager):
    def get_query_set(self):
        return super(SpecieManager, self).get_query_set().filter(rank="sp.")
