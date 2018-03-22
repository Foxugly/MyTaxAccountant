from __future__ import absolute_import, unicode_literals
from mta.celery import app
from django.conf import settings
import shutil
import os
from documents.models import Document
import logging


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOGGER)


@app.task
def build_pdf(doc_id, output_path):
    logger.debug('build_pdf | doc_id = %d | output_filename = %s' % (doc_id, output_filename))
    doc = Document.objects.get(id=doc_id)
    cmd = "convert "
    for p in doc.all_pages():
        cmd += p.get_absolute_path() + " "
    cmd += output_path)
    if os.path.exists(output_path)):
        shutil.remove(output_path)
    os.system(cmd)
    return True
