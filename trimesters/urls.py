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
from trimesters.views import list_categories, admin_trimesters, view_trimester


urlpatterns = (
    url(r'^(?P<trimester_id>[0-9]+)/list/$', login_required(list_categories), name='list_categories'),
    url(r'^(?P<trimester_id>[0-9]+)/$', login_required(view_trimester), name='view_trimester'),
    url(r'^$', login_required(admin_trimesters), name='trimesters'),
)
