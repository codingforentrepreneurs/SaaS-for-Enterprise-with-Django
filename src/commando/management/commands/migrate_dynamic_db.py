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

from decouple import config
import dj_database_url

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        db_url = config("DB_URL_2", default=None)
        if db_url is None:
            return
        alias = "db-2"
        # default -> public -> database
        # qs = Tenant.objects.all()
        # obj = qs.first()
        # db_url = obj.db_url
        db_parsed_config = dj_database_url.parse(
                db_url,
                conn_health_checks=True,
                engine='helpers.db.engine'
        )
        db_parsed_config.setdefault('TIME_ZONE', getattr(settings, 'TIME_ZONE', 'UTC'))
        db_parsed_config.setdefault('AUTOCOMMIT', True)
        db_parsed_config.setdefault('ATOMIC_REQUESTS', False)
        settings.DATABASES[alias] = db_parsed_config
        call_command('migrate', database=alias)