#from __future__ import annotations
import os
import logging
from .base import *

# Жестко отключаем режим отладки для безопасности
DEBUG = False

# Секретный ключ берется строго из переменных окружения сервера
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# Разрешенные хосты вашего приложения (передаются через запятую, например: app.railway.app,://render.com)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# База данных продакшена (читает переменные, заданные в облаке)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PG_NAME'),
        'USER': os.getenv('PG_USER'),
        'PASSWORD': os.getenv('PG_PASSWORD'),
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT'),
        'CONN_MAX_AGE': 600,  # Постоянные соединения с БД для ускорения работы
        'OPTIONS': {
            'options': '-c timezone=UTC'
        }
    }
}

# Динамическая обработка одной переменной REDIS_URL для облака
# На хостингах обычно выдают одну строку вида: redis://default:password@host:port
REDIS_BASE_URL = os.getenv('REDIS_URL', 'redis://redis:6379')

# Если URL заканчивается на номер базы данных (/0, /1), отрезаем его для ручного распределения
if REDIS_BASE_URL.endswith('/0') or REDIS_BASE_URL.endswith('/1') or REDIS_BASE_URL.endswith('/2'):
    REDIS_BASE_URL = REDIS_BASE_URL.rsplit('/', 1)[0]

# Разводим кэш и вебсокеты по разным базам Redis в продакшене
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f"{REDIS_BASE_URL}/1",
        'TIMEOUT': 5*60,
        'KEY_PREFIX': 'ecom',
    },
    'page_cache': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f"{REDIS_BASE_URL}/2",
        'TIMEOUT': 15*60,
        'KEY_PREFIX': 'ecom_page',
    }
}

# Настройка Django Channels для продакшн Redis (база 0)
CHANNELS_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [f"{REDIS_BASE_URL}/0"]
        }
    }
}

# Настройки хранилищ для продакшена: default уходит в S3, staticfiles — в кэширующий WhiteNoise
STORAGES = {
    'default': {
        'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
        'OPTIONS': {
            'access_key': AWS_ACCESS_KEY_ID,
            'secret_key': AWS_SECRET_KEY,
            'endpoint_url': os.getenv('AWS_S3_ENDPOINT_URL'),
            'bucket_name': AWS_STORAGE_BUCKET_NAME,
        },
    },
    'staticfiles': {
        # WhiteNoise сжимает файлы (gzip/brotli) и заставляет браузеры кэшировать их "навечно"
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# --- Жесткие настройки безопасности (Security Headers) ---
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Передает Django флаг, что запрос пришел в контейнер по защищенному HTTPS от прокси-сервера облака
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# HTTP Strict Transport Security (HSTS) для принудительного HTTPS в браузерах
SECURE_HSTS_SECONDS = 31536000  # 1 год
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Доверенные домены для CSRF (передаются строкой через запятую)
if os.getenv('CSRF_TRUSTED_ORIGINS'):
    CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(',')

# Логирование на продакшене: пишем строго в стандартный вывод (консоль контейнера)
# Файловые логи на Ephemeral дисках облака запрещены, так как они стираются при перезапуске
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[{levelname}] {asctime} {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'django': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
        'shopname': {'handlers': ['console'], 'level': 'INFO', 'propagate': False},
    }
}

# Инициализация Sentry для продакшена (окружение production-hillel)
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
    environment='production-hillel',
    send_default_pii=True,
)
