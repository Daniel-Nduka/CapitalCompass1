import os

ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'local')

if ENVIRONMENT == 'production':
    from .settings_production import *
else:
    from .settings_local import *
