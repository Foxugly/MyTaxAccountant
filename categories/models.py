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
from documents.models import Document
import os
import uuid


class TypeCategory(models.Model):
    name = models.CharField(_("Type of documents"), max_length=128)
    priority = models.IntegerField(_('Priority'), unique=True)
    active = models.BooleanField(_('active'), default=True)
    default = models.BooleanField(_('default'), default=True)

    def __str__(self):
        return '[%d] %s' % (self.priority, self.name)


class Category(models.Model):
    cat = models.ForeignKey(TypeCategory)
    documents = models.ManyToManyField(Document, verbose_name=_('documents'), blank=True)
    refer_trimester = models.ForeignKey('trimesters.Trimester', verbose_name=_('trimester'),
                                        related_name="back_trimester", null=True)
    active = models.BooleanField(_('active'), default=True)
    random = models.CharField(max_length=24, blank=True, null=True)

    def get_name(self):
        return u'%s' % self.cat.name

    def __str__(self):
        return u'[%d] %s - %s' % (self.id, self.refer_trimester, self.get_name())

    def add_doc(self, document):
        self.documents.add(document)

    def get_docs(self):
        return sorted(self.documents.all(), key=lambda x: x.date, reverse=True)

    def count_docs(self):
        return len(self.documents.all())

    def get_doc(self, i):
        return self.documents.get(id=i)

    def as_json(self):
        name = "%sT%s %s" % (self.refer_trimester.refer_year.fiscal_year.name, self.refer_trimester.template.number,
                             self.cat.name)
        return dict(id=self.id, name=name, n=str(self.count_docs()), )

    def get_relative_path(self):
        return os.path.join(self.refer_trimester.get_relative_path(), self.cat.name.replace(" ", "_") + "_" + self.random)

    def get_absolute_path(self):
        return os.path.join(self.refer_trimester.get_absolute_path(), self.cat.name.replace(" ", "_") + "_" + self.random)

    def save(self, *args, **kwargs):
        if not self.random:
            self.random = str(uuid.uuid4().hex.upper()[0:16])
        super(Category, self).save(*args, **kwargs)
        if not os.path.isdir(self.get_absolute_path()):
            os.mkdir(self.get_absolute_path(), 0o711)

    def delete(self, **kwargs):
        for d in self.documents.all():
            d.delete()
        os.rmdir(self.get_absolute_path())
        super(Category, self).delete()
