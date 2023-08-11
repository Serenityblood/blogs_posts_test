import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_blogs.settings")
app = Celery("api_blogs")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'run-me-every-ten-seconds': {
        'task': 'api.tasks.send_posts',
        'schedule': 86400
    },
}
app.conf.timezone = 'UTC'
