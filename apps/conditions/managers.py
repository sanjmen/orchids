# -*- coding: utf-8 -*-
from django.db import models


class NaturalConditionManager(models.Manager):
    def get_query_set(self):
        return super(NaturalConditionManager, self).get_query_set().filter(natural=True)


class GrowingConditionManager(models.Manager):
    def get_query_set(self):
        return super(GrowingConditionManager, self).get_query_set().filter(natural=False)
