def add_node(v):
    if v in graphs:
        print(v,"is already present in graphs")
    else:
        graphs[v]=[]
def add_edge(v1,v2):
    if v1 not in graphs:
        print(v1,"is not present in graph")
    elif v2 not in graphs:
        print(v2,"is not present in graph ")
    else:

        graphs[v1].append(v2)
        graphs[v2].append(v1)
'''
def dfs(node,visited,graphs):
    if node not in visited:
        print(node)
        visited.add(node)
        for i in graphs[node]:
            dfs(i,visited,graphs)
'''
def dfsiterative(node,graphs):
    visited=set()
    stack=[]
    if node not  in graphs:
        print(node,"cuurent node not present")
        return
    stack.append(node)
    while stack:
        current = stack.pop()
        if current not in visited:
            print(current)
            visited.add(current)
            for i in graphs[current]:
                    stack.append(i)





#visited=set()
graphs={}
add_node("A")
add_node("B")
add_node("C")
add_edge("A","C")
add_edge("A","B")
add_edge("B","C")

print(graphs)
dfsiterative("A",graphs)