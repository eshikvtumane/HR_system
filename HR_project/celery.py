from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HR_project.settings')


from django.conf import settings

app = Celery('hr_project')

app.config_from_object('django.conf:settings')
app.config_from_object('HR_project.celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS )
