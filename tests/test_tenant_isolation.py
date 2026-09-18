"""The most important test in this repository.

Two tenants, real Postgres, no mocks. Mocking the database here would defeat
the entire purpose — a cross-tenant leak is a patient-data breach, not a bug.
"""
import pytest

from apps.common.middleware import SCHEMA_RE


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
