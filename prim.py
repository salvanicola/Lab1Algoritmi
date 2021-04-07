from heap import FibonacciHeap, Node
from graph import Vertex


def prim(G, s):
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
        n = Node(v.key, v)
        nodes.append(n)
        q.insert(n)

    # per accedere al valore dovremmo utilizzare il campo id,
    # ma per semplificare il tutto si assume che in posizione s ci sia id = s
    vert[s].key = 0
    while q.total_nodes > 0:
        u_node = q.extract_min()
        u = u_node.value
        for v_arch in G.list:
            v_vert = None
            if u.id == v_arch.vert1:
                v_vert = v_arch.vert2
            elif u.id == v_arch.vert2:
                v_vert = v_arch.vert1
            if v_vert is not None and v_arch.flag == False and v_arch.weight < vert[v_vert].key:
                vert[v_vert].parent = u
                vert[v_vert].key = v_arch.weight
                print("culo", q.total_nodes)
                q.decrease_key(nodes[v_vert], v_arch.weight)
                v_arch.flag = True
                print("culo", q.total_nodes)

    print("debuggami sto cazzo!")