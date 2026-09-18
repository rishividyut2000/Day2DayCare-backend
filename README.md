# Day2DayCare — Backend

Multi-tenant physiotherapy platform API.
**Python 3.14 · Django 5.2 LTS · DRF · django-tenants 3.14 · PostgreSQL 16 · Celery/Redis**

Each clinic is a tenant with its own PostgreSQL schema (`tenant_<code>`).
Shared data (tenant registry, global user accounts, exercise master library)
lives in the `public` schema.

## Quick start

```bash
cp .env.example .env
docker compose up -d db redis
uv sync                    # or: pip install -e ".[dev]"
python manage.py migrate_schemas --shared
python manage.py provision_tenant --code demo --name "Demo Clinic" --email admin@demo.in
python manage.py runserver
```

API docs: http://localhost:8000/api/v1/docs/
Django admin (public schema): http://localhost:8000/admin/

## Layout

```
config/          settings, urls, celery, asgi/wsgi
apps/
  common/        base models, middleware, pagination, error handling
  tenants/       Client + Domain models, provisioning command   [SHARED]
  accounts/      global users, tenant access, JWT auth          [SHARED]
  catalog/       exercise master library                        [SHARED]
  branches/      branches, disciplines, settings, numbering     [TENANT]
  staff/         therapists, availability, zones                [TENANT]
  patients/      patients, addresses, consents, documents       [TENANT]
  referrals/     referring doctors, referrals, prescriptions    [TENANT]
  clinical/      episodes, assessments, measures                [TENANT]
  exercises/     tenant exercise library                        [TENANT]
  plans/         treatment plans, phases, revisions             [TENANT]
  scheduling/    appointments, sessions, home visits            [TENANT]
  billing/       packages, invoices, payments                   [TENANT]
  notifications/ templates, reminders, delivery log             [TENANT]
  reports/       materialised views, report endpoints           [TENANT]
```

## The two rules that matter

**1. Schema name never comes from the client.** The JWT carries a tenant *id*.
`TenantFromJWTMiddleware` looks the schema name up from `public.tenants` and
validates it against `^tenant_[a-z0-9_]{1,40}$` before touching a connection.
One bypass here is a cross-clinic data leak, so it lives in one function.

**2. Business rules live in `services.py`, never in views.** Package consumption
and invoice totalling both run from an HTTP request *and* from a Celery task.
A rule written in a view is a rule you will duplicate.

## Migrations

```bash
python manage.py makemigrations
python manage.py migrate_schemas --shared      # public schema only
python manage.py migrate_schemas               # every tenant schema
```

Never run plain `migrate`. `migrate_schemas` is what keeps tenants in step.
