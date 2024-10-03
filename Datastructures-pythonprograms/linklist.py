class node:
    def __init__(self,data):
        self.data=data
        self.ref=None
class linkedlist():
    def __init__(self):
        self.head=None

    def print_ll(self):
        if self.head is None:
            print("linked list is empty")
        else:
            n=self.head
            while n is not None:
                print(n.data,"--->",end="")
                n=n.ref

    def add_begin(self,data):
            new_node=node(data)
            new_node.ref=self.head
            self.head=new_node

    def add_end(self,data):
        new_node=node(data)
        if self.head is None:
              self.head=new_node
        else:
            n=self.head
            while n.ref is  not  None:
                n=n.ref
            n.ref=new_node

    def add_after(self,data,x):
        n=self.head
        while n is not None:
            if x==n.data:
                break
            n=n.ref
        if n is None:
            print("node is not present is linked list")
        else:
            new_node=node(data)
            new_node.ref=n.ref
            n.ref=new_node
    def add_before(self,data,x):
        n=self.head
        while n.ref is not None:
            if x==n.ref.data:
                break
            n=n.ref
        if n.ref is None:
            print("node is not present is linked list")
        else:
            new_node=node(data)
            new_node.ref=n.ref
            n.ref=new_node

    def insert_empty(self,data):
        if self.head is None:
            new_node=node(data)
            self.head=new_node
        else:
            print("linked list not empty")
    def  delete_begin(self):
        if self.head is None:
            print("linked list is empty we can not perform delete operration")
        else:
            self.head=self.head.ref
    def delete_end(self):
         if self.head is None:
             print("linked list is empty")
         elif self.head.ref is None:
             self.head =self.head.ref
         else:
             n=self.head
             while n.ref.ref is not None:
                 n=n.ref
             n.ref=None
    def delete_by_value(self,x):
        if self.head is None:
            print('linked list is empty')
        elif x==self.head.data:
            self.head=self.head.ref
        else:
            n=self.head
            while n.ref is not None:
                if x==n.ref.data:
                    break
                n=n.ref
            if n.ref is None:
                print("the element is present in linked list")
            else:
                n.ref=n.ref.ref

    def search(self,data):
        if self.head  is None:
            print("linked list is empty")
            return

        n=self.head
        while n.ref is not None:
            if data==n.data:
                print("\nelement is found")
                break
            n=n.ref
        else:
            print("\nelement not found")


obj=linkedlist()
obj.add_begin(74)
obj.add_end(72)
obj.add_begin(85)
obj.add_after(85,72)
obj.add_after(102,74)
obj.add_before(45,85)

obj.add_end(102)
obj.print_ll()
obj.search(102)



