# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from django.forms import ModelForm
from trimesters.models import Trimester
from utils.models import FiscalYear
import os
from django.utils.translation import ugettext_lazy as _
import uuid
import json


class Year(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE)
    active = models.BooleanField(_('active'), default=False)
    trimesters = models.ManyToManyField(Trimester, blank=True)
    refer_company = models.ForeignKey('companies.Company', verbose_name=_('company'), related_name="back_company",
                                      blank=True, null=True, on_delete=models.CASCADE)
    favorite = models.BooleanField(_('favorite'), default=False)
    random = models.CharField(max_length=16, blank=True, null=True)
    admin = models.BooleanField(_('admin'), default=False)

    def get_company(self):
        return self.refer_company

    def get_trimesters_count(self):
        return len(self.trimesters.all())

    def get_trimesters(self):
        return self.trimesters.all().order_by('template__number')

    def get_active_trimesters(self):
        return self.trimesters.filter(active=True).order_by('template__number')

    def add_trimester(self, trimester):
        self.trimesters.add(trimester)

    def __str__(self):
        return u'%s - %s' % (self.fiscal_year, self.refer_company.name)

    def get_name(self):
        return u'%s' % self.fiscal_year

    def as_json(self):
        return dict(id=self.id, name=self.get_name())

    def get_relative_path(self):
        return os.path.join(self.refer_company.get_relative_path(), self.fiscal_year.get_name() + '_' + self.random)

    def get_absolute_path(self):
        return os.path.join(self.refer_company.get_absolute_path(), self.fiscal_year.get_name() + '_' + self.random)

    def save(self, *args, **kwargs):
        if not self.random:
            self.random = str(uuid.uuid4().hex.upper()[0:16])
        super(Year, self).save(*args, **kwargs)
        if not os.path.isdir(self.get_absolute_path()):
            os.mkdir(self.get_absolute_path(), 0o771)

    def delete(self, **kwargs):
        for t in self.trimesters.all():
            t.delete()
        os.rmdir(self.get_absolute_path())
        super(Year, self).delete(kwargs)

    def treeview(self):
        sum_json = []
        sum_n = 0
        for t in self.get_trimesters():
            (n, json) = t.treeview()
            if n:
                sum_n += n
                sum_json.append(json)
        return sum_n, dict(text=str(self.fiscal_year), href=str('#%s' % self.id), tags=["%d" % sum_n], nodes=sum_json)

    def get_favorite_trimester(self):
        tris = self.trimesters.filter(favorite=True)
        if len(tris) > 0:
            t = tris[0]
        if not t:
            t = self.trimesters.filter(active=True).order_by('template__number')[-1]
        return t


class YearForm(ModelForm):
    class Meta:
        model = Year
        exclude = ['refer_company', ]

