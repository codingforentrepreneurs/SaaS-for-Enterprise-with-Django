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
    with connection.cursor() as cursor:
        sql = f'SET search_path TO "{schema_to_use}";'
        cursor.execute(sql)
        connection.schema_name = schema_to_use



@contextmanager
def use_tenant_schema(schema_name, create_if_missing=True, revert_public=True):
    """
    with use_tenant_schema(schema_name):
        Visit.object.all()
    """
    try:
        with connection.cursor() as cursor:
            if create_if_missing and not check_if_schema_exists(schema_name):
                cursor.execute(
                    f'CREATE SCHEMA IF NOT EXISTS "{schema_name}";'
                )
            sql = f'SET search_path TO "{schema_name}";'
            cursor.execute(sql)
        yield
    finally:
        if revert_public:
            activate_tenent_schema(DEFAULT_SCHEMA)


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
