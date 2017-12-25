# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.http import HttpResponse
from django.utils import translation
from django import http
import json
from django.conf import settings
from utils.models import FiscalYear, FiscalYearForm, TemplateTrimester, TemplateTrimesterForm
from django.shortcuts import render
from companies.models import Company
from trimesters.models import Trimester


def lang(request):
    results = {}
    if request.is_ajax():
        user_language = request.POST['lang']
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language
        results['return'] = True
        response = http.HttpResponse(json.dumps(results))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
        return response
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))


def admin_utils(request):
    c = dict(fiscalyears=FiscalYear.objects.all(), fiscalyear_form=FiscalYearForm(),
             fiscalyear_url='/utils/add_fiscal_year/', templatetrimesters=TemplateTrimester.objects.all(),
             templatetrimester_form=TemplateTrimesterForm(), templatetrimester_url='/utils/add_model_trimester/')
    return render(request, 'utils.tpl', c)


def add_fiscal_year(request):
    form = FiscalYearForm(request.POST)
    if form.is_valid():
        form.save()
        c = dict(fiscalyears=FiscalYear.objects.all(), fiscalyear_form=FiscalYearForm(), fiscalyear_return=True,
                 fiscalyear_url='/utils/add_fiscal_year/', templatetrimesters=TemplateTrimester.objects.all(),
                 templatetrimester_form=TemplateTrimesterForm(), templatetrimester_url='/utils/add_model_trimester/')
    else:
        c = dict(fiscalyears=FiscalYear.objects.all(), fiscalyear_form=form,
                 fiscalyear_url='/utils/add_fiscal_year/', templatetrimesters=TemplateTrimester.objects.all(),
                 templatetrimester_form=TemplateTrimesterForm(), templatetrimester_url='/utils/add_model_trimester/')
    return render(request, 'utils.tpl', c)


def add_model_trimester(request):
    form = TemplateTrimesterForm(request.POST)
    if form.is_valid():
        form.save()
        c = dict(fiscalyears=FiscalYear.objects.all(), fiscalyear_form=FiscalYearForm(), templatetrimester_return=True,
                 fiscalyear_url='/utils/add_fiscal_year/', templatetrimesters=TemplateTrimester.objects.all(),
                 templatetrimester_form=TemplateTrimesterForm(), templatetrimester_url='/utils/add_model_trimester/')
    else:
        c = dict(fiscalyears=FiscalYear.objects.all(), fiscalyear_form=FiscalYearForm,
                 fiscalyear_url='/utils/add_fiscal_year/', templatetrimesters=TemplateTrimester.objects.all(),
                 templatetrimester_form=form, templatetrimester_url='/utils/add_model_trimester/')
    return render(request, 'utils.tpl', c)


def add_trimesters(request):
    tt = TemplateTrimester.objects.get(favorite=True)
    for com in Company.objects.all():
        year_new, created = com.years.get_or_create(fiscal_year=tt.year, active=True, refer_company=com, favorite=True)
        if created:
            for year_old in com.years.filter(favorite=True):
                if year_old.id is not year_new.id:
                    year_old.favorite = False
                    year_old.save()
            com.add_year(year_new)
        trim_new, created = Trimester.objects.get_or_create(template=tt, start_date=tt.start_date, active=True,
                                                            refer_year=year_new, favorite=True)
        if created:
            for trim_old in year_new.trimesters.filter(favorite=True):
                if trim_old is not trim_new:
                    trim_old.favorite = False
                    trim_old.save()
            year_new.add_trimester(trim_new)
        trim_new.add_categories()
        # for cat in com.model_trimester.categories.all().order_by('priority'):
        #     cat_new, created = Category.objects.get_or_create(cat=cat, refer_trimester=trim_new, active=True)
        #    if created:
        #        trim_new.add_trimester(cat_new)

    c = dict(fiscalyears=FiscalYear.objects.all(), fiscalyear_form=FiscalYearForm, trimesters_return=True,
             fiscalyear_url='/utils/add_fiscal_year/', templatetrimesters=TemplateTrimester.objects.all(),
             templatetrimester_form=TemplateTrimesterForm, templatetrimester_url='/utils/add_model_trimester/')
    return render(request, 'utils.tpl', c)


def custom_403(request):
    return render(request, "403.tpl")


def custom_404(request):
    return render(request, "404.tpl")


def custom_500(request):
    return render(request, "500.tpl")
