"""
WSGI config for dc_bikelane_grafiti_map project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dc_bikelane_grafiti_map.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
