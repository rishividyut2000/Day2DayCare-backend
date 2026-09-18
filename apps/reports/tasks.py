from celery import shared_task


@shared_task
def refresh_report_views() -> None:
    """REFRESH MATERIALIZED VIEW CONCURRENTLY for each tenant."""
    # TODO(DSS-89)
