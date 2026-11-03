"""Scraper configuration — one dataclass, sensible production defaults."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScraperConfig:
    base_url: str = "https://books.toscrape.com/"
    max_pages: int = 3                 # safety cap; raise deliberately
    delay_seconds: float = 0.5         # polite per-request delay
    timeout_seconds: float = 15.0
    max_retries: int = 4               # urllib3 retries on 429/5xx
    backoff_factor: float = 0.8        # waits ~0.8s, 1.6s, 3.2s, 6.4s
    user_agent: str = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0 Safari/537.36 "
        "python-web-scraper-demo/2.0"
    )
    respect_robots: bool = True
    output_csv: str = "books.csv"
    stats_json: str = "run_stats.json"
