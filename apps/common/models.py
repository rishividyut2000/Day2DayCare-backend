"""Abstract bases every model in the project inherits from.

Conventions decided once, here:
  - UUID primary keys (safe for offline create, no enumeration)
  - created/updated audit columns on everything
  - soft delete on clinical and financial records — nothing is hard-deleted
  - row_version for optimistic locking where two roles edit the same record
"""
import uuid

from django.db import models


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.UUIDField(null=True, blank=True)
    updated_by = models.UUIDField(null=True, blank=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    def alive(self):
        return self.filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True, db_index=True)
    deleted_by = models.UUIDField(null=True, blank=True)

    objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True

    def soft_delete(self, actor_id=None):
        from django.utils import timezone

        self.deleted_at = timezone.now()
        self.deleted_by = actor_id
        self.save(update_fields=["deleted_at", "deleted_by"])


class VersionedModel(models.Model):
    """Optimistic locking. Reject stale writes rather than last-write-wins."""

    row_version = models.PositiveIntegerField(default=1)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimeStampedModel, SoftDeleteModel):
    class Meta:
        abstract = True
