from celery import shared_task


@shared_task
def dispatch_reminders() -> None:
    """Claim queued reminders with SELECT ... FOR UPDATE SKIP LOCKED and send.

    The send and the notification_log write share a transaction, so a retried
    reminder never sends twice.
    """
    # TODO(DSS-86)


@shared_task
def enqueue_appointment_reminders() -> None:
    """Create reminder rows for appointments 24h out."""
    # TODO(DSS-86)
