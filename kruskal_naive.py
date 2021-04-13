import logging

from dfs import dfs
from graph import Graph
from merge_sort import mergeSort


def kruskalNaive(G):
    logger = logging.getLogger('tipper')
    A = Graph(G.n_vertexes)
    mergeSort(G.arch_list)
    for e in G.arch_list:
        A.add(e.vert1, e.vert2, e.weight)
        if A.n_arches == G.n_vertexes - 1:
            break
        else:
            if dfs(A):
                A.pop()
            for x in A.arch_list:
                x.label = None
                A.vert_list[x.vert1].flag = False
                A.vert_list[x.vert2].flag = False
    logger.debug("Kruskal su grafo con %s vertici e %s archi ha terminato", G.n_vertexes, G.n_arches)
    return A



