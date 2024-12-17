from typing import Any

from django.core.management import BaseCommand, call_command
from django.db import connection
from django.conf import settings
from django.apps import apps
from django.db.migrations.executor import MigrationExecutor

from helpers.db import statements as db_statements

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        schemas = ["example_a"]
        skip_public = True

        if not skip_public:
            with connection.cursor() as cursor:
                cursor.execute(
                    db_statements.CREATE_SCHEMA_SQL.format(schema_name="public")
                )
                cursor.execute(
                    db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name="public")
                )
                call_command("migrate", interactive=False)

        
        
        for schema_name in schemas:
            # Check if the schema already exists
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT schema_name 
                    FROM information_schema.schemata 
                    WHERE schema_name = %s
                """, [schema_name])
                schema_exists = bool(cursor.fetchone())

                if not schema_exists:
                    cursor.execute(
                        db_statements.CREATE_SCHEMA_SQL.format(schema_name=schema_name)
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created schema '{schema_name}'"))

                # Set the search_path
                cursor.execute(db_statements.ACTIVATE_SCHEMA_SQL.format(schema_name=schema_name))

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
                self.stdout.write(f"Applying migrations for '{app_label}':")
                for migration in ordered_migrations:
                    self.stdout.write(f"  - {migration.app_label}.{migration.name}")

                # Apply the migrations
                # The plan to migrate is the leaf_nodes for this app
                executor.migrate(leaf_nodes)
                # Rebuild the graph after applying migrations
                executor.loader.build_graph()

            self.stdout.write(self.style.SUCCESS("All migrations for CUSTOMER_APPS are completed."))