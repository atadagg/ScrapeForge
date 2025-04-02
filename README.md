# Scrape Machine

A web scraping tool focused on extracting business lead information from Google Maps using Selenium and Scrapy.

## Features

- Google Maps search result scraping using Selenium
- Extracts business name, address, phone number, and website
- Configurable search query and location
- Data cleaning and validation (basic)
- JSON export with proper formatting

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

## License

MIT License
