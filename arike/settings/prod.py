from .base import *
from .base import env

DEBUG = False

ALLOWED_HOSTS = ["rithviknishad-arike.herokuapp.com"]

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
