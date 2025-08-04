
from os import getenv, path 
from dotenv import load_dotenv

from .base import *  # noqa: F403, F401
from .base import BASE_DIR

# local env settings 
local_env_file = path.join(BASE_DIR, '.envs', '.env.local')

if path.isfile(local_env_file):
    load_dotenv(local_env_file)


##################### Secret Key and Host Configuration #####################
SECRET_KEY = getenv('SECRET_KEY')

DEBUG = getenv('DEBUG', 'False').lower() in ('true', '1', 'yes')

SITE_NAME = getenv('SITE_NAME', 'Finance Backend')

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

ADMIN_URL = getenv('ADMIN_URL', 'admin')

##################### Email Configuration #####################
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(getenv('EMAIL_PORT', 1025))
DEFAULT_FROM_EMAIL = getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost')

EMAIL_USE_TLS = getenv('EMAIL_USE_TLS', 'False').lower() in ('true', '1', 'yes')
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD', '')


##################### Domain Configuration #####################
DOMAIN = getenv('DOMAIN', 'localhost')
if not DOMAIN.startswith('http'):
    DOMAIN = f'http://{DOMAIN}' 
    if not DOMAIN.endswith('/'):
        DOMAIN += '/'   

##################### Image Upload Configuration #####################
MAXIMUM_UPLOAD_SIZE = 1 * 1024 * 1024  # 1 MB

##################### CSRF Configuration #####################
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:8080", "http://127.0.0.1:8080"]


##################### Authentication Configuration #####################
LOCKOUT_DURATION = timedelta(minutes=1)  # Lockout duration for failed login attempts, 1 for develo"http://127.0.0.1:8000"pment, increase for production

LOGIN_ATTEMPTS = 3  # Number of allowed login attempts before lockout, increase for production

OTP_EXPIRATION = timedelta(minutes=1)  # OTP expiration time, increase for production


