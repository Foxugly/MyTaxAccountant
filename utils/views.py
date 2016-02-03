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
