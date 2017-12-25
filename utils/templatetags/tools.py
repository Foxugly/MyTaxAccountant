# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django import template
register = template.Library()


@register.filter()
def id(inst):
    return inst[0].id


@register.filter()
def current_trimester(inst):
    try:
        return inst.years.filter(favorite=True)[0].trimesters.filter(favorite=True)[0]
    except:
        return '<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>'
