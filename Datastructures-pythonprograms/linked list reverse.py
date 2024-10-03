class node():
    def __init__(self,data):
        self.data=data
        self.next=None

class linkedlist():
    def __init__(self):
        self.head=None

    def print(self):
        if self.head is None:
            print("linked list is empty")
        else:
            current=self.head
            while current is not None:
                print(current.data,"--->",end="")
                current =current.next
    def add(self,data):
        new_node=node(data)
        if self.head is None:
            self.head=new_node

        else:
            current =self.head
            while current.next is not None:
                current =current.next
            current.next=new_node

    def reverse(self):
        previous=None
        current=self.head
        while current is not None:
            n=current.next
            current.next=previous
            previous=current
            current=n
        self.head = previous
obj=linkedlist()
print("the linked list is :")
obj.add(100)
obj.add(200)
obj.add(300)
obj.print()

print("\nthe reverse linked list is:")
obj.reverse()
obj.print()
