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
from django.forms import ModelForm


class Country(models.Model):
    name = models.TextField(_("Country"))
    
    def __str__(self):
        return self.name


class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields = ['name']


class FiscalYear(models.Model):
    name = models.TextField(_("Fiscal year"), max_length=20)
    init = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name.replace(' ', '_')


class FiscalYearForm(ModelForm):
    class Meta:
        model = FiscalYear
        fields = ['name']


class TemplateTrimester(models.Model):
    number = models.IntegerField(_('trimester number'), null=True)
    year = models.ForeignKey(FiscalYear, null=True)
    favorite = models.BooleanField(_('favorite'), default=False)
    start_date = models.DateField(_('start date'), null=True)

    def __str__(self):
        return '%sT%s (%d)' % (self.year, self.number, self.favorite)


class TemplateTrimesterForm(ModelForm):
    class Meta:
        model = TemplateTrimester
        fields = '__all__'
