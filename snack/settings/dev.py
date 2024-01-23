import os

from .base import *

DEBUG = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_DATABASE_NAME'),
        'USER': os.getenv('DB_USERNAME'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'snack-postgres',
        'PORT': '5432',
    }
}


STATIC_URL = 'static/'
STATIC_ROOT = 'static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

CELERY_BROKER_URL = 'redis://snack-redis:6379'
CELERY_RESULT_BACKEND = 'redis://snack-redis:6379'
