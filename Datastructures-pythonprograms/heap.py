# In Python, heaps are a special kind of binary tree that are often implemented using lists. 
# They are mainly used for efficient retrieval of the smallest (or largest) element.

# import heapq

# nums = [5, 3, 8, 4, 1, 9, 6]
# heapq.heapify(nums)   # convert list into a min heap
# print(nums) 

# print(heapq.heappop(nums))  # pops smallest element (1)
# print(heapq.heappop(nums)) 
# print(heapq.heappop(nums))  # pops smallest element (1)
# print(heapq.heappop(nums)) 


# import heapq

# nums = [5, 3, 8, 4, 1, 9, 6]
# max_heap = [-n for n in nums]
# heapq.heapify(max_heap)
# print(max_heap)
# print(-heapq.heappop(max_heap))  # pops largest element (9)
# print(-heapq.heappop(max_heap))  # 

try:
    a="23"
    print(a)
    x = a/3
except (NameError,Exception) as e:
    print(e)