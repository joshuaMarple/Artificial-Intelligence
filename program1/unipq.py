from heapq import *

class unipq():
    
    def hasher(self, item):
        return str(item)

    def __init__(self):
        self.all_items = list()
        
    def put(self, item):
        if item not in self.all_items:
            heappush(self.all_items, item)

    def get(self):
        return heappop(self.all_items)
        
    def __contains__(self, item):
        return item in self.all_items

    def show(self):
        for i in self.all_items:
            print(i)

    def empty(self):
        return len(self.all_items) == 0
