import os
from decouple import config, Csv
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- Core Django Settings ---
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ENV = config('ENV', default='development')
ALLOWED_HOSTS = ['.onrender.com']

# --- CORS settings ---
CORS_ORIGIN_ALLOW_ALL = config('CORS_ORIGIN_ALLOW_ALL', default=DEBUG, cast=bool)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='', cast=Csv())

# --- CSRF Trusted Origins ---
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

# --- Security ---
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=not DEBUG, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=not DEBUG, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=not DEBUG, cast=bool)

# --- Logging ---
LOG_LEVEL = config('LOG_LEVEL', default='INFO')

# --- Timezone and Localization ---
TIME_ZONE = config('TIME_ZONE', default='UTC')
LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')
USE_I18N = True
USE_L10N = True
USE_TZ = True

# --- Admin URL ---
DJANGO_ADMIN_URL = config('DJANGO_ADMIN_URL', default='admin/')

# --- Custom App Settings ---
FEATURE_X_ENABLED = config('FEATURE_X_ENABLED', default=False, cast=bool)
SITE_TITLE = config('SITE_TITLE', default='Himanshu-Lodhi-Portfolio')

# --- REST Framework  ---
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        config('REST_FRAMEWORK_DEFAULT_PERMISSION_CLASSES', default='rest_framework.permissions.IsAuthenticated')
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        cls.strip() for cls in config(
            'REST_FRAMEWORK_DEFAULT_AUTHENTICATION_CLASSES',
            default='rest_framework.authentication.SessionAuthentication,rest_framework.authentication.BasicAuthentication'
        ).split(',')
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': config('PAGINATION_PAGE_SIZE', default=10, cast=int),
}

LOGIN_URL = '/dashboard/login/'
LOGOUT_URL = '/dashboard/logout/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'info',
    'dashboard',
    'cloudinary_storage',
    'cloudinary',
    'django_ckeditor_5',
    'rest_framework',
    # Add any other apps here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": {
            "items": [
                "heading", "|",
                "bold", "italic", "underline", "strikethrough", "code", "subscript", "superscript", "|",
                "link", "blockQuote", "codeBlock", "|",
                "bulletedList", "numberedList", "todoList", "|",
                "outdent", "indent", "|",
                "alignment", "|",
                "imageUpload", "mediaEmbed", "insertTable", "horizontalLine", "pageBreak", "|",
                "undo", "redo", "|",
                "fontSize", "fontFamily", "fontColor", "fontBackgroundColor", "|",
                "highlight", "removeFormat", "|",
                "specialCharacters", "findAndReplace", "selectAll", "|",
                "sourceEditing"
            ],
            "shouldNotGroupWhenFull": True
        },
        "image": {
            "toolbar": [
                "imageTextAlternative", "imageStyle:inline", "imageStyle:wrapText",
                "imageStyle:breakText", "imageStyle:side", "toggleImageCaption"
            ]
        },
        "table": {
            "contentToolbar": [
                "tableColumn", "tableRow", "mergeTableCells", "tableCellProperties", "tableProperties"
            ]
        },
        "mediaEmbed": {
            "previewsInData": True
        },
        "language": "en"
    }
}

ROOT_URLCONF = 'portfolio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'filter_tags': 'info.templatetags.filter',
            }
        },
    },
]

WSGI_APPLICATION = 'portfolio.wsgi.application'

# ---- Use ONLY Render Postgres Database ----
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}
# Make sure DATABASE_URL is set in your environment (Render dashboard).

# --- Static and Media Files ---
STATIC_URL = config('STATIC_URL', default='/static/')
MEDIA_URL = config('MEDIA_URL', default='/media/')
STATIC_ROOT = config('STATIC_ROOT', default=os.path.join(BASE_DIR, 'staticfiles'))
MEDIA_ROOT = config('MEDIA_ROOT', default=os.path.join(BASE_DIR, 'media'))

# Always include the top-level static directory for collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

USE_CLOUDINARY = config('USE_CLOUDINARY', default=True, cast=bool)
if USE_CLOUDINARY:
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': config('CLOUD_NAME'),
        'API_KEY': config('API_KEY'),
        'API_SECRET': config('API_SECRET'),
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    if not DEBUG:
        STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'
    else:
        STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    if not DEBUG:
        STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    else:
        STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
