from .base import *
from .base import env

DEBUG = True

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "*"]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "arike_django",
        "USER": "arike_django",
        "PASSWORD": "arike_django",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}
