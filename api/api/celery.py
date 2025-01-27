import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
# DJANGO_SETTINGS_MODULE is an environment variable 
# that tells Django which settings module to use.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

# create a new Celery instance
# The first argument to the Celery() function is the 
# name of the Celery instance. This is usually the name of the
# django project, in which the Celery App lies.
app = Celery('api')

# Load settings from Django settings file using the 'CELERY' namespace.
# django.conf:settings is the default settings module for Django.
# CELERY namespace means that all Celery settings in settings.py
# needs to be prefixed with CELERY_

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
