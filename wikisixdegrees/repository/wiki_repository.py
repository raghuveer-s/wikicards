from typing import List
import mysql.connector
import wikisixdegrees.settings as settings
from wikisixdegrees.model.node import Node

class NodeRepository:
    '''
    Data access methods to return one or more specific nodes
    '''

    def get_unvisited_nodes(self) -> List[Node]:
        '''
        Get nodes whose visited time is null
        '''
        db_uri = settings.MYSQL_HOST
        db_name = settings.MYSQL_DB
        db_user = settings.MYSQL_USER
        db_pass = settings.MYSQL_PASS

        db = mysql.connector.connect(
                host = db_uri,
                database = db_name,
                user = db_user,
                password = db_pass
            )
        
        cursor = db.cursor()

        query = "select * from node where date_visited is null"
        cursor.execute(query)

        nodes = cursor.fetchall()

        for node in nodes:
            yield Node(*node)

class PathRepository:
    '''
    Data access methods to get paths
    '''
    
    def get_shortest_paths(self, link_a:str, link_b:str) -> List[Node]:
        return []
