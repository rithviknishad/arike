import os
from datetime import timedelta

from django.conf import settings

from celery import Celery
from celery.task import periodic_task

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arike.settings.dev")
app = Celery("arike")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
