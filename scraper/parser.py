"""Parsing layer: HTML -> typed Book records. Pure functions, unit-testable."""
from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from urllib.parse import urljoin

from bs4 import BeautifulSoup

RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
_PRICE_RE = re.compile(r"£\s*([0-9]+(?:\.[0-9]{1,2})?)")


@dataclass(frozen=True)
class Book:
    title: str
    price_gbp: Decimal
    rating: int            # 1-5, 0 if unknown
    in_stock: bool
    detail_url: str        # absolute URL; also the dedupe key


def _parse_price(text: str) -> Decimal:
    m = _PRICE_RE.search(text or "")
    if not m:
        return Decimal("0")
    try:
        return Decimal(m.group(1))
    except InvalidOperation:
        return Decimal("0")


def parse_book_cards(html: str, page_url: str) -> list[Book]:
    soup = BeautifulSoup(html, "lxml") if _has_lxml() else BeautifulSoup(html, "html.parser")
    books: list[Book] = []
    for card in soup.select("article.product_pod"):
        title_el = card.select_one("h3 a")
        if title_el is None:
            continue
        rating_el = card.select_one("p.star-rating")
        rating = 0
        if rating_el:
            for cls in rating_el.get("class", []):
                if cls in RATING_WORDS:
                    rating = RATING_WORDS[cls]
        price_el = card.select_one("p.price_color")
        stock_el = card.select_one("p.availability")
        books.append(
            Book(
                title=title_el.get("title") or title_el.get_text(strip=True),
                price_gbp=_parse_price(price_el.get_text() if price_el else ""),
                rating=rating,
                in_stock=bool(stock_el and "In stock" in stock_el.get_text()),
                detail_url=urljoin(page_url, title_el.get("href", "")),
            )
        )
    return books


def parse_next_page(html: str, page_url: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    nxt = soup.select_one("ul.pager li.next a")
    if nxt and nxt.get("href"):
        return urljoin(page_url, nxt["href"])
    return None


def _has_lxml() -> bool:
    try:
        import lxml  # noqa: F401
        return True
    except ImportError:
        return False
