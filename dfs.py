
# Implementazione iterativa dell'algoritmo DFS, usando le liste di adiacenza.
def dfs_iter(graph, s, visited):
    # Crea uno stack per il DFS.
    stack = list()

    # Inserisce il primo vertice all'interno dello stack.
    stack.append(s)

    while len(stack) != 0:

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
    # Se nessun ciclo è stato trovato, viene ritornato False.
    return False
