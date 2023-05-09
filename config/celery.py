# import os
# from celery.schedules import crontab

# from celery import Celery

# # Set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# app = Celery('config')

# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django apps.
# app.autodiscover_tasks()


# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

# from celery.schedules import crontab

# app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     'check-birthday-every-day': {
#         'task': 'bio.tasks.check_birthday',
#         'schedule': crontab(hour=0, minute=0),
#     },
# }