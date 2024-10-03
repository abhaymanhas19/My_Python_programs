stack=[]
def push():
    if len(stack)==n:
        print("stack is full")
    else:
        value=int(input("nter the value to push the stack"))
        stack.append(value)
        print(stack)

def pop():
    if len(stack)==0:
        print("stack is empty")
    else:
        stack.pop()
        print(stack)
n=int(input("enter the limit"))

def peek():
    if  not stack:
        print("stack has no value")
    else:
        print("the peek value of stack is :", stack[-1])
while True:
     print("select the operation 1.Push 2.pop 3.peek_value 4.quit")
     choose=int(input())
     if choose==1:
         push()

     elif choose==2:
         pop()

     elif choose==3:
         peek()
     elif choose==4:
         break
     else:
         print("enter the corret input")
#import collections
#stack=collections.deque()
#stack

#import queue
#stack=queue.Lifoqueue()
#print(stack)
#put means push()
#get(value,timeout=1) means pop