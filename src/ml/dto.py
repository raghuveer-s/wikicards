# NOTE: Currently abusing this by also using it as an "entity"... 
# Oh well.

class ArticleDTO:
    def __init__(self, id, node_id, content, topics):
        self.id = id
        self.node_id = node_id
        self.content = content
        self.topics = []

class TopicDTO:
    def __init__(self, id, article_id, topic):
        self.id = id
        self.article_id = article_id
        self.topic = topic