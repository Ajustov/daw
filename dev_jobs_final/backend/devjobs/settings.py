import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()
APPEND_SLASH = False
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'
DEBUG = not PRODUCTION
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
AUTH_USER_MODEL = 'jobs.User'
INSTALLED_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'apps.jobs',
  'ninja_extra',
  'ninja_jwt',
  'ninja_jwt.token_blacklist',
  'corsheaders',
]
if os.getenv('DATABASE_URL'):
  DATABASES = {
    'default': dj_database_url.config(
      conn_max_age=600, conn_health_checks=True, ssl_require=True
    )
  }
else:
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql',
      'NAME': os.getenv('POSTGRES_DB'),
      'USER': os.getenv('POSTGRES_USER'),
      'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
      'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
      'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
  }
cors_origins = os.getenv('CORS_ALLOWED_ORIGINS')
CORS_ALLOWED_ORIGINS = (
  [origin.strip() for origin in cors_origins.split(',')]
  if cors_origins
  else ['http://localhost:5173', 'http://127.0.0.1:5173']
)
MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'devjobs.urls'
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]
WSGI_APPLICATION = 'devjobs.wsgi.application'
AUTH_PASSWORD_VALIDATORS = [
  {
    # Mínimo de 8 (default)
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },
  {
    # No puede ser númerico, incluido unicode
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]
LANGUAGE_CODE = 'en-es'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True
STATIC_URL = 'static/'

NINJA_JWT = {
  # Para que en el /refresh me refresque tambien el refresh token
  'ROTATE_REFRESH_TOKENS': True,
  # Para invalidar refresh tokens
  'BLACKLIST_AFTER_ROTATION': True,
  'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
  'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
