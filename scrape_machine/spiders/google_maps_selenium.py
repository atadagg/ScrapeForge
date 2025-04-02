import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from scrapy import Spider
from ..items import LeadItem
from .base_spider import BaseSpider

class GoogleMapsSeleniumSpider(BaseSpider):
    name = 'google_maps_selenium'
    allowed_domains = ['google.com']
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': random.uniform(3, 5),
        'COOKIES_ENABLED': True,
    }
    
    def __init__(self, query=None, location=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query or "doctor"
        self.location = location or "Tulsa, OK"
        
        # Setup Chrome options
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Commented out to avoid detection
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize the Chrome WebDriver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Add random delay between actions
        self.driver.implicitly_wait(10)
        
    def scroll_results(self):
        """Scroll through the results panel to load more listings."""
        try:
            results_panel = self.driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
            for _ in range(30):  # Just scroll 30 times
                self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", results_panel)
                time.sleep(2)
        except Exception:
            pass
            
    def extract_listing_data(self, listing):
        """Extract data from a listing element."""
        try:
            lead = LeadItem()
            
            # Get name
            name_elem = listing.find_element(By.CSS_SELECTOR, "div.qBF1Pd")
            lead['name'] = name_elem.text
            lead['company'] = lead['name']
            
            # Get address
            try:
                address_elem = listing.find_element(By.CSS_SELECTOR, "div.W4Efsd span:last-child")
                lead['address'] = address_elem.text
            except:
                lead['address'] = None
            
            # Get phone
            try:
                phone_elem = listing.find_element(By.CSS_SELECTOR, "span.UsdlK")
                lead['phone'] = phone_elem.text
            except:
                lead['phone'] = None
            
            # Get website
            try:
                website_elem = listing.find_element(By.CSS_SELECTOR, "a[data-item-id='authority']")
                lead['website'] = website_elem.get_attribute('href')
            except:
                lead['website'] = None
            
            lead['source'] = 'google_maps'
            lead['scraped_date'] = self.get_current_datetime()
            
            return lead
            
        except Exception:
            return None
        
    def start_requests(self):
        """Start with a direct search request."""
        url = f'https://www.google.com/maps/search/{self.query}+{self.location}'
        
        try:
            self.driver.get(url)
            time.sleep(5)
            
            # Wait for results to load
            try:
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.Nv2PK"))
                )
            except TimeoutException:
                return
            
            # Scroll to load more results
            self.scroll_results()
            
            # Get all listings
            listings = self.driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
            
            # Process each listing
            for listing in listings:
                try:
                    lead = self.extract_listing_data(listing)
                    if lead:
                        yield lead
                except Exception:
                    continue
                    
        except Exception:
            pass
        finally:
            self.driver.quit()
            
    def closed(self, reason):
        """Clean up when spider closes."""
        if hasattr(self, 'driver'):
            self.driver.quit() 