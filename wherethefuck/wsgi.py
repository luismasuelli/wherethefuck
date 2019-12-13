"""
WSGI config for wherethefuck project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

major, minor = sys.version_info.major, sys.version_info.minor
if major < 3 or major == 3 and minor < 5:
    raise RuntimeError("This application only works on Python 3.5 or greater due to some involved dependencies")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wherethefuck.settings')

application = get_wsgi_application()
