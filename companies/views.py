# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from django.shortcuts import render_to_response, render, redirect
from django.http import HttpResponse
import json
from users.models import UserProfile, UserProfileForm, UserCreateForm
from companies.models import Company, CompanyForm
from utils.models import FiscalYear, TemplateTrimester
from years.models import Year
from trimesters.models import Trimester
from categories.models import Category, TypeCategory


def favorite_year(company):
    y = company.years.filter(active=True, favorite=True)
    if not y:
        return company.years.filter(active=True)[0]
    else:
        return y[0]


def company_view(request, company_id):
    userprofile = UserProfile.objects.get(user=request.user)
    return render_to_response('folder.tpl', {'userprofile': userprofile})


def list_year(request, company_id):
    if request.is_ajax():
        c = Company.objects.get(id=company_id)
        results = {'list': [y.as_json() for y in c.years.filter(active=True)], 'return': True,
                   'favorite': favorite_year(c).as_json()}
        return HttpResponse(json.dumps(results))


def admin_companies(request):
    c = {'list': Company.objects.all(), 'form': [UserProfileForm(), UserCreateForm(), CompanyForm()], 'url': '/company/add/'}
    return render(request, 'list.tpl', c)


def add_company(request):
    form1 = UserProfileForm(request.POST)
    form2 = UserCreateForm(request.POST)
    form3 = CompanyForm(request.POST)
    if form1.is_valid() and form2.is_valid() and form3.is_valid():
        up = form1.save(commit=False)
        c = form3.save()
        c.active = True
        u = form2.save()
        up.user = u
        up.save()
        up.companies.add(c)
        request.user.userprofile.companies.add(c)
        # add dossier global
        fy_init = FiscalYear.objects.filter(init=True)[0]
        y_init = Year(fiscal_year=fy_init, active=True, refer_company=c, favorite=False)
        y_init.save()
        c.years.add(y_init)
        tt_init = TemplateTrimester.objects.filter(year=fy_init, favorite=True)[0]
        tri_init = Trimester(template=tt_init, start_date=tt_init.start_date, active=True, refer_year=y_init, favorite=True)
        tri_init.save()
        y_init.trimesters.add(tri_init)
        tp_init = TypeCategory.objects.filter(priority=10)[0]
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
        first = True
        for tp in TypeCategory.objects.filter(priority__lt=10).order_by('priority'):
            cat_fav = Category(cat=tp, refer_trimester=tri_fav, active=True, favorite=first)
            first = False
            cat_fav.save()
            tri_fav.categories.add(cat_fav)
        return redirect('companies')
    else:
        c = {'view_form': True, 'list': Company.objects.all(), 'form': [form1(), form2(), form3()]}
        return render(request, 'list.tpl', c)
