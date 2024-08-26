import os
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

# Base settings
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'financeapp',
    'registration',
    'django.contrib.sites',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'financeapp.middleware.SelectedBudgetMiddleware',
]

ROOT_URLCONF = 'CapitalCompass.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'financeapp.context_processors.selected_budget',
            ],
        },
    },
]

WSGI_APPLICATION = 'CapitalCompass.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATICFILES_DIRS = [STATIC_DIR, ]
STATIC_URL = '/static/'


# Django Registration settings
REGISTRATION_OPEN = True
REGISTRATION_AUTO_LOGIN = False
LOGIN_REDIRECT_URL = '/overview/'
LOGIN_URL = 'auth_login'

ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window

# Email settings (defaults, can be overridden)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = 'Capital.Compass12@gmail.com'
CONTACT_EMAIL = 'Capital.Compass12@gmail.com'

# Secret key (placeholder, should be overridden in env-specific settings)
SECRET_KEY = env('DJANGO_SECRET_KEY', default='your-default-secret-key')

# Load environment-specific settings
#ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'local')

CSRF_FAILURE_VIEW = 'financeapp.views.csrf_failure'

# settings.py
PLAID_CLIENT_ID = env('PLAID_CLIENT_ID')
PLAID_SECRET = env('PLAID_SECRET')
PLAID_ENV = 'sandbox' 
#PLAID_ENV = 'production'
PLAID_PRODUCTS = ['auth', 'transactions', 'balance'] 
PLAID_COUNTRY_CODES = ["GB"]


