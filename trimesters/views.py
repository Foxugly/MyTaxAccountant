from django.shortcuts import render_to_response
from django.http import HttpResponse
from users.models import UserProfile
from trimesters.models import Trimester
import json

def trimester_view(request, trimester_id):
    u = UserProfile.objects.get(user=request.user)
    t = Trimester.objects.get(id=trimester_id)
    y = t.refer_year
    c = y.refer_company
    return render_to_response('folder.tpl', {'userprofile' : u, 'trimester' : t, 'year': y,'company': c})


def list_categories(request, trimester_id):
	if request.is_ajax():
		t = Trimester.objects.get(id=trimester_id)
		result = {}
		nav_list = []
		doc_list = []
		for c in t.categories.filter(active=True).order_by('cat__priority'):
			nav_list.append(c.as_json())
		result['nav_list'] = nav_list
		c = t.categories.filter(active=True).order_by('cat__priority')[:1]
		for d in c[0].get_docs():
			doc_list.append(d.as_json())
		result['doc_list'] = doc_list
		return HttpResponse(json.dumps(result))
