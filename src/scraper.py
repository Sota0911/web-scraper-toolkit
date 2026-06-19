"""HTTP fetching with rate limiting and retry logic."""
import time
from typing import Optional

import requests
from rich.console import Console

console = Console()

BASE_URL = "https://books.toscrape.com"
DEFAULT_DELAY = 1.0  # seconds between requests
MAX_RETRIES = 3


def fetch(url: str, session: requests.Session, delay: float = DEFAULT_DELAY) -> Optional[str]:
    time.sleep(delay)
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            if attempt == MAX_RETRIES:
                console.print(f"[red]Failed after {MAX_RETRIES} attempts: {url}[/red]")
                return None
            wait = attempt * 2
            console.print(f"[yellow]Retry {attempt}/{MAX_RETRIES} in {wait}s — {e}[/yellow]")
            time.sleep(wait)
    return None


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (educational web scraper - books.toscrape.com)"
    })
    return session


def get_category_urls(session: requests.Session) -> dict[str, str]:
    """Return {category_name: url} from the sidebar."""
    html = fetch(BASE_URL, session, delay=0)
    if not html:
        return {}

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    categories = {}
    for link in soup.select("ul.nav-list ul a"):
        name = link.get_text(strip=True)
        href = link["href"]
        categories[name] = f"{BASE_URL}/{href}"
    return categories
