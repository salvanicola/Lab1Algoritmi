class Arc:
    # Funzione di inizializzazione dell'arco.
    def __init__(self, v1, v2, w):
        self.vert1 = v1
        self.vert2 = v2
        self.weight = w

    # Funzione di accesso al peso dell'arco.
    def weight(self):
        return self.weight


class Graph:
    # Funzione di inizializzazione del grafo.
    def __init__(self):
        self.arch_list = []
        self.vert_list = [None] * 100000
        self.n_vertexes = 0
        self.n_arches = 0

    # Funzione di aggiunta di un arco al grafo.
    def add(self, v1, v2, w):
        self.arch_list.append(Arc(v1, v2, w))
        self.n_arches += 1
        if self.vert_list[v1] is None:
            self.vert_list[v1] = Vertex(v1)
            self.n_vertexes += 1
        if self.vert_list[v2] is None:
            self.vert_list[v2] = Vertex(v2)
            self.n_vertexes += 1

    # Funzione di rimozione di un arco dal grafo.
    def remove(self, arch):
        self.arch_list.remove(arch)
        self.n_arches -= 1


# Funzione di generazione di un grafo a partire da un file fornito in input.
def graph_generator(file):
    n_v = None
    n_a = None
    try:
        fp = open(file, "r")
        lines = fp.readlines()
        if lines.__len__() > 0:
            parsing = lines[0].split(" ")
            graph = Graph()
            n_v = int(parsing[0])
            n_a = int(parsing[1])
            lines.pop(0)
            for x in lines:
                x = x.split(" ")
                graph.add(int(x[0]) - 1, int(x[1]) - 1, int(x[2]))
    finally:
        fp.close()
    if n_a == graph.n_arches and n_v == graph.n_vertexes:
        return graph
    else:
        raise Exception('graph not coherent')


class Vertex:
    # Funzione di inizializzazione di un vertice.
    def __init__(self, i, k=float('inf')):
        self.key = k
        self.parent = None
        self.id = i
        # Flag che indica se il vertice è già stato estratto dallo spanning tree.
        self.flag = False
