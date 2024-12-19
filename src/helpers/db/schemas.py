from django.apps import apps
from django.db import connection
from contextlib import contextmanager

from helpers.db import statements as db_statements

DEFAULT_SCHEMA = "public"


def check_if_schema_exists(schema_name, require_check=False):
    if schema_name == DEFAULT_SCHEMA and not require_check:
        return True
    exists = False
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name = %s
        """, [schema_name])
        exists = cursor.fetchone() is not None
    return exists


def activate_tenent_schema(schema_name):
    is_check_exists_required = schema_name != DEFAULT_SCHEMA
    schema_to_use = DEFAULT_SCHEMA
    if is_check_exists_required and check_if_schema_exists(schema_name):
        schema_to_use = schema_name
    if schema_to_use == connection.schema_name:
        print("Schema activated, return")
        return
    with connection.cursor() as cursor:
        sql = f'SET search_path TO "{schema_to_use}";'
        cursor.execute(sql)
        connection.schema_name = schema_to_use


@contextmanager
def use_public_schema(revert_schema_name=None, revert_schema=False):
    """
    with use_public_schema():
        Tenant.object.all()
    """
    try:
        schema_to_use = DEFAULT_SCHEMA
        with connection.cursor() as cursor:
            sql = f'SET search_path TO "{schema_to_use}";'
            cursor.execute(sql)
        yield
    finally:
        if revert_schema:
            activate_tenent_schema(revert_schema_name)
