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
from categories.views import category_view, add_documents, list_documents, form_document

urlpatterns = patterns('categories.views',
                       url(r'^(?P<category_id>[0-9]+)/add_documents/$', login_required(add_documents),
                           name='add_documents'),
                       url(r'^(?P<category_id>[0-9]+)/list/(?P<n>[0-9]+)/$', login_required(list_documents),
                           name='list_documents'),
                       url(r'^(?P<category_id>[0-9]+)/form/(?P<n>[0-9]+)/$', login_required(form_document),
                           name='list_documents'),
                       url(r'^(?P<category_id>[0-9]+)/$', login_required(category_view), name='category_view'),
                       )
