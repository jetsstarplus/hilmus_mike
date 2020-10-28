"""
Production Settings for Heroku
"""

import environ

# If using in your own project, update the project namespace below

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, True)
)

# False if not in os.environ
DEBUG = env('DEBUG')


# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}


# CACHES = {
#     # read os.environ['CACHE_URL'] and raises ImproperlyConfigured exception if not found
#     'default': env.cache(),
#     # read os.environ['REDIS_URL']
#     'redis': env.cache('REDIS_URL')
# }


# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

