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
from threading import Timer
from PyPDF2 import PdfFileReader
import re
import subprocess
#import logging


#logger = logging.getLogger(__name__)


def view_category(request, category_id):
    cat = Category.objects.get(id=category_id)
    docs = [d for d in cat.get_docs()]
    # il faut continuer et envoyerau template
    if request.user.is_authenticated():
        return render(request, 'folder.tpl')
    return render(request, "layout.tpl")


def remove_fileupload(liste):
    print("remove_fileupload")
    print(liste)
    for path in liste:
        for fu in FileUpload.objects.all():
            if fu.file.path == path:
                fu.delete()


def convert_pdf_to_jpg(l):
    print("convert_pdf_to_jpg")
    for (cat, path, f, doc) in l:
        #print("%s %s %s %s" % (cat, path, f, doc))
        try:
            n = PdfFileReader(open(path, 'rb')).getNumPages()
        except:
            os.rename(path, path + '_old')
            cmd = u'gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=%s %s' % (path, path + '_old')
            print(cmd.encode('utf-8'))
            os.system(cmd.encode('utf-8'))
            cmd = u'rm -f %s' % (path + '_old')
            print(cmd.encode('utf-8'))
            os.system(cmd.encode('utf-8'))
            pass
        try:
            pdf = PdfFileReader(open(path, 'rb'))
            n = pdf.getNumPages()
        except:
            print("ERREUR FORMAT PDF")
            return None
        cat = cat[0]
        doc = doc[0]
        p = re.compile(r'.[Pp][Dd][Ff]$')
        filename = p.sub('.jpg', str(f))
        new_path = u'%s/%d' % (cat.get_absolute_path(), doc.id) + u'_%03d_' + filename
        cmd = u'gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -r600x600 -sOutputFile=%s %s' % (new_path, path)
        print(cmd.encode('utf-8'))
        os.system(cmd.encode('utf-8'))
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        for i in range(1, n+1):
            name_page = str(doc.id) + "_%03d_" % i + filename
            path_page = '%s/%s' % (cat.get_absolute_path(), name_page)
            im = Image.open(path_page)
            w, h = im.size
            doc.add_page(doc.get_npages() + 1, name_page, w, h)
        doc.complete = True
        doc.save()


def manage_convert_doc_to_pdf(cmds, paths, liste):
    print("manage_convert_doc_to_pdf")
    print(cmds)
    print(paths)
    print(liste)
    for c in cmds:
        os.system(c)
        print(c)
    convert_pdf_to_jpg(liste)
    remove_fileupload(paths)
    for (c, path, f, d) in liste:
        os.remove(path)
        print("remove %s" % (path))


def manage_convert_pdf_to_jpg(liste):
    print("manage_convert_pdf_to_jpg")
    convert_pdf_to_jpg(liste)
    l_path = []
    for (cat, path, f, doc) in liste:
        l_path.append(path)
    remove_fileupload(l_path)


def add_documents(request, category_id):
    if request.is_ajax():
        files = request.GET.getlist('files', False)
        cat = Category.objects.get(id=category_id)
        l_doc = []
        l_pdf = []
        cmds = []
        paths = []
        for f in list(files):
            mime = MimeTypes()
            #logger.error('[ERROR]Something went wrong!')
            #logger.debug('[DEBUG] add %s to %s' % (f, cat))
            print('[INFO] add %s to %s' % (f, cat))
            path = os.path.join(settings.MEDIA_ROOT, settings.UPLOAD_DIR, f)
            m = mime.guess_type(path)[0]
            d = Document(name=f.encode('ascii', 'ignore'), owner=request.user, refer_category=cat)
            d.save()
            cat.add_doc(d)
            if m == 'application/pdf':
                l_pdf.append(([cat], path, f, [d]))
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
                remove_fileupload([path])
            elif m in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                p = re.compile(r'.[Dd][Oo][Cc][xX]?$')
                new_f = p.sub('.pdf', f)
                new_path = path.replace(f, new_f)
                cmd = 'soffice --headless --convert-to pdf  %s --outdir %s/upload' % (path, settings.MEDIA_ROOT)
                cmds.append(cmd)
                paths.append(path)
                l_doc.append(([cat], new_path, new_f, [d]))
            elif m in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                p = re.compile(r'.[Xx][Ll][Ss][xX]?$')
                new_f = p.sub('.pdf', f)
                new_path = path.replace(f, new_f)
                cmd = 'soffice --headless --convert-to pdf  %s --outdir %s/upload' % (path, settings.MEDIA_ROOT)
                cmds.append(cmd)
                paths.append(path)
                l_doc.append(([cat], new_path, new_f, [d]))
            else:
                print("ERREUR FORMAT FICHIER")
        if len(l_doc):
            thread1 = Timer(0, manage_convert_doc_to_pdf, (cmds, paths, l_doc,))
            thread1.start()
        if len(l_pdf):
            thread = Timer(0, manage_convert_pdf_to_jpg, (l_pdf,))
            thread.start()
        results = {'doc_list': [d.as_json() for d in cat.get_docs()], 'n': cat.count_docs()}
        return HttpResponse(json.dumps(results))


def list_documents(request, category_id, n):
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
