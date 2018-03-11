# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later veron.


from django.http import HttpResponse
from django.shortcuts import redirect
from trimesters.models import Trimester
import json
from django.conf import settings


def view_trimester(request, trimester_id):
    if settings.DEBUG:
        print("view_trimester | id = %d" % trimester_id)
    t = Trimester.objects.get(id=trimester_id)
    cat = t.categories.filter(active=True).order_by('cat__priority')[0].id
    return redirect('/category/%s/' % cat)


def favorite_trimester(year):
    if settings.DEBUG:
        print("favorite_trimester")
    t = year.trimesters.filter(active=True, favorite=True)
    if not t:
        t = [year.trimesters.filter(active=True)[0]]
    return t[0]


def list_categories(request, trimester_id):
    if settings.DEBUG:
        print("list_categories")
    if request.is_ajax():
        t = Trimester.objects.get(id=trimester_id)
        result = {}
        nav_list = []
        for c in t.categories.filter(active=True).order_by('cat__priority'):
            nav_list.append(c.as_json())
        result['nav_list'] = nav_list
        result['title_trimester'] = str(t)
        return HttpResponse(json.dumps(result))


def forward_categorie(request, trimester_id):
    if settings.DEBUG:
        print("forward_categorie")
    if request.is_ajax():
        t = Trimester.objects.get(id=trimester_id)
        url_cat = t.get_favorite_category_url()
        return HttpResponse(json.dumps({'forward': url_cat}))
