from .base import *
from .base import BASE_DIR
import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "-h&@&!q%c-$%=$0=mqvg3"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': 'mike',
#             'USER': 'postgres',
#             'PASSWORD': 'Otieno',
#             'HOST': 'localhost',
#             'PORT': '',
#         }
#     }

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mikecrea_mike',
            'USER': os.environ.get('DATABASE_USER'), #mikecrea_mike
            'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '5432',
        }
        }

MAILER_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = False
EMAIL_HOST = 'mail.mikecreatives.com'
EMAIL_HOST_USER = 'connect@mikecreatives.com'
EMAIL_HOST_PASSWORD = 'Ekimsevitearc'
EMAIL_PORT = 26


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"