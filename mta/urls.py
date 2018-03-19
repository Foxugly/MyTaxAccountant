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
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.conf.urls.static import static
from utils.views import lang
from django.contrib.auth.decorators import login_required
from users.views import home
from django.urls import path
from categories.tasks import add

admin.autodiscover()


def test(request):
    return render(request, "test.tpl")


def addition(request, a , b):
    return HttpResponse("Result = %s" % add.delay(a, b))


urlpatterns = [
    path('', login_required(home)),
    path('lang/', lang),
    path('test/', test),
    path('celery/<int:a>/<int:b>/', addition),
    path('admin/webshell/', include('webshell.urls')),
    path('admin/', admin.site.urls),
    path('category/', include('categories.urls')),
    path('company/', include('companies.urls')),
    path('document/', include('documents.urls')),
    path('hijack/', include('hijack.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('upload/', include('fileupload.urls')),
    path('user/', include('users.urls')),
    path('utils/', include('utils.urls')),
    path('trimester/', include('trimesters.urls')),
    path('year/', include('years.urls'))
              ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = 'utils.views.custom_403'
handler404 = 'utils.views.custom_404'
handler500 = 'utils.views.custom_500'
