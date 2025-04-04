"""
Django settings for utility_services project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key
import pymysql
pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'x24112682-bookingapp-devops.eba-qbftmn5g.ap-southeast-2.elasticbeanstalk.com/','*'
    ]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "services_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "utility_services.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'services_app/templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "utility_services.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.environ.get('DB_NAME', ''),       # DB name
        'USER': os.environ.get('DB_USER', ''),       # DB username
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),  # DB password
        'HOST': os.environ.get('DB_HOST', ''),       # DB host
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}

""" DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'x24112682-utility-rds',       
        'USER': 'admin',       
        'PASSWORD': 'x24112682-utility-rds',  
        'HOST': 'x24112682-utility-rds.cid6gtv3k6ak.ap-southeast-2.rds.amazonaws.com',      
        'PORT': 3306,
    }
} """


""" 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'x24112682-utility-rds',
        'USER': 'admin',
        'PASSWORD': 'x24112682-utility-rds',
        'HOST': 'x24112682-utility-rds.cid6gtv3k6ak.ap-southeast-2.rds.amazonaws.com',
        'PORT': '3306',
        'TEST': {
            'NAME': 'test_utility',  # Use a different name for the test database
            'CHARSET': 'utf8mb4',  # Ensures utf8 support (optional but recommended)
            'COLLATION': 'utf8mb4_unicode_ci',
        },
    }
} """

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SESSION_COOKIE_AGE = 1800  
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
