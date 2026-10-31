from rest_framework.permissions import BasePermission

from apps.accounts.permissions import Perm


class HasPermissionFlag(BasePermission):
    """Checks a permission bit carried in the JWT `per` claim.

    The claim is a decimal string (see apps.accounts.serializers.D2DTokenSerializer)
    so it's parsed with `int()`, not treated as a JS-unsafe JSON number.

    Usage:
        class PatientViewSet(...):
            permission_classes = [IsAuthenticated, HasPermissionFlag]
            required_permissions = {"POST": Perm.PATIENTS_MANAGE}
    """

    def has_permission(self, request, view):
        required = getattr(view, "required_permissions", {}).get(request.method)
        if required is None:
            return True
        payload = getattr(request.auth, "payload", {})
        granted = Perm(int(payload.get("per", 0)))
        return bool(granted & required)


def scope_branches(queryset, request, field="branch_id"):
    """Restrict a queryset to the caller's branches.

    Applied in the repository/queryset layer, never per view — a scoping rule
    that has to be remembered at each call site will eventually be forgotten.
    """
    payload = getattr(request.auth, "payload", {})
    granted = Perm(int(payload.get("per", 0)))
    if granted & Perm.BRANCHES_VIEW_ALL:
        return queryset
    return queryset.filter(**{f"{field}__in": payload.get("brn", [])})
