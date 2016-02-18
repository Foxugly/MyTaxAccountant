# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from trimesters.views import trimester_view, list_categories, list_categorie_n


urlpatterns = patterns('trimesters.views',
    url(r'^(?P<trimester_id>[0-9]+)/list/$', login_required(list_categories), name='list_categories'),
    url(r'^(?P<trimester_id>[0-9]+)/category_n/(?P<num>[0-9]+)/$', login_required(list_categorie_n), name='list_categorie_n'),
    url(r'^(?P<trimester_id>[0-9]+)/$', login_required(trimester_view), name='trimester_view'),
)
