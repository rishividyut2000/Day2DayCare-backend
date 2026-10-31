"""Bitmask permission catalog and role grants.

Source of truth: "Day2Day CARE: Role Matrix" (claude.ai/artifact/NyG1JVtbTKT66eUVJc18Nv),
draft v1, 31 Oct 2026. Each `Perm` flag is one bit, grouped by the matrix's
module rows. A role's grant is the bitwise-OR of the flags for the cells in
its column marked C/R/U/D/A in that doc.

Granularity note: this catalog uses one VIEW bit and one MANAGE bit (create +
update together) per module rather than a bit per CRUD verb — delete/archive
and ownership scoping ("own"/"branch") are enforced downstream (soft-delete
guards, apps.common.permissions.scope_branches, and per-row `created_by`/
`staff_id` ownership checks in services.py), not encoded as bits. APPROVE and
a few collect/check-in-only actions get their own bit where the matrix singles
them out as a distinct, narrower grant than MANAGE.

Encoding: ~42 flags comfortably fits a JS-safe integer (< 2**53), but JS's
native `&`/`|`/`<<` truncate to 32 bits — so the JWT `per` claim is serialized
as a *decimal string* (`str(mask)`), not a JSON number, and any frontend code
that decodes it must parse with `BigInt(claim)`, never native bitwise ops on
a `number`. See src/types/roles.ts in Day2DayCare-Frontend for the mirrored
catalog (kept in sync by hand — no shared package between the two repos).
"""
from enum import IntFlag, auto

from .models import Role


class Perm(IntFlag):
    TENANTS_MANAGE = auto()  # Tenants and subscriptions

    SETTINGS_VIEW = auto()  # Clinic settings and branding
    SETTINGS_MANAGE = auto()

    BRANCHES_VIEW = auto()  # Branches
    BRANCHES_MANAGE = auto()
    BRANCHES_VIEW_ALL = auto()  # cross-branch visibility, not just own

    STAFF_ACCOUNTS_VIEW = auto()  # Users and roles
    STAFF_ACCOUNTS_MANAGE = auto()

    STAFF_PROFILES_VIEW = auto()  # Therapist profiles and availability
    STAFF_PROFILES_MANAGE = auto()

    PATIENTS_VIEW = auto()  # Patient registration and demographics
    PATIENTS_MANAGE = auto()

    CLINICAL_NOTES_VIEW = auto()  # Patient clinical history and notes
    CLINICAL_NOTES_MANAGE = auto()

    ASSESSMENTS_VIEW = auto()  # Assessments
    ASSESSMENTS_MANAGE = auto()
    ASSESSMENTS_APPROVE = auto()

    PLANS_VIEW = auto()  # Treatment plans
    PLANS_MANAGE = auto()
    PLANS_APPROVE = auto()

    EXERCISES_VIEW = auto()  # Exercise Studio: library and authoring
    EXERCISES_MANAGE = auto()

    AVATARS_VIEW = auto()  # Exercise Studio: avatars
    AVATARS_MANAGE = auto()

    EXERCISE_ASSIGN = auto()  # Assign exercises to patient

    ADHERENCE_VIEW = auto()  # Home exercise player and adherence logging

    APPOINTMENTS_VIEW = auto()  # Appointments
    APPOINTMENTS_MANAGE = auto()

    SESSIONS_VIEW = auto()  # Sessions (check-in, treatment record, outcome)
    SESSIONS_MANAGE = auto()
    SESSIONS_CHECKIN = auto()  # front-desk check-in only, no treatment record access

    PROGRESS_VIEW = auto()  # Progress tracking and outcome measures
    PROGRESS_MANAGE = auto()

    BILLING_VIEW = auto()  # Invoices and payments
    BILLING_MANAGE = auto()
    BILLING_COLLECT = auto()  # front-desk collect-payment only

    BILLING_APPROVE_REFUND = auto()  # Refunds, discounts and write-offs sign-off

    REPORTS_VIEW = auto()  # Reports and analytics (row-level scope via role/branch)

    NOTIFICATIONS_MANAGE_TEMPLATES = auto()  # Notifications and reminders
    NOTIFICATIONS_SEND = auto()

    AUDIT_LOG_VIEW = auto()  # Audit log

    DATA_EXPORT_MANAGE = auto()  # Data export and deletion requests


ALL_PERMS = Perm(0)
for _flag in Perm:
    ALL_PERMS |= _flag


