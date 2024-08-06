from .settings_base import *

# Local-specific settings
SECRET_KEY = env('DJANGO_SECRET_KEY', default='your-local-secret-key')

DEBUG = True
ALLOWED_HOSTS = []


SITE_ID = 1
