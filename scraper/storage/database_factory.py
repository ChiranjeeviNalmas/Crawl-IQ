"""
Database adapter factory.

This module creates the appropriate database adapter based on configuration.
It implements the Factory pattern to decouple database creation from usage.

Why use a factory?
- Centralizes database adapter creation logic
- Easy to add new database types without changing existing code
- Follows the Factory pattern for object creation
- Makes switching databases as simple as changing configuration
"""

from typing import Optional
from .database_base import DatabaseAdapter
from .mongodb_adapter import MongoDBAdapter
from .settings import settings
from .constants import DB_TYPE_MONGODB, DB_TYPE_POSTGRESQL
from ..logger import get_logger

log = get_logger("database_factory")


class DatabaseFactory:
    """
    Factory for creating database adapters.
    
    This class creates the appropriate database adapter based on
    the DB_TYPE setting. To add a new database:
    1. Create a new adapter class inheriting from DatabaseAdapter
    2. Add a case in create_adapter() method
    3. Update .env with new DB_TYPE
    """
    
    _adapter = None  # Lazy-loaded adapter

    @staticmethod
    def create_adapter() -> DatabaseAdapter:
        """
        Create a database adapter based on settings.
        
        Returns:
            DatabaseAdapter: Appropriate database adapter instance.
        
        Raises:
            ValueError: If database type is not supported.
        """
        db_type = settings.db_type.lower()
        
        if db_type == DB_TYPE_MONGODB:
            log.info("Creating MongoDB adapter")
            db_config = settings.get_db_config()
            return MongoDBAdapter(
                uri=db_config["uri"],
                db_name=db_config["db"],
                collection_name=db_config["collection"],
            )
        
        elif db_type == DB_TYPE_POSTGRESQL:
            log.info("Creating PostgreSQL adapter")
            # Uncomment when PostgreSQL adapter is implemented
            # from .postgresql_adapter import PostgreSQLAdapter
            # db_config = settings.get_db_config()
            # return PostgreSQLAdapter(
            #     host=db_config["host"],
            #     port=db_config["port"],
            #     db=db_config["db"],
            #     user=db_config["user"],
            #     password=db_config["password"],
            # )
            raise NotImplementedError("PostgreSQL adapter not yet implemented")
        
        else:
            raise ValueError(
                f"Unsupported database type: {db_type}. "
                f"Supported types: {[DB_TYPE_MONGODB, DB_TYPE_POSTGRESQL]}"
            )

    @staticmethod
    def get_adapter() -> DatabaseAdapter:
        """
        Get or create a database adapter (singleton pattern).
        
        Returns:
            DatabaseAdapter: Database adapter instance.
        """
        if DatabaseFactory._adapter is None:
            DatabaseFactory._adapter = DatabaseFactory.create_adapter()
        return DatabaseFactory._adapter

    @staticmethod
    def reset_adapter() -> None:
        """Reset the adapter instance (useful for testing)."""
        DatabaseFactory._adapter = None
