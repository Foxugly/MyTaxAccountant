from django.shortcuts import render_to_response
from django.http import HttpResponse
from users.models import UserProfile
from trimesters.models import Trimester

def trimester_view(request, trimester_id):
    u = UserProfile.objects.get(user=request.user)
    t = Trimester.objects.get(id=trimester_id)
    y = t.refer_year
    c = y.refer_company
    return render_to_response('folder.tpl', {'userprofile' : u, 'trimester' : t, 'year': y,'company': c})


