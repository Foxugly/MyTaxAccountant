# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.ersion 3 of the License, or (at
# your option) any later version.


from django.db import models
from categories.models import Category, TypeCategory
from django.utils.translation import ugettext_lazy as _
import os


class Trimester(models.Model):
    number = models.IntegerField(_('trimester number'), null=True)
    start_date = models.DateField(_('start date'), null=True)
    end_date = models.DateField(_('end_date'), null=True, blank=True)
    active = models.BooleanField(_('active'), default=False)
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), blank=True)
    refer_year = models.ForeignKey('years.Year', verbose_name=_('year'), related_name="back_year", null=True)
    favorite = models.BooleanField(_('favorite'), default=False)

    def get_docs(self):
        out = []
        for category in self.categories.all().order_by('cat__priority'):
            out += category.documents.all()
        return out

    def count_docs(self):
        out = 0
        for category in self.categories.all():
            out += len(category.documents.all())
        return out

    def get_year(self):
        return self.refer_year

    def get_name(self):
        t = _('trimester')
        return u'%s %s (%s)' % (t, str(self.number), self.start_date)

    def __str__(self):
        return u' %s - %s - %s' % (
            str(self.refer_year.refer_company.get_name()), str(self.refer_year.get_name()), self.get_name())

    def as_json(self):
        return dict(id=self.id, name=self.get_name())

    def add_categories(self):
        for c in TypeCategory.objects.filter(active=True).order_by('priority'):
            new_cat = Category(cat=c, refer_trimester=self)
            new_cat.save()
            self.categories.add(new_cat)

    def get_relative_path(self):
        return os.path.join(self.refer_year.get_relative_path(), str(self.number))

    def get_absolute_path(self):
        return os.path.join(self.refer_year.get_absolute_path(), str(self.number))

    def save(self, *args, **kwargs):
        super(Trimester, self).save(*args, **kwargs)
        if not os.path.isdir(self.get_absolute_path()):
            os.mkdir(self.get_absolute_path(), 0711)

    def delete(self, **kwargs):
        for c in self.categories.all():
            c.delete()
        os.rmdir(self.get_absolute_path())
        super(Trimester, self).delete()
