from django.urls import reverse

from apps.branches.models import Branch, Discipline
from apps.patients.models import Patient
from apps.staff.models import ServiceZone, Specialization, Staff


def test_core_tenant_models_are_defined():
    assert Branch._meta.app_label == "branches"
    assert Discipline._meta.app_label == "branches"
    assert Staff._meta.app_label == "staff"
    assert ServiceZone._meta.app_label == "staff"
    assert Specialization._meta.app_label == "staff"
    assert Patient._meta.app_label == "patients"


def test_core_api_routes_exist():
    assert reverse("branch-list") == "/api/v1/branches/"
    assert reverse("patient-list") == "/api/v1/patients/"
    assert reverse("staff-list") == "/api/v1/staff/"
