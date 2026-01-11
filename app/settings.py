import os
from decouple import config
from pathlib import Path
import dj_database_url
import cloudinary

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-build-dummy-key')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

DJANGO_ADMIN_URL = config('DJANGO_ADMIN_URL', default='admin/')

CORS_ORIGIN_ALLOW_ALL = config('CORS_ORIGIN_ALLOW_ALL', default=True, cast=bool)
CORS_ALLOW_CREDENTIALS = True

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
]

ADDITIONAL_APPS = [
    'app',
    'info',
    'dashboard',
    'cloudinary_storage',
    'cloudinary',
    'django_ckeditor_5',
    'rest_framework',
]

INSTALLED_APPS += ADDITIONAL_APPS

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

ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'

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

if not DEBUG:
    # PRODUCTION: Use Supabase
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
        DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True
    else:
        # Fallback if URL is missing in Production to prevent crash
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
else:
    # DEVELOPMENT: Always use SQLite (Docker or Non-Docker)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
cloudinary.config( 
    cloud_name = config("CLOUDINARY_CLOUD_NAME", default="dummy_name"), 
    api_key = config("CLOUDINARY_API_KEY", default="dummy_key"), 
    api_secret = config("CLOUDINARY_API_SECRET", default="dummy_secret") 
)

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            ['heading', '|', 'bold', 'italic', 'underline', 'strikethrough', 'code', 'subscript', 'superscript'],
            ['link', 'blockQuote', 'highlight'],
            ['bulletedList', 'numberedList', 'todoList'],
            ['alignment', 'outdent', 'indent'],
            ['insertTable', 'mediaEmbed', 'imageUpload', 'horizontalLine'],
            ['undo', 'redo', 'removeFormat'],
            ['codeBlock', 'sourceEditing'],
        ],
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'},
                {'model': 'heading4', 'view': 'h4', 'title': 'Heading 4', 'class': 'ck-heading_heading4'},
            ]
        },
        'alignment': {
            'options': ['left', 'center', 'right', 'justify']
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties'
            ]
        },
        'image': {
            'toolbar': [
                'imageTextAlternative', 'imageStyle:inline', 'imageStyle:block', 'imageStyle:side'
            ]
        },
        'mediaEmbed': {
            'previewsInData': True
        },
        'codeBlock': {
            'languages': [
                {'language': 'plaintext', 'label': 'Plain text'},
                {'language': 'python', 'label': 'Python'},
                {'language': 'javascript', 'label': 'JavaScript'},
                {'language': 'html', 'label': 'HTML'},
                {'language': 'css', 'label': 'CSS'},
                {'language': 'bash', 'label': 'Bash'},
                {'language': 'json', 'label': 'JSON'},
            ]
        },
        'style': {
            'definitions': [
                {
                    'name': 'Typing Text Style',
                    'element': 'span',
                    'classes': ['typing-text-style'],
                    'styles': {
                        'color': '#222222',
                        'background-color': '#f5f5f5',
                        'padding': '2px 4px',
                        'border-radius': '4px',
                        'font-family': 'monospace'
                    }
                }
            ]
        },
        'htmlSupport': {
            'allow': [
                {
                    'name': '.*',  
                    'attributes': True,
                    'classes': True,
                    'styles': True
                }
            ]
        },
        'language': 'en',
        'placeholder': 'Start typing your content here...',
        'removePlugins': ['Title']
    }
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
# Update these lines in settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] # os.path still works with Path objects
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
