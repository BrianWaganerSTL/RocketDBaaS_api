SECRET_KEY = 'lwgooy5r7-7roe5d5m6g5w-zuzg+957ger!y-9)ccxewyr_-ac'

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'RocketDBaaS',
        'USER': 'postgres',
        'PASSWORD': 'Pineapple!!!',
        'HOST':'localhost',
        'PORT':'5432',
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DJANGO_LOG_LEVEL=DEBUG
# LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}  {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'C:/logs/RocketDBaaS_API_debug.log'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

MINION_PORT = 8000
