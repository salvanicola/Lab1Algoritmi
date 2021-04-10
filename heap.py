# Classe di rappresentazione di un nodo del Fibonacci Heap.
class Node:
    def __init__(self, value, id):
        # Valore della key del nodo.
        self.value = value
        # ID del vertice associato al nodo.
        self.id = id
        # Puntatore al nodo parent.
        self.parent = None
        # Puntatore al primo figlio nella lista dei figli.
        self.child = None
        # Puntatore al nodo sinistro.
        self.left = None
        # Puntatore al nodo destro.
        self.right = None
        # Grado del nodo - numero di figli.
        self.deg = 0
        # Marcatura del nodo, utilizzata da alcune operazioni specifiche.
        self.mark = False

class FibonacciHeap:
    # Puntatore ad un elemento della lista doppiamente linkata e circolare di componenti dell'heap.
    # Agisce come testa e riferimento all'intera struttura heap.
    root_list = None
    # Puntatore al nodo contenente il minimo elemento nell'heap.
    min_node = None
    # Numero totale di nodi all'interno dell'intero heap.
    total_num_elements = 0

    # Funzione per l'iterazione attraverso la lista di nodi fornita (può essere una root list come una child list).
    # Ci si muoverà attraverso i figli destri nella lista fino a raggiungere nuovamente il nodo di partenza.
    def iterate(self, head=None):
        if head is None:
            head = self.root_list
        current = head
        while True:
            yield current
            if current is None:
                break
            current = current.right
            if current == head:
                break

    # Funzione per l'inserimento di un nuovo nodo all'interno dell'heap. Il nodo deve essere costruito all'esterno
    # della struttura heap. Questa funzione crea un nuovo heap di un elemento ed effettua il merge di quest'ultimo con
    # l'heap di partenza, il tutto in tempo costante O(1).
    def insert(self, node):
        # Create a new singleton tree
        node.left = node.right = node
        # Add to root list
        self.meld_into_root_list(node)
        # Update min pointer (if necessary)
        if self.min_node is not None:
            if self.min_node.value > node.value:
                self.min_node = node
        else:
            self.min_node = node
        self.total_num_elements += 1
        return node

    # Funzione per l'estrazione del minimo elemento dall'heap, gestita in vari passi. Primo, viene preso il nodo contenente
    # il minimo elemento e lo rimuove. I suoi figli diventano radici di nuovi alberi. Se il numero di figli era d, è necessario
    # tempo O(d) per processare tutte le nuove root ed il potenziale aumento di d-1. Quindi, il tempo di esecuzione ammortizzato
    # di questa fase è O(d) = O(log n).
    def extract_minimum(self):
        m = self.min_node
        if m is None:
            raise ValueError('Il Fibonacci heap è vuoto, non è possibile estrarre il minimo.')
        if m.child is not None:
            # Inserisce i figli nella root list.
            children = [x for x in self.iterate(m.child)]
            for i in range(0, len(children)):
                self.meld_into_root_list(children[i])
                children[i].parent = None
        # Elimina il nodo minimo.
        self.remove_from_root_list(m)
        self.total_num_elements -= 1
        # Consolida (tramite la funzione consolidate) gli alberi, in modo tale che nessuna root abbia lo stesso rank.
        self.consolidate()
        # Aggiorna il nodo minimo.
        if m == m.right:
            self.min_node = None
            self.root_list = None
        else:
            self.min_node = self.find_min_node()
        return m.id

    # Funzione per la riduzione del valore della chiave di un nodo, e se la proprietà dell'heap viene violata (la nuova chiave
    # è minore di quella del suo parent), viene effettuato il cut (eventualmente ricorsivo) del nodo dai suoi parent.
    def decrease_key(self, node, v):
        if v >= node.value:
            raise ValueError("Non è possibile ridurre la chiave con un velore maggiore di quello attuale.")
        node.value = v
        p = node.parent
        if p is not None and node.value < p.value:
            self.cut(node, p)
            self.cascading_cut(p)
        if node.value < self.min_node.value:
            self.min_node = node
        return

    # Funzione per il cut di un nodo dai suoi parent, rimuovendolo quindi dalla lista di figli ed inserendolo in root list.
    def cut(self, node, parent):
        self.remove_from_child_list(parent, node)
        parent.deg -= 1
        self.meld_into_root_list(node)
        node.parent = None
        node.mark = False

    # Funzione per l'esecuzione del controllo del mark ed eventuale cut del parent del nodo fornito.
    def cascading_cut(self, node):
        p = node.parent
        if p is not None:
            if p.mark is False:
                p.mark = True
            else:
                self.cut(node, p)
                self.cascading_cut(p)


    # Funzione per l'unione di un nodo con la root list tramite la sua aggiunta nella seconda posizione della lista.
    def meld_into_root_list(self, node):
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    # Funzione per l'eliminazione di un nodo dalla root list.
    def remove_from_root_list(self, node):
        if self.root_list is None:
            raise ValueError('Heap vuoto')
        if self.root_list == node:
            # Check if there's only one element in the list
            if self.root_list == self.root_list.right:
                self.root_list = None
                return
            else:
                self.root_list = node.right
        node.left.right = node.right
        node.right.left = node.left
        return

    # Funzione per la rimozione di un nodo dalla lista di figli
    def remove_from_child_list(self, parent, node):
        if parent.child == parent.child.right:
            parent.child = None
        elif parent.child == node:
            parent.child = node.right
            node.right.parent = parent
        node.left.right = node.right
        node.right.left = node.left

    # Funzione per il controllo e la revisione del tree, per fare in modo che nessuna root abbia lo stesso grado.
    def consolidate(self):
        if self.root_list is None:
            return
        ranks_mapping = [None] * self.total_num_elements
        nodes = [x for x in self.iterate(self.root_list)]
        for node in nodes:
            degree = node.deg
            while ranks_mapping[degree] != None:
                other = ranks_mapping[degree]
                if node.value > other.value:
                    node, other = other, node
                self.merge_nodes(node, other)
                ranks_mapping[degree] = None
                degree += 1
            ranks_mapping[degree] = node
        return

    # Funzione per l'unione di due nodi, inserendo il nodo con chiave maggiore come figlio di un altro nodo.
    def merge_nodes(self, node, other):
        self.remove_from_root_list(other)
        other.left = other.right = other
        # Adding other node to child list of the frst one.
        self.merge_with_child_list(node, other)
        node.deg += 1
        other.parent = node
        other.mark = False
        return

    # Funzione che unisce un nodo con la lista dei figli di un nodo root.
    def merge_with_child_list(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    # Funzione che itera attraverso l'intera lista (child o root) e trova il nodo minimo.
    def find_min_node(self):
        if self.root_list is None:
            return None
        else:
            min = self.root_list
            for x in self.iterate(self.root_list):
                if x.value < min.value:
                    min = x
            return min

