# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class ScrapeMachineItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class LeadItem(Item):
    """
    Item class to store lead information.
    
    Fields:
    - name: Full name of the person
    - email: Email address
    - phone: Phone number
    - company: Company name
    - position: Job position/title
    - website: Company/personal website
    - linkedin_url: LinkedIn profile URL
    - source: Where this lead was found
    - scraped_date: When this lead was scraped
    """
    name = Field()
    email = Field()
    phone = Field()
    company = Field()
    position = Field()
    website = Field()
    linkedin_url = Field()
    source = Field()
    scraped_date = Field()
