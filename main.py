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


def mxn(a, b):
    return a * b


def log_n_m_n(a, b):
    return math.log(a) * (a + b)


def log_n_m(a, b):
    return math.log(a) * b


def plotting_plot(t, vert, arches, fun):
    comp_fun = None
    if fun.__name__ == "prim":
        comp_fun = log_n_m_n
    elif fun.__name__ == "kruskalNaive":
        comp_fun = mxn
    elif fun.__name__ == "kruskal":
        comp_fun = log_n_m
    else:
        raise Exception("nessuna funzione trovata con quel nome")
    comp = [round(comp_fun(vert[i], arches[i]), 3) for i in range(len(vert))]
    constant = [round((t[i] / comp[i]), 3) for i in range(len(comp))]
    references = [round(average(constant) * comp[i], 3) for i in range(len(comp))]
    plt.plot(vert, t)
    plt.plot(vert, references)
    plt.legend(["Measure time", "ApproxTime"])
    plt.ylabel('Operation time')
    plt.xlabel('n')
    plt.title(fun.__name__.title())
    plt.show()


# prende in input i grafici e le funzioni ed esegue i test su ognuna
def testing(g, f, **args):
    times = []
    complexity = []
    arch_num = []
    current_instance = g[0].n_vertexes
    instance_list = []
    results = []
    bar = Bar('Processing ' + f.__name__.title(), max=len(g), check_tty=False)
    for x in g:
        bar.next()
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
            # function(x, x.vert_list[0])
            out = f(x, x.vert_list[0])
        stop_time = time.perf_counter_ns()
        gc.enable()
        # -----------------stop-------------------

        duration = stop_time - start_time
        instance_list.append([duration / num_calls, x.n_arches])
        current_instance = x.n_vertexes

        # costruisco un array per visualizzare i risultati
        if f.__name__.title() == "Prim":
            gr = Graph(len(out))
            for m in out:
                if m.parent is not None:
                    gr.add(m.parent.id, m.id, m.key)
            out = gr
        results.append(out.graph_total_weight())

    bar.finish()
    update_data(instance_list, times, arch_num, complexity, current_instance)
    return times, complexity, arch_num, results


# aggiorna i dati con tutti i risultati d'istanza
def update_data(ins, tim, ar, comp, curr):
    avg_times = average([c[0] for c in ins])
    avg_arch = average([c[1] for c in ins])
    tim.append(avg_times)
    ar.append(avg_arch)
    comp.append(curr)


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

    # eseguo i test sugli algoritmi
    times_p, complexity_p, arch_p, res1 = testing(graphs, prim)
    times_kn, complexity_kn, arch_kn, res2 = testing(graphs, kruskalNaive)
    times_k, complexity_k, arch_k, res3 = testing(graphs, kruskal)
    # testo se i risultati sono corretti
    is_result_right(res1, res2, res3)
    # genero i grafici per ognuno degli algoritmi
    plotting_plot(times_p, complexity_p, arch_p, prim)
    plotting_plot(times_kn, complexity_kn, arch_kn, kruskalNaive)
    plotting_plot(times_k, complexity_k, arch_k, kruskal)
