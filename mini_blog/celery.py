import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mini_blog.settings.dev')

app = Celery('mini_blog')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Celery test task request: {self.request!r}')
    return "Celery is working!"