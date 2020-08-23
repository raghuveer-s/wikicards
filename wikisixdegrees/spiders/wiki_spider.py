import scrapy
import datetime
from wikisixdegrees.items import WikiPageItem

class WikiSpider(scrapy.Spider):
    name = 'wikispider'
    allowed_domains = ['wikipedia.org']

    start_urls = ["https://en.wikipedia.org/wiki/Main_Page"]

    def parse(self, response):
        url = response.url
        links = [s.get() for s in response.xpath("//a/@href")]
        title = response.xpath("//head/title/text()").get()
        content = response.xpath("//html").get()
        date_visited = datetime.datetime.now()

        # construct item objects to return
        pageItem = WikiPageItem(url=url, title=title, content=content, date_visited=date_visited)
        yield pageItem


