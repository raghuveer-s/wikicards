import logging
import os
import sys

import ml
import webapp
import wikicrawler

# configure logging
log_format = "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
handler = logging.FileHandler("logfile.log")

logging.basicConfig(format=log_format, handlers=[handler], level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)

def train():
    logger.info("Started training.")
    ml.train()

if __name__ == "__main__":
    args = sys.argv

    # TODO: change this to use argpase

    if len(args) == 2 and args[1] == "train":
        train()
    else:
        logger.info("Started application.")

        # Environment variables
        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "wikicrawler.settings")

        #log_file = open("logfile.log", "a")
        wikicrawler.perform_crawl()
        webapp.app.run(host="127.0.0.1", port=8000)