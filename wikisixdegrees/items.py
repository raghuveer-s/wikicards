# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field

class WikiPageItem(scrapy.Item):
    url = Field()
    title = Field()
    content = Field()
    outgoing_links = Field()
    date_visited = Field()
    followed = Field()