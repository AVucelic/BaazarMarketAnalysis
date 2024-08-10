from celery import Celery
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_routes={
        'myapp.tasks.fetch_bazaar_data': {'queue': 'bazaar'},
    },
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
