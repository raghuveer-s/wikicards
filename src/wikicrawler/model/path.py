from typing import List
from .node import Node


class Path:
    nodes = []

    def __init__(self, nodes: List[Node]):
        self.nodes = nodes