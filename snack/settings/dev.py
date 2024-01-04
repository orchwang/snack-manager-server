import os

from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_DATABASE_NAME"),
        "USER": os.getenv("DB_USERNAME"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": "snack-postgres",
        "PORT": "5432",
    }
}


STATIC_URL = "static/"

STATIC_ROOT = "static/"
