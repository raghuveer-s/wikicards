# crochet for running twisted code
import crochet
crochet.setup()

from apscheduler.schedulers.background import BackgroundScheduler

from . import server
from wikicrawler import WikiCrawler

@crochet.run_in_reactor
def perform_crawl():
    print("Performing crawl..")
    wiki_crawler = WikiCrawler()
    wiki_crawler.explore_existing()

app = server.create_app()

sched = BackgroundScheduler(daemon=True)
sched.add_job(perform_crawl, 'interval', minutes=5)
sched.start()