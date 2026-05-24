from .browser import launch_browser, new_page
from .navigator import goto, click_link_by_text
from .extractor import extract
from .storage import save
from .config import ScraperConfig
from .logger import get_logger

log = get_logger("runner")


def run(config: ScraperConfig) -> str:
    log.info("=== Scrape start: %s ===", config.name)
    with launch_browser(headless=config.headless) as browser:
        page = new_page(browser)
        goto(page, config.start_url, config.nav_timeout)

        if config.link_text:
            found = click_link_by_text(page, config.link_text)
            if not found:
                if not config.direct_url:
                    raise RuntimeError(f"Link '{config.link_text}' not found and no direct_url configured")
                log.warning("Falling back to direct_url: %s", config.direct_url)
                goto(page, config.direct_url, config.nav_timeout)
        elif config.direct_url:
            goto(page, config.direct_url, config.nav_timeout)

        data = extract(page, config.base_url)

    path = save(data, config.output_filename)
    log.info("=== Scrape done: %s ===", config.name)
    return path
