# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.http import HttpResponse
from years.models import Year
import json


def favorite_trimester(year):
    t = year.trimesters.filter(active=True, favorite=True)
    if not t:
        t = [year.trimesters.filter(active=True)[0]]
    return t[0]


def year_view(request, year_id):
    return HttpResponse("year_view")


def list_trimester(request, year_id):
    if request.is_ajax():
        y = Year.objects.get(id=year_id)
        if request.user.is_superuser:
            results = {'list': [t.as_json() for t in y.trimesters.filter(active=True).order_by('template__number')],
                       'return': True, 'favorite': favorite_trimester(y).as_json()}
        else:
            results = {'list': [t.as_json() for t in y.trimesters.filter(active=True).order_by('template__number')],
                       'return': True, 'favorite': favorite_trimester(y).as_json()}
        return HttpResponse(json.dumps(results))

