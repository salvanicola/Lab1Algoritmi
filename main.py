# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
import gc
import logging
from numpy import average
from progress.bar import Bar

from graph import graph_generator, Graph
import matplotlib.pyplot as plt
import time
import glob
import math

from kruskal_naive import kruskalNaive
from prim import prim

###################
# mac fix
import re

numbers = re.compile(r'(\d+)')


def numerical_sort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


####################

# ho dovuto ordinare i file per nome (ty stefano lavori)
def upload_graph():
    # files = glob.glob("mst_dataset/*.txt")
    gs = []
    for infile in sorted(glob.glob("mst_dataset/*.txt"), key=numerical_sort):
        gs.append(graph_generator(infile))
    return gs


def mxn(a, b):
    return a * b


def log_n_m_n(a, b):
    return math.log(a) * (a + b)


def plotting_plot(t, vert, arches, fun):
    comp = [round(mxn(vert[i], arches[i]), 3) for i in range(len(vert))]
    constant = [round((t[i] / comp[i]), 3) for i in range(len(comp))]
    references = [round(average(constant) * comp[i], 3) for i in range(len(comp))]
    # logger.debug("references %s \n constant %s \n constants %s \n complexity %s \n vertexes %s \n arch %s \n times %s", references, average(constant), constant, comp, vert, arches, t)
    plt.plot(vert, t)
    plt.plot(vert, references)
    plt.legend(["Measure time", "ApproxTime"])
    plt.ylabel('Operation time')
    plt.xlabel('n')
    plt.title(fun.__name__.title())
    plt.show()
    logger.debug("plotted")


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


def update_data(ins, tim, ar, comp, curr):
    avg_times = average([c[0] for c in ins])
    avg_arch = average([c[1] for c in ins])
    tim.append(avg_times)
    ar.append(avg_arch)
    comp.append(curr)


def is_result_right(result1, result2):
    if result1 == result2:
        logger.debug("i risultati sono corretti")
    else:
        logger.debug("sgreva non sa programmare un cazzo")


logger = logging.getLogger('tipper')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

if __name__ == '__main__':
    graphs = upload_graph()
    function = kruskalNaive
    _, _, _, res1 = testing(graphs, prim)
    times, complexity, arch, res2 = testing(graphs, function)
    is_result_right(res1, res2)
    plotting_plot(times, complexity, arch, function)
