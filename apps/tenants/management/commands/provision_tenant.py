"""Provision a new clinic: schema, migrations, master data, first admin.

    python manage.py provision_tenant --code cbe --name "Day2Day Coimbatore" \
        --email admin@day2daycare.in
"""
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django_tenants.utils import schema_context

from apps.accounts.models import GlobalUser, TenantAccess
from apps.billing.models import Package
from apps.branches.models import Branch, Discipline
from apps.exercises.models import Exercise, ExerciseCategory
from apps.scheduling.models import Modality, ServiceType
from apps.tenants.models import Client, Domain


class Command(BaseCommand):
    help = "Create a tenant schema and seed it."

    def add_arguments(self, parser):
        parser.add_argument("--code", required=True)
        parser.add_argument("--name", required=True)
        parser.add_argument("--email", required=True)
        parser.add_argument("--password", default=None)

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
        password = opts.get("password")
        if password:
            user.set_password(password)
            user.save()
        elif created:
            user.set_unusable_password()
            user.save()

        TenantAccess.objects.create(user=user, tenant=client, is_default=True)

        with schema_context(client.schema_name):
            self.seed_masters()

        self.stdout.write(self.style.SUCCESS(
            f"provisioned {client.schema_name} for {opts['name']}"
        ))

    def seed_masters(self) -> None:
        """Seed the first clinic with the essential clinic and scheduling metadata.

        The tenant needs at least one branch, a core discipline, and the default
        scheduling catalog used for patient appointments and therapy sessions.
        """
        Branch.objects.get_or_create(
            code="main",
            defaults={
                "name": "Main Clinic",
                "city": "Bangalore",
                "state": "Karnataka",
                "address": "Primary clinic location",
                "is_active": True,
            },
        )

        Discipline.objects.get_or_create(
            code="physiotherapy",
            defaults={
                "name": "Physiotherapy",
                "description": "Core physiotherapy and rehabilitation care.",
                "is_active": True,
            },
        )

        for name, duration in {
            "Physiotherapy Consultation": 45,
            "Manual Therapy": 30,
            "Exercise Therapy": 30,
            "Electrotherapy": 30,
        }.items():
            ServiceType.objects.get_or_create(
                name=name,
                defaults={"duration_minutes": duration, "is_active": True},
            )

        for name in [
            "Manual Therapy",
            "Exercise Therapy",
            "Electrotherapy",
            "Therapeutic Ultrasound",
            "Stretching",
        ]:
            Modality.objects.get_or_create(name=name, defaults={"is_active": True})

        mobility, _ = ExerciseCategory.objects.get_or_create(
            name="Mobility",
            defaults={"description": "Mobility and flexibility work for recovery and movement quality.", "is_active": True},
        )
        Exercise.objects.get_or_create(
            code="ankle-dorsiflexion",
            defaults={
                "category": mobility,
                "name": "Ankle Dorsiflexion Mobility",
                "body_part": "Ankle",
                "difficulty": 1,
                "default_sets": 2,
                "default_reps": 10,
                "default_hold_seconds": 20,
                "instructions": "Sit with the knee over the foot and gently move the shin forward.",
                "precautions": "Stop if sharp pain or tingling occurs.",
                "is_active": True,
            },
        )

        Package.objects.get_or_create(
            code="starter-10",
            defaults={
                "name": "Starter 10 Sessions",
                "package_type": "session_bundle",
                "validity_days": 120,
                "session_count": 10,
                "price": 7500,
                "currency": "INR",
                "is_active": True,
            },
        )
