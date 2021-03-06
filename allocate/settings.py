"""
Django settings for allocate project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

PRODUCTION = False

DOMAIN_PRODUCTION = 'http://app.getallocate.in'
DOMAIN_LOCAL = 'http://localhost:8000'

LOCAL_LOGGING_FILE = '/tmp/django_debug.log'
PRODUCTION_LOGGING_FILE = '/home/ubuntu/debug.log'

# Change this in production
DOMAIN = DOMAIN_PRODUCTION if PRODUCTION else DOMAIN_LOCAL
LOGGING_FILE = PRODUCTION_LOGGING_FILE if PRODUCTION else LOCAL_LOGGING_FILE

DEBUG = not PRODUCTION

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_URL = '/authentication/login'
LOGIN_REDIRECT_URL = '/authentication'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

SECRETS_DIR = '../.secret'
with open(SECRETS_DIR + '/secret_key.txt') as f:
  SECRET_KEY = f.read().strip()

with open(SECRETS_DIR + '/db_pass.txt') as f:
  DB_PASSWORD = f.read().strip()

ALLOWED_HOSTS = ['localhost', 'app.getallocate.in']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'authentication',
    'allocate_app'
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'allocate.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'allocate.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'allocate',
        'NAME': 'allocate_django',
        'PASSWORD': DB_PASSWORD
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = "/home/ubuntu/allocate-django/static"

# Outlook API
MS_APP_ID = '20abe469-8d38-4057-9ced-f31a8f15bf06'
MS_PASS_FILE = SECRETS_DIR + '/ms_pass'
MS_AUTH_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
MS_TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'

# Google API
GOOGLE_CLIENT_SECRETS = SECRETS_DIR + "/client_secret.json"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGGING_FILE,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
