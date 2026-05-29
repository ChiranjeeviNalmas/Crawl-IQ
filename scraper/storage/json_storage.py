"""
JSON file storage utility.

This module handles saving data to JSON files.
It's separate from database storage to keep concerns isolated.

Why separate?
- JSON storage is independent of database storage
- Can be disabled/enabled via configuration
- Easier to test and maintain
- Follows Single Responsibility Principle
"""

import json
import os
from datetime import datetime
from typing import Any, Dict
from .settings import settings
from .constants import TIMESTAMP_FORMAT, JSON_EXTENSION
from ..logger import get_logger

log = get_logger("json_storage")


class JSONStorage:
    """Handles JSON file storage operations."""

    @staticmethod
    def save(data: Dict[str, Any], filename: str) -> str:
        """
        Save data to a JSON file.
        
        Args:
            data: Dictionary to save.
            filename: Base filename (without extension or timestamp).
        
        Returns:
            str: Full path to the saved file.
        
        Raises:
            Exception: If save fails.
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(settings.output_dir, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
            full_filename = f"{filename}_{timestamp}{JSON_EXTENSION}"
            filepath = os.path.join(settings.output_dir, full_filename)
            
            # Save to JSON
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            log.info("Saved JSON file: %s", filepath)
            return filepath
        except Exception as e:
            log.error("Failed to save JSON file: %s", e)
            raise

    @staticmethod
    def load(filepath: str) -> Dict[str, Any]:
        """
        Load data from a JSON file.
        
        Args:
            filepath: Path to the JSON file.
        
        Returns:
            Dict: Loaded data.
        
        Raises:
            Exception: If load fails.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            log.info("Loaded JSON file: %s", filepath)
            return data
        except Exception as e:
            log.error("Failed to load JSON file: %s", e)
            raise
