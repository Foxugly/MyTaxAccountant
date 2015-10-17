# Copyright 2015, foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU Affero General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or (at 
# your option) any later version.

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from trimesters.views import trimester_view, list_categories


urlpatterns = patterns('trimesters.views',
    url(r'^(?P<trimester_id>[0-9]+)/list_categories/$', login_required(list_categories), name='list_categories'),
    url(r'^(?P<trimester_id>[0-9]+)/$', login_required(trimester_view), name='trimester_view'),
)
