"""Bit math and role-grant checks for the Role Matrix catalog.

Each assertion traces back to a specific row/column in the
"Day2Day CARE: Role Matrix" doc — see apps.accounts.permissions module
docstring for the source.
"""
import pytest

from apps.accounts.models import Role
from apps.accounts.permissions import ALL_PERMS, ROLE_PERMISSIONS, Perm, has_perm


def test_has_perm_true_when_bit_is_set():
    mask = int(Perm.PATIENTS_VIEW | Perm.PATIENTS_MANAGE)
    assert has_perm(mask, Perm.PATIENTS_VIEW) is True
    assert has_perm(mask, Perm.PATIENTS_MANAGE) is True


def test_has_perm_false_when_bit_is_not_set():
    mask = int(Perm.PATIENTS_VIEW)
    assert has_perm(mask, Perm.BILLING_MANAGE) is False


def test_every_role_is_mapped():
    assert set(ROLE_PERMISSIONS) == set(Role)


def test_all_perms_contains_every_flag():
    for flag in Perm:
        assert flag in ALL_PERMS


@pytest.mark.parametrize("role", list(Role))
def test_patient_role_has_no_staff_side_bits(role):
    if role == Role.PATIENT:
        assert int(ROLE_PERMISSIONS[role]) == 0


def test_least_privilege_receptionist_cannot_read_clinical_notes():
    """'Clinical data is never visible to Receptionist or Billing.'"""
    mask = ROLE_PERMISSIONS[Role.RECEPTIONIST]
    assert not (mask & Perm.CLINICAL_NOTES_VIEW)
    assert not (mask & Perm.ASSESSMENTS_VIEW)
    assert not (mask & Perm.PLANS_VIEW)


def test_least_privilege_billing_cannot_read_clinical_notes():
    mask = ROLE_PERMISSIONS[Role.BILLING]
    assert not (mask & Perm.CLINICAL_NOTES_VIEW)
    assert not (mask & Perm.ASSESSMENTS_VIEW)


def test_physiotherapist_owns_clinical_workflow():
    mask = ROLE_PERMISSIONS[Role.PHYSIOTHERAPIST]
    for flag in (
        Perm.CLINICAL_NOTES_MANAGE,
        Perm.ASSESSMENTS_MANAGE,
        Perm.ASSESSMENTS_APPROVE,
        Perm.PLANS_MANAGE,
        Perm.PLANS_APPROVE,
    ):
        assert mask & flag
    # But not financial sign-off or staff management.
    assert not (mask & Perm.BILLING_APPROVE_REFUND)
    assert not (mask & Perm.STAFF_ACCOUNTS_MANAGE)


def test_financial_overrides_need_approval_role():
    """Refunds/discounts/write-offs: only Owner and Branch Manager approve."""
    for role in (Role.CLINIC_OWNER, Role.BRANCH_MANAGER):
        assert ROLE_PERMISSIONS[role] & Perm.BILLING_APPROVE_REFUND

    for role in (Role.PHYSIOTHERAPIST, Role.RECEPTIONIST, Role.BILLING):
        assert not (ROLE_PERMISSIONS[role] & Perm.BILLING_APPROVE_REFUND)


def test_receptionist_can_check_in_but_not_manage_sessions():
    mask = ROLE_PERMISSIONS[Role.RECEPTIONIST]
    assert mask & Perm.SESSIONS_CHECKIN
    assert not (mask & Perm.SESSIONS_MANAGE)


def test_platform_admin_excluded_from_clinical_and_financial_data():
    """'Platform Admin cannot read clinical data without an audited grant.'"""
    mask = ROLE_PERMISSIONS[Role.PLATFORM_ADMIN]
    for flag in (
        Perm.CLINICAL_NOTES_VIEW,
        Perm.ASSESSMENTS_VIEW,
        Perm.PLANS_VIEW,
        Perm.BILLING_VIEW,
        Perm.APPOINTMENTS_VIEW,
    ):
        assert not (mask & flag)


def test_tenants_manage_is_platform_admin_only():
    for role, mask in ROLE_PERMISSIONS.items():
        if role == Role.PLATFORM_ADMIN:
            assert mask & Perm.TENANTS_MANAGE
        else:
            assert not (mask & Perm.TENANTS_MANAGE)
