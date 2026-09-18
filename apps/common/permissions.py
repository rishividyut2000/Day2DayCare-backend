from rest_framework.permissions import BasePermission


class HasPermissionCode(BasePermission):
    """Checks a permission code carried in the JWT `per` claim.

    Usage:
        class PatientViewSet(...):
            permission_classes = [IsAuthenticated, HasPermissionCode]
            required_permissions = {"POST": "patients.create"}
    """

    def has_permission(self, request, view):
        required = getattr(view, "required_permissions", {}).get(request.method)
        if required is None:
            return True
        granted = set(getattr(request.auth, "payload", {}).get("per", []))
        return required in granted


def scope_branches(queryset, request, field="branch_id"):
    """Restrict a queryset to the caller's branches.

    Applied in the repository/queryset layer, never per view — a scoping rule
    that has to be remembered at each call site will eventually be forgotten.
    """
    payload = getattr(request.auth, "payload", {})
    if "branches.view_all" in set(payload.get("per", [])):
        return queryset
    return queryset.filter(**{f"{field}__in": payload.get("brn", [])})
