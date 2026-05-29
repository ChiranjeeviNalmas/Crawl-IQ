"""
Storage service - orchestrates all storage operations.

This module coordinates between JSON storage and database storage.
It's the main entry point for all storage operations.

Why use a service?
- Orchestrates multiple storage backends
- Provides a single interface for storage operations
- Handles configuration-based storage selection
- Follows the Facade pattern
"""

from typing import Any, Dict, Optional
from .settings import settings
from .json_storage import JSONStorage
from .page_repository import PageRepository
from .database_factory import DatabaseFactory
from ..logger import get_logger

log = get_logger("storage_service")


class StorageService:
    """
    Main storage service that coordinates all storage operations.
    
    This service handles:
    - Saving to JSON files (if enabled)
    - Saving to database (if enabled)
    - Retrieving data from database
    - Health checks
    """

    def __init__(self):
        """Initialize storage service."""
        self.json_storage = JSONStorage()
        self.repository = PageRepository()
        self.settings = settings

    def save_page(self, page_data: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """
        Save page data to configured storage backends.
        
        Args:
            page_data: Page data to save.
            filename: Base filename for JSON storage.
        
        Returns:
            Dict: Result containing paths/IDs of saved data.
        
        Raises:
            Exception: If all storage backends fail.
        """
        result = {
            "json_path": None,
            "db_id": None,
            "success": False,
        }
        
        errors = []
        
        # Save to JSON if enabled
        if self.settings.save_json:
            try:
                json_path = self.json_storage.save(page_data, filename)
                result["json_path"] = json_path
                log.info("Saved to JSON: %s", json_path)
            except Exception as e:
                error_msg = f"JSON save failed: {e}"
                log.error(error_msg)
                errors.append(error_msg)
        
        # Save to database if enabled
        if self.settings.save_db:
            try:
                db_id = self.repository.save_page(page_data)
                result["db_id"] = db_id
                log.info("Saved to database: %s", db_id)
            except Exception as e:
                error_msg = f"Database save failed: {e}"
                log.error(error_msg)
                errors.append(error_msg)
        
        # Mark as success if at least one backend succeeded
        result["success"] = result["json_path"] is not None or result["db_id"] is not None
        
        if not result["success"]:
            error_summary = "; ".join(errors)
            raise RuntimeError(f"All storage backends failed: {error_summary}")
        
        return result

    def get_page_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a page by URL from database.
        
        Args:
            url: Page URL.
        
        Returns:
            Optional[Dict]: Page data if found, None otherwise.
        """
        try:
            return self.repository.get_page_by_url(url)
        except Exception as e:
            log.error("Failed to retrieve page: %s", e)
            raise

    def get_all_pages(self) -> list:
        """
        Retrieve all pages from database.
        
        Returns:
            list: All pages.
        """
        try:
            return self.repository.get_all_pages()
        except Exception as e:
            log.error("Failed to retrieve pages: %s", e)
            raise

    def health_check(self) -> Dict[str, Any]:
        """
        Check health of all storage backends.
        
        Returns:
            Dict: Health status of each backend.
        """
        health = {
            "json_storage": self.settings.save_json,
            "database": self.settings.save_db,
            "database_connected": False,
        }
        
        if self.settings.save_db:
            try:
                health["database_connected"] = self.repository.health_check()
            except Exception as e:
                log.warning("Database health check failed: %s", e)
                health["database_connected"] = False
        
        return health

    def disconnect(self) -> None:
        """Disconnect from database."""
        try:
            self.repository.adapter.disconnect()
            log.info("Storage service disconnected")
        except Exception as e:
            log.warning("Error during disconnect: %s", e)
