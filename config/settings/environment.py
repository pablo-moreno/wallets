from os import environ


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environ.get('DEBUG', 'FALSE') == 'TRUE'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('SECRET_KEY', 'set secret key')

DATABASE_URL = environ.get('DATABASE_URL', 'postgres://admin:development@postgres:5432/wallets')

SENTRY_DSN = environ.get('SENTRY_DSN')

PAGE_SIZE = environ.get('PAGE_SIZE', 20)

APP_VERSION = environ.get('VERSION', 'latest')

ENVIRONMENT = environ.get('ENVIRONMENT', 'staging')
