queue=[]
def push():
    if len(queue)==n:
        print("queue is full")
    else:
        value=int(input("enterr the value"))
        queue.append(value)    #queue.insert(0,value)
        print(queue)

def pop():
    if not queue:
        print("queue is  empty")
    else:
         queue.pop(0)    #queue.pop()
         print(queue)

def show_queue():
    print(queue)

def first_value():
    print(queue[0])

def last_value():
    print(queue[-1])


n=int(input(" enter the limit of the queue"))
while(True):
    print("enter the operation \n 1.push \n 2.pop \n 3.show \n 4.first_value \n 5.last_value \n 6.quit ")
    choice=int(input())
    if choice==1:
        push()
    elif choice==2:
        pop()
    elif choice==3:
        show_queue()
    elif choice==4:
        first_value()
    elif choice==5:
        last_value()
    elif choice==6:
        break

    else:
        print("enter correct operation")


#another methd to implement queue

#import collections
#q=collections.deque()
#print(q)
#appendleft(w)  -- append()
#pop() ============ popleft()


#another method

#import queue
#q=queue.priorityqueue()
#print(q)
#put()
#get()