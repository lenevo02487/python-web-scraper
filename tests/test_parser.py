import sys
import unittest
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scraper.parser import parse_book_cards, parse_next_page

FIXTURE = """
<html><body>
<article class="product_pod">
  <h3><a href="catalogue/a-light-in-the-attic_1000/index.html"
         title="A Light in the Attic">A Light in the ...</a></h3>
  <p class="star-rating Three"></p>
  <p class="price_color">£51.77</p>
  <p class="instock availability"> In stock </p>
</article>
<article class="product_pod">
  <h3><a href="catalogue/tipping-the-velvet_999/index.html"
         title="Tipping the Velvet">Tipping the Velvet</a></h3>
  <p class="star-rating One"></p>
  <p class="price_color">£53.74</p>
  <p class="availability"> Out of stock </p>
</article>
<ul class="pager"><li class="next"><a href="catalogue/page-2.html">next</a></li></ul>
</body></html>
"""


class TestParser(unittest.TestCase):
    URL = "https://books.toscrape.com/"

    def test_two_books_parsed(self):
        books = parse_book_cards(FIXTURE, self.URL)
        self.assertEqual(len(books), 2)

    def test_fields(self):
        first = parse_book_cards(FIXTURE, self.URL)[0]
        self.assertEqual(first.title, "A Light in the Attic")
        self.assertEqual(first.price_gbp, Decimal("51.77"))
        self.assertEqual(first.rating, 3)
        self.assertTrue(first.in_stock)
        self.assertTrue(first.detail_url.endswith("_1000/index.html"))

    def test_out_of_stock(self):
        second = parse_book_cards(FIXTURE, self.URL)[1]
        self.assertFalse(second.in_stock)
        self.assertEqual(second.rating, 1)

    def test_next_page(self):
        self.assertEqual(
            parse_next_page(FIXTURE, self.URL),
            "https://books.toscrape.com/catalogue/page-2.html",
        )


if __name__ == "__main__":
    unittest.main()
