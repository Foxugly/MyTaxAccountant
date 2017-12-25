from documents.models import Document
from categories.models import Category
import os


def move_doc(doc_id, cat_id):
    doc = Document.objects.get(pk=int(doc_id))
    old_cat = doc.refer_category
    new_cat = Category.objects.get(pk=int(cat_id))
    for p in doc.pages.all():
        cmd = "mv " + p.get_absolute_path() + " " + new_cat.get_absolute_path() + "/"
        os.system(cmd)
    doc.refer_category = new_cat
    doc.save()
    old_cat.documents.remove(doc)
    new_cat.documents.add(doc)


