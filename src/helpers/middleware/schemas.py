from django.apps import apps
from django.db import connection
from django.core.cache import cache

from helpers.db.schemas import (
    use_public_schema,
    activate_tenent_schema
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
        activate_tenent_schema(schema_name)
        return self.get_response(request)
    
    def get_schema_name(self, subdomain=None):
        if subdomain in [None, "localhost", 'desalsa']:
            return "public"
        schema_name = "public"
        cache_key = f"subdomain_schema:{subdomain}"
        cache_val = cache.get(cache_key)
        if cache_val:
            print('schema cache hit', cache_val)
            return cache_val
        with use_public_schema():
            Tenant = apps.get_model('tenants', 'Tenant')
            try:
                obj = Tenant.objects.get(subdomain=subdomain)
                schema_name =  obj.schema_name
            except Tenant.DoesNotExist:
                print(f"{subdomain} does not exist as Tenant")
            except Exception as e:
                print(f"{subdomain} does not exist as Tenant.\n {e}")
            cache_ttl = 60 # seconds
            cache.set(cache_key, str(schema_name), cache_ttl)
        return schema_name