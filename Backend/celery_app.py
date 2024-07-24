from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Load Django settings into Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Ensure that Celery Beat checks for tasks every minute
app.conf.beat_max_loop_interval = 60  # Check for due tasks every 1 minute

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Optional: Define your periodic tasks directly here, if not using Django settings
app.conf.beat_schedule = {
    'fetch-bazaar-data-every-minute': {
        'task': 'myapp.tasks.fetch_bazaar_data',
        'schedule': crontab(minute='*/1'),  # Runs every minute
    },
}

@app.task(bind=True)
def fetch_bazaar_data(self):
    # Task implementation here
    pass
