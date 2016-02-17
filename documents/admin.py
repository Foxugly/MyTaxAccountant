# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.contrib import admin
from documents.models import Document, Page


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    filter_horizontal = ('pages',)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass