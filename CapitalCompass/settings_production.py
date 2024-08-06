from .settings_base import *

# Production-specific settings
SECRET_KEY = env('DJANGO_SECRET_KEY')

DEBUG = False
ALLOWED_HOSTS = ['capitalcompass.pythonanywhere.com']



SITE_ID = 2
