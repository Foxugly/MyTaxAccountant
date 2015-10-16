# -*- coding: utf-8 -*-

# Copyright 2015, hast. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from django.db import models
from categories.models import Category, TypeCategory
from django.utils.translation import ugettext_lazy  as _


class Trimester(models.Model):
    number = models.IntegerField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, blank=True)
    refer_year = models.ForeignKey('years.Year', related_name="back_year", null=True)
    favorite = models.BooleanField(default=False)

    def get_docs(self):
        # TODO trier par date de réception
        out = []
        for category in self.categories.all() :
            out += category.documents.all()
        return out

    def count_docs(self): 
        out = 0
        for category in self.categories.all() :
            out += len(category.documents.all())
        return out


    def get_year(self):
        return self.refer_year

    def get_name(self):
        t = _('trimester')
        return u'%s %s (%s)' % (t, str(self.number), self.start_date) 

    def __str__(self):
        return u' %s - %s - %s' % (str(self.refer_year.refer_company.get_name()), str(self.refer_year.get_name()), self.get_name())

    def as_json(self):
        return dict(id=self.id, name=str(self))# .get_name())

    def add_categories(self):
        for c in TypeCategory.objects.filter(active=True).order_by('priority'):
            new_cat = Category(cat=c, refer_trimester=self)
            new_cat.save()
            self.categories.add(new_cat)
            self.save()
