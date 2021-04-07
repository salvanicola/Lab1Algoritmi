from heap import FibonacciHeap
from graph import Vertex


def prim(G, s):
    vert = []
    q = FibonacciHeap()
    # assumo che tutti i valori da 0 a n_vertexes - 1 (numero di vertici del grafo) siano tutti gli esatti indici dei
    # vertici
    for x in range(0, G.n_vertexes - 1):
        v = Vertex(x)
        if x == s:
            v.key = 0
        vert.append(v)
        q.insert(v.key, v)

    # per accedere al valore dovremmo utilizzare il campo id, ma per semplificare il tutto si assume che in posizione s ci sia id = s
    vert[s].key = 0

    print("debuggami sto cazzo!")
    while q.total_nodes > 0:
        u = q.extract_min().value
        for v_arch in G.list:
            v_vert = None
            if u == v_arch.vert1:
                v_vert = v_arch.vert2
            elif u == v_arch.vert2:
                v_vert = v_arch.vert1
            if v_vert is not None and v_arch.flag == False and v_arch.weight < v_vert.key:
                vert[v_vert.id].parent = u
                vert[v_vert.id].key = v_arch.weight
                # UPDATE THE FIBONACCI HEAP KEY IN O(LOGN)
