"""
ASGI config for finance_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# TODO: Remove this when the project is ready for production.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_backend.settings.local')

application = get_asgi_application()
