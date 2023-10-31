"""
Django settings for vtokens project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
# from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# load_dotenv(os.path.join(BASE_DIR, '.dev.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't7ua9rcplht^2x&gh&y2mspv6p&3x99s^sa6c5zno8e1x%k9p5'

# Use for decode user's JWT token
JWT_KEY = '1540596AD107034AECF78CE71A012DF216595300EF0B32EDFFAE4B0E0B66332A'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'true').lower() in ('true', '1')


ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    'api.apps.ApiConfig',
    'django_cleanup.apps.CleanupConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Note that this needs to be placed above CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vtokens.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'vtokens.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

default_db = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'gr',
    'USER': 'gr',
    'PASSWORD': 'gr@20211',
}

if os.environ.get('ENV') == 'dev':
    default_db.update({
        'HOST': 'database',
        'PORT': '5432',
    })
else:
    default_db.update({
        'HOST': 'localhost',
        'PORT': '5432',
    })

DATABASES = {
    'default': default_db
}

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Saigon'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'data', 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'data', 'media')

import subprocess

if not os.path.exists(os.path.join(BASE_DIR, 'data', 'node_modules', '@openzeppelin')):
    subprocess.call(['npm', 'install'], cwd=os.path.join(BASE_DIR, 'data'))

DEFAULT_PERMISSION_CLASSES = ['rest_framework.permissions.IsAuthenticated']

# if DEBUG:
#     # DEFAULT_PERMISSION_CLASSES.append('rest_framework.permissions.AllowAny')

#     DEFAULT_PERMISSION_CLASSES = ['rest_framework.permissions.AllowAny']

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': DEFAULT_PERMISSION_CLASSES,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'vtokens.authentication.CustomAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
}

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:3000',
# ]

# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3000'
# ]

# CELERY CONFIG
if os.environ.get('ENV') == 'dev':
    CELERY_BROKER_URL = 'redis://redis:6379'
    CELERY_RESULT_BACKEND = 'redis://redis:6379'
else:
    print(os.environ.get('ENV'))
    CELERY_BROKER_URL = 'redis://139.59.217.172:6379'
    CELERY_RESULT_BACKEND = 'redis://139.59.217.172:6379'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Saigon'   # celery will use TIME_ZONE of Django project

# INFURA
INFURA_RINKEBY_PROJECT_ID = os.environ.get('INFURA_RINKEBY_PROJECT_ID')
INFURA_RINKEBY_PROJECT_SECRET = os.environ.get('INFURA_RINKEBY_PROJECT_SECRET')
INFURA_RINKEBY_HTTP_URL = os.environ.get('INFURA_RINKEBY_HTTP_URL')

INFURA_GOERLI_PROJECT_ID = os.environ.get('INFURA_GOERLI_PROJECT_ID')
INFURA_GOERLI_PROJECT_SECRET = os.environ.get('INFURA_GOERLI_PROJECT_SECRET')
INFURA_GOERLI_HTTP_URL = os.environ.get('INFURA_GOERLI_HTTP_URL')

# BRIDGE DAPPS
ETHEREUM_BRIDGE_CONTRACT_ADDRESS = os.environ.get('ETHEREUM_BRIDGE_CONTRACT_ADDRESS')

RINKEBY_BRIDGE_CONTRACT_ADDRESS = os.environ.get('RINKEBY_BRIDGE_CONTRACT_ADDRESS')
RINKEBY_BRIDGE_CONTRACT_ABI_FILEPATH = os.path.join(BASE_DIR, 'data', 'abi', 'rinkeby_bridge.json')

GOERLI_BRIDGE_CONTRACT_ADDRESS = os.environ.get('GOERLI_BRIDGE_CONTRACT_ADDRESS')
GOERLI_BRIDGE_CONTRACT_ABI_FILEPATH = os.path.join(BASE_DIR, 'data', 'abi', 'goerli_bridge.json')

RINKEBY_BRIDGE_CONTRACT_ADDRESS_V2 = os.environ.get('RINKEBY_BRIDGE_CONTRACT_ADDRESS_V2')
RINKEBY_BRIDGE_CONTRACT_ABI_FILEPATH_V2 = os.path.join(BASE_DIR, 'data', 'abi', 'rinkeby_bridge_v2.json')

GOERLI_BRIDGE_CONTRACT_ADDRESS_V2 = os.environ.get('GOERLI_BRIDGE_CONTRACT_ADDRESS_V2')
GOERLI_BRIDGE_CONTRACT_ABI_FILEPATH_V2 = os.path.join(BASE_DIR, 'data', 'abi', 'goerli_bridge_v2.json')



RINKEBY_VCHAIN_TOKEN_CONTRACT_ADDRESS = os.environ.get('RINKEBY_VCHAIN_TOKEN_CONTRACT_ADDRESS')
GOERLI_VCHAIN_TOKEN_CONTRACT_ADDRESS = os.environ.get('GOERLI_VCHAIN_TOKEN_CONTRACT_ADDRESS')

ETHEREUM_PRIVATE_KEY = os.environ.get('ETHEREUM_PRIVATE_KEY')

GOERLI_BRIDGE_ADMIN_ADDRESS = os.environ['GOERLI_BRIDGE_ADMIN_ADDRESS']
RINKEBY_BRIDGE_ADMIN_ADDRESS = os.environ['RINKEBY_BRIDGE_ADMIN_ADDRESS']

## SHELL_PLUS
NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--port', '8888',
    '--allow-root'
]

# FABRIC SERVICE
VCHAIN_DB_HOST = os.environ.get('DB_HOST')
VCHAIN_DB_PORT = os.environ.get('DB_PORT')
VCHAIN_DB_NAME = os.environ.get('DB_NAME')
VCHAIN_DB_USERNAME = os.environ.get('DB_USERNAME')
VCHAIN_DB_PASSWORD = os.environ.get('DB_PASSWORD')
K8S_TOKEN = os.environ.get('K8S_TOKEN')

IPYTHON_ARGUMENTS = [
    "--ext",
    "django_extensions.management.notebook_extension",
    "--debug",
]

APPEND_SLASH = False
