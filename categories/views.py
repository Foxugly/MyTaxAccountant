# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.utils import timezone
from categories.models import Category
from mimetypes import MimeTypes
from documents.models import Document, DocumentForm, DocumentAdminForm, DocumentReadOnlyForm
from fileupload.models import FileUpload
from error.models import Error
from .tasks import add_pdf_document, add_img_document, add_doc_document, add_xls_document
import datetime
import os
import shutil
import json
import logging


logger = logging.getLogger(__name__)
logger.setLevel(settings.logger)


def view_category(request, category_id):
    logger.debug("view_category | id = %d" % category_id)
    category_current = get_object_or_404(Category, id=category_id)
    trimester_current = category_current.refer_trimester
    year_current = trimester_current.refer_year
    company_current = year_current.refer_company
    companies = request.user.userprofile.companies.all().order_by('name')
    years = company_current.get_years()
    trimesters = year_current.get_trimesters()
    categories = trimester_current.get_categories()
    docs = category_current.get_docs()
    c = dict(companies=companies, company_current=company_current, years=years, year_current=year_current,
             trimesters=trimesters, trimester_current=trimester_current, categories=categories,
             category_current=category_current, docs=docs, view='list')
    if trimester_current.refer_year.refer_company in request.user.userprofile.companies.all():
        # il faut continuer et envoyer au template
        if request.user.is_authenticated:
                return render(request, 'folder_list.tpl', c)
    else:
        raise PermissionDenied


def create_document(name, owner, cat, i):
    logger.debug("create_document | filename = %s " % name)
    d = Document(name=name, owner=owner, refer_category=cat, date=timezone.now() + datetime.timedelta(seconds=i))
    d.save()
    cat.add_doc(d)
    return d


def add_documents(request, category_id):
    logger.debug("add_documents | category_id = %d " % category_id)
    if request.is_ajax():
        files = request.GET.getlist('files', False)
        get_object_or_404(Category, id=category_id)
        error_list = []
        i = 0
        for f in list(files):
            fu = None
            fu_list = FileUpload.objects.filter(slug=f)
            if len(fu_list) == 1:
                fu = fu_list[0]
            else:
                fu_list2 = FileUpload.objects.filter(file__contains=f)
                if len(fu_list2) == 1:
                    fu = fu_list2[0]
            if not fu:
                e = Error(user=request.user, detail='[add_documents] FileUpload id error : %s ' % f)
                e.save()
                return 0
                # TODO gestion des erreurs
            pathname = os.path.basename(fu.file.name)
            k = pathname.rfind(".")
            pathname_new = '%s.%s' % (slugify(pathname[0:k]), pathname[k + 1:])
            shutil.move(os.path.join(settings.MEDIA_ROOT, fu.file.name),
                        os.path.join(settings.MEDIA_ROOT, settings.UPLOAD_DIR, pathname_new))
            fu.file.name = os.path.join(settings.UPLOAD_DIR, pathname_new)
            fu.save()
            mime = MimeTypes()
            m = mime.guess_type(os.path.join(settings.MEDIA_ROOT, fu.file.name))[0]
            d = create_document(os.path.basename(fu.file.name), request.user, cat, i)
            i += 1
            if m == 'application/pdf':
                add_pdf_document.delay(cat.id, d.id, fu.id)
            elif m in ['image/png', 'image/jpeg', 'image/bmp']:
                add_img_document(cat.id, d.id, fu.id)
            elif m in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                add_doc_document.delay(cat.id, d.id, fu.id)
            elif m in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                add_xls_document.delay(cat.id, d.id, fu.id)
            else:
                e = Error(user=request.user, detail='[add_documents] FileUpload id : %s Format error' % fu.id)
                e.save()
                error_list.append(d.as_json())
                d.delete()
            # TODO Gestion des mauvais fichiers
        results = {'doc_list': [d.as_json() for d in cat.get_docs()], 'n': cat.count_docs(), }
        return HttpResponse(json.dumps(results))


