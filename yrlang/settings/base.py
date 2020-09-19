"""
Django settings for yrlang project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')thtzwyo&rja&umv_yrpl%wsoxnp+r7&vmx_xx6qaimmb+df-m'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'users.CustomUser'
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
# ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "none"
LOGIN_REDIRECT_URL = '/'
ACCOUNT_ADAPTER = 'yrlang.adapter.MyAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'yrlang.adapter.MySocialAccountAdepter'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
WAGTAIL_FRONTEND_LOGIN_URL = '/accounts/login/'
# ACCOUNT_FORMS = {'signup': 'users.forms.ClientSignupForm'}
# Application definition

INSTALLED_APPS = [
    'django_crontab',
    'channels',
    # cron-tab


    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',

    # all_auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',

    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # project apps
    'users',
    'main',
    'appointments',
    'rooms',
    'blogpost',
    'invoices',
    'payment',

    # django-wagtail
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    # middele ware thaat support for waigtail
    'modelcluster',
    'taggit',

    # paypal
    'paypal.standard.ipn',
    'webpush',

]


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # wagtail middelware
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'yrlang.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                #custome context processor
                'custome_context_processor.home_page_listing.city_list_view',
                'custome_context_processor.home_page_listing.post_list_view',
                # 'custome_context_processor.home_page_listing.language_list',
            ],
        },
    },
]

WSGI_APPLICATION = 'yrlang.wsgi.application'

#channels settings
ASGI_APPLICATION = 'yrlang.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

MESSAGE_LEVEL = 10
SITE_ID = 1
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# static files settings
STATIC_URL = '/static/'

# stripe keys

STRIPE_KEYS = {
  'secret_key': 'sk_test_51H2DyaHfiYMY9ftZKm47X0nRCs5f6lrmhU71rv0jXz2PskQuf07CTIgaWvgz81NYh0UMdndH4OcaRZT6O0oAl3Z800ZBBPTc6G',
  'publishable_key': 'pk_test_51H2DyaHfiYMY9ftZAZnlyH7TniUIByW7tS7U9px2eTivaZ8FRqtDTqVUDO9OC7NG92cdJDGsnXJ6XhQpw75ikPgi001ZfGYJ9G'
}
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]
STATIC_ROOT = os.path.join(PROJECT_DIR, 'assets')
# STATIC_ROOT = os.path(join(PROJECT_ROOT, 'assets'))
# media settings
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'

# wagtail setting
WAGTAIL_SITE_NAME = 'Yr.lang CMS'
WAGTAILEMBEDS_RESPONSIVE_HTML = True

# paypal Settings
PAYPAL_RECEIVER_EMAIL = '' # This is the email where all the notification will be sent
PAYPAL_TEST = True


#cron-tabs schedule
CRONJOBS = [
    ('*/5 * * * *', 'cron_tabs.task_reminder.appointment_reminder_before_24H'),
    ]

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY":"BPFHKZ8EDMVFgfPZ6P8vrbLGP0sNlaNMs6ss5x1WZ9HlNdrNVZcsZToBnfvo4-pbSQQxQLv8VxHUnt_-1wKLWBk",
    "VAPID_PRIVATE_KEY":"eyH6m2JH3pDaT6m9nX58y0KejEICQ_nwOHdJEegAn9s",
    "VAPID_ADMIN_EMAIL": "trootechak@gmail.com"
}