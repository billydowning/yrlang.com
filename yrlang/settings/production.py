import os

from .base import *


DEBUG = False
ALLOWED_HOSTS = ['18.216.99.152']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'yrlang2020',
        'USER': 'postgres',  # Do not change. Create a separate settings file for local dev if needs to be different
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
