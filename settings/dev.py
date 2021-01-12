from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c%-$4e9f8a@##ow4%*sk47%(x88cr=%l3b2-&g2ua0s+v&ak%^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

PRICE_BASE = 10

CONTRACT_TEMPLATE = BASE_DIR / 'example' / 'content.xml'
CONTRACT_REFERENCE = BASE_DIR / 'example' / 'contract.odt'
