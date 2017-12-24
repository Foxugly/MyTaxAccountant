# -*- coding: utf-8 -*-

from utils.models import FiscalYear, TemplateTrimester
from companies.models import Company
from years.models import Year
from trimesters.models import Trimester
from datetime import datetime

year = '2017'
trim = 1
date = datetime(2017, 1, 1)


fiscal_year = FiscalYear.objects.filter(name=year)
if not fiscal_year:
    fy = FiscalYear(name=year)
    fy.save()
else:
    fy = fiscal_year[0]

for t1 in TemplateTrimester.objects.all():
    t1.favorite = False
    t1.save

for t2 in Trimester.objects.all():
    t2.favorite = False
    t2.save

tts = TemplateTrimester.objects.filter(number=trim, year=fy)
if len(tts):
    tt = tts[0]
    tt.favorite = True
    tt.start_date = date
    tt.save
else:
    tt = TemplateTrimester(number=trim, year=fy, favorite=True, start_date=date)
    tt.save()

for c in Company.objects.all():
    for old_year in c.years.filter(favorite=True, refer_company=c):
        if old_year.fiscal_year != fy:
            old_year.favorite = False
            old_year.save
            actual_year = Year(fiscal_year=fy, refer_company=c, active=True, favorite=True)
            actual_year.save()
            c.add_year(actual_year)
        else:
            actual_year = old_year
    new_t1 = Trimester(template=tt, start_date=date, active=True, favorite=True, refer_year=actual_year)
    new_t1.save()
    new_t1.add_categories()
    actual_year.add_trimester(new_t1)
