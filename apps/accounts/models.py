"""Global identity. Lives in the public schema.

A staff member has one GlobalUser and one TenantAccess row per clinic they can
sign into. Their clinical profile (role, specializations, availability) lives
in the tenant schema as apps.staff.Staff.
"""
import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class GlobalUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra):
        if not email:
            raise ValueError("email is required")
        user = self.model(email=self.normalize_email(email), **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra):
        extra.setdefault("is_platform_admin", True)
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra)


class GlobalUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_e164 = models.CharField(max_length=20, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_platform_admin = models.BooleanField(default=False)
    failed_login_count = models.PositiveSmallIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)
    password_changed_at = models.DateTimeField(null=True, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = GlobalUserManager()

    def __str__(self) -> str:
        return self.email


class Role(models.TextChoices):
    """The 7 actors from the Role Matrix doc (Day2Day CARE: Role Matrix, 31 Oct 2026).

    One role per (user, tenant) pair, stored on TenantAccess. Permission grants
    for each role live in apps.accounts.permissions.ROLE_PERMISSIONS as a
    bitmask — this enum is just the label, not the authorization logic.
    """

    PLATFORM_ADMIN = "platform_admin", "Platform Admin"
    CLINIC_OWNER = "clinic_owner", "Clinic Owner"
    BRANCH_MANAGER = "branch_manager", "Branch Manager"
    PHYSIOTHERAPIST = "physiotherapist", "Physiotherapist"
    RECEPTIONIST = "receptionist", "Receptionist"
    BILLING = "billing", "Billing / Accounts"
    PATIENT = "patient", "Patient"


class TenantAccess(models.Model):
    """Which clinics a user may sign into. The JWT `tid` claim comes from here."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(GlobalUser, on_delete=models.CASCADE, related_name="tenants")
    tenant = models.ForeignKey("tenants.Client", on_delete=models.CASCADE)
    staff_id = models.UUIDField(null=True, blank=True)  # tenant_<x>.staff.id
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.PHYSIOTHERAPIST)
    is_default = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "tenant")


class PatientGlobal(models.Model):
    """Patient identity, unused in v1 (no mobile app) but kept from day one.

    Adding auth tables to 40 live tenant schemas later is a migration; an empty
    table now is free.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_e164 = models.CharField(max_length=20, unique=True)
    email = models.EmailField(null=True, blank=True)
    full_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
