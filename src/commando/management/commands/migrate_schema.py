from typing import Any

from django.apps import apps
from django.core.management import BaseCommand, call_command
from django.db import connection
from django.conf import settings
from django.db.migrations.executor import MigrationExecutor

from helpers.db import statements as db_statements
from helpers.db.schemas import (
    use_public_schema,
    use_tenant_schema
)

from tenants import tasks

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Starting migrations")
        tasks.migrate_tenant_schemas_task()
        self.stdout.write(self.style.SUCCESS("All migrations for CUSTOMER_APPS are completed."))