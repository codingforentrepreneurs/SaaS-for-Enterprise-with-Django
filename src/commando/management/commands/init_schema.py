from typing import Any
from django.db import connection
from django.core.management.base import BaseCommand

from helpers.db import statements as db_statements

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        schema_name = 'example'
        with connection.cursor() as cursor:
            cursor.execute(
                db_statements.CREATE_SCHEMA_SQL.format(schema_name=schema_name)
            )