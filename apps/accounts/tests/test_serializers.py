import pytest

from apps.accounts.models import GlobalUser, Role, TenantAccess
from apps.accounts.permissions import ALL_PERMS, ROLE_PERMISSIONS
from apps.accounts.serializers import D2DTokenSerializer
from apps.branches.models import Branch
from apps.staff.models import Staff, StaffBranch

PASSWORD = "Passw0rd!123"  # noqa: S105 - test fixture, not a real credential


@pytest.mark.django_db
def test_token_carries_role_and_bitmask_permission_claim(tenant_a):
    user = GlobalUser.objects.create_user(
        email="therapist@alpha.in", password=PASSWORD, full_name="Therapist One"
    )
    TenantAccess.objects.create(
        user=user, tenant=tenant_a, role=Role.PHYSIOTHERAPIST, is_default=True, is_active=True
    )

    token = D2DTokenSerializer.get_token(user)

    assert token["tid"] == str(tenant_a.id)
    assert token["rol"] == Role.PHYSIOTHERAPIST
    assert token["per"] == str(int(ROLE_PERMISSIONS[Role.PHYSIOTHERAPIST]))
    assert token["brn"] == []


@pytest.mark.django_db
def test_token_carries_branch_ids_from_tenant_schema(tenant_a, in_tenant):
    with in_tenant(tenant_a.schema_name):
        branch = Branch.objects.create(code="main", name="Main Branch", city="Pune", state="MH")
        staff = Staff.objects.create(employee_code="STF-100", first_name="Asha", last_name="Nair")
        StaffBranch.objects.create(staff=staff, branch_id=branch.id, is_primary=True)

    user = GlobalUser.objects.create_user(
        email="recept@alpha.in", password=PASSWORD, full_name="Front Desk One"
    )
    TenantAccess.objects.create(
        user=user, tenant=tenant_a, role=Role.RECEPTIONIST,
        staff_id=staff.id, is_default=True, is_active=True,
    )

    token = D2DTokenSerializer.get_token(user)

    assert token["sid"] == str(staff.id)
    assert token["brn"] == [str(branch.id)]


@pytest.mark.django_db
def test_platform_admin_gets_all_perms_regardless_of_role(tenant_a):
    user = GlobalUser.objects.create_superuser(
        email="root@alpha.in", password=PASSWORD, full_name="Root"
    )
    TenantAccess.objects.create(
        user=user, tenant=tenant_a, role=Role.PHYSIOTHERAPIST, is_default=True, is_active=True
    )

    token = D2DTokenSerializer.get_token(user)

    assert token["per"] == str(int(ALL_PERMS))
