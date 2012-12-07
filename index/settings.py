# Django settings for index project.
import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from django.core.urlresolvers import reverse_lazy
import django_cache_url
import dj_database_url
from S3 import CallingFormat


DIRNAME = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

DEBUG = bool(os.environ.get('DEBUG', False))
DEVELOPMENT_SITE = bool(os.environ.get('DEVELOPMENT_SITE', False))

DATABASES = {'default': dj_database_url.config(default='postgres://localhost/index')}
CACHES = {'default': django_cache_url.config()}

ADMINS = (('Admin', 'admin@incuna.com'),)
MANAGERS = ADMINS
ADMIN_EMAILS = zip(*ADMINS)[1]
EMAIL_SUBJECT_PREFIX = '[index] '
SERVER_EMAIL = DEFAULT_FROM_EMAIL = 'info@incuna.com'
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

TIME_ZONE = 'UTC'
USE_L10N = True  # Locale
USE_TZ = True

LANGUAGE_CODE = 'en-GB'
USE_I18N = False  # Internationalization

# AWS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = False
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'index.incuna.com')
AWS_CLOUDFRONT_DOMAIN = os.environ.get('AWS_CLOUDFRONT_DOMAIN')
AWS_CLOUDFRONT_STREAMING_DOMAIN = os.environ.get('AWS_CLOUDFRONT_STREAMING_DOMAIN')
DEFAULT_FILE_STORAGE = 'cloudfront.cloudfrontstorage.CouldFrontStorage'
STATICFILES_STORAGE = os.environ.get('STATICFILES_STORAGE', 'incuna.storage_backends.S3StaticStorage')
S3_URL = 'http://{0}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)

# Static
MEDIA_ROOT = os.path.join(DIRNAME, 'client_media')
MEDIA_URL = os.environ.get('MEDIA_URL', S3_URL + 'media/')
STATIC_ROOT = os.path.join(DIRNAME, 'static_media')
STATIC_URL = os.environ.get('STATIC_URL', S3_URL + 'static/')
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'incuna.staticfiles.LegacyAppDirectoriesFinder',
)

TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (os.path.join(DIRNAME, 'templates'))
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'incuna.context_processors.devsite',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.google.GoogleOAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = reverse_lazy('login')

GOOGLE_OAUTH2_CLIENT_ID = os.environ['GOOGLE_OAUTH2_CLIENT_ID']
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ['GOOGLE_OAUTH2_CLIENT_SECRET']
GOOGLE_WHITE_LISTED_DOMAINS = ['incuna.com']
SOCIAL_AUTH_USER_MODEL = 'auth.User'


ROOT_URLCONF = 'index.urls'
SECRET_KEY = '(7a$_!38=ao^y790z$4f-zqx(@y@82x)lyq(_hebby+=u_20#d'
SITE_ID = 1
WSGI_APPLICATION = 'index.wsgi.application'

INSTALLED_APPS = (
    # Project Apps
    'index',

    # Libraries
    'incuna_auth',
    'incuna.admin',
    'incuna',
    'south',
    'debug_toolbar',
    'django_extensions',
    'gunicorn',
    'sorl.thumbnail',
    'social_auth',

    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

SENTRY_DSN = 'http://72f1b7b18e3944b999fbe5a34afa3ad7:cb90b765fdbf4f7f89cbd85dd3cea33d@sentry.incuna.com/39'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '[%(asctime)s][%(levelname)s] %(name)s %(filename)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': '%H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['sentry', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'incuna.default': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propogate': True,
        },
        'sentry.errors': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propogate': True,
        },
    }
}

# Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}
INTERNAL_IPS = ('127.0.0.1',)

# Sorl settings
THUMBNAIL_DEBUG = DEBUG
THUMBNAIL_SUBDIR = '_thumbs'
THUMBNAIL_QUALITY = 95
# activate ImageMagick for converting images
THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine'
THUMBNAIL_CONVERT = 'convert'
IMAGEMAGICK_FILE_TYPES = ('pdf')
