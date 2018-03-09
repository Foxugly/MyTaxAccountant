# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from users.views import user_settings, personal_data, password, treeview
from django.contrib.auth import views as auth_views

#urlpatterns = (
    #url(r'^ajax/personal_data/$', login_required(personal_data)),
    #url(r'^ajax/password/$', login_required(password)),
    #url(r'^settings/$', login_required(user_settings)),
#    path('login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    #url(r'^login/$', auth_views.LoginView.as_view(template_name='login.tpl'), name='login'),
    #url(r'^treeview/$', login_required(treeview)),
    #url(r'^logout/$', login_required(auth_views.LogoutView.as_view(template_name='logout.tpl')), name='logout'),
    #url(r'^password_change/$', login_required(views.password_change)),
    #url(r'^password_change/done/$', login_required(views.password_change_done)),
    #url(r'^password_reset/$', login_required(views.password_reset)),
    #url(r'^password_reset/done/$', login_required(views.password_reset_done)),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    login_required(views.password_reset_confirm)),
    #url(r'^reset/done/$', login_required(views.password_reset_complete)),
#)

urlpatterns = (
    url(r'^ajax/personal_data/$', login_required(personal_data), name="personal_data"),
    url(r'^ajax/password/$', login_required(password), name='password'),
    url(r'^settings/$', login_required(user_settings), name='settings'),
    path('login/', auth_views.LoginView.as_view(template_name='login.tpl'), name='login'),
    path('treeview/', login_required(treeview), name='treeview'),
    path('logout/', login_required(auth_views.LogoutView.as_view(template_name='logout.tpl')), name='logout'),
    url(r'^password_change/$', login_required(views.password_change), name='password_change'),
    url(r'^password_change/done/$', login_required(views.password_change_done), name='password_change_done'),
    url(r'^password_reset/$', login_required(views.password_reset), name='password_reset'),
    url(r'^password_reset/done/$', login_required(views.password_reset_done), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        login_required(views.password_reset_confirm), name='password_reset_confirm'),
    url(r'^reset/done/$', login_required(views.password_reset_complete), name='password_reset_complete'),
)