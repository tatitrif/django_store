import os
import sys
from pathlib import Path

from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't add DEBUG to env in production
DEBUG = os.environ.get("DEBUG", False) == "True"

# Admin
ADMIN_URL = os.getenv("ADMIN_URL", "admin/")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1, 10.0.2.2, localhost").split(", ")

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# APPS
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]
THIRD_PARTY_APPS = [
    "captcha",
    "tinymce",
    "mptt",
    "rest_framework",
    "django_filters",
]
LOCAL_APPS = [
    "store.apps.StoreConfig",
    "catalog.apps.CatalogConfig",
    "account.apps.AccountConfig",
    "cart.apps.CartConfig",
    "order.apps.OrderConfig",
    "chat.apps.ChatConfig",
]
INSTALLED_APPS = (
    [
        "daphne",
    ]
    + DJANGO_APPS
    + THIRD_PARTY_APPS
    + LOCAL_APPS
)

# MIDDLEWARE
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS = [
        "debug_toolbar",
        "django_extensions",
    ] + INSTALLED_APPS

if DEBUG:
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ] + MIDDLEWARE

# for debug_toolbar
INTERNAL_IPS = [
    "127.0.0.1",
    "127.0.0.1",
    "10.0.2.2",
    "localhost",
]

USE_DOCKER = os.environ.get("USE_DOCKER", False) == "True"

if USE_DOCKER and DEBUG:

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    }

# SCHEME for DB
SCHEME_DB = ""
SCHEME = os.getenv("SCHEME", "")
if SCHEME:
    SCHEME_DB = SCHEME + "'.'"

if os.getenv("DATABASE_URL", default=None):
    db_settings = os.getenv("DATABASE_URL")
elif os.getenv("DJANGO_POSTGRES_DB", default=None):
    db_settings = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DJANGO_POSTGRES_DB"),
        "USER": os.getenv("DJANGO_POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DJANGO_POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.getenv("DJANGO_POSTGRES_PORT", 5432),
    }
else:
    db_settings = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / os.getenv("DB_NAME", "db.sqlite3"),
    }

if "test" in sys.argv:
    db_settings = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "TEST_CHARSET": "UTF8",
        "TEST_NAME": ":memory:",
    }

    CAPTCHA_TEST_MODE = True  # Disables captcha

DATABASES = {"default": db_settings}

# PASSWORDS
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
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "store.context_processors.get_store_context",
                "cart.context_processors.cart",
            ],
        },
    },
]

# LOGGING
LOG_FILENAME = os.getenv("LOG_FILENAME", BASE_DIR / "logs.log")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": LOG_FILENAME,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": [
                "console",
            ],
            "level": "INFO",
            "propagate": True,
        },
        "root": {
            "handlers": [
                "mail_admins",
                "console",
                "file",
            ],
            "level": "WARNING",
            "propagate": True,
        },
    },
}

# Internationalization
TIME_ZONE = os.getenv("TIME_ZONE", "Europe/Moscow")
USE_I18N = True
USE_TZ = True
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "ru-RU")
LANGUAGES = [
    ("en", _("English")),
    ("ru", _("Russian")),
]

# Localization
LOCALE_PATHS = [BASE_DIR / "locale"]

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# The URL to use when referring to static files (where they will be served from)
STATIC_URL = "static/"

# MEDIA
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = 1

DEFAULT_CURRENCY_SYMBOL = "₽"

PAGINATE_BY = os.environ.get("PAGINATE_BY", 2)

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 2,
}

AUTHENTICATION_BACKENDS = [
    "social_core.backends.github.GithubOAuth2",
    "django.contrib.auth.backends.ModelBackend",
    "account.authentication.EmailAuthBackend",
]

AUTH_USER_MODEL = "account.User"

LOGIN_REDIRECT_URL = "account:profile"
LOGOUT_REDIRECT_URL = "store:home"
LOGIN_URL = "account:login"

EMAIL_BACKEND_console = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND_smtp = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_BACKEND = EMAIL_BACKEND_console if DEBUG else EMAIL_BACKEND_smtp

EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "admin@example.com")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.yandex.ru")
EMAIL_PORT = 465
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "users.pipeline.new_users_handler",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)

SOCIAL_AUTH_GITHUB_KEY = os.environ.get("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = os.environ.get("SOCIAL_AUTH_GITHUB_SECRET")

CART_SESSION_ID = "cart"

CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")

CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
