from typing import Any

from django.apps import apps
from django.conf import settings
from django.db import connection
from django.core.management import BaseCommand, call_command

from helpers.db import statements as db_statements

CUSTOMER_INSTALLED_APPS = getattr(settings, 'CUSTOMER_INSTALLED_APPS', [])

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        schemas = ['example']
        with connection.cursor() as cursor:
            cursor.execute(
                db_statements.CREATE_SCHEMA_SQL.format(schema_name="public")
            )
            cursor.execute(
                db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name="public")
            )
            call_command("migrate", interactive=False)

        for schema_name in schemas:
            with connection.cursor() as cursor:
                cursor.execute(
                    db_statements.CREATE_SCHEMA_SQL.format(schema_name=schema_name)
                )
                cursor.execute(
                    db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name=schema_name)
                )
            for app in apps.get_app_configs():
                # print(app)
                app_name = app.name
                if app_name not in CUSTOMER_INSTALLED_APPS:
                    continue
                print("customer app", app)
                try:    
                    call_command("migrate", app.label, interactive=False)
                except:
                    continue
                # python manage.py migrate --no-input
                # 
        # User = get_user_model()
        # user_a = User.objects.create_superuser(
        #     username='example',
        #     password='example1233'
        # )
        