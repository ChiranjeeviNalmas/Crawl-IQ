"""
Storage module - database-agnostic storage layer.

This module provides a clean, modular storage architecture that supports
multiple database backends while maintaining a consistent interface.

Architecture Overview:
├── storage.py (main entry point)
├── storage_service.py (orchestrator)
├── page_repository.py (business logic)
├── database_factory.py (adapter creation)
├── database_base.py (abstract interface)
├── mongodb_adapter.py (MongoDB implementation)
├── json_storage.py (JSON file storage)
├── settings.py (configuration)
└── constants.py (constants)

How it works:
1. storage.py calls StorageService
2. StorageService coordinates JSON and database storage
3. PageRepository provides business logic
4. DatabaseFactory creates the appropriate adapter
5. Adapter implements database-specific operations

To switch databases:
1. Create new adapter inheriting from DatabaseAdapter
2. Add case in DatabaseFactory.create_adapter()
3. Update .env with DB_TYPE
"""

from .storage_service import StorageService
from .page_repository import PageRepository
from .database_factory import DatabaseFactory
from .settings import settings

__all__ = [
    "StorageService",
    "PageRepository",
    "DatabaseFactory",
    "settings",
]
