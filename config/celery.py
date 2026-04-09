from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery
import config.settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send-upcoming-reminders': {
        'task': 'library.tasks.send_upcoming_due_reminders',
        'schedule': crontab(hour=9),
    },
    'send-overdue-notifications': {
        'task': 'library.tasks.send_overdue_notifications',
        'schedule': crontab(hour=9),
    },
}
app.conf.timezone = config.settings.TIME_ZONE
