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
def companies(user):
    return user.userprofile.companies.filter(active=True)


@register.filter()
def favorite_company(user):
    c = user.userprofile.companies.filter(active=True, favorite=True)
    if not c:
        c = [user.userprofile.companies.filter(active=True)[0]]
    return c[0]


@register.filter()
def years(company):
    return company.years.filter(active=True)


@register.filter()
def favorite_year(company):
    y = company.years.filter(active=True, favorite=True)
    if not y:
        y = [company.years.filter(active=True)[0]]
    return y[0]


@register.filter()
def trimesters(year):
    return year.trimesters.filter(active=True)


@register.filter()
def favorite_trimester(year):
    t = year.trimesters.filter(active=True, favorite=True)
    if not t:
        t = [year.trimesters.filter(active=True)[0]]
    return t[0]


@register.filter()
def categories(trimester):
    return trimester.categories.filter(active=True)


@register.filter()
def documents(category):
    return category.documents.all()


@register.filter()
def name(inst):
    return inst.get_name()
