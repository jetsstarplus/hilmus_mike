import environ
# importing the base settings
from .base import *

from .heroku import *

env = environ.Env()
# Authentication information
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'hilmus-mike-1'

# Storage location
DEFAULT_FILE_STORAGE = 'hilmus_mike.storage_backends.MediaStorage'
# DEFAULT_FILE_STORAGE =STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'hilmus_mike.storage_backends.StaticStorage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_REGION = 'af-south-1'

AWS_S3_CUSTOM_DOMAIN = '{}.s3.{}.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION)

# AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)

AWS_DEFAULT_ACL = None

AWS_S3_HOST = 's3.{}.amazonaws.com'.format(AWS_S3_REGION)

AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age = 86400',}
# This transfered to the storage backends file
AWS_STATIC_LOCATION = 'static'

AWS_PUBLIC_MEDIA_LOCATION = 'media'

AWS_PRIVATE_MEDIA_LOCATION = 'private-media'

# For future deployment purposes
STATIC_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

MEDIA_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_PUBLIC_MEDIA_LOCATION)

# STATIC_URL = 'http://' + AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com/'

# arn:aws:s3:::hilmus-rentit

THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
