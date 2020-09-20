import logging

from scrapy.crawler import CrawlerProcess
import wikisixdegrees.settings as settings
from wikisixdegrees.spiders.wiki_spider import WikiSpider
from wikisixdegrees.repository.wiki_repository import WikiRepository

def main():
    '''
    Main file
    '''
    repo = WikiRepository()
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

def start_spider(requests):
    '''
    Start the wiki spider
    '''

    if len(requests) == 0:
        requests.append("https://en.wikipedia.org/wiki/Main_Page")
    
    WikiSpider.start_urls = requests
    
    process = CrawlerProcess(settings={key:getattr(settings, key) for key in dir(settings)})
    process.crawl(WikiSpider)
    process.start()

if __name__ == "__main__":
    main()