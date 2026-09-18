from celery import shared_task


@shared_task
def no_show_sweep() -> None:
    """Appointments past their end with no session -> no_show + follow-up row."""
    # TODO(DSS-70)
