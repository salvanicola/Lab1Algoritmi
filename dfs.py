def dfs(visited, graph, node):
    cyclic = False
    if node not in visited:
        visited.add(node)
        for neighbour in graph[node]:
            dfs(visited, graph, neighbour)
    else
        cyclic