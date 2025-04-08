# Contributing to ScrapeForge

Hey there! 👋 Thanks for wanting to help out with ScrapeForge. We're building a toolkit to make web scraping less painful, and we'd love your help.

## What We're Building

We want ScrapeForge to be:
- Easy to extend with new scrapers
- Tough enough to handle real-world websites
- Simple to configure 
- Clean and well-documented

## Getting Started

1. **Fork the Repo**
   - Hit that "Fork" button up in the top right
   - Clone your fork: `git clone https://github.com/YOUR_USERNAME/scrapeforge.git`

2. **Set Up Your Environment**
   ```bash
   # Create a virtual environment 
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install the good stuff
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Extra tools for development
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-cool-feature
   # or
   git checkout -b fix/that-annoying-bug
   ```

## How We Work

### Writing Code
- Keep it clean and readable (PEP 8 is your friend)
- Add type hints (they're not just for show)
- Keep functions short and sweet (under 50 lines if you can)
- Add docstrings (your future self will thank you)


### Building Modules
Here's how we structure our scraping modules:
```
modules/
└── your_module/
    ├── __init__.py
    ├── scraper.py      # The main scraping logic lives here
    ├── config.py       # Configuration options
    └── tests/          # Tests go here
```

### Testing
- Write tests for new stuff
- Make sure everything passes before you submit
- Run `pytest` to check your work

### Documentation
- Update the README if you add new features
- Document any new config options
- Add examples in the `examples/` folder

## Making Pull Requests

1. **Before You Submit**
   - Run the tests: `pytest`
   - Check your code style: `flake8`
   - Update docs if needed
   - Make sure you're up to date with main

2. **Creating Your PR**
   - Give it a clear title
   - Link to any related issues
   - Add screenshots if you changed the UI
   - Tell us what you changed and why

3. **During Review**
   - We might ask for changes - that's normal!
   - Keep your commits focused
   - Update your PR as needed

## Reporting Bugs

Found a bug? Help us fix it! Please include:
- Your Python version
- Your OS
- Steps to make it happen
- What you expected vs what happened
- Screenshots if they help

## Suggesting Features

Got a cool idea? Tell us about it! We want to know:
- What problem are you trying to solve?
- How would you solve it?
- Got any examples?
- Will it break existing stuff?

## Building a New Module

Here's a quick example of how to build a new scraper:

```python
from scrapeforge.core import BaseModule

class CoolScraper(BaseModule):
    def __init__(self, config):
        super().__init__(config)
    
    def run(self):
        # Your scraping magic here
        pass
```

And here's how to set up its config:

```python
# config.py
from pydantic import BaseModel

class CoolScraperConfig(BaseModel):
    url: str
    max_pages: int = 10
    # Add other options here
```

And a basic test:

```python
# tests/test_cool_scraper.py
def test_cool_scraper():
    config = CoolScraperConfig(url="https://example.com")
    scraper = CoolScraper(config)
    results = scraper.run()
    assert len(results) > 0
```

## Being Part of the Community

- Be nice to each other
- Help others learn
- Share what you know
- Follow our code of conduct

## Need Help?

- Found a bug? Open an issue
- Got questions? Start a discussion
- Want to chat? Join our community

Thanks for helping make ScrapeForge better! 🚀