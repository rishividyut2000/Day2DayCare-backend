from django_tenants.utils import schema_context
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import TenantAccess
from .permissions import ALL_PERMS, ROLE_PERMISSIONS


class D2DTokenSerializer(TokenObtainPairSerializer):
    """Adds tenant, staff, role, branch and permission claims to the token.

    Permissions are materialised at login as a bitmask so authorisation never
    hits the database per request, and never grows the token with a long
    string array — see apps.accounts.permissions for the flag catalog and
    per-role grants (sourced from the Role Matrix doc).
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        access = TenantAccess.objects.filter(
            user=user, is_active=True, is_default=True
        ).select_related("tenant").first()
        if access:
            mask = ALL_PERMS if user.is_platform_admin else ROLE_PERMISSIONS[access.role]

            token["tid"] = str(access.tenant_id)
            token["sid"] = str(access.staff_id) if access.staff_id else None
            token["rol"] = access.role
            token["brn"] = cls._branch_ids(access)
            # Decimal string, not a JSON number: JS bitwise ops truncate to 32
            # bits, so any frontend decode must use BigInt(claim), never `&`/`|`
            # on a plain `number`. See apps.accounts.permissions module docstring.
            token["per"] = str(int(mask))
        return token

    @staticmethod
    def _branch_ids(access: TenantAccess) -> list[str]:
        """Branch ids this staff member belongs to, read from the tenant schema.

        Login runs against the public schema (TenantAccess lives there), so the
        tenant schema has to be entered explicitly to read apps.staff.StaffBranch
        — same pattern as the `in_tenant` fixture in tests/conftest.py.
        """
        if not access.staff_id:
            return []

        from apps.staff.models import StaffBranch

        with schema_context(access.tenant.schema_name):
            return [
                str(branch_id)
                for branch_id in StaffBranch.objects.filter(
                    staff_id=access.staff_id
                ).values_list("branch_id", flat=True)
            ]
