# from celery import shared_task
from typing import Any

from django.apps import apps
from django.core.management import call_command
from django.db import connection
from django.conf import settings
from django.db.migrations.executor import MigrationExecutor
from helpers.db.schemas import (
    use_public_schema,
    use_tenant_schema
)


# @shared_task
def migrate_public_schema_task():
    with use_public_schema():
        call_command("migrate", interactive=False)


# @shared_task
def migrate_tenant_task(tenant_id:str, branch=True):
    if branch:
        call_command("db_branch")
    Tenant = apps.get_model("tenants", "Tenant")
    try:
        instance = Tenant.objects.get(id=tenant_id)
    except Exception as e:
        print(f'Tenant {tenant_id} failed: {e}')
        return
    schema_name = instance.schema_name
    with use_tenant_schema(schema_name, create_if_missing=True, revert_public=True):
        # Initialize the executor after setting the search path
        executor = MigrationExecutor(connection)
        loader = executor.loader
        loader.build_graph()  # Ensure the graph is up-to-date

        customer_apps = getattr(settings, 'CUSTOMER_INSTALLED_APPS', [])
        customer_app_configs = [
            app_config for app_config in apps.get_app_configs()
            if app_config.name in customer_apps
        ]

        # For each customer app, determine what migrations need to be run
        for app_config in customer_app_configs:
            app_label = app_config.label

            # Get all leaf nodes for this app
            leaf_nodes = [
                node for node in loader.graph.leaf_nodes()
                if node[0] == app_label
            ]

            if not leaf_nodes:
                # App has no migrations at all, do nothing silently
                continue

            # For each leaf node, figure out the plan to get there
            # If the plan is empty, it means no new migrations are needed.
            full_plan = []
            for leaf in leaf_nodes:
                plan = executor.migration_plan([leaf])
                for migration, backwards in plan:
                    if not backwards:  # only include forward migrations
                        full_plan.append(migration)

            # Remove duplicates while preserving order
            seen = set()
            ordered_migrations = []
            for m in full_plan:
                if m not in seen:
                    seen.add(m)
                    ordered_migrations.append(m)

            if not ordered_migrations:
                # No forward migrations needed for this app
                continue

            # Print out which migrations are going to be applied
            print(f"Applying migrations for '{app_label}':")
            for migration in ordered_migrations:
                print(f"  - {migration.app_label}.{migration.name}")

            # Apply the migrations
            # The plan to migrate is the leaf_nodes for this app
            executor.migrate(leaf_nodes)
            # Rebuild the graph after applying migrations
            executor.loader.build_graph()


# @shared_task
def migrate_tenant_schemas_task():
    Tenant = apps.get_model("tenants", "Tenant")
    qs = Tenant.objects.none()
    with use_public_schema():
        qs = Tenant.objects.all().values_list('id', flat=True)
        call_command("migrate", interactive=False)
    call_command("db_branch")
    for tenant_id in qs:
        migrate_tenant_task(tenant_id, branch=False)