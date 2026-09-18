from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import TenantAccess


class D2DTokenSerializer(TokenObtainPairSerializer):
    """Adds tenant, staff, role, branch and permission claims to the token.

    Permissions are materialised at login so authorisation never hits the
    database per request. If the list grows past ~60 entries, move to a
    role-only claim plus a cached permission set in Redis.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        access = TenantAccess.objects.filter(
            user=user, is_active=True, is_default=True
        ).select_related("tenant").first()
        if access:
            token["tid"] = str(access.tenant_id)
            token["sid"] = str(access.staff_id) if access.staff_id else None
            token["rol"] = []    # TODO(DSS-26): from tenant staff roles
            token["brn"] = []    # TODO(DSS-26): accessible branch ids
            token["per"] = []    # TODO(DSS-26): materialised permission codes
        return token
