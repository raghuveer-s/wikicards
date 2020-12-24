import logging

from typing import List

# configure logging
logger = logging.getLogger("machine-learning")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logfile.log")
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def train():
    from ml.train import calculate_lsa
    from ml.repository import CleanedContentRepository

    articles = CleanedContentRepository().list()
    calculate_lsa(articles)

def get_topics(document) -> List:
    return []

def get_recommendations(document) -> List:
    return []