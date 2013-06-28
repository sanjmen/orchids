# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from sorl.thumbnail import ImageField
from tagging.fields import TagField

from conditions.models import Condition
from countries.models import Country, UsState
from taxon.models import Name


class Grower(models.Model):
    """
    """
    name = models.CharField(max_length=255, db_index=True)
    url = models.URLField()
    #add fb_url, twitter_url, g+_url, etc

    description = models.TextField(max_length=2000, null=True, blank=True)
    home_body = models.TextField(max_length=5000, null=True, blank=True)

    # temporary: we start only with growers from USA.
    # If this app get good revenue then: add world states, cities, ...
    # and address models to extend the generic country app
    country = models.ForeignKey(Country, null=True, blank=True)
    usstate = models.ForeignKey(UsState, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True,
            help_text="example: 734 Ocean View Ave, Encinitas, CA, 92024")
    phone = models.CharField(max_length=20, null=True, blank=True)

    tags = TagField()

    slug = models.SlugField(max_length=100, editable=False)

    logo = ImageField(upload_to='images', max_length=200)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ("name", )
        verbose_name = _("Grower")
        verbose_name_plural = _("Growers")

    def __unicode__(self):
        return u"%s" % self.name

    def get_address(self):
        address = " ".join(self.addres.split(','))
        return u"%s" % address

    @models.permalink
    def get_absolute_url(self):
        return ('growers.views.grower_detail', [], dict(slug=self.slug))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Grower, self).save(*args, **kwargs)


GROWING_SCALE = (
        (1, _("easy growing")),
        (2, _("intermediate growing")),
        (3, _("hard growing")),
        )

SIZES = (
        ("FS", _("Flowering Size")),
        ("BS", _("Blooming Size")),
        ("NB", _("Near Blooming Size")),
        ("MS", _("Medium Size")),
        ("SS", _("Seedling Size")),
        ("CP", _("Compots")),
        ("FK", _("Flask")),
        )


class OrchidProduct(models.Model):
    """
    """
    grower = models.ForeignKey(Grower)
    title = models.CharField(max_length=255)
    origin = models.ForeignKey(Country, null=True, blank=True)

    description = models.TextField(max_length=2000, null=True, blank=True)

    imagen = ImageField(upload_to='images', max_length=200, null=True, blank=True)
    url = models.URLField()

    price = models.FloatField(max_length=20, db_index=True)
    mount = models.CharField(max_length=50, null=True, blank=True)

    size = models.CharField(max_length=2, choices=SIZES, null=True, blank=True)
    growing_scale = models.PositiveSmallIntegerField(max_length=2, choices=GROWING_SCALE, null=True, blank=True)

    publish = models.BooleanField(default=False, help_text="visible on website")

    related_taxon = models.ManyToManyField(Name, null=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ("title", "price", )
        verbose_name = _("OrchidProduct")
        verbose_name_plural = _("OrchidProducts")

    def __unicode__(self):
        return u"%s" % self.title

    def get_conditions(self):
        """
            get the conditions and growing tips recommended by the grower
        """
        conditions = []
        for taxon in self.related_taxon.all():
            c = Condition.objects.filter(name=taxon, source_description=self.grower.name)
            for i in c:
                conditions.append(i)
        return conditions

    def get_slug(self):
        return "{}-{}".format(slugify(self.grower.name), slugify(self.title))

    @models.permalink
    def get_absolute_url(self):
        return ('growers.views.product_detail', [], dict(slug=self.get_slug(), product_id=self.id))

