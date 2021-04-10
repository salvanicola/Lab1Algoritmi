import logging

from heap import FibonacciHeap, Node
from graph import Vertex


def prim(G, s):
    logger = logging.getLogger('tipper')
    logger.debug("ESEGUO prim su grafo con %s vertici e %s archi", G.n_vertexes, G.n_arches)
    vert = []
    nodes = []
    q = FibonacciHeap()
    # assumo che tutti i valori da 0 a n_vertexes - 1 (numero di vertici del grafo) siano tutti gli esatti indici dei
    # vertici
    for x in range(0, G.n_vertexes):
        v = Vertex(x)
        if x == s:
            v.key = 0
        vert.append(v)
        n = Node(v.key, v.id)
        nodes.append(n)
        q.insert(n)

    while q.total_num_elements > 0:
        u_id = q.extract_minimum()
        vert[u_id].flag = True
        v_vert = None
        for v_arch in G.list:
            if v_arch.vert1 == u_id:
                v_vert = v_arch.vert2
            elif v_arch.vert2 == u_id:
                v_vert = v_arch.vert1
            if v_vert is not None and vert[v_vert].flag is False and v_arch.weight < vert[v_vert].key:
                vert[v_vert].parent = nodes[u_id] # questo mi preoccupa
                vert[v_vert].key = v_arch.weight
                q.decrease_key(nodes[v_vert], v_arch.weight)
    logger.debug("FINITO prim su grafo con %s vertici e %s archi.", G.n_vertexes, G.n_arches)
    # print("debuggami!")

    # # per accedere al valore dovremmo utilizzare il campo id,
    # # ma per semplificare il tutto si assume che in posizione s ci sia id = s
    # print("Grafo con vertici:", q.total_num_elements)
    # while q.total_num_elements > 0:
    #     u_id = q.extract_minimum()
    #     for v_arch in G.list:
    #         v_vert = None
    #         if u_id == v_arch.vert1:
    #             v_vert = v_arch.vert2
    #         elif u_id == v_arch.vert2:
    #             v_vert = v_arch.vert1
    #         if v_vert is not None and v_arch.flag == False and v_arch.weight < vert[v_vert].key:
    #             vert[v_vert].parent = nodes[u_id]
    #             vert[v_vert].key = v_arch.weight
    #             q.decrease_key(nodes[v_vert], v_arch.weight)
    #             v_arch.flag = True


