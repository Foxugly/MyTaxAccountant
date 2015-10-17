# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.utils.translation import ugettext_lazy  as _
from django.db import models, connection
from django import forms
from django.contrib.auth.models import User
from settings import UPLOAD_DIR
from re import sub
from os.path import getsize
from PIL import Image

class Page(models.Model):
    num = models.IntegerField()
    filename = models.CharField(max_length=100, default='blank')
    width = models.IntegerField()
    height = models.IntegerField()
    
    def get_size(self):
        s = getsize(self.filename)
        return s

    def __str__(self):
        return '%s - %s' % (self.filename, self.num)

class Document(models.Model):
    name = models.TextField()
    owner = models.ForeignKey(User)
    refer_category = models.ForeignKey('categories.Category', related_name="back_category", null=True)
    size = models.IntegerField(default=0)
    pages = models.ManyToManyField(Page, blank=True)
    date = models.DateTimeField(auto_now=True, null=False)
    description = models.TextField()
    complete = models.BooleanField(default=False)

    def get_npages(self):
        return len(self.pages.all())

    def set_npages(self, num):
        self.size = num
        self.save()

    def add_page(self, num, fname, w, h):
        p = Page(num=num, filename=fname, width=w, height=h)
        p.save()
        self.size += p.get_size()
        self.pages.add(p)

    def all_pages(self):
        return self.pages.all().order_by('id')

    def get_size(self):
        return self.size

    def __str__(self):
        return self.name

    def as_json(self):
        return dict(id=self.id, name=self.name, date=self.date.strftime('%d/%m/%Y'), description= self.description, complete=self.complete)