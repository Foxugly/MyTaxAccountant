# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.shortcuts import render
from django.http import HttpResponse
from categories.models import Category
from mimetypes import MimeTypes
import json
from django.conf import settings
from documents.models import Page, Document
from fileupload.models import FileUpload
import shutil
from PIL import Image
import os
from threading import Thread
from pyPdf import PdfFileReader

def category_view(request, category_id):
    return HttpResponse("category_view")

def convert_pdf_to_jpg(cat, path, f, doc):
    filename = f.replace('.pdf', '.jpg') #TODO 
    new_path =  cat.get_path() + str(doc.id) + '_' + '%03d' + '_' + filename
    cmd = 'convert -density 600 ' + path + ' ' + new_path
    os.system(cmd)
    pdf = PdfFileReader(open(path,'rb'))
    n = pdf.getNumPages()
    for i in range(0,n) :
        path_page = cat.get_path() + str(doc.id) + '_' + "%03d" % i + '_' + filename
        im = Image.open(path_page)
        w, h = im.size
        doc.add_page(doc.get_npages()+1, path_page, w, h)
    for fu in FileUpload.objects.all():
        if fu.file.path == path :
            fu.delete()
    doc.complete = True
    doc.save()

def add_documents(request,category_id):
    if request.is_ajax():
        files = request.GET.getlist('files', False)
        cat = Category.objects.get(id=category_id)
        for f in list(files) :
            mime = MimeTypes()
            path = settings.MEDIA_ROOT + '/' + settings.UPLOAD_DIR + '/' + f
            m = mime.guess_type(path)[0]
            d = Document(name=f,owner=request.user,refer_category=cat)
            d.save()
            cat.add_doc(d)
            if m == 'application/pdf':
                thread = Thread(target = convert_pdf_to_jpg, args = (cat,path,f,d))
                thread.start()
            elif m in ['image/png', 'image/jpeg', 'image/bmp']:
                im = Image.open(path)
                w, h = im.size
                new_path =  cat.get_path() + str(d.id) + '_' + f
                shutil.copy2(path, new_path)
                d.add_page(d.get_npages()+1, new_path, w, h)
                for fu in FileUpload.objects.all():
                    if fu.file.path == path :
                        fu.delete()
                d.complete = True
                d.save()
            else :
                print 'ERREUR FORMAT FICHIER'
        cat.save()
        results = {}
        data = []
        for d in cat.get_docs() :
            data.append(d.as_json())
        results['doc_list'] = data
        results['n'] = cat.count_docs()
        return HttpResponse(json.dumps(results))

def list_documents(request,category_id):
    if request.is_ajax():
        results = {}
        data = []
        c = Category.objects.get(id=category_id)
        for d in c.get_docs() :
            data.append(d.as_json())
        results['doc_list'] = data
        return HttpResponse(json.dumps(results))