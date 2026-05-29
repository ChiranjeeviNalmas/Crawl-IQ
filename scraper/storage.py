"""
Main storage entry point.

This is the ONLY file that should be imported from outside the storage module.
It provides a simple, clean interface for all storage operations.

Why this design?
- Single entry point for all storage operations
- Hides internal complexity
- Easy to use from other modules
- Follows the Facade pattern

Usage:
    from scraper.storage import save_page, get_page_by_url
    
    # Save data
    result = save_page(page_data, "ai_engineer")
    
    # Retrieve data
    page = get_page_by_url("https://example.com")
"""

from typing import Any, Dict, Optional
from .storage.storage_service import StorageService
from .logger import get_logger

log = get_logger("storage")

# Global storage service instance
_storage_service: Optional[StorageService] = None


def _get_storage_service() -> StorageService:
    """
    Get or create the global storage service instance.
    
    Returns:
        StorageService: The storage service instance.
    """
    global _storage_service
    if _storage_service is None:
        _storage_service = StorageService()
    return _storage_service


def save_page(page_data: Dict[str, Any], filename: str) -> Dict[str, Any]:
    """
    Save page data to configured storage backends (JSON and/or database).
    
    This is the main entry point for saving data. It handles:
    - Saving to JSON file (if enabled in settings)
    - Saving to database (if enabled in settings)
    
    Args:
        page_data: Dictionary containing page data to save.
        filename: Base filename for JSON storage (without extension).
    
    Returns:
        Dict: Result containing:
            - json_path: Path to saved JSON file (or None)
            - db_id: ID of saved database record (or None)
            - success: Whether at least one backend succeeded
    
    Raises:
        RuntimeError: If all storage backends fail.
    
    Example:
        >>> page_data = {
        ...     "url": "https://example.com",
        ...     "title": "Example",
        ...     "links": [...]
        ... }
        >>> result = save_page(page_data, "example")
        >>> print(result["json_path"])
        output/example_20260528_120000.json
        >>> print(result["db_id"])
        507f1f77bcf86cd799439011
    """
    service = _get_storage_service()
    return service.save_page(page_data, filename)


def get_page_by_url(url: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a page from database by URL.
    
    Args:
        url: Page URL to search for.
    
    Returns:
        Optional[Dict]: Page data if found, None otherwise.
    
    Example:
        >>> page = get_page_by_url("https://example.com")
        >>> if page:
        ...     print(page["title"])
    """
    service = _get_storage_service()
    return service.get_page_by_url(url)


def get_all_pages() -> list:
    """
    Retrieve all pages from database.
    
    Returns:
        list: List of all pages.
    
    Example:
        >>> pages = get_all_pages()
        >>> print(f"Total pages: {len(pages)}")
    """
    service = _get_storage_service()
    return service.get_all_pages()


def health_check() -> Dict[str, Any]:
    """
    Check health of all storage backends.
    
    Returns:
        Dict: Health status containing:
            - json_storage: Whether JSON storage is enabled
            - database: Whether database storage is enabled
            - database_connected: Whether database is connected
    
    Example:
        >>> health = health_check()
        >>> if health["database_connected"]:
        ...     print("Database is healthy")
    """
    service = _get_storage_service()
    return service.health_check()


def disconnect() -> None:
    """
    Disconnect from database and cleanup resources.
    
    Should be called when the application is shutting down.
    
    Example:
        >>> try:
        ...     # Do work
        ... finally:
        ...     disconnect()
    """
    service = _get_storage_service()
    service.disconnect()


