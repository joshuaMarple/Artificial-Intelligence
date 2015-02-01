from heapq import *

class unipq():
    
    def hasher(self, item):
        return str(item)

    def __init__(self):
        # self.heap = heapq()
        self.all_items = list()
        
    def add(self, item):
        print(item not in self.all_items)
        if item not in self.all_items:
            # self.heap.add(item)
            heappush(self.all_items, item)

    def pop(self):
        return heappop(self.all_items)
        
    def __contains__(self, item):
        return item in self.all_items

    def show(self):
        for i in self.all_items:
            print(i)

    def empty(self):
        return len(self.all_items) == 0

# test_pq = unipq()
# test_pq.add((5, "test1"))
# test_pq.add((6, "test2"))
# test_pq.add((3, "test3"))
# test_pq.add((100, "test4"))
# test_pq.add((100, "test4"))
# print(test_pq.pop())
# test_pq.show()

