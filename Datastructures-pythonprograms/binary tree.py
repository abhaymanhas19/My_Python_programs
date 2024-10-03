class bt:
    def __init__(self,data):
        self.lt=None
        self.rt=None
        self.data=data
    def insert(self,data):
        if self.data is None:
            self.data =data
            return
    def preorder(self):
        print(self.data,"",end="")
        if self.lt is not None:
            self.lt.preorder()
        if self.rt is not None:
            self.rt.preorder()
    def leftview(self):
        current=self
        while current is  not None:
            print(current.data,"",end="")
            current=current.lt
        return
    def rightview(self):
        current=self
        while current  is not None:
            print(current.data,"",end="")
            current=current.rt
        return
root=bt(None)
root.insert(100)
root.lt=bt(2)
root.rt=bt(1)
root.lt.lt=bt(250)
root.lt.lt.lt=bt(853)
root.lt.rt=bt(85)
print('preorder traversal')
root.preorder()

print("\nleft view ")
root.leftview()

print("\n rightview")
root.rightview()