from django.shortcuts import render, render_to_response
from django.http import HttpResponse
# Create your views here.
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