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
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from settings import UPLOAD_DIR
from re import sub
import os
from PIL import Image
from django.utils import timezone

class Page(models.Model):
    num = models.IntegerField(_('page number'))
    filename = models.CharField(_('filename'), max_length=100, default='blank')
    width = models.IntegerField(_('width'))
    height = models.IntegerField(_('height'))
    refer_document = models.ForeignKey('documents.Document', verbose_name=_('document'), related_name="back_document", null=True)

    def get_absolute_path(self):
        return os.path.join(self.refer_document.refer_category.get_absolute_path(),self.filename)

    def get_relative_path(self):
        return os.path.join(self.refer_document.refer_category.get_relative_path(),self.filename)

    def as_img(self):
        return '<img style="max-width:95%;" src="' + str(self.get_relative_path()) + '" />'

    def get_size(self):
        s = os.path.getsize(self.get_absolute_path())
        return s

    def __str__(self):
        return '%s - %s' % (self.filename, self.num)

    def delete(self):
        os.remove(self.get_absolute_path())
        super(Page, self).delete()

class Document(models.Model):
    name = models.TextField(_('filename'))
    owner = models.ForeignKey(User)
    refer_category = models.ForeignKey('categories.Category', verbose_name=_('category'), related_name="back_category", null=True)
    size = models.IntegerField(_('size'), default=0)
    pages = models.ManyToManyField(Page, blank=True)
    date = models.DateTimeField( _('date'), default=timezone.now, null=False)
    description = models.TextField(_('description'))
    complete = models.BooleanField(_('complete'), default=False)

    def get_npages(self):
        return len(self.pages.all())

    def set_npages(self, num):
        self.size = num
        self.save()

    def add_page(self, num, fname, w, h):
        p = Page(num=num, filename=fname, width=w, height=h,refer_document=self)
        p.save()
        self.size += p.get_size()
        self.pages.add(p)

    def all_pages(self):
        return self.pages.all().order_by('id')

    def as_img(self):
        txt = ''
        for p in self.all_pages():
            txt+= p.as_img()
        return txt

    def get_size(self):
        return self.size

    def __str__(self):
        return self.name

    def as_json(self):
        return dict(id=self.id, name=self.name, date=self.date.strftime('%d/%m/%Y'), description= self.description, complete=self.complete)

    def delete(self):
        for p in self.pages.all():
            p.delete()
        super(Document, self).delete()

class DocumentForm(ModelForm):
    name = forms.CharField(label=_('Filename'), max_length=200, widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Document
        fields = ['name', 'date', 'description']


    def as_div(self):
        txt = '<form class="form-horizontal">\n<fieldset>\n<legend>' + str(_('Document')) +'</legend>'
        for f in self:
            txt+= '<div class="form-group">\n'
            txt+= f.label_tag().replace('<label ', '<label class="col-md-4 control-label" ' )+'\n'
            txt+= '<div class="col-md-8">' + str(f) + '</div>\n<span class="help-block"></span>\n'
            txt+= '</div>\n'
        txt+= '<div class="form-group">\n'
        txt+= '<div class="col-md-offset-2 col-md-8">\n'
        txt+= '<a id="btn_save" class="btn btn-block btn-success">' + str(_('Save')) + '</a>\n</div>\n</div>'
        txt += '</fieldset>\n</form>'
        return txt