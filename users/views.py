# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.core import serializers
from users.models import UserForm, UserProfileForm
from companies.models import CompanyForm, Company
import json
# Create your views here.


def home(request):
    c = {}
    if request.user.is_authenticated:
        companies = request.user.userprofile.companies.all()
        company_current = companies[0]
        if request.user.is_staff:
            years = company_current.get_active_years()
        else:
            years = company_current.get_years()
        year_current = next(y for y in years if y.favorite is True)
        if request.user.is_staff:
            trimesters = year_current.get_active_trimesters()
        else:
            trimesters = year_current.get_trimesters()
        trimester_current = next(t for t in trimesters if t.favorite is True)
        categories = trimester_current.get_categories()
        cat = categories[0]
        return redirect('/category/%s/' % cat.id)
    return render(request, "layout.tpl", c)


@login_required
def treeview(request):
    context = {}
    sum_json = []
    for c in Company.objects.all():
        n, c_json = c.treeview_favorite()
        if n:
            sum_json.append(json.dumps(c_json))
    context['tree'] = sum_json

    return render(request, "treeview.tpl", context)

@login_required
def user_settings(request):
    companies = request.user.userprofile.companies.all()
    companiesform = [(c.id, CompanyForm(instance=c)) for c in companies]
    c = {'user_form': UserForm(instance=request.user),
         'userprofile_form': UserProfileForm(instance=request.user.userprofile),
         'password_change_form': PasswordChangeForm(user=request.user), 'companies': companies,
         'companiesForm': companiesform
         }
    return render(request, 'config.tpl', c)


@login_required
def personal_data(request):
    results = {}
    if request.is_ajax():
        user_form = UserForm(request.POST, instance=request.user)
        userprofile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and userprofile_form.is_valid():
            user_form.save()
            userprofile_form.save()
            results['return'] = True
        else:
            combo = userprofile_form.errors
            combo.update(user_form.errors)
            results['errors'] = combo
            results['return'] = False
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))


@login_required
def password(request):
    results = {}
    if request.is_ajax():
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            results['return'] = True
        else:
            results['errors'] = form.errors
            results['return'] = False
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))
