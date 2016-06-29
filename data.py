from users.models import UserProfile
from django.contrib.auth.models import User

u = User.objects.all()
up = UserProfile(user=u[0])
up.save()

from utils.models import Country, FiscalYear
fy1 = FiscalYear(name='2015')
fy1.save()
fy2 = FiscalYear(name='2016')
fy2.save()

country1 = Country(name='Belgium')
country1.save()

from companies.models import Company
c1 = Company(name='Alpha',slug='alpha',vat_number='123456789', country=country1, active=True)
c1.save()
up.add_company(c1)
c2 = Company(name='Beta',slug='beta',vat_number='123456780', country=country1, active=True)
c2.save()
up.add_company(c2)

from years.models import Year
y11 = Year(fiscal_year=fy1, refer_company=c1, active=True)
y11.save()
c1.add_year(y11)
y12 = Year(fiscal_year=fy2, refer_company=c1, active=True)
y12.save()
c1.add_year(y12)
y21 = Year(fiscal_year=fy1, refer_company=c2, active=True)
y21.save()
c2.add_year(y21)
y22 = Year(fiscal_year=fy2, refer_company=c2, active=True)
y22.save()
c2.add_year(y22)


from categories.models import TypeCategory
tc1 = TypeCategory(name='Sales', priority=1, active=True)
tc1.save()
tc2 = TypeCategory(name='Invoice', priority=2, active=True)
tc2.save()
tc3 = TypeCategory(name='Bank', priority=3, active=True)
tc3.save()
tc4 = TypeCategory(name='Others', priority=4, active=True)
tc4.save()

from utils.models import TemplateTrimester
from datetime import datetime
tt0 = TemplateTrimester(number=3, year=fy1, favorite=False, start_date=datetime(2015, 7, 1))
tt0.save()
tt1 = TemplateTrimester(number=4, year=fy1, favorite=False, start_date=datetime(2015, 10, 1))
tt1.save()
tt2 = TemplateTrimester(number=1, year=fy2, favorite=False, start_date=datetime(2016, 1, 1))
tt2.save()
tt3 = TemplateTrimester(number=2, year=fy2, favorite=True, start_date=datetime(2016, 4, 1))
tt3.save()
tt4 = TemplateTrimester(number=3, year=fy2, favorite=False, start_date=datetime(2016, 7, 1))
tt4.save()

from trimesters.models import Trimester
from datetime import datetime	
t1 = Trimester(template=tt1, start_date=datetime(2015, 10, 1), active=True, refer_year=y11)
t1.save()
t1.add_categories()
y11.add_trimester(t1)
t2 = Trimester(template=tt0, start_date=datetime(2015, 7, 1), active=True, refer_year=y11)
t2.save()
t2.add_categories()
y11.add_trimester(t2)
t3 = Trimester(template=tt2, start_date=datetime(2016, 1, 1), active=True, refer_year=y12)
t3.save()
t3.add_categories()
y12.add_trimester(t3)
t4 = Trimester(template=tt3, start_date=datetime(2016, 4, 1), active=True, refer_year=y12)
t4.save()
t4.add_categories()
y12.add_trimester(t4)
t5 = Trimester(template=tt1, start_date=datetime(2015, 10, 1), active=True, refer_year=y21)
t5.save()
t5.add_categories()
y21.add_trimester(t5)
t6 = Trimester(template=tt0, start_date=datetime(2015, 7, 1), active=True, refer_year=y21)
t6.save()
t6.add_categories()
y21.add_trimester(t6)
t7 = Trimester(template=tt2, start_date=datetime(2016, 1, 1), active=True, refer_year=y22)
t7.save()
t7.add_categories()
y22.add_trimester(t7)
t8 = Trimester(template=tt3, start_date=datetime(2016, 4, 1), active=True, refer_year=y22)
t8.save()
t8.add_categories()
y22.add_trimester(t8)

t9 = Trimester(template=tt4, start_date=datetime(2016, 7, 1), active=True, refer_year=y12)
t9.save()
t9.add_categories()
y12.add_trimester(t9)

t10 = Trimester(template=tt4, start_date=datetime(2016, 7, 1), active=True, refer_year=y22)
t10.save()
t10.add_categories()
y22.add_trimester(t10)




