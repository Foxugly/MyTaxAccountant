# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.urls import path
from fileupload.views import FileUploadCreateView, FileUploadDeleteView, FileUploadListView, remove_upload


urlpatterns = (
    path('', FileUploadCreateView.as_view(), name='upload-basic1'),
    path('basic/', FileUploadCreateView.as_view(), name='upload-basic'),
    path('new/', FileUploadCreateView.as_view(), name='upload-new'),
    path('delete/<int:pk>/', FileUploadDeleteView.as_view(), name='upload-delete'),
    path('view/', FileUploadListView.as_view(), name='upload-view'),
    path('remove/<int:fileupload_id>/', remove_upload, name='remove_upload'),
)
