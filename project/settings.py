import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "blog.apps.BlogConfig",
    "core.apps.CoreConfig",
    "dashboard.apps.DashboardConfig",
    "feedreader.apps.FeedreaderConfig",
    "pages.apps.PagesConfig",
    "timers.apps.TimersConfig",
    "tools.apps.ToolsConfig",
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

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.normpath(os.path.join(BASE_DIR, "project", "templates"))],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("AHERNP_DATABASE_NAME"),
        "USER": os.environ.get("AHERNP_DATABASE_USER"),
        "PASSWORD": os.environ.get("AHERNP_DATABASE_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

# USE_I18N = True

# USE_L10N = True

USE_TZ = True

STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, "static"))
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.normpath(os.path.join(BASE_DIR, "site_assets"))]

MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, "media"))
MEDIA_URL = "/media/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"ahernp.com": {"format": "%(message)s (%(module)s)"}},
    "handlers": {
        "db_log": {
            "level": "INFO",
            "class": "core.log.DbLogHandler",
            "formatter": "ahernp.com",
        }
    },
    "loggers": {
        "core.management.commands.delete_logs": {
            "handlers": ["db_log"],
            "level": "INFO",
            "propagate": True,
        },
        "feedreader.utils": {
            "handlers": ["db_log"],
            "level": "INFO",
            "propagate": True,
        },
        "feedreader.management.commands.poll_feeds": {
            "handlers": ["db_log"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

TIME_ZONE = "Europe/London"

LOGIN_URL = "/admin/login"

SITE_NAME = "ahernp.com"
HOMEPAGE_SLUG = "ahernp-com"
BLOG_ROOT_SLUG = "blog"

# Dashboard
LOG_ENTRIES_TO_SHOW = 5

# Feedreader
MAX_ENTRIES_SAVED = 100
MAX_ENTRIES_SHOWN = 100
MAX_DAYS_SHOWN = 1
MAX_DAYS_AGE = 3


REST_FRAMEWORK = { 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' }
