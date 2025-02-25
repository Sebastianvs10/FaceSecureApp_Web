# Autor: Jhohan Sebastian Vargas S
# Fecha: 2025-02-25
# Project: FaceSecureApp

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
