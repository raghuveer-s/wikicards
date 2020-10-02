import logging
import sys

from scrapy.crawler import CrawlerProcess
from scrapy import signals
import wikisixdegrees.settings as settings
from wikisixdegrees.spiders.wiki_spider import WikiSpider
from wikisixdegrees.repository.wiki_repository import NodeRepository
from wikisixdegrees.service.path_finder import PathFinder
import validators

def explore_existing():
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

def explore_paths(link_a:str):
    requests = []
    requests.append(link_a)
    start_spider(requests)

def get_paths(link_a:str, link_b:str):
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

def start_spider(requests,**kwargs):
    '''
    Start the wiki spider
    '''

    if len(requests) == 0:
        requests.append("https://en.wikipedia.org/wiki/Main_Page")
    
    WikiSpider.start_urls = requests
    if kwargs.get('depth_limit'):
        WikiSpider.custom_settings['DEPTH_LIMIT'] = kwargs['depth_limit']
    
    crawler_process = CrawlerProcess(settings={key:getattr(settings, key) for key in dir(settings)})
    crawler = crawler_process.create_crawler(WikiSpider)
    crawler.signals.connect(cb_spider_closed, signals.spider_closed)
    crawler_process.crawl(crawler)
    crawler_process.start()

def cb_spider_closed():
    print('spider closed')

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1 and args[0] == "app.py":
        explore_existing()
    elif len(args) == 2 and args[0] == "app.py" and validators.url(args[1]):
        link_a = args[1]
        explore_paths(link_a)
    elif len(args) == 3 and args[0] == "app.py" and validators.url(args[1]) and validators.url(args[2]):
        link_a = args[1]
        link_b = args[2]
        get_paths(link_a, link_b)