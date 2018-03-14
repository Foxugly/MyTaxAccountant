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
from categories.models import Category
from mimetypes import MimeTypes
import json
from django.conf import settings
from documents.models import Document, DocumentForm, DocumentAdminForm, DocumentReadOnlyForm
from fileupload.models import FileUpload
from PIL import Image
import os
from threading import Timer
from PyPDF2 import PdfFileReader
import re
import subprocess
from users.models import Log
import time
from django.core.exceptions import ObjectDoesNotExist
from error.models import Error
from django.http import Http404
from unidecode import unidecode
from django.template.defaultfilters import slugify
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime


def view_category(request, category_id):
    if settings.DEBUG:
        print("view_category | id = "+str(category_id))
    try:
        category_current = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        e = Error(user=request.user, detail='[view_category] Category id : %s does not exists' % category_id)
        e.save()
        raise Http404('Category id : %s does not exists' % category_id)

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


def convert_pdf_to_jpg(request, cat, path, f, doc, fu):
    try:
        PdfFileReader(open(unidecode(path), 'rb')).getNumPages()
    except:
        os.rename(path, path + '_old')
        txt = 'mv %s %s \n' % (path, path + '_old')
        cmd = 'gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=%s %s' % (path, path + '_old')
        if settings.DEBUG:
            print(cmd)
        txt += cmd + '\n'
        os.system(cmd)
        cmd = 'rm -f %s' % (path + '_old')
        if settings.DEBUG:
            print(cmd)
        txt += cmd + '\n'
        os.system(cmd)
        l = Log(userprofile=request.user.userprofile, category=cat, cmd=txt)
        l.save()
        pass
    try:
        pdf = PdfFileReader(open(unidecode(path), 'rb'))
        n = pdf.getNumPages()
    except:
        print("ERREUR FORMAT PDF")
        return None
    p = re.compile(r'.[Pp][Dd][Ff]$')
    filename = p.sub('.jpg', f)
    new_path = '%s/%d' % (cat.get_absolute_path(), doc.id) + '_%03d_' + filename
    cmd = 'gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -r300x300 -sOutputFile=%s %s' % (new_path, path)
    if settings.DEBUG:
        print(cmd)
    l = Log(userprofile=request.user.userprofile, category=cat, cmd=cmd)
    l.save()
    # os.system(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    time.sleep(2)
    for i in range(1, n+1):
        name_page = str(doc.id) + "_%03d_" % i + filename
        path_page = '%s/%s' % (cat.get_absolute_path(), name_page)
        im = Image.open(path_page)
        w, h = im.size
        doc.add_page(doc.get_npages() + 1, name_page, w, h)
    doc.complete = True
    doc.save()
    fu.delete()
    return 1


def manage_convert_pdf_to_jpg(request, l):
    if settings.DEBUG:
        print("convert_pdf_to_jpg")
    for (cat, path, f, doc, fu) in l:
        convert_pdf_to_jpg(request, cat, path, f, doc, fu)


def manage_convert_doc_to_pdf(request, liste):
    if settings.DEBUG:
        print("manage_convert_doc_to_pdf")
    for l in liste:
        if settings.DEBUG:
            print(l['cmd'])
        os.system(l['cmd'])
        convert_pdf_to_jpg(request, l['cat'], l['path'], l['filename'], l['document'], l['fileupload'])


def create_document(name, owner, cat, i):
    d = Document(name=name, owner=owner, refer_category=cat, date=timezone.now() + datetime.timedelta(seconds=i))
    d.save()
    cat.add_doc(d)
    return d


def add_documents(request, category_id):
    if request.is_ajax():
        files = request.GET.getlist('files', False)
        try:
            cat = Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            e = Error(user=request.user, detail='[add_documents] Category id : %s does not exists' % category_id)
            e.save()
            return HttpResponse(json.dumps({}))
        l_doc = []
        l_pdf = []
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

            pathname = fu.file.name.split('/')[1]
            pathfile = os.path.join(settings.MEDIA_ROOT, fu.file.name)
            k = pathname.rfind(".")
            pathname_new = '%s.%s' % (slugify(pathname[0:k]), pathname[k+1:])
            pathfile_new = os.path.join(settings.MEDIA_ROOT, settings.UPLOAD_DIR, pathname_new)
            cmd = ['mv', pathfile, pathfile_new]
            subprocess.call(cmd)
            mime = MimeTypes()
            m = mime.guess_type(pathfile_new)[0]
            d = create_document(pathname_new, request.user, cat, i)
            i += 1
            if m == 'application/pdf':
                l_pdf.append((cat, pathfile_new, pathname_new, d, fu))
            elif m in ['image/png', 'image/jpeg', 'image/bmp']:
                im = Image.open(pathfile_new)
                w, h = im.size
                new_filename = '%s_%s' % (str(d.id), pathname_new)
                new_path = os.path.join(cat.get_absolute_path(), new_filename)
                cmd = ['cp', pathfile_new, new_path]
                subprocess.call(cmd)
                d.add_page(d.get_npages() + 1, new_filename, w, h)
                d.complete = True
                d.save()
                if isinstance(fu, FileUpload):
                    fu.delete()
            elif m in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                p = re.compile(r'.[Dd][Oo][Cc][xX]?$')
                new_f = p.sub('.pdf', pathname_new)
                new_path = pathfile_new.replace(pathname_new, new_f)
                cmd = 'soffice --headless --convert-to pdf %s --outdir %s/upload' % (pathfile_new, settings.MEDIA_ROOT)
                l_doc.append(dict(filename=pathname_new, path=new_path, cmd=cmd, fileupload=fu, document=d, cat=cat))
            elif m in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                p = re.compile(r'.[Xx][Ll][Ss][xX]?$')
                new_f = p.sub('.pdf', pathname_new)
                new_path = pathfile_new.replace(pathname_new, new_f)
                cmd = 'soffice --headless --convert-to pdf  %s --outdir %s/upload' % (pathfile_new, settings.MEDIA_ROOT)
                l_doc.append(dict(filename=pathname_new, path=new_path, cmd=cmd, fileupload=fu, document=d, cat=cat))
            else:
                e = Error(user=request.user, detail='[add_documents] FileUpload id : %s Format error' % fu.id)
                e.save()
                error_list.append(d.as_json())
                d.delete()
        if len(l_doc):
            thread1 = Timer(0, manage_convert_doc_to_pdf, (request, l_doc,))
            thread1.start()
        if len(l_pdf):
            thread = Timer(0, manage_convert_pdf_to_jpg, (request, l_pdf,))
            thread.start()
        results = {'doc_list': [d.as_json() for d in cat.get_docs()], 'n': cat.count_docs(), }
        return HttpResponse(json.dumps(results))


def list_documents(request, category_id, n):
    if settings.DEBUG:
        print("list_documents %s %s" % (category_id, n))
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
    l = [None, 'fiscal_id', 'id', 'name', 'date', 'description', 'lock', 'complete']
    arg += l[int(field)]
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
