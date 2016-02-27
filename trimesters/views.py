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
from categories.models import Category
import json


def trimester_view(request, trimester_id):
    u = UserProfile.objects.get(user=request.user)
    t = Trimester.objects.get(id=trimester_id)
    y = t.refer_year
    c = y.refer_company
    return render_to_response('folder.tpl', {'userprofile': u, 'trimester': t, 'year': y, 'company': c})


def list_categories(request, trimester_id, cat_id):
    if request.is_ajax():
        t = Trimester.objects.get(id=trimester_id)
        result = {}
        nav_list = []
        doc_list = []
        for c in t.categories.filter(active=True).order_by('cat__priority'):
            nav_list.append(c.as_json())
        result['nav_list'] = nav_list
        if int(cat_id) is not 0:
            c = Category.objects.get(pk=int(cat_id))
        else:
            c = t.categories.filter(active=True).order_by('cat__priority')[0]
        first = True
        if c.count_docs() > 0:
            for d in c.get_docs():
                if first:
                    if request.user.is_superuser:
                        form = DocumentAdminForm(instance=d)
                    else:
                        if d.lock:
                            form = DocumentReadOnlyForm(instance=d)
                        else:
                            form = DocumentForm(instance=d)
                    result['img'] = d.as_img()
                    result['form'] = form.as_div()
                    result['doc_id'] = d.id
                    result['fiscal_id'] = d.fiscal_id
                    result['lock'] = d.lock
                    result['valid'] = True
                    first = False
                doc_list.append(d.as_json())
        else:
            result['img'] = None
            result['form'] = None
            result['doc_id'] = 0
            result['valid'] = False
        result['title_trimester'] = str(t)
        result['doc_list'] = doc_list
        return HttpResponse(json.dumps(result))


def list_categorie_n(request, trimester_id, num):  # num = [1,4]
    if request.is_ajax():
        t = Trimester.objects.get(id=trimester_id)
        results = {}
        data = []
        c = t.categories.filter(active=True).order_by('cat__priority')[int(num)-1]
        for d in c.get_docs():
            data.append(d.as_json())
        results['doc_list'] = data
        results['n'] = c.count_docs()
        return HttpResponse(json.dumps(results))
