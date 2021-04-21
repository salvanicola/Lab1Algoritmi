from graph import Graph
from merge_sort import mergeSort


def kruskal(G, *args):
    # Inizializzo un grafo vuoto, ovvero con un numero di vertici vuoti uguale a G, per evitare l'uscita dai limiti
    # durante l'assegnazione del valore dei vertici. Viene inoltre convertita la lista di archi a deque, per favorire
    # l'operazione di pop ed aggiunta archi.
    G.initialize()
    A = Graph(G.n_vertexes)
    # L'algoritmo di merge sort qui utilzzato ha complessità O(n*log(n)), come previsto.
    mergeSort(G.arch_list)
    for e in G.arch_list:
        # Viene aggiunto un arco al grafo dell'MST.
        if e.vert1 != e.vert2:
            r1 = G.find(e.vert1)
            r2 = G.find(e.vert2)
            if r1 != r2:
                A.add(e.vert1, e.vert2, e.weight)
                G.union(r1, r2)
            # Ottimizzazione suggerita a lezione, per una terminazione anticipata dell'algoritmo.
            if A.n_arches == G.n_vertexes - 1:
                break
    return A