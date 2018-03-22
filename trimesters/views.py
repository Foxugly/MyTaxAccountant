# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later veron.


from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from trimesters.models import Trimester
import json
from django.conf import settings
import logging


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOGGER)


def view_trimester(request, tri_id):
    logger.debug("view_trimester | id = %d" % tri_id)
    t = get_object_or_404(Trimester, id=tri_id)
    return redirect('/category/%s/' % t.categories.filter(active=True).order_by('cat__priority')[0].id)


def favorite_trimester(year):
    logger.debug("favorite_trimester | year = %s" % year)
    t = year.trimesters.filter(active=True, favorite=True)
    if not t:
        t = [year.trimesters.filter(active=True)[0]]
    return t[0]


def list_categories(request, tri_id):
    logger.debug("list_categories | tri_id = %d" % tri_id)
    if request.is_ajax():
        t = get_object_or_404(Trimester, id=tri_id)
        result = {}
        nav_list = []
        for c in t.categories.filter(active=True).order_by('cat__priority'):
            nav_list.append(c.as_json())
        result['nav_list'] = nav_list
        result['title_trimester'] = str(t)
        return HttpResponse(json.dumps(result))


def forward_category(request, tri_id):
    logger.debug("forward_category | tri_id =  %d" % tri_id)
    if request.is_ajax():
        t = get_object_or_404(Trimester, id=tri_id)
        return HttpResponse(json.dumps({'forward': t.get_favorite_category_url()}))
