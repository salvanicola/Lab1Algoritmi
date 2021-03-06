class Arc:
    # Funzione di inizializzazione dell'arco.
    def __init__(self, v1, v2, w):
        self.vert1 = v1
        self.vert2 = v2
        self.weight = w
        self.label = None

    # Funzione di accesso al peso dell'arco.
    def weight(self):
        return self.weight

    # Funzione per l'ottenimento del vertice opposto a quello dato, all'interno di un arco.
    def opposite(self, s):
        if self.vert1 == s:
            return self.vert2
        if self.vert2 == s:
            return self.vert1
        return None

class Vertex:
    # Funzione di inizializzazione di un vertice.
    def __init__(self, i, k=float('inf')):
        self.key = k
        self.parent = None
        self.id = i
        # Flag che indica se il vertice è già stato estratto dallo spanning tree.
        self.flag = False
        # Campo che indica il numero di vertici presenti nel sotto-albero di cui è radice, utilizzato nella Union-Find
        self.size = 1

    # Funzione di utility per Union-Find che definisce se un vertice é una root.
    def is_root(self):
        return self.parent == self.id

class Graph:
    # Funzione di inizializzazione del grafo.
    def __init__(self, n_v):
        self.arch_list = []
        self.vert_list = [None] * n_v
        self.n_vertexes = 0
        self.n_arches = 0
        self.adj = [None] * n_v

    # Funzione di aggiunta di un arco al grafo.
    def add(self, v1, v2, w):
        # Vengono aggiunti i vertici ed inizializzate le liste di adiacenza.
        if self.vert_list[v1] is None:
            self.adj[v1] = set()
            self.vert_list[v1] = Vertex(v1)
            self.n_vertexes += 1
        if self.vert_list[v2] is None:
            self.adj[v2] = set()
            self.vert_list[v2] = Vertex(v2)
            self.n_vertexes += 1
        # Viene aggiunto l'arco dato in input.
        self.arch_list.append(Arc(v1, v2, w))
        self.n_arches += 1
        # Vengono aggiornate le liste di adiacenza.
        self.adj[v1].add((v2, w))
        self.adj[v2].add((v1, w))

    # Funzione per l'eliminazione dell'ultimo arco nella lista degli archi. Vengono gestiti anche gli effetti
    # collaterali sulle liste di adiacenza e di vertici.
    def pop(self):
        last = self.arch_list.pop()
        self.n_arches -= 1
        if self.vert_list[last.vert1] is not None:
            self.adj[last.vert1].remove((last.vert2, last.weight))
            if len(self.adj[last.vert1]) == 0:
                self.vert_list[last.vert1] = None
        if self.vert_list[last.vert2] is not None:
            self.adj[last.vert2].remove((last.vert1, last.weight))
            if len(self.adj[last.vert2]) == 0:
                self.vert_list[last.vert2] = None

    # Funzione per l'inserimento del nodo y come figlio del nodo x.
    def union(self, i, j):
        iv = self.vert_list[i]
        jv = self.vert_list[j]
        # Verifica sei vertici sono entrambi root (secondo Union-find), e in caso positivo
        # pone quello con grado maggiore come "parent" dell'altro.
        if iv.is_root() and jv.is_root():
            if iv.size >= jv.size:
                self.vert_list[j].parent = i
                iv.size = iv.size + jv.size
            else:
                self.vert_list[i].parent = j
                jv.size = iv.size + jv.size

    # Funzione utilizzata per trovare la radice dell'albero a partire da s.
    def find(self, s):
        while self.vert_list[s].parent is not self.vert_list[s].id:
            s = self.vert_list[s].parent
        return s

    # Funzione di inizializzazione dell'Union-find, pone tutti i campi "parent" dei vertici
    # equivalenti all'id del vertice stesso.
    def initialize(self):
        for v in self.vert_list:
            v.parent = v.id

    # Funzione che ritorna la somma dei pesi di tutti gli archi del grafo.
    def graph_total_weight(self):
        return sum(x.weight for x in self.arch_list)


# Funzione di generazione di un grafo a partire da un file fornito in input.
def graph_generator(file):
    n_v = None
    n_a = None
    try:
        fp = open(file, "r")
        lines = fp.readlines()
        if lines.__len__() > 0:
            parsing = lines[0].split(" ")
            n_v = int(parsing[0])
            n_a = int(parsing[1])
            graph = Graph(n_v)
            lines.pop(0)
            for x in lines:
                x = x.split(" ")
                graph.add(int(x[0]) - 1, int(x[1]) - 1, int(x[2]))
    finally:
        fp.close()
    if n_a == graph.n_arches and n_v == graph.n_vertexes:
        return graph
    else:
        raise Exception('Grafo non coerente.')
