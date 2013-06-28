# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from conditions.managers import NaturalConditionManager, GrowingConditionManager

class ConditionType(models.Model):
    """
    """

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=15, primary_key=True)

    class Meta:
        ordering = ("code", "name")
        verbose_name = _("Condition Type")
        verbose_name_plural = _("Condition Types")

    def __unicode__(self):
        return self.name


class Condition(models.Model):
    """
    """
    condition_type = models.ForeignKey("conditions.ConditionType")
    name = models.ForeignKey("taxon.Name")
    text = models.TextField()

    natural = models.BooleanField(default=True, help_text='Is natural condition and not grower environment')

    author = models.ForeignKey("auth.User")

    source_description = models.CharField(max_length=255, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ("-created_at", )
        verbose_name = _("Condition")
        verbose_name_plural = _("Conditions")

    def __unicode__(self):
        return "%s by %s" % (self.condition_type, self.author)


class NaturalCondition(Condition):
    """
    """

    objects = NaturalConditionManager()

    class Meta:
        proxy = True
        verbose_name = _("Natural Condition")
        verbose_name_plural = _("Natural Conditions")


class GrowingCondition(Condition):
    """
    """

    objects = GrowingConditionManager()

    class Meta:
        proxy = True
        verbose_name = _("Growing Condition")
        verbose_name_plural = _("Growing Conditions")


