#from __future__ import annotations
import logging
from .base import *

# Включаем режим отладки для локальной разработки
DEBUG = True

# Разрешаем любые хосты локально
ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Локальная база данных из Docker Compose
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PG_NAME'),
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT'),
        'OPTIONS': {
            'options': '-c timezone=UTC'
        }
    }
}

# Локальное хранилище медиа-файлов через MinIO и стандартный бэкенд статики
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {
            'access_key': AWS_ACCESS_KEY_ID,
            'secret_key': AWS_SECRET_KEY,
            'endpoint_url': 'http://e_commerce_minio:9000',  # Локальный контейнер MinIO
            'bucket_name': AWS_STORAGE_BUCKET_NAME,
        },
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

# Локальный Redis для Django Channels (WebSockets)
CHANNELS_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [{'redis': 6379}]
        }
    }
}

# Локальный Redis для кэширования данных и страниц
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'TIMEOUT': 5*60,
        'KEY_PREFIX': 'ecom',
    },
    'page_cache': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/2',
        'TIMEOUT': 15*60,
        'KEY_PREFIX': 'ecom_page',
    }
}

# Отключаем строгое SSL-шифрование на локальном компьютере, чтобы куки не пропадали
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

CSRF_TRUSTED_ORIGINS = [
    'https://localhost',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
CSRF_COOKIE_SAMESITE = None
SESSION_COOKIE_SAMESITE = None

# Локальное логирование: создаем папку logs и пишем ошибки/запросы в файлы
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {module} {process:d} {thread:d} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[{levelname}] {asctime} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'filters': {
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'},
    },
    'handlers': {
        'console': {'level': 'INFO', 'class': 'logging.StreamHandler', 'formatter': 'simple'},
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'error.log',
            'maxBytes': 1024*1024*10, 'backupCount': 10, 'formatter': 'verbose'
        },
        'file_django': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'django.log',
            'maxBytes': 1024*1024*10, 'backupCount': 10, 'formatter': 'verbose'
        },
        'file_db': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'database.log',
            'maxBytes': 1024*1024*10, 'backupCount': 10, 'formatter': 'verbose',
            'filters': ['require_debug_true']
        },
        'file_all': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'all.log',
            'maxBytes': 1024*1024*10, 'backupCount': 10, 'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {'handlers': ['console', 'file_error', 'file_all'], 'level': 'INFO', 'propagate': False},
        'django': {'handlers': ['console', 'file_django', 'file_error'], 'level': 'DEBUG', 'propagate': False},
        'django.db.backends': {'handlers': ['file_db'], 'level': 'DEBUG', 'propagate': False},
        'shopname': {'handlers': ['console', 'file_all', 'file_error'], 'level': 'DEBUG', 'propagate': False},
    }
}

# Инициализация Sentry для локальной разработки (окружение development)
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    dsn="https://1f143d5547dcbec67e60a67e0a59413d@o4511390442127360.ingest.de.sentry.io/4511390482497616",
    integrations=[
        DjangoIntegration(),
        LoggingIntegration(event_level=logging.ERROR),
        CeleryIntegration(),
        RedisIntegration()
    ],
    attach_stacktrace=True,
    environment='development',
    send_default_pii=True,
)