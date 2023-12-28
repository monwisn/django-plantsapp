# absolute_import - all imports are treated as absolute, rather than relative imports.
from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plants_app.settings')

app = Celery('plants_app')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Warsaw')

# Using a string here means the worker doesn't have to serialize the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys should have a `CELERY_` prefix.
app.config_from_object(settings, namespace='CELERY')

# Load task modules from all registered Django apps.
# Celery Beat tasks registration (60 means that every 1 minute it will be called)
app.conf.beat_schedule = {
    'Send_mail_to_Client': {
        'task': 'main.tasks.send_mail_task',
        'schedule': crontab(hour='21', minute='30', day_of_week='2'),
    },
}

# Celery will automatically discover tasks from all of django apps.
app.autodiscover_tasks(settings.INSTALLED_APPS)


# task: the name of the task to execute.
# schedule: the frequency od execution (number of seconds as int, timedelta or crontab)
# args: positional arguments (list or tuple)
# kwargs: keyword arguments (dict)

# Crontab schedules:
@app.task(bind=True)
def debug_test(arg):
    print(f'Request: {arg.request}')


@app.task
def add(x, y):
    z = x + y
    print(z)


app.conf.beat_schedule = {
    'add-every-60-seconds': {
        'task': 'task.add',
        'schedule': 60,
        'args': (16, 16)
    },
}

app.conf.beat_schedule = {
    # Executes every Tuesday evening at 8:30 p.m.
    'add-every-tuesday-evening': {
        'task': 'tasks.add',
        'schedule': crontab(hour='20', minute='30', day_of_week='2'),
    }
}

app.conf.beat_schedule = {
    # Executes every Wednesday night at 00:30 a.m.
    'add-every-wednesday-evening': {
        'task': 'tasks.add',
        'schedule': crontab(hour='00', minute='30', day_of_week='3'),
    }
}

app.conf.beat_schedule = {
    'send-mail': {
        'task': 'main.tasks.send_mail_task',
        'schedule': crontab(hour='14', minute='40', day_of_week='3'),
    },
}

app.conf.beat_schedule = {
    'Send_Newsletter': {
        'task': 'main.tasks.send_weekly_newsletters',
        'schedule': crontab(hour='00', minute='35', day_of_week='3'),
    }
}

app.conf.beat_schedule = {
    'Send_reminder_3_days': {
        'task': 'main.tasks.send_reminder_3_days',
        'schedule': crontab(hour='00', minute='50', day_of_week='3')
    }
}
