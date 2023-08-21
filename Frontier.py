
from Node import *
from collections import deque

class BFSFrontier:
    def __init__(self):
        self.queue = deque()
            
    # Insert a node
    def insert(self, node) -> None:
        self.queue.append(node)
    
    # Pop a state, or tell me if the Frontier is empty
    def next(self) -> Node:
        return self.queue.popleft()
    
    def size(self) -> int:
        return len(self.queue)