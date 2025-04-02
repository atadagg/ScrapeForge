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
        """Clean text by removing extra whitespace."""
        if not text:
            return None
        return ' '.join(text.strip().split())
    
    def get_current_datetime(self) -> str:
        """Get current datetime in ISO format."""
        return datetime.now().isoformat() 