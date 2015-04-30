from heapq import *

class unipq():
    
    def hasher(self, item):
        return str(item)

    def __init__(self):
        self.all_items = list()
        self.checker = {}
        
    def put(self, item):
        try:
            self.checker[self.hasher(item)] == True
        except KeyError:
            heappush(self.all_items, item)
            self.checker[self.hasher(item)] = True

    def get(self):
        tmp = heappop(self.all_items)
        del self.checker[self.hasher(tmp)]
        return tmp
        
    def __contains__(self, item):
        try:
            return self.checker[self.hasher(item)]
        except KeyError:
            return False

    def show(self):
        for i in self.all_items:
            print(i)

    def empty(self):
        return len(self.all_items) == 0
