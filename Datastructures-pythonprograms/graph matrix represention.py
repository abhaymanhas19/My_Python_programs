def node(v):
    global node_count
    if v in nodes:
        print("this node is already present in graph")
    else:
        node_count=node_count+1
        nodes.append(v)
        for n in graph:
            n.append(0)
        temp=[]
        for i in range(node_count):
            temp.append(0)

        graph.append(temp)
def add_edge(v1,v2,cost):
    if v1 not in nodes:
        print(v1,"node not present")
    elif v2 not in nodes:
        print(v2,"node is not present")
    else:
        index1=nodes.index(v1)
        index2=nodes.index(v2)
        graph[index1][index2]=cost
        graph[index2][index1]=cost

def delete_node(v):
    global node_count
    if v not in nodes:
        print(v, " is not present in nodes")
    else:

        index=nodes.index(v)
        node_count=node_count-1
        nodes.remove(v)
        graph.pop(index)
        for n in graph:
            n.pop(index)



def delete_edge(v1,v2):
    if v1 not in nodes:
        print(v1,"not present in nodes")

    elif v2 not in nodes:
        print(v2,"not present in list")
    else:
        index=nodes.index(v1)
        index2=nodes.index(v2)
        graph[index][index2]=0
        graph[index2][index]=0



def print_matrix():
    for i in range(node_count):
        for j in range(node_count):
            print(format(graph[i][j],"<3"),"" ,end="  ")
        print()
nodes=[]
graph=[]
node_count=0


print("before adding nodes")
print(nodes)
print(graph)

print("After adding nodes")
node("A")
node("B")
node("C")
node("D")
print(nodes)

add_edge("A","B",10)
add_edge("C","C",5)
print_matrix()
print("after delete node")

delete_node("C")
add_edge("B","D",5)


print(nodes)
print_matrix()
