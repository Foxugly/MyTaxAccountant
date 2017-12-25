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
from companies.views import *


urlpatterns = (
    url(r'^(?P<company_id>[0-9]+)/list/$', login_required(list_year), name='list_year'),
    url(r'^(?P<company_id>[0-9]+)/$', login_required(company_view), name='company_view'),
    url(r'^$', login_required(admin_companies), name='companies'),
    url(r'^add/$', login_required(add_company), name='add_company'),
    url(r'^ajax/update/(?P<company_id>[0-9]+)/$', login_required(update_company), name='update_company'),
)
