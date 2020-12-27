from typing import Dict, List

import mysql.connector

from .dto import ArticleDTO, TopicDTO

class BaseRepository():
    
    def __init__(self):
        self.db_uri = "127.0.0.1"
        self.db_user = "root"
        self.db_pass = "mysql123"
        self.db_name = "wikidb"

        self.cnx = mysql.connector.connect(
            host=self.db_uri, 
            database=self.db_name,
            user=self.db_user,
            password=self.db_pass
        )

class CleanedContentRepository(BaseRepository):

    def add(self, node_id, content):
        cursor = self.cnx.cursor()
        stmt_insert_article_content = "insert into articles(node_id, content) values(%s, %s)"
        data = (node_id, content)
        cursor.execute(stmt_insert_article_content, data)
        
        self.cnx.commit()
        
        cursor.close()
    
    def save_article_topics(self, article_topics_map:Dict[int, List[TopicDTO]]):
        """
        This method saves (replaces) the existing topics for an article.
        So use it with care as this means it is data / model dependent and can potentially cause model drift.
        """
        cursor = self.cnx.cursor()

        for item in article_topics_map.items():
            article_id = item[0]
            topics = item[1]

            # Remove existing topics for article
            stmt = "delete from topics where article_id = %s"
            data = (article_id,)
            cursor.execute(stmt, data)

            # Insert new topics for the article
            data = []
            for t in topics:
                data.append((article_id, t.topic))
            
            stmt = "insert into topics(article_id, topic) values(%s, %s)"
            cursor.executemany(stmt, data)

        self.cnx.commit()

        cursor.close()

    def get(self):
        pass

    def list(self) -> List[ArticleDTO]:
        cursor = self.cnx.cursor()
        
        cursor.execute("select id, node_id, content from articles")
        
        article_list = []
        for article in cursor.fetchall():
            article = ArticleDTO(id=article[0], node_id=article[1], content=article[2], topics=[])
            article_list.append(article)

        cursor.close()

        return article_list