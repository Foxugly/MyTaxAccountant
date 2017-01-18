# -*- coding: utf-8 -*-
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

from django.utils.translation import ugettext_lazy as _
import socket
"""
Django settings for MyTaxAccountant project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-b+&3%*nxun2l+id*85aou#vpkw%uhd3ko&b06jmkr#ke)6k3k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'companies',
    'years',
    'trimesters',
    'categories',
    'documents',
    'utils',
    'users',
    'fileupload'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

UPLOAD_LOG = '/tmp/upload_log'

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Brussels'
USE_I18N = True
USE_L10N = True
USE_TZ = True
AUTH_PROFILE_MODULE = 'users.UserProfile'
LOGIN_REDIRECT_URL = '/user/'
LOGIN_URL = '/user/login/'

LANGUAGES = (
  ('fr', _('Francais')),
  ('nl', _('Nederlands')),
  ('en', _('English')),
)

DEFAULT_LANGUAGE = 1

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
UPLOAD_DIR = 'upload'
STOCK_DIR = 'folders'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
TMP_ROOT = MEDIA_ROOT + '/tmp/'
TMP_URL = MEDIA_URL + 'tmp/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.core.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
