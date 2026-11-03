#!/usr/bin/env python3
"""Entry point: scrape books.toscrape.com catalogue pages into a clean CSV.

Usage:
    python main.py --pages 3 --output books.csv
"""
from __future__ import annotations

import argparse
import logging
import sys

from scraper.config import ScraperConfig
from scraper.fetcher import Fetcher
from scraper.parser import parse_book_cards, parse_next_page
from scraper.storage import BookStore, RunStats


def run(cfg: ScraperConfig) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    log = logging.getLogger("scraper.main")
    fetcher = Fetcher(cfg)
    store = BookStore()
    stats = RunStats()

    url: str | None = cfg.base_url
    for _ in range(cfg.max_pages):
        if url is None:
            break
        try:
            html = fetcher.fetch(url)
        except Exception as exc:
            stats.pages_failed += 1
            log.error("FAILED %s -> %s", url, exc)
            break
        stats.pages_fetched += 1
        books = parse_book_cards(html, url)
        store.add_many(books, stats)
        log.info("page ok: %d books (total new=%d)", len(books), stats.items_new)
        url = parse_next_page(html, url)

    written = store.write_csv(cfg.output_csv)
    stats.to_json(cfg.stats_json)
    log.info("done: wrote %d rows to %s | success rate %.1f%%",
             written, cfg.output_csv, stats.success_rate)
    return 0 if stats.pages_fetched else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pages", type=int, default=3, help="max catalogue pages")
    ap.add_argument("--output", default="books.csv", help="output CSV path")
    ap.add_argument("--delay", type=float, default=0.5, help="delay between requests (s)")
    args = ap.parse_args()
    cfg = ScraperConfig(max_pages=args.pages, output_csv=args.output,
                        delay_seconds=args.delay)
    return run(cfg)


if __name__ == "__main__":
    sys.exit(main())
