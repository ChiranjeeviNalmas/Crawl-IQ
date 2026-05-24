from playwright.sync_api import Page, TimeoutError as PWTimeout
from .logger import get_logger

log = get_logger("navigator")


def goto(page: Page, url: str, timeout: int = 60000) -> None:
    log.info("Navigating → %s", url)
    page.goto(url, timeout=timeout)
    _wait_for_content(page)


def click_link_by_text(page: Page, text: str) -> bool:
    loc = page.locator(f'a:has-text("{text}")').first
    if loc.count() == 0:
        log.warning("Link not found on page: '%s'", text)
        return False
    log.info("Clicking link: '%s'", text)
    loc.click()
    _wait_for_content(page)
    return True


def _wait_for_content(page: Page) -> None:
    try:
        page.wait_for_load_state("networkidle", timeout=30000)
    except PWTimeout:
        log.warning("networkidle timed out — falling back to <main> selector")
        page.wait_for_selector("main", timeout=15000)
