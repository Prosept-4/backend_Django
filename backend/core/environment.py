import os

from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

################################################
#               Settings
################################################

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(' ')

DB_ENGINE = os.getenv('DB_ENGINE', 'sqlite3')  # sqlite3 или postgresql

DEBUG = True

IS_LOGGING = os.getenv('IS_LOGGING', 'False') == 'True'

SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

################################################
#               Celery
################################################

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
