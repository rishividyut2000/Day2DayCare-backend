"""Tenant resolution.

django-tenants routes by subdomain by default. This API is JWT-based, so the
schema is resolved from the token's `tid` claim instead.

The token carries a tenant *id*, never a schema name. The schema name is looked
up from public.tenants and regex-validated before it touches a connection.
This is the tenancy boundary — one bypass is a cross-clinic data leak, so it
lives in exactly one place and nothing else duplicates it.
"""
import re

from django.db import connection
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import get_public_schema_name, get_tenant_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

SCHEMA_RE = re.compile(r"^tenant_[a-z0-9_]{1,40}$")

PUBLIC_PATHS = ("/admin/", "/health/", "/api/v1/auth/login", "/api/v1/auth/refresh",
                "/api/v1/schema/", "/api/v1/docs/")


class TenantFromJWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith(PUBLIC_PATHS):
            connection.set_schema_to_public()
            return None

        header = JWTAuthentication().get_header(request)
        if header is None:
            connection.set_schema_to_public()
            return None

        try:
            raw = JWTAuthentication().get_raw_token(header)
            token = JWTAuthentication().get_validated_token(raw)
        except (InvalidToken, TokenError):
            return JsonResponse({"detail": "invalid token"}, status=401)

        tenant_id = token.get("tid")
        if not tenant_id:
            return JsonResponse({"detail": "token carries no tenant"}, status=403)

        try:
            tenant = get_tenant_model().objects.get(id=tenant_id, is_active=True)
        except get_tenant_model().DoesNotExist:
            return JsonResponse({"detail": "unknown tenant"}, status=403)

        if tenant.schema_name == get_public_schema_name():
            return JsonResponse({"detail": "invalid tenant"}, status=403)

        if not SCHEMA_RE.fullmatch(tenant.schema_name):
            return JsonResponse({"detail": "invalid tenant"}, status=403)

        connection.set_tenant(tenant)
        request.tenant = tenant
        return None
