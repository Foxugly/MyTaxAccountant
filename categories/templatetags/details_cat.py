# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU Affero General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or (at 
# your option) any later version.

from django import template
from categories.models import Category


register = template.Library()


@register.filter()
def len_docs(category):
    return len(category.documents.all())

