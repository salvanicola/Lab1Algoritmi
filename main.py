import gc
import logging
from numpy import average
from progress.bar import Bar

from graph import graph_generator, Graph
import matplotlib.pyplot as plt
import time
import glob
import math
from kruskal import kruskal
from kruskal_naive import kruskalNaive
from prim import prim
import re

numbers = re.compile(r'(\d+)')


###################################################
# --- ordino i grafi letti in maniera crescente ---
def numerical_sort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


####################################################

# Funzione per l'upload dei file di input data.
def upload_graph():
    gs = []
    for infile in sorted(glob.glob("mst_dataset/*.txt"), key=numerical_sort):
        gs.append(graph_generator(infile))
    return gs


# Dato numero di vertici e lati a calcola la complessità O(m*n) attesa per un grafico.
def mxn(a, b):
    return a * b


# Dato numero di vertici e lati a calcola la complessità O(log(n)*m) attesa per un grafico.
def mx_log_n(a, b):
    return math.log(a) * b


# Funzione che dati i tempi risultanti, array con numero di vertici, array con numero di archi, e l'algoritmo
# testato, restituisce il grafico con il riferimento calcolato dalle costanti.
def plotting_plot(t, vert, arches, fun):
    comp_fun = None
    if fun.__name__ == "prim" or fun.__name__ == "kruskal":
        comp_fun = mx_log_n
    elif fun.__name__ == "kruskalNaive":
        comp_fun = mxn
    else:
        raise Exception("nessuna funzione trovata con quel nome")
    # Calcolo un array con le complessità attese in base all'algoritmo selezionato.
    comp = [round(comp_fun(vert[i], arches[i]), 3) for i in range(len(vert))]
    # La costante é calcolata come la media del rapporto tra i tempi calcolati e la complessità calcolata dai vertici
    # e archi dei grafici.
    constant = [round((t[i] / comp[i]), 3) for i in range(len(comp))]
    constant = constant[(len(constant)//2):]
    # Calcola i valori del grafo di riferimento.
    references = [round(average(constant) * comp[i], 3) for i in range(len(comp))]
    plt.plot(vert, t)
    plt.plot(vert, references)
    plt.legend(["Tempo misurato", "Tempo approssimato"])
    plt.ylabel('Tempo di esecuzione')
    plt.xlabel('Numero di vertici')
    plt.title(fun.__name__.title())
    plt.show()


# Prende in input i risultati dei tre algoritmi e crea un grafico unico.
def plotting_multiple(t1, t2, t3, vert):
    plt.plot(vert, t1)
    plt.plot(vert, t2)
    if t3 is not None:
        plt.plot(vert, t3)
        plt.legend(["Prim", "Kruskal", "Kruskal naive"])
    else:
        plt.legend(["Prim", "Kruskal"])
    plt.ylabel('Tempo di esecuzione')
    plt.xlabel('Numero di vertici')
    plt.title('Comparazione algoritmi')
    plt.show()


# Prende in input l'array di grafi e l'algoritmo da testare ed esegue i test su ognuno di essi.
def testing(g, f, **args):
    times = []
    complexity = []
    arch_num = []
    current_instance = g[0].n_vertexes
    instance_list = []
    results = []
    # logger.debug("%s", f.__name__)
    bar = Bar('Processing ' + f.__name__.title(), max=len(g), check_tty=False)
    for x in g:
        bar.next()

        # Su i grafici da meno di 1000 vertici esegue 100 volte il test e ne fa la media per ottenere un risultato
        # più attendibile
        num_calls = 1
        if x.n_vertexes < 1000:
            num_calls = 100
        if x.n_vertexes != current_instance:
            update_data(instance_list, times, arch_num, complexity, current_instance)
        out = x

        # -----------------start-------------------
        gc.disable()
        start_time = time.perf_counter_ns()
        for i in range(num_calls):
            out = f(x, x.vert_list[0])
        stop_time = time.perf_counter_ns()
        gc.enable()
        # -----------------stop-------------------

        duration = stop_time - start_time
        # Raccolgo i dati dei tempi e del numero di archi in questo array
        instance_list.append([duration / num_calls, x.n_arches])
        current_instance = x.n_vertexes

        # Costruisco un array per visualizzare i risultati
        if f.__name__ == "prim":
            gr = Graph(len(out))
            for m in out:
                if m.parent is not None:
                    gr.add(m.parent.id, m.id, m.key)
            out = gr
        results.append(out.graph_total_weight())
        # logger.debug("%s", "{:.2e}".format(duration))
    bar.finish()
    update_data(instance_list, times, arch_num, complexity, current_instance)
    return times, complexity, arch_num, results


# Aggiorna i dati con tutti i risultati d'istanza.
def update_data(ins, tim, ar, comp, curr):
    avg_times = average([c[0] for c in ins])
    avg_arch = average([c[1] for c in ins])
    tim.append(avg_times)
    ar.append(avg_arch)
    comp.append(curr)


# Prende in input tutti i risultati di MST dei tre algoritmi, se sono uguali stampa su terminale la conferma del
# successo del programma.
def is_result_right(result1, result2, result3):
    if result1 == result2 and result2 == result3:
        logger.debug("I risultati sono corretti, perché tutti e tre gli algoritmi restuiscono lo stesso risultato")
    elif result1 != result2 and result2 == result3:
        logger.debug("Oh no! Prim restituisce i risultati sbagliati")
    elif result2 != result1 and result1 == result3:
        logger.debug("Oh no! Kruskal in versione naive restituisce i risultati sbagliati")
    elif result3 != result1 and result1 == result2:
        logger.debug("Oh no! Kruskal restituisce i risultati sbagliati")
    else:
        logger.debug("Oh no! Nessuno dei tre algoritmi resistuisce i risultati aspettati")


logger = logging.getLogger('tipper')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

if __name__ == '__main__':
    graphs = upload_graph()

    # Eseguo i test su tutti e tre gli algoritmi.
    times_p, complexity_p, arch_p, res1 = testing(graphs, prim)
    times_kn, complexity_kn, arch_kn, res2 = testing(graphs, kruskalNaive)
    times_k, complexity_k, arch_k, res3 = testing(graphs, kruskal)
    # Testo se i risultati sono corretti.
    is_result_right(res1, res2, res3)
    # Genero i grafici per ognuno degli algoritmi.
    plotting_plot(times_p, complexity_p, arch_p, prim)
    plotting_plot(times_kn, complexity_kn, arch_kn, kruskalNaive)
    plotting_plot(times_k, complexity_k, arch_k, kruskal)
    # Genero il grafico unico.
    plotting_multiple(times_p, times_k, times_kn, complexity_p)
    plotting_multiple(times_p, times_k, None, complexity_p)
