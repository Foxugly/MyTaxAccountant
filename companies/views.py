# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
from users.models import UserProfile
from companies.models import Company

def company_view(request, company_id):
    userprofile = UserProfile.objects.get(user=request.user)
    return render_to_response('folder.tpl', {'userprofile' : userprofile})

def list_year(request, company_id):
	if request.is_ajax():
		c = Company.objects.get(id=company_id)
		results = [y.as_json() for y in c.years.filter(active=True)]
		return HttpResponse(json.dumps(results))