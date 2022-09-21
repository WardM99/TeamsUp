"""Error when the database is not fully migrated"""
class PendingMigrationsException(Exception): # pragma: no cover
    """
    Exception indication the database is not yet fully migrated.
    """
