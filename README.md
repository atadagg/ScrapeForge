# ScrapeForge

**Modular, ready-to-use web scrapers for real-world data extraction**

ScrapeForge is an open-source scraping toolkit designed to solve *actual problems* — like finding business leads, extracting product listings, or crawling article archives — without writing boilerplate code.

We're building a plug-and-play system of scraping modules that:
- Abstract common patterns (e.g., following paginated lists, extracting from template-based pages)
- Are reusable and composable
- Require minimal configuration
- Come with smart defaults, including anti-bot measures and fault tolerance

> Think of it like a power toolset, not a framework.

---

## 🔧 Use Cases

ScrapeForge provides out-of-the-box modules for:

- ✅ Scraping local businesses from public directories  
- ✅ Extracting data from paginated product lists or search result pages  
- ✅ Following links from a listing to detail pages and extracting structured fields  
- ✅ Periodic scraping with automatic retries & rotation (coming soon)  

---

## 🧱 Architecture

ScrapeForge is built around a modular plugin-style architecture:
- `core/`: Execution engine, scheduler, config loader
- `modules/`: Plug-and-play scraping flows (e.g., `business_directory`, `ecommerce_listing`, etc.)
- `utils/`: Common helpers for pagination, proxy rotation, HTML parsing, etc.

Each module:
- Has a standard interface (`run(config)` or CLI)
- Accepts config files (YAML or JSON)
- Outputs structured data (CSV, JSON, or directly to DBs)

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/your-org/scrapeforge.git
cd scrapeforge

# Install dependencies
pip install -r requirements.txt

# Run a sample scraper
python main.py --module=business_directory --config=configs/istanbul_local.json
```

## 📦 Tech Stack

- Python: Simplicity and wide ecosystem support
- Scrapy (tentative): Industrial-strength crawling framework with battle-tested features like retries, throttling, and selectors
- Playwright or Selenium (optional): For JavaScript-heavy pages
- Rotating proxies / user-agent pools: Built-in or pluggable
- Docker (optional): For sandboxed, repeatable scrapes
- JSON/YAML: For configuration-driven scrapes
- Pandas / SQLite / CSV: For lightweight data output

## 🧠 Future

A unified CLI + GUI dashboard for managing scrapes across modules.

## 🤝 Contributing

We welcome contributions! If you have an idea for a new scraper module (e.g., job boards, product listings, open datasets), or want to improve the system, start here:

- [Read the CONTRIBUTING guide](./CONTRIBUTING.md)
- Browse [open issues](https://github.com/your-org/your-project/issues)
- Check out ["good first issue"](https://github.com/atadagg/scrape-machine/labels/good%20first%20issue) tasks

We’re especially looking for:
- New modules for scraping real websites
- Improvements to our modular architecture
- Anti-bot techniques (proxy pools, captcha solvers, etc.)

## 📜 License

MIT — open to all.

## 🌍 Join Us

This project was created to make scraping faster, cleaner, and accessible. If you've ever built a throwaway script for a one-off scrape, we've been there. ScrapeForge turns those scripts into durable tools.

Follow us on Twitter or join the Discussions to shape the roadmap.

---

# Current Implementation: Google Maps Scraper

The current implementation includes a Google Maps scraper that extracts business lead information. Below are the specific details for this module:

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Google Maps Selenium Spider

Basic usage (uses default query "doctor" and location "Tulsa, OK"):
```bash
scrapy crawl google_maps_selenium
```

With custom query and location:
```bash
scrapy crawl google_maps_selenium -a query="dentist" -a location="New York, NY"
```

**Note:** The spider uses a visible Chrome browser window by default to avoid detection. You can uncomment the `--headless` option in the spider code if needed, but it might increase the chances of being blocked.

## Output

The scraper will create a JSON file in the format `leads_YYYYMMDD_HHMMSS.json` containing the scraped leads. Each lead will include:
- `name`: Business name
- `company`: Business name (same as name)
- `address`: Business address (may sometimes capture rating/reviews - needs refinement)
- `phone`: Business phone number
- `website`: Business website URL (if available)
- `source`: Always 'google_maps'
- `scraped_date`: Timestamp of when the lead was scraped

## Customization

You can modify the following files to customize the scraper:

- `scrape_machine/settings.py`: General Scrapy settings
- `scrape_machine/spiders/google_maps_selenium.py`: Google Maps Selenium spider logic
- `scrape_machine/pipelines.py`: Data processing pipeline
- `scrape_machine/items.py`: Definition of the `LeadItem` structure

## Notes

- Respect websites' robots.txt and terms of service.
- Google Maps frequently changes its layout; the CSS selectors in the spider might need updating.
- Use appropriate delays between requests (already implemented with `DOWNLOAD_DELAY` and `time.sleep`).
- Consider using proxies for large-scale scraping to avoid IP bans.
