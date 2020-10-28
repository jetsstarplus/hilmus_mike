try:
    from .production import *
except:
    from .local import *

# import environ

# env=environ.Env()
# if env('DEBUG'):
#     from .production import *
# else:
#     from .local import *