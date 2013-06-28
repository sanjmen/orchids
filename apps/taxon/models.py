# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField
from tagging.fields import TagField

from taxon.managers import SpecieManager, GenusManager


class Source(models.Model):
    """
    """
    name = models.CharField(max_length=20)
    url = models.URLField(blank=True, null=True)
    citation = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

    def __unicode__(self):
        return self.name


class SourceKey(models.Model):
    """
    """
    source = models.ForeignKey(Source)
    name = models.ForeignKey("taxon.Name")
    key = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("SourceKey")
        verbose_name_plural = _("SourceKeys")

    def __unicode__(self):
        return u"%s: %s" % (self.source ,self.key)


class Authorship(models.Model):
    """
    """
    author = models.CharField(max_length=200, unique=True)

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __unicode__(self):
        return u"%s" % (self.author, )


class Reference(models.Model):
    """
    """
    name = models.ManyToManyField("taxon.Name")
    full_citation = models.CharField(max_length=300)
    publication = models.CharField(max_length=200, null=True, blank=True)
    collation = models.CharField(max_length=200, null=True, blank=True)
    page = models.CharField(max_length=10, null=True, blank=True)
    date = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = _("Reference")
        verbose_name_plural = _("References")

    def get_citation(self):
        str_list = []
        if self.publication:
            str_list.append(self.publication)
        if self.collation:
            str_list.append(self.collation)
        if self.page:
            str_list.append(self.page)
        if self.date:
            str_list.append(self.date)

        return u"; ".join(str_list)

    def __unicode__(self):
       return self.full_citation

    def save(self, *args, **kwargs):
        if not self.full_citation:
            self.full_citation = self.get_citation()
        super(Reference, self).save(*args, **kwargs)


RANK_CHOICES = (
    ('cl.', _("class")),
    ('ord.', _("order")),
    ('fam.', _("family")),
    ('tr.', _("tribe")),
    ('gen.', _("genus")),
    ('sect.', _("section")),
    ('ser.', _("series")),
    ('sp.', _("species")),
    ('var.', _("variety")),
    ('f.', _("form")),
    ('subg.', _("subgenus")),
    ('subsp.', _("subspecies")),
    ('nothosp.', _("nothospecies")),
    ('subvar.', _("subvariety")),
    ('subf.', _("subform")),
    )

STATUS_CHOICES = (
    ('a', _("Accepted")),
    ('s', _("Synonym")),
)

class Name(models.Model):
    """
    A model to store plant Names and related information.
        examples:
        "Aerides odorata var. ballantiniana (Rchb. f.) H.J. Veitch"
        "Aerides Lour."
        "Aerides odorata Lour."
        "Aerides odorata var. annamensis Costantin"
        "Aerides odorata fo. immaculata M. Wolff & O. Gruss"
        "Aerides odorata subvar. immaculata Guillaumin"
        "× Cephalopactis hybrida (Jáv.) Domin"
    """

    scientific = models.CharField(max_length=200, null=True, blank=True, db_index=True)
    common_name = models.CharField(max_length=200, null=True, blank=True)
    etymology = models.TextField(max_length=500, null=True, blank=True)

    parent = models.ForeignKey("taxon.Name", null=True, blank=True)

    genus_hybrid_marker = models.CharField(max_length=5, null=True, blank=True)
    genus_name = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    species_hybrid_marker = models.CharField(max_length=5, null=True, blank=True)
    species_epithet = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    infraspecific_rank = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    infraspecific_epithet = models.CharField(max_length=100, null=True, blank=True, db_index=True)

    author = models.ForeignKey(Authorship, null=True, blank=True)

    rank = models.CharField(max_length=10, null=True, blank=True, choices=RANK_CHOICES, db_index=True)

    countries = models.ManyToManyField("countries.Country", blank=True, null=True, related_name="country_names")

    description = models.TextField(max_length=1000, null=True, blank=True)

    synonyms = models.ManyToManyField("self", symmetrical=False, related_name="reverse_synonyms",\
            help_text="choice synonyms from list, add new one or leave blank", null=True, blank=True)

    name_status = models.CharField(max_length=3, null=True, blank=True, choices=STATUS_CHOICES, db_index=True)

    tags = TagField()

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ("scientific", "genus_name", "species_epithet", "infraspecific_epithet")
        verbose_name = _("Name")
        verbose_name_plural = _("Names")

    def get_partial(self):
        """ without authorship """
        if self.scientific:
            return self.scientific
        str_list = []

        if self.genus_hybrid_marker:
            str_list.append(self.genus_hybrid_marker)
        str_list.append(self.genus_name)
        if self.species_hybrid_marker:
            str_list.append(self.species_hybrid_marker)
        if self.species_epithet:
            str_list.append(self.species_epithet)
        if self.infraspecific_rank:
            str_list.append(self.infraspecific_rank)
        if self.infraspecific_epithet:
            str_list.append(self.infraspecific_epithet)

        return u" ".join(str_list)

    def get_complete(self):
        """ scientific name + authorship """
        return "%s %s" % (self.get_partial(), self.author)

    def get_rank(self):
        """
        """
        if self.infraspecific_rank:
            self.rank = self.infraspecific_rank
        elif self.species_epithet:
            self.rank = 'sp.'
        else:
            self.rank = 'gen.'

    def get_parent(self):
        return self.parent

    def get_slug(self):
        return slugify(self.get_partial())

    def get_main_image(self):
        """Return only primary image"""
        return self.imagen_set.get(is_primary=True)

    def get_extra_images(self):
        """Return all extra images except primary image"""
        return self.imagen_set.filter(is_primary=False)

    def get_accepted_name(self):
        if self.name_status == 's':
            return self.reverse_synonyms.all()[0]
        if self.name_status == 'a':
            return self.scientific

    def __unicode__(self):
        return self.get_partial()

    def save(self, *args, **kwargs):
        if not self.scientific:
            self.scientific = self.get_partial()
        if not self.rank:
            self.get_rank()
        super(Name, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        if self.name_status == 's':
            return ('taxon.views.synonym_detail', [], dict(synonym_id=self.id, slug=self.get_slug()))
        if self.rank == 'gen.':
            return ('taxon.views.genus_detail', [], dict(slug=self.get_slug(), genus_id=self.id))
        else:
            return ('taxon.views.species_detail', [], dict(slug=self.get_slug(), species_id=self.id))


    def get_proxy(self):
        if self.rank == "sp.":
            return Species.objects.get(pk=self.pk)
        elif self.rank == "gen.":
            return Genus.objects.get(pk=self.pk)
        else:
            return self


class Genus(Name):
    """
    """

    objects = GenusManager()

    class Meta:
        proxy = True
        verbose_name = _("Genus")
        verbose_name_plural = _("Genus")

    @models.permalink
    def get_absolute_url(self):
        return ('taxon.views.genus_detail', [], dict(slug=self.get_slug(), genus_id=self.id))


class Species(Name):
    """
    """

    objects = SpecieManager()

    class Meta:
        proxy = True
        verbose_name = _("Species")
        verbose_name_plural = _("Species")

    @models.permalink
    def get_absolute_url(self):
        return ('taxon.views.species_detail', [], dict(slug=self.get_slug(), species_id=self.id))


class Imagen(models.Model):
    name = models.ForeignKey(Name)
    member = models.ForeignKey(User)
    image = ImageField(upload_to='images', max_length=200)
    caption = models.TextField(null=True, blank=True)
    is_primary = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = _("Imagen")
        verbose_name_plural = _("Images")
        get_latest_by = "id"

    def __unicode__(self):
        return slugify("%s-%s" % (self.name.scientific, self.created_at))

