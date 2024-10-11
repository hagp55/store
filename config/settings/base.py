import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
COUNT_PER_PAGE = int(os.getenv("COUNT_PER_PAGE"))
ALLOWED_HOSTS = [os.getenv("ALLOWED_HOSTS")]

NAME = os.getenv("MYSQL_DATABASE")
USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("DB_HOST")

LANGUAGE_CODE = os.getenv("LANGUAGE_CODE")
TIME_ZONE = os.getenv("TIME_ZONE")
SITE_TITLE = os.getenv("SITE_TITLE")
SITE_HEADER = os.getenv("SITE_HEADER")
INDEX_TITLE = os.getenv("INDEX_TITLE")

DEBUG = False

AUTH_USER_MODEL = "accounts.User"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # My app
    "store.apps.StoreConfig",
    "telebot.apps.TelebotConfig",
    "accounts.apps.AccountsConfig",
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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processor.get_context_data",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": NAME,
        "USER": USER,
        "PASSWORD": PASSWORD,
        "HOST": HOST,
        "PORT": "3306",
    }
}


LANGUAGE_CODE = LANGUAGE_CODE

TIME_ZONE = TIME_ZONE

USE_I18N = True

USE_TZ = True


MEDIA_URL = "media/"
STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = (BASE_DIR / "config/static",)


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR / "django_cache",
    }
}


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# For Context Processor
# HEAD
title = os.getenv("title")
description = os.getenv("description")
keywords = os.getenv("keywords")
author = os.getenv("Author")
copyright = os.getenv("Copyright")
address = os.getenv("Address")
# Social media
whatsapp = os.getenv("whatsapp")
telegram = os.getenv("telegram")
vk = os.getenv("vk")
# Contacts
address = os.getenv("address")
phone = os.getenv("phone")
phone_preview = os.getenv("phone_preview")
email = os.getenv("email")
map = os.getenv("map")
