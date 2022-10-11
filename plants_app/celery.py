# from __future__ import absolute_import, unicode_literals
#
# import os
# import main.tasks
# from celery import Celery
# from celery.schedules import crontab
# from django.conf import settings
#
# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plants_app.settings')
#
# app = Celery('plants_app')
# app.conf.enable_utc = False
# app.conf.update(timezone='Europe/Warsaw')
#
# # Using a string here means the worker doesn't have to serialize the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys should have a `CELERY_` prefix.
# app.config_from_object(settings, namespace='CELERY')
#
# # Load task modules from all registered Django apps.
# # Celery Beat tasks registration (60 means that every 1 minute it will be called)
# app.conf.beat_schedule = {
#     'Send_mail_to_Client': {
#         'task': 'main.tasks.send_mail_task',
#         'schedule': 60.0,
#     }
# }
#
# app.autodiscover_tasks()
#
#
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds
#     sender.add_periodic_task(10, test.s('hello'), name='add every 10')
#
#     # Calls test('world') every 60 seconds
#     sender.add_periodic_task(60, test.s('world'), expires=10)
#
#     # Executes every Monday morning at 8:30 a.m.
#     sender.add_periodic_task(crontab(hour=8, minute=30, day_of_week=1), test.s('Happy Mondays'))
#
#
# @app.task
# def test(arg):
#     print(arg)
#
#
# @app.task
# def add(x, y):
#     z = x + y
#     print(z)
#
#
# app.conf.beat_schedule = {
#     'add-every-60-seconds': {
#         'task': 'task.add',
#         'schedule': 60,
#         'args': (16, 16)
#     },
# }
#
# # task-the name of the task to execute
# # schedule-the frequency od execution (number of seconds as int, timedelta or crontab)
# # args-positional arguments (list or tuple)
# # kwargs-keyword arguments (dict)
#
#
# # crontab schedules:
#
# app.conf.beat_schedule = {
#     # Executes every Tuesday morning at 10:30 a.m.
#     'add-every-tuesday-morning': {
#         'task': 'tasks.add',
#         'schedule': crontab(hour=10, minute=30, day_of_week=2),
#         'args': (16, 16),
#     },
# }
