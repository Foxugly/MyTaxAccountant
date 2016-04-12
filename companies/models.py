# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from django.utils.translation import ugettext_lazy as _
from django.db import models
from django import forms
from django.forms import ModelForm
from utils.models import Country
from years.models import Year
from django.conf import settings
import os


class Company(models.Model):
    name = models.TextField(_("Name of the company"))
    slug = models.SlugField(unique=True)
    description = models.TextField(_("Description of the company"), blank=True, null=True)
    vat_number = models.CharField(_("TVA number"), unique=True, max_length=10, null=True)
    address_1 = models.CharField(_("address"), max_length=128, blank=True, null=True)
    address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True, null=True)
    zip_code = models.CharField(_("zip code"), max_length=5, blank=True, null=True)
    city = models.CharField(_("city"), max_length=128, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True)
    years = models.ManyToManyField(Year, blank=True)
    active = models.BooleanField(_('active'), default=False)
    favorite = models.BooleanField(_('favorite'), default=False)

    def as_json(self):
        return dict(id=self.id, name=self.name)

    def get_name(self):
        return self.name

    def add_year(self, year):
        self.years.add(year)

    def __str__(self):
        return '%s' % self.get_name()

    def get_relative_path(self):
        return os.path.join(settings.MEDIA_URL, settings.STOCK_DIR, self.slug)

    def get_absolute_path(self):
        return os.path.join(settings.MEDIA_ROOT, settings.STOCK_DIR, self.slug)

    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs)
        if not os.path.isdir(self.get_absolute_path()):
            os.mkdir(self.get_absolute_path(), 0711)

    def delete(self, **kwargs):
        for y in self.years.all():
            y.delete(kwargs)
        os.rmdir(self.get_absolute_path())
        super(Company, self).delete()


class CompanyForm(ModelForm):
    n = 'companyform'
    name = forms.CharField()

    class Meta:
        model = Company
        fields = ['name', 'description', 'vat_number', 'address_1', 'address_2', 'zip_code', 'city', 'country']

    def __init__(self, *args, **kw):
        super(CompanyForm, self).__init__(*args, **kw)
        self.fields['country'].widget.attrs['class'] = 'select2-nosearch'
        self.fields['description'].widget.attrs['rows'] = 2
