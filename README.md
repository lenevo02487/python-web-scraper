# Python Web Scraper — books.toscrape.com Demo

A working web scraper that walks the **entire catalogue** of
[books.toscrape.com](https://books.toscrape.com/) (a site built specifically
for scraping practice) and saves every book into one clean CSV file:
**title, price, star rating and stock availability**.

This is a live, runnable demo of the web-scraping service I sell on Fiverr —
send me a sample page from your own project and I'll show you a mini demo
before you pay anything.

## What it does

- Scrapes all **50 catalogue pages — 1,000 books** — following the site's
  pagination automatically
- Extracts title, price (GBP), star rating (1–5) and availability per book
- Writes a clean, ready-to-use `books.csv`
- Polite by default: custom User-Agent and a small delay between pages

## Files

| File | What it is |
|---|---|
| `books_scraper.py` | Full scraper (requests + BeautifulSoup) → CSV |
| `quick_demo.py` | Tiny standard-library-only version (no installs) that prints the first 6 books |
| `requirements.txt` | Dependencies for the full scraper |
| `books.csv` | Real output from a full run (1,000 rows) |

## How to run

```bash
pip install -r requirements.txt
python3 books_scraper.py              # full catalogue -> books.csv
python3 books_scraper.py --pages 1    # first page only (20 books)
python3 quick_demo.py                 # no installs needed, prints 6 rows
```

## Sample output

`books.csv` (first rows of a real run):

```csv
title,price_gbp,rating,availability
A Light in the Attic,51.77,3,In stock
Tipping the Velvet,53.74,1,In stock
Soumission,50.10,1,In stock
Sharp Objects,47.82,4,In stock
Sapiens: A Brief History of Humankind,54.23,5,In stock
```

`quick_demo.py` output:

```text
A Light in the Attic | £51.77 | Three stars
Tipping the Velvet | £53.74 | One stars
Soumission | £50.10 | One stars
Sharp Objects | £47.82 | Four stars
Sapiens: A Brief History of Humankind | £54.23 | Five stars
The Requiem Red | £22.65 | One stars
```

## Tech used

Python 3 · requests · BeautifulSoup 4 · csv (standard library)

## Hire me

Need data pulled from a website into CSV/Excel, or a repetitive data task
automated? **Demo first — on YOUR sample — before you pay anything.**

- Fiverr gig (from $15): https://www.fiverr.com/lenevo509/build-a-python-web-scraper-or-automation-script-for-you
- LinkedIn: https://www.linkedin.com/in/abhishek-phukan-a220b9448/

*Built by Abhishek Phukan — Python Automation Developer.*
