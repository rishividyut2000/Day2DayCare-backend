import pytest
from django_tenants.utils import schema_context

from apps.tenants.models import Client, Domain


@pytest.fixture
def tenant_a(db):
    client = Client.objects.create(
        code="alpha", schema_name="tenant_alpha",
        legal_name="Alpha Clinic", display_name="Alpha Clinic",
    )
    Domain.objects.create(domain="alpha.localhost", tenant=client, is_primary=True)
    return client


@pytest.fixture
def tenant_b(db):
    client = Client.objects.create(
        code="beta", schema_name="tenant_beta",
        legal_name="Beta Clinic", display_name="Beta Clinic",
    )
    Domain.objects.create(domain="beta.localhost", tenant=client, is_primary=True)
    return client


@pytest.fixture
def in_tenant():
    return schema_context
