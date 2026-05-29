"""
Storage constants and configuration values.

This module defines all constants used across the storage layer,
including database types, field names, and default values.
"""

# Database Types
DB_TYPE_MONGODB = "mongodb"
DB_TYPE_POSTGRESQL = "postgresql"

SUPPORTED_DB_TYPES = [DB_TYPE_MONGODB, DB_TYPE_POSTGRESQL]

# Default Values
DEFAULT_DB_TYPE = DB_TYPE_MONGODB
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_COLLECTION_NAME = "pages"

# Field Names (standardized across all databases)
FIELD_URL = "url"
FIELD_TITLE = "title"
FIELD_H1 = "h1"
FIELD_TEXT = "text"
FIELD_LINKS = "links"
FIELD_TOPICS = "topics"
FIELD_SCRAPED_AT = "scraped_at"
FIELD_ID = "_id"

# Timestamp Format
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# File Extensions
JSON_EXTENSION = ".json"
