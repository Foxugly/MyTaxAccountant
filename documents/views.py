# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.http import HttpResponse
from documents.models import Document, DocumentAdminForm, DocumentForm
from categories.models import Category
import json
import os


def document_view(request, document_id):
    if request.is_ajax():
        d = Document.objects.get(id=document_id)
        result = {'name': d.name, 'img': ''}
        for p in d.pages.all().order_by('num'):
            result['img'] += '<img style="max-width:100%;" src="' + str(p.get_relative_path()) + '" />'
        return HttpResponse(json.dumps(result))


def update_ajax(request, document_id):
    if request.is_ajax():
        doc = Document.objects.get(id=document_id)
        if request.user.is_superuser:
            form = DocumentAdminForm(request.GET, instance=doc)
        else:
            form = DocumentForm(request.GET, instance=doc)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps('OK'))
        else:
            return HttpResponse(json.dumps('ERROR'))


def ajax_move(request, n):
    if request.is_ajax():
        results = {}
        doc = Document.objects.get(pk=int(n))
        cat = doc.refer_category
        if cat.count_docs() > 0:
            results['doc_id'] = int(n)
            tri = cat.refer_trimester
            year = tri.refer_year
            company = year.refer_company
            results['category'] = cat.as_json()
            results['trimester'] = tri.as_json()
            results['year'] = year.as_json()
            results['company'] = company.as_json()
            results['companies'] = [c.as_json() for c in request.user.userprofile.companies.all()]
            results['valid'] = True
        else:
            results['valid'] = False
        return HttpResponse(json.dumps(results))


def ajax_merge(request, n):
    if request.is_ajax():
        results = {}
        doc = Document.objects.get(pk=int(n))
        cat = doc.refer_category
        if cat.count_docs() > 0:
            # TODO AJOUTER
            results['valid'] = True
        else:
            results['valid'] = False
        return HttpResponse(json.dumps(results))


def ajax_split(request, n):
    if request.is_ajax():
        results = {}
        doc = Document.objects.get(pk=int(n))
        cat = doc.refer_category
        if cat.count_docs() > 0:
            # TODO AJOUTER
            results['valid'] = True
        else:
            results['valid'] = False
        return HttpResponse(json.dumps(results))


def ajax_move_doc(request, doc_id, cat_id):
    if request.is_ajax():
        results = {}
        doc = Document.objects.get(pk=int(doc_id))
        old_cat = doc.refer_category
        new_cat = Category.objects.get(pk=int(cat_id))
        for p in doc.pages.all():
            cmd = "mv " + p.get_absolute_path() + " " + new_cat.get_absolute_path() + "/"
            os.system(cmd)
        doc.refer_category = new_cat
        doc.save()
        old_cat.documents.remove(doc)
        new_cat.documents.add(doc)
        results['valid'] = True
        return HttpResponse(json.dumps(results))


def ajax_delete(request, doc_id):
    if request.is_ajax():
        results = {}
        doc = Document.objects.get(pk=int(doc_id))
        cat = doc.refer_category
        cat.documents.remove(doc)
        doc.delete()
        results['valid'] = True
        return HttpResponse(json.dumps(results))
