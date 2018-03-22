# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from companies.models import Company
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.core.validators import RegexValidator
from fileupload.models import FileUpload
from categories.models import Category
from django.utils import timezone


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kw):
        new_kw = {}
        super(UserCreateForm, self).__init__(*args, **new_kw)
        if len(kw):
            for key, val in kw.items():
                self.fields[key].initial = val


class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_('user'), on_delete=models.CASCADE)
    language = models.CharField(verbose_name=_(u'language'), max_length=8, choices=settings.LANGUAGES, default=1)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_(
        "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=16)  # validators should be a list
    birth_date = models.DateField(blank=True, null=True)
    companies = models.ManyToManyField(Company, verbose_name=_('companies'), blank=True)

    def get_favorites(self):
        c = self.companies.get(active=True, favorite=True)
        y = c.years.get(active=True, favorite=True)
        t = y.trimesters.get(active=True, favorite=True)
        return t

    def __str__(self):
        return self.user.username

    def real_name(self):
        return self.user.first_name + " " + self.user.last_name

    def add_company(self, company):
        self.companies.add(company)

    def get_companies(self):
        return self.companies.all().order_by('name')


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u, language=settings.LANGUAGES[0])[0])


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserProfileForm(ModelForm):
    n = 'userprofileform'

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'birth_date', 'language']
        help_texts = {
            'phone_number': _(
        "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
        }

    def __init__(self, *args, **kw):
        super(UserProfileForm, self).__init__(*args, **kw)
        self.fields['language'].widget.attrs['class'] = 'select2100-nosearch'
        self.fields['birth_date'].widget.attrs['class'] = 'datepicker'


class UserProfileCreateForm(ModelForm):
    n = 'userprofileform'

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'birth_date', 'language']
        help_texts = {
            'phone_number': _(
        "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
        }

    def __init__(self, *args, **kw):
        super(ModelForm, self).__init__(*args, **kw)
        self.fields['language'].widget.attrs['class'] = 'select2100-nosearch'
        self.fields['birth_date'].widget.attrs['class'] = 'datepicker'


class Log(models.Model):
    userprofile = models.ForeignKey(UserProfile, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField(_('date'), default=timezone.now, null=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    cmd = models.TextField(null=True)

    def __str__(self):
        return "%i" % self.pk