def list_documents(request, category_id, n):
    logger.debug("list_documents | category_id = %d | n = %s" % (category_id, n))
    if request.is_ajax():
        try:
            cat = Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            e = Error(user=request.user, detail='[list_documents] Category id : %s does not exists' % category_id)
            e.save()
            return HttpResponse(json.dumps({}))
        if cat.count_docs() == 0:
            docjson = None
            form = None
        else:
            doc = cat.get_docs()[int(n)-1]
            docjson = doc.as_json()
            if request.user.is_superuser:
                form = DocumentAdminForm(instance=doc).as_div()
            else:
                if doc.lock:
                    form = DocumentReadOnlyForm(instance=doc).as_div()
                else:
                    form = DocumentForm(instance=doc).as_div()
        results = {'doc_list': [d.as_json() for d in cat.get_docs()], 'n': cat.count_docs(), 'form': form,
                   'doc': docjson, 'valid': True}
        return HttpResponse(json.dumps(results))


def form_document(request, category_id, n):
    if settings.DEBUG:
        print("form_document %s %s" % (category_id, n))
    if request.is_ajax():
        try:
            cat = Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            e = Error(user=request.user, detail='[form_document] Category id : %s does not exists' % category_id)
            e.save()
            return HttpResponse(json.dumps({}))
        if cat.count_docs() > 0:
            try:
                doc = Document.objects.get(pk=n)
            except ObjectDoesNotExist:
                e = Error(user=request.user, detail='[form_document] doc id : %s does not exists' % n)
                e.save()
                return HttpResponse(json.dumps({}))
            if request.user.is_superuser:
                form = DocumentAdminForm(instance=doc).as_div()
            else:
                if doc.lock:
                    form = DocumentReadOnlyForm(instance=doc).as_div()
                else:
                    form = DocumentForm(instance=doc).as_div()
            results = {'form': form, 'img': doc.as_img, 'doc_id': doc.id, 'valid': True}
        else:
            results = {'valid': False}
        return HttpResponse(json.dumps(results))


def view_form(request, category_id, field, sens, n):
    if settings.DEBUG:
        print("view_form")
    if not request.user.is_authenticated:
        raise PermissionDenied
    try:
            category_current = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        e = Error(user=request.user, detail='[view_form] Category id : %s does not exists' % category_id)
        e.save()
        raise Http404('Category id : %s does not exists' % category_id)
    trimester_current = category_current.refer_trimester
    year_current = trimester_current.refer_year
    company_current = year_current.refer_company
    companies = request.user.userprofile.companies.all()
    years = company_current.years.all()
    trimesters = year_current.trimesters.all()
    categories = trimester_current.categories.all()
    docs_all = category_current.documents.all()
    if company_current not in request.user.userprofile.companies.all():
        raise PermissionDenied
    arg = ''
    if sens == 'desc':
        arg += '-'
    list_fields = [None, 'fiscal_id', 'id', 'name', 'date', 'description', 'lock', 'complete']
    arg += list_fields[int(field)]
    docs = docs_all.order_by(arg)
    indice = int(n)-1
    try:
        doc = docs[indice]
    except IndexError:
        e = Error(user=request.user, detail='[view_form] doc[%s] of category %s out of range' % (indice, category_id))
        e.save()
        raise Http404('doc[%s] of category %s out of range' % (indice, category_id))
    if request.user.is_superuser:
        form = DocumentAdminForm(instance=doc)
    else:
        if doc.lock:
            form = DocumentReadOnlyForm(instance=doc)
        else:
            form = DocumentForm(instance=doc)
    c = dict(companies=companies, company_current=company_current, years=years, year_current=year_current,
             trimesters=trimesters, trimester_current=trimester_current, categories=categories, view='form',
             category_current=category_current, doc_form=form, doc_id=doc.id, n_max=len(docs), n_cur=int(n),
             img=doc.as_img)
    return render(request, 'folder_form.tpl', c)
