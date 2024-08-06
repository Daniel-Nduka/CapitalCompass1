from .settings_base import *

# Production-specific settings
SECRET_KEY = env('DJANGO_SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['capitalcompass.pythonanywhere.com'])



SITE_ID = 2
