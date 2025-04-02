from urllib.parse import urlencode, quote
import random
import time
import json
import re
from scrapy.http import Request, JsonRequest
from ..items import LeadItem
from .base_spider import BaseSpider

class GoogleMapsSpider(BaseSpider):
    name = 'google_maps'
    allowed_domains = ['google.com']
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': random.uniform(2, 4),
        'COOKIES_ENABLED': True,
    }
    
    def __init__(self, query=None, location=None, radius=50000, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query or "doctor"
        self.location = location or "Tulsa, OK"
        self.radius = int(radius)  # radius in meters
        self.user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        ]
        
    def start_requests(self):
        """Start with a direct search request."""
        encoded_query = quote(f"{self.query} {self.location}")
        url = f'https://www.google.com/maps/search/{encoded_query}'
        
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/maps',
            'Origin': 'https://www.google.com',
        }
        
        yield Request(
            url=url,
            callback=self.parse_initial_response,
            headers=headers,
            dont_filter=True
        )
        
    def parse_initial_response(self, response):
        """Parse the initial response to extract the data."""
        try:
            # Save response for debugging
            with open('debug_response.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Extract the data section
            data_section = re.search(r'window\.APP_INITIALIZATION_STATE=([^;]+);', response.text)
            if not data_section:
                self.logger.error("Could not find APP_INITIALIZATION_STATE")
                return
                
            # The data is a list of lists, we need to find the one with business data
            raw_data = data_section.group(1)
            
            # Find all arrays in the data
            arrays = re.findall(r'\[\[.*?\]\]', raw_data)
            
            for array in arrays:
                try:
                    data = json.loads(array)
                    # Business data typically has specific fields we can check for
                    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                        for business_data in data:
                            if not isinstance(business_data, list) or len(business_data) < 5:
                                continue
                                
                            # Try to extract business information
                            try:
                                lead = LeadItem()
                                
                                # Extract what we can find
                                for item in business_data:
                                    if isinstance(item, str):
                                        # Look for business name
                                        if not lead.get('name') and len(item) > 3:
                                            lead['name'] = item
                                            lead['company'] = item
                                        # Look for website
                                        elif item.startswith('http'):
                                            lead['website'] = item
                                        # Look for phone
                                        elif re.match(r'[\d\-\(\)\s\+]{10,}', item):
                                            lead['phone'] = item
                                    elif isinstance(item, list):
                                        # Address is often in a list
                                        if len(item) > 0 and isinstance(item[0], str):
                                            lead['address'] = item[0]
                                
                                if lead.get('name'):  # Only yield if we found at least a name
                                    lead['source'] = 'google_maps'
                                    lead['scraped_date'] = self.get_current_datetime()
                                    
                                    # If we have a website, try to find email there
                                    if lead.get('website'):
                                        yield Request(
                                            lead['website'],
                                            callback=self.parse_website,
                                            meta={'lead': lead},
                                            headers={'User-Agent': random.choice(self.user_agents)},
                                            dont_filter=True,
                                            errback=self.handle_error
                                        )
                                    else:
                                        yield lead
                                        
                            except Exception as e:
                                self.logger.error(f"Error parsing business data: {str(e)}")
                                continue
                                
                except json.JSONDecodeError:
                    continue
                    
            # Look for pagination token
            next_token = re.search(r'"VQF1hc":"([^"]+)"', response.text)
            if next_token:
                next_url = f"{response.url}?pageToken={next_token.group(1)}"
                yield Request(
                    next_url,
                    callback=self.parse_initial_response,
                    headers={'User-Agent': random.choice(self.user_agents)},
                    dont_filter=True
                )
                
        except Exception as e:
            self.logger.error(f"Error in parse_initial_response: {str(e)}")
            # Save the raw response for debugging
            with open('error_response.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
                
    def parse_website(self, response):
        """Parse business website to find contact information."""
        try:
            lead = response.meta.get('lead', LeadItem())
            
            # Look for contact page links
            contact_links = response.css('a[href*="contact"]::attr(href), a[href*="Contact"]::attr(href)').getall()
            if contact_links:
                # Visit the first contact page found
                contact_url = response.urljoin(contact_links[0])
                yield Request(
                    contact_url,
                    callback=self.parse_contact_page,
                    meta={'lead': lead},
                    headers={'User-Agent': random.choice(self.user_agents)},
                    dont_filter=True,
                    errback=self.handle_error
                )
            else:
                # If no contact page, extract from current page
                self.extract_contact_info(response, lead)
                yield lead
                
        except Exception as e:
            self.logger.error(f"Error parsing website: {str(e)}")
            yield response.meta.get('lead')
            
    def parse_contact_page(self, response):
        """Parse the contact page for information."""
        try:
            lead = response.meta.get('lead', LeadItem())
            self.extract_contact_info(response, lead)
            yield lead
            
        except Exception as e:
            self.logger.error(f"Error parsing contact page: {str(e)}")
            yield response.meta.get('lead')
            
    def extract_contact_info(self, response, lead):
        """Extract contact information from a page."""
        # Extract all text from the page
        text = ' '.join(response.css('body ::text').getall())
        
        # Look for email addresses
        emails = self.extract_emails(text)
        if emails and not lead.get('email'):
            lead['email'] = emails[0]
            
        # Look for additional phone numbers
        phones = self.extract_phones(text)
        if phones and not lead.get('phone'):
            lead['phone'] = phones[0]
            
    def handle_error(self, failure):
        """Handle request errors."""
        self.logger.error(f"Request failed: {failure.value}")
        # If there's a lead in meta, yield it even if we couldn't get more info
        lead = failure.request.meta.get('lead')
        if lead:
            return lead 