"""
Django settings for donder project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages
import dj_database_url
from environ import Env 
from pathlib import Path

env = Env()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = BASE_DIR / 'templates'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False

# ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', '127.0.0.2', '192.168.0.15', '172.31.13.139']
# ALLOWED_HOSTS = ['']
ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', '127.0.0.2', '192.168.0.15', '172.31.13.139', 'www.donder.co.uk', 'donder.co.uk', 'donder-production.up.railway.app']


# SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SESSION_COOKIE_SECURE = False 
# CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['https://donder-production.up.railway.app']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',   #add Django sitemaps to installed apps
    
    # third-party
    'crispy_forms',
    'import_export',
    'django_filters',
    'django_s3_storage',

    # own apps 
    'pages',
    'mountainsdir',
    'user_accounts'
]

IMPORT_EXPORT_USE_TRANSACTIONS = True

CRISPY_TEMPLATE_PACK = 'bootstrap4'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MIDDLEWARE = [
    'donder.middleware.HealthCheckMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'donder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'donder.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# if 'RDS_DB_NAME' in os.environ:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ['RDS_DB_NAME'],
#         'USER': os.environ['RDS_USERNAME'],
#         'PASSWORD': os.environ['RDS_PASSWORD'],
#         'HOST': os.environ['RDS_HOSTNAME'],
#         'PORT': os.environ['RDS_PORT'],
#     }
# }

POSTGRES_LOCALLY = False
if ENVIRONMENT == 'production' or POSTGRES_LOCALLY == True:
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': env('PRD_DB_NAME'),
    #         'USER': env('PRD_DB_USER'),
    #         'PASSWORD': env('PRD_DB_PASS'),
    #         'HOST': env('PRD_DB_HOST'),
    #         'PORT': env('PRD_DB_PORT'),
    #     }
    # }
    DATABASES = {
        'default': dj_database_url.config(
            default=env('DATABASE_URL'),
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('LOCAL_DB_NAME'), 
            'USER': env('LOCAL_DB_USER'), 
            'PASSWORD': env('LOCAL_DB_PASS'),
            'HOST': env('LOCAL_DB_HOST'),
            'PORT': env('LOCAL_DB_PORT'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATIC_URL = 'static/'

# STATICFILES_DIRS = [
#     BASE_DIR / ".." / "static",
# ]

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, '..' ,'media')

# stripe vars
STRIPE_PUBLIC_KEY = ''
STRIPE_SECRET_KEY = ''

AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'no-cache'  # or 'max-age=0'
}

# if ENVIRONMENT == 'development':
#     STATIC_URL = 'static/'
#     STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, '..', 'static'),
#     ]
#     MEDIA_URL = '/media/'
#     MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
# else:

STATIC_URL = '/static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'mediafiles'

    # # STATIC_ROOT = os.path.join(BASE_DIR, '..','static')
    # S3_BUCKET_NAME = env('S3_BUCKET_NAME')
    # STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
    # AWS_S3_BUCKET_NAME_STATIC = S3_BUCKET_NAME
    # AWS_S3_BUCKET_NAME = env('AWS_S3_BUCKET_NAME')

    # # serve the static files directly from the specified s3 bucket
    # AWS_S3_CUSTOM_DOMAIN = f'{S3_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com' 
    # STATIC_URL = env('STATIC_URL')
    # AWS_S3_PUBLIC_URL_STATIC = env('AWS_S3_PUBLIC_URL_STATIC')

    # print(AWS_S3_PUBLIC_URL_STATIC)

    # # for admin static files
    # ADMIN_MEDIA_PREFIX = env('ADMIN_MEDIA_PREFIX')

    # # MEDIA_URL = 'https://donderstaticmedia.s3.eu-west-1.amazonaws.com/media/'
    # DEFAULT_FILE_STORAGE = 'django_s3_storage.storage.S3Storage'
    # MEDIA_URL = env('MEDIA_URL')
    # AWS_S3_BUCKET_AUTH = False
    # AWS_S3_MAX_AGE_SECONDS = 60 * 60 * 24 * 365  # 1 year.



