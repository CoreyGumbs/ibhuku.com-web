#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .base import *

# Quick-start development settings - unsuitable for production
DEBUG = True


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('db_NAME'),
        'USER': get_secret('db_USER'),
        'PASSWORD': get_secret('db_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')