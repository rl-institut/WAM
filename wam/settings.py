"""
Django settings for wam project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import importlib
import logging
from configobj import ConfigObj

config_file_path = os.environ.get('WAM_CONFIG_PATH')

if config_file_path is None:
    raise KeyError(
        'Please add WAM_CONFIG_PATH as an environment variable, see '
        'https://wam.readthedocs.io/en/latest/getting_started.html#environment-variables'
    )
config = ConfigObj(config_file_path)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['WAM']['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config['WAM'].as_bool('DEBUG')

logging_level = logging.DEBUG if DEBUG else logging.INFO
logging.getLogger().setLevel(logging_level)

ALLOWED_HOSTS = config['WAM'].as_list('ALLOWED_HOSTS')

# Additional apps are loaded from environment variable
WAM_APPS = os.environ.get('WAM_APPS')

if WAM_APPS is None:
    raise KeyError(
        'Please add WAM_APPS as an environment variable, see '
        'https://wam.readthedocs.io/en/latest/getting_started.html#environment-variables'
    )

if WAM_APPS == '':
    # The environment variable exists but no apps are defined
    WAM_APPS = []
else:
    # Apps name are retrieved
    WAM_APPS = WAM_APPS.split(',')

APP_LABELS = {
    app: ConfigObj(os.path.join(BASE_DIR, app, 'labels.cfg'))
    for app in WAM_APPS
}

# Application definition
INSTALLED_APPS = WAM_APPS + [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.forms',
    'crispy_forms',
    'meta',
    'user_sessions'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wam.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'labels': 'templatetags.labels',
                'simple': 'templatetags.simple',
            },
        },
    },
]
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'wam.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DJANGO_DB = config['WAM'].get('DJANGO_DB', 'DEFAULT')
DATABASES = {
    'default': {
        **config['DATABASES'][DJANGO_DB],
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'de-DE'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# USE_THOUSAND_SEPARATOR = True
# DECIMAL_SEPARATOR = ','
# THOUSAND_SEPARATOR = '.'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    [
        os.path.join(app, 'static') for app in WAM_APPS
        if os.path.exists(os.path.join(app, 'static'))
    ] +
    [os.path.join(BASE_DIR, "static")]
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Contains data under session key:
SESSION_DATA = None

# Import Applicaton-specific Settings
for app in WAM_APPS:
    # Import settings module from app and add constants to wam.settings
    try:
        settings = importlib.import_module(f'{app}.settings', package='wam')
    except ModuleNotFoundError:
        pass
    else:
        for setting in dir(settings):
            if setting == setting.upper():
                if setting in locals() and isinstance(locals()[setting], list):
                    locals()[setting] += getattr(settings, setting)
                else:
                    locals()[setting] = getattr(settings, setting)

    # Import app_settings from app
    try:
        importlib.import_module(f'{app}.app_settings', package='wam')
    except ModuleNotFoundError:
        pass

# E-mail config for outgoing mails (used by exchangelib)
WAM_EXCHANGE_ACCOUNT = os.environ.get('WAM_EXCHANGE_ACCOUNT')
WAM_EXCHANGE_EMAIL = os.environ.get('WAM_EXCHANGE_EMAIL')
WAM_EXCHANGE_PW = os.environ.get('WAM_EXCHANGE_PW')
