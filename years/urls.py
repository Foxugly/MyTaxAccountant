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
from years.views import *


urlpatterns = patterns('categories.views',
	url(r'^(?P<year_id>[0-9]+)/list/$', login_required(list_trimister), name='list_trimister'),
    url(r'^(?P<year_id>[0-9]+)/$', login_required(year_view), name='year_view'),
)
