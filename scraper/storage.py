"""Storage layer: dedupe + CSV export + run statistics."""
from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass

from .parser import Book


@dataclass
class RunStats:
    pages_fetched: int = 0
    pages_failed: int = 0
    items_found: int = 0
    items_new: int = 0
    items_duplicate: int = 0

    @property
    def success_rate(self) -> float:
        total = self.pages_fetched + self.pages_failed
        return round(100.0 * self.pages_fetched / total, 1) if total else 0.0

    def to_json(self, path: str) -> None:
        data = asdict(self)
        data["success_rate_percent"] = self.success_rate
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)


class BookStore:
    """In-memory dedupe by detail URL, then one clean CSV write."""

    def __init__(self) -> None:
        self._by_url: dict[str, Book] = {}

    def add_many(self, books: list[Book], stats: RunStats) -> None:
        for book in books:
            stats.items_found += 1
            if book.detail_url in self._by_url:
                stats.items_duplicate += 1
            else:
                self._by_url[book.detail_url] = book
                stats.items_new += 1

    def write_csv(self, path: str) -> int:
        rows = sorted(self._by_url.values(), key=lambda b: b.title.lower())
        with open(path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["title", "price_gbp", "rating", "in_stock", "detail_url"])
            for b in rows:
                writer.writerow([b.title, f"{b.price_gbp:.2f}", b.rating,
                                 "yes" if b.in_stock else "no", b.detail_url])
        return len(rows)
