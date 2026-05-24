import sys
from scraper.runner import run
from scraper.logger import get_logger
from scrapers.roadmap_ai_engineer import AI_ENGINEER
from scrapers.roadmap_system_design import SYSTEM_DESIGN

log = get_logger("main")

SCRAPERS = {
    "ai-engineer": AI_ENGINEER,
    "system-design": SYSTEM_DESIGN,
}


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "ai-engineer"
    if target not in SCRAPERS:
        log.error("Unknown scraper '%s'. Available: %s", target, list(SCRAPERS.keys()))
        sys.exit(1)
    try:
        output = run(SCRAPERS[target])
        print(f"\nDone! Output saved to: {output}")
    except Exception as e:
        log.exception("Scrape failed with unhandled error: %s", e)
        sys.exit(1)
