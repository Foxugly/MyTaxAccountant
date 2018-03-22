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
from categories.views import add_documents, list_documents, view_form, view_category

urlpatterns = (
    path('<int:cat_id>/add_documents/$', login_required(add_documents), name='add_documents'),
    path('<int:cat_id>/list/<int:n>/$', login_required(list_documents), name='list_documents'),
    path('<int:cat_id>/form/<int:field>/<sens>/<int:n>/$', login_required(view_form), name='view_forms'),
    path('<int:cat_id>+)/$', login_required(view_category), name='view_category'),
)
