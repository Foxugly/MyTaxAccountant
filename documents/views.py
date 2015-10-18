# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.shortcuts import render
from django.http import HttpResponse
from documents.models import Document
import json

def document_view(request, document_id):
	if request.is_ajax():
		d = Document.objects.get(id=document_id)
		result = {}
		result['name'] = d.name
		result['img'] = ''
		for p in d.pages.order_by('num'):
			result['img'] += '<img style="max-width:100%;" src="' + p.get_relative_path() + '" />'
		return HttpResponse(json.dumps(result))