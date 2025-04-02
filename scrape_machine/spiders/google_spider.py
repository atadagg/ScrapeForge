from urllib.parse import urlencode
import random
import time
import gzip
import brotli
from scrapy.http import Request
from ..items import LeadItem
from .base_spider import BaseSpider

class GoogleSpider(BaseSpider):
    name = 'google'
    allowed_domains = ['google.com']
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': random.uniform(3, 7),
        'COOKIES_ENABLED': False,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
    }
    
    def __init__(self, query=None, num_pages=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query or "site:linkedin.com/in/ AND (email OR contact) AND (CEO OR founder)"
        self.num_pages = int(num_pages)
        self.user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        
    def start_requests(self):
        """Generate start URLs for Google search."""
        base_url = 'https://www.google.com/search?'
        
        for page in range(self.num_pages):
            # Add random delay between requests
            time.sleep(random.uniform(2, 5))
            
            params = {
                'q': self.query,
                'start': page * 10,
                'hl': 'en',  # Set language to English
                'num': 100,  # Get 100 results per page
                'filter': '0'  # Show all results
            }
            url = base_url + urlencode(params)
            
            # Randomize user agent for each request
            headers = {
                'User-Agent': random.choice(self.user_agents)
            }
            
            yield Request(
                url,
                callback=self.parse,
                meta={'page': page + 1},
                headers=headers,
                dont_filter=True
            )
            
    def parse(self, response):
        """Parse Google search results page."""
        try:
            # Get the response body and decode it
            body = response.body
            if response.headers.get('Content-Encoding', b'').lower() == b'br':
                body = brotli.decompress(body)
            elif response.headers.get('Content-Encoding', b'').lower() == b'gzip':
                body = gzip.decompress(body)
            
            # Convert to text
            text = body.decode('utf-8', errors='ignore')
            
            # Check if we got blocked
            if 'Our systems have detected unusual traffic' in text:
                self.logger.warning('Google detected automated traffic. Waiting...')
                time.sleep(random.uniform(30, 60))
                yield Request(response.url, callback=self.parse, dont_filter=True)
                return
                
            # Extract search result links
            for result in response.css('div.g'):
                # Extract title and link
                title_elem = result.css('h3::text').get()
                link = result.css('a::attr(href)').get()
                
                if not link or not link.startswith('http'):
                    continue
                    
                # Extract snippet
                snippet = result.css('div.VwiC3b::text').get()
                if not snippet:
                    snippet = result.css('div.VwiC3b span::text').get()
                    
                # Clean the data
                title = self.clean_text(title_elem)
                snippet = self.clean_text(snippet)
                
                # Extract potential lead information from the snippet
                emails = self.extract_emails(snippet)
                phones = self.extract_phones(snippet)
                
                if emails or phones:
                    lead = LeadItem()
                    lead['name'] = title
                    lead['email'] = emails[0] if emails else None
                    lead['phone'] = phones[0] if phones else None
                    lead['website'] = link
                    lead['source'] = 'google_search'
                    lead['scraped_date'] = self.get_current_datetime()
                    yield lead
                    
                # Follow the link if it's a LinkedIn profile
                if 'linkedin.com/in/' in link:
                    # Add random delay before following LinkedIn links
                    time.sleep(random.uniform(2, 4))
                    yield Request(
                        link,
                        callback=self.parse_linkedin_profile,
                        meta={'lead': lead},
                        headers={'User-Agent': random.choice(self.user_agents)},
                        dont_filter=True
                    )
                    
        except Exception as e:
            self.logger.error(f"Error parsing response: {str(e)}")
            # Save the response for debugging
            with open(f'error_response_{int(time.time())}.html', 'wb') as f:
                f.write(response.body)
                
    def parse_linkedin_profile(self, response):
        """Parse LinkedIn profile page for additional information."""
        try:
            lead = response.meta.get('lead', LeadItem())
            
            # Extract more information from LinkedIn profile
            lead['position'] = self.clean_text(response.css('h2.top-card-layout__headline::text').get())
            lead['company'] = self.clean_text(response.css('h4.top-card-company-name::text').get())
            lead['linkedin_url'] = response.url
            
            yield lead
        except Exception as e:
            self.logger.error(f"Error parsing LinkedIn profile: {str(e)}") 