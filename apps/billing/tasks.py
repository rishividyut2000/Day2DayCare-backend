from datetime import date, timedelta

from celery import shared_task
from django.db.models import F, Q
from django_tenants.utils import get_tenant_model, schema_context

from apps.billing.models import PatientPackage


def for_each_tenant(fn):
    for tenant in get_tenant_model().objects.filter(is_active=True):
        with schema_context(tenant.schema_name):
            fn(tenant)


@shared_task
def expire_packages() -> None:
    """Move patient packages past valid_to to expired."""
    today = date.today()

    def expire(tenant):
        PatientPackage.objects.filter(
            status__in=["active", "expiring"],
            end_date__lt=today,
        ).update(status="expired")

    for_each_tenant(expire)


@shared_task
def renewal_alerts() -> None:
    """Flag packages with <=2 sessions or <=7 days remaining."""
    today = date.today()
    cutoff = today + timedelta(days=7)

    def alert(tenant):
        PatientPackage.objects.filter(
            status__in=["active", "expiring"],
        ).filter(
            Q(end_date__lte=cutoff)
            | (
                Q(sessions_included__gt=F("sessions_used"))
                & Q(sessions_included__lte=F("sessions_used") + 2)
            )
        ).update(status="expiring")

    for_each_tenant(alert)
