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

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mike',
            'USER': 'postgres',
            'PASSWORD': 'Otieno',
            'HOST': 'localhost',
            'PORT': '',
        }
    }


# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'mikecrea_mike',
#             'USER': os.environ.get('DATABASE_USER'), #mikecrea_mike
#             'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
#             'HOST': 'localhost',
#             'PORT': '',
#             }
#         }

# EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
# MAILER_EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
# MAILER_EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_USE_TLS = False
# EMAIL_HOST = 'mail.mikecreatives.com'
# EMAIL_HOST_USER = 'account@mikecreatives.com'
# EMAIL_HOST_PASSWORD = 'Ekimsevitearc'
# EMAIL_PORT = 26

DEFAULT_FROM_EMAIL='account@mikecreatives.com'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = '812aee1cfc75ed'
EMAIL_HOST_PASSWORD = '699bc7b3cf7c96'
EMAIL_PORT = '2525'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
# git push -u cpanel


STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
