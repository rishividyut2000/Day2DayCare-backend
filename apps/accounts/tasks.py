from celery import shared_task


@shared_task
def purge_expired_tokens() -> None:
    """Delete expired refresh tokens, OTPs and unconfirmed document rows."""
    # TODO(DSS-27)
