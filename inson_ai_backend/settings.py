import os
from datetime import timedelta
from pathlib import Path

from corsheaders.defaults import default_headers
from dotenv import load_dotenv

load_dotenv(override=True)

BASE_HOST = os.environ.get("BASE_HOST", default="localhost")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY", default="foo")

DEBUG = os.environ.get("DEBUG") == "1"

ALLOWED_HOSTS = ["*"]

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PACKAGES = [
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
]

PROJECT_APPS = [
    "main",
]

INSTALLED_APPS = DJANGO_APPS + PACKAGES + PROJECT_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

ROOT_URLCONF = "inson_ai_backend.urls"
WSGI_APPLICATION = "inson_ai_backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("SQL_DB"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Rest framework

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework.authentication.SessionAuthentication',
    ),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    "DATETIME_FORMAT": "%d-%m-%Y, %H:%M",
    "DATE_FORMAT": "%d-%m-%Y",
    "TIME_FORMAT": "%H:%M",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Hakathon INSON.AI API",
    "DESCRIPTION": "",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "DISABLE_ERRORS_AND_WARNINGS": True,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": os.getenv("LOG_LEVEL", "DEBUG"),
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "all_logs.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "apps": {
            "handlers": ["file"],
            "level": os.getenv("PROJECT_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["file"],
        "level": os.getenv("PROJECT_LOG_LEVEL", "INFO"),
        "propagate": False,
    },
}

# Internationalization

TIME_ZONE = "Asia/Tashkent"

LANGUAGE_CODE = "ru"

USE_I18N = True

USE_TZ = False

gettext = lambda s: s

LANGUAGES = (
    ("ru", gettext("Russia")),
    ("en", gettext("English")),
    ("uz", gettext("Uzbek")),
)


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# SERVER SETTINGS

CORS_ALLOW_ALL_ORIGINS = True
USE_X_FORWARDED_HOST = True
# CSRF_TRUSTED_ORIGINS = ['https://']

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DATE FORMATS

DATE_FORMAT = ("d-m-Y",)
TIME_FORMAT = "HH:mm"
DATETIME_FORMAT = "HH:mm, d-m-Y"
DATE_INPUT_FORMATS = ("d-m-Y",)
DATETIME_INPUT_FORMATS = "d-m-Y, HH:mm"

# CORS
CORS_ALLOW_ALL_ORIGINS = True
USE_X_FORWARDED_HOST = True


SPEECH_KEY = "8db7642eab544a81b2129aab2fcfe43e"
SPEECH_REGION = "eastasia"
TOGETHER_KEY = "02d53a82e160ac94b919de8f680d3e7186aee4a5d97683e80f189a985bda361a"