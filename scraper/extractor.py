from playwright.sync_api import Page
from .logger import get_logger

log = get_logger("extractor")


def extract(page: Page, base_url: str) -> dict:
    log.info("Extracting page data from %s", page.url)
    return {
        "url": page.url,
        "title": _safe(page.title),
        "h1": _text(page.query_selector("h1")),
        "text": _text(page.query_selector("main")) or _safe(lambda: page.inner_text("body").strip()),
        "links": _extract_links(page, base_url),
    }


def _extract_links(page: Page, base_url: str) -> list:
    scope = "main a" if page.query_selector("main") else "body a"
    links = []
    for a in page.query_selector_all(scope):
        href = _safe(lambda el=a: el.get_attribute("href"))
        if href:
            if href.startswith("/"):
                href = base_url.rstrip("/") + href
            links.append({"text": _text(a), "href": href})
    log.debug("Extracted %d links", len(links))
    return links


def _text(el) -> str | None:
    try:
        return el.inner_text().strip() if el else None
    except Exception as e:
        log.debug("Failed to read element text: %s", e)
        return None


def _safe(fn) -> str | None:
    try:
        return fn()
    except Exception as e:
        log.debug("Safe call failed: %s", e)
        return None
