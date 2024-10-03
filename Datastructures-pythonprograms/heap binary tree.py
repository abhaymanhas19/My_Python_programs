#binary heap is a heap data struucture that follow properties of complete binary tree and follow heap
#property . it is mainly used for priority queue.heapq follow min heap property.
import heapq
list=[]
heapq.heappush(list,5)
heapq.heappush(list,85)
heapq.heappush(list,2)
heapq.heappush(list,6)
print(list)
heapq.heappop(list)
print(list)

heap=[8,5,4,6,7,23]
heapq.heapify(heap)
heapq.heappop(heap)
heapq.heappop(heap)
heapq.heappop(heap)
heapq.heappop(heap)
print(heap)