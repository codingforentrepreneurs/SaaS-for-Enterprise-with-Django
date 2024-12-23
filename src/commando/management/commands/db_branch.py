import uuid
from typing import Any

from django.conf import settings

from django.core.management.base import BaseCommand

from helpers.neonctl.clients import NeonBranchClient

NEON_MIGRATION_BRANCH_BASE = getattr(settings, "NEON_MIGRATION_BRANCH_BASE", "saas_migration")

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--clear-migrations",
            action="store_true",
            help="Clear migrations before branching",
        )

    def handle(self, *args: Any, **options: Any):
        neon = NeonBranchClient()
        clear_migrations = options["clear_migrations"]
        if clear_migrations:
            print("Clearing neon migration branches")
            branches = neon.list_branches()
            deleted_branches = []
            for branch in branches:
                if branch["name"].startswith(NEON_MIGRATION_BRANCH_BASE):
                    neon.delete_branch(branch["id"])
                    deleted_branches.append(branch["name"])
                    import time

                    time.sleep(2)
            print(f"Deleted branches: {deleted_branches}")
            return
        print("Branching Neon")
        new_branch_name = f"{NEON_MIGRATION_BRANCH_BASE}_{uuid.uuid1()}"
        try:
            neon.create_branch(name=new_branch_name)
            print(f"Created branch: {new_branch_name}")
        except Exception as e:
            print(f"Failed creating branch: {e}")
            return