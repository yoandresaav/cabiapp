
# url in http://reportecabifeet.sytes.net/
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

from django.utils.six.moves import configparser
config = configparser.SafeConfigParser(allow_no_value=True)

# Import socket to read host name
import socket

# If the host name starts with 'MacBook', load configparser from "production.cfg"
if socket.gethostname().startswith('MacBook'):
    DEBUG = True
    # In other project use a debug config file
    config.read('%s/production.cfg' % (SETTINGS_DIR))
# If the host name starts with 'othe', load configparser from "production.cfg"
else:
    DEBUG = False
    config.read('%s/production.cfg' % (SETTINGS_DIR))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('security', 'SECRET_KEY')

ALLOWED_HOSTS = [    
    config.get('host', 'HOST_LOCAL'),
    config.get('host', 'HOST_LIVE')
]


if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'crispy_forms',
    
    # User app
    'web_site',
    'profiles',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'cabiapp.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'cabiapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'cabiapp.wsgi.application'

if DEBUG:
    # Config debug tools 
    INSTALLED_APPS.append(
        'debug_toolbar',
    )
    # if delete this the toolbar not show
    INTERNAL_IPS = ('127.0.0.1',)
    MIDDLEWARE.append(
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATA_BASES_ENGINE = config.get('databases', 'DATA_BASES_ENGINE')
DATA_BASES_NAME   = config.get('databases', 'DATA_BASES_NAME')

if DEBUG:
    DATA_BASES_NAME = os.path.join(BASE_DIR, DATA_BASES_NAME)

DATABASES = {
    'default': {
        'ENGINE': DATA_BASES_ENGINE,
        'NAME': DATA_BASES_NAME,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]
else:
    STATIC_ROOT = '/home/ubuntu/cabiapp/cabiapp/static/'

LOGOUT_REDIRECT_URL = '/'
LOGOUT_URL = 'logout'


if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    ADMINS = [(config.get('adminemail', 'USER'), config.get('adminemail', 'EMAIL')),]
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_SSL = False
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = config.get('email', 'EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config.get('email', 'EMAIL_HOST_PASSWORD')
    #EMAIL_PORT = 465
    EMAIL_PORT = 587

RECAPTCHA_SECRET_KEY = config.get('recaptcha', 'RECAPTCHA_SECRET_KEY'),

# Loggin
# import logging.config
# from django.utils.log import AdminEmailHandler

# Reset logging
LOGFILE_ROOT = os.path.join(BASE_DIR, 'logs')
ERROR_LOG_FILE = os.path.join(LOGFILE_ROOT, 'ErrorLoggers.log')
INFO_LOG_FILE = os.path.join(LOGFILE_ROOT, 'InfoLoggers.log')

if not os.path.exists(ERROR_LOG_FILE):
    os.makedirs(LOGFILE_ROOT, exist_ok=True)
    file = open(ERROR_LOG_FILE, 'w')
    file.close()

if not os.path.exists(INFO_LOG_FILE):
    os.makedirs(LOGFILE_ROOT, exist_ok=True)
    file = open(INFO_LOG_FILE, 'w')
    file.close()

# importing logger settings

from .logger_settings import *

    