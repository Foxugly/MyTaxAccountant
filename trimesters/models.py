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
from django.forms import ModelForm
from categories.models import Category, TypeCategory
from django.utils.translation import ugettext_lazy as _
from utils.models import TemplateTrimester
import os
import uuid


class Trimester(models.Model):
    template = models.ForeignKey(TemplateTrimester, null=True, blank=True, on_delete=models.CASCADE)
    start_date = models.DateField(_('start date'), null=True)
    end_date = models.DateField(_('end_date'), null=True, blank=True)
    active = models.BooleanField(_('active'), default=False)
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), blank=True)
    refer_year = models.ForeignKey('years.Year', verbose_name=_('year'), related_name="back_year", null=True,
                                   on_delete=models.CASCADE)
    favorite = models.BooleanField(_('favorite'), default=False)
    random = models.CharField(max_length=16, blank=True, null=True)

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

    def get_name_short(self):
        t = _('trimester')
        return '%s %s' % (t, str(self.template.number))

    def get_name(self):
        t = _('trimester')
        return u'%s %s (%s)' % (t, str(self.template.number), self.start_date)

    def __str__(self):
        return ' [%d] %s - %s' % (
            self.id, self.refer_year.refer_company.slug, str(self.template))

    def as_json(self):
        return dict(id=self.id, name=self.get_name())

    def add_categories(self):
        for c in self.refer_year.refer_company.model_trimester.categories.all().order_by('priority'):
            new_cat, created = Category.objects.get_or_create(cat=c, refer_trimester=self, active=True)
            if created:
                self.categories.add(new_cat)

    def get_categories(self):
        return self.categories.all().order_by('cat__priority')

    def get_absolute_path(self):
        return os.path.join(self.refer_year.get_absolute_path(), "%s_%s" % (str(self.template.number), self.random))

    def get_relative_path(self):
        return os.path.join(self.refer_year.get_relative_path(), "%s_%s" % (str(self.template.number), self.random))

    def save(self, *args, **kwargs):
        if not self.random:
            self.random = str(uuid.uuid4().hex.upper()[0:16])
        super(Trimester, self).save(*args, **kwargs)
        if not os.path.isdir(self.get_absolute_path()):
            os.mkdir(self.get_absolute_path(), 0o771)

    def delete(self, **kwargs):
        for c in self.categories.all():
            c.delete()
        os.rmdir(self.get_absolute_path())
        super(Trimester, self).delete()

    def treeview(self):
        sum_json = []
        sum_n = 0
        for c in self.get_categories():
            (n, json) = c.treeview()
            if n:
                sum_n += n
                sum_json.append(json)
        return sum_n, dict(text=str(self.get_name_short()), href=str('#%d' % self.id), tags=["%d" % sum_n],
                           nodes=sum_json)

    def get_favorite_category(self):
        c = self.categories.all().order_by('cat__priority')[0]
        return c


class TrimesterForm(ModelForm):
    class Meta:
        model = Trimester
        exclude = ['refer_year', ]


class TemplateTrimesterForm(ModelForm):
    class Meta:
        model = TemplateTrimester
        fields = '__all__'
