"""Production settings — PostgreSQL, DEBUG=False."""

import os
from pathlib import Path

from dotenv import load_dotenv

from .base import *  # noqa: F401, F403
from .base import BASE_DIR

load_dotenv(Path(BASE_DIR) / ".env")

DEBUG = False

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

_db_url = os.environ["DATABASE_URL"]
# Simple DATABASE_URL parser (postgresql://user:pass@host:port/name)
import urllib.parse  # noqa: E402

_parsed = urllib.parse.urlparse(_db_url)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _parsed.path.lstrip("/"),
        "USER": _parsed.username,
        "PASSWORD": _parsed.password,
        "HOST": _parsed.hostname,
        "PORT": str(_parsed.port or 5432),
    }
}

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CORS_ALLOW_CREDENTIALS = True

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
