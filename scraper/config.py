from dataclasses import dataclass
from typing import Optional


@dataclass
class ScraperConfig:
    """
    Scraper configuration.
    
    Database settings are now managed via environment variables in .env
    instead of being passed through config. This keeps concerns separated.
    """
    name: str
    start_url: str
    base_url: str
    output_filename: str
    link_text: Optional[str] = None   # text of <a> to click from start_url
    direct_url: Optional[str] = None  # fallback if link not found
    headless: bool = False
    nav_timeout: int = 60000


