# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from users.models import UserProfile
from companies.models import Company
from years.models import Year
from trimesters.models import Trimester
from categories.models import Category, TypeCategory
from documents.models import Document

from utils.models import FiscalYear

def get_context(request):
    c = {}
    c['userprofile'] = UserProfile.objects.get(user=request.user)
    c['type_doc'] = TypeCategory.objects.filter(active=True).order_by('priority')
    return c