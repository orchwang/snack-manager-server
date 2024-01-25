import os

from fakeredis import FakeConnection

from .base import *

DEBUG = True
CELERY_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': [
            'redis://127.0.0.1:6379',
        ],
        'OPTIONS': {'connection_class': FakeConnection},
    }
}


STATIC_URL = 'static/'

STATIC_ROOT = 'static/'


CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
