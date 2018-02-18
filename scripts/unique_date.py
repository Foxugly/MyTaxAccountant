
from categories.models import Category
from datetime import timedelta


cat = Category.objects.all()
for c in cat:
    for d in c.documents.all():
        same_date = c.documents.filter(date=d.date).order_by('id')
        if len(same_date) > 1:
            i = 0
            for sd in same_date:
                sd.date = sd.date + timedelta(seconds=i)
                sd.save()
                print('%s %s %s' % (sd.id, sd.date, sd))
                i += 1
