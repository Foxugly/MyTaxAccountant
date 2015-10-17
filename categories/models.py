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
from documents.models import Document
from django.conf import settings


class TypeCategory(models.Model):
    name = models.CharField(_("Type of documents"), max_length=128)
    priority = models.IntegerField(unique=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    cat = models.ForeignKey(TypeCategory)
    documents = models.ManyToManyField(Document, blank=True)
    refer_trimester = models.ForeignKey('trimesters.Trimester', related_name="back_trimester", null=True)
    active = models.BooleanField(default=True)

    def get_name(self):
        return u'%s' % (self.cat.name)

    def __str__(self):
        return u'%s - %s' % (self.refer_trimester, self.get_name())

    def add_doc(self, document):
        self.documents.add(document)

    def get_docs(self):
        return sorted(self.documents.all(), key=lambda x: x.date, reverse=True)

    def count_docs(self):
        return len(self.documents.all())

    def get_path(self):
        path = 'media/'+ settings.STOCK_DIR + '/' + str(self.refer_trimester.refer_year.refer_company.slug) + '/' + str(self.refer_trimester.refer_year.fiscal_year) + '/' + str(self.refer_trimester.number) + '/' + self.cat.name + '/'
        print path
        return path

    def as_json(self):
        return dict(id=self.id, name=self.cat.name, n=str(self.count_docs()), )  