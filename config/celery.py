import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("day2daycare")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Every job iterates public.tenants and runs per schema. All must be idempotent:
# a retry must never double-send or double-charge.
app.conf.beat_schedule = {
    "dispatch-reminders": {
        "task": "apps.notifications.tasks.dispatch_reminders",
        "schedule": crontab(minute="*/5"),
    },
    "enqueue-appointment-reminders": {
        "task": "apps.notifications.tasks.enqueue_appointment_reminders",
        "schedule": crontab(minute=0),
    },
    "expire-packages": {
        "task": "apps.billing.tasks.expire_packages",
        "schedule": crontab(hour=0, minute=30),
    },
    "renewal-alerts": {
        "task": "apps.billing.tasks.renewal_alerts",
        "schedule": crontab(hour=9, minute=0),
    },
    "no-show-sweep": {
        "task": "apps.scheduling.tasks.no_show_sweep",
        "schedule": crontab(minute="*/30"),
    },
    "refresh-report-views": {
        "task": "apps.reports.tasks.refresh_report_views",
        "schedule": crontab(hour=1, minute=0),
    },
    "purge-expired-tokens": {
        "task": "apps.accounts.tasks.purge_expired_tokens",
        "schedule": crontab(hour=2, minute=0),
    },
}
