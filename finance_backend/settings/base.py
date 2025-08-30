
from os import getenv, path 
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
from datetime import timedelta

##################### Settings Configuration #####################
# goes to the root of the project where the manage.py file is located
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

APPS_DIR = BASE_DIR / 'core_apps'

local_env_file = path.join(BASE_DIR, '.envs', '.env.local')

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


##################### Application Definition #####################
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_countries',
    'phonenumber_field',
    'drf_spectacular',
    'djoser',
    'cloudinary',
    'django_filters',
    'djcelery_email',
    'django_celery_beat',
]


LOCAL_APPS = ["core_apps.user_auth",
              "core_apps.user_profile",
              "core_apps.common",]

# installed apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

##################### Middleware Configuration #####################
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

##################### Root URL Configuration #####################
ROOT_URLCONF = 'finance_backend.urls'



##################### Templates Configuration #####################
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR / 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



##################### WSGI Configuration #####################
WSGI_APPLICATION = 'finance_backend.wsgi.application'


##################### Database Configuration #####################
# SQLite database configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# postgres database configuration  
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('POSTGRES_DB'),
        'USER': getenv('POSTGRES_USER'),
        'PASSWORD': getenv('POSTGRES_PASSWORD'),
        'HOST': getenv('POSTGRES_HOST'),
        'PORT': getenv('POSTGRES_PORT', '5432'),
    }
}



##################### Passwords Hashing #####################
# Django uses PBKDF2 as the default password hasher, but we can change it to 
# uses argon2 as the default password hasher
# https://docs.djangoproject.com/en/4.2/topics/auth/passwords/#password-hashing
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


##################### Password Validation #####################
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
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


################ Internationalization ###############
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

SITE_ID = 1


################## STATIC FILES #################
STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / 'staticfiles')


################## User Model ##################
AUTH_USER_MODEL = 'user_auth.User'

##################### Misc #####################
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


##################### DRF #####################
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

################## Spectacular Documentation ############
SPECTACULAR_SETTINGS = {
    "TITLE": "Finance Backend API",
    "DESCRIPTION": "Documentation of API endpoints of Finance Backend",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "LICENSE": {
        "name": "MIT License",
        "url": "https://opensource.org/license/mit/",
    },
    # OTHER SETTINGS
    # "SWAGGER_UI_DIST": "SIDECAR",  # shim
    # "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    # "REDOC_DIST": "SIDECAR",
}

##################### Logging Configuration #####################
LOGGING_CONFIG = None # Disable Django's default logging configuration

LOGURU_LOGGING = {
    "handlers": [
        {
            # Logs only DEBUG messages
            "sink": BASE_DIR / "logs" / "debug.log",
            "level": "DEBUG",
            "filter": lambda record: record["level"].name == "DEBUG",
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            "rotation": "10 MB",
            "retention": "30 days",
            "compression": "zip",
            "enqueue": True,
        },
        {
            # Logs INFO and WARNING messages
            "sink": BASE_DIR / "logs" / "info_warning.log",
            "level": "INFO",
            "filter": lambda record: record["level"].name in ("INFO", "WARNING"),
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            "rotation": "10 MB",
            "retention": "30 days",
            "compression": "zip",
            "enqueue": True,
        },
        {
            # Logs ERROR and CRITICAL messages
            "sink": BASE_DIR / "logs" / "error_critical.log",
            "level": "ERROR",
            "filter": lambda record: record["level"].name in ("ERROR", "CRITICAL"),
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            "rotation": "10 MB",
            "retention": "1 month",
            "compression": "zip",
            "enqueue": True,
            "backtrace": True,
            "diagnose": True,
        },
    ],
}

logger.configure(**LOGURU_LOGGING)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "loguru": {
            "class": "log_intercepter.LogInterceptHandler",
        }
    },
    "root": {
        "handlers": ["loguru"],
        "level": "DEBUG",
    }
}


