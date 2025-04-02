# Scrape Machine

A powerful web scraping tool for lead generation, built with Scrapy.

## Features

- Google search scraping
- Email and phone number extraction
- LinkedIn profile scraping (example implementation)
- Data cleaning and validation
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

### Running the Google Search Spider

Basic usage:
```bash
scrapy crawl google
```

With custom query and number of pages:
```bash
scrapy crawl google -a query="site:linkedin.com/in/ AND (email OR contact) AND (CTO OR developer)" -a num_pages=5
```

### Output

The scraper will create a JSON file in the format `leads_YYYYMMDD_HHMMSS.json` containing the scraped leads. Each lead will include:
- Name
- Email (if found)
- Phone (if found)
- Company
- Position
- Website
- LinkedIn URL
- Source
- Scrape date

## Customization

You can modify the following files to customize the scraper:

- `scrape_machine/settings.py`: Scraper configuration
- `scrape_machine/spiders/google_spider.py`: Google search spider
- `scrape_machine/pipelines.py`: Data processing pipeline

## Notes

- Respect websites' robots.txt and terms of service
- Use appropriate delays between requests
- Consider using proxies for large-scale scraping
- Some websites (like LinkedIn) have strict scraping policies

## License

MIT License
