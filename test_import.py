#!/usr/bin/env python
"""Test script to debug import issues."""

print("1. Testing basic imports...")
try:
    from scraper.logger import get_logger
    print("   ✓ logger imported")
except Exception as e:
    print(f"   ✗ logger import failed: {e}")
    exit(1)

print("2. Testing constants...")
try:
    from scraper.storage.constants import DB_TYPE_MONGODB
    print("   ✓ constants imported")
except Exception as e:
    print(f"   ✗ constants import failed: {e}")
    exit(1)

print("3. Testing settings...")
try:
    from scraper.storage.settings import settings
    print(f"   ✓ settings imported: {settings}")
except Exception as e:
    print(f"   ✗ settings import failed: {e}")
    exit(1)

print("4. Testing database_base...")
try:
    from scraper.storage.database_base import DatabaseAdapter
    print("   ✓ database_base imported")
except Exception as e:
    print(f"   ✗ database_base import failed: {e}")
    exit(1)

print("5. Testing mongodb_adapter...")
try:
    from scraper.storage.mongodb_adapter import MongoDBAdapter
    print("   ✓ mongodb_adapter imported")
except Exception as e:
    print(f"   ✗ mongodb_adapter import failed: {e}")
    exit(1)

print("6. Testing database_factory...")
try:
    from scraper.storage.database_factory import DatabaseFactory
    print("   ✓ database_factory imported")
except Exception as e:
    print(f"   ✗ database_factory import failed: {e}")
    exit(1)

print("7. Testing json_storage...")
try:
    from scraper.storage.json_storage import JSONStorage
    print("   ✓ json_storage imported")
except Exception as e:
    print(f"   ✗ json_storage import failed: {e}")
    exit(1)

print("8. Testing page_repository...")
try:
    from scraper.storage.page_repository import PageRepository
    print("   ✓ page_repository imported")
except Exception as e:
    print(f"   ✗ page_repository import failed: {e}")
    exit(1)

print("9. Testing storage_service...")
try:
    from scraper.storage.storage_service import StorageService
    print("   ✓ storage_service imported")
except Exception as e:
    print(f"   ✗ storage_service import failed: {e}")
    exit(1)

print("10. Testing storage.py...")
try:
    from scraper.storage import save_page, disconnect
    print("   ✓ storage.py imported")
except Exception as e:
    print(f"   ✗ storage.py import failed: {e}")
    exit(1)

print("\n✓ All imports successful!")
