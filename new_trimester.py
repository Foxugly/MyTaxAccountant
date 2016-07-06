from utils.models import FiscalYear, TemplateTrimester
from companies.models import Company
from years.models import Year
from categories.models import TypeCategory
from trimesters.models import Trimester
from datetime import datetime	

year = '2016'
trim = 3
date = datetime(2016, 7, 1)


fy = FiscalYear.objects.get(name=year)
if not fy:
	fy = FiscalYear(name=year)
	fy.save()

for t in TemplateTrimester.objects.all():
	t.favorite = False
	t.save()

tt = TemplateTrimester.objects.get(number=trim, year=fy)
if tt:
	tt.favorite = True
	tt.start_date = date
	tt.save()
else :
	tt = TemplateTrimester(number=trim, year=fy, favorite=True, start_date=date)
	tt.save()

for c in Company.objects.all():
	y = Year.objects.filter(fiscal_year=fy, refer_company=c)
	if not y:
		y = Year(fiscal_year=fy, refer_company=c, active=True)
		y.save()
		c.add_year(y)
	new_t1 = Trimester(template=tt, start_date=date, active=True, refer_year=y)
	new_t1.save()
	new_t1.add_categories()
	y.add_trimester(new_t1)