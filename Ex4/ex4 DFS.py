#ex 4 dfs


visited = set() 
 
def dfs(visited, graph, node):
    if node not in visited:
        print (node)
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)
            
graph = {
  'A' : ['B','C'],
  'B' : ['D'],
  'C' : ['F'],
  'D' : ['E', 'F'],
  'E' : [],
  'F' : ['A']
} 
 
dfs(visited, graph, 'A')