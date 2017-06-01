"""
Django settings for EVChargingGame project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

### settings that are not environment dependent
try:
    from local_settings import *
except ImportError:
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'updatethisb4=38)ui)x)wu@r5j(y0&b3r6wpi34vu%4&9fgbl6#x0q@n54cupdatethis'

ALLOWED_HOSTS = ['www.bid2charge.com', 'bid2charge.com', 'www.bid2charge.co.uk', 'bid2charge.co.uk',]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
ACCOUNT_USER_MODEL_USERNAME_FIELD = ("username")
ACCOUNT_USER_MODEL_EMAIL_FIELD = ("email")

# Custom User and Authentication Backend

AUTHENTICATION_BACKENDS = (
    # Authentication through Djano admin
    'django.contrib.auth.backends.ModelBackend',
    # Authentication through 'allauth'
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_PASSWORD_MIN_LENGTH = 1

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
    'django.core.context_processors.static'
)

TEMPLATE_DIRS=(
    os.path.join(BASE_DIR, 'templates'),
)

# Overriding the Auth User Model
AUTH_USER_MODEL = 'webapp.EVUser'

# Auth and allauth settings
#SOCIALACCOUNT_AUTO_SIGNUP = False
LOGIN_REDIRECT_URL = '/webapp/home'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'js_sdk' #instead of 'oauth2'
    }
}

# The SITE_ID setting specifies the database ID of the site
# object associated with that particular #settings file
SITE_ID = 1

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp',
    'subscribe',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'south'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'EVChargingGame.urls'

WSGI_APPLICATION = 'EVChargingGame.wsgi.application'

SOUTH_TESTS_MIGRATE = False

# Email Configuration
EMAIL_HOST = 'smtp.ecs.soton.ac.uk'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = '
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = ''

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join (BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "webapp/static"),
    os.path.join(BASE_DIR, "subscribe/static"),
    os.path.join(BASE_DIR, "common-static"),
)
