"""HTTP layer: session with retry/backoff, robots.txt check, polite delays.

Techniques (current production practice):
- urllib3 Retry on 429/500/502/503/504 with exponential backoff, mounted
  via HTTPAdapter on a shared requests.Session (connection reuse).
- robots.txt is checked once per host before the first fetch.
- A fixed polite delay between requests; failures are logged, never silent.
"""
from __future__ import annotations

import logging
import time
import urllib.robotparser
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import ScraperConfig

log = logging.getLogger("scraper.fetcher")


def build_session(cfg: ScraperConfig) -> requests.Session:
    retry = Retry(
        total=cfg.max_retries,
        backoff_factor=cfg.backoff_factor,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET"]),
        raise_on_status=False,
    )
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"User-Agent": cfg.user_agent})
    return session


class RobotsBlocked(RuntimeError):
    """Raised when robots.txt disallows the target path."""


class Fetcher:
    def __init__(self, cfg: ScraperConfig) -> None:
        self.cfg = cfg
        self.session = build_session(cfg)
        self._robots: dict[str, urllib.robotparser.RobotFileParser] = {}
        self._last_request_at = 0.0

    def _allowed(self, url: str) -> bool:
        if not self.cfg.respect_robots:
            return True
        host = urlparse(url).netloc
        if host not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(f"{urlparse(url).scheme}://{host}/robots.txt")
            try:
                rp.read()
            except Exception as exc:  # unreadable robots.txt -> allow, but log
                log.warning("robots.txt unreadable for %s: %s", host, exc)
            self._robots[host] = rp
        return self._robots[host].can_fetch(self.cfg.user_agent, url)

    def fetch(self, url: str) -> str:
        """GET a page and return its HTML. Raises on HTTP/network errors."""
        if not self._allowed(url):
            raise RobotsBlocked(f"robots.txt disallows {url}")
        wait = self.cfg.delay_seconds - (time.monotonic() - self._last_request_at)
        if wait > 0:
            time.sleep(wait)
        log.info("GET %s", url)
        resp = self.session.get(url, timeout=self.cfg.timeout_seconds)
        self._last_request_at = time.monotonic()
        resp.raise_for_status()
        return resp.text
