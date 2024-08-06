import os
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

ENVIRONMENT = env('DJANGO_ENVIRONMENT')

if ENVIRONMENT == 'production':
    from .settings_production import *
else:
    from .settings_local import *
