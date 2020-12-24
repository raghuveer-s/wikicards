import logging
import datetime

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
import scrapy

from wikicrawler.items import WikiPageItem
from wikicrawler.repository.wiki_repository import NodeRepository

logger = logging.getLogger("wikicrawler")

class WikiSpider(scrapy.Spider):
    name = "wikispider"
    allowed_domains = ["wikipedia.org"]
    custom_settings = {"DEPTH_LIMIT": 0}

    start_urls = ["https://en.wikipedia.org/wiki/Main_Page"]

    def start_requests(self):
        self.logger.info(self.start_urls)
        for url in self.start_urls:
            yield Request(url, callback=self.parse, errback=self.errback, dont_filter=True)

    def parse(self, response):
        url = response.url
        # links = [s.get() for s in response.xpath("//a/@href")]
        link_extractor = LinkExtractor(
            allow=("\/wiki\/.*"), allow_domains=("en.wikipedia.org"), canonicalize=True
        )
        links = link_extractor.extract_links(response)

        title = response.xpath("//head/title/text()").get()
        content = response.xpath("//html").get()
        date_visited = datetime.datetime.now()

        # construct item objects to return
        # Note that this page item has outgoing links since it has been followed
        pageItem = WikiPageItem(
            url=url,
            title=title,
            content=content,
            date_visited=date_visited,
            followed=True,
            outgoing_links=links,
        )
        yield pageItem

        # meta["depth"] is part of the DepthMiddleware in scrapy.
        # It is used to control the depth of each request in the site being scraped.
        if response.request.meta["depth"] < self.custom_settings["DEPTH_LIMIT"]:
            for link in links:
                req = Request(link.url)
                yield req
    
    def errback(self, failure):
        logger.error(repr(failure))

        url = failure.request.url

        node_repository = NodeRepository()
        node_repository.delete_node_by_url(url)

        print("Deleted url since it gave error: " + url)