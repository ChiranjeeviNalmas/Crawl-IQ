"""
MongoDB database adapter implementation.

This module implements the DatabaseAdapter interface for MongoDB.
It handles all MongoDB-specific operations while maintaining the
abstract interface, allowing easy switching to other databases.

Why separate from base?
- Keeps MongoDB-specific code isolated
- Easy to add PostgreSQL adapter without touching this file
- Can be tested independently
- Follows Open/Closed Principle (open for extension, closed for modification)
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from .database_base import DatabaseAdapter
from ..logger import get_logger

log = get_logger("mongodb_adapter")


class MongoDBAdapter(DatabaseAdapter):
    """
    MongoDB implementation of DatabaseAdapter.
    
    This adapter handles all MongoDB operations and provides a clean
    interface that matches the abstract base class.
    """

    def __init__(self, uri: str, db_name: str, collection_name: str):
        """
        Initialize MongoDB adapter.
        
        Args:
            uri: MongoDB connection string (e.g., mongodb://localhost:27017)
            db_name: Database name
            collection_name: Collection name
        """
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client: Optional[MongoClient] = None
        self.db = None
        self.collection = None

    def connect(self) -> None:
        """
        Establish connection to MongoDB.
        
        Raises:
            ConnectionError: If connection fails.
        """
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Verify connection
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            log.info(
                "Connected to MongoDB: %s (db=%s, collection=%s)",
                self.uri,
                self.db_name,
                self.collection_name,
            )
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            log.error("Failed to connect to MongoDB: %s", e)
            raise ConnectionError(f"MongoDB connection failed: {e}") from e

    def disconnect(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            log.info("Disconnected from MongoDB")

    def is_connected(self) -> bool:
        """
        Check if connected to MongoDB.
        
        Returns:
            bool: True if connected, False otherwise.
        """
        return self.client is not None and self.collection is not None

    def insert_one(self, data: Dict[str, Any]) -> str:
        """
        Insert a single document into MongoDB.
        
        Args:
            data: Dictionary containing the data to insert.
        
        Returns:
            str: ID of the inserted document.
        
        Raises:
            Exception: If insertion fails.
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to MongoDB")
        
        try:
            # Add timestamp if not present
            if "scraped_at" not in data:
                data["scraped_at"] = datetime.now()
            
            result = self.collection.insert_one(data)
            log.debug("Inserted document with ID: %s", result.inserted_id)
            return str(result.inserted_id)
        except Exception as e:
            log.error("Failed to insert document: %s", e)
            raise

    def insert_many(self, data_list: List[Dict[str, Any]]) -> List[str]:
        """
        Insert multiple documents into MongoDB.
        
        Args:
            data_list: List of dictionaries to insert.
        
        Returns:
            List[str]: List of inserted document IDs.
        
        Raises:
            Exception: If insertion fails.
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to MongoDB")
        
        try:
            # Add timestamp to all documents
            for data in data_list:
                if "scraped_at" not in data:
                    data["scraped_at"] = datetime.now()
            
            result = self.collection.insert_many(data_list)
            log.debug("Inserted %d documents", len(result.inserted_ids))
            return [str(id_) for id_ in result.inserted_ids]
        except Exception as e:
            log.error("Failed to insert documents: %s", e)
            raise

    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Find a single document in MongoDB.
        
        Args:
            query: Query dictionary to filter results.
        
        Returns:
            Optional[Dict]: Document if found, None otherwise.
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to MongoDB")
        
        try:
            result = self.collection.find_one(query)
            return result
        except Exception as e:
            log.error("Failed to find document: %s", e)
            raise

    def find_many(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find multiple documents in MongoDB.
        
        Args:
            query: Query dictionary to filter results.
        
        Returns:
            List[Dict]: List of matching documents.
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to MongoDB")
        
        try:
            results = list(self.collection.find(query))
            return results
        except Exception as e:
            log.error("Failed to find documents: %s", e)
            raise

    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """
        Update a single document in MongoDB.
        
        Args:
            query: Query to find the document.
            update: Update data.
        
        Returns:
            int: Number of documents updated.
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to MongoDB")
        
        try:
            result = self.collection.update_one(query, {"$set": update})
            log.debug("Updated %d document(s)", result.modified_count)
            return result.modified_count
        except Exception as e:
            log.error("Failed to update document: %s", e)
            raise

    def delete_one(self, query: Dict[str, Any]) -> int:
        """
        Delete a single document from MongoDB.
        
        Args:
            query: Query to find the document.
        
        Returns:
            int: Number of documents deleted.
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to MongoDB")
        
        try:
            result = self.collection.delete_one(query)
            log.debug("Deleted %d document(s)", result.deleted_count)
            return result.deleted_count
        except Exception as e:
            log.error("Failed to delete document: %s", e)
            raise

    def count(self, query: Optional[Dict[str, Any]] = None) -> int:
        """
        Count documents in MongoDB.
        
        Args:
            query: Optional query to filter results.
        
        Returns:
            int: Number of documents matching the query.
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to MongoDB")
        
        try:
            if query is None:
                query = {}
            count = self.collection.count_documents(query)
            return count
        except Exception as e:
            log.error("Failed to count documents: %s", e)
            raise

    def health_check(self) -> bool:
        """
        Check MongoDB health/connectivity.
        
        Returns:
            bool: True if MongoDB is healthy, False otherwise.
        """
        try:
            if self.client:
                self.client.admin.command("ping")
                return True
        except Exception as e:
            log.warning("MongoDB health check failed: %s", e)
        return False
