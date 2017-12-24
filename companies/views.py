# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from django.shortcuts import render_to_response, render
from django.http import HttpResponse
import json
from users.models import UserProfile, UserProfileCreateForm, UserCreateForm
from companies.models import Company, CompanyForm, CompanyCreateForm
from utils.models import FiscalYear, TemplateTrimester
from years.models import Year
from trimesters.models import Trimester
from categories.models import Category, TypeCategory
from django.contrib.auth.models import User


def favorite_year(company):
    y = company.years.filter(active=True, favorite=True)
    if not y:
        return company.years.filter(active=True)[0]
    else:
        return y[0]


def company_view(request):
    return render_to_response('folder.tpl', {'userprofile': UserProfile.objects.get(user=request.user)})


def list_year(request, company_id):
    if request.is_ajax():
        c = Company.objects.get(id=company_id)
        results = {'list': [y.as_json() for y in c.years.filter(active=True)], 'return': True,
                   'favorite': favorite_year(c).as_json()}
        return HttpResponse(json.dumps(results))


def admin_companies(request):
    companies = request.user.userprofile.companies.all()
    company_current = companies[0]
    years = company_current.years.all()
    year_current = next(y for y in years if y.favorite is True)
    trimesters = year_current.trimesters.all()
    trimester_current = next(t for t in trimesters if t.favorite is True)
    c = dict(companies=companies, company_current=company_current, years=years, year_current=year_current,
             trimesters=trimesters, trimester_current=trimester_current, view='list', list=Company.objects.all(),
             forms=[UserProfileCreateForm(), UserCreateForm(), CompanyCreateForm()], url='/company/add/')
    return render(request, 'list.tpl', c)


def add_company(request):
    form1 = UserProfileCreateForm(request.POST)
    form2 = UserCreateForm(request.POST)
    form3 = CompanyCreateForm(request.POST)
    if form1.is_valid() and form2.is_valid() and form3.is_valid():
        up = form1.save(commit=False)
        c = form3.save()
        c.active = True
        c.favorite = True
        c.save()
        u = form2.save()
        up.user = u
        up.save()
        up.companies.add(c)
        for user in User.objects.filter(is_superuser=True):
            user.userprofile.companies.add(c)
            user.userprofile.save()
        # add dossier global
        fy_init = FiscalYear.objects.filter(init=True)[0]
        y_init = Year(fiscal_year=fy_init, active=True, refer_company=c, favorite=False)
        y_init.save()
        c.years.add(y_init)
        tt_init = TemplateTrimester.objects.filter(year=fy_init, favorite=True)[0]
        #BUG ICI
        print(tt_init)
        tri_init = Trimester(template=tt_init, start_date=tt_init.start_date, active=True, refer_year=y_init,
                             favorite=True)
        tri_init.save()
        y_init.trimesters.add(tri_init)
        tp_init = TypeCategory.objects.get(priority=2000)
        cat_init = Category(cat=tp_init, refer_trimester=tri_init, active=True)
        cat_init.save()
        tri_init.categories.add(cat_init)
        # add favorite_year and favorite_trimester
        fy_fav = FiscalYear.objects.filter(favorite=True)[0]
        y_fav = Year(fiscal_year=fy_fav, active=True, refer_company=c, favorite=True)
        y_fav.save()
        c.years.add(y_fav)
        tt_fav = TemplateTrimester.objects.filter(year=fy_fav, favorite=True)[0]
        tri_fav = Trimester(template=tt_fav, start_date=tt_fav.start_date, active=True, refer_year=y_fav, favorite=True)
        tri_fav.save()
        y_fav.trimesters.add(tri_fav)
        for tp in c.model_trimester.categories.all().order_by('priority'):
            cat_fav = Category(cat=tp, refer_trimester=tri_fav, active=True)
            cat_fav.save()
            tri_fav.categories.add(cat_fav)
        c = {'return': True, 'list': Company.objects.all(),
             'form': [UserProfileCreateForm(), UserCreateForm(), CompanyCreateForm()], 'url': '/company/add/'}
        return render(request, 'list.tpl', c)
    else:
        c = {'view_form': True, 'list': Company.objects.all(), 'form': [form1, form2, form3]}
        return render(request, 'list.tpl', c)


def update_company(request, company_id):
    results = {}
    if request.is_ajax():
        company_form = CompanyForm(request.POST, instance=Company.objects.get(id=company_id))
        if company_form.is_valid():
            company_form.save()
            results['return'] = True
        else:
            results['errors'] = company_form.errors
            results['return'] = False
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))
