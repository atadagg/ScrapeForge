# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from datetime import datetime


class ScrapeMachinePipeline:
    def process_item(self, item, spider):
        return item


class LeadPipeline:
    """Pipeline for processing and storing lead items."""
    
    def __init__(self):
        self.file = None
        
    def open_spider(self, spider):
        """Called when spider starts - open the output file."""
        filename = f'leads_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        self.file = open(filename, 'w')
        
    def close_spider(self, spider):
        """Called when spider ends - close the output file."""
        if self.file:
            self.file.close()
            
    def process_item(self, item, spider):
        """Process each lead item."""
        adapter = ItemAdapter(item)
        
        # Clean and validate email
        if adapter.get('email'):
            adapter['email'] = adapter['email'].lower()
            
        # Clean and format phone number
        if adapter.get('phone'):
            # Remove all non-numeric characters
            phone = ''.join(filter(str.isdigit, adapter['phone']))
            # Format as XXX-XXX-XXXX
            if len(phone) == 10:
                adapter['phone'] = f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
            elif len(phone) == 11 and phone.startswith('1'):
                adapter['phone'] = f"{phone[1:4]}-{phone[4:7]}-{phone[7:]}"
            else:
                adapter['phone'] = None
                
        # Ensure all strings are stripped of whitespace
        for field in adapter.field_names():
            if isinstance(adapter.get(field), str):
                adapter[field] = adapter[field].strip()
                
        # Write to JSON file
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        
        return item
