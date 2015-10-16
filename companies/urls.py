# Copyright 2015, foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU Affero General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or (at 
# your option) any later version.

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from companies.views import *


urlpatterns = patterns('companies.views',
	url(r'^(?P<company_id>[0-9]+)/list/$', login_required(list_year), name='list_year'),
    url(r'^(?P<company_id>[0-9]+)/$', login_required(company_view), name='company_view'),
)
