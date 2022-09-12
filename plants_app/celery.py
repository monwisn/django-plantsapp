from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plants_app.settings')

app = Celery('plants_app')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Warsaw')

# Using a string here means the worker doesn't have to serialize the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django apps.
# Celery Beat tasks registration (60 means that every 1 minute it will be called)
app.conf.beat_schedule = {'Send_mail_to_Client': {'task': 'main.tasks.send_mail_task', 'schedule': 60.0, }}

app.autodiscover_tasks()
