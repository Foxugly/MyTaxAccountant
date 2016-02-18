# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.http import HttpResponse
from categories.models import Category
from mimetypes import MimeTypes
import json
from django.conf import settings
from documents.models import Document, DocumentForm, DocumentAdminForm, DocumentReadOnlyForm
from fileupload.models import FileUpload
import shutil
from PIL import Image
import os
from threading import Thread
from pyPdf import PdfFileReader
import re


def category_view(request, category_id):
    return HttpResponse("category_view")


def convert_pdf_to_jpg(cat, path, f, doc):
    p = re.compile(r'.[Pp][Dd][Ff]$')
    filename = p.sub('.jpg', f)
    new_path = cat.get_absolute_path() + '/' + str(doc.id) + '_' + '%03d' + '_' + filename
    cmd = 'convert -density 600 ' + path + ' ' + new_path
    os.system(cmd)
    pdf = PdfFileReader(open(path, 'rb'))
    n = pdf.getNumPages()
    for i in range(0, n):
        name_page = str(doc.id) + '_' + "%03d" % i + '_' + filename
        path_page = cat.get_absolute_path() + '/' + name_page
        im = Image.open(path_page)
        w, h = im.size
        doc.add_page(doc.get_npages() + 1, name_page, w, h)
    for fu in FileUpload.objects.all():
        if fu.file.path == path:
            fu.delete()
    doc.complete = True
    doc.save()


def add_documents(request, category_id):
    if request.is_ajax():
        files = request.GET.getlist('files', False)
        cat = Category.objects.get(id=category_id)
        for f in list(files):
            mime = MimeTypes()
            path = os.path.join(settings.MEDIA_ROOT, settings.UPLOAD_DIR, f)
            m = mime.guess_type(path)[0]
            d = Document(name=f, owner=request.user, refer_category=cat)
            d.save()
            cat.add_doc(d)
            if m == 'application/pdf':
                thread = Thread(target=convert_pdf_to_jpg, args=(cat, path, f, d))
                thread.start()
            elif m in ['image/png', 'image/jpeg', 'image/bmp']:
                im = Image.open(path)
                w, h = im.size
                new_filename = str(d.id) + '_' + f
                new_path = os.path.join(cat.get_absolute_path(), new_filename)
                shutil.copy2(path, new_path)
                d.add_page(d.get_npages() + 1, new_filename, w, h)
                for fu in FileUpload.objects.all():
                    if fu.file.path == path:
                        fu.delete()
                d.complete = True
                d.save()
            elif m in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                p = re.compile(r'.[Dd][Oo][Cc][xX]?$')
                new_f = p.sub('.pdf', f)
                new_path = path.replace(f, new_f)
                cmd = 'soffice --headless --convert-to pdf  %s --outdir media/upload' % path
                os.system(cmd)
                thread = Thread(target=convert_pdf_to_jpg, args=(cat, new_path, new_f, d))
                thread.start()
            else:
                print 'ERREUR FORMAT FICHIER'
        results = {}
        data = []
        for d in cat.get_docs():
            data.append(d.as_json())
        results['doc_list'] = data
        results['n'] = cat.count_docs()
        return HttpResponse(json.dumps(results))


def list_documents(request, category_id):
    if request.is_ajax():
        results = {}
        data = []
        c = Category.objects.get(id=category_id)
        for d in c.get_docs():
            data.append(d.as_json())
        results['doc_list'] = data
        results['n'] = c.count_docs()
        return HttpResponse(json.dumps(results))


def form_document(request, category_id, n):
    if request.is_ajax():
        results = {}
        cat = Category.objects.get(pk=category_id)
        if cat.count_docs() > 0:
            doc = cat.get_doc(int(n))
            if request.user.is_superuser:
                results['form'] = DocumentAdminForm(instance=doc).as_div()
            else:
                if doc.lock:
                    results['form'] = DocumentReadOnlyForm(instance=doc).as_div()
                else:
                    results['form'] = DocumentForm(instance=doc).as_div()
            results['img'] = doc.as_img()
            results['doc_id'] = doc.id
            results['valid'] = True
        else:
            results['valid'] = False
        return HttpResponse(json.dumps(results))


def ajax_move(request, category_id, n):
    if request.is_ajax():
        results = {}
        cat = Category.objects.get(pk=category_id)
        if cat.count_docs() > 0:
            results['doc_id'] = cat.get_doc(int(n))
            tri = cat.refer_trimester
            results['categories'] = [c.get_name() for c in tri.categories.all()]
            results['category'] = cat.get_name()
            year = tri.refer_year
            results['trimesters'] = [t.get_name() for t in year.trimesters.all()]
            results['trimester'] = tri.get_name()
            company = year.refer_company
            results['years'] = [y.get_name() for y in company.years.all()]
            results['year'] = year.get_name()
            results['companies'] = [c.get_name() for c in request.user.userprofile.companies.all()]
            results['company'] = company.get_name()
            results['valid'] = True
        else:
            results['valid'] = False
        return HttpResponse(json.dumps(results))


def ajax_merge(request, category_id, n):
    if request.is_ajax():
        results = {}
        cat = Category.objects.get(pk=category_id)
        if cat.count_docs() > 0:
            doc = cat.get_doc(int(n))
            # TODO AJOUTER
            results['valid'] = True
        else:
            results['valid'] = False
        return HttpResponse(json.dumps(results))


def ajax_split(request, category_id, n):
    if request.is_ajax():
        results = {}
        cat = Category.objects.get(pk=category_id)
        if cat.count_docs() > 0:
            doc = cat.get_doc(int(n))
            # TODO AJOUTER
            results['valid'] = True
        else:
            results['valid'] = False
        return HttpResponse(json.dumps(results))
