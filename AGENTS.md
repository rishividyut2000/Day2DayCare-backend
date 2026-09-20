# AGENTS.md

Guidance for AI coding agents working in this repository. See [README.md](README.md)
for the human-facing quick start; this file goes deeper on conventions an agent
needs to not break tenancy, billing, or clinical data.

## What this is

Multi-tenant physiotherapy platform API — Python 3.14, Django 5.2 LTS, DRF,
django-tenants 3.14, PostgreSQL 16, Celery/Redis. Each clinic is a tenant with
its own Postgres schema (`tenant_<code>`); shared data (tenant registry, global
user accounts, the exercise master library) lives in the `public` schema.

## Layout

```
config/          settings (base/local/production/test), urls, celery, asgi/wsgi
apps/
  common/        base models, middleware, pagination, error handling, exceptions
  tenants/       Client + Domain models, provisioning command          [SHARED]
  accounts/      global users, tenant access, JWT auth                 [SHARED]
  catalog/       exercise master library                               [SHARED]
  branches/      branches, disciplines, settings, numbering            [TENANT]
  staff/         therapists, availability, zones                       [TENANT]
  patients/      patients, addresses, consents, documents              [TENANT]
  referrals/     referring doctors, referrals, prescriptions           [TENANT]
  clinical/      episodes, assessments, measures                       [TENANT]
  exercises/     tenant exercise library                               [TENANT]
  plans/         treatment plans, phases, revisions                    [TENANT]
  scheduling/    appointments, sessions, home visits                   [TENANT]
  billing/       packages, invoices, payments                          [TENANT]
  notifications/ templates, reminders, delivery log                    [TENANT]
  reports/       materialised views, report endpoints                  [TENANT]
tests/           cross-app tests (tenant isolation, core schema/API)
```

Within each app: `models.py`, `serializers.py`, `services.py` (business rules),
`views.py`, `urls.py`, `admin.py`, `tests/`. `SHARED_APPS` vs `TENANT_APPS` is
defined in [config/settings/base.py](config/settings/base.py) — an app only
migrates into the schemas it's listed under.

## The two rules that matter

**1. Schema name never comes from the client.** The JWT carries a tenant *id*
(`tid` claim), never a schema name.
[`TenantFromJWTMiddleware`](apps/common/middleware.py) looks the schema up from
`public.tenants`, checks `tenant.is_active`, and validates it against
`^tenant_[a-z0-9_]{1,40}$` before calling `connection.set_tenant(...)`. This is
the entire tenancy boundary — one bypass here is a cross-clinic data leak, so
it lives in exactly this one function. Don't add a second path that resolves
schemas (from a query param, header, subdomain, etc.) without routing it
through this same validated lookup.

**2. Business rules live in `services.py`, never in views.** Package
consumption, invoice totalling, and similar rules must be callable from an
HTTP request *and* from a Celery task. A rule written into a view is a rule
you will end up duplicating into a task. When adding logic that a
`tasks.py` will also need (billing, notifications, reports, scheduling,
accounts all have one), put it in `services.py` and call it from both places.

## Base model conventions ([apps/common/models.py](apps/common/models.py))

Every model composes from these abstract bases — don't reinvent them:

- `UUIDModel` — UUID primary keys (safe for offline create, no enumeration).
- `TimeStampedModel` — `created_at`/`updated_at`/`created_by`/`updated_by`.
- `SoftDeleteModel` — `deleted_at`/`deleted_by` + `.objects.alive()`; clinical
  and financial records are **never hard-deleted**. Deleting a row via
  `.delete()` instead of `.soft_delete()` on these models is a bug, not a
  style choice.
- `VersionedModel` — `row_version` for optimistic locking where two roles
  (e.g. therapist + billing) can edit the same record concurrently. Reject
  stale writes; don't silently last-write-wins.
- `BaseModel` — `UUIDModel + TimeStampedModel + SoftDeleteModel` combined;
  the default base for tenant-schema models holding clinical/financial data.

## Auth & permissions

- `AUTH_USER_MODEL = accounts.GlobalUser` — users are global (public schema),
  tenant access is a separate relation, not a per-tenant user table.
- JWT via `djangorestframework-simplejwt`. Public, unauthenticated paths are
  enumerated in `PUBLIC_PATHS` in the middleware (`/admin/`, `/health/`,
  login/refresh, schema/docs) — adding a new public endpoint means adding it
  there deliberately, not as a side effect of a view's permission class.
- `apps/common/permissions.py` holds shared DRF permission classes.

## Running things

```bash
docker compose up -d db redis        # or: make up
uv sync                              # or: pip install -e ".[dev]"
python manage.py migrate_schemas --shared   # public schema only
python manage.py migrate_schemas            # every tenant schema — NEVER plain `migrate`
python manage.py provision_tenant --code demo --name "Demo Clinic" --email admin@demo.in
python manage.py runserver
```

`make migrate` / `make tenant CODE=... NAME=... EMAIL=...` wrap the same
commands. `migrate_schemas` is what keeps tenants in step — plain `migrate`
will only touch whatever schema the connection happens to be on.

API docs: `http://localhost:8000/api/v1/docs/` · Django admin (public schema
only): `http://localhost:8000/admin/`.

## Tests

```bash
pytest                # or: make test
ruff check . && mypy . # or: make lint
ruff format . && ruff check --fix .  # or: make fmt
```

- Settings module for tests: `config.settings.test`
  ([pyproject.toml](pyproject.toml) `[tool.pytest.ini_options]`).
- `tests/` at repo root covers cross-cutting concerns —
  [tests/test_tenant_isolation.py](tests/test_tenant_isolation.py) in
  particular exists to prove one tenant cannot read another's data. Any
  change touching the middleware, `connection.set_tenant`, or schema
  resolution should be checked against this file, and extended if it adds a
  new way schemas get resolved.
- Per-app tests live in `apps/<app>/tests/`.
- `tests/conftest.py` provides `tenant_a`/`tenant_b` fixtures (two isolated
  clinics) and an `in_tenant` fixture wrapping `django_tenants.utils.schema_context`
  for running assertions inside a specific tenant's schema.
- `ruff` lint rules include `S` (bandit/security) and `DJ` (Django-specific);
  `S101` (assert usage) is deliberately ignored since pytest relies on plain
  `assert`.

## Migrations

```bash
python manage.py makemigrations
python manage.py migrate_schemas --shared
python manage.py migrate_schemas
```

An app in `SHARED_APPS` migrates once, into `public`. An app in `TENANT_APPS`
migrates into every `tenant_<code>` schema. Moving an app between the two
lists is a data-affecting decision, not a refactor — don't do it without
understanding where its existing data already lives.

## Related docs

- [README.md](README.md) — human quick start.
- [SKILLS.md](SKILLS.md) — index of the third-party agent skill packages in
  `.agents/skills/` (Postgres, Redis, DRF performance, SQL optimization,
  security scanning) available to agents working in this repo.
