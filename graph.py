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
    def __init__(self, v, a):
        self.arch_list = []
        self.vert_list = []
        self.n_vertexes = v
        self.n_arches = a

    # Funzione di aggiunta di un arco al grafo.
    def add(self, v1, v2, w):
        self.arch_list.append(Arc(v1, v2, w))

    # Funzione di rimozione di un arco dal grafo.
    def remove(self, arch):
        self.arch_list.remove(arch)

# Funzione di generazione di un grafo a partire da un file fornito in input.
def graph_generator(file):
    try:
        fp = open(file, "r")
        lines = fp.readlines()
        if lines.__len__() > 0:
            parsing = lines[0].split(" ")
            graph = Graph(int(parsing[0]), int(parsing[1]))
            lines.pop(0)
            for x in range(0, graph.n_vertexes):
                graph.vert_list.append(Vertex(x))
            for x in lines:
                x = x.split(" ")
                graph.add(int(x[0])-1, int(x[1])-1, int(x[2]))
    finally:
        fp.close()
        return graph



class Vertex:
    # Funzione di inizializzazione di un vertice.
    def __init__(self, i, k=float('inf')):
        self.key = k
        self.parent = None
        self.id = i
        # Flag che indica se il vertice è già stato estratto dallo spanning tree.
        self.flag = False
