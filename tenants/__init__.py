"""Compatibility package for the Django app label used by the project.

This project installs the app as apps.tenants, but Django and pylint-django
resolve model references using the app label "tenants". Keeping a lightweight
compatibility package here avoids import resolution errors without changing the
actual app wiring.
"""

from apps.tenants import *  # noqa: F401,F403
