# Database Migration Guide

## Overview

This project uses Alembic for database migrations. The migration has been configured to work with PostgreSQL.

## Database URL

The database URL is configured via the `.env` file:

```
DATABASE_URL=postgresql://postgres:BospJhRMqpPGUyBcvisuWNfsvgoXQmvt@acela.proxy.rlwy.net:44859/railway
```

## Common Alembic Commands

### Generate a new migration

When you make changes to your models, generate a new migration:

```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply migrations (upgrade)

To apply all pending migrations:

```bash
alembic upgrade head
```

To apply migrations up to a specific version:

```bash
alembic upgrade <revision_id>
```

### Rollback migrations (downgrade)

To rollback the last migration:

```bash
alembic downgrade -1
```

To rollback to a specific version:

```bash
alembic downgrade <revision_id>
```

### View migration history

To view the current migration status:

```bash
alembic history
```

To view migration history with verbose output:

```bash
alembic history -v
```

### View current revision

To see the current database revision:

```bash
alembic current
```

## Current Migration Status

The current migration version is: `d3941962d7a2` (Initial migration)

## Tables Created

The initial migration created the following tables:

1. **exam_files** - Stores information about exam files
2. **exam_schedules** - Stores exam schedules for students
3. **subscriptions** - Stores user subscription preferences
4. **email_logs** - Stores email sending logs
5. **alembic_version** - Tracks migration version

## Foreign Key Relationships

- `exam_schedules.exam_file_id` → `exam_files.id`
- `email_logs.subscription_id` → `subscriptions.id`
- `email_logs.exam_schedule_id` → `exam_schedules.id`

## Indexes

The following indexes were created:

- `ix_subscriptions_email` on subscriptions(email)
- `ix_subscriptions_subject_code` on subscriptions(subject_code)
- `ix_exam_schedules_student_id` on exam_schedules(student_id)
- `ix_exam_schedules_student_name` on exam_schedules(student_name)
- `ix_exam_schedules_subject_code` on exam_schedules(subject_code)
- `ix_email_logs_email` on email_logs(email)
- `ix_email_logs_status` on email_logs
