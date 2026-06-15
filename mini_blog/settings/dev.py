from .base import *

# Celery Eager Mode for Development
# Tasks execute synchronously instead of being queued
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True