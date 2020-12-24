import mysql.connector

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

    def get(self):
        pass

    def list(self):
        cursor = self.cnx.cursor()
        
        cursor.execute("select content from articles")
        article_list = cursor.fetchall()
        cursor.close()

        return article_list