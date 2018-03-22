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
from years.views import list_trimesters, year_view, forward_trimester


urlpatterns = (
    path('<int:year_id>/forward/', login_required(forward_trimester), name='forward_trimister'),
    path('<int:year_id>/list/', login_required(list_trimesters), name='list_trimisters'),
    path('<int:year_id>/', login_required(year_view), name='year_view'),
)
