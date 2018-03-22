# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.urls import path
from django.contrib.auth.decorators import login_required
from companies.views import *

urlpatterns = (
    path('<int:company_id>/forward/', login_required(forward_year), name='forward_year'),
    path('<int:company_id>/list/', login_required(list_year), name='list_year'),
    path('<int:company_id>/', login_required(company_view), name='company_view'),
    path('', login_required(admin_companies), name='companies'),
    path('add/', login_required(add_company), name='add_company'),
    path('ajax/update/<int:company_id>/', login_required(update_company), name='update_company'),
)
