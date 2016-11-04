
from utils.models import FiscalYear, TemplateTrimester
from companies.models import Company
from years.models import Year
from trimesters.models import Trimester
from datetime import datetime

year = '2016'
trim = 4
date = datetime(2016, 10, 1)


fy = FiscalYear.objects.get(name=year)
if not fy:
    fy = FiscalYear(name=year)
    fy.save()

for t1 in TemplateTrimester.objects.all():
    t1.favorite = False
    t1.save()

for t2 in Trimester.objects.all():
    t2.favorite = False
    t2.save()

tts = TemplateTrimester.objects.filter(number=trim, year=fy)
if len(tts):
    tt = tts[0]
    tt.favorite = True
    tt.start_date = date
    tt.save()
else:
    tt = TemplateTrimester(number=trim, year=fy, favorite=True, start_date=date)
    tt.save()

for c in Company.objects.all():
    y = Year.objects.filter(fiscal_year=fy, refer_company=c)[0]
    if not y:
        y = Year(fiscal_year=fy, refer_company=c, active=True)
        y.save()
        c.add_year(y)
    new_t1 = Trimester(template=tt, start_date=date, active=True, refer_year=y)
    new_t1.save()
    new_t1.add_categories()
    y.add_trimester(new_t1)
