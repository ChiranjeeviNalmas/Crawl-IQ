from contextlib import contextmanager
from playwright.sync_api import sync_playwright, Browser, Page
from .logger import get_logger

log = get_logger("browser")


@contextmanager
def launch_browser(headless: bool = False):
    log.info("Launching Chromium (headless=%s)", headless)
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=headless)
        try:
            yield browser
        finally:
            browser.close()
            log.info("Browser closed")


def new_page(browser: Browser) -> Page:
    page = browser.new_page()
    log.debug("New page created")
    return page
