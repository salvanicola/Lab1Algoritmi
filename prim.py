from heap import FibonacciHeap, Node
from graph import Vertex


def prim(G, s):
    # Inizializzazione di una semplice progress bar per verificare l'operazione in corso.
    # with progressbar.ProgressBar(G.n_vertexes) as bar:
    vert = []
    nodes = []
    q = FibonacciHeap()
    # Assumiamo che tutti i valori da 0 a n_vertexes - 1 (numero di vertici del grafo) siano tutti gli esatti indici
    # dei vertici.

    # Inizializza gli array ed il Fibonacci Heap con dei valori di base.
    for x in range(0, G.n_vertexes):
        v = Vertex(x)
        if x == s:
            v.key = 0
        vert.append(v)
        n = Node(v.key, v.id)
        nodes.append(n)
        q.insert(n)

    # Viene iterato un ciclo while, fino a che non vengono esauriti tutti gli elementi del Fibonacci Heap.
    while q.total_num_elements > 0:
        # u_id è l'indice di un light edge per l'algoritmo.
        u_id = q.extract_minimum()
        vert[u_id].flag = True
        # Vengono esaminati tutti i vertici adiacenti al vertice identificato da u_id.
        for v_arch in G.adj[u_id]:
            v_vert = v_arch[0]
            if vert[v_vert].flag is False and v_arch[1] < vert[v_vert].key:
                # Se verificate le condizioni, il vertice viene inserito nel corretto indice della lista vert,
                # diventando componente del MST da restituire a fine ciclo.
                vert[v_vert].parent = nodes[u_id]
                vert[v_vert].key = v_arch[1]
                # Viene aggiornata la chiave del vertice all'interno del Fibonacci Heap con il valore dell'arco
                # preso in esame.
                q.decrease_key(nodes[v_vert], v_arch[1])
    return vert
