from categories.models import Category
from os import listdir
for c in Category.objects.all():
    path = c.get_absolute_path()
    list_path = listdir(path)
    for d in c.get_docs():
        for p in d.all_pages():
            if p.filename in list_path:
                list_path.remove(p.filename)
            else:
                 print "[NOT IN DIRECTORY] " + path
                 print p.filename
    if len(list_path):
        print "[NOT IN DATABASE]" + path
        for e in list_path:
            print e

