import os

# Database Connection Settings
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ev_game_db',
            'USER': '',             # add your db username here
            'PASSWORD': '',         # add your db password here
            'HOST': 'localhost',
            'PORT': '3306',
            }
        }

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# Logging Settings
here = lambda *x: os.path.join(os.path.dirname(os.path.realpath(__file__)), *x)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': here('debug.log'),
        },
        'stream_to_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers':{
        'console_logger':{
            'handlers': ['stream_to_console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'file_logger':{
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}