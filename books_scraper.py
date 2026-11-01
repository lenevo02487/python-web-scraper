#!/usr/bin/env python3
"""
Books Web Scraper — demo scraper for the practice site books.toscrape.com.

Walks every catalogue page of the site and writes all books to a clean CSV:
title, price (GBP), star rating and stock availability.

Usage:
    pip install -r requirements.txt
    python3 books_scraper.py              # full catalogue  -> books.csv
    python3 books_scraper.py --pages 1    # first page only (20 books)

books.toscrape.com is a website built specifically for scraping practice,
so scraping it is allowed and encouraged.
"""

import argparse
import csv
import sys
import time

import requests
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com/"
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_book(article):
    """Pull title, price, rating and availability out of one book card."""
    title = article.h3.a["title"]
    price = article.select_one(".price_color").get_text(strip=True)
    rating_word = article.select_one(".star-rating")["class"][1]
    availability = article.select_one(".availability").get_text(strip=True)
    return {
        "title": title,
        "price_gbp": price.replace("£", ""),
        "rating": RATING_WORDS.get(rating_word, ""),
        "availability": availability,
    }


def scrape(max_pages=None):
    books = []
    page_url = BASE
    page_no = 0
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (demo scraper)"

    while page_url:
        page_no += 1
        resp = session.get(page_url, timeout=25)
        resp.raise_for_status()
        resp.encoding = "utf-8"  # the site is UTF-8; requests may guess Latin-1 and mangle the £ sign
        soup = BeautifulSoup(resp.text, "html.parser")

        for article in soup.select("article.product_pod"):
            books.append(parse_book(article))
        print(f"page {page_no}: {len(books)} books so far", file=sys.stderr)

        if max_pages and page_no >= max_pages:
            break
        next_link = soup.select_one("li.next a")
        page_url = requests.compat.urljoin(page_url, next_link["href"]) if next_link else None
        if page_url:
            time.sleep(0.3)  # be polite to the demo server

    return books


def main():
    ap = argparse.ArgumentParser(description="Scrape books.toscrape.com into a CSV.")
    ap.add_argument("--pages", type=int, default=None, help="limit catalogue pages (default: all)")
    ap.add_argument("--output", default="books.csv", help="output CSV file (default: books.csv)")
    args = ap.parse_args()

    books = scrape(max_pages=args.pages)
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price_gbp", "rating", "availability"])
        writer.writeheader()
        writer.writerows(books)

    print(f"Done: {len(books)} books written to {args.output}")


if __name__ == "__main__":
    main()
