from django.utils import timezone
from django_tenants.utils import get_tenant_model, schema_context
from celery import shared_task

from apps.notifications.models import FollowUp
from apps.scheduling.models import Appointment


def for_each_tenant(fn):
    for tenant in get_tenant_model().objects.filter(is_active=True):
        with schema_context(tenant.schema_name):
            fn(tenant)


@shared_task
def no_show_sweep() -> None:
    """Appointments past their end with no session -> no_show + follow-up row."""
    now = timezone.now()

    def sweep(tenant):
        for appointment in Appointment.objects.filter(
            status__in=["scheduled", "confirmed"],
            end_at__lt=now,
        ).exclude(sessions__isnull=False):
            appointment.status = "no_show"
            appointment.save(update_fields=["status", "updated_at"])
            FollowUp.objects.get_or_create(
                patient=appointment.patient,
                follow_up_at=now,
                defaults={
                    "note": f"Missed appointment {appointment.id}",
                    "status": "pending",
                },
            )

    for_each_tenant(sweep)
