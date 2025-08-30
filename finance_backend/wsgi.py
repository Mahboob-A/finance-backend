"""
WSGI config for finance_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# TODO: Remove this when the project is ready for production.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_backend.settings.local')

application = get_wsgi_application()
