from playwright.sync_api import Page
from .logger import get_logger

log = get_logger("extractor")


def extract(page: Page, base_url: str) -> dict:
    log.info("Extracting page data from %s", page.url)
    #simple timeout for 5s    
    page.wait_for_timeout(5000)
    log.debug("Page content loaded, starting extraction")
    return {
        "url": page.url,
        "title": _safe(page.title),
        "h1": _text(page.query_selector("h1")),
        "text": _text(page.query_selector("main")) or _safe(lambda: page.inner_text("body").strip()),
        "topics": _extract_topics(page),
    }


def close_ad_blocker(page: Page) -> None:
    """Close ad blocker popup by clicking the close button."""
    try:
        # Try to find and click the close button in the iframe
        iframe_locator = page.frame_locator("iframe").first
        close_button = iframe_locator.locator('xpath=//span[@class="close-button"]')
        
        if close_button.count() > 0:
            close_button.click()
            log.info("Closed ad blocker popup")
        else:
            log.debug("No ad blocker close button found")
    except Exception as e:
        log.debug("Failed to close ad blocker: %s", e)


def _extract_topics(page: Page) -> list:
    """Extract data from elements matching XPath //*[@data-type="topic"] by clicking and extracting."""
    topics = []
    xpath = '//*[@data-type="topic"]'
    close_button_xpath = '//*[@id="close-topic"]'
    
    try:
        topic_elements = page.locator(f"xpath={xpath}").all()
        log.info("Found %d topic elements", len(topic_elements))
        
        for idx, element in enumerate(topic_elements):
            try:
                # Click the topic element to reveal/load data
                element.click()
                log.debug("Clicked topic element %d", idx)
                
                panel = page.locator("div.flex.h-full.flex-1.flex-col").first
                panel.wait_for(state="visible", timeout=5000)
                raw = _text(panel.element_handle()) or ""
                name, description = _parse_panel(raw)
                topic_data = {"name": name, "description": description}
                try:
                    close_button = page.locator(f"xpath={close_button_xpath}")
                    if close_button.count() > 0:
                        close_button.click()
                        log.debug("Closed topic %d", idx)
                except Exception as e:
                    log.debug("Failed to close topic %d: %s", idx, e)
                topics.append(topic_data)
                
                # Try to close the topic by clicking the close button
                log.debug("Extracted topic %d: %s", idx, topic_data.get("text", "N/A"))
            except Exception as e:
                log.warning("Failed to extract topic %d: %s", idx, e)
                continue
    except Exception as e:
        log.warning("Failed to extract topics: %s", e)
    
    log.debug("Extracted %d topics total", len(topics))
    return topics


def _parse_panel(raw: str) -> tuple:
    try:
        after = raw.split("Pending\n")[1]
        name = after.split("\n")[0].strip()
        description = after.split("\n\n")[1].split("\n\n")[0].strip()
        return name, description
    except (IndexError, ValueError):
        return None, None


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
