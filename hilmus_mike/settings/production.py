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


# CACHES = {
#     "default": {
#          "BACKEND": "redis_cache.RedisCache",
#          "LOCATION": env('REDIS_URL'),
#     }
# }