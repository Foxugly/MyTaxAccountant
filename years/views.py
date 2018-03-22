# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from years.models import Year
import json
import logging


logger = logging.getLogger(__name__)
logger.setLevel(settings.LOGGER)


def favorite_trimester(year):
    logger.debug("favorite_trimester | year = %s" % year)
    t = year.trimesters.filter(active=True, favorite=True)
    if not t:
        t = [year.trimesters.filter(active=True)[0]]
    return t[0]


#def year_view(request, year_id):
#    return HttpResponse("year_view")


def list_trimesters(request, year_id):
    logger.debug("list_trimesters | year_id = %d" % year_id)
    if request.is_ajax():
        y = get_object_or_404(Year, id=year_id)
        if request.user.is_superuser:
            results = {'list': [t.as_json() for t in y.trimesters.filter(active=True).order_by('template__number')],
                       'return': True, 'favorite': favorite_trimester(y).as_json()}
        else:
            results = {'list': [t.as_json() for t in y.trimesters.filter(active=True).order_by('template__number')],
                       'return': True, 'favorite': favorite_trimester(y).as_json()}
        return HttpResponse(json.dumps(results))


def forward_trimester(request, year_id):
    logger.debug("forward_trimester | year_id = %d" % year_id)
    if request.is_ajax():
        y = get_object_or_404(Year, id=year_id)
        c = y.get_favorite_trimester().get_favorite_category()
        if c:
            return HttpResponse(json.dumps({'forward': c.get_url()}))
        else:
            return HttpResponse(json.dumps({'forward': None}))
