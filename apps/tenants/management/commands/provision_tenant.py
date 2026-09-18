"""Provision a new clinic: schema, migrations, master data, first admin.

    python manage.py provision_tenant --code cbe --name "Day2Day Coimbatore" \
        --email admin@day2daycare.in
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django_tenants.utils import schema_context

from apps.accounts.models import GlobalUser, TenantAccess
from apps.tenants.models import Client, Domain


class Command(BaseCommand):
    help = "Create a tenant schema and seed it."

    def add_arguments(self, parser):
        parser.add_argument("--code", required=True)
        parser.add_argument("--name", required=True)
        parser.add_argument("--email", required=True)

    @transaction.atomic
    def handle(self, *args, **opts):
        code = opts["code"].lower()
        if not code.isidentifier():
            raise CommandError("code must be alphanumeric/underscore")

        if Client.objects.filter(code=code).exists():
            raise CommandError(f"tenant {code} already exists")

        client = Client.objects.create(
            code=code,
            schema_name=f"tenant_{code}",
            legal_name=opts["name"],
            display_name=opts["name"],
        )
        Domain.objects.create(domain=f"{code}.localhost", tenant=client, is_primary=True)

        user, created = GlobalUser.objects.get_or_create(
            email=opts["email"], defaults={"full_name": "Administrator"}
        )
        if created:
            user.set_unusable_password()
            user.save()

        TenantAccess.objects.create(user=user, tenant=client, is_default=True)

        with schema_context(client.schema_name):
            self.seed_masters()

        self.stdout.write(self.style.SUCCESS(
            f"provisioned {client.schema_name} for {opts['name']}"
        ))

    def seed_masters(self) -> None:
        """Seed reference data: body regions, joints, modalities, roles, service types.

        Copy exercises from the shared catalog here too.
        """
        # TODO(DSS-23): implement master data seeding
