# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django import template
from users.models import UserProfile


register = template.Library()

@register.filter()
def companies(userprofile):
    return userprofile.companies.filter(active=True)

@register.filter()
def favorite_company(userprofile):
    out = None
    first = True
    for c in userprofile.companies.filter(active=True):
        if first :
            out = c
            first = False
        if c.favorite :
            out = c
    return out

@register.filter()
def years(company):
    return company[0].years.filter(active=True)

@register.filter()
def favorite_year(company):
    out = None
    first = True
    for c in company[0].years.filter(active=True):
        if first :
            out = c
            first = False
        if c.favorite :
            out = c
    return out

@register.filter()
def trimesters(year):
    return year[0].trimesters.filter(active=True)

@register.filter()
def favorite_trimester(year):
    out = None
    first = True
    for y in year[0].trimesters.filter(active=True):
        if first :
            out = y
            first = False
        if y.favorite :
            out = y
    return out

@register.filter()
def categories(trimester):
    return trimester[0].categories.filter(active=True)

@register.filter()
def documents(category):
    return category[0].documents.all()

@register.filter()
def name(inst):
    return inst.get_name()