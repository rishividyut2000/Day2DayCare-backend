"""Therapist double-booking guard.

Not expressible in the Django ORM. Django will not manage this constraint but
the database still enforces it — which is the point. The API surfaces the
resulting 409; an application-level pre-check is for UX only and loses the
race under concurrency.
"""
from django.db import migrations

SQL = """
ALTER TABLE scheduling_appointment
  ADD CONSTRAINT ex_appt_no_overlap
  EXCLUDE USING gist (
    therapist_id WITH =,
    tstzrange(scheduled_start, scheduled_end) WITH &&
  ) WHERE (status IN ('scheduled','confirmed','checked_in') AND deleted_at IS NULL);
"""

REVERSE = "ALTER TABLE scheduling_appointment DROP CONSTRAINT ex_appt_no_overlap;"


class Migration(migrations.Migration):
    dependencies = [("scheduling", "0001_initial")]
    operations = [migrations.RunSQL(SQL, REVERSE)]
