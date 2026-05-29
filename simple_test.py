print("Starting test...")
print("1. Importing logger...")
from scraper.logger import get_logger
print("2. Logger imported successfully")
log = get_logger("test")
print("3. Logger created successfully")
log.info("Test message")
print("4. Done!")
