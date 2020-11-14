import environ

from .amazon import *
# Database connection settings
# DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True

#MY EMAIL SETTING
MAILER_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.mikecreatives.com'  #Hosted on namecheap Ex: mail.pure.com
EMAIL_USE_TLS = False
EMAIL_PORT = 26 #This will be different based on your Host, for Namecheap I use this`
EMAIL_HOST_USER = 'connect@mikecreatives.com' # Ex: info@pure.com
EMAIL_HOST_PASSWORD = 'connectmikecreativesemail' #


# CACHES = {
#     "default": {
#          "BACKEND": "redis_cache.RedisCache",
#          "LOCATION": env('REDIS_URL'),
#     }
# }