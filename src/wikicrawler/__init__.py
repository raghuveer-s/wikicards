#import crochet
#crochet.setup()

import logging
import sched
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.twisted import TwistedScheduler

#from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy import signals
from scrapy.utils.project import get_project_settings
from . import settings

from .spiders.wiki_spider import WikiSpider
from .repository.wiki_repository import NodeRepository
from .service.path_finder import PathFinder
import validators

logger = logging.getLogger("crawler")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logfile.log")
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class WikiCrawler:
    def explore_existing(self):
        repo = NodeRepository()
        unvisited_nodes = repo.get_unvisited_nodes()

        max_requests = settings.CUSTOM_MAX_REQUESTS

        requests = []
        i = 0
        for node in unvisited_nodes:
            if i < max_requests:
                requests.append(node.url)
                i += 1

        logger.info(' , '.join(requests))

        self.start_spider(requests)

    def explore_paths(self, link_a: str):
        requests = []
        requests.append(link_a)
        self.start_spider(requests)

    def get_paths(self, link_a: str, link_b: str):
        paths = PathFinder().find(link_a, link_b)
        requests = []

        if len(paths) == 0:
            # TODO
            # Output that path does not exist, trying to find
            requests.append(link_a)
            requests.append(link_b)

            self.start_spider(requests, depth_limit=2)
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

        # crawler_process = CrawlerProcess(
        #     settings={key: getattr(settings, key) for key in dir(settings)}
        # )
        # crawler = crawler_process.create_crawler(WikiSpider)
        # crawler.signals.connect(self.cb_spider_closed, signals.spider_closed)
        # crawler_process.crawl(crawler)
        # crawler_process.start()
        
        #crawler_settings = {key: getattr(settings, key) for key in dir(settings)}
        #print(crawler_settings)
        #crawler_runner = CrawlerRunner(settings=crawler_settings)
        crawler_runner = CrawlerRunner(get_project_settings())
        deferred = crawler_runner.crawl(WikiSpider)
        deferred.addCallback(self.cb_spider_closed)

    def cb_spider_closed(self, param):
        logger.info("Spider closed.")

# @crochet.run_in_reactor
# def start(*args):
#     wikicrawler = WikiCrawler()
#     wikicrawler.explore_existing()

    # TODO: Uncomment later when six degrees is implemented

    # if len(args) == 1 and args[0] == "app.py":
    #     wikicrawler.explore_existing()
    # elif len(args) == 2 and args[0] == "app.py" and validators.url(args[1]):
    #     link_a = args[1]
    #     wikicrawler.explore_paths(link_a)
    # elif (
    #     len(args) == 3
    #     and args[0] == "app.py"
    #     and validators.url(args[1])
    #     and validators.url(args[2])
    # ):
    #     link_a = args[1]
    #     link_b = args[2]
    #     wikicrawler.get_paths(link_a, link_b)

def perform_crawl():
    logger.info("Performing crawl.")
    wiki_crawler = WikiCrawler()
    wiki_crawler.explore_existing()

#sched = BackgroundScheduler(daemon=True)
sched = TwistedScheduler()
sched.add_job(perform_crawl, 'interval', minutes=1)
sched.start()