# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
import json
from users.models import UserForm, UserProfileForm
# Create your views here.


def home(request):
    if request.user.is_authenticated():
        return render(request, 'folder.tpl')
    return render(request, "layout.tpl")


@login_required
def user_settings(request):
    c = {'user_form': UserForm(instance=request.user),
         'userprofile_form': UserProfileForm(instance=request.user.userprofile),
         'password_change_form': PasswordChangeForm(user=request.user)}
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
            results['errors'] = userprofile_form.errors + user_form.errors
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
