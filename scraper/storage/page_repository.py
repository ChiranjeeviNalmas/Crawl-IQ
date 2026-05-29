"""
Repository for page data operations.

This module provides a high-level interface for page data operations.
It abstracts away database-specific details and provides business logic.

Why use a repository?
- Separates data access logic from business logic
- Provides a clean interface for CRUD operations
- Makes it easy to add validation and transformations
- Follows the Repository pattern
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from .database_base import DatabaseAdapter
from .database_factory import DatabaseFactory
from .constants import FIELD_SCRAPED_AT, FIELD_URL
from ..logger import get_logger

log = get_logger("page_repository")


class PageRepository:
    """
    Repository for managing page data.
    
    This class provides business logic for page operations while
    delegating database operations to the adapter.
    """

    def __init__(self, adapter: Optional[DatabaseAdapter] = None):
        """
        Initialize page repository.
        
        Args:
            adapter: Database adapter. If None, uses factory to create one.
        """
        self.adapter = adapter or DatabaseFactory.get_adapter()

    def save_page(self, page_data: Dict[str, Any]) -> str:
        """
        Save a single page to the database.
        
        Args:
            page_data: Dictionary containing page data.
        
        Returns:
            str: ID of the saved page.
        
        Raises:
            Exception: If save fails.
        """
        try:
            # Ensure adapter is connected
            if not self.adapter.is_connected():
                self.adapter.connect()
            
            # Add timestamp if not present
            if FIELD_SCRAPED_AT not in page_data:
                page_data[FIELD_SCRAPED_AT] = datetime.now()
            
            page_id = self.adapter.insert_one(page_data)
            log.info("Saved page: %s (ID: %s)", page_data.get(FIELD_URL, "unknown"), page_id)
            return page_id
        except Exception as e:
            log.error("Failed to save page: %s", e)
            raise

    def save_pages(self, pages_data: List[Dict[str, Any]]) -> List[str]:
        """
        Save multiple pages to the database.
        
        Args:
            pages_data: List of page data dictionaries.
        
        Returns:
            List[str]: List of saved page IDs.
        
        Raises:
            Exception: If save fails.
        """
        try:
            # Ensure adapter is connected
            if not self.adapter.is_connected():
                self.adapter.connect()
            
            # Add timestamp to all pages
            for page_data in pages_data:
                if FIELD_SCRAPED_AT not in page_data:
                    page_data[FIELD_SCRAPED_AT] = datetime.now()
            
            page_ids = self.adapter.insert_many(pages_data)
            log.info("Saved %d pages", len(page_ids))
            return page_ids
        except Exception as e:
            log.error("Failed to save pages: %s", e)
            raise

    def get_page_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Get a page by URL.
        
        Args:
            url: Page URL.
        
        Returns:
            Optional[Dict]: Page data if found, None otherwise.
        """
        try:
            if not self.adapter.is_connected():
                self.adapter.connect()
            
            page = self.adapter.find_one({FIELD_URL: url})
            return page
        except Exception as e:
            log.error("Failed to get page by URL: %s", e)
            raise

    def get_all_pages(self) -> List[Dict[str, Any]]:
        """
        Get all pages from the database.
        
        Returns:
            List[Dict]: List of all pages.
        """
        try:
            if not self.adapter.is_connected():
                self.adapter.connect()
            
            pages = self.adapter.find_many({})
            return pages
        except Exception as e:
            log.error("Failed to get all pages: %s", e)
            raise

    def get_pages_by_query(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get pages matching a query.
        
        Args:
            query: Query dictionary.
        
        Returns:
            List[Dict]: List of matching pages.
        """
        try:
            if not self.adapter.is_connected():
                self.adapter.connect()
            
            pages = self.adapter.find_many(query)
            return pages
        except Exception as e:
            log.error("Failed to get pages by query: %s", e)
            raise

    def update_page(self, url: str, update_data: Dict[str, Any]) -> int:
        """
        Update a page by URL.
        
        Args:
            url: Page URL.
            update_data: Data to update.
        
        Returns:
            int: Number of pages updated.
        """
        try:
            if not self.adapter.is_connected():
                self.adapter.connect()
            
            count = self.adapter.update_one({FIELD_URL: url}, update_data)
            log.info("Updated %d page(s)", count)
            return count
        except Exception as e:
            log.error("Failed to update page: %s", e)
            raise

    def delete_page(self, url: str) -> int:
        """
        Delete a page by URL.
        
        Args:
            url: Page URL.
        
        Returns:
            int: Number of pages deleted.
        """
        try:
            if not self.adapter.is_connected():
                self.adapter.connect()
            
            count = self.adapter.delete_one({FIELD_URL: url})
            log.info("Deleted %d page(s)", count)
            return count
        except Exception as e:
            log.error("Failed to delete page: %s", e)
            raise

    def count_pages(self) -> int:
        """
        Count total pages in the database.
        
        Returns:
            int: Total number of pages.
        """
        try:
            if not self.adapter.is_connected():
                self.adapter.connect()
            
            count = self.adapter.count()
            return count
        except Exception as e:
            log.error("Failed to count pages: %s", e)
            raise

    def health_check(self) -> bool:
        """
        Check database health.
        
        Returns:
            bool: True if database is healthy, False otherwise.
        """
        return self.adapter.health_check()
