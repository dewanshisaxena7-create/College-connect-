import os
from pathlib import Path
import dj_database_url
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-development-key-do-not-use-in-prod')
DEBUG = True

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# CSRF Trusted Origins - Handles dynamic Cloudflare tunnel URLs
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]
# Add dynamic tunnel URL if provided via environment variable
CLOUDFLARE_TUNNEL_URL = os.environ.get("CLOUDFLARE_TUNNEL_URL")
if CLOUDFLARE_TUNNEL_URL:
    CSRF_TRUSTED_ORIGINS.append(CLOUDFLARE_TUNNEL_URL)

# Secure Proxy Settings for Cloudflare
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# Security Settings (Enabled when running via tunnel)
if CLOUDFLARE_TUNNEL_URL:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = False # Cloudflare handles the redirect

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
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

ROOT_URLCONF = 'college_connect.urls'

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

WSGI_APPLICATION = 'college_connect.wsgi.application'

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://devanshi:nyXWgJ4XrewdN1ooRrft0IuZ8y0lr6MT@dpg-d80ej10g4nts73f6dmjg-a.singapore-postgres.render.com/my_project_db_fwlx")

DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600, conn_health_checks=True, ssl_require=True)
}

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]



LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# For testing locally, print emails to the terminal instead of sending real ones
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# REAL EMAIL CONFIGURATION
# (To make this work, you MUST put your Gmail and App Password below)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'dewanshi.saxena7@gmail.com'
EMAIL_HOST_PASSWORD = 'ujerbfmnulnigans'
