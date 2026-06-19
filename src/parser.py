"""Parse book data from HTML pages."""
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def parse_books(html: str, page_url: str) -> list[dict]:
    soup = BeautifulSoup(html, "lxml")
    books = []

    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price_text = article.select_one("p.price_color").get_text(strip=True)
        price = float(price_text.replace("£", "").replace("Â", "").strip())
        rating_class = article.select_one("p.star-rating")["class"][1]
        rating = RATING_MAP.get(rating_class, 0)
        availability = article.select_one("p.availability").get_text(strip=True)
        relative_url = article.h3.a["href"].replace("../", "")
        book_url = urljoin(page_url, relative_url)

        books.append({
            "title": title,
            "price_gbp": price,
            "rating": rating,
            "availability": availability,
            "url": book_url,
        })

    return books


def get_next_page_url(html: str, current_url: str) -> Optional[str]:
    soup = BeautifulSoup(html, "lxml")
    next_btn = soup.select_one("li.next a")
    if not next_btn:
        return None
    return urljoin(current_url, next_btn["href"])
