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
from fileupload.views import FileUploadCreateView, FileUploadDeleteView, FileUploadListView , remove_upload


urlpatterns = (
    url(r'^basic/$', FileUploadCreateView.as_view(), name='upload-basic'),
    url(r'^new/$', FileUploadCreateView.as_view(), name='upload-new'),
    url(r'^delete/(?P<pk>\d+)$', FileUploadDeleteView.as_view(), name='upload-delete'),
    url(r'^view/$', FileUploadListView.as_view(), name='upload-view'),
    url(r'^remove/(?P<fileupload_id>[0-9]+)/$', login_required(remove_upload), name='remove_upload'),
)
