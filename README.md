# Python Web Scraper — Production-Grade Demo

A modular Python scraper that pulls the full book catalogue from
[books.toscrape.com](https://books.toscrape.com) (a site built for scraping
practice) into a clean CSV — built the way a client scraper should be:
retries, politeness, dedupe, typed records and a run report, not a
20-line script that breaks on the first hiccup.

## What it does

- Walks catalogue pages via the "next" pager (configurable page cap)
- Extracts title, price (£), star rating, stock status and detail URL
  into typed `Book` records
- Dedupes by detail URL, writes one sorted CSV, and saves run statistics
  (pages fetched/failed, duplicates skipped, success rate) as JSON

## How it's built

| Layer | File | Responsibility |
|---|---|---|
| Config | `scraper/config.py` | One frozen dataclass: delays, timeouts, retry policy, user agent |
| Fetch | `scraper/fetcher.py` | `requests` session + urllib3 `Retry` (429/5xx, exponential backoff), robots.txt check per host, polite delay between requests |
| Parse | `scraper/parser.py` | Pure functions HTML → `Book` dataclasses (CSS selectors, `lxml` when available) |
| Store | `scraper/storage.py` | Dedupe + CSV export + `RunStats` success-rate reporting |
| Entry | `main.py` | CLI wiring + structured logging |

## Run it

```bash
pip install -r requirements.txt
python main.py --pages 3 --output books.csv
python -m unittest discover -s tests
```

## Sample output (real run, 2 pages)

```
2026-11-03 INFO scraper.main: page ok: 20 books (total new=40)
2026-11-03 INFO scraper.main: done: wrote 40 rows to sample_output.csv | success rate 100.0%
```

```csv
title,price_gbp,rating,in_stock,detail_url
A Light in the Attic,51.77,3,yes,https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
```

`sample_output.csv` and `run_stats.json` in this repo are from that actual run.

## Notes

- Respects `robots.txt` and rate-limits itself by default; raise the page
  cap deliberately, not accidentally.
- Parser tests run offline against a fixed HTML fixture
  (`tests/test_parser.py`, 4 tests).

## Want this for your site?

This demo is free to judge. Send me your target website and I'll first
build a small working demo scrape on *your* sample — you see the output
before paying anything. — Abhishek
