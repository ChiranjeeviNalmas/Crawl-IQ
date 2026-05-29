"""
Storage configuration and settings management.

This module loads and validates configuration from environment variables.
It provides a single source of truth for all storage-related settings.

Why separate from storage.py?
- Keeps configuration logic isolated
- Easy to test configuration independently
- Can be reused across different modules
- Follows Single Responsibility Principle
"""

import os
from typing import Optional
from dotenv import load_dotenv
from .constants import (
    DB_TYPE_MONGODB,
    SUPPORTED_DB_TYPES,
    DEFAULT_DB_TYPE,
    DEFAULT_OUTPUT_DIR,
)

# Load environment variables from .env file
load_dotenv()


class StorageSettings:
    """
    Centralized storage configuration.
    
    This class loads and validates all storage settings from environment variables.
    It ensures type safety and provides defaults for missing values.
    """

    def __init__(self):
        """Initialize storage settings from environment variables."""
        self._load_settings()
        self._validate_settings()

    def _load_settings(self) -> None:
        """Load all settings from environment variables."""
        # Database Configuration
        self.db_type: str = os.getenv("DB_TYPE", DEFAULT_DB_TYPE).lower()
        
        # MongoDB Settings
        self.mongodb_uri: str = os.getenv(
            "MONGODB_URI", "mongodb://localhost:27017"
        )
        self.mongodb_db: str = os.getenv("MONGODB_DB", "webscraper")
        self.mongodb_collection: str = os.getenv("MONGODB_COLLECTION", "pages")
        
        # PostgreSQL Settings (for future use)
        self.postgres_host: str = os.getenv("POSTGRES_HOST", "localhost")
        self.postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
        self.postgres_db: str = os.getenv("POSTGRES_DB", "webscraper")
        self.postgres_user: str = os.getenv("POSTGRES_USER", "postgres")
        self.postgres_password: str = os.getenv("POSTGRES_PASSWORD", "")
        
        # Storage Configuration
        self.output_dir: str = os.getenv("STORAGE_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
        self.save_json: bool = os.getenv("STORAGE_SAVE_JSON", "true").lower() == "true"
        self.save_db: bool = os.getenv("STORAGE_SAVE_DB", "true").lower() == "true"
        
        # Logging
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def _validate_settings(self) -> None:
        """Validate that all settings are correct."""
        if self.db_type not in SUPPORTED_DB_TYPES:
            raise ValueError(
                f"Invalid DB_TYPE: {self.db_type}. "
                f"Supported types: {SUPPORTED_DB_TYPES}"
            )
        
        if not self.output_dir:
            raise ValueError("STORAGE_OUTPUT_DIR cannot be empty")
        
        if self.db_type == DB_TYPE_MONGODB and not self.mongodb_uri:
            raise ValueError("MONGODB_URI is required when DB_TYPE=mongodb")

    def get_db_config(self) -> dict:
        """
        Get database-specific configuration.
        
        Returns:
            dict: Configuration dictionary for the selected database type.
        """
        if self.db_type == DB_TYPE_MONGODB:
            return {
                "uri": self.mongodb_uri,
                "db": self.mongodb_db,
                "collection": self.mongodb_collection,
            }
        elif self.db_type == "postgresql":
            return {
                "host": self.postgres_host,
                "port": self.postgres_port,
                "db": self.postgres_db,
                "user": self.postgres_user,
                "password": self.postgres_password,
            }
        else:
            raise ValueError(f"Unknown database type: {self.db_type}")

    def __repr__(self) -> str:
        """String representation of settings."""
        return (
            f"StorageSettings(db_type={self.db_type}, "
            f"output_dir={self.output_dir}, "
            f"save_json={self.save_json}, "
            f"save_db={self.save_db})"
        )


# Global settings instance
settings = StorageSettings()
