import os

from .base import *


DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

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

#debug toolbar
INTERNAL_IPS = ('127.0.0.1', )

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

# mail configurations
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'pm.trootech@gmail.com'
EMAIL_HOST_PASSWORD = 'TEst@123'
EMAIL_PORT = 587

# for allauth email sender
DEFAULT_FROM_EMAIL = 'pm.trootech@gmail.com'