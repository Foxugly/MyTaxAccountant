# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.


"""MyTaxAccountant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.shortcuts import redirect, render, render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from os.path import dirname, abspath, join
from utils.perms import get_context



def home(request):
    if request.user.is_authenticated():
        return render_to_response('folder.tpl', get_context(request))
    return render(request, "layout.tpl")

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('users.urls'), name='users'),
    url(r'^company/', include('companies.urls'), name='companies'),
    url(r'^year/', include('years.urls'), name='years'),
    url(r'^document/', include('documents.urls'), name='documents'),
    url(r'^trimester/', include('trimesters.urls'), name='trimesters'),
    url(r'^category/', include('categories.urls'), name='categories'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^upload/', include('fileupload.urls')),
    url(r'^$', home, name='index'),
] + patterns('',(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)