
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
]

if DEBUG:
    INSTALLED_APPS.append(
        'debug_toolbar',
    )
    # if delete this the toolbar not show
    INTERNAL_IPS = ('127.0.0.1',)

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


LOGOUT_REDIRECT_URL = '/'
LOGOUT_URL = 'logout'