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
import logging


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOGGER)


@app.task
def add(a, b):
    return a+b


@app.task
def add_img(d_id, filename):
    logger.debug("add_img | d_id = %d | filename = %s" % (d_id, filename))
    d = Document.objects.get(id=d_id)
    if not d:
        logger.error("add_img | document (id = %d) does not exist" % d_id)
    path = os.path.join(d.refer_category.get_absolute_path(), filename)
    if not os.path.exists(path):
        logger.error("add_img | path: %s doesn't exist" % path)
    else:
        w, h = Image.open(path).size
        d.add_page(d.get_npages() + 1, filename, w, h)
        d.save()


@app.task
def add_img_document(cat_id, d_id, fu_id):
    logger.debug("add_img_document | cat_id = %d | d_id = %d | fu_id = %d" % (cat_id, d_id, fu_id))
    cat = Category.objects.get(id=cat_id)
    if not cat:
        logger.error("add_img_document | Category (id = %d) does not exist" % cat_id)
    d = Document.objects.get(id=d_id)
    if not d:
        logger.error("add_img_document | Document (id = %d) does not exist" % d_id)
    fu = FileUpload.objects.get(id=fu_id)
    if not fu:
        logger.error("add_img_document | FileUpload (id = %d) does not exist" % fu_id)
    path = os.path.join(settings.MEDIA_ROOT, fu.file.name)
    new_filename = '%d_%s' % (d.id, os.path.basename(fu.file.name))
    shutil.copy(path, os.path.join(cat.get_absolute_path(), new_filename))
    add_img(d.id, new_filename)
    d.complete = True
    d.save()
    fu.delete()


@app.task
def add_pdf_document(cat_id, d_id, fu_id):
    logger.debug("add_pdf_document | cat_id = %d | d_id = %d | fu_id = %d" % (cat_id, d_id, fu_id))
    cat = Category.objects.get(id=cat_id)
    if not cat:
        logger.error("add_pdf_document | Category (id = %d) does not exist" % cat_id)
    d = Document.objects.get(id=d_id)
    if not d:
        logger.error("add_pdf_document | Document (id = %d) does not exist" % d_id)
    fu = FileUpload.objects.get(id=fu_id)
    if not fu:
        logger.error("add_pdf_document | FileUpload (id = %d) does not exist" % fu_id)
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
            logger.info("add_pdf_document %s exists" % last_img)
            break
        else:
            logger.error("add_pdf_document | %d %s does not exist" % (i, last_img))
    if not os.path.exists(last_img):
        logger.error("add_pdf_document | %s does not exist" % last_img)
    for i in range(1, n + 1):
        name_page = "%d_%03d_%s" % (d.id, i, filename)
        add_img(d_id, name_page)
    d.complete = True
    d.save()
    fu.delete()
    return 1


@app.task
def add_spec_document(cat_id, d_id, fu_id, regex):
    logger.debug("add_spec_document | cat_id = %d | d_id = %d | fu_id = %d | regex = %s" % (cat_id, d_id, fu_id, regex))
    fu = FileUpload.objects.get(id=fu_id)
    if not fu:
        logger.error("add_spec_document | FileUpload (id = %d) does not exist" % fu_id)
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
    logger.debug("add_doc_document | cat_id = %d | d_id = %d | fu_id = %d" % (cat_id, d_id, fu_id))
    return add_spec_document(cat_id, d_id, fu_id, r'.[Dd][Oo][Cc][xX]?$')


@app.task
def add_xls_document(cat_id, d_id, fu_id):
    logger.debug("add_xls_document | cat_id = %d | d_id = %d | fu_id = %d" % (cat_id, d_id, fu_id))
    return add_spec_document(cat_id, d_id, fu_id, r'.[Xx][Ll][Ss][xX]?$')

@app.task
def backup_document(fu_id, d_id):
    logger.debug("backup_document | fu_id = %d | d_id = %d" % (fu_id, d_id))
    fu = FileUpload.objects.get(id=fu_id)
    if not fu:
        logger.error("backup_document | FileUpload (id = %d) does not exist" % fu_id)
    d = Document.objects.get(id=d_id)
    if not d:
        logger.error("add_pdf_document | Document (id = %d) does not exist" % d_id)
    path = os.path.join(settings.MEDIA_ROOT, fu.file.name)
    new_filename = "%d_%s" % (d_id, os.path.basename(path))
    new_path = os.path.join(settings.MEDIA_ROOT, settings.BACKUP_DIR, new_filename)
    cmd = 'cp %s %s' % (path, new_path)
    os.system(cmd)
