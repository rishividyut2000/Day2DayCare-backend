"""The most important test in this repository.

Two tenants, real Postgres, no mocks. Mocking the database here would defeat
the entire purpose — a cross-tenant leak is a patient-data breach, not a bug.
"""
from datetime import date, timedelta

import pytest
from django.core.management import call_command
from django.utils import timezone
from django_tenants.utils import schema_context

from apps.accounts.models import GlobalUser, TenantAccess
from apps.billing.models import Package, PatientPackage
from apps.billing.tasks import expire_packages, renewal_alerts
from apps.branches.models import Branch, Discipline
from apps.common.middleware import SCHEMA_RE
from apps.exercises.models import Exercise, ExerciseCategory
from apps.notifications.models import FollowUp
from apps.patients.models import Patient
from apps.scheduling.models import Appointment, Modality, ServiceType
from apps.scheduling.tasks import no_show_sweep
from apps.staff.models import Staff


@pytest.mark.django_db
def test_schemas_are_separate(tenant_a, tenant_b, in_tenant):
    assert tenant_a.schema_name != tenant_b.schema_name
    # TODO(DSS-92): create a patient in each schema, assert neither is visible
    # from the other, across every repository method.


@pytest.mark.parametrize("bad", [
    "public", "tenant_x; DROP TABLE patients", "TENANT_ALPHA", "tenant_",
    "../etc/passwd", "tenant_" + "a" * 41,
])
def test_schema_regex_rejects_injection(bad):
    assert SCHEMA_RE.fullmatch(bad) is None


@pytest.mark.parametrize("good", ["tenant_alpha", "tenant_cbe_01", "tenant_a"])
def test_schema_regex_accepts_valid(good):
    assert SCHEMA_RE.fullmatch(good) is not None


@pytest.mark.django_db
def test_provision_tenant_creates_usable_admin_password():
    call_command(
        "provision_tenant",
        code="alphaauth",
        name="Alpha Auth Clinic",
        email="admin@alphaauth.in",
        password="Passw0rd!123",
    )

    user = GlobalUser.objects.get(email="admin@alphaauth.in")
    assert user.has_usable_password() is True
    assert TenantAccess.objects.filter(user=user).exists() is True


@pytest.mark.django_db
def test_provision_tenant_seeds_reference_data():
    call_command(
        "provision_tenant",
        code="seeddemo",
        name="Seed Demo Clinic",
        email="seed@seeddemo.in",
        password="Passw0rd!123",
    )

    with schema_context("tenant_seeddemo"):
        assert Branch.objects.filter(code="main").exists() is True
        assert Discipline.objects.filter(code="physiotherapy").exists() is True


@pytest.mark.django_db
def test_provision_tenant_seeds_scheduling_reference_data():
    call_command(
        "provision_tenant",
        code="scheddemo",
        name="Schedule Demo Clinic",
        email="schedule@scheddemo.in",
        password="Passw0rd!123",
    )

    with schema_context("tenant_scheddemo"):
        assert ServiceType.objects.filter(name="Physiotherapy Consultation").exists() is True
        assert Modality.objects.filter(name="Manual Therapy").exists() is True


@pytest.mark.django_db
def test_provision_tenant_seeds_exercise_reference_data():
    call_command(
        "provision_tenant",
        code="exercisedemo",
        name="Exercise Demo Clinic",
        email="exercise@exercisedemo.in",
        password="Passw0rd!123",
    )

    with schema_context("tenant_exercisedemo"):
        assert ExerciseCategory.objects.filter(name="Mobility").exists() is True
        assert Exercise.objects.filter(code="ankle-dorsiflexion").exists() is True


@pytest.mark.django_db
def test_provision_tenant_seeds_billing_reference_data():
    call_command(
        "provision_tenant",
        code="billingdemo",
        name="Billing Demo Clinic",
        email="billing@billingdemo.in",
        password="Passw0rd!123",
    )

    with schema_context("tenant_billingdemo"):
        assert Package.objects.filter(code="starter-10").exists() is True


@pytest.mark.django_db
def test_no_show_sweep_marks_overdue_appointments_and_creates_follow_up(tenant_a, in_tenant):
    with in_tenant(tenant_a.schema_name):
        patient = Patient.objects.create(uhid="UHID-NS-1", first_name="Ria", last_name="Patel")
        therapist = Staff.objects.create(employee_code="STF-001", first_name="Asha", last_name="Nair")
        service_type = ServiceType.objects.create(name="Consultation", duration_minutes=45)
        appointment = Appointment.objects.create(
            patient=patient,
            therapist=therapist,
            service_type=service_type,
            start_at=timezone.now() - timedelta(hours=3),
            end_at=timezone.now() - timedelta(hours=2),
            status="scheduled",
        )

        no_show_sweep()

        appointment.refresh_from_db()
        assert appointment.status == "no_show"
        assert FollowUp.objects.filter(patient=patient, status="pending").exists() is True


@pytest.mark.django_db
def test_package_lifecycle_tasks_update_expired_and_renewal_statuses(tenant_a, in_tenant):
    with in_tenant(tenant_a.schema_name):
        patient = Patient.objects.create(uhid="UHID-PKG-1", first_name="Kiran", last_name="Rao")
        package = Package.objects.create(
            code="pkg-expiry-check",
            name="Expiry Check Pack",
            package_type="session_bundle",
            session_count=5,
            validity_days=30,
            price=3000,
        )
        expired = PatientPackage.objects.create(
            patient=patient,
            package=package,
            start_date=date.today() - timedelta(days=45),
            end_date=date.today() - timedelta(days=1),
            sessions_included=5,
            sessions_used=1,
            status="active",
        )
        expiring = PatientPackage.objects.create(
            patient=patient,
            package=package,
            start_date=date.today() - timedelta(days=10),
            end_date=date.today() + timedelta(days=4),
            sessions_included=5,
            sessions_used=3,
            status="active",
        )

        expire_packages()
        renewal_alerts()

        expired.refresh_from_db()
        expiring.refresh_from_db()
        assert expired.status == "expired"
        assert expiring.status == "expiring"
