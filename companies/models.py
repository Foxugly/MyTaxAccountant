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
from utils.models import Country
from years.models import Year
from categories.models import TypeCategory
from django.conf import settings
from django.utils.text import slugify
import os
import uuid


class ModelTrimester(models.Model):
    name = models.CharField(_("Name of the model trimester"), max_length=128)
    categories = models.ManyToManyField(TypeCategory, verbose_name=_('Types of category'), blank=True)

    def __str__(self):
        return '[%d] %s' % (self.pk, self.name)


class ModelTrimesterForm(ModelForm):
    class Meta:
        model = ModelTrimester
        fields = '__all__'


class Company(models.Model):
    name = models.CharField(_("Name of the company"), max_length=128)
    slug = models.SlugField(unique=True)
    description = models.TextField(_("Description of the company"), blank=True, null=True)
    vat_number = models.CharField(_("TVA number"), unique=True, max_length=10, blank=True, null=True)
    address_1 = models.CharField(_("address"), max_length=128, blank=True, null=True)
    address_2 = models.CharField(_("address cont'd"), max_length=128, blank=True, null=True)
    zip_code = models.CharField(_("zip code"), max_length=5, blank=True, null=True)
    city = models.CharField(_("city"), max_length=128, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, on_delete=models.CASCADE)
    random = models.CharField(max_length=16, blank=True, null=True)
    sales_revenue = models.IntegerField(_("Sales revenue"),
                                        choices=(
                                            (1, _("Lower than 50.000 euros")),
                                            (2, _("Between 50.000 euros and 250.000 euros")),
                                            (3, _("Between 250.000 euros and 700.000 euros")),
                                            (4, _("Between 700.000 euros and 4.500.000 euros")),
                                            (5, _("More than 4.500.000 euros"))
                                        ),
                                        default=1)
    number_employees = models.IntegerField(_("Number of employees"),
                                           choices=(
                                               (1, _("1")),
                                               (2, _("Between 1 and 10")),
                                               (3, _("Between 10 and 50")),
                                               (4, _("More than 50"))
                                           ),
                                           default=1)
    creation_date = models.DateField(_("Creation date"), blank=True, null=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    years = models.ManyToManyField(Year, blank=True)
    active = models.BooleanField(_('active'), default=False)
    favorite = models.BooleanField(_('favorite'), default=False)
    model_trimester = models.ForeignKey(ModelTrimester, null=True, blank=True, on_delete=models.CASCADE)

    def as_json(self):
        return dict(id=self.id, name=self.name)

    def get_name(self):
        return self.name

    def add_year(self, year):
        self.years.add(year)
    
    def get_years(self):
        return self.years.all().order_by('fiscal_year__priority')

    def get_active_years(self):
        return self.years.filter(active=True).order_by('fiscal_year__priority')
        
    def __str__(self):
        return '%s' % (self.get_name())

    def get_absolute_path(self):
        return os.path.join(settings.MEDIA_ROOT, settings.STOCK_DIR, self.slug + '_' + self.random)

    def get_relative_path(self):
        if self.get_absolute_path():
            return os.path.join(settings.MEDIA_URL, settings.STOCK_DIR, self.slug + '_' + self.random)

    def create_directory(self):
        if not os.path.isdir(self.get_absolute_path()):
            os.mkdir(self.get_absolute_path(), 0o771)

    def save(self, *args, **kwargs):
        if not self.random:
            self.random = str(uuid.uuid4().hex.upper()[0:16])
        create = True
        if not self.slug:
            self.slug = slugify(self.name)
            create = False
        super(Company, self).save(*args, **kwargs)
        if create:
            self.create_directory()

    def delete(self, **kwargs):
        for y in self.years.all():
            y.delete()
        os.rmdir(self.get_absolute_path())
        super(Company, self).delete()

    def treeview_favorite(self):
        sum_json = []
        sum_n = 0
        for y in self.years.filter(favorite=True):
            (n, json) = y.treeview()
            if n:
                sum_n += n
                sum_json.append(json)
        out = dict(text=str(self.name), href=str('#%s' % self.name), tags=["%d" % sum_n])
        if sum_n:
            out['nodes'] = sum_json
        return sum_n, out

    def get_favorite_year(self):
        y = self.years.filter(favorite=True)[0]
        if not y:
            y = self.years.filter(active=True).order_by('fiscal_year__priority')[0]
        return y


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'vat_number', 'creation_date', 'sales_revenue', 'number_employees',
                  'address_1', 'address_2', 'zip_code', 'city', 'country']
        help_texts = {
            'vat_number': _("10 digits."),
        }

    def __init__(self, *args, **kw):
        super(CompanyForm, self).__init__(*args, **kw)
        self.fields['country'].widget.attrs['class'] = 'select2100-nosearch'
        self.fields['sales_revenue'].widget.attrs['class'] = 'select2100-nosearch'
        self.fields['number_employees'].widget.attrs['class'] = 'select2100-nosearch'
        self.fields['creation_date'].widget.attrs['class'] = 'datepicker'
        self.fields['description'].widget.attrs['rows'] = 2

    def save(self, *args, **kwargs):
        instance = super(CompanyForm, self).save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.name)
        instance.save()
        return instance


class CompanyCreateForm(ModelForm):

    class Meta:
        model = Company
        fields = ['name', 'description', 'vat_number', 'creation_date', 'sales_revenue', 'number_employees',
                  'address_1', 'address_2', 'zip_code', 'city', 'country', 'model_trimester']
        help_texts = {
            'vat_number': _("10 digits."),
        }

    def __init__(self, *args, **kw):
        super(CompanyCreateForm, self).__init__(*args, **kw)
        self.fields['country'].widget.attrs['class'] = 'select2100-nosearch'
        self.fields['sales_revenue'].widget.attrs['class'] = 'select2100-nosearch'
        self.fields['number_employees'].widget.attrs['class'] = 'select2100-nosearch'
        self.fields['creation_date'].widget.attrs['class'] = 'datepicker'
        self.fields['description'].widget.attrs['rows'] = 2
        self.fields['model_trimester'].widget.attrs['class'] = 'select2100-nosearch'

    def save(self, *args, **kwargs):
        instance = super(CompanyCreateForm, self).save(commit=False)
        if not instance.slug:
            instance.slug = slugify(instance.name)
        instance.save()
        return instance
