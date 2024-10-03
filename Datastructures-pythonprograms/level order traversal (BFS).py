
class tree():
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def levelorder_traverrsal(self):
        if self is None:
            return
        queue=[]

        queue.append(self)
        while(len(queue)>0):
            print(queue[0].data)
            node=queue.pop(0)
            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)
        return

root=tree(100)
root.left=tree(50)
root.right=tree(96)
root.left.left=tree(85)
root.left.right=tree(96)
root.levelorder_traverrsal()