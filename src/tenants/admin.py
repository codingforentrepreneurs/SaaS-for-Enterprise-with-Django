from django.contrib import admin

# Register your models here.
from .models import Tenant

class TenantAdmin(admin.ModelAdmin):
    readonly_fields = ['schema_name', 'active_at', 'inactive_at', 'timestamp', 'updated' ]
    list_display = ['subdomain', 'owner', 'schema_name']

admin.site.register(Tenant, TenantAdmin)