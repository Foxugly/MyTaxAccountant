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
			result['img'] += '<img style="max-width:100%;" src="' + p.filename + '" />'
		print result
		return HttpResponse(json.dumps(result))