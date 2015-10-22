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
from documents.models import Document, DocumentAdminForm, DocumentForm
import json

def document_view(request, document_id):
	if request.is_ajax():
		d = Document.objects.get(id=document_id)
		result = {}
		result['name'] = d.name
		result['img'] = ''
		for p in d.pages.all().order_by('num'):
			result['img'] += '<img style="max-width:100%;" src="' + str(p.get_relative_path()) + '" />'
		return HttpResponse(json.dumps(result))

def update_ajax(request, document_id):
	if request.is_ajax():
		doc = Document.objects.get(id=document_id)
		form = None
		if request.user.is_superuser:
			form = DocumentAdminForm(request.GET,instance=doc)
		else:
			form = DocumentForm(request.GET,instance=doc)
		if form.is_valid():
			form.save()
			return HttpResponse(json.dumps('OK'))
		else :
			return HttpResponse(json.dumps('ERROR'))
