import re
from datetime import datetime
from scrapy import Spider
from typing import List, Optional

class BaseSpider(Spider):
    """
    Base spider class with common functionality for all spiders.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Common regex patterns
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.phone_pattern = re.compile(r'\+?1?\s*\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}')
        
    def extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text."""
        if not text:
            return []
        return list(set(self.email_pattern.findall(text)))
    
    def extract_phones(self, text: str) -> List[str]:
        """Extract phone numbers from text."""
        if not text:
            return []
        return list(set(self.phone_pattern.findall(text)))
    
    def clean_text(self, text: Optional[str]) -> Optional[str]:
        """Clean text by removing extra whitespace and special characters."""
        if not text:
            return None
        # Remove special characters and normalize whitespace
        text = re.sub(r'[\r\n\t]+', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def get_current_datetime(self) -> str:
        """Get current datetime in ISO format."""
        return datetime.now().isoformat()
        
    def safe_extract_text(self, response, css_selector: str) -> Optional[str]:
        """Safely extract text from a CSS selector."""
        try:
            text = response.css(css_selector).get()
            return self.clean_text(text)
        except Exception as e:
            self.logger.warning(f"Error extracting text with selector {css_selector}: {str(e)}")
            return None 