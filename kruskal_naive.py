from collections import deque

from dfs import dfs_iter
from graph import Graph
from merge_sort import mergeSort


def kruskalNaive(G, *args):
    # Inizializzo un grafo vuoto, ovvero con un numero di vertici vuoti uguale a G, per evitare l'uscita dai limiti
    # durante l'assegnazione del valore dei vertici. Viene inoltre convertita la lista di archi a deque, per favorire
    # l'operazione di pop ed aggiunta archi.
    A = Graph(G.n_vertexes)
    A.arch_list = deque()
    # L'algoritmo di merge sort qui utilzzato ha complessità O(n*log(n)), come previsto.
    mergeSort(G.arch_list)
    for e in G.arch_list:
        # Viene aggiunto un arco al grafo dell'MST, solo se non si tratta di un self loop, altrimenti viene ignorato.
        if e.vert1 != e.vert2:
            A.add(e.vert1, e.vert2, e.weight)
            visited = [False] * G.n_vertexes
            # È stato scelto l'algoritmo DFS per il controllo sulla ciclicità del grafo.
            if dfs_iter(A, e.vert1, visited):
                # Qualora il grafo fosse ciclico, viene rimosso l'ultimo arco aggiunto.
                A.pop()
            # Ottimizzazione suggerita a lezione, per una terminazione anticipata dell'algoritmo.
            if A.n_arches == G.n_vertexes - 1:
                break
    return A
