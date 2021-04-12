import logging

from dfs import dfs
from graph import Graph
from merge_sort import mergeSort


def kruskalNaive(G):
    logger = logging.getLogger('tipper')
    logger.debug("ESEGUO Kruskal su grafo con %s vertici e %s archi", G.n_vertexes, G.n_arches)
    A = Graph(G.n_vertexes)
    mergeSort(G.arch_list)
    for e in G.arch_list:
        B = Graph(G.n_vertexes)
        B.deepcopy(A, G.n_vertexes)
        B.add(e.vert1, e.vert2, e.weight)
        if B.n_arches == G.n_vertexes - 1:
            A.deepcopy(B, G.n_vertexes)
            break
        else:
            if not dfs(B):
                A.deepcopy(B, G.n_vertexes)
    return A



