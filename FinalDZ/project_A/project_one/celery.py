import os
from celery import Celery
from django.conf import settings
from datetime import timezone
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_one.settings')

app = Celery('project_one')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

#app.conf.timezone = timezone.utc
app.conf.beat_schedule = {
    'low-stock-check': {
        'task':  'shop.tasks.notify.low_stock_products',
        'schedule': crontab(minute='*/5'),
    }
}