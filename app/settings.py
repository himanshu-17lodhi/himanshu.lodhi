import os
from decouple import config
import dj_database_url
import cloudinary

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

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

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=0,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    
cloudinary.config( 
    cloud_name = config("CLOUDINARY_CLOUD_NAME"), 
    api_key = config("CLOUDINARY_API_KEY"), 
    api_secret = config("CLOUDINARY_API_SECRET") 
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
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
# EMAIL_PORT = config('EMAIL_PORT', cast=int)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

LANGUAGE_CODE = config('LANGUAGE_CODE', default='en-us')
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
