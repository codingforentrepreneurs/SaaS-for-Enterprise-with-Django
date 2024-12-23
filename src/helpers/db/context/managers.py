
from django.conf import settings
from django.db import connections, OperationalError

from contextlib import contextmanager
import dj_database_url

@contextmanager
def use_dynamic_database_url(db_url, alias='dynamic_db', schema='public'):
    """
    A context manager to temporarily add/use a dynamic database from a URL.

    Args:
        db_url (str): The database URL (e.g. "postgres://user:pass@host:5432/dbname").
        alias (str): The alias for the dynamic database (default: 'dynamic_db').
        schema (str): The schema to set in search_path (default: 'public').

    Yields:
        str: The alias of the database being used.
    """
    # Parse the URL into a proper Django database config dict
    database_config = dj_database_url.parse(db_url, engine='django.db.backends.postgresql')

    # Provide fallback or extra config as needed
    database_config.setdefault('TIME_ZONE', getattr(settings, 'TIME_ZONE', 'UTC'))
    database_config.setdefault('AUTOCOMMIT', True)
    database_config.setdefault('ATOMIC_REQUESTS', False)

    # If you want a specific schema for Postgres, set search_path
    if schema:
        database_config.setdefault('OPTIONS', {})
        # Combine existing options with search_path
        existing_options = database_config['OPTIONS'].get('options', '')
        new_options = f"-c search_path={schema}"
        if existing_options:
            new_options = existing_options + " " + new_options
        database_config['OPTIONS']['options'] = new_options

    # Save any existing config for this alias so we can restore it later
    original_config = connections.databases.get(alias)

    try:
        # Override the alias with our new dynamic config
        connections.databases[alias] = database_config

        # Force a connection to ensure we can connect
        connection = connections[alias]
        connection.ensure_connection()

        # Hand over control
        yield alias

    except OperationalError as e:
        raise RuntimeError(f"Could not connect to the database '{alias}' using url: {db_url}. Error: {e}")

    finally:
        # Restore the original config or remove the alias
        if original_config is not None:
            connections.databases[alias] = original_config
        else:
            del connections.databases[alias]