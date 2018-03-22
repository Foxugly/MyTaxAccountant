# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from documents.models import Document, DocumentAdminForm, DocumentForm
from categories.models import Category
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import json
import os
from subprocess import Popen
from django.core.exceptions import PermissionDenied
import logging
import shutil

logger = logging.getLogger(__name__)
logger.setLevel(settings.LOGGER)


def view(request, doc_id):
    logger.debug("viewy | doc_id = %d" % doc_id)
    d = get_object_or_404(Document, id=doc_id)
    if d.refer_category.refer_trimester.refer_year.refer_company in request.user.userprofile.companies.all().order_by('name'):
        img = ''
        for p in d.pages.all().order_by('num'):
            img += r"<img style=""max-width:100%%"" src=""%s"" />" % p.get_relative_path()
        c = dict(img=img)
        return render(request, 'doc.tpl', c)
    else:
        raise PermissionDenied


def document_view(request, doc_id):
    logger.debug("document_view | doc_id = %d" % doc_id)
    result = {}
    if request.is_ajax():
        d = get_object_or_404(Document, id=doc_id)
        result['name'] = d.name
        result['img'] = ''
        i = 1
        for p in d.pages.all().order_by('num'):
            result['img'] += r"<img style=""max-width:100%%"" src=""%s"" />" % p.get_relative_path()
            result['img'] += r"<div class=""text-center"">%s %d</div>" % (_('Page'), i)
            i += 1
    return HttpResponse(json.dumps(result))


def update_ajax(request, doc_id):
    logger.debug('update_ajax | doc_id = %d' % doc_id)
    results = {}
    if request.is_ajax():
        doc = get_object_or_404(Document, id=doc_id)
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


def ajax_move(request, doc_id):
    logger.debug('ajax_move | doc_id = %d' % doc_id)
    results = {}
    if request.is_ajax():
        doc = get_object_or_404(Document, pk=doc_id)
        cat = doc.refer_category
        if cat.count_docs() > 0:
            results['doc_id'] = doc_id
            tri = cat.refer_trimester
            year = tri.refer_year
            company = year.refer_company
            results['category'] = cat.as_json()
            results['trimester'] = tri.as_json()
            results['year'] = year.as_json()
            results['company'] = company.as_json()
            results['companies'] = [c.as_json() for c in request.user.userprofile.get_companies()]
            results['valid'] = True
        else:
            results['valid'] = False
    return HttpResponse(json.dumps(results))


def ajax_merge(request, doc_id):
    logger.debug('ajax_merge | doc_id = %d' % doc_id)
    if request.is_ajax():
        doc = get_object_or_404(Document, pk=doc_id)
        if doc.refer_category.count_docs() > 1:
            return HttpResponse(json.dumps([d.as_json() for d in doc.refer_category.documents.exclude(id=doc.id)]))
        else:
            return HttpResponse(json.dumps([]))


def ajax_split(request, doc_id):
    logger.debug('ajax_split | doc_id = %d' % doc_id)
    results = {}
    if request.is_ajax():
        doc = get_object_or_404(Document, pk=doc_id)
        if doc.get_npages() > 1:
            results['doc_id'] = doc.id
            results['name'] = doc.name
            results['valid'] = True
            results['nname'] = "new doc"
            results['img'] = doc.pages.all()[0].as_img()
            results['size'] = doc.get_npages()
        else:
            results['valid'] = False
    return HttpResponse(json.dumps(results))


def move_document(doc_id, cat_id):
    logger.debug('move_document | doc_id = %d | cat_id = %d' % (doc_id, cat_id))
    doc = get_object_or_404(Document, pk=doc_id)
    old_cat = doc.refer_category
    new_cat = get_object_or_404(Category, pk=cat_id)
    for p in doc.pages.all():
        shutil.move(p.get_absolute_path(), new_cat.get_absolute_path())
    doc.refer_category = new_cat
    doc.save()
    old_cat.documents.remove(doc)
    new_cat.documents.add(doc)
    return True


def ajax_move_doc(request, doc_id, cat_id):
    logger.debug('ajax_move_doc | doc_id = %d | cat_id = %d' % (doc_id, cat_id))
    results = {}
    if request.is_ajax():
        results['valid'] = move_document(doc_id, cat_id)
    return HttpResponse(json.dumps(results))


def delete_document(doc_id):
    logger.debug('delete_document | doc_id = %d' % doc_id)
    doc = get_object_or_404(Document, pk=doc_id)
    doc.refer_category.documents.remove(doc)
    doc.delete()


def ajax_delete(request, doc_id):
    logger.debug('ajax_delete | doc_id = %d' % doc_id)
    results = {}
    if request.is_ajax():
        results['valid'] = delete_document(doc_id)
    return HttpResponse(json.dumps(results))


def ajax_img(request, doc_id, num):
    logger.debug('ajax_img | doc_id = %d | num = %d' % (doc_id, num))
    results = {}
    if request.is_ajax():
        doc = get_object_or_404(Document, pk=doc_id)
        results['img'] = doc.pages.all()[int(num) - 1].as_img()
        results['valid'] = True
    return HttpResponse(json.dumps(results))


def split_doc(request):
    logger.debug('split_doc')
    results = {}
    if request.is_ajax():
        cut = int(request.GET['modal_split_cut'][0])
        doc = get_object_or_404(Document, pk=int(request.GET['modal_split_doc_id']))
        doc.name = request.GET['modal_split_name']
        new_doc = Document(name=request.GET['modal_split_new_name'], owner=request.user,
                           refer_category=doc.refer_category, complete=True)
        pages = doc.all_pages()
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
    logger.debug('merge_doc')
    results = {}
    if request.is_ajax():
        doc = get_object_or_404(Document, pk=int(request.GET['modal_merge_doc_id']))
        l = request.GET['doc_ids'].split(',')
        for add_doc in l:
            old_doc = get_object_or_404(Document, pk=int(add_doc))
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


def ajax_download(request, doc_id):
    logger.debug('ajax_download | doc_id = %d' % doc_id)
    results = {}
    if request.is_ajax():
        doc = get_object_or_404(Document, pk=doc_id)
        # name = doc.name.replace(' ', '_')
        if ".pdf" != doc.name[-4:]:
            name += ".pdf"
        output_abs = settings.TMP_ROOT + name
        output_rel = settings.TMP_URL + name
        # TODO change ouvrir popup avec lien et utiliser le broker
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
    logger.debug("ajax_multiple_move | cat_id = %d" % cat_id)
    results = {}
    if request.is_ajax():
        for key, val in dict(request.GET).items():
            move_document(val[0], cat_id)
        results['valid'] = True
    return HttpResponse(json.dumps(results))


def ajax_multiple_delete(request):
    logger.debug("ajax_multiple_delete")
    results = {}
    if request.is_ajax():
        for key, val in dict(request.GET).items():
            delete_document(val[0])
        results['valid'] = True
    return HttpResponse(json.dumps(results))


def ajax_multiple_download(request):
    logger.debug('ajax_multiple_download')
    results = {}
    if request.is_ajax():
        for key, val in dict(request.GET).items():
            print('%s : %s' % (key, val))
        #TODO finish multiple download broker
        results['valid'] = True
    return HttpResponse(json.dumps(results))
