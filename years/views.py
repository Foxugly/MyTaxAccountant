from django.shortcuts import render
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