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
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import json
import os


def document_view(request, document_id):
    if request.is_ajax():
        d = Document.objects.get(id=document_id)
        result = {'name': d.name, 'img': ''}
        i = 1
        for p in d.pages.all().order_by('num'):
            result['img'] += '<img style="max-width:100%;" src="' + str(p.get_relative_path()) + '" />'
            result['img'] += '<div class="text-center">%s %d</div>' % (_('Page'), i)
            i += 1
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
        doc = Document.objects.get(pk=int(n))
        if doc.refer_category.count_docs() > 1:
            return HttpResponse(json.dumps([d.as_json() for d in doc.refer_category.documents.exclude(id=doc.id)]))
        else:
            return HttpResponse(json.dumps([]))


def ajax_split(request, n):
    if request.is_ajax():
        results = {}
        doc = Document.objects.get(pk=int(n))
        if doc.get_npages() > 1:
            results['doc_id'] = doc.id
            results['name'] = doc.name
            results['valid'] = True
            results['nname'] = "new doc"
            results['img'] = doc.pages.all()[0].as_img(50)
            results['size'] = doc.get_npages()
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


def ajax_img(request, doc_id, num):
    if request.is_ajax():
        results = {}
        doc = Document.objects.get(pk=int(doc_id))
        results['img'] = doc.pages.all()[int(num) - 1].as_img(50)
        results['valid'] = True
        return HttpResponse(json.dumps(results))


def split_doc(request):
    if request.is_ajax():
        results = {}
        cut = int(request.GET['modal_split_cut'][0])
        doc = Document.objects.get(pk=int(request.GET['modal_split_doc_id']))
        doc.name = request.GET['modal_split_name']
        new_doc = Document(name=request.GET['modal_split_new_name'], owner=request.user,
                           refer_category=doc.refer_category, complete=True)
        pages = doc.pages.all()
        new_doc.save()
        i = 0
        for p in pages:
            if i >= cut:
                new_doc.pages.add(p)
                new_doc.size += p.get_size()
                doc.size -= p.get_size()
                doc.pages.remove(p)
            i += 1
        doc.refer_category.documents.add(new_doc)
        doc.save()
        new_doc.save()
        results['valid'] = True
        return HttpResponse(json.dumps(results))


def merge_doc(request):
    if request.is_ajax():
        results = {}
        doc = Document.objects.get(pk=int(request.GET['modal_merge_doc_id']))
        l = request.GET['doc_ids'].split(',')
        print l
        for add_doc in l:
            print add_doc
            old_doc = Document.objects.get(pk=int(add_doc))
            print old_doc
            for p in old_doc.all_pages():
                print p
                print doc.pages.all()
                doc.pages.add(p)
                print doc.pages.all()
                print old_doc.pages.all()
                old_doc.pages.remove(p)
                print old_doc.pages.all()
                doc.size += p.get_size()
            old_doc.delete()
        doc.save()
        results['valid'] = True
        return HttpResponse(json.dumps(results))


def ajax_download(request, n):
    if request.is_ajax():
        results = {}
        doc = Document.objects.get(pk=int(n))
        name = doc.name.replace(' ', '_')
        if ".pdf" != doc.name[-4:]:
            name += ".pdf"
        output_abs = settings.MEDIA_ROOT + '/tmp/' + name
        output_rel = settings.MEDIA_URL + 'tmp/' + name
        cmd = "convert "
        for p in doc.all_pages():
            cmd += p.get_absolute_path() + " "
        cmd += output_abs
        if os.path.exists(output_abs):
            os.system("rm " + output_abs)
        os.system(cmd)
        results['url'] = output_rel
        results['valid'] = True
        return HttpResponse(json.dumps(results))
