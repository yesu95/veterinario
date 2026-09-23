"""
WSGI config for veterinario_core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinario_core.settings')

application = get_wsgi_application()
# Envuelve la aplicación e indícale dónde buscar los archivos recolectados
application = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), '../staticfiles'))

app = application  # Vercel busca la variable 'app'