ROLE_PERMISSIONS: dict[str, Perm] = {
    Role.PLATFORM_ADMIN: (
        Perm.TENANTS_MANAGE
        | Perm.SETTINGS_VIEW
        | Perm.BRANCHES_VIEW
        | Perm.STAFF_ACCOUNTS_VIEW
        | Perm.STAFF_PROFILES_VIEW
        | Perm.PATIENTS_VIEW
        | Perm.REPORTS_VIEW
        | Perm.AUDIT_LOG_VIEW
        | Perm.DATA_EXPORT_MANAGE
        # Deliberately excludes every clinical/financial bit: "Platform Admin
        # cannot read clinical data without an audited support-access grant."
    ),
    Role.CLINIC_OWNER: (
        Perm.SETTINGS_VIEW
        | Perm.SETTINGS_MANAGE
        | Perm.BRANCHES_VIEW
        | Perm.BRANCHES_MANAGE
        | Perm.BRANCHES_VIEW_ALL
        | Perm.STAFF_ACCOUNTS_VIEW
        | Perm.STAFF_ACCOUNTS_MANAGE
        | Perm.STAFF_PROFILES_VIEW
        | Perm.STAFF_PROFILES_MANAGE
        | Perm.PATIENTS_VIEW
        | Perm.PATIENTS_MANAGE
        | Perm.CLINICAL_NOTES_VIEW
        | Perm.ASSESSMENTS_VIEW
        | Perm.PLANS_VIEW
        | Perm.EXERCISES_VIEW
        | Perm.AVATARS_VIEW
        | Perm.AVATARS_MANAGE
        | Perm.ADHERENCE_VIEW
        | Perm.APPOINTMENTS_VIEW
        | Perm.APPOINTMENTS_MANAGE
        | Perm.SESSIONS_VIEW
        | Perm.PROGRESS_VIEW
        | Perm.BILLING_VIEW
        | Perm.BILLING_MANAGE
        | Perm.BILLING_APPROVE_REFUND
        | Perm.REPORTS_VIEW
        | Perm.NOTIFICATIONS_MANAGE_TEMPLATES
        | Perm.AUDIT_LOG_VIEW
        | Perm.DATA_EXPORT_MANAGE
    ),
    Role.BRANCH_MANAGER: (
        Perm.SETTINGS_VIEW
        | Perm.BRANCHES_VIEW
        | Perm.BRANCHES_MANAGE
        | Perm.STAFF_ACCOUNTS_VIEW
        | Perm.STAFF_ACCOUNTS_MANAGE
        | Perm.STAFF_PROFILES_VIEW
        | Perm.STAFF_PROFILES_MANAGE
        | Perm.PATIENTS_VIEW
        | Perm.PATIENTS_MANAGE
        | Perm.CLINICAL_NOTES_VIEW
        | Perm.ASSESSMENTS_VIEW
        | Perm.PLANS_VIEW
        | Perm.EXERCISES_VIEW
        | Perm.AVATARS_VIEW
        | Perm.ADHERENCE_VIEW
        | Perm.APPOINTMENTS_VIEW
        | Perm.APPOINTMENTS_MANAGE
        | Perm.SESSIONS_VIEW
        | Perm.PROGRESS_VIEW
        | Perm.BILLING_VIEW
        | Perm.BILLING_APPROVE_REFUND  # "A (up to a limit)" — limit enforced in services.py
        | Perm.REPORTS_VIEW
        | Perm.AUDIT_LOG_VIEW
    ),
    Role.PHYSIOTHERAPIST: (
        Perm.BRANCHES_VIEW
        | Perm.STAFF_PROFILES_VIEW
        | Perm.PATIENTS_VIEW
        | Perm.PATIENTS_MANAGE
        | Perm.CLINICAL_NOTES_VIEW
        | Perm.CLINICAL_NOTES_MANAGE
        | Perm.ASSESSMENTS_VIEW
        | Perm.ASSESSMENTS_MANAGE
        | Perm.ASSESSMENTS_APPROVE
        | Perm.PLANS_VIEW
        | Perm.PLANS_MANAGE
        | Perm.PLANS_APPROVE
        | Perm.EXERCISES_VIEW
        | Perm.EXERCISES_MANAGE
        | Perm.AVATARS_VIEW
        | Perm.AVATARS_MANAGE
        | Perm.EXERCISE_ASSIGN
        | Perm.ADHERENCE_VIEW
        | Perm.APPOINTMENTS_VIEW
        | Perm.APPOINTMENTS_MANAGE
        | Perm.SESSIONS_VIEW
        | Perm.SESSIONS_MANAGE
        | Perm.PROGRESS_VIEW
        | Perm.PROGRESS_MANAGE
        | Perm.BILLING_VIEW
        | Perm.REPORTS_VIEW
        # No CLINICAL_NOTES/ASSESSMENTS/PLANS bit reaches Receptionist or
        # Billing below — "least privilege by default" per the doc's key rules.
    ),
    Role.RECEPTIONIST: (
        Perm.BRANCHES_VIEW
        | Perm.STAFF_PROFILES_VIEW
        | Perm.PATIENTS_VIEW
        | Perm.PATIENTS_MANAGE
        | Perm.APPOINTMENTS_VIEW
        | Perm.APPOINTMENTS_MANAGE
        | Perm.SESSIONS_VIEW
        | Perm.SESSIONS_CHECKIN
        | Perm.BILLING_VIEW
        | Perm.BILLING_COLLECT
        | Perm.REPORTS_VIEW
        | Perm.NOTIFICATIONS_SEND
    ),
    Role.BILLING: (
        Perm.BRANCHES_VIEW
        | Perm.STAFF_PROFILES_VIEW
        | Perm.PATIENTS_VIEW
        | Perm.APPOINTMENTS_VIEW
        | Perm.SESSIONS_VIEW
        | Perm.BILLING_VIEW
        | Perm.BILLING_MANAGE
        | Perm.REPORTS_VIEW
    ),
    # Patients aren't TenantAccess users in v1 (no mobile/portal app yet — see
    # apps.accounts.models.PatientGlobal docstring), so no staff-side bits apply.
    Role.PATIENT: Perm(0),
}


def has_perm(mask: int, flag: Perm) -> bool:
    """True if `mask` (an int decoded from the JWT `per` claim) grants `flag`."""
    return bool(Perm(mask) & flag)
