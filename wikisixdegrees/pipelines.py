from itemadapter import ItemAdapter
from wikisixdegrees.items import WikiPageItem
import mysql.connector

class WikiPagesPipeline:
    def __init__(self, db_uri, db_name, db_user, db_pass):
        self.db_uri = db_uri
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

        self.db = mysql.connector.connect(
            host = self.db_uri,
            database = self.db_name,
            user = self.db_user,
            password = self.db_pass
        )
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_uri = crawler.settings.get('MYSQL_URI'),
            db_name = crawler.settings.get('MYSQL_DB'),
            db_user = crawler.settings.get('MYSQL_USER'),
            db_pass = crawler.settings.get('MYSQL_PASS')
        )

    def close_spider(self, spider):
        self.db.close()
        pass
    
    def process_item(self, item:WikiPageItem, spider):
        cursor = self.db.cursor()
        stmt_insert_link = "insert into node (id, url, title, content, date_visited) values(uuid_to_bin(uuid()), %s, %s, %s, %s)"
        data = (item['url'], item['title'], item['content'], item['date_visited'])
        cursor.execute(stmt_insert_link, data)

        self.db.commit()

        cursor.close()

        return item