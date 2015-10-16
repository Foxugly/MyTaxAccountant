# -*- coding: utf-8 -*-

# Copyright 2015, foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from django.utils.translation import ugettext_lazy  as _
from django.db import models
from django.forms import ModelForm
from utils.models import Country
from years.models import Year

class Company(models.Model):
    name = models.TextField(_("Name of the company"))
    slug = models.SlugField(unique=True)
    description = models.TextField(_("Description of the company"), null=True)
    vat_number = models.CharField(_("TVA number"), max_length=10, null=True)
    address_1 = models.CharField(_("address"), max_length=128)
    address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True, null=True)
    zip_code = models.CharField(_("zip code"), max_length=5, blank=True, null=True)
    city = models.CharField(_("city"), max_length=128, blank=True, null=True)
    country = models.ForeignKey(Country)
    years = models.ManyToManyField(Year, blank=True)
    active = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)

    def as_json(self):
        return dict(id=self.id, name=self.name)

    def get_name(self):
        return self.name

    def __str__(self):
        return '%s' % self.get_name()

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'slug', 'description', 'vat_number', 'address_1', 'address_2', 'zip_code', 'city', 'country']
