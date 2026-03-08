"""WSGI config for DataPulse project."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datapulse.settings.dev")

# Import after Django setup
from datapulse.tracing import setup_tracing  # noqa: E402

setup_tracing()

application = get_wsgi_application()
