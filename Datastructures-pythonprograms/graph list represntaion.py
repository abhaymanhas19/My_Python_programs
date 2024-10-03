def node(v):
    if v in graph:
        print(v,"node is alreay present in graph")
    else:
        graph[v]=[]

def add_edge(v1,v2,cost):
    if v1 not in graph:
        print(v1,"is not present in graph")
    elif v2 not in graph:
        print(v2,"is not present in graph")
    else:
        list=[v2,cost]
        list2=[v1,cost]
        graph[v1].append(list)
        graph[v2].append(list2)

def delete_node(v):
    if v not in graph:
        print(v,"is not present in graph")
    else:
      graph.pop(v)
      for i in graph:
         list=graph[i]
         #if v in list:
          #  list.remove(v)
         for j in list:
             if v==j[0]:
                 list.remove(j)

def delete_edge(v1,v2,cost):
    if v1 not in graph:
        print(v1,"is not present in graph")
    elif v2 not in graph:
        print(v2,'is notpresent in graph')
    else:
        temp=[v2,cost]
        temp2=[v1,cost]
        if temp in graph[v1]:
           graph[v1].remove(temp)
           graph[v2].remove(temp2)


graph={}
node("A")

node("B")
node("C")
add_edge("A","B",5)

add_edge("A","C",41)
print("Before delete")
print(graph)
print("After delete")

delete_edge("A","C",41)
print(graph)
