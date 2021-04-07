import math


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        # genitore di Node.
        self.parent = None
        # figlio specifico (dei vari ed eventuali) verso il quale Node ha un riferimento.
        self.child = None
        # fratello sinistro (stesso grado).
        self.left = None
        # fratello destro (stesso grado).
        self.right = None
        # grado del Node.
        self.degree = 0
        # indicatore di marcaggio del Node.
        self.mark = False


class FibonacciHeap:
    # classe Node utilizzata per contenere i valori del singolo nodo ed i puntatori della double linked list. La
    # struttura è standard e contenente: chiave, valore, genitore, (un) figlio, fratello sinistro, fratello destro,
    # grado e marchio.

    # puntatori alla testa della root list ed al suo nodo minimo.
    root_list, min_node = None, None

    total_nodes = 0

    # funzione di iterazione all'interno della double linked list.
    def iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag is True:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right

    # inserisce un elemento in tempo O(1). Questo viene semplicemente inserito nella lista delle roots.
    def insert(self, n):
        n.left = n.right = n
        self.merge_with_root_list(n)
        if self.min_node is None or n.key < self.min_node.key:
            self.min_node = n
        self.total_nodes += 1
        return n

    # inserisce il Node passato come parametro, dopo la head della root list.
    def merge_with_root_list(self, node):
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    # estrae il minimo valore, aggiorna l'heap e lo restituisce.
    def extract_min(self):
        z = self.min_node
        if z is not None:
            if z.child is not None:
                # uniamo il nodi figli alla root list.
                children = [x for x in self.iterate(z.child)]
                for i in range(0, len(children)):
                    self.merge_with_root_list(children[i])
                    children[i].parent = None
            self.remove_from_root_list(z)
            # imposta il nuovo min node nell'heap.
            if z == z.right:
                self.min_node = self.root_list = None
            else:
                self.min_node = z.right
                self.consolidate()
            self.total_nodes -= 1
        return z

    # funzione che combina i Node della root list di ugual grado per consolidare l'heap, tramite la creazione di una
    # lista di alberi binari non ordinati. la variabile "A" è una lista di puntatori di nodi di lunghezza "log(n)",
    # in cui è inserito in posizione "t" il nodo in root list con "rank = t".
    def consolidate(self):
        A = [None] * int(math.log(self.total_nodes) * 2)
        nodes = [w for w in self.iterate(self.root_list)]
        for w in range(0, len(nodes)):
            x = nodes[w]
            d = x.degree
            while A[d] != None:
                y = A[d]
                if x.key > y.key:
                    temp = x
                    x, y = y, temp
                self.heap_link(y, x)
                A[d] = None
                d += 1
            A[d] = x
        # viene ricercato il nuovo nodo minimo, senza necessità di ricostruire la root list, 
        # perchè la root list è stata iterativamente modificata durante lo spostamento dei nodi svolto in precedenza.
        for i in range(0, len(A)):
            if A[i] is not None:
                if A[i].key < self.min_node.key:
                    self.min_node = A[i]

    # dati i nodi "x" e "y", questa funzione rimuove "y" dalla root list e lo aggiunge come figlio di "x",
    # aggiornando gli opportuni attributi.
    def heap_link(self, y, x):
        self.remove_from_root_list(y)
        y.left = y.right = y
        self.merge_with_child_list(x, y)
        x.degree += 1
        y.parent = x
        y.mark = False

    # fuzione per la rimozione di un nodo dalla root list.
    def remove_from_root_list(self, node):
        if node == self.root_list:
            self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left

    # unisce un nodo con la child list di un nodo della root list.
    def merge_with_child_list(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    # metodo che modifica la key di un nodo in tempo costante O(logn).
    def decrease_key(self, x, k):
        if k > x.key:
            return None
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.key < self.min_node.key:
            self.min_node = x

    # metodo che si occupa di spostare un nodo figlio x di y nella root_list.
    def cut(self, x, y):
        self.remove_from_child_list(y, x)
        y.degree -= 1
        self.merge_with_root_list(x)
        x.parent = None
        x.mark = False

    # metodo che effettua un taglio a cascata da y verso l'alto che, se marcato "True", inserisce il nodo in root_list.
    def cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    # metodo che rimuove un nodo dalla child_list
    def remove_from_child_list(self, parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left
