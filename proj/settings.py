"""
Django settings for proj project.

For production, comment out the sections: DEV, uncomment the sections: PRODUCTION
For local development, comment out the sections: PRODUCTION, uncomment the sections: DEV

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'proj/templates')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# PRODUCTION:
SECRET_KEY = 'dh64rv632oqrv-ot&7)j-i9ghp*_h@#t3f*dwv^&28!!=@#4pb'

# DEV:
#SECRET_KEY = 'jzrs#c#8n&+9c-n=#cr8pt7hmv2h0b$0o9@v-+or7#z*xjxl^l'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'proj.urls'

WSGI_APPLICATION = 'proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'PORT': '',
        'USER': 'django',
        'HOST': 'localhost',

        # PRODUCTION:
        'NAME': 'django',
        'PASSWORD': 'iWishIwas',

        # DEV:
        #'NAME': 'oligo',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_DIR = (
	'/usr/lib/python2.6/site-packages/django/contrib/admin/static/admin',
	'/data/www/djangoOligo/proj/templates/docs/_build',
)
STATIC_URL = '/static/'
STATIC_ROOT = '/data/www/djangoOligo/static/'
