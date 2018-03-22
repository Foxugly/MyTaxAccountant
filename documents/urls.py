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
from documents.views import *


urlpatterns = (
    path('<int:doc_id>/update/', login_required(update_ajax), name='document_update_ajax'),
    path('<int:doc_id>/', login_required(document_view), name='document_view'),
    path('ajax/move/<int:doc_id>/', login_required(ajax_move), name='ajax_move_modal'),
    path('ajax/move/<int:doc_id>/<int:cat_id>/', login_required(ajax_move_doc), name='ajax_move'),
    path('ajax/merge/<int:doc_id>/', login_required(ajax_merge), name='ajax_merge_modal'),
    path('ajax/download/<int:doc_id>/', login_required(ajax_download), name='ajax_download'),
    path('ajax/split/<int:doc_id>/', login_required(ajax_split), name='ajax_split_modal'),
    path('ajax/img/<int:doc_id>/<int:num>/', login_required(ajax_img), name='ajax_img'),
    path('ajax/delete/<int:doc_id>/', login_required(ajax_delete), name='ajax_delete'),
    path('split/', login_required(split_doc), name='doc_split'),
    path('merge/', login_required(merge_doc), name='doc_merge'),
    path('ajax/multiple_move/<int:cat_id>/', login_required(ajax_multiple_move), name='multiple_move'),
    path('ajax/multiple_delete/', login_required(ajax_multiple_delete), name='multiple_delete'),
    path('ajax/multiple_download/', login_required(ajax_multiple_download), name='multiple_download'),
    path('view/<int:doc_id>/', login_required(view), name='view'),
)
