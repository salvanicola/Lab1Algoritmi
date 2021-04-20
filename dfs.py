from collections import deque

import logging


# def DFSUtil(self, s, visited):
#     # Create a stack for DFS
#     stack = []
#
#     # Push the current source node.
#     stack.append(s)
#
#     while (len(stack) != 0):
#
#         # Pop a vertex from stack and print it
#         s = stack.pop()
#
#         # Stack may contain same vertex twice.
#         # So we need to prthe popped item only
#         # if it is not visited.
#         if not visited[s]:
#             visited[s] = True
#
#         # Get all adjacent vertices of the
#         # popped vertex s. If a adjacent has not
#         # been visited, then push it to the stack.
#         i = 0
#         while i < len(self.adj[s]):
#             if not visited[self.adj[s][i]]:
#                 stack.append(self.adj[s][i])
#             i += 1

# prints all vertices in DFS manner
# def DFS(graph):
#     # Mark all the vertices as not visited
#     visited = [False] * graph.n_vertexes
#     for i in range(graph.n_vertexes):
#         if not visited[i]:
#             DFSUtil(graph, i, visited)

# Implementazione iterativa dell'algoritmo DFS, usando le liste di adiacenza.
def dfs_iter(graph, s, visited):
    # Crea uno stack per il DFS.
    stack = []

    # Inserisce il primo vertice all'interno dello stack.
    stack.append(s)

    while (len(stack) != 0):

        # Elimina l'ultimo elemento dallo stack e lo ritorna.
        s = stack.pop()

        # Se il vertice ottenuto non è stato visitato, viene marchiato come tale.
        # Altrimenti è stato trovato un ciclo, quindi l'operazione si ferma.
        if not visited[s]:
            visited[s] = True
        else:
            return True

        # Esamina tutti i vertici adiacenti a quello attuale (s), e se uno di essi
        # non è stato ancora visitato, questi viene aggiunto in fondo allo stack.
        for n in graph.adj[s]:
            if not visited[n[0]]:
                stack.append(n[0])
            elif n[0] == s:
                return True
    # Se nessun ciclo è stato trovato, viene ritornato False.
    return False


# # Funzione per l'iterazione su tutte le componenti connesse del grafo dato.
# def dfs(graph, n_vertexes):
#     # Inizializzazione di un array di bool, che indica se il vertice corrispondente
#     # all'indice è stato visitato (inizialmente False).
#     visited = [False] * n_vertexes
#     for i in range(graph.n_vertexes):
#         # In Kruskal il grafo ha una lista di vertici contenente possibilmente dei valori None.
#         # Controlliamo quindi per tale eventualità.
#         if graph.vert_list[i] is not None:
#             if not visited[i]:
#                 if dfs_iter(graph, i, visited):
#                     # Se viene trovato un ciclo anche in una sola componente connessa,
#                     # l'operazione si interrompe e ritorna True.
#                     return True
#     # Se nessun ciclo è stato trovato, viene ritornato False.
#     return False

# def dfs(graph, n_vertex):
#     visited_v = [False] * n_vertex
#     for i in range(graph.n_vertexes):
#         if graph.vert_list[i] is not None:
#             if visited_v[i] is False:
#                 if dfs_iter(graph, i, visited_v) is True:
#                     return True
#     return False
#
#
# def dfs_iter(graph, s, visited_v):
#     stack = deque()
#     stack.append(s)
#     while len(stack) != 0:
#         s = stack.pop()
#
#         if not visited_v[s]:
#             visited_v[s] = True
#         else:
#             return True
#
#         i = 0
#         while i < len(graph.adj[s]):
#             if not visited_v[graph.adj[s][i]]:
#                 stack.append(graph.adj[s][i])
#             i += 1
#     return False

# while len(stack):
#     s = stack.pop()
#     visited_v[s] = True
#     for x in graph.arch_list:
#         if x.label is None:
#             opposite = None
#             if x.vert1 == s.id:
#                 opposite = graph.vert_list[x.vert2]
#             elif x.vert2 == s.id:
#                 opposite = graph.vert_list[x.vert1]
#             if opposite is not None:
#                 if opposite.flag is False:
#                     x.label = "discovery"
#                     opposite.flag = True
#                     stack.append(opposite)
#                 else:
#                     return True

# def dfs_rec(graph, vert, checker, out=False):
#     vert.flag = not checker
#     for arch in graph.arch_list:
#         if arch.label is checker:
#             opposite = None
#             if arch.vert1 == vert.id:
#                 opposite = graph.vert_list[arch.vert2]
#             elif arch.vert2 == vert.id:
#                 opposite = graph.vert_list[arch.vert1]
#             if opposite is not None:
#                 if opposite.flag is checker:
#                     arch.label = not checker
#                     if dfs_rec(graph, opposite, checker) is True:
#                         out = True
#                 else:
#                     out = True
#     return out