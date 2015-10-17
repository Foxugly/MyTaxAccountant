# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from django.utils.translation import ugettext_lazy  as _
from django.db import models
from django.forms import ModelForm


CAT_DOCUMENTS = (
    ('S', _('Sales')),
    ('I', _('Invoice')),
    ('B', _('Bank')),
    ('O', _('Others')),
)


class Country(models.Model):
    name = models.TextField(_("Country"))
    
    def __str__(self):
        return self.name

class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields = ['name']


class FiscalYear(models.Model):
    name = models.TextField(_("Fiscal year"), max_length=6)

    def __str__(self):
        return self.name

class FiscalYearForm(ModelForm):
    class Meta:
        model = FiscalYear
        fields = ['name']