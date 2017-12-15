# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.contrib import admin
from companies.models import Company, ModelTrimester


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    filter_horizontal = ('years',)


@admin.register(ModelTrimester)
class ModelTrimesterAdmin(admin.ModelAdmin):
    filter_horizontal = ('categories',)

