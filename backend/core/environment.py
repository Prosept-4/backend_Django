import os

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

################################################
#               Settings
################################################

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(' ')
DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite3')  # sqlite3 или postgresql
DEBUG = os.getenv('DEBUG', 'False') == 'True'
IS_LOGGING = os.getenv('IS_LOGGING', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

################################################
#               Settings - Email
################################################

EMAIL_HOST_ENV = os.getenv('EMAIL_HOST')
EMAIL_PORT_ENV = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS_ENV = bool(os.getenv('EMAIL_USE_TLS', 'False'))
EMAIL_USE_SSL_ENV = bool(os.getenv('EMAIL_USE_SSL', 'True'))
EMAIL_HOST_USER_ENV = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD_ENV = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL_ENV = os.getenv('DEFAULT_FROM_EMAIL')

################################################
#               Celery
################################################

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
