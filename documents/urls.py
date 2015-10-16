# Copyright 2015, foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU Affero General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or (at 
# your option) any later version.

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from documents.views import document_view



urlpatterns = patterns('documents.views',
    url(r'^(?P<document_id>[0-9]+)/$', login_required(document_view), name='document_view'),
)
