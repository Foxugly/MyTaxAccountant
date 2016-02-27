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
from documents.views import document_view, update_ajax, ajax_move, ajax_merge, ajax_split, ajax_move_doc

urlpatterns = patterns('documents.views',
                       # url(r'^update/$', login_required(update_ajax), name='document_update_ajax'),
                       url(r'^(?P<document_id>[0-9]+)/update/$', login_required(update_ajax),
                           name='document_update_ajax'),
                       url(r'^(?P<document_id>[0-9]+)/$', login_required(document_view), name='document_view'),
                       url(r'^ajax/move/(?P<n>[0-9]+)/$', login_required(ajax_move), name='ajax_move_modal'),
                       url(r'^ajax/move/(?P<doc_id>[0-9]+)/(?P<cat_id>[0-9]+)/$', login_required(ajax_move_doc), name='ajax_move'),
                       url(r'^ajax/merge/(?P<n>[0-9]+)/$', login_required(ajax_merge), name='ajax_merge_modal'),
                       url(r'^ajax/split/(?P<n>[0-9]+)/$', login_required(ajax_split), name='ajax_split_modal'),
                       )
