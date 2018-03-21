# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.http import HttpResponse
from django.shortcuts import render
from documents.models import Document, DocumentAdminForm, DocumentForm
from categories.models import Category
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import json
import os
from subprocess import Popen
from time import sleep
from django.core.exceptions import PermissionDenied


def view(request, doc_id):
    if request.user.is_authenticated:
        d = Document.objects.get(id=doc_id)
        if d.refer_category.refer_trimester.refer_year.refer_company in request.user.userprofile.companies.all().order_by('name'):
            img = ''
            for p in d.pages.all().order_by('num'):
                img += r"<img style=""max-width:100%%"" src=""%s"" />" % p.get_relative_path()
            c = dict(img=img)
            return render(request, 'doc.tpl', c)
        else:
            raise PermissionDenied
    else:
        raise PermissionDenied


def document_view(request, document_id):
    result = {}
    if request.is_ajax():
        d = Document.objects.get(id=document_id)
        result['name'] = d.name
        result['img'] = ''
        i = 1
        for p in d.pages.all().order_by('num'):
            result['img'] += r"<img style=""max-width:100%%"" src=""%s"" />" % p.get_relative_path()
            result['img'] += r"<div class=""text-center"">%s %d</div>" % (_('Page'), i)
            i += 1
    return HttpResponse(json.dumps(result))


def update_ajax(request, document_id):
    if settings.DEBUG:
        print('update_ajax')
    results = {}
    if request.is_ajax():
        doc = Document.objects.get(id=document_id)
        if request.user.is_superuser:
            form = DocumentAdminForm(request.GET, instance=doc)
        else:
            form = DocumentForm(request.GET, instance=doc)
        results['n'] = doc.refer_category.count_docs()
        if form.is_valid():
            form.save()
            results['return'] = True
        else:
            results['return'] = False
            results['errors'] = str(form.errors)
    return HttpResponse(json.dumps(results))


def ajax_move(request, n):
    if settings.DEBUG:
        print('ajax_move')
    results = {}
    if request.is_ajax():
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
            results['companies'] = [c.as_json() for c in request.user.userprofile.companies.all().order_by('name')]
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
    results = {}
    if request.is_ajax():
        doc = Document.objects.get(pk=int(n))
        if doc.get_npages() > 1:
            results['doc_id'] = doc.id
            results['name'] = doc.name
            results['valid'] = True
            results['nname'] = "new doc"
            results['img'] = doc.pages.all()[0].as_img
            results['size'] = doc.get_npages()
        else:
            results['valid'] = False
    return HttpResponse(json.dumps(results))


def move_document(doc_id, cat_id):
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
    return True


def ajax_move_doc(request, doc_id, cat_id):
    results = {}
    if request.is_ajax():
        results['valid'] = move_document(doc_id, cat_id)
    return HttpResponse(json.dumps(results))


def delete_document(doc_id):
    if settings.DEBUG:
        print('delete_document')
    try:
        doc = Document.objects.get(pk=doc_id)
        print(doc)
        doc.refer_category.documents.remove(doc)
        doc.delete()
        return True
    except:
        print("ERROR delete_document id %d" % doc_id)
        return False


def ajax_delete(request, doc_id):
    if settings.DEBUG:
        print('ajax_delete')
    results = {}
    if request.is_ajax():
        results['valid'] = delete_document(doc_id)
    return HttpResponse(json.dumps(results))


def ajax_img(request, doc_id, num):
    if settings.DEBUG:
        print('ajax_img')
    results = {}
    if request.is_ajax():
        doc = Document.objects.get(pk=int(doc_id))
        results['img'] = doc.pages.all()[int(num) - 1].as_img
        results['valid'] = True
    return HttpResponse(json.dumps(results))


def split_doc(request):
    if settings.DEBUG:
        print('split_doc')
    results = {}
    if request.is_ajax():
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
                p.refer_document = new_doc
                p.save()
                doc.size -= p.get_size()
                doc.pages.remove(p)
            i += 1
        doc.refer_category.documents.add(new_doc)
        doc.save()
        new_doc.save()
        results['valid'] = True
    return HttpResponse(json.dumps(results))


def merge_doc(request):
    if settings.DEBUG:
        print('merge_doc')
    results = {}
    if request.is_ajax():
        doc = Document.objects.get(pk=int(request.GET['modal_merge_doc_id']))
        l = request.GET['doc_ids'].split(',')
        for add_doc in l:
            old_doc = Document.objects.get(pk=int(add_doc))
            for p in old_doc.all_pages():
                doc.pages.add(p)
                p.refer_document = doc
                p.save()
                old_doc.pages.remove(p)
                old_doc.save()
                doc.size += p.get_size()
            old_doc.delete()
        doc.save()
        results['valid'] = True
    return HttpResponse(json.dumps(results))


def ajax_download(request, n):
    if settings.DEBUG:
        print('ajax_download')
    results = {}
    if request.is_ajax():
        doc = Document.objects.get(pk=int(n))
        name = doc.name.replace(' ', '_')
        if ".pdf" != doc.name[-4:]:
            name += ".pdf"
        output_abs = settings.TMP_ROOT + name
        output_rel = settings.TMP_URL + name
        cmd = "convert "
        for p in doc.all_pages():
            cmd += p.get_absolute_path() + " "
        cmd += output_abs
        if os.path.exists(output_abs):
            os.system("rm " + output_abs)
        p1 = Popen(cmd, shell=True)
        p1.wait()
        sleep(1)
        results['url'] = output_rel
        results['valid'] = True
    return HttpResponse(json.dumps(results))


def ajax_multiple_move(request, cat_id):
    if settings.DEBUG:
        print("ajax_multiple_move")
    results = {}
    if request.is_ajax():

        for key, val in dict(request.GET).items():
            move_document(val[0], cat_id)
        results['valid'] = True
    return HttpResponse(json.dumps(results))


def ajax_multiple_delete(request):
    if settings.DEBUG:
        print("ajax_multiple_delete")
    results = {}
    if request.is_ajax():
        for key, val in dict(request.GET).items():
            delete_document(val[0])
        results['valid'] = True
    return HttpResponse(json.dumps(results))


def ajax_multiple_download(request):
    if settings.DEBUG:
        print('ajax_multiple_download')
    results = {}
    if request.is_ajax():

        for key, val in dict(request.GET).items():
            print('%s : %s' % (key, val))
        #TODO finish multiple download
        results['valid'] = True
    return HttpResponse(json.dumps(results))
