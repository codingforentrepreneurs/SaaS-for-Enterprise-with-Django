from django.apps import apps
from django.db import connection

from helpers.db.schemas import (
    use_public_schema
)
from helpers.db import statements as db_statements

class SchemaTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        host = request.get_host()
        host_portless = host.split(":")[0]
        host_split = host_portless.split('.')
        subdomain = None
        if len(host_split) > 1:
            subdomain = host_split[0]
        schema_name = self.get_schema_name(subdomain=subdomain)
        self.set_search_path(schema_name)
        return self.get_response(request)
    
    def set_search_path(self, schema_name):
        print("activate the schema", schema_name)
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT schema_name 
                FROM information_schema.schemata 
                WHERE schema_name = %s
            """, [schema_name])
            schema_exists = bool(cursor.fetchone())

            if not schema_exists:
                schema_name = "public"
            cursor.execute(db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name=schema_name))
        return 
    
    def get_schema_name(self, subdomain=None):
        if subdomain in [None, "localhost", 'desalsa']:
            return "public"
        schema_name = "public"
        with use_public_schema():
            Tenant = apps.get_model('tenants', 'Tenant')
            try:
                obj = Tenant.objects.get(subdomain=subdomain)
                schema_name =  obj.schema_name
            except Tenant.DoesNotExist:
                print(f"{subdomain} does not exist as Tenant")
            except Exception as e:
                print(f"{subdomain} does not exist as Tenant.\n {e}")
        return schema_name