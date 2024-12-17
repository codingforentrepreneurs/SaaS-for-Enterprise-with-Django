from typing import Any
from django.db import connection
from django.core.management import BaseCommand, call_command

from django.contrib.auth import get_user_model

from helpers.db import statements as db_statements

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        schema_name = 'example'
        with connection.cursor() as cursor:
            cursor.execute(
                db_statements.CREATE_SCHEMA_SQL.format(schema_name=schema_name)
            )
            cursor.execute(
                db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name=schema_name)
            )
        # python manage.py migrate --no-input
        call_command("migrate", interactive=False)
        # User = get_user_model()
        # user_a = User.objects.create_superuser(
        #     username='example',
        #     password='example1233'
        # )
        