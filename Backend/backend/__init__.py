# backend/__init__.py

from __future__ import absolute_import, unicode_literals

# Import Celery app so that it's available for Django to use
from .celery_app import app as celery_app

__all__ = ('celery_app',)
