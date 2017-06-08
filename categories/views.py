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
import shutil
from PIL import Image
import os
from threading import Timer
from PyPDF2 import PdfFileReader
import re
import subprocess
from users.models import Log
import time


def view_category(request, category_id):
    if settings.DEBUG:
        print("view_category | id = "+str(category_id))
    category_current = Category.objects.get(id=category_id)
    trimester_current = category_current.refer_trimester
    year_current = trimester_current.refer_year
    company_current = year_current.refer_company
    companies = request.user.userprofile.companies.all()
    years = company_current.years.all()
    trimesters = year_current.trimesters.all()
    categories = trimester_current.categories.all()
    docs = category_current.documents.all()
    c = {'companies': companies, 'company_current': company_current, 'years': years, 'year_current': year_current,
         'trimesters': trimesters, 'trimester_current': trimester_current, 'categories': categories,
         'category_current': category_current, 'docs': docs}

    # il faut continuer et envoyer au template
    if request.user.is_authenticated():
            return render(request, 'folder.tpl', c)
    return render(request, "layout.tpl", c)


def convert_pdf_to_jpg(request, cat, path, f, doc):
    try:
        PdfFileReader(open(path, 'rb')).getNumPages()
    except:
        os.rename(path, path + '_old')
        txt = 'mv %s %s \n' % (path, path + '_old')
        cmd = u'gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=%s %s' % (path, path + '_old')
        if settings.DEBUG:
            print(cmd.encode('utf-8'))
        txt += cmd.encode('utf-8') + '\n'
        os.system(cmd.encode('utf-8'))
        cmd = u'rm -f %s' % (path + '_old')
        if settings.DEBUG:
            print(cmd.encode('utf-8'))
        txt += cmd.encode('utf-8') + '\n'
        os.system(cmd.encode('utf-8'))
        l = Log(userprofile=request.user.userprofile, category=cat, cmd=txt)
        l.save()
        pass
    try:
        pdf = PdfFileReader(open(path, 'rb'))
        n = pdf.getNumPages()
    except:
        print("ERREUR FORMAT PDF")
        return None
    p = re.compile(r'.[Pp][Dd][Ff]$')
    filename = p.sub('.jpg', str(f))
    new_path = u'%s/%d' % (cat.get_absolute_path(), doc.id) + u'_%03d_' + filename
    cmd = u'gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -r300x300 -sOutputFile=%s %s' % (new_path, path)
    if settings.DEBUG:
        print(cmd.encode('utf-8'))
    l = Log(userprofile=request.user.userprofile, category=cat, cmd=cmd.encode('utf-8'))
    l.save()
    os.system(cmd.encode('utf-8'))
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    time.sleep(5)
    for i in range(1, n+1):
        name_page = str(doc.id) + "_%03d_" % i + filename
        path_page = '%s/%s' % (cat.get_absolute_path(), name_page)
        im = Image.open(path_page)
        w, h = im.size
        doc.add_page(doc.get_npages() + 1, name_page, w, h)
    doc.complete = True
    doc.save()
    return 1


def manage_convert_pdf_to_jpg(request, l):
    if settings.DEBUG:
        print("convert_pdf_to_jpg")
    for (cat, path, f, doc) in l:
        convert_pdf_to_jpg(request, cat, path, f, doc)


def manage_convert_doc_to_pdf(request, liste):
    if settings.DEBUG:
        print("manage_convert_doc_to_pdf")
    for l in liste:
        if settings.DEBUG:
            print(l['cmd'])
        out = os.system(l['cmd'])
        print(out)
        out2 = convert_pdf_to_jpg(request, l['cat'], l['path'], l['filename'], l['document'])
        print(out2)
        l['fileupload'].delete()


def create_document(name, owner, cat):
    d = Document(name=name, owner=owner, refer_category=cat)
    d.save()
    cat.add_doc(d)
    return d


def add_documents(request, category_id):
    if request.is_ajax():
        files = request.GET.getlist('files', False)
        cat = Category.objects.get(id=category_id)
        l_doc = []
        l_pdf = []
        for f in list(files):
            print f
            fu = None
            fu_list = FileUpload.objects.filter(slug=f)
            if len(fu_list) == 1:
                fu = fu_list[0]
            else:
                fu_list2 = FileUpload.objects.filter(file__contains=f)
                if len(fu_list2) == 1:
                    fu = fu_list2[0]
            if not fu:
                print("ERREUR")
                return 0
            else:
                print(fu)
            mime = MimeTypes()
            if settings.DEBUG:
                print('[INFO] add %s to %s' % (fu, cat))
            path = os.path.join(settings.MEDIA_ROOT, settings.UPLOAD_DIR, fu.slug)
            m = mime.guess_type(path)[0]
            d = create_document(fu.slug, request.user, cat)
            if m == 'application/pdf':
                l_pdf.append((cat, path, fu, d))
            elif m in ['image/png', 'image/jpeg', 'image/bmp']:
                im = Image.open(path)
                w, h = im.size
                new_filename = '%s_%s' % (str(d.id), fu.slug)
                new_path = os.path.join(cat.get_absolute_path(), new_filename)
                shutil.copy2(path, new_path)
                print(path)
                print(new_path)
                d.add_page(d.get_npages() + 1, new_filename, w, h)
                d.complete = True
                d.save()
                if isinstance(fu, FileUpload):
                    fu.delete()
            elif m in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                p = re.compile(r'.[Dd][Oo][Cc][xX]?$')
                new_f = p.sub('.pdf', fu.slug)
                new_path = path.replace(fu.slug, new_f)
                cmd = 'soffice --headless --convert-to pdf  %s --outdir %s/upload' % (path, settings.MEDIA_ROOT)
                l_doc.append(dict(filename=new_f, path=new_path, cmd=cmd, fileupload=fu, document=d, cat=cat))
            elif m in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                p = re.compile(r'.[Xx][Ll][Ss][xX]?$')
                new_f = p.sub('.pdf', f.slug)
                new_path = path.replace(f.slug, new_f)
                cmd = 'soffice --headless --convert-to pdf  %s --outdir %s/upload' % (path, settings.MEDIA_ROOT)
                l_doc.append(dict(filename=new_f, path=new_path, cmd=cmd, fileupload=fu, document=d, cat=cat))
            else:
                print("ERREUR FORMAT FICHIER")
        if len(l_doc):
            thread1 = Timer(0, manage_convert_doc_to_pdf, (request, l_doc,))
            thread1.start()
        if len(l_pdf):
            thread = Timer(0, manage_convert_pdf_to_jpg, (request, l_pdf,))
            thread.start()
        results = {'doc_list': [d.as_json() for d in cat.get_docs()], 'n': cat.count_docs()}
        return HttpResponse(json.dumps(results))


def list_documents(request, category_id, n):
    if settings.DEBUG:
        print("list_documents %s %s" % (category_id, n))
    if request.is_ajax():
        cat = Category.objects.get(id=category_id)
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
        cat = Category.objects.get(pk=category_id)
        if cat.count_docs() > 0:
            doc = Document.objects.get(pk=n)
            if request.user.is_superuser:
                form = DocumentAdminForm(instance=doc).as_div()
            else:
                if doc.lock:
                    form = DocumentReadOnlyForm(instance=doc).as_div()
                else:
                    form = DocumentForm(instance=doc).as_div()
            results = {'form': form, 'img': doc.as_img(), 'doc_id': doc.id, 'valid': True}
        else:
            results = {'valid': False}
        return HttpResponse(json.dumps(results))
