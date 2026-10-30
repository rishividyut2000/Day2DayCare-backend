from .base import *  # noqa: F403

DEBUG = False

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

STORAGES = {
    "default": {"BACKEND": "storages.backends.azure_storage.AzureStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

# PgBouncer in transaction mode: server-side cursors and persistent
# connections must be off. This is a PgBouncer requirement, not a
# django-tenants one.
DATABASES["default"]["CONN_MAX_AGE"] = 0          # noqa: F405
DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True  # noqa: F405
