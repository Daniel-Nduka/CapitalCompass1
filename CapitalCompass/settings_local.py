from .settings_base import *

# Local-specific settings
SECRET_KEY = env('DJANGO_SECRET_KEY', default='your-local-secret-key')

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SITE_ID = 2
