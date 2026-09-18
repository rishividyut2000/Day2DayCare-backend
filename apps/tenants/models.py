import uuid

from django.db import models
from django_tenants.models import DomainMixin, TenantMixin


class Client(TenantMixin):
    """A clinic. Lives in the public schema; owns a tenant_<code> schema."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.SlugField(max_length=30, unique=True)
    legal_name = models.CharField(max_length=200)
    display_name = models.CharField(max_length=200)
    gstin = models.CharField(max_length=15, blank=True)
    country_code = models.CharField(max_length=2, default="IN")
    time_zone = models.CharField(max_length=64, default="Asia/Kolkata")
    currency = models.CharField(max_length=3, default="INR")
    plan_code = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    onboarded_on = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Create the schema automatically when a Client row is saved.
    auto_create_schema = True

    def __str__(self) -> str:
        return self.display_name


class Domain(DomainMixin):
    """Kept because django-tenants requires it. Routing is by JWT, not domain."""
