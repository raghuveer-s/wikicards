from typing import List
import mysql.connector
from .. import settings
from ..model.node import Node

class NodeRepository:
    """
    Data access methods to return one or more specific nodes
    """

    def __init__(self):
        self.db_uri = settings.MYSQL_HOST
        self.db_name = settings.MYSQL_DB
        self.db_user = settings.MYSQL_USER
        self.db_pass = settings.MYSQL_PASS

    def get_unvisited_nodes(self) -> List[Node]:
        """
        Get nodes whose visited time is null
        """

        db = mysql.connector.connect(
            host=self.db_uri, database=self.db_name, user=self.db_user, password=self.db_pass
        )

        cursor = db.cursor()

        query = "select * from node where date_visited is null"
        cursor.execute(query)

        nodes = cursor.fetchall()

        for node in nodes:
            yield Node(*node)
    
    def delete_node_by_url(self, url) -> bool:
        """
        Delete given node by url
        """
        
        db = mysql.connector.connect(
            host=self.db_uri, database=self.db_name, user=self.db_user, password=self.db_pass
        )

        cursor = db.cursor()

        query = "delete from node where url like %s"
        data = (url,)
        cursor.execute(query, data)

        db.commit()

    def delete_node_by_id(self, id) -> bool:
        """
        Delete given node by id
        """
        raise Exception("Not implemented yet.")


class PathRepository:
    """
    Data access methods to get paths
    """

    def get_shortest_paths(self, link_a: str, link_b: str) -> List[Node]:
        return []
