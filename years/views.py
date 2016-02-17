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


def year_view(request, year_id):
    return HttpResponse("year_view")


def list_trimister(request, year_id):
    if request.is_ajax():
        y = Year.objects.get(id=year_id)
        results = [t.as_json() for t in y.trimesters.filter(active=True)]
        return HttpResponse(json.dumps(results))
