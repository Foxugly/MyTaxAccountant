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
from documents.views import document_view, update_ajax, ajax_move, ajax_merge, ajax_split, ajax_move_doc, ajax_delete, \
    ajax_img, split_doc, merge_doc, ajax_download, ajax_multiple_move, ajax_multiple_delete, ajax_multiple_download

urlpatterns = (
    # url(r'^update/$', login_required(update_ajax), name='document_update_ajax'),
    url(r'^(?P<document_id>[0-9]+)/update/$', login_required(update_ajax), name='document_update_ajax'),
    url(r'^(?P<document_id>[0-9]+)/$', login_required(document_view), name='document_view'),
    url(r'^ajax/move/(?P<n>[0-9]+)/$', login_required(ajax_move), name='ajax_move_modal'),
    url(r'^ajax/move/(?P<doc_id>[0-9]+)/(?P<cat_id>[0-9]+)/$', login_required(ajax_move_doc), name='ajax_move'),
    url(r'^ajax/merge/(?P<n>[0-9]+)/$', login_required(ajax_merge), name='ajax_merge_modal'),
    url(r'^ajax/download/(?P<n>[0-9]+)/$', login_required(ajax_download), name='ajax_download'),
    url(r'^ajax/split/(?P<n>[0-9]+)/$', login_required(ajax_split), name='ajax_split_modal'),
    url(r'^ajax/img/(?P<doc_id>[0-9]+)/(?P<num>[0-9]+)/$', login_required(ajax_img), name='ajax_img'),
    url(r'^ajax/delete/(?P<doc_id>[0-9]+)/$', login_required(ajax_delete), name='ajax_delete'),
    url(r'^split/$', login_required(split_doc), name='doc_split'),
    url(r'^merge/$', login_required(merge_doc), name='doc_merge'),
    url(r'^ajax/multiple_move/(?P<cat_id>[0-9]+)/$', login_required(ajax_multiple_move), name='multiple_move'),
    url(r'^ajax/multiple_delete/$', login_required(ajax_multiple_delete), name='multiple_delete'),
    url(r'^ajax/multiple_download/$', login_required(ajax_multiple_download), name='multiple_download'),
)
