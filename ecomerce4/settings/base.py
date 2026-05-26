
import os
#from __future__ import annotations
from datetime import timedelta
import certifi
from pathlib import Path
from dotenv import load_dotenv
from celery.schedules import crontab

# Загрузка переменных окружения
load_dotenv()
os.environ['SSL_CERT_FILE'] = certifi.where()

# Путь к корню проекта (теперь папка settings глубже, поэтому три .parent)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Секретный ключ по умолчанию для локальной разработки
SECRET_KEY = 'django-insecure-s9@76-smwycjvsgw=(&7(az0@8gd(2&899z=*vnky3i-6$7uaw'

# Список установленных приложений
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'corsheaders',
    'storages',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'i18n',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'mptt',
    'shopname.apps.ShopnameConfig',
    'payments.apps.PaymentsConfig',
    'shop_chat.apps.ShopChatConfig'
]

# Список Middleware (WhiteNoise уже на месте)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'ecomerce2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

# Использование ASGI для Django Channels
ASGI_APPLICATION = 'ecomerce2.asgi.application'

SITE_ID = 1

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Интернационализация и языки
LANGUAGE_CODE = 'uk'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
USE_L10N = True

LANGUAGES = [
    ('uk', 'Українська'),
    ('en', 'English'),
    ('ar', 'Arabic'),
]
LANGUAGES_BIDI = ['ar']
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# Настройки статики по умолчанию
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Кастомные переменные вашего интернет-магазина
SOME_DUMB_VALUE = 'dumb_value'
CART_SESSION_ID = 'cart'
LOW_STOCK_THRESHOLD = 5

# Платежные ключи Stripe
STRIPE_PUBLIC_KEY = 'pk_test_'
STRIPE_API_KEY = 'sk_test_'

# Настройки отправки почты
DEFAULT_FROM_EMAIL = 'admin@shopname.com'
APP_MAIL_PWD = ''
EMAIL_HOST_USER = 'mogaalexandr@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = '://gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Настройки Celery и периодических задач (Beat)
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_BEAT_SCHEDULE = {
    'check-low-stock-every-minute': {
        'task': 'shopname.tasks.notify_low_stock_products',
        'schedule': crontab(),
    },
    'clear-expired-sessions-daily': {
        'task': 'shopname.tasks.clear_django_sessions_task',
        'schedule': crontab(hour=0, minute=0),
    },
}
CELERY_TIMEZONE = "Europe/Kyiv"

# Конфигурация Django REST Framework (DRF)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'shopname.api.authentication.EcommerceJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

CORS_ALLOW_ALL_ORIGINS = True

# Конфигурация Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=15),
    'AUTH_HEADER_TYPES': ('Hillel',),
    'USER_ID_FIELDS': ['id', 'username'],
}

# Базовые переменные для облачного хранилища AWS S3 / MinIO
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False