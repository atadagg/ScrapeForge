# ScrapeForge

![ScrapeForge Logo](assets/temporary-logo.png)

Hey there! 👋 Ever found yourself writing the same scraping code over and over? We've been there too. That's why we built ScrapeForge - a toolkit that makes web scraping less painful and more fun.

## What's This All About?

We're building a collection of ready-to-use scrapers that:
- Handle the boring stuff (like pagination and anti-bot measures)
- Work together like building blocks
- Just need a simple config file to get going
- Come with smart defaults that actually work

Think of it as your scraping toolbox, not another framework to learn.

## What Can You Do With It?

Right now, you can:
- ✅ Find local businesses from public directories
- ✅ Grab data from product listings and search results
- ✅ Follow links and extract details from pages
- ✅ (Coming soon) Set up automatic scraping with retries

## How It's Built

We keep things simple and modular:
- `core/`: The engine that runs everything
- `modules/`: Ready-to-use scrapers (like `business_directory`, `ecommerce_listing`)
- `utils/`: Handy tools for pagination, proxies, and parsing

Each scraper:
- Has a simple interface (`run(config)` or CLI)
- Uses YAML/JSON for config
- Spits out clean data (CSV, JSON, or straight to DB)

## Quick Start

```bash
# Get the code
git clone https://github.com/atadagg/scrapeforge.git
cd scrapeforge

# Set up your environment
pip install -r requirements.txt

# Try it out
python main.py --module=business_directory --config=configs/istanbul_local.json
```

## What's Under the Hood?

We use:
- Python (because it's awesome for scraping)
- Scrapy (for the heavy lifting)
- Playwright/Selenium (when we need to handle JavaScript)
- Smart proxy rotation (to avoid getting blocked)
- Docker (optional, but handy for testing)
- YAML/JSON (for easy config)
- Pandas/SQLite (for storing results)

## What's Next?

We're working on a cool dashboard to manage all your scrapes in one place. Stay tuned!

## Want to Help?

We'd love your help! Whether you want to:
- Add new scrapers for real websites
- Make the system more robust
- Help with anti-bot tricks
- Or something else cool

Check out:
- Our [contributing guide](./CONTRIBUTING.md)
- [Open issues](https://github.com/atadagg/ScrapeForge/issues)
- ["Good first issue"](https://github.com/atadagg/ScrapeForge/labels/good%20first%20issue) tasks

## License

MIT - because sharing is caring! 

## Join the Fun

We built this because we were tired of writing one-off scraping scripts. If that sounds familiar, you're in the right place!

Follow us on Twitter or jump into our Discussions to help shape what's next.

---

# Current Feature: Google Maps Scraper

Right now, we've got a solid Google Maps scraper that finds business leads. Here's how to use it:

## Setting It Up

1. Create a virtual environment (trust us, you'll want this):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install what you need:
```bash
pip install -r requirements.txt
```

## Using It

### Basic Usage
Want to find doctors in Tulsa? Just run:
```bash
scrapy crawl google_maps_selenium
```

### Custom Search
Looking for dentists in New York? Try:
```bash
scrapy crawl google_maps_selenium -a query="dentist" -a location="New York, NY"
```

**Pro Tip:** We use a visible Chrome window by default to avoid getting blocked. You can use headless mode if you want, but it might make Google suspicious.

## What You Get

The scraper creates a JSON file named `leads_YYYYMMDD_HHMMSS.json` with:
- Business name
- Address (sometimes includes ratings - we're working on cleaning that up)
- Phone number
- Website (if they have one)
- Source (always 'google_maps')
- When we found it

## Customizing It

Want to tweak how it works? Check out:
- `scrape_machine/settings.py`: General settings
- `scrape_machine/spiders/google_maps_selenium.py`: The main scraping logic
- `scrape_machine/pipelines.py`: How we process the data
- `scrape_machine/items.py`: The data structure

## A Few Tips

- Play nice with robots.txt
- Google Maps changes its layout sometimes - we might need to update selectors
- We've got built-in delays to avoid overwhelming servers
- For big jobs, consider using proxies

Let me know if you need anything else! 🚀
