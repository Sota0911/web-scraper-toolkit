# Web Scraper Toolkit

A polished Python web scraper that collects book data from [books.toscrape.com](https://books.toscrape.com) and exports it to CSV and Excel with a formatted summary sheet.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Features

- Scrape all books or filter by category
- Auto-pagination (follows "next" pages automatically)
- Rate limiting — configurable delay between requests
- Retry logic — handles temporary network errors
- Export to **CSV** and/or **Excel** (formatted, with summary sheet)
- Clean CLI with progress bar and color output

## Quickstart

```bash
# 1. Clone
git clone https://github.com/Sota0911/web-scraper-toolkit.git
cd web-scraper-toolkit

# 2. Install
pip install -r requirements.txt

# 3. Run (scrape first 3 pages)
python src/main.py scrape --pages 3
```

Open `output/books.xlsx` to see the result.

## Usage

```bash
# Scrape first 5 pages (all categories)
python src/main.py scrape --pages 5

# Scrape a specific category
python src/main.py scrape --category Mystery

# CSV only
python src/main.py scrape --pages 3 --format csv

# Custom output path
python src/main.py scrape --pages 3 --output output/mystery_books

# List available categories
python src/main.py categories
```

## Output

| File | Contents |
|------|----------|
| `output/books.csv` | Raw data, UTF-8 with BOM (Excel-friendly) |
| `output/books.xlsx` | Formatted workbook with Books sheet + Summary sheet |

**Excel Summary sheet includes:**
- Total books, avg/min/max price, avg rating, in-stock count
- Rating breakdown table

## CLI options

| Option | Default | Description |
|--------|---------|-------------|
| `--category` | all | Category to scrape (e.g. `Mystery`) |
| `--pages` | unlimited | Max pages to scrape |
| `--delay` | 1.0 | Seconds between requests |
| `--output` | `output/books` | Output path (no extension) |
| `--format` | `both` | `csv` / `excel` / `both` |

## Run tests

```bash
pip install pytest
pytest tests/
```

## Tech stack

- **requests** — HTTP client
- **beautifulsoup4 + lxml** — HTML parsing
- **pandas + openpyxl** — data export
- **typer + rich** — CLI and terminal output

## Ethical scraping

This tool targets [books.toscrape.com](https://books.toscrape.com), a site built specifically for practicing web scraping. It includes a configurable delay between requests to avoid overloading servers.

## License

MIT
