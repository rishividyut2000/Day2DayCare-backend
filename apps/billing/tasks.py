from celery import shared_task
from django_tenants.utils import get_tenant_model, schema_context


def for_each_tenant(fn):
    for tenant in get_tenant_model().objects.filter(is_active=True):
        with schema_context(tenant.schema_name):
            fn(tenant)


@shared_task
def expire_packages() -> None:
    """Move patient packages past valid_to to expired."""
    # TODO(DSS-76)


@shared_task
def renewal_alerts() -> None:
    """Flag packages with <=2 sessions or <=7 days remaining."""
    # TODO(DSS-76)
