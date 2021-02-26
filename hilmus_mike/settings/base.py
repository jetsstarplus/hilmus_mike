import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    
    # downloaded applications
    # 'versatileimagefield',
    'django_registration',
    'mailer',
    'django_summernote',
    'crispy_forms',
    'easy_thumbnails',
    'mptt',
    'filer',
    'rest_framework',
    
    # Edited libraries for django-registration    
    # 'account_registration',
    # Installed applications
    'pages.apps.PagesConfig',
    'account.apps.AccountConfig',
    'mike_admin.apps.MikeAdminConfig',
    'article.apps.ArticleConfig',
    'daraja',
    'mpesa',
    'upload_handler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hilmus_mike.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates", os.path.join(BASE_DIR, 'templates'), 'Templates', os.path.join(BASE_DIR, 'Templates')],
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

WSGI_APPLICATION = 'hilmus_mike.wsgi.application'

AUTH_USER_MODEL='account.Account'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

SITE_ID = 1

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# Static settings for the directory to fetch the static files from
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
MEDIAFILES_DIRS = [
    os.path.join(BASE_DIR, "media"),
]

# rest framework configuration

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
}

# Login and logout redirect
LOGOUT_REDIRECT_URL="/account/login/"
LOGIN_REDIRECT_URL="/account/"
LOGIN_URL="/account/login/"

# Thumbnail settings
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
FILER_CANONICAL_URL = 'sharing/'
THUMBNAIL_HIGH_RESOLUTION = True
# summenote settings
X_FRAME_OPTIONS = 'SAMEORIGIN'
# Email configurations
EMAIL_BACKEND = "mailer.backend.DbBackend"
DEFAULT_FROM_EMAIL=os.environ.get('EMAIL_USER')
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (90, 90), 'crop': True},
        'avatar2': {'size': (150, 150), 'crop': True},
        'blog': {'size': (500, 350), 'crop': True},
        'avatar_small': {'size': (30, 30), 'crop': True},
    },
}

ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window

CRISPY_TEMPLATE_PACK='bootstrap4'
SUMMERNOTE_THEME = 'bs4'  # Show summernote with Bootstrap4
SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode, default
    'iframe': True,

    # Or, you can set it to `False` to use SummernoteInplaceWidget by default - no iframe mode
    # In this case, you have to load Bootstrap/jQuery sources and dependencies manually.
    # Use this when you're already using Bootstrap/jQuery based themes.
    # 'iframe': False,

    # You can put custom Summernote settings
    'summernote': {
        # As an example, using Summernote Air-mode
        'airMode': False,

        # Change editor size
        'width': '100%',
        'height': '480',

        # Use proper language setting automatically (default)
        'lang': LANGUAGE_CODE,
        
        'codemirror': {
            'mode': 'htmlmixed',
            'lineNumbers': 'true',
            # You have to include theme file in 'css' or 'css_for_inplace' before using it.
            'theme': 'monokai',
        },
    },

    # Require users to be authenticated for uploading attachments.
    'attachment_require_authentication': True,

    # You can completely disable the attachment feature.
    'disable_attachment': False,

    # Set to `True` to return attachment paths in absolute URIs.
    'attachment_absolute_uri': False,

    # Codemirror as codeview
    # If any codemirror settings are defined, it will include codemirror files automatically.
    'css': (
        'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.29.0/theme/monokai.min.css',
    ),

    # Lazy initialization
    # If you want to initialize summernote at the bottom of page, set this as True
    # and call `initSummernote()` on your page.
    'lazy': True,    
}
REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
   'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
  }

FILE_UPLOAD_HANDLERS = [
    "upload_handler.uploadhandler",
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler"]
