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
from utils.views import admin_utils, add_fiscal_year, add_model_trimester, add_trimesters


urlpatterns = (
    path('', login_required(admin_utils), name='utils'),
    path('add_fiscal_year/', login_required(add_fiscal_year), name='add_fiscal_year'),
    path('add_model_trimester/', login_required(add_model_trimester), name='add_model_trimester'),
    path('add_trimesters/', login_required(add_trimesters), name='add_trimesters'),
)
