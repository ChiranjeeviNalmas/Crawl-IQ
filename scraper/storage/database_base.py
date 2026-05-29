"""
Abstract base class for database implementations.

This module defines the interface that all database adapters must implement.
This allows us to switch databases without changing the storage layer.

Why use an abstract base class?
- Enforces consistent interface across all database implementations
- Makes it easy to add new database types (PostgreSQL, MySQL, etc.)
- Enables dependency injection and testing
- Follows the Strategy pattern for database abstraction
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime


class DatabaseAdapter(ABC):
    """
    Abstract base class for database adapters.
    
    All database implementations (MongoDB, PostgreSQL, etc.) must inherit
    from this class and implement all abstract methods.
    """

    @abstractmethod
    def connect(self) -> None:
        """
        Establish connection to the database.
        
        Raises:
            ConnectionError: If connection fails.
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """
        Check if database is connected.
        
        Returns:
            bool: True if connected, False otherwise.
        """
        pass

    @abstractmethod
    def insert_one(self, data: Dict[str, Any]) -> str:
        """
        Insert a single document/record.
        
        Args:
            data: Dictionary containing the data to insert.
        
        Returns:
            str: ID of the inserted document.
        
        Raises:
            Exception: If insertion fails.
        """
        pass

    @abstractmethod
    def insert_many(self, data_list: List[Dict[str, Any]]) -> List[str]:
        """
        Insert multiple documents/records.
        
        Args:
            data_list: List of dictionaries to insert.
        
        Returns:
            List[str]: List of inserted document IDs.
        
        Raises:
            Exception: If insertion fails.
        """
        pass

    @abstractmethod
    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find a single document/record.
        
        Args:
            query: Query dictionary to filter results.
        
        Returns:
            Optional[Dict]: Document if found, None otherwise.
        """
        pass

    @abstractmethod
    def find_many(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find multiple documents/records.
        
        Args:
            query: Query dictionary to filter results.
        
        Returns:
            List[Dict]: List of matching documents.
        """
        pass

    @abstractmethod
    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """
        Update a single document/record.
        
        Args:
            query: Query to find the document.
            update: Update data.
        
        Returns:
            int: Number of documents updated.
        """
        pass

    @abstractmethod
    def delete_one(self, query: Dict[str, Any]) -> int:
        """
        Delete a single document/record.
        
        Args:
            query: Query to find the document.
        
        Returns:
            int: Number of documents deleted.
        """
        pass

    @abstractmethod
    def count(self, query: Optional[Dict[str, Any]] = None) -> int:
        """
        Count documents/records.
        
        Args:
            query: Optional query to filter results.
        
        Returns:
            int: Number of documents matching the query.
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Check database health/connectivity.
        
        Returns:
            bool: True if database is healthy, False otherwise.
        """
        pass
