from django.db.backends.postgresql import base

class DatabaseWrapper(base.DatabaseWrapper):
    schema_name = None