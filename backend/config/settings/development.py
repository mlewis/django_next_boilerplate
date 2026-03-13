"""Development settings — SQLite, DEBUG=True, .env loaded."""

import os
from pathlib import Path

from dotenv import load_dotenv

from .base import *  # noqa: F401, F403
from .base import BASE_DIR

load_dotenv(Path(BASE_DIR) / ".env")

DEBUG = True

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-key-do-not-use-in-production",
)

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
