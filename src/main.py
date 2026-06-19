"""CLI entry point for web-scraper-toolkit."""
from pathlib import Path
from typing import Optional

import pandas as pd
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table

from scraper import build_session, fetch, get_category_urls
from parser import parse_books, get_next_page_url
from exporter import to_csv, to_excel

BASE_URL = "https://books.toscrape.com"
app = typer.Typer(help="Scrape books.toscrape.com and export to CSV / Excel.")
console = Console()


def _scrape_pages(start_url: str, session, max_pages: Optional[int], delay: float) -> list[dict]:
    books = []
    url = start_url
    page = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Scraping pages...", total=max_pages)

        while url:
            html = fetch(url, session, delay=delay)
            if not html:
                break

            page_books = parse_books(html, url)
            books.extend(page_books)
            page += 1
            progress.advance(task)
            console.print(f"  Page {page}: {len(page_books)} books (total {len(books)})")

            if max_pages and page >= max_pages:
                break

            url = get_next_page_url(html, url)

    return books


@app.command()
def scrape(
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Category name (e.g. 'Mystery'). Scrapes all if omitted."),
    max_pages: Optional[int] = typer.Option(None, "--pages", "-p", help="Max pages to scrape per category."),
    delay: float = typer.Option(1.0, "--delay", "-d", help="Seconds between requests."),
    output: Path = typer.Option(Path("output/books"), "--output", "-o", help="Output path without extension."),
    fmt: str = typer.Option("both", "--format", "-f", help="Output format: csv / excel / both."),
):
    console.print("\n[bold cyan]Web Scraper Toolkit[/bold cyan]")
    console.print(f"Target : [yellow]books.toscrape.com[/yellow]")
    console.print(f"Output : [yellow]{output}.[csv/xlsx][/yellow]\n")

    session = build_session()
    all_books = []

    if category:
        console.print(f"Fetching category list...")
        categories = get_category_urls(session)
        matched = {k: v for k, v in categories.items() if k.lower() == category.lower()}
        if not matched:
            available = ", ".join(categories.keys())
            console.print(f"[red]Category '{category}' not found.[/red]\nAvailable: {available}")
            raise typer.Exit(1)
        name, url = next(iter(matched.items()))
        console.print(f"Category: [green]{name}[/green]")
        all_books = _scrape_pages(url, session, max_pages, delay)
    else:
        console.print("Scraping [green]all categories[/green]...")
        all_books = _scrape_pages(BASE_URL, session, max_pages, delay)

    if not all_books:
        console.print("[red]No books scraped.[/red]")
        raise typer.Exit(1)

    df = pd.DataFrame(all_books)

    # Summary table
    table = Table(title=f"Scrape Complete — {len(df)} books")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")
    table.add_row("Total books", str(len(df)))
    table.add_row("Avg price", f"£{df['price_gbp'].mean():.2f}")
    table.add_row("Avg rating", f"{df['rating'].mean():.1f} / 5")
    table.add_row("In stock", str((df["availability"] == "In stock").sum()))
    console.print(table)

    if fmt in ("csv", "both"):
        csv_path = output.with_suffix(".csv")
        to_csv(df, csv_path)
        console.print(f"[green]✓[/green] CSV  → {csv_path}")

    if fmt in ("excel", "both"):
        xlsx_path = output.with_suffix(".xlsx")
        to_excel(df, xlsx_path)
        console.print(f"[green]✓[/green] Excel → {xlsx_path}")


@app.command()
def categories():
    """List all available categories."""
    session = build_session()
    cats = get_category_urls(session)
    table = Table(title="Available Categories")
    table.add_column("Category", style="cyan")
    table.add_column("URL")
    for name, url in cats.items():
        table.add_row(name, url)
    console.print(table)


if __name__ == "__main__":
    app()
