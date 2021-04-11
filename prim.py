import logging

import progressbar

from heap import FibonacciHeap, Node
from graph import Vertex
import time
from progress.bar import Bar


def prim(G, s):
    # Inizializzazione di una semplice progress bar per verificare l'operazione in corso.
    with progressbar.ProgressBar(G.n_vertexes) as bar:
        logger = logging.getLogger('tipper')
        logger.debug("ESEGUO prim su grafo con %s vertici e %s archi", G.n_vertexes, G.n_arches)
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

        initial_node_number = 0

        # Viene iterato un ciclo while, fino a che non vengono esauriti tutti gli elementi del Fibonacci Heap.
        while q.total_num_elements > 0:
            # u_id è l'indice di un light edge per l'algoritmo.
            u_id = q.extract_minimum()
            vert[u_id].flag = True
            v_vert = None
            # Vengono esaminati tutti i vertici adiacenti al vertice identificato da u_id.
            for v_arch in G.arch_list:
                if v_arch.vert1 == u_id:
                    v_vert = v_arch.vert2
                elif v_arch.vert2 == u_id:
                    v_vert = v_arch.vert1
                if v_vert is not None and vert[v_vert].flag is False and v_arch.weight < vert[v_vert].key:
                    # Se verificate le condizioni, il vertice viene inserito nel corretto indice della lista vert,
                    # diventando componente del MST da restituire a fine ciclo.
                    vert[v_vert].parent = nodes[u_id]
                    vert[v_vert].key = v_arch.weight
                    # Viene aggiornata la chiave del vertice all'interno del Fibonacci Heap con il valore dell'arco
                    # preso in esame.
                    q.decrease_key(nodes[v_vert], v_arch.weight)
            initial_node_number = initial_node_number + 1
            bar.update(initial_node_number)

    logger.debug("FINITO prim su grafo con %s vertici e %s archi.", G.n_vertexes, G.n_arches)

