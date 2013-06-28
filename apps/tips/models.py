# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tip(models.Model):
    """
    """
    name = models.ForeignKey("taxon.Name")
    text = models.TextField()

    author = models.ForeignKey("auth.User")

    source_description = models.CharField(max_length=255, blank=True, null=True)
    source_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ("-created_at", )
        verbose_name = _("Growing Tip")
        verbose_name_plural = _("Growing Tips")

    def __unicode__(self):
        return "%s by %s" % (self.text, self.author)
