class bst:
    def __init__(self,data):
        self.data=data
        self.lefttree=None
        self.righttree=None

    def insert(self,data):
        if self.data is None:
            self.data=data
            return
        if self.data==data:
            return
        if self.data>data:
            if self.lefttree is None:
                self.lefttree=bst(data)
            else:
                self.lefttree.insert(data)
        else:
            if self.righttree is None:
                self.righttree=bst(data)
            else:
                self.righttree.insert(data)

    def search(self,data):
        if self.data is None:
            print("tree has no value")
            return
        if self.data==data:
            print("element is found")
            return
        if self.data>data:
            if self.lefttree is None:
                print("element is not found ")
            else:
                self.lefttree.search(data)
        else:
            if self.righttree is None:
                print("element is not found")
            else:
                self.righttree.search(data)
    def preorder(self):
        print(self.data,"",end="")
        if self.lefttree is not None:
            self.lefttree.preorder()
        if self.righttree is not None:
            self.righttree.preorder()

    def inorder(self):
        if self.lefttree is not None:
            self.lefttree.inorder()
        print(self.data,"",end="")
        if self.righttree is not None:
            self.righttree.inorder()

    def postorder(self):
        if self.lefttree is not None:
            self.lefttree.postorder()
        if self.righttree is not None:
            self.righttree.postorder()
        print(self.data,"",end="")
    def delete(self,data):
        if self.data is None:
            print("tree is empty")
            return
        if self.data>data:
            if self.lefttree is None:
                print("elemwnt is not present ")
            else:
                self.lefttree=self.lefttree.delete(data)
        elif self.data< data:
            if self.righttree is None:
                print("eelement is not present ")
            else:
                self.righttree=self.righttree.delete(data)
        else:
            if self.lefttree is None:
                temp=self.righttree
                self.data=None
                return temp
            if self.righttree is None:
                temp=self.lefttree
                self.data=None
                return temp
            node=self.righttree
            while node.righttree is not None:
                node=node.lefttree
            self.data=node.data
            self.righttree=self.righttree.delete(node.data)
            return self.data
def count(node):
    if node is None:
        return 0
    return 1+count(node.lefttree)+count(node.righttree)
root=bst(None)
list=[5,75,25,24,4,1,3]
for x in list:
    root.insert(x)
print(" the element in tree is :",count(root))
if count(root)>1:
    root.delete(24)
else:
    print("canit perform delete operation")
print("preorder traversal ")
root.preorder()
print(" inorder traversal")
root.inorder()
print("post order ")
root.postorder()