import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from parser import parse_books, get_next_page_url

SAMPLE_HTML = """
<html><body>
<ol class="row">
  <article class="product_pod">
    <h3><a href="catalogue/a-light-in-the-attic_1000/index.html"
           title="A Light in the Attic">A Light in the Attic</a></h3>
    <p class="price_color">£51.77</p>
    <p class="star-rating Three"></p>
    <p class="availability">In stock</p>
  </article>
  <article class="product_pod">
    <h3><a href="catalogue/tipping-the-velvet_999/index.html"
           title="Tipping the Velvet">Tipping the Velvet</a></h3>
    <p class="price_color">£53.74</p>
    <p class="star-rating One"></p>
    <p class="availability">In stock</p>
  </article>
</ol>
<li class="next"><a href="catalogue/page-2.html">next</a></li>
</body></html>
"""

PAGE_URL = "https://books.toscrape.com/"


def test_parse_books_count():
    books = parse_books(SAMPLE_HTML, PAGE_URL)
    assert len(books) == 2


def test_parse_books_fields():
    book = parse_books(SAMPLE_HTML, PAGE_URL)[0]
    assert book["title"] == "A Light in the Attic"
    assert book["price_gbp"] == 51.77
    assert book["rating"] == 3
    assert book["availability"] == "In stock"


def test_get_next_page_url():
    next_url = get_next_page_url(SAMPLE_HTML, PAGE_URL)
    assert next_url is not None
    assert "page-2" in next_url


def test_no_next_page():
    html_no_next = SAMPLE_HTML.replace('<li class="next"><a href="catalogue/page-2.html">next</a></li>', "")
    assert get_next_page_url(html_no_next, PAGE_URL) is None
