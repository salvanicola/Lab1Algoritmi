class Arc:
    def __init__(self, v1, v2, w):
        self.vert1 = v1
        self.vert2 = v2
        self.weight = w

    def weight(self):
        return self.weight


class Graph:
    def __init__(self, v, a):
        self.list = []
        self.n_vertexes = v
        self.n_arches = a

    def add(self, v1, v2, w):
        self.list.append(Arc(v1, v2, w))

    def remove(self, arch):
        self.list.remove(arch)


def graph_generator(file):
    try:
        fp = open(file, "r")
        lines = fp.readlines()
        if lines.__len__() > 0:
            parsing = lines[0].split(" ")
            graph = Graph(int(parsing[0]), int(parsing[1]))
            lines.pop(0)
            for x in lines:
                x = x.split(" ")
                graph.add(int(x[0])-1, int(x[1])-1, int(x[2]))
    finally:
        fp.close()
        return graph


class Vertex:
    def __init__(self, i, k=float('inf')):
        self.key = k
        self.parent = None
        self.id = i
        # flag dice se è già stato estratto dallo spanning tree
        self.flag = False
