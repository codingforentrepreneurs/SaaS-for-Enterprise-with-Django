from django.apps import apps
from django.db import connection
from contextlib import contextmanager

from helpers.db import statements as db_statements

DEFAULT_SCHEMA = "public"

@contextmanager
def use_public_schema():
    """
    with use_public_schema():
        Tenant.object.all()
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name=DEFAULT_SCHEMA))
        yield
    finally:
        print("something")
