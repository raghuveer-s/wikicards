import logging
import sys

from scrapy.crawler import CrawlerProcess
from scrapy import signals
from . import settings

from .spiders.wiki_spider import WikiSpider
from .repository.wiki_repository import NodeRepository
from .service.path_finder import PathFinder
import validators


class WikiCrawler:
    def explore_existing(self):
        repo = NodeRepository()
        unvisited_nodes = repo.get_unvisited_nodes()

        max_requests = settings.CUSTOM_MAX_REQUESTS

        print("Max requests: {}".format(max_requests))

        requests = []
        i = 0
        for node in unvisited_nodes:
            if i < max_requests:
                requests.append(node.url)
                i += 1

        start_spider(requests)

    def explore_paths(self, link_a: str):
        requests = []
        requests.append(link_a)
        start_spider(requests)

    def get_paths(self, link_a: str, link_b: str):
        paths = PathFinder().find(link_a, link_b)
        requests = []

        if len(paths) == 0:
            # TODO
            # Output that path does not exist, trying to find
            requests.append(link_a)
            requests.append(link_b)

            start_spider(requests, depth_limit=2)
        else:
            # TODO
            # If path exists, the app must catch the stop signal and give the shortest path
            pass
        pass

    def start_spider(self, requests, **kwargs):
        """
        Start the wiki spider
        """

        if len(requests) == 0:
            requests.append("https://en.wikipedia.org/wiki/Main_Page")

        WikiSpider.start_urls = requests
        if kwargs.get("depth_limit"):
            WikiSpider.custom_settings["DEPTH_LIMIT"] = kwargs["depth_limit"]

        crawler_process = CrawlerProcess(
            settings={key: getattr(settings, key) for key in dir(settings)}
        )
        crawler = crawler_process.create_crawler(WikiSpider)
        crawler.signals.connect(cb_spider_closed, signals.spider_closed)
        crawler_process.crawl(crawler)
        crawler_process.start()

    def cb_spider_closed(self):
        print("spider closed")


def start(args):
    wikicrawler = WikiCrawler()
    if len(args) == 1 and args[0] == "app.py":
        wikicrawler.explore_existing()
    elif len(args) == 2 and args[0] == "app.py" and validators.url(args[1]):
        link_a = args[1]
        wikicrawler.explore_paths(link_a)
    elif (
        len(args) == 3
        and args[0] == "app.py"
        and validators.url(args[1])
        and validators.url(args[2])
    ):
        link_a = args[1]
        link_b = args[2]
        wikicrawler.get_paths(link_a, link_b)