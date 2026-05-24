from dataclasses import dataclass
from typing import Optional


@dataclass
class ScraperConfig:
    name: str
    start_url: str
    base_url: str
    output_filename: str
    link_text: Optional[str] = None   # text of <a> to click from start_url
    direct_url: Optional[str] = None  # fallback if link not found
    headless: bool = False
    nav_timeout: int = 60000
