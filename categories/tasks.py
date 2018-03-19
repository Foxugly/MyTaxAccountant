from __future__ import absolute_import, unicode_literals
from mta.celery import app
from django.conf import settings
from PyPDF2 import PdfFileReader
import shutil
import os
from PIL import Image
import re
import time
from categories.models import Category
from fileupload.models import FileUpload
from documents.models import Document


@app.task
def add(a, b):
    return a+b


@app.task
def add_img(d_id, filename):
    d = Document.objects.get(id=d_id)
    if settings.DEBUG:
        print('add_img')
    path = os.path.join(d.refer_category.get_absolute_path(), filename)
    if not os.path.exists(path) and settings.DEBUG:
        print("[add_img] ERROR path: %s doesn't exist" % path)
    else:
        w, h = Image.open(path).size
        d.add_page(d.get_npages() + 1, filename, w, h)
        d.save()


@app.task
def add_img_document(cat_id, d_id, fu_id):
    if settings.DEBUG:
        print('add_img_document')
    cat = Category.objects.get(id=cat_id)
    d = Document.objects.get(id=d_id)
    fu = FileUpload.objects.get(id=fu_id)
    path = os.path.join(settings.MEDIA_ROOT, fu.file.name)
    new_filename = '%d_%s' % (d.id, os.path.basename(fu.file.name))
    shutil.copy(path, os.path.join(cat.get_absolute_path(), new_filename))
    add_img(d.id, new_filename)
    d.complete = True
    d.save()
    fu.delete()


@app.task
def add_pdf_document(cat_id, d_id, fu_id):
    if settings.DEBUG:
        print('add_pdf_document')
    cat = Category.objects.get(id=cat_id)
    d = Document.objects.get(id=d_id)
    fu = FileUpload.objects.get(id=fu_id)
    path = os.path.join(settings.MEDIA_ROOT, fu.file.name)
    try:
        PdfFileReader(open(path, 'rb')).getNumPages()
    except:
        shutil.move(path, path + '_old')
        cmd = 'gs -dBATCH -dNOPAUSE -sDEVICE=pdfwrite -sOutputFile=%s %s' % (path, path + '_old')
        if settings.DEBUG:
            print(cmd)
        os.system(cmd)
        cmd = 'rm -f %s' % (path + '_old')
        if settings.DEBUG:
            print(cmd)
        os.system(cmd)
        pass
    # usable pdf
    try:
        pdf = PdfFileReader(open(path, 'rb'))
        n = pdf.getNumPages()
    except:
        print("ERREUR FORMAT PDF")
        return None
    p = re.compile(r'.[Pp][Dd][Ff]$')
    filename = p.sub('.jpg', os.path.basename(fu.file.name))
    new_path = '%s/%d' % (cat.get_absolute_path(), d.id) + '_%03d_' + filename
    cmd = 'gs -dBATCH -dNOPAUSE -sDEVICE=jpeg -r300x300 -sOutputFile=%s %s' % (new_path, path)
    if settings.DEBUG:
        print(cmd)
    os.system(cmd)
    last_img = os.path.join(cat.get_absolute_path(), "%d_%03d_%s" % (d.id, n, filename))
    for i in range(1, 10):
        time.sleep(1)
        if os.path.exists(last_img):
            if settings.DEBUG:
                print("[add_pdf_document] %s exists" % last_img)
            break
        else:
            if settings.DEBUG:
                print("[add_pdf_document] [%d] %s doesn't exist" % (i, last_img))
    if not os.path.exists(last_img):
        if settings.DEBUG:
            print("[add_pdf_document] ERROR path: %s doesn't exist" % last_img)
    for i in range(1, n + 1):
        name_page = "%d_%03d_%s" % (d.id, i, filename)
        add_img(d_id, name_page)
    d.complete = True
    d.save()
    fu.delete()
    return 1


@app.task
def add_spec_document(cat_id, d_id, fu_id, regex):
    if settings.DEBUG:
        print('add_spec_document')
    fu = FileUpload.objects.get(id=fu_id)
    path = os.path.join(settings.MEDIA_ROOT, fu.file.name)
    filename = os.path.basename(path)
    p = re.compile(regex)
    new_filename = p.sub('.pdf', filename)
    cmd = 'soffice --headless --convert-to pdf %s --outdir %s/%s' % (path, settings.MEDIA_ROOT, settings.UPLOAD_DIR)
    os.system(cmd)
    fu.file.name = os.path.join(settings.UPLOAD_DIR, new_filename)
    fu.save()
    return add_pdf_document(cat_id, d_id, fu_id)


@app.task
def add_doc_document(cat_id, d_id, fu_id):
    if settings.DEBUG:
        print('add_doc_document')
    return add_spec_document(cat_id, d_id, fu_id, r'.[Dd][Oo][Cc][xX]?$')


@app.task
def add_xls_document(cat_id, d_id, fu_id):
    if settings.DEBUG:
        print('add_xls_document')
    return add_spec_document(cat_id, d_id, fu_id, r'.[Xx][Ll][Ss][xX]?$')
