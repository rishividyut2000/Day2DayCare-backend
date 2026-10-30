"""Production settings for deployment without a domain/TLS cert yet.

Everything else is identical to `production` — only the TLS-enforcing
settings are relaxed, since without a certificate SECURE_SSL_REDIRECT would
force an HTTPS redirect that can never succeed (redirect loop). Switch back
to DJANGO_SETTINGS_MODULE=config.settings.production once a domain and
certificate are in place.
"""
from .production import *  # noqa: F403

SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
