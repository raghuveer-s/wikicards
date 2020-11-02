import logging
import hashlib
import traceback

from itemadapter import ItemAdapter
from scrapy.link import Link
from wikisixdegrees.items import WikiPageItem
import mysql.connector


class WikiPagesPipeline:
    def __init__(self, db_uri, db_name, db_user, db_pass):
        self.db_uri = db_uri
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

        self.db = mysql.connector.connect(
            host=self.db_uri,
            database=self.db_name,
            user=self.db_user,
            password=self.db_pass,
        )

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_uri=crawler.settings.get("MYSQL_URI"),
            db_name=crawler.settings.get("MYSQL_DB"),
            db_user=crawler.settings.get("MYSQL_USER"),
            db_pass=crawler.settings.get("MYSQL_PASS"),
        )

    def close_spider(self, spider):
        self.db.close()
        pass

    def process_item(self, item: WikiPageItem, spider):
        cursor = self.db.cursor()

        # Moved id generation from database side to server side due to edge referencing it
        item["url"] = item["url"].lower()
        m = hashlib.md5()
        m.update(bytes(item["url"], "utf-8"))
        node_a_id = m.hexdigest()

        stmt_insert_node = "insert ignore into node (id, url, title, content, date_visited) values(%s, %s, %s, %s, %s)"
        data = (
            node_a_id,
            item["url"],
            item["title"],
            item["content"],
            item["date_visited"],
        )
        cursor.execute(stmt_insert_node, data)

        self.db.commit()

        # If item has been followed, it should have outgoing links
        # There should only be 1 edge from this node to an outgoing node

        outgoing_urls = set()

        try:
            if item["followed"] == True and item["outgoing_links"] is not None:
                for link in item["outgoing_links"]:
                    link.url = link.url.lower()
                    outgoing_urls.add(link.url)

            for url in outgoing_urls:
                m = hashlib.md5()
                m.update(bytes(url, "utf-8"))
                node_b_id = m.hexdigest()

                # no cycles of length 1
                if node_a_id == node_b_id:
                    continue

                stmt_insert_node = "insert ignore into node(id, url) values(%s, %s)"
                data = (node_b_id, url)
                cursor.execute(stmt_insert_node, data)

                self.db.commit()

                print(node_a_id, node_b_id, item["url"], url)
                stmt_insert_edge = "insert into edge(a, b) values(%s, %s)"
                data = (node_a_id, node_b_id)
                cursor.execute(stmt_insert_edge, data)

                self.db.commit()
        except Exception as e:
            # logging.error(traceback.format_exc())
            print(traceback.format_exc())

        self.db.commit()

        cursor.close()

        return item