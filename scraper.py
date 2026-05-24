from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import json
import os
import re

OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "ai_engineer.json")


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def text_or_none(locator):
    try:
        return locator.inner_text().strip()
    except Exception:
        return None


def main():
    ensure_output_dir()
    result = {"title": None, "h1": None, "url": None, "text": None, "links": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://roadmap.sh", timeout=60000)

        # Try to find link to AI Engineer
        ai_locator = page.locator("a:has-text(\"AI Engineer\")").first
        try:
            if ai_locator.count() > 0:
                ai_locator.click()
            else:
                # fallback to common candidate URL
                page.goto("https://roadmap.sh/ai-engineer", timeout=60000)
        except Exception:
            try:
                page.goto("https://roadmap.sh/ai-engineer", timeout=60000)
            except Exception as e:
                print("Failed to navigate to AI Engineer page:", e)
                browser.close()
                return

        try:
            page.wait_for_load_state("networkidle", timeout=30000)
        except PlaywrightTimeoutError:
            print("Warning: networkidle timed out, waiting for page content instead...")
            page.wait_for_selector("main", timeout=15000)

        result["url"] = page.url
        try:
            result["title"] = page.title()
        except Exception:
            result["title"] = None

        # h1
        h1 = page.query_selector("h1")
        if h1:
            try:
                result["h1"] = h1.inner_text().strip()
            except Exception:
                result["h1"] = None

        # main text or whole body
        main = page.query_selector("main")
        try:
            if main:
                result["text"] = main.inner_text().strip()
            else:
                result["text"] = page.inner_text("body").strip()
        except Exception:
            result["text"] = None

        # collect links within main (or body)
        anchors = page.query_selector_all("main a")
        if not anchors:
            anchors = page.query_selector_all("body a")

        links = []
        for a in anchors:
            try:
                text = a.inner_text().strip()
            except Exception:
                text = None
            try:
                href = a.get_attribute("href")
            except Exception:
                href = None
            if href:
                # normalize relative urls
                if href.startswith("/"):
                    href = "https://roadmap.sh" + href
                links.append({"text": text, "href": href})

        result["links"] = links

        browser.close()

    # save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
