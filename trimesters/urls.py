# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from trimesters.views import list_categories, view_trimester, forward_category


urlpatterns = (
    url(r'^(?P<tri_id>[0-9]+)/forward/$', login_required(forward_category), name='forward_category'),
    url(r'^(?P<trir_id>[0-9]+)/list/$', login_required(list_categories), name='list_categories'),
    url(r'^(?P<tri_id>[0-9]+)/$', login_required(view_trimester), name='view_trimester'),
)
