# SKILLS.md

Index of the third-party agent skill packages installed in
[.agents/skills/](.agents/skills/), tracked by [skills-lock.json](skills-lock.json).
These are pulled from external repos (see each entry's source below) — don't
hand-edit a `SKILL.md` in place; update the source and reinstall instead. This
file exists so an agent can tell at a glance which installed skill applies to
a given task in *this* project, without opening all fourteen.

## Directly relevant to this stack

This project is Django 5.2 + DRF + django-tenants + PostgreSQL 16 + Celery/Redis
(see [AGENTS.md](AGENTS.md)). These skills apply to everyday work here:

| Skill | Use when |
|---|---|
| [drf-api-performance](.agents/skills/drf-api-performance/SKILL.md) | Adding/changing a DRF viewset, serializer, pagination class, or queryset — N+1s, `select_related`/`prefetch_related`, keeping ORM calls out of serializers. |
| [postgres-best-practices](.agents/skills/postgres-best-practices/SKILL.md) | Schema design, indexing, migrations, query optimization on Postgres 14–18. |
| [sql-optimization-patterns](.agents/skills/sql-optimization-patterns/SKILL.md) | Debugging a slow query, reading an `EXPLAIN` plan, indexing strategy. |
| [database-migration](.agents/skills/database-migration/SKILL.md) | Zero-downtime schema/data migration strategy and rollback procedures. General ORM migration guidance — for the django-tenants specifics (`migrate_schemas`, SHARED_APPS vs TENANT_APPS) see [AGENTS.md](AGENTS.md#migrations) instead. |
| [python-security-scan](.agents/skills/python-security-scan/SKILL.md) | Security audit of a Django view/serializer, dependency CVE check, pre-deploy scan. Relevant to `apps/common/middleware.py` tenant-boundary code especially — see [AGENTS.md](AGENTS.md#the-two-rules-that-matter). |

Redis here is Celery's broker/result backend and `django-celery-beat`'s
scheduler — not a data store the app queries directly. If that changes
(caching, session store, rate limiting):

| Skill | Use when |
|---|---|
| [redis-core](.agents/skills/redis-core/SKILL.md) | Choosing a Redis data structure, key naming conventions. |
| [redis-connections](.agents/skills/redis-connections/SKILL.md) | Configuring a Redis client, pooling, avoiding slow commands. |
| [redis-security](.agents/skills/redis-security/SKILL.md) | Auth, ACLs, TLS, network exposure for a production Redis instance. |
| [redis-observability](.agents/skills/redis-observability/SKILL.md) | Monitoring/alerting or diagnosing a Redis performance regression. |
| [redis-clustering](.agents/skills/redis-clustering/SKILL.md) | Sharded Redis Cluster, CROSSSLOT errors, replica reads. |

## Not applicable to this project

These are installed but cover capabilities this codebase doesn't use — no LLM
integration, no Redis Search/vector index, no semantic caching. Skip them
unless the project's scope changes:

- [redis-search](.agents/skills/redis-search/SKILL.md) — `FT.CREATE`/`FT.SEARCH`, vector similarity, RAG retrieval.
- [redis-semantic-cache](.agents/skills/redis-semantic-cache/SKILL.md) — LangCache semantic caching of LLM responses.
- [iris-development](.agents/skills/iris-development/SKILL.md) — Redis Agent Memory (RAM) for AI agents.

## Meta

- [skill-creator](.agents/skills/skill-creator/SKILL.md) — guide for authoring
  a new skill. Use this only if you're adding a *new* skill package to
  `.agents/skills/`, not for applying an existing one.

## Adding or updating a skill

Skills here are managed externally (see `source`/`sourceType` per entry in
[skills-lock.json](skills-lock.json), all `github`). Don't edit a `SKILL.md`
directly — changes will be overwritten on the next sync from source. If a
skill's guidance is wrong or stale for this project, note the correction in
this file or in [AGENTS.md](AGENTS.md) instead of patching the vendored copy.
