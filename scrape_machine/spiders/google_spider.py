from urllib.parse import urlencode
from scrapy.http import Request
from ..items import LeadItem
from .base_spider import BaseSpider

class GoogleSpider(BaseSpider):
    name = 'google'
    allowed_domains = ['google.com']
    
    custom_settings = {
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 1,  # Be nice to Google
        'DOWNLOAD_DELAY': 5,  # Wait 5 seconds between requests
    }
    
    def __init__(self, query=None, num_pages=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query = query or "site:linkedin.com/in/ AND (email OR contact) AND (CEO OR founder)"
        self.num_pages = int(num_pages)
        
    def start_requests(self):
        """Generate start URLs for Google search."""
        base_url = 'https://www.google.com/search?'
        
        for page in range(self.num_pages):
            params = {
                'q': self.query,
                'start': page * 10  # Google uses multiples of 10 for pagination
            }
            url = base_url + urlencode(params)
            yield Request(url, callback=self.parse, meta={'page': page + 1})
            
    def parse(self, response):
        """Parse Google search results page."""
        # Extract search result links
        for result in response.css('div.g'):
            title = self.clean_text(result.css('h3::text').get())
            link = result.css('a::attr(href)').get()
            snippet = self.clean_text(result.css('div.VwiC3b::text').get())
            
            if not link or not link.startswith('http'):
                continue
                
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
                yield Request(
                    link,
                    callback=self.parse_linkedin_profile,
                    meta={'lead': lead}
                )
                
    def parse_linkedin_profile(self, response):
        """Parse LinkedIn profile page for additional information."""
        lead = response.meta.get('lead', LeadItem())
        
        # Extract more information from LinkedIn profile
        # Note: LinkedIn has strict scraping policies, so this is just an example
        lead['position'] = self.clean_text(response.css('h2.top-card-layout__headline::text').get())
        lead['company'] = self.clean_text(response.css('h4.top-card-company-name::text').get())
        lead['linkedin_url'] = response.url
        
        yield lead 