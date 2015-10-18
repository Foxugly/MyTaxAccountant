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
from django.utils.translation import ugettext_lazy  as _

class Year(models.Model):
    fiscal_year = models.ForeignKey(FiscalYear)
    active = models.BooleanField(_('active'), default=False)
    trimesters = models.ManyToManyField(Trimester, blank=True)
    refer_company = models.ForeignKey('companies.Company', related_name="back_company", blank=True, null=True)
    favorite = models.BooleanField(_('favorite'), default=False)

    def get_company(self):
        return self.refer_company


    def get_trimesters_count(self):
        return len(self.trimesters.all())


    def get_trimesters(self):
        return self.trimesters.all()

    def add_trimester(self,trimester):
        self.trimesters.add(trimester)

    def __str__(self):
        return u'%s - %s' % (self.fiscal_year, self.refer_company.name)

    def get_name(self):
        return u'%s' % (self.fiscal_year)

    def as_json(self):
        return dict(id=self.id, name=self.get_name())

    def get_relative_path(self):
        return os.path.join(self.refer_company.get_relative_path(), self.fiscal_year.name)

    def get_absolute_path(self):
        return os.path.join(self.refer_company.get_absolute_path(), self.fiscal_year.name)

    def save(self, *args, **kwargs):
        super(Year, self).save(*args, **kwargs)
        os.mkdir( self.get_absolute_path(), 0711 );

    def delete(self):
        for t in self.trimesters.all():
            t.delete()
        os.rmdir(self.get_absolute_path())
        super(Year, self).delete()