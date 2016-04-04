# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.shortcuts import render_to_response
from django.http import HttpResponse
from users.models import UserProfile
from trimesters.models import Trimester
from documents.models import DocumentForm, DocumentAdminForm, DocumentReadOnlyForm
import json


def favorite_trimester(year):
    t = year.trimesters.filter(active=True, favorite=True)
    if not t:
        t = [year.trimesters.filter(active=True)[0]]
    return t[0]


def list_categories(request, trimester_id):
    if request.is_ajax():
        t = Trimester.objects.get(id=trimester_id)
        result = {}
        nav_list = []
        for c in t.categories.filter(active=True).order_by('cat__priority'):
            nav_list.append(c.as_json())
        result['nav_list'] = nav_list
        result['title_trimester'] = str(t)
        return HttpResponse(json.dumps(result))


def admin_trimesters(request):
    return HttpResponse("admin_trimesters")
