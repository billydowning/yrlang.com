import os

from .base import *


DEBUG = False
ALLOWED_HOSTS = ['18.216.99.152', 'yrlang.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'yrlang2020',
        'USER': 'postgres',  # Do not change. Create a separate settings file for local dev if needs to be different
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
