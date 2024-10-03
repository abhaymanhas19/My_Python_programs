class node:
    def __init__(self,data):
        self.data=data
        self.ref=None
        self.prevref=None

class linkedlist:
    def __init__(self):
        self.head=None

    def print(self):
        if self.head is None:
            print("linked list is empty")
        else:
            n=self.head
            while n is not None:
                print(n.data,"-->",end="")
                n=n.ref

    def print_backward(self):
        if self.head is None:
            print("linked list is empty")

        else:
            n=self.head
            while n.ref is not None:
                n=n.ref
            while n is not None:
                print(n.data,"-->",end="")
                n=n.prevref
    def add(self,data):
        if self.head is None:
           new_node=node(data)
           self.head=new_node
        else:
            print("linked list is not empty")
    def addbegin(self,data):
        new_node=node(data)
        new_node.ref=self.head
        self.head.prevref=new_node
        self.head=new_node

    def add_end(self,data):
        new_node=node(data)
        if self.head is None:
            self.head=new_node
        else:
            n=self.head
            while n.ref is not None:
                n=n.ref
            n.ref=new_node
            new_node.prevref=n


    def delete(self):
        if self.head is None:
            print("linkekd list is empty")
        else:
            self.head=self.head.ref
            self.head.prevref=None



obj=linkedlist()
obj.add(100)
obj.addbegin(300)
obj.add_end(852)
obj.print()
print("\n Backward traverrsal")
obj.print_backward()