import os

from .settings import *

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "fjgjgdgjsttigmvvmwpiegjsg")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}